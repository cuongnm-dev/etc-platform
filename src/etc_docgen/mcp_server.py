"""etc-docgen MCP Server — expose documentation tools via Model Context Protocol.

Allows AI agents in any MCP-compatible IDE (VS Code, Cursor, Claude Desktop,
Windsurf, etc.) to call etc-docgen tools directly without subprocess CLI parsing.

Tools exposed:
  - validate:       validate content-data.json against Pydantic schema
  - export:         render Office files from content-data.json
  - schema:         get JSON Schema for content-data.json
  - section_schema: get schema for a specific doc type (saves tokens)
  - merge_content:  deep-merge partial JSON into content-data.json
  - field_map:      get interview-to-field mapping for a doc type
  - template_list:  list bundled templates with sizes
  - template_fork:  fork an ETC template with Jinja2 tags

Resources exposed:
  - schema://content-data  → JSON Schema for content-data.json

Transports:
  - stdio (default): for local IDE integration
  - sse: for remote/Docker deployment (HTTP + Server-Sent Events)
  - streamable-http: newer HTTP-based MCP transport

Usage:
  # stdio transport (default for IDE integration)
  python -m etc_docgen.mcp_server

  # SSE transport (for Docker / remote)
  python -m etc_docgen.mcp_server --transport sse --host 0.0.0.0 --port 8000

  # or via etc-docgen CLI
  etc-docgen mcp
  etc-docgen mcp --transport sse --port 8000
"""

from __future__ import annotations

import copy
import json
import logging
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from etc_docgen.paths import template, templates_dir

log = logging.getLogger("etc-docgen.mcp")

# ---------------------------------------------------------------------------
# DoD whitelist — warnings matching these substrings do NOT block dod_met.
# Specialists must not loop trying to fix these; they are expected/acceptable.
# Orchestrator Phase 3.5 validate() still sees them for reporting purposes.
# ---------------------------------------------------------------------------
_DOD_WHITELIST_PATTERNS: tuple[str, ...] = (
    "priority_distribution",       # noisy stats field — not actionable by specialists
    "features_without_test_cases", # expected before xlsx specialist (03f) runs
    "flow_diagram",                # optional TKCT module diagrams — may be skipped
    "tkcs.pm_method",              # TKCS Section 10 — business-only, BA must fill
    "tkcs.stakeholders",           # TKCS Section 11 — business-only, BA must fill
    "tkcs.budget",                 # TKCS Section 10 — business-only
    "tkcs.procurement",            # TKCS Section 10 — business-only
    "expansion_gap",               # Phase 3g logged gap — intel source incomplete
)


def _is_whitelisted(warning: str) -> bool:
    """Return True if this warning is on the DoD whitelist (should not block dod_met)."""
    return any(pat in warning for pat in _DOD_WHITELIST_PATTERNS)

mcp = FastMCP(
    "etc-docgen",
    instructions=(
        "etc-docgen is a template-first documentation generator for Vietnamese "
        "government IT projects. It turns structured data into standardized "
        "documents (HDSD, TKKT, TKCS, TKCT, Test Cases) via a content-data.json "
        "intermediate format.\n\n"
        "## Specialist write + feedback loop (PRIMARY workflow)\n\n"
        "Each doc-writer specialist follows this loop until DoD is met:\n\n"
        "  1. section_schema(doc_type) → receive schema + minimums + banned_phrases\n"
        "  2. Produce JSON matching schema fields (Vietnamese prose, specific facts)\n"
        "  3. merge_content(path, json, auto_validate=True)\n"
        "     → returns {success, validation: {errors[], warnings[], dod_met, action_required}}\n"
        "  4. If dod_met=false → read every warning in warnings[] → fix content → go to step 3\n"
        "     Note: warnings_whitelisted[] are informational only — do NOT try to fix them.\n"
        "  5. Loop exits when dod_met=true (errors:[] AND blocking warnings:[] — whitelisted OK)\n"
        "  6. export(path, out, targets) → render Office files (Phase 4 only)\n\n"
        "## Key rule: do NOT call validate() separately\n\n"
        "merge_content(auto_validate=True) runs full validation inline and returns "
        "feedback in the same response. Calling validate() as a separate step wastes "
        "one round-trip. Only call validate() for the final cross-block check in "
        "Phase 3.5 quality gate (orchestrator role, not specialist role).\n\n"
        "## Warning routing\n\n"
        "merge_content returns warnings for ALL blocks. Route to owning specialist:\n"
        "  architecture.* → tkkt | tkcs.* → tkcs | tkct.* → tkct\n"
        "  test_cases.*   → xlsx | [F-NNN].* → xlsx | diagrams.* → shared\n\n"
        "## Definition of Done\n\n"
        "dod_met:true = errors:[] AND blocking warnings:[] (whitelisted warnings do not block).\n"
        "Whitelisted patterns: priority_distribution, features_without_test_cases (before xlsx),\n"
        "  flow_diagram (optional TKCT modules), tkcs.pm_method/stakeholders/budget/procurement\n"
        "  (business-only fields BA must fill), expansion_gap (Phase 3g logged sections).\n"
        "These appear in warnings_whitelisted[] — informational only, no action needed.\n\n"
        "Tools: validate, export, schema, section_schema, merge_content, "
        "template_list, template_fork."
    ),
)


