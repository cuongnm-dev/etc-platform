"""Rewire content-data.json: move Mermaid source from block.*_diagram fields
into top-level `diagrams` block, replace block fields with PNG filename refs.

Root cause: agents were filling `architecture.architecture_diagram` with Mermaid
source (```mermaid\n...``` fenced) instead of PNG filename. The field is a
filename reference used by docxtpl InlineImage — Mermaid source there breaks
image embedding. Engine's auto-render only reads `data["diagrams"]` block.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

# (block_name, field_name) → diagrams_key
MOVES = [
    ("architecture", "architecture_diagram"),
    ("architecture", "logical_diagram"),
    ("architecture", "data_diagram"),
    ("architecture", "deployment_diagram"),
    ("architecture", "integration_diagram"),
    ("architecture", "security_diagram"),
    ("tkcs", "architecture_diagram"),
    ("tkcs", "data_model_diagram"),
    ("tkct", "architecture_overview_diagram"),
    ("tkct", "db_erd_diagram"),
    ("tkct", "ui_layout_diagram"),
    ("tkct", "integration_diagram"),
]

MERMAID_FENCE = re.compile(r"^\s*```(?:mermaid)?\s*\n?|```\s*$", re.MULTILINE)


def strip_fence(s: str) -> str:
    """Remove ```mermaid ... ``` fences if present."""
    if not isinstance(s, str):
        return s
    s = MERMAID_FENCE.sub("", s).strip()
    return s


def looks_like_mermaid(s) -> bool:
    if not isinstance(s, str):
        return False
    head = strip_fence(s).lstrip().split("\n", 1)[0].strip()
    return head.startswith((
        "flowchart", "graph", "sequenceDiagram", "erDiagram", "classDiagram",
        "stateDiagram", "journey", "gantt", "pie", "mindmap", "C4Context",
    ))


def rewire(data: dict) -> dict:
    data.setdefault("diagrams", {})
    moved = []
    for block, field in MOVES:
        b = data.get(block)
        if not isinstance(b, dict):
            continue
        val = b.get(field)
        if val and looks_like_mermaid(val):
            # Use a unique diagrams key: block-scoped if field collides
            diagrams_key = field
            if diagrams_key in data["diagrams"]:
                # Prefix with block for TKCS/TKCT to avoid architecture collision
                if block == "tkcs":
                    diagrams_key = f"tkcs_{field}"
                elif block == "tkct":
                    diagrams_key = f"tkct_{field}"
            data["diagrams"][diagrams_key] = strip_fence(val)
            # Replace field with PNG filename reference
            b[field] = f"{diagrams_key}.png"
            moved.append(f"{block}.{field} → diagrams.{diagrams_key}")
    return data, moved


if __name__ == "__main__":
    path = Path(sys.argv[1])
    data = json.loads(path.read_text(encoding="utf-8"))
    data, moved = rewire(data)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Rewired {len(moved)} fields in {path}:")
    for m in moved:
        print(f"  - {m}")
    print(f"\n`diagrams` block now has {len(data['diagrams'])} keys:")
    for k, v in data["diagrams"].items():
        head = v.split("\n", 1)[0][:60]
        print(f"  - {k}: {head}...")
