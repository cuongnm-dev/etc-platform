#!/usr/bin/env python3
"""Test PlantUML detection logic without requiring java/plantuml at local machine."""
import sys, io, json, tempfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, "src")

from pathlib import Path
from etc_platform.engines.diagram import _detect_type, render_all
from etc_platform.tools.render_plantuml import find_plantuml, render_one

# 1. Detection
print("=== Detection logic ===")
cases = [
    ("@startuml\nA-->B\n@enduml", "plantuml"),
    ("@startmindmap\n* Root\n** Child\n@endmindmap", "plantuml"),
    ("graph TD\n  A-->B", "mermaid"),
    ("flowchart LR\n  A-->B", "mermaid"),
    ("erDiagram\n  A ||--o{ B : has", "mermaid"),
    ({"type": "plantuml", "source": "skinparam ..."}, "plantuml"),
    ({"type": "mermaid", "source": "graph TD"}, "mermaid"),
    ({"template": "kien-truc-4-lop", "data": {}}, "svg"),
    ({"source": "@startuml\nA-->B\n@enduml"}, "plantuml"),
    ({"source": "graph TD\n  A-->B"}, "mermaid"),
]
for value, expected in cases:
    actual = _detect_type(value)
    status = "OK" if actual == expected else "FAIL"
    label = value if isinstance(value, str) else json.dumps(value)
    print(f"  [{status}] expected={expected} actual={actual}  src={label[:60]!r}")

# 2. Availability
print("\n=== Availability probe ===")
spec = find_plantuml()
print(f"  find_plantuml() = {spec}")

# 3. End-to-end render call (graceful fallback if plantuml not available)
print("\n=== Render dispatch ===")
data = {
    "diagrams": {
        "test_plantuml": "@startuml\nA --> B\n@enduml",
        "test_mermaid": "graph TD\n  A-->B",
    }
}
with tempfile.TemporaryDirectory() as tmp:
    rep = render_all(data, Path(tmp))
    d = rep.to_dict()
    print(f"  status: {d['status']}")
    print(f"  mmdc_available: {d['mmdc_available']}")
    print(f"  plantuml_available: {d['plantuml_available']}")
    print(f"  rendered: {[r['key']+':'+r['type'] for r in d['rendered']]}")
    print(f"  failed:   {[(f['key'], f['type'], f['error'][:60]) for f in d['failed']]}")
    print(f"  warnings: {d['warnings'][:3]}")