# ─────────────────────────── Path safety ───────────────────────────

# Base allowed root: /data Docker mount.
# Add extra roots via ETC_DOCGEN_EXTRA_ROOTS env var (colon-separated) for local dev/testing.
_ALLOWED_ROOTS: list[Path] = [Path("/data")]
if _extra := os.environ.get("ETC_DOCGEN_EXTRA_ROOTS", ""):
    _ALLOWED_ROOTS.extend(Path(r) for r in _extra.split(os.pathsep) if r)


def _resolve_data_path(raw: str, *, must_exist: bool = False, allow_write: bool = False) -> Path:
    """Resolve and contain a caller-supplied path to allowed roots.

    Prevents path traversal (../../etc/passwd) and restricts writes
    to /data mount only.

    Raises:
        ValueError: if path escapes allowed roots.
        FileNotFoundError: if must_exist=True and path not found.
    """
    try:
        path = Path(raw).resolve()
    except Exception as exc:
        raise ValueError(f"Invalid path '{raw}': {exc}") from exc

    # Check containment — both reads and writes MUST stay within allowed roots.
    # Use Path.is_relative_to (PurePath semantics) to avoid prefix-string false positives
    # like "/data2/foo" matching "/data".
    def _is_contained(p: Path) -> bool:
        for root in _ALLOWED_ROOTS:
            try:
                root_resolved = root.resolve()
            except Exception:
                root_resolved = root
            try:
                if p.is_relative_to(root_resolved):
                    return True
            except AttributeError:  # pragma: no cover — Python < 3.9
                if str(p).startswith(str(root_resolved) + os.sep) or p == root_resolved:
                    return True
        return False

    if not _is_contained(path):
        verb = "Write" if allow_write else "Read"
        raise ValueError(
            f"{verb} path '{raw}' is outside allowed roots "
            f"({[str(r) for r in _ALLOWED_ROOTS]}). "
            "Use /data/{project-slug}/... paths. "
            "The MCP server runs in Docker: D:\\Projects\\etc-docgen\\data\\ → /data/"
        )

    if must_exist and not path.exists():
        raise FileNotFoundError(f"Path not found: {raw}")

    return path


# ─────────────────────────── Resources ───────────────────────────


@mcp.resource("schema://content-data")
def get_content_data_schema() -> str:
    """JSON Schema for content-data.json — the contract between agents and engines."""
    from etc_docgen.data.models import ContentData

    schema = ContentData.model_json_schema()
    return json.dumps(schema, indent=2, ensure_ascii=False)


# ─────────────────────────── Tools ───────────────────────────


@mcp.tool()
def validate(content_data: dict) -> str:
    """Validate content_data dict against Pydantic schema + quality checks.

    Pure API mode — NO filesystem access. Suitable for multi-user hosted MCP deploy.

    Returns validation result with errors, warnings, stats, and elapsed time.

    Args:
        content_data: Full content-data dict (per `schema()` tool's structure).
            Pass the whole document state; partial validation is not supported.
    """
    from etc_docgen.data.validation import validate_content_data

    t0 = time.monotonic()
    log.info("validate called: keys=%d", len(content_data) if content_data else 0)

    if not isinstance(content_data, dict):
        return json.dumps({
            "valid": False,
            "errors": ["content_data must be a JSON object/dict"],
            "error_code": "INVALID_ARGS",
        })

    result = validate_content_data(content_data)
    elapsed = round(time.monotonic() - t0, 3)
    log.info("validate done: valid=%s errors=%d elapsed=%.3fs",
             result.valid, len(result.errors), elapsed)
    payload = result.to_dict()
    payload["elapsed_s"] = elapsed
    return json.dumps(payload, ensure_ascii=False, indent=2)


