# Contributing to etc-docgen

## Development setup

```bash
git clone https://github.com/etc-vn/etc-docgen
cd etc-docgen
python -m venv .venv
.venv/Scripts/activate   # Windows
# source .venv/bin/activate   # Unix
pip install -e ".[dev]"
```

## Run tests

```bash
pytest                           # All tests
pytest tests/unit               # Unit only
pytest -m "not slow"            # Fast tests
pytest --cov                    # With coverage
```

## Lint + format

```bash
ruff check .                    # Lint
ruff format .                   # Auto-format
mypy src/etc_docgen             # Type check
```

## Adding a new template (ETC version upgrade)

1. Save new ETC template to `src/etc_docgen/assets/templates/source/`
2. Fork via CLI:
   ```bash
   etc-docgen template fork src/etc_docgen/assets/templates/source/new-hdsd.docx --kind hdsd
   ```
3. Run regression test:
   ```bash
   pytest tests/integration/test_templates.py
   ```
4. Update `CHANGELOG.md`
5. Commit both source + jinjafied templates

## Project structure

```
src/etc_docgen/
├── cli.py               # User-facing CLI (typer)
├── config.py            # Pydantic config model
├── paths.py             # Resolve bundled assets
├── engines/             # Pure render logic (xlsx, docx)
├── capture/             # Playwright + auth
├── research/            # Codebase analysis (v0.2+)
├── data/                # content-data builder + schema
├── sharding/            # Enterprise-scale splitter (v0.2+)
├── integrations/        # Jira, Confluence, etc.
├── assets/              # Bundled templates + schemas (PEP 302)
└── tools/               # One-time utilities (jinjafy, extract)
```

## Design principles

1. **Deterministic rendering**: AI produces JSON, Python renders binary. Never AI → binary.
2. **Template-first**: Templates authority, schemas declare; code doesn't rebuild layout.
3. **Fail fast**: Pre-flight validators. No silent fallback to wrong style.
4. **Subprocess isolation**: Engines run as subprocesses — zero impact on AI context window.
5. **Incremental-friendly**: Design for large projects (1000+ features) — sharding, Git diff.

## Commit message format

```
type(scope): subject

body (optional)

footer (optional)
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`.

Example:
```
feat(engines/xlsx): add MergedCell-safe write helper

Fixes issue where writing to a non-anchor merged cell raised exception.

Closes #12
```

## Release process (for maintainers)

1. Update version in `src/etc_docgen/__init__.py` + `pyproject.toml`
2. Update `CHANGELOG.md`
3. Tag: `git tag v0.1.1 -m "Release v0.1.1"`
4. Push: `git push --tags`
5. GitHub Actions auto-builds wheel + publishes
