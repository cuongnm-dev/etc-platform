# Claude Code integration

Thin skill wrapper that orchestrates `etc-docgen` CLI from Claude Code agent dispatch.

## Installation

```bash
pip install etc-docgen
cp -r integrations/claude-code/skill ~/.claude/skills/generate-docs
```

## Usage

```
/generate-docs
```

Skill dispatch multiple agents (researcher, test-runner, data-writer, exporter) which
coordinate through subprocess calls to `etc-docgen`.

## Claude Code leverage

| Feature | Claude Code advantage |
|---|---|
| Parallel Agent() | 5 agents dispatched in 1 message (vs sequential in Cursor) |
| run_in_background | Long Playwright capture phase non-blocking |
| Extended thinking | Native for Opus research FLOW phase |
| Subprocess | Runs `etc-docgen` reliably |

## How it differs from Cursor

- **Multi-agent parallel** instead of single-agent
- **Background tasks** for long phases
- Agent-specific sub-prompts (tdoc-researcher, tdoc-data-writer, tdoc-exporter)
- No IDE integration (Design Mode, Composer) — agent does vision review