def _run_export_job(
    name: str,
    spec: dict,
    tpl_path: Path,
    data_file: Path,
    out_dir: Path,
    screenshots_dir: str | None,
    diagrams_dir: str | None,
) -> dict:
    """Execute a single export job — safe to call from a thread pool."""
    from etc_docgen.engines import docx as docx_engine
    from etc_docgen.engines import xlsx as xlsx_engine
    from etc_docgen.paths import schema as schema_path

    output_path = out_dir / spec["output"]
    try:
        if spec["engine"] == "xlsx":
            report = xlsx_engine.fill(
                tpl_path,
                schema_path("test-case.xlsx.schema.yaml"),
                data_file,
                output_path,
            )
            return {
                "target": name,
                "success": not report.validator_failures,
                "output": str(output_path),
                "warnings": report.validator_failures[:5] if report.validator_failures else [],
            }
        ss_dir = Path(screenshots_dir) if screenshots_dir and name == "hdsd" else None
        if ss_dir and not ss_dir.exists():
            ss_dir = None
        dg_dir = Path(diagrams_dir) if diagrams_dir else None
        if dg_dir and not dg_dir.exists():
            dg_dir = None
        report = docx_engine.render(
            tpl_path,
            data_file,
            output_path,
            screenshots_dir=ss_dir,
            diagrams_dir=dg_dir,
        )
        return {
            "target": name,
            "success": not report.errors,
            "output": str(output_path),
            "screenshots_embedded": report.screenshots_embedded,
            "screenshots_missing": report.screenshots_missing,
            "warnings": report.warnings[:5],
            "errors": report.errors[:5],
        }
    except Exception as e:
        return {"target": name, "success": False, "error": str(e)}


