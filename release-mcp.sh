#!/usr/bin/env bash
# release-mcp — Build, push, and roll out a new etc-platform MCP image.
# Usage:
#   ./release-mcp.sh v3.1.0                        # build + push (no team-config bump)
#   ./release-mcp.sh v3.1.0 --bump-team            # also update team-ai-config + git push
#   ./release-mcp.sh v3.1.0 --bump-team --yes      # non-interactive (skip confirmations)
#
# Env overrides:
#   NAMESPACE=<dockerhub-ns>   (default: o0mrblack0o)
#   TEAM_REPO=<path>           (default: $HOME/dev/team-ai-config — adjust per machine)

set -euo pipefail

VERSION="${1:-}"
BUMP_TEAM=0
YES=0
shift || true
while [ $# -gt 0 ]; do
  case "$1" in
    --bump-team) BUMP_TEAM=1 ;;
    --yes|-y)    YES=1 ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
  shift
done

NAMESPACE="${NAMESPACE:-o0mrblack0o}"
TEAM_REPO="${TEAM_REPO:-$HOME/dev/team-ai-config}"
BUILD_CTX="$(cd "$(dirname "$0")" && pwd)"

# ─── colors ────────────────────────────────────────────────────────────
if [ -t 1 ]; then BOLD='\033[1m'; GREEN='\033[32m'; YELLOW='\033[33m'; RED='\033[31m'; RESET='\033[0m'
else BOLD=''; GREEN=''; YELLOW=''; RED=''; RESET=''; fi
info() { echo -e "${BOLD}▶${RESET} $*"; }
ok()   { echo -e "  ${GREEN}✓${RESET} $*"; }
warn() { echo -e "  ${YELLOW}⚠${RESET} $*"; }
err()  { echo -e "  ${RED}✗${RESET} $*" >&2; }

# ─── validate ──────────────────────────────────────────────────────────
if [ -z "$VERSION" ]; then
  err "Usage: $0 vX.Y.Z [--bump-team] [--yes]"
  exit 1
fi
if [[ ! "$VERSION" =~ ^v[0-9]+\.[0-9]+\.[0-9]+(-[A-Za-z0-9.]+)?$ ]]; then
  err "Version must be 'vMAJOR.MINOR.PATCH' (e.g. v3.1.0). Got: $VERSION"
  exit 1
fi

IMAGE="${NAMESPACE}/etc-platform"
IMAGE_VER="${IMAGE}:${VERSION}"
IMAGE_LATEST="${IMAGE}:latest"

if [ ! -f "$BUILD_CTX/Dockerfile" ]; then
  err "Dockerfile not found at $BUILD_CTX — run from etc-platform source root"
  exit 1
fi

docker info >/dev/null 2>&1 || { err "Docker daemon not running"; exit 1; }

# ─── confirm ───────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}Release Plan${RESET}"
echo "  Image      : $IMAGE_VER + :latest"
echo "  Build ctx  : $BUILD_CTX"
if [ "$BUMP_TEAM" = 1 ]; then
  echo "  Bump team  : Yes (-> $TEAM_REPO/mcp/etc-platform/.env.example)"
else
  echo "  Bump team  : No"
fi
echo ""

if [ "$YES" != 1 ]; then
  read -p "Proceed? (y/N) " yn
  [[ "$yn" =~ ^[Yy] ]] || { echo "Aborted."; exit 0; }
fi

# ─── build + push (multi-arch via buildx) ─────────────────────────────
info "Building + pushing multi-arch ($IMAGE_VER + :latest, linux/amd64 + linux/arm64)"
if ! docker buildx build \
    --platform linux/amd64,linux/arm64 \
    -t "$IMAGE_VER" \
    -t "$IMAGE_LATEST" \
    --push \
    "$BUILD_CTX"; then
  err "buildx push failed - Did you 'docker login'? (token: app.docker.com/settings/personal-access-tokens)"
  err "Or buildx not enabled? Run: docker buildx create --use"
  exit 1
fi
ok "Pushed multi-arch manifest: $IMAGE_VER + :latest"

# ─── bump team-ai-config (optional) ────────────────────────────────────
if [ "$BUMP_TEAM" = 1 ]; then
  if [ ! -d "$TEAM_REPO" ]; then
    warn "team-ai-config repo not found at $TEAM_REPO — skip bump (set TEAM_REPO env to override)"
  else
    info "Bumping team-ai-config to $VERSION"
    ENV_FILE="$TEAM_REPO/mcp/etc-platform/.env.example"
    if [ ! -f "$ENV_FILE" ]; then
      err "Not found: $ENV_FILE"
      exit 1
    fi
    if grep -q "ETC_PLATFORM_IMAGE=$IMAGE_VER" "$ENV_FILE"; then
      ok ".env.example already at $VERSION"
    else
      # Cross-platform sed: write to temp file
      tmpfile=$(mktemp)
      sed -E "s|^ETC_PLATFORM_IMAGE=.*|ETC_PLATFORM_IMAGE=$IMAGE_VER|" "$ENV_FILE" > "$tmpfile"
      mv "$tmpfile" "$ENV_FILE"
      ok "Updated $ENV_FILE"
    fi

    cd "$TEAM_REPO"
    if git diff --quiet; then
      ok 'No changes to commit (env already pinned)'
    else
      git add mcp/etc-platform/.env.example
      git commit -m "Bump MCP image to $VERSION"
      git push
      ok "team-ai-config pushed"
    fi
    cd - >/dev/null
  fi
fi

# ─── done ──────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}${GREEN}✅ Released $IMAGE_VER${RESET}"
echo ""
echo "Team rollout:"
if [ "$BUMP_TEAM" = 1 ]; then
  echo "  Team: ai-kit update    (will pull new image + restart)"
else
  echo "  1. Bump team-ai-config/mcp/etc-platform/.env.example -> ETC_PLATFORM_IMAGE=$IMAGE_VER"
  echo "  2. cd team-ai-config && git add . && git commit -m \"Bump MCP $VERSION\" && git push"
  echo "  3. Team: ai-kit update"
  echo ""
  echo "  (or re-run with --bump-team to do steps 1-2 automatically)"
fi
