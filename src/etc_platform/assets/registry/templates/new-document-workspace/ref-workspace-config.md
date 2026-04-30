# ref-workspace-config.md — Workspace Configuration Templates

Scaffold tạo file `_workspace.md` tại root workspace. Đây là config trung tâm — mọi agent đọc file này trước khi hoạt động.

---

## `_workspace.md` — Master Config

```markdown
---
workspace-type: document
workspace-name: "{name}"
created: "{YYYY-MM-DD}"
last-updated: "{YYYY-MM-DD}"

# Đơn vị
unit: "{đơn vị chủ trì}"
ministry: "{BXD | BCA | BTTTT | Generic}"

# Scope
scope: "{single | group}"
group-name: "{tên dự án / gói thầu}"  # chỉ khi scope=group

# Source (nếu từ Đề án CĐS)
source-de-an: ""                       # path tới thinking-bundle/ (nếu có)
source-initiative: ""                  # DA-XX ID (nếu có)

# Document types configured
doc-types:
  - id: "DT-01"
    name: "TKCS"
    outline-id: "tkcs-nd73-2019"
    legal-basis: "NĐ 73/2019"
  # - id: ...

# Pipeline config
automation-mode: "REVIEW"              # REVIEW | AUTOPILOT | STEP
export-format: "docx"                  # docx | pdf | both
snippet-level: "full"                  # full | minimal | none
ministry-variant: "Generic"            # BXD | BCA | BTTTT | Generic
---

# Workspace: {name}

## Agent Roster

| Agent | Model | Role | Dispatch |
|---|---|---|---|
| doc-orchestrator | haiku | Wave coordinator | User invoke / resume |
| doc-writer | sonnet | Section content | Orchestrator → Agent tool (background) |
| doc-reviewer | sonnet | Quality gate | Orchestrator → Agent tool |

## Operational Config

### Parallel Dispatch
- Max sections per wave: **5**
- Max parallel doc-writers: **5** (1 per section)
- Dependent sections: sequential (wait for dependency to complete)

### Context Budget
| Agent | Max input | Sources |
|---|---|---|
| doc-writer | ~5K tokens | DCB excerpt + dependencies + constraints |
| doc-reviewer | ~6K tokens | Section content + legal refs |

### Stall Detection
- Agent fails → retry_count += 1
- retry_count == 1 → auto-retry with expanded context
- retry_count == 2 → STOP, ask user: "tách nhỏ | thêm context | bỏ qua | tự viết"

### Auto-continuation Protocol
```
DO:
  ✓ After completing phase → IMMEDIATELY next phase
  ✓ After dispatch → wait → collect → continue
  ✓ After user approve wave → auto-start next wave
  ✓ Status 1 line: "[Wave 3] Viết Mục 5, 6... ⏳"

DON'T:
  ✗ NEVER stop between auto phases to ask permission
  ✗ NEVER output document content in chat
  ✗ NEVER re-explain what just done
```

### Wave Cycle
```
PREP → DISPATCH (parallel) → COLLECT → VALIDATE → EXPORT DRAFT → REVIEW
  │                                                                  │
  └─── auto ────────────────────────────────────────────────────────┘
                                                  REVIEW mode: stop
                                                  AUTOPILOT: continue if clean
                                                  STEP mode: stop each phase