@mcp.tool()
def export(
    content_data: dict,
    screenshots: dict | None = None,
    targets: list[str] | None = None,
    auto_render_mermaid: bool = True,
) -> str:
    """Render Office files from inline content_data. Pure API mode.

    Produces up to 5 files (returned as base64-encoded blobs in `outputs`):
      - kich-ban-kiem-thu.xlsx  (test cases)
      - huong-dan-su-dung.docx (user manual — HDSD)
      - thiet-ke-kien-truc.docx (architecture design — TKKT)
      - thiet-ke-co-so.docx (basic design — TKCS)
      - thiet-ke-chi-tiet.docx (detailed design — TKCT)

    Auto-renders diagrams declared in `content_data.diagrams` (SVG hero + Mermaid)
    inside server temp dir before DOCX fill. Supported entry forms:
      - Mermaid (string):   "arch": "graph TD\\n..."
      - SVG hero (dict):    "T1": {"template": "kien-truc-4-lop", "data": {...}}
        Available SVG templates: kien-truc-4-lop (T1), ndxp-hub-spoke (T2),
        swimlane-workflow (T3).

    Size limits (MCP message bounds):
      - content_data:  recommend ≤ 1 MB (≤ 30 features typical)
      - screenshots:   recommend ≤ 20 MB total base64 (≤ 100 images @ 200 KB each)
      - outputs returned: ≤ 25 MB total base64 (5 docx + 1 xlsx typically 5-15 MB)
      - For larger projects: split into multiple export calls per target,
        OR contact MCP admin to enable session-based upload protocol (future).

    Args:
        content_data: Full content-data dict (per `schema()` structure).
        screenshots: Optional `{filename: base64_string}` dict for HDSD images.
            Filenames must be plain (no `/`, `\\`, `..`).
        targets: Which docs to export. Options: xlsx, hdsd, tkkt, tkcs, tkct.
            Default: all 5.
        auto_render_mermaid: If True (default), render `content_data.diagrams`
            into PNG before DOCX fill. Set False to skip.

    Returns JSON with:
        success: bool
        outputs: {filename: base64_string} for each successfully rendered file
        targets: per-target status report (incl. screenshots_embedded counts)
        diagrams: diagram render report
        elapsed_s: float
    """
    import base64
    import tempfile

    t0 = time.monotonic()
    log.info("export called: content_keys=%s targets=%s screenshots=%d",
             list(content_data.keys()) if content_data else None,
             targets,
             len(screenshots) if screenshots else 0)

    if not isinstance(content_data, dict):
        return json.dumps({"success": False, "error": "content_data must be a dict"})

    # Validate screenshots dict
    if screenshots is not None:
        if not isinstance(screenshots, dict):
            return json.dumps({"success": False, "error": "screenshots must be a dict {filename: base64}"})
        for fn in screenshots.keys():
            if not isinstance(fn, str) or "/" in fn or "\\" in fn or ".." in fn:
                return json.dumps({"success": False, "error": f"Invalid screenshot filename: {fn!r}"})

    target_set = set(targets or ["xlsx", "hdsd", "tkkt", "tkcs", "tkct"])

    # Use server-side temp dir for the rendering session
    with tempfile.TemporaryDirectory(prefix="etc-docgen-export-") as tmp:
        tmp_path = Path(tmp)
        data_file = tmp_path / "content-data.json"
        data_file.write_text(json.dumps(content_data, ensure_ascii=False, indent=2), encoding="utf-8")

        # Decode screenshots to temp dir
        screenshots_dir = None
        if screenshots:
            ss_dir = tmp_path / "screenshots"
            ss_dir.mkdir()
            for filename, b64 in screenshots.items():
                try:
                    (ss_dir / filename).write_bytes(base64.b64decode(b64))
                except Exception as e:
                    return json.dumps({"success": False, "error": f"Invalid base64 for {filename}: {e}"})
            screenshots_dir = str(ss_dir)

        out_dir = tmp_path / "output"
        out_dir.mkdir()

        # Auto-render diagrams from content_data.diagrams
        diagrams_dir = None
        diagram_report = None
        if auto_render_mermaid and content_data.get("diagrams"):
            try:
                from etc_docgen.engines import diagram as diagram_engine
                render_dir = out_dir / "diagrams"
                dr = diagram_engine.render_all(content_data, render_dir)
                diagram_report = dr.to_dict()
                if dr.rendered:
                    diagrams_dir = str(render_dir)
            except Exception as e:
                diagram_report = {"status": "failed", "error": f"{type(e).__name__}: {e}"}

        jobs = {
            "xlsx": {
                "template": "test-case.xlsx",
                "output": "kich-ban-kiem-thu.xlsx",
                "engine": "xlsx",
            },
            "hdsd": {
                "template": "huong-dan-su-dung.docx",
                "output": "huong-dan-su-dung.docx",
                "engine": "docx",
            },
            "tkkt": {
                "template": "thiet-ke-kien-truc.docx",
                "output": "thiet-ke-kien-truc.docx",
                "engine": "docx",
            },
            "tkcs": {
                "template": "thiet-ke-co-so.docx",
                "output": "thiet-ke-co-so.docx",
                "engine": "docx",
            },
            "tkct": {
                "template": "thiet-ke-chi-tiet.docx",
                "output": "thiet-ke-chi-tiet.docx",
                "engine": "docx",
            },
        }

        # Resolve template paths eagerly (fail-fast before spawning threads)
        active_jobs: dict[str, tuple[dict, Path]] = {}
        results: list = []
        for name, spec in jobs.items():
            if name not in target_set:
                continue
            try:
                tpl_path = template(spec["template"])
            except FileNotFoundError:
                results.append({"target": name, "success": False, "error": "Template not found"})
                continue
            active_jobs[name] = (spec, tpl_path)

        # Run export jobs in parallel
        with ThreadPoolExecutor(max_workers=max(len(active_jobs), 1)) as executor:
            futures = {
                executor.submit(
                    _run_export_job,
                    name,
                    spec,
                    tpl_path,
                    data_file,
                    out_dir,
                    screenshots_dir,
                    diagrams_dir,
                ): name
                for name, (spec, tpl_path) in active_jobs.items()
            }
            for future in as_completed(futures):
                results.append(future.result())

        # ── Read rendered outputs into base64 (BEFORE temp dir cleanup) ──
        outputs: dict[str, str] = {}
        outputs_meta: dict[str, dict] = {}
        for r in results:
            if not r.get("success"):
                continue
            output_path_str = r.get("output")
            if not output_path_str:
                continue
            output_path = Path(output_path_str)
            if not output_path.exists():
                continue
            try:
                blob = output_path.read_bytes()
                outputs[output_path.name] = base64.b64encode(blob).decode("ascii")
                outputs_meta[output_path.name] = {
                    "size_bytes": len(blob),
                    "target": r["target"],
                }
            except Exception as e:
                log.warning("Failed reading output %s: %s", output_path, e)

        all_ok = all(r["success"] for r in results)
        elapsed = round(time.monotonic() - t0, 3)
        total_b64_mb = sum(len(v) for v in outputs.values()) / (1024 * 1024)
        log.info("export done: success=%s targets=%d outputs=%d total_b64=%.2fMB elapsed=%.3fs",
                 all_ok, len(results), len(outputs), total_b64_mb, elapsed)

        payload = {
            "success": all_ok,
            "outputs": outputs,
            "outputs_meta": outputs_meta,
            "targets": results,
            "elapsed_s": elapsed,
        }
        if diagram_report is not None:
            payload["diagrams"] = diagram_report
        return json.dumps(payload, ensure_ascii=False, indent=2)


