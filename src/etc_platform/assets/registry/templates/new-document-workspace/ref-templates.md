# ref-templates.md — DCB, _doc_state Templates (Claude Code)

## Nguyên tắc DCB

**Vấn đề gốc rễ của nội dung generic:** DCB cũ lưu context dạng narrative mơ hồ → writer không có data cụ thể → viết chung chung.

**Thiết kế mới:** DCB là **kho dữ liệu có nhãn** (labeled data store), mỗi field tương ứng với một câu trả lời interview cụ thể, map trực tiếp tới section cần dùng. Orchestrator trích đúng field → inject cho writer → writer viết xoay quanh data thật.

**Quy tắc điền DCB (bắt buộc):**
- Mỗi field phải có DATA THẬT từ interview. Nếu chưa có → điền `[CẦN BỔ SUNG: {tên field}]`
- KHÔNG điền câu chung chung (VD: "hệ thống còn nhiều hạn chế")
- CÓ điền số liệu, tên hệ thống, tên đơn vị, timeline cụ thể

---

## Template 1: `templates/dcb-template.md`

```markdown
# Document Context Brief (DCB)

---

## Metadata

| Field | Value |
|---|---|
| Document type | {doc-type-name} |
| Outline ID | {outline-id} |
| Legal basis | {NĐ/TT} |
| Project | {project-name} |
| Created | {date} |
| Last updated | {date} |
| DCB version | 1.0 |

---

## § Thông tin dự án (→ Sections 1.1, 1.2, bìa)

| Field | Value |
|---|---|
| Tên dự án đầy đủ | {tên đầy đủ theo QĐ phê duyệt} |
| Đơn vị chủ đầu tư | {tên đầy đủ + địa chỉ} |
| Đơn vị thực hiện | {tên đơn vị triển khai, nếu biết} |
| Bộ chủ quản | {BXD / BCA / BTTTT / ...} |
| Số QĐ phê duyệt chủ trương | {số QĐ, ngày ký, cơ quan ký} |
| Tổng mức đầu tư dự kiến | {X đồng} |
| Nguồn vốn | {NSNN / ODA / PPP / ...} |
| Timeline | {Quý X/202Y} — {Quý X/202Z} |
| Địa bàn áp dụng | {tỉnh/thành phố, đơn vị áp dụng} |

---

## § Căn cứ pháp lý (→ Section 1.2)

Liệt kê các văn bản pháp lý trực tiếp làm căn cứ:

- {Nghị định số XX/YYYY/NĐ-CP ngày dd tháng mm năm yyyy của Chính phủ về...}
- {Quyết định số XX/QĐ-TTg ngày dd tháng mm năm yyyy của Thủ tướng...}
- {Thông tư số XX/YYYY/TT-BTTTT ngày ...}
- {Quyết định phê duyệt chủ trương số ...}

---

## § Sự cần thiết (→ Section 1.3)

**QUAN TRỌNG: Phải có số liệu cụ thể. Không điền câu chung chung.**

- **Vấn đề đang gây thiệt hại/chậm trễ:** {mô tả cụ thể. VD: "Hệ thống quản lý văn bản triển khai năm 2009 không hỗ trợ ký số theo NĐ 30/2020, buộc phải in ấn 100% văn bản trước khi ký"}
- **Số liệu thiệt hại/tác động:** {VD: "2.400 văn bản/tháng, trung bình 3 ngày/văn bản vs SLA 1 ngày"}
- **CBCC/người dân bị ảnh hưởng:** {số lượng cụ thể, vị trí, đơn vị}
- **Hệ thống/quy trình hiện tại:** {tên hệ thống, năm triển khai, nhà cung cấp, vấn đề cụ thể}
- **Đơn vị tương đương đã giải quyết:** {VD: "Sở TTTT tỉnh X đã triển khai Y, giảm Z% thời gian xử lý"}
- **Yêu cầu từ cấp trên/pháp luật:** {QĐ/CT yêu cầu phải có hệ thống này trước ngày...}

---

## § Mục tiêu (→ Section 1.4)

**Mục tiêu tổng quát:** {1 câu súc tích, measurable}

**Mục tiêu cụ thể (measurable):**
- KPI 1: {VD: "Giảm thời gian xử lý văn bản từ 3 ngày xuống 1 ngày (giảm 67%)"}
- KPI 2: {VD: "100% văn bản được ký số điện tử theo NĐ 30/2020 trước 31/12/202Y"}
- KPI 3: {VD: "1.200 CBCC sử dụng hệ thống thường xuyên"}
- KPI 4: {VD: "Uptime 99.5%"}

---

## § Phạm vi (→ Section 1.5)

- **Module/chức năng:** {liệt kê ngắn gọn, đầy đủ}
- **Đơn vị áp dụng:** {tên các đơn vị, số lượng}
- **Địa bàn:** {tỉnh/thành phố}
- **Loại trừ (nếu có):** {những gì KHÔNG nằm trong phạm vi}
- **Giai đoạn:** {nếu phân kỳ: đợt này gồm module nào}

---

## § Hiện trạng (→ Section 2.x)

### Hạ tầng hiện có
- **Máy chủ:** {số lượng, cấu hình tóm tắt, năm, vị trí TTDL}
- **Mạng:** {băng thông WAN/LAN, nhà cung cấp}
- **TTDL:** {tên, địa điểm, cấp Tier}
- **Vấn đề hạ tầng:** {thiếu gì, quá tải gì}

### Phần mềm đang dùng
| # | Tên hệ thống | Nhà cung cấp | Năm | Vấn đề |
|---|---|---|---|---|
| 1 | {tên} | {đơn vị} | {năm} | {vấn đề cụ thể} |

### Nhân lực CNTT
- **Số CBCNTT:** {N người}
- **Trình độ:** {đại học CNTT / cao đẳng / tự học}
- **Vận hành:** {tự vận hành / thuê ngoài}

---

## § Danh mục module / chức năng (→ Section 3.1)

| # | Tên module | Chức năng chính | Người dùng | Độ ưu tiên |
|---|---|---|---|---|
| 1 | {tên module 1} | {mô tả chính xác chức năng} | {CBCC / người dân / cả hai} | Cao/Trung/Thấp |
| 2 | | | | |

**Tổng số module:** {N}
**Tổng người dùng dự kiến:** {N CBCC nội bộ + M người dân/doanh nghiệp}

---

## § Yêu cầu phi chức năng (→ Section 3.2)

| Tiêu chí | Yêu cầu | Ghi chú |
|---|---|---|
| Concurrent users | {N người} | Peak load |
| Response time | {< X giây} | 95th percentile |
| Uptime SLA | {99.X%} | {N giờ/năm downtime tối đa} |
| Data retention | {X năm} | |
| Cấp ATTT | Cấp {1/2/3} | Theo TCVN 11930:2017 |
| Backup | {daily/weekly, RPO X giờ, RTO Y giờ} | |
| Mobile support | {có/không} | {iOS/Android/web responsive} |

---

## § Giải pháp kỹ thuật (→ Sections 3.3, 3.4, 3.5, 3.6)

### Stack công nghệ
- **Ngôn ngữ lập trình:** {Java / .NET / Python / Node.js / ...}
- **Framework:** {Spring Boot / ASP.NET Core / Django / ...}
- **Cơ sở dữ liệu:** {PostgreSQL / Oracle / SQL Server / MySQL}
- **Middleware:** {Apache Kafka / RabbitMQ / Redis / ...}
- **Frontend:** {React / Angular / Vue / server-side JSP / ...}

### Kiến trúc hệ thống
- **Mô hình:** {Monolithic / Microservices / Modular monolith / SOA}
- **Pattern:** {MVC / CQRS / Event-driven / ...}
- **API style:** {REST / SOAP / GraphQL}

### Triển khai
- **Hình thức:** {On-premise / Cloud / Hybrid}
- **TTDL:** {tên trung tâm dữ liệu, địa điểm}
- **Cloud provider (nếu có):** {VNPT Cloud / Viettel IDC / AWS / Azure / ...}
- **Containerization:** {Docker + Kubernetes / bare metal / VM}

### Tích hợp
| Hệ thống | Giao thức | Mục đích | Bắt buộc? |
|---|---|---|---|
| LGSP tỉnh | REST API | Kết nối dịch vụ công | Bắt buộc |
| NDXP | REST API | Chia sẻ dữ liệu | Bắt buộc |
| VNeID | OAuth 2.0 | Xác thực công dân | Bắt buộc |
| {hệ thống legacy} | {giao thức} | {mục đích} | {có/không} |

### ATTT
- **Cấp ATTT:** Cấp {X} theo TCVN 11930:2017
- **Xác thực:** {SSO + LDAP / VNeID / username+password / 2FA}
- **Mã hóa:** {TLS 1.3 đường truyền, AES-256 lưu trữ}
- **Yêu cầu đặc biệt:** {nếu BCA: phân vùng mạng, mật, tuyệt mật}

---

## § Hạ tầng (→ Section 4)

### Máy chủ đề xuất
| Vai trò | Số lượng | CPU | RAM | Storage | OS |
|---|---|---|---|---|---|
| App server | {N} | {X core} | {Y GB} | {Z GB SSD} | {Linux/Windows} |
| DB server | {N} | {X core} | {Y GB} | {Z GB SSD RAID} | {Linux} |
| Backup/DR | {N} | {X core} | {Y GB} | {Z TB} | |

### Mạng
- **Băng thông Internet:** {X Mbps}
- **Mạng nội bộ:** {Gigabit LAN}
- **Phân vùng (VLAN):** {DMZ / Internal / Management}

---

## § Ngân sách sơ bộ (→ Section 6)

| Hạng mục | Tỷ trọng | Ước tính (đồng) |
|---|---|---|
| Phần mềm (PM, tích hợp, kiểm thử) | ~{X}% | {Y đồng} |
| Phần cứng, hạ tầng | ~{X}% | {Y đồng} |
| Triển khai, đào tạo | ~{X}% | {Y đồng} |
| Quản lý dự án | ~{X}% | {Y đồng} |
| Dự phòng | ~10% | {Y đồng} |
| **TỔNG** | **100%** | **{TỔNG đồng}** |

- **Nguồn vốn:** {NSNN cấp Bộ / tỉnh / ODA ...}
- **Năm bố trí vốn:** {202X-202Y}

---

## § Section Data Map (orchestrator lookup)

Orchestrator dùng bảng này để trích đúng DCB section cho từng writer:

| Section ID | DCB sections cần trích | Ghi chú |
|---|---|---|
| 1.1 | § Thông tin dự án | Tên, đơn vị, phê duyệt |
| 1.2 | § Căn cứ pháp lý | Copy nguyên list |
| 1.3 | § Sự cần thiết (TOÀN BỘ) | Critical: cần số liệu thật |
| 1.4 | § Mục tiêu | Tổng quát + cụ thể + KPI |
| 1.5 | § Phạm vi + § Danh mục module | Module list |
| 2.1 | § Hiện trạng > Hạ tầng | |
| 2.2 | § Hiện trạng > Phần mềm | Bảng hệ thống hiện có |
| 2.3 | § Hiện trạng > Nhân lực | |
| 2.4 | § Hiện trạng (tổng hợp) | Tổng hợp tất cả vấn đề |
| 3.1 | § Danh mục module | Bảng module đầy đủ |
| 3.2 | § Yêu cầu phi chức năng | Bảng NFR |
| 3.3 | § Giải pháp kỹ thuật > Kiến trúc + Stack | Sơ đồ kiến trúc |
| 3.4 | § Giải pháp kỹ thuật > Stack công nghệ | Framework, DB, middleware |
| 3.5 | § Giải pháp kỹ thuật > ATTT | Cấp ATTT, xác thực, mã hóa |
| 3.6 | § Giải pháp kỹ thuật > Tích hợp | Bảng tích hợp |
| 4.1 | § Hạ tầng > Mô hình triển khai | On-prem/Cloud/Hybrid |
| 4.2 | § Hạ tầng > Máy chủ | Bảng server config |
| 4.3 | § Hạ tầng > Mạng | Thiết kế mạng |
| 6.1 | § Căn cứ pháp lý + § Ngân sách sơ bộ | TT 04/2020 refs |
| 6.2 | § Ngân sách sơ bộ | Bảng chi phí |
| 6.3 | § Thông tin dự án > Nguồn vốn | |
| 7.x | § Mục tiêu + § Ngân sách | Hiệu quả KT-XH |

---

## Terminology Registry

| Viết tắt | Đầy đủ | Giải thích |
|---|---|---|
| HTTT | Hệ thống thông tin | — |
| CSDL | Cơ sở dữ liệu | — |
| ATTT | An toàn thông tin | — |
| CBCC | Cán bộ công chức | — |
| TTDL | Trung tâm dữ liệu | — |

---

## Cross-Reference Registry

| From Section | To Section | Type | Note |
|---|---|---|---|
| — | — | — | — |

---

## Wave History

| Wave | Sections | Status | Key outputs |
|---|---|---|---|
| — | — | — | — |
```

