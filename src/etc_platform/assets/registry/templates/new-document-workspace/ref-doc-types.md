# ref-doc-types.md — Document Type Catalog

## Document Types

| ID    | Tên                        | Outline ID           | Căn cứ pháp lý                    | Thành phần chính                                         | Độ dài điển hình |
| ----- | -------------------------- | -------------------- | --------------------------------- | -------------------------------------------------------- | ---------------- |
| DT-01 | Thiết kế sơ bộ (TKCS)      | `tkcs-nd73-2019`     | NĐ 73/2019, Điều 18               | Giải pháp tổng thể, sơ đồ kiến trúc, kế hoạch triển khai | 30-60 trang      |
| DT-02 | Thiết kế chi tiết (TKCT)   | `tkct-nd73-2019`     | NĐ 73/2019, Điều 19               | Thiết kế module, DB schema, API spec, test plan          | 80-150 trang     |
| DT-03 | Dự toán phần mềm           | `du-toan-tt04-2020`  | TT 04/2020, TT 12/2020            | Bảng tính chi phí, hệ số, đơn giá nhân công              | 20-40 trang      |
| DT-04 | Báo cáo chủ trương đầu tư  | `bao-cao-chu-truong` | Luật Đầu tư công 2019, Điều 30-33 | Sự cần thiết, mục tiêu, phạm vi, dự kiến nguồn vốn       | 15-25 trang      |
| DT-05 | Thuyết minh đề án / dự án  | `thuyet-minh`        | NĐ 73/2019, Điều 16-17            | Hiện trạng, giải pháp đề xuất, kế hoạch, kinh phí        | 40-80 trang      |
| DT-06 | Hồ sơ mời thầu (HSMT)      | `hsmt-ldt2023`       | Luật 22/2023, NĐ 24/2024          | Chỉ dẫn nhà thầu, điều kiện hợp đồng, yêu cầu kỹ thuật   | 50-100 trang     |
| DT-07 | Hồ sơ dự thầu (HSDT)       | `hsdt-ldt2023`       | Luật 22/2023, NĐ 24/2024          | Đơn dự thầu, năng lực, giải pháp, giá dự thầu            | 60-120 trang     |
| DT-08 | Báo cáo nghiên cứu khả thi | `nghien-cuu-kha-thi` | NĐ 73/2019, Điều 15               | Hiện trạng, NCKT, phân tích lựa chọn, kế hoạch           | 50-80 trang      |

---

## Document Group Presets

Các bộ tài liệu thường đi cùng nhau:

| Group Preset      | Documents                    | Use Case               |
| ----------------- | ---------------------------- | ---------------------- |
| `hsdt-full`       | TKCS + TKCT + Dự toán + HSDT | Gói thầu đầy đủ        |
| `pre-feasibility` | Báo cáo chủ trương + NCKT    | Giai đoạn tiền khả thi |
| `investment`      | NCKT + TKCS + Dự toán        | Dự án đầu tư mới       |
| `custom`          | User selects                 | Custom combination     |

**Phase 3 shortcut:** Nếu user chọn Scope B (document group), hiện group presets trước danh sách đơn lẻ:

```
Bộ tài liệu gợi ý:
  ★ HSDT đầy đủ     — TKCS + TKCT + Dự toán + HSDT
  ◦ Tiền khả thi    — Báo cáo chủ trương + NCKT
  ◦ Đầu tư mới      — NCKT + TKCS + Dự toán
  ◦ Tùy chọn        — [multi-select]
```

---

## Document Dependencies

Một số tài liệu **inherit** nội dung từ tài liệu khác trong group:

| Document | Depends On         | Inherited Sections                        |
| -------- | ------------------ | ----------------------------------------- |
| TKCT     | TKCS               | Kiến trúc tổng thể, yêu cầu phi chức năng |
| Dự toán  | TKCS hoặc TKCT     | Danh mục module, phần mềm, thiết bị       |
| HSDT     | TKCS + Dự toán     | Giải pháp kỹ thuật, bảng giá              |
| NCKT     | Báo cáo chủ trương | Sự cần thiết, mục tiêu đầu tư             |

**Orchestrator rule:** Khi viết doc phụ thuộc, tự động inject DCB sections từ doc gốc. Không yêu cầu user copy-paste.

---

## Outline-to-Legal Mapping

Mỗi section trong outline gắn với điều khoản pháp lý cụ thể:

| Outline             | Section Pattern           | Legal Reference              |
| ------------------- | ------------------------- | ---------------------------- |
| `tkcs-nd73-2019`    | `1. Thông tin chung`      | NĐ 73/2019, Điều 18, khoản 1 |
| `tkcs-nd73-2019`    | `2. Kiến trúc hệ thống`   | NĐ 73/2019, Điều 18, khoản 2 |
| `tkcs-nd73-2019`    | `3. Giải pháp kỹ thuật`   | NĐ 73/2019, Điều 18, khoản 3 |
| `du-toan-tt04-2020` | `1. Căn cứ lập dự toán`   | TT 04/2020, Điều 3           |
| `du-toan-tt04-2020` | `2. Nội dung chi phí`     | TT 04/2020, Điều 4-8         |
| `du-toan-tt04-2020` | `3. Phương pháp tính`     | TT 04/2020, Phụ lục I-III    |
| `hsmt-ldt2023`      | `Chương I. Chỉ dẫn`       | NĐ 24/2024, Mẫu 1A           |
| `hsmt-ldt2023`      | `Chương II. Bảng dữ liệu` | NĐ 24/2024, Mẫu 1A           |
| `hsdt-ldt2023`      | `1. Đơn dự thầu`          | NĐ 24/2024, Mẫu 01           |
| `hsdt-ldt2023`      | `2. Thỏa thuận liên danh` | NĐ 24/2024, Mẫu 02           |

**Validator rule:** Nếu outline section bị thiếu content → cảnh báo "Section X.Y bắt buộc theo {legal ref}".