@mcp.tool()
def schema() -> str:
    """Get the full JSON Schema for content-data.json.

    Use this to understand the exact format agents must produce.
    The schema defines all fields for HDSD, TKKT, TKCS, TKCT and test case data.
    """
    from etc_docgen.data.models import ContentData

    return json.dumps(
        ContentData.model_json_schema(),
        indent=2,
        ensure_ascii=False,
    )


@mcp.tool()
def section_schema(doc_type: str) -> str:
    """Get the JSON Schema for a specific document type — saves tokens vs full schema.

    Returns only the relevant Pydantic model schema for the target document type,
    plus shared models (project, meta, overview) needed as context.

    This is the recommended first call for doc-writer agents: get the schema for
    the section you need to fill, understand the fields, then produce JSON.

    Args:
        doc_type: Target document type. Options:
            - tkcs: Thiết kế cơ sở (NĐ 45/2026 Điều 13)
            - tkct: Thiết kế chi tiết
            - tkkt: Thiết kế kiến trúc
            - hdsd: Hướng dẫn sử dụng
            - xlsx: Kịch bản kiểm thử (test cases)
    """
    from etc_docgen.data.models import (
        Architecture,
        Feature,
        Meta,
        Overview,
        ProjectInfo,
        Service,
        TestCases,
        TestSheetConfig,
        TkcsData,
        TkctData,
        TroubleshootingItem,
    )

    # Map doc type → primary models + which content-data keys to fill
    type_map: dict[str, dict] = {
        "tkcs": {
            "primary_model": TkcsData,
            "support_models": [ProjectInfo, Meta, Overview],
            "content_data_keys": ["project", "meta", "overview", "tkcs"],
            "description": (
                "TKCS (Thiết kế cơ sở) — NĐ 45/2026 Điều 13. "
                "Fill tkcs.* fields with formal Vietnamese prose. "
                "Reuse project/meta/overview from shared context."
            ),
        },
        "tkct": {
            "primary_model": TkctData,
            "support_models": [ProjectInfo, Meta, Overview],
            "content_data_keys": ["project", "meta", "overview", "tkct"],
            "description": (
                "TKCT (Thiết kế chi tiết). Fill tkct.* with detailed design: "
                "modules, db_tables, api_details, screens, integration, security."
            ),
        },
        "tkkt": {
            "primary_model": Architecture,
            "support_models": [ProjectInfo, Meta, Overview],
            "content_data_keys": ["project", "meta", "overview", "architecture"],
            "description": (
                "TKKT (Thiết kế kiến trúc). Fill architecture.* with: "
                "tech_stack, components, data_entities, apis, deployment, security, nfr."
            ),
        },
        "hdsd": {
            "primary_model": Service,
            "support_models": [ProjectInfo, Meta, Overview, Feature, TroubleshootingItem],
            "content_data_keys": ["project", "meta", "overview", "services", "troubleshooting"],
            "description": (
                "HDSD (Hướng dẫn sử dụng). Fill services[].features[] with steps, "
                "ui_elements, dialogs, error_cases. Also fill troubleshooting[]."
            ),
        },
        "xlsx": {
            "primary_model": TestCases,
            "support_models": [ProjectInfo, Meta, TestSheetConfig],
            "content_data_keys": ["project", "meta", "dev_unit", "test_cases", "test_sheets"],
            "description": (
                "Test cases (xlsx). Fill test_cases.ui[] and test_cases.api[] "
                "with feature_group, section_header, and test_case rows. "
                "Also fill dev_unit (đơn vị phát triển) and test_sheets labels if needed."
            ),
        },
    }

    if doc_type not in type_map:
        return json.dumps(
            {"error": f"Unknown doc_type: {doc_type}. Options: {list(type_map.keys())}"}
        )

    spec = type_map[doc_type]
    primary_schema = spec["primary_model"].model_json_schema()
    support_schemas = {m.__name__: m.model_json_schema() for m in spec["support_models"]}

    # Diagrams contract — applies to tkkt/tkcs/tkct. The *_diagram fields inside
    # architecture/tkcs/tkct are FILENAME REFERENCES; raw Mermaid source goes in
    # the top-level ContentData.diagrams dict keyed by the same name. Engine
    # auto-renders diagrams.{key} → {key}.png, then docxtpl InlineImage reads
    # the filename-reference field. Without this info, agents routinely put
    # Mermaid source directly into the *_diagram field, which crashes docxtpl.
    diagrams_contract = None
    if doc_type in ("tkkt", "tkcs", "tkct"):
        required_keys_map = {
            "tkkt": [
                "architecture_diagram", "logical_diagram", "data_diagram",
                "integration_diagram", "deployment_diagram", "security_diagram",
            ],
            "tkcs": ["tkcs_architecture_diagram", "tkcs_data_model_diagram"],
            "tkct": [
                "tkct_architecture_overview_diagram", "tkct_db_erd_diagram",
                "tkct_ui_layout_diagram", "tkct_integration_diagram",
                "{module_slug}_flow_diagram (per module)",
            ],
        }
        diagrams_contract = {
            "rule": (
                "TWO-FIELD PATTERN: *_diagram fields in this block are FILENAME "
                "REFERENCES ONLY (e.g. 'architecture_diagram.png'). Raw Mermaid "
                "source goes in top-level ContentData.diagrams[{key}]. Engine "
                "auto-renders Mermaid → PNG; docxtpl reads the filename."
            ),
            "correct_example": {
                "diagrams": {
                    "architecture_diagram": "flowchart LR\n  Web --> API\n  API --> DB"
                },
                "architecture": {
                    "architecture_diagram": "architecture_diagram.png"
                },
            },
            "wrong_example": {
                "architecture": {
                    "architecture_diagram": "```mermaid\nflowchart LR\n  Web --> API\n```"
                },
                "why_wrong": (
                    "docxtpl tries InlineImage('```mermaid...') → crash/blank. "
                    "Also: never use ```mermaid fences — raw source only."
                ),
            },
            "required_diagram_keys": required_keys_map[doc_type],
            "merge_content_note": (
                "Call merge_content TWICE or merge both blocks in one call: "
                "partial_json={'diagrams': {...Mermaid source...}, "
                f"'{ 'architecture' if doc_type=='tkkt' else doc_type }': "
                "{..., '*_diagram': '*.png'}}. Do NOT manually render PNG — "
                "export() auto-renders via mmdc CLI."
            ),
            "svg_hero_option": (
                "For 3 hero keys (architecture_diagram, integration_diagram, "
                "tkct_integration_diagram), diagrams.{key} may be a dict "
                "{template, data} instead of Mermaid string. Templates: "
                "'kien-truc-4-lop', 'ndxp-hub-spoke', 'swimlane-workflow'."
            ),
        }

    # Minimums contract — quantity + semantic rules enforced by validate().
    minimums = None
    try:
        from etc_docgen.data.quality_checks import MINIMUMS, BANNED_PHRASES
        minimums = MINIMUMS.get(doc_type)
        banned_list = BANNED_PHRASES
    except Exception:
        banned_list = []

    return json.dumps(
        {
            "doc_type": doc_type,
            "description": spec["description"],
            "content_data_keys": spec["content_data_keys"],
            "primary_schema": primary_schema,
            "support_schemas": support_schemas,
            "diagrams_contract": diagrams_contract,
            "minimums": minimums,
            "banned_phrases": banned_list,
            "enforcement_note": (
                "These rules are checked by validate(). Warnings are advisory "
                "(non-blocking) but agents SHOULD fix them before export. "
                "Run validate(path) after merge_content to see violations."
            ),
        },
        indent=2,
        ensure_ascii=False,
    )