---

## Template 2: `templates/doc-state-template.md`

```markdown
---
document-type: {doc-type-name}
outline-id: {outline-id}
project: {project-name}
status: in-progress
current-wave: 0
completion-pct: 0
created: {date}
last-updated: {date}
---

# Document State: {project-name}

## Section Tracker

| Section ID | Title | Status | Wave | Words | Review | Dependencies |
|---|---|---|---|---|---|---|
| 1 | {section-title} | not-started | — | 0 | pending | — |
| 1.1 | {section-title} | not-started | — | 0 | pending | — |

## Status Legend

- `not-started`: Chưa bắt đầu
- `in-progress`: Writer đang viết
- `draft`: Writer xong, chưa review
- `reviewed`: Reviewer đã rà soát
- `revision`: Cần sửa
- `final`: Hoàn chỉnh

## Wave History

| Wave | Sections | Started | Completed | Issues |
|---|---|---|---|---|
| — | — | — | — | — |

## Review History

| Review # | Type | Verdict | Errors | Warnings | Date |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

## Placeholders Outstanding

| Section | Placeholder | Priority |
|---|---|---|
| — | — | — |

## KPI

| Metric | Value |
|---|---|
| Total sections | {N} |
| Completed sections | 0 |
| Total words | 0 |
| Open placeholders | 0 |
```

