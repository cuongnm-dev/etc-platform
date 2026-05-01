#!/usr/bin/env python3
"""Test diagram quality checker."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, "src")
from etc_platform.data.quality_checks import check_diagram_quality

# Case 1: BAD — bare PlantUML missing everything
bad1 = "@startuml\nA --> B\n@enduml"

# Case 2: BAD — markdown fence
bad2 = "```plantuml\n@startuml\nA --> B\n@enduml\n```"

# Case 3: BAD — rectangle-only no semantic
bad3 = """@startuml
title Test
top to bottom direction
skinparam defaultFontName "Times New Roman"
skinparam shadowing false
skinparam linetype ortho
rectangle "A"
rectangle "B"
rectangle "C"
rectangle "D"
rectangle "E"
A --> B
B --> C
C --> D
D --> E
@enduml"""

# Case 4: GOOD — full preset + title + grouping + semantic + direction
good = """@startuml
title <b>Hình 7.1</b>: Mô hình kiến trúc tổng thể
left to right direction
skinparam defaultFontName "Times New Roman"
skinparam shadowing false
skinparam linetype ortho

package "Lớp ứng dụng" {
  component "Service A" as A
  component "Service B" as B
}
package "Lớp dữ liệu" {
  database "PostgreSQL" as DB
}
A --> B
B --> DB : SQL
@enduml"""

# Case 5: GOOD sequence — polyline OK no direction needed
good_seq = """@startuml
title <b>Hình 8.3</b>: Luồng tạo hồ sơ
skinparam defaultFontName "Times New Roman"
skinparam shadowing false
skinparam linetype polyline
participant User
participant API
User -> API : POST /ho-so
API --> User : 201 Created
@enduml"""

cases = [
    ("BAD1 (bare)", bad1),
    ("BAD2 (fence)", bad2),
    ("BAD3 (rect-only)", bad3),
    ("GOOD struct", good),
    ("GOOD sequence", good_seq),
]
for label, src in cases:
    print(f"\n=== {label} ===")
    ws = check_diagram_quality({"diagrams": {"test": src}})
    if not ws:
        print("  (no warnings)")
    for w in ws:
        print(f"  - {w[:200]}")