@mcp.tool()
def merge_content(
    current_data: dict,
    partial: dict,
    auto_validate: bool = True,
) -> str:
    """Deep-merge partial content into current_data. Pure API mode.

    Returns the new merged_data dict so caller can persist + chain. NO filesystem I/O.

    Deep merge semantics:
      - nested dicts → merge recursively
      - lists → replaced (not appended)
      - scalar values → overwritten by partial

    With auto_validate=True (default), runs quality checks on the merged result and
    returns warnings/errors inline.

    Workflow (typical orchestrator loop):
      1. current = {}
      2. for each block (shared, tkkt, tkcs, tkct, hdsd, xlsx):
           result = merge_content(current_data=current, partial=block_dict)
           current = result["merged_data"]
           if result["validation"]["dod_met"]: continue
           else: agent fixes warnings, re-merges
      3. final current passed to export()

    Args:
        current_data: Current document state. Pass `{}` for first merge.
        partial: Partial content to merge in (JSON object).
            Example: {"tkcs": {"legal_basis": "...", "necessity": "..."}}
        auto_validate: If True (default), run quality checks after merge.
            Set False only for first-pass skeleton drafts.
    """
    t0 = time.monotonic()
    log.info("merge_content called: auto_validate=%s", auto_validate)

    if not isinstance(current_data, dict):
        return json.dumps({"success": False, "error": "current_data must be a dict (use {} for first merge)"})
    if not isinstance(partial, dict):
        return json.dumps({"success": False, "error": "partial must be a dict"})

    # Deep merge helper — produces new dict, never mutates caller inputs.
    def _deep_merge(base: dict, patch: dict) -> dict:
        out = copy.deepcopy(base)
        for k, v in patch.items():
            if k in out and isinstance(out[k], dict) and isinstance(v, dict):
                out[k] = _deep_merge(out[k], v)
            else:
                out[k] = copy.deepcopy(v)
        return out

    merged = _deep_merge(current_data, partial)

    partial_keys = list(partial.keys())
    total_keys = list(merged.keys())
    elapsed = round(time.monotonic() - t0, 3)
    log.info("merge_content done: keys=%s elapsed=%.3fs", partial_keys, elapsed)

    response: dict = {
        "success": True,
        "merged_data": merged,
        "merged_keys": partial_keys,
        "total_keys": total_keys,
        "elapsed_s": elapsed,
    }

    # ── Auto-validate: run quality checks on merged content ──────────────────
    if auto_validate:
        try:
            from etc_docgen.data.validation import validate_content_data

            vr = validate_content_data(merged)

            # Filter warnings to those blocks touched by this merge (keeps noise low)
            # If no warnings, show empty list. If warnings exist, show all (cross-block
            # issues are relevant context too).
            # Split warnings into blocking vs whitelisted
            blocking_warnings = [w for w in vr.warnings if not _is_whitelisted(w)]
            whitelisted_warnings = [w for w in vr.warnings if _is_whitelisted(w)]
            _dod_met = vr.valid and len(vr.errors) == 0 and len(blocking_warnings) == 0

            if vr.errors:
                _action = "FIX ERRORS before export."
            elif blocking_warnings:
                _action = "Fix blocking warnings then re-merge."
            elif whitelisted_warnings:
                _action = (
                    "DoD met — whitelisted warnings only (no action needed): "
                    + "; ".join(whitelisted_warnings[:3])
                    + ("..." if len(whitelisted_warnings) > 3 else "")
                )
            else:
                _action = "DoD met — this block is done."

            response["validation"] = {
                "valid": vr.valid,
                "errors": vr.errors,                  # blocking — must fix
                "warnings": blocking_warnings,         # must fix before export
                "warnings_whitelisted": whitelisted_warnings,  # informational only
                "quality_warnings_count": len(blocking_warnings),
                "stats": {
                    k: v for k, v in vr.stats.items()
                    if k not in ("priority_distribution",)  # omit noisy stats
                },
                "dod_met": _dod_met,
                "action_required": _action,
            }
            log.info(
                "merge_content auto_validate: valid=%s errors=%d warnings=%d (blocking=%d whitelisted=%d) dod_met=%s",
                vr.valid, len(vr.errors), len(vr.warnings),
                len(blocking_warnings), len(whitelisted_warnings), _dod_met,
            )
        except Exception as e:
            response["validation"] = {"error": f"auto_validate failed: {e}"}

    return json.dumps(response, ensure_ascii=False, indent=2)


