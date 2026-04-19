# etc-docgen

**Template-first documentation generator for ETC projects.**

Turn your codebase + running Docker stack into a complete set of ETC-compliant documents:

- 📘 **Thiết kế Kiến trúc** (TKKT) — architecture design
- 📗 **Thiết kế Cơ sở** (TKCS) — technical specification (NĐ 45/2026 Điều 13)
- 📙 **Hướng dẫn Sử dụng** (HDSD) — user manual with screenshots
- 📊 **Bộ Test Case** — test cases in ETC Excel template (BM.QT.04.04)

## Architecture — Docs-as-Code

```
Codebase + Docker   →   intel/*.json   →   content-data.json   →   4 Office files
                          (AI)              (AI)                    (Python deterministic)
```

**No AI-generated binaries.** AI produces structured JSON; Python engines render using:
- `openpyxl` for Excel (preserves formulas, validations, conditional formatting)
- `docxtpl` (Jinja2-for-Word) for Word (preserves styles, TOC, signing pages)

## Quick start

```bash
# Install
pip install etc-docgen

# Or from source
git clone https://github.com/etc-vn/etc-docgen
cd etc-docgen
pip install -e .

# Bootstrap in your project
cd my-project/
etc-docgen init
# → creates etc-docgen.yaml

# Edit config
vim etc-docgen.yaml

# Set credentials (never commit)
export DOCGEN_USERNAME=admin@etc.vn
export DOCGEN_PASSWORD=yourpass

# Run pipeline
etc-docgen generate

# Or step-by-step
etc-docgen research         # Phase 1: scan code
etc-docgen capture          # Phase 2: Playwright screenshots
etc-docgen data             # Phase 3: build content-data.json
etc-docgen export           # Phase 4: render 4 Office files
```

## Status

**v0.1 MVP** — export phase fully working end-to-end. Research + Capture + Data phases have AI integration hooks (work via Cursor/Claude Code for now).

| Phase | v0.1 | v0.2 | v0.3 |
|---|---|---|---|
| Research | 🟡 via AI adapter | ✅ Native LLM | ✅ Native |
| Capture | 🟡 via AI adapter | ✅ Native Playwright | ✅ Incremental |
| Data | 🟡 via AI adapter | ✅ Native LLM (batch) | ✅ Sharded |
| Export | ✅ Complete | ✅ Complete | ✅ + Web portal |
| Sharding | ❌ | 🟡 by_service | ✅ Incremental |
| Jira Xray | ❌ | 🟡 Push TCs | ✅ Bidirectional |
| Web portal | ❌ | 🟡 MkDocs | ✅ Custom theme |

## Features

### Template-first
Templates are the layout authority — Jinja2 tags embedded in Word files. Change layout by editing Word, not Python code.

### Scale-ready
Designed for enterprise: monorepo sharding, parallel LLM calls (Claude Batch API), incremental regen from Git diff.

### Standards-compliant
ETC templates (BM.QT.04.04, BM.QT.04.05) preserved pixel-perfect. NĐ 45/2026 structure for TKCS.

### Zero AI hallucination at render
AI outputs JSON only. Binary generation is 100% deterministic Python code.

## Commands

```bash
etc-docgen init              # Create etc-docgen.yaml
etc-docgen generate          # Full pipeline
etc-docgen research          # Phase 1 only
etc-docgen capture           # Phase 2 only
etc-docgen data              # Phase 3 only
etc-docgen export            # Phase 4 only
etc-docgen validate FILE     # Validate content-data.json
etc-docgen template list     # Show bundled templates
etc-docgen template fork FILE --kind hdsd    # Fork new ETC template
etc-docgen --version
```

## Integrations

### Cursor IDE
```
~/.cursor/skills/generate-docs/
```
Thin skill wrapper that orchestrates `etc-docgen` CLI. See `integrations/cursor/`.

### Claude Code
```
~/.claude/skills/generate-docs/
```
Same pattern. See `integrations/claude-code/`.

### CI/CD (GitHub Actions)
See `examples/incremental-ci/` for auto-regen on merge.

### Jira Xray (v0.2)
Push test cases directly to Jira — configure `integrations.jira_xray` in config.

## Project structure

```
etc-docgen/
├── src/etc_docgen/
│   ├── cli.py             # typer CLI
│   ├── config.py          # Pydantic config
│   ├── engines/           # xlsx (openpyxl), docx (docxtpl)
│   ├── capture/           # Playwright automation + auth
│   ├── research/          # Codebase analysis (v0.2+)
│   ├── data/              # content-data.json schema
│   ├── sharding/          # Enterprise-scale support (v0.2+)
│   ├── integrations/      # Jira Xray, Confluence
│   ├── assets/            # Bundled templates + schemas
│   └── tools/             # One-time scripts (jinjafy, extract)
├── tests/
├── examples/
├── docs/
└── integrations/          # Cursor, Claude Code skill adapters
```

## Requirements

- Python 3.11+
- Docker (for capture phase)
- Playwright browser (installed via `playwright install chromium` if using capture)

## License

Proprietary — Công ty CP Hệ thống Công nghệ ETC.

## Links

- **Issues**: https://github.com/etc-vn/etc-docgen/issues
- **Docs**: https://etc-vn.github.io/etc-docgen/
- **Changelog**: [CHANGELOG.md](CHANGELOG.md)