---

## Template 3: `templates/group-dcb-template.md` (Scope B only)

```markdown
# Group Document Context Brief

## Group Metadata

| Field | Value |
|---|---|
| Group name | {tên dự án / gói thầu} |
| Group slug | {slug} |
| Created | {date} |

## Shared Project Context

| Field | Value |
|---|---|
| Tên dự án / gói thầu | {tên} |
| Đơn vị chủ đầu tư | {đơn vị} |
| Bộ chủ quản | {bộ} |
| Nguồn vốn | {NSNN / ODA / ...} |
| Tổng mức đầu tư | {số tiền} |
| Thời gian | {timeline} |
| Phạm vi | {scope} |

## Documents in Group

| # | Document | Type | Outline ID | Status | Depends On |
|---|---|---|---|---|---|
| 01 | {name} | {type} | {id} | not-started | — |
| 02 | {name} | {type} | {id} | not-started | 01 |

## Shared DCB Reference

→ Xem `{tkcs-slug}/dcb.md` cho data kỹ thuật đầy đủ.
→ Group DCB chỉ lưu shared context và cross-doc registry.

## Cross-Document Data Registry

| Data item | Source doc | Used by |
|---|---|---|
| Danh mục module | TKCS § Danh mục module | TKCT, Dự toán, HSDT |
| Ngân sách | TKCS § Ngân sách | Dự toán, HSMT |
| Tech stack | TKCS § Giải pháp kỹ thuật | TKCT |
| Yêu cầu kỹ thuật | TKCS § ATTT + NFR | HSMT Chapter V |

## Shared Terminology

| Viết tắt | Đầy đủ |
|---|---|
| — | — |

## Shared Legal Basis

- {NĐ/TT/Luật 1}

## Shared Constraints

- {constraint}
```