@mcp.tool()
def field_map(doc_type: str) -> str:
    """Get the interview-to-field mapping for a doc type.

    Returns a structured reference showing which interview questions/data
    map to which content-data.json fields, organized by field type
    (prose, structured, diagram).

    Use this to understand HOW to fill content-data.json from interview/DCB data.
    Complements section_schema which shows WHAT fields exist.

    Args:
        doc_type: Target document type (tkcs, tkct, tkkt, hdsd)
    """
    from etc_docgen.integrations.field_maps import (
        get_field_map,
        get_writer_prompt_context,
        uses_docgen,
    )

    if not uses_docgen(doc_type):
        return json.dumps(
            {
                "doc_type": doc_type,
                "renderer": "pandoc",
                "message": f"'{doc_type}' uses Pandoc pipeline. No etc-docgen field mapping.",
            }
        )

    fmap = get_field_map(doc_type)
    if not fmap:
        return json.dumps({"error": f"No field map for '{doc_type}'"})

    return json.dumps(
        {
            "doc_type": doc_type,
            "renderer": "etc-docgen",
            "field_map": fmap,
            "writer_prompt_context": get_writer_prompt_context(doc_type),
        },
        ensure_ascii=False,
        indent=2,
    )


@mcp.tool()
def template_list() -> str:
    """List all bundled ETC document templates with their sizes.

    Returns template filenames and sizes. These templates are pre-configured
    with Jinja2 tags for docxtpl rendering.
    """
    tpl_dir = templates_dir()
    items = []
    for p in sorted(tpl_dir.glob("*")):
        items.append(
            {
                "filename": p.name,
                "size_kb": p.stat().st_size // 1024,
                "path": str(p),
            }
        )
    return json.dumps(items, ensure_ascii=False, indent=2)