```

### File Isolation
| Agent | WRITES (exclusive) | NEVER writes |
|---|---|---|
| doc-writer A (section X) | `content/{X}.md` | Other content files |
| doc-reviewer | (nothing — readonly) | Any file |
| doc-orchestrator | `_doc_state.md`, `dcb.md` (append) | `content/*.md` |

## Active Projects

| Project | Doc-Type | Status | Current Stage | Last Updated |
|---|---|---|---|---|
| (none) | — | — | — | — |

## Resume Instructions

Khi mở session mới:
1. Đọc `_workspace.md` → biết config
2. Đọc project `_doc_state.md` → biết progress
3. Xác định `current_stage` + `next_action`
4. Tiếp tục từ đúng chỗ dang dở
```

---

## `_doc_state.md` — Per-Project State (ENHANCED)

```markdown
---
# Project Identity
project-name: "{tên}"
doc-type: "{DT-01}"
outline-id: "{tkcs-nd73-2019}"
project-path: "projects/{slug}/"
created: "{YYYY-MM-DD}"
last-updated: "{YYYY-MM-DD}"

# Pipeline State
current-stage: "INIT"
  # INIT → INTERVIEW → PLANNING → WAVE_N → REVIEW_N → EXPORT → DONE
next-action: "Begin doc-type-specific interview"
automation-mode: "REVIEW"

# Wave Progress
total-waves: 0
current-wave: 0
waves-complete: 0

# Completion
completion-pct: 0
total-sections: 0
sections-complete: 0
total-words: 0
open-placeholders: 0

# Source (inherited data)
source-de-an: ""
source-doc: ""         # dependent document (TKCS for TKCT)

# KPI
kpi:
  tokens-used: 0
  duration-minutes: 0
  review-loops: 0
  stall-count: 0
---

# Document State: {project-name}

## Stage Progress

| Stage | Started | Completed | Verdict | Agent | Notes |
|---|---|---|---|---|---|
| INIT | {date} | | | | |
| INTERVIEW | | | | | |
| PLANNING | | | | | |
| WAVE_1 | | | | | |
| REVIEW_1 | | | | | |
| WAVE_N | | | | | |
| FINAL_REVIEW | | | | | |
| EXPORT | | | | | |

## Section Tracker

| Section ID | Title | Status | Wave | Words | Review | Dependencies |
|---|---|---|---|---|---|---|
| 1 | {title} | not-started | — | 0 | pending | — |
| 1.1 | {title} | not-started | — | 0 | pending | — |

Status: not-started → in-progress → draft → reviewed → revision → final

## Active Blockers

| Blocker | Since | Type | Resolution |
|---|---|---|---|
| (none) | | | |

## Wave History

| Wave | Sections | Started | Completed | Verdict | Issues |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

## Review History

| Review # | Type | Verdict | Errors | Warnings | Date |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

## Next Action

{Mô tả cụ thể bước tiếp theo. Đủ detail để agent mới có thể resume.}

## Placeholders Outstanding

| Section | Placeholder | Priority |
|---|---|---|
| — | — | — |
```

---

## `_strategy_state.md` — Strategic Pipeline State (ENHANCED)

```markdown
---
# Project Identity
project-name: "{Tên Đề án}"
org-name: "{Tên đơn vị}"
doc-type: "de-an-cds"
project-path: "projects/{slug}/"
created: "{YYYY-MM-DD}"
last-updated: "{YYYY-MM-DD}"

# Pipeline State
current-stage: "SPIRAL_1_SCOPE"
  # SPIRAL_1_SCOPE → SPIRAL_2_STRATEGY → CHECKPOINT_1
  # → SPIRAL_3_SOLUTIONS → DEDUP_GATE → CHECKPOINT_2
  # → SPIRAL_4_STRUCTURE → CHECKPOINT_3 → FREEZE
  # → WRITE_INIT → WRITE_WAVE_N → FINAL_REVIEW → EXPORT → DONE
next-action: "Begin Deep Context Interview Blocks 1-2"
automation-mode: "REVIEW"

# Checkpoints
checkpoint-1: "pending"     # pending | approved | revision_requested
checkpoint-2: "pending"
checkpoint-3: "pending"

# Thinking Bundle
thinking-bundle-status: "draft"   # draft | frozen
outline-status: "mutable"         # mutable | locked

# Spiral Progress
spirals:
  scope:
    status: "not_started"
    org-profile: false
    policy-landscape: false
  strategy:
    status: "not_started"
    gap-analysis: false
    strategic-framework: false
  solutions:
    status: "not_started"
    initiative-portfolio: false
    dedup-complete: false
  structure:
    status: "not_started"
    outline-proposed: false
    section-briefs: false

# Write Layer
write:
  dcb-generated: false
  total-waves: 0
  current-wave: 0
  waves-complete: 0

# KPI
kpi:
  tokens-total: 0
  kb-entries-added: 0
  dedup-proposals-total: 0
  dedup-proposals-modified: 0
  interview-questions-asked: 0
  spiral-backs: 0
---

# Strategy State: {Tên Đề án}

## Stage Progress

| Stage | Started | Completed | Verdict | Agent | Notes |
|---|---|---|---|---|---|
| SPIRAL_1_SCOPE | | | | strategy-analyst + policy-researcher | |
| SPIRAL_2_STRATEGY | | | | strategy-analyst | |
| CHECKPOINT_1 | | | | user | |
| SPIRAL_3_SOLUTIONS | | | | strategy-analyst + policy-researcher | |
| DEDUP_GATE | | | | strategy-analyst | |
| CHECKPOINT_2 | | | | user | |
| SPIRAL_4_STRUCTURE | | | | structure-advisor + strategy-analyst | |
| CHECKPOINT_3 | | | | user | |
| FREEZE | | | | | |
| WRITE_INIT | | | | strategy-analyst (DCB) | |
| WRITE_WAVE_N | | | | doc-writer | |
| FINAL_REVIEW | | | | doc-reviewer | |
| EXPORT | | | | | |

## Checkpoint History

| Checkpoint | Date | Verdict | User Feedback | Action Taken |
|---|---|---|---|---|
| | | | | |

## Spiral Back Log

| From | To | Reason | Date |
|---|---|---|---|
| | | | |

## Active Blockers

| Blocker | Since | Type | Resolution |
|---|---|---|---|
| (none) | | | |

## Next Action

{Mô tả cụ thể bước tiếp theo cho agent resume.}
```
