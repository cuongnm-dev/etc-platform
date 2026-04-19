# Changelog

All notable changes to `etc-docgen` will be documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] — 2026-04-18

### Added
- Initial MVP extracted from Claude Code + Cursor 3 skills
- Typer CLI with subcommands: `init`, `generate`, `research`, `capture`, `data`, `export`, `validate`, `template`
- Pydantic v2 config model + YAML loader with env var interpolation
- Bundled ETC templates (BM.QT.04.04 + BM.QT.04.05) forked with Jinja2 tags
- `engines/xlsx.py` — openpyxl-based Excel filler (preserves formulas, merged cells, DV, CF)
- `engines/docx.py` — docxtpl-based Word renderer (Jinja2-for-Word, TOC auto-refresh, orphan media cleanup)
- `capture/auth.py` — simple auth runner (user-supplied credentials + optional recording mode)
- `tools/jinjafy_templates.py` — fork ETC template into Jinja-tagged version (one-time)
- `tools/extract_*_schema.py` — analyze template structure for schema authoring

### Working end-to-end
- `etc-docgen export` — render 4 Office files from `content-data.json`
- `etc-docgen validate` — check content-data shape + priority values
- `etc-docgen template list` / `fork` — manage templates

### Integrations
- Thin skill adapters for Cursor 3 + Claude Code (orchestrate CLI)

### Not yet implemented (planned for v0.2)
- Native `research` phase (currently via AI adapter)
- Native `capture` phase (currently via AI adapter using Playwright MCP)
- Native `data` phase (currently AI produces content-data.json)
- Jira Xray integration
- Web portal (MkDocs) output
- Sharding support for enterprise-scale projects
- Git-diff incremental regeneration