@mcp.tool()
def template_fork(source_path: str, kind: str = "hdsd") -> str:
    """Fork an original ETC template by adding Jinja2 (docxtpl) tags.

    Use this when ETC releases a new template version. The forked template
    replaces the bundled one and is used by the export tool.

    Args:
        source_path: Path to the original ETC .docx template
        kind: Template type — hdsd, tkkt, tkcs, or tkct
    """
    from etc_docgen.tools.jinjafy_templates import (
        jinjafy_hdsd,
        jinjafy_tkcs,
        jinjafy_tkct,
        jinjafy_tkkt,
    )

    source = Path(source_path)
    if not source.exists():
        return json.dumps({"success": False, "error": f"Source not found: {source_path}"})

    dest_map = {
        "hdsd": "huong-dan-su-dung.docx",
        "tkkt": "thiet-ke-kien-truc.docx",
        "tkcs": "thiet-ke-co-so.docx",
        "tkct": "thiet-ke-chi-tiet.docx",
    }
    if kind not in dest_map:
        return json.dumps(
            {"success": False, "error": f"Unknown kind: {kind}. Use: hdsd, tkkt, tkcs, tkct"}
        )

    dest = templates_dir() / dest_map[kind]
    fork_fn = {
        "hdsd": jinjafy_hdsd,
        "tkkt": jinjafy_tkkt,
        "tkcs": jinjafy_tkcs,
        "tkct": jinjafy_tkct,
    }[kind]

    try:
        fork_fn(source, dest)
        return json.dumps(
            {
                "success": True,
                "kind": kind,
                "source": str(source),
                "output": str(dest),
            }
        )
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)})


# ─────────────────────────── Entry point ───────────────────────────


def main():
    """Run MCP server. Supports stdio, sse, and streamable-http transports.

    Use --transport to select transport, --host/--port for network transports.
    """
    # Configure logging
    logging.basicConfig(
        level=os.environ.get("LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    import argparse

    parser = argparse.ArgumentParser(
        description="etc-docgen MCP Server",
        prog="etc-docgen-mcp",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default="stdio",
        help="Transport protocol (default: stdio)",
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to bind for sse/streamable-http (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind for sse/streamable-http (default: 8000)",
    )

    args = parser.parse_args()

    # Update host/port on the mcp settings for network transports
    if args.transport in ("sse", "streamable-http"):
        mcp.settings.host = args.host
        mcp.settings.port = args.port

    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
