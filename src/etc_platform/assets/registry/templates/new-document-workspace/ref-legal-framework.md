# ref-legal-framework.md — Legal Reference Summaries

Tạo các file summary trong `reference/legal/`. Chỉ tạo cho doc-types đã chọn trong Phase 3.

---

## `nd-30-2020-summary.md` — Luôn tạo (thể thức văn bản)

```markdown
# NĐ 30/2020/NĐ-CP — Công tác Văn thư

**Hiệu lực:** 05/03/2020
**Thay thế:** NĐ 110/2004/NĐ-CP

## Phạm vi áp dụng

Quy định về công tác văn thư: soạn thảo, ban hành, quản lý văn bản hành chính nhà nước.

## Các quy định chính cho tài liệu CNTT

### Thể thức văn bản (Phụ lục I)

| Thành phần           | Quy cách                                                         |
| -------------------- | ---------------------------------------------------------------- |
| Quốc hiệu — Tiêu ngữ | CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM / Độc lập - Tự do - Hạnh phúc |
| Font chữ             | Times New Roman                                                  |
| Cỡ chữ nội dung      | 13-14pt                                                          |
| Giãn dòng            | Tối thiểu cách dòng đơn, tối đa 1.5 lines                        |
| Lề trang             | Trên: 20-25mm, Dưới: 20-25mm, Trái: 30-35mm, Phải: 15-20mm       |
| Đánh số trang        | Số Ả Rập, giữa trang, lề dưới                                    |

### Ký hiệu văn bản

- Tờ trình: `TTr`
- Báo cáo: `BC`
- Công văn: không có ký hiệu loại
- Quyết định: `QĐ`

### Ngày tháng

- Đầy đủ: `ngày ... tháng ... năm ...`
- Ngày < 10: thêm `0` (01, 02...)
- Tháng < 10: thêm `0`

## Lưu ý

- NĐ 30/2020 quy định thể thức **văn bản hành chính**, không phải tài liệu kỹ thuật
- Tài liệu CNTT (TKCS, TKCT, Dự toán) áp dụng thể thức NĐ 30/2020 cho phần hành chính (trang bìa, tờ trình kèm theo), nội dung kỹ thuật bên trong theo format riêng của NĐ 45/2026
```

---

## `nd-45-2026-summary.md` — Tạo khi có TKCS/TKCT/NCKT/Thuyết minh

```markdown
# NĐ 45/2026/NĐ-CP — Quản lý Đầu tư Ứng dụng CNTT

**Tên đầy đủ:** Nghị định số 45/2026/NĐ-CP ngày 26 tháng 01 năm 2026 của Chính phủ
 quy định quản lý đầu tư ứng dụng công nghệ thông tin sử dụng nguồn vốn ngân sách nhà nước
**Hiệu lực:** 01/03/2026
**Thay thế:** NĐ 73/2019/NĐ-CP và NĐ 82/2024/NĐ-CP
**Cơ quan chủ trì:** Bộ Khoa học và Công nghệ (thay Bộ TT&TT)
**Tổng số điều:** 31 (tinh gọn hơn NĐ 73/2019)

## Phạm vi

Quản lý đầu tư ứng dụng CNTT sử dụng nguồn vốn ngân sách nhà nước.
Định hướng: **Chuyển đổi số / Quốc gia số** (thay Chính phủ điện tử).

## Cấu trúc NĐ 45/2026

| Chương | Nội dung | Điều |
|---|---|---|
| I | Quy định chung | 1–6 |
| II Mục 1 | Quản lý dự án — Quy định chung | 7–9 |
| II Mục 2 | Chuẩn bị đầu tư (NCKT, TKCS, TKCT, Dự toán, Thẩm định) | 10–17 |
| II Mục 3 | Thực hiện đầu tư (Kiểm thử, Nghiệm thu, Bàn giao) | 18–24 |
| II Mục 4 | Kết thúc đầu tư (Quyết toán) | 25–26 |
| III | Nhiệm vụ CNTT chi thường xuyên | 27–28 |
| IV | Giám sát, đánh giá, xử lý vi phạm | 29–31 |

## Mapping Điều khoản: NĐ 73/2019 → NĐ 45/2026

| Nội dung | NĐ 73/2019 | NĐ 45/2026 |
|---|---|---|
| Thiết kế sơ bộ (TKCS) | Điều 18 | **Điều 13** |
| Thiết kế chi tiết (TKCT) | Điều 19 | **Điều 14** |
| Dự toán / Tổng mức đầu tư | Điều 19–20 | **Điều 16** |
| Thẩm định TKCS | Điều 20–21 | **Điều 17** |
| Kiểm thử, vận hành thử | Điều 25+ | **Điều 22** |
| Nghiệm thu, bàn giao | Điều 26+ | **Điều 24** |
| Quyết toán vốn | Chương cuối | **Điều 25–26** |
| Nhiệm vụ CNTT TX | Chương III | **Điều 27–28** |

## Yêu cầu nội dung TKCS — Điều 13 (BẮT BUỘC MỚI)

| STT | Nội dung | Mới? |
|---|---|---|
| 1 | Mô tả các yêu cầu của dự án | |
| 2 | Danh mục quy chuẩn kỹ thuật, tiêu chuẩn áp dụng | |
| 3 | Phân tích sự tuân thủ **Khung kiến trúc tổng thể quốc gia số** | **MỚI — BẮT BUỘC** |
| 4 | Phân tích, lựa chọn phương án công nghệ; kết nối, liên thông, chia sẻ dữ liệu | **MỚI — BẮT BUỘC** |
| 5 | Tuyên bố sẵn sàng IPv6 hoặc lộ trình nâng cấp (dự án Internet) | **MỚI — BẮT BUỘC** |
| 6 | Phương án an toàn, an ninh mạng | |
| 7 | **Mô hình tổng thể + mô hình lô-gic + mô hình vật lý** | **MỚI — BẮT BUỘC 3 tầng** |

## Yêu cầu nội dung TKCT — Điều 14

| STT | Nội dung | Ghi chú |
|---|---|---|
| 1 | Phù hợp với TKCS đã phê duyệt | |
| 2 | Chi tiết thông số kỹ thuật, chức năng, tính năng | |
| 3 | Sơ đồ chi tiết (mặt bằng, đi dây, lắp đặt) | |
| 4 | Danh mục thiết bị với thông số kỹ thuật cụ thể | |
| 5 | Chủ đầu tư **tự thẩm định, phê duyệt** TKCT | **MỚI — phân quyền** |

## Phân loại dự án — theo Luật 58/2024/QH15 (lĩnh vực CNTT)

| Nhóm | Tổng mức đầu tư |
|---|---|
| Quan trọng quốc gia | Quốc hội quyết định |
| **A** | ≥ **1.600 tỷ đồng** |
| **B** | 90 tỷ — dưới 1.600 tỷ đồng |
| **C** | Dưới **90 tỷ đồng** |

⚠ Ngưỡng cũ (NĐ 73/2019): A ≥ 200 tỷ, B 15–200 tỷ, C < 15 tỷ — **ĐÃ HẾT HIỆU LỰC**

## Ngưỡng thiết kế & BQLDA — Điều 9

| Quy định | NĐ 73/2019 | NĐ 45/2026 |
|---|---|---|
| Thiết kế **01 bước** (BKTKT) | ≤ 15 tỷ đồng | ≤ **20 tỷ đồng** |
| Thiết kế **02 bước** (TKCS + TKCT) | > 15 tỷ đồng | > **20 tỷ đồng** |
| BQLDA bắt buộc | ≥ 15 tỷ | ≥ **20 tỷ** (trừ dự án mua sắm: miễn) |

## Thẩm quyền thẩm định — Điều 17

- **Nhóm A:** Bộ Khoa học và Công nghệ thẩm định TKCS
- **Nhóm B, C:** Chủ đầu tư tổ chức thẩm định
- **TKCT:** Chủ đầu tư **tự thẩm định, phê duyệt** (phân quyền mới)

## Loại hình dự án mới (không có trong NĐ 73/2019)

| Loại | Điều | Đặc điểm |
|---|---|---|
| **Phần mềm phổ biến** | Điều 5 | Áp dụng quy trình mua sắm thương mại thay vì đầu tư dự án |
| **Phần mềm nội bộ** | Điều 5 | Xếp vào **mua sắm hàng hóa** (không phải dự án đầu tư) |
| **Sandbox thử nghiệm** | Điều 6 | Tổ chức tự chi phí, không dùng ngân sách |
| **Mô hình EP** | Điều 7 | Kết hợp thiết kế + cung cấp hàng hóa |

## Bắt buộc mới — Yêu cầu khi lập TKCS (Điều 4, 13)

1. **Khung kiến trúc số quốc gia:** Mọi dự án PHẢI tuân thủ và chứng minh tuân thủ trong TKCS
2. **3 tầng mô hình:** TKCS phải có đủ mô hình tổng thể + lô-gic + vật lý
3. **IPv6:** Dự án Internet phải tuyên bố sẵn sàng hoặc có lộ trình
4. **Liên thông dữ liệu:** Bắt buộc phân tích kết nối, chia sẻ dữ liệu với hệ thống liên quan
5. **Kiểm thử (Điều 22):** Bắt buộc kiểm thử và vận hành thử TRƯỚC nghiệm thu

## Điều khoản chuyển tiếp

- Từ 01/03/2026: NĐ 73/2019/NĐ-CP và NĐ 82/2024/NĐ-CP **hết hiệu lực hoàn toàn**
- Dự án đang thẩm định nhưng chưa phê duyệt: nên cập nhật theo NĐ 45/2026
- Thông tư hướng dẫn TT 04/2020/TT-BTTTT: tạm thời vẫn áp dụng đến khi Bộ KH&CN ban hành thay thế
```

---

## `tt-04-2020-summary.md` — Tạo khi có Dự toán

```markdown
# TT 04/2020/TT-BTTTT — Dự toán Chi phí Phần mềm

**Hiệu lực:** 24/02/2020
**Sửa đổi bởi:** TT 12/2020/TT-BTTTT (sửa hệ số K_3)
**Phạm vi:** Xác định chi phí phần mềm nội bộ trong dự án CNTT sử dụng vốn NSNN.

## Cấu trúc chi phí

### Tổng chi phí phần mềm (Điều 4)
```

G_PM = G_NC + G_CDPM

```

### Chi phí xây dựng, phát triển (Điều 5)
```

G_NC = Σ (S_i × K_1 × K_2 × K_3 × D)

```

| Ký hiệu | Ý nghĩa | Nguồn |
|---|---|---|
| S_i | Điểm chức năng (FP) theo IFPUG | Phân tích yêu cầu |
| K_1 | Hệ số ngôn ngữ lập trình | Phụ lục I |
| K_2 | Hệ số phức tạp kỹ thuật (14 yếu tố) | Phụ lục II |
| K_3 | Hệ số đặc thù | Phụ lục III (sửa đổi TT 12/2020) |
| D | Đơn giá nhân công (người-tháng) | Theo vùng, theo năm |

### Hệ số K_1 — Ngôn ngữ lập trình (Phụ lục I, trích)
| Ngôn ngữ | K_1 |
|---|---|
| Java | 1.00 |
| C# / .NET | 1.00 |
| Python | 0.85 |
| JavaScript/TypeScript | 0.95 |
| PHP | 0.90 |
| Mobile (Swift/Kotlin) | 1.10 |

### Hệ số K_2 — Phức tạp kỹ thuật (Phụ lục II)
14 yếu tố đánh giá, mỗi yếu tố: 0-5 điểm → tổng → K_2

| # | Yếu tố | Thang |
|---|---|---|
| 1 | Mức độ tin cậy | 0-5 |
| 2 | Hiệu năng | 0-5 |
| 3 | Khả năng bảo mật | 0-5 |
| 4 | Tính phức tạp cấu hình | 0-5 |
| 5-14 | ... (xem Phụ lục II đầy đủ) | 0-5 |

### Chi phí khác
| Loại chi phí | Tỷ lệ | Căn cứ |
|---|---|---|
| Chi phí quản lý dự án | 5-10% G_NC | Điều 9 |
| Chi phí tư vấn | Theo hợp đồng | Điều 10 |
| Dự phòng | ≤ 10% tổng | Điều 11 |
| Chi phí đào tạo | Thực tế | Điều 8 |

## Lưu ý thực tế
- Đơn giá nhân công D thay đổi hàng năm — luôn dùng bảng giá năm hiện hành
- K_3 phải dùng bản sửa đổi TT 12/2020, không dùng TT 04/2020 gốc
- Function Point phải tính theo IFPUG CPM (Counting Practices Manual)
```

---

## `luat-dau-thau-2023-summary.md` — Tạo khi có HSMT/HSDT

```markdown
# Luật Đấu thầu 2023 (số 22/2023/QH15) + NĐ 214/2025/NĐ-CP

**Luật 22/2023/QH15 hiệu lực:** 01/01/2024 | **Thay thế:** Luật Đấu thầu 2013
**NĐ 214/2025/NĐ-CP hiệu lực:** 04/08/2025 | **Thay thế:** NĐ 24/2024/NĐ-CP

## Phạm vi

Quản lý hoạt động đấu thầu, lựa chọn nhà thầu sử dụng vốn NSNN.
Hệ thống đấu thầu điện tử: **e-GP** tại muasamcong.mpi.gov.vn
Tài liệu là **E-HSMT** (Electronic), nhà thầu nộp **E-HSDT** qua Hệ thống.

## Hình thức lựa chọn nhà thầu (Điều 20-30)

| Hình thức            | Áp dụng khi                                      |
| -------------------- | ------------------------------------------------ |
| Đấu thầu rộng rãi    | Mặc định, mọi gói thầu                           |
| Đấu thầu hạn chế     | Gói thầu đặc thù, ít nhà thầu                    |
| Chỉ định thầu        | Theo Điều 23 (an ninh, cấp bách, < 500 triệu...) |
| Chào hàng cạnh tranh | Hàng hóa thông dụng, < 5 tỷ                      |
| Mua sắm trực tiếp    | Mở rộng hợp đồng đã có, ≤ 130%                   |

## Phương thức tổ chức đấu thầu

| Phương thức | Số túi hồ sơ | Đặc điểm |
|---|---|---|
| Một giai đoạn một túi | 1 | Kỹ thuật + giá gộp chung |
| Một giai đoạn hai túi | 2 | Kỹ thuật (E-HSĐXKT) tách riêng giá (E-HSĐXTC) |

*CNTT: thường dùng **một giai đoạn hai túi hồ sơ***

## Quy trình đấu thầu điện tử (e-GP)

1. Phê duyệt kế hoạch LCNT (Điều 37)
2. Lập E-HSMT → Phê duyệt → Phát hành (Điều 38)
3. Nhà thầu nộp chi phí (vd: 330.000đ) → Mua E-HSMT
4. Phát hành E-HSMT ≥ 20 ngày trước đóng thầu
5. Hội nghị tiền đấu thầu (nếu có)
6. Nhà thầu nộp E-HSDT qua Hệ thống trước đóng thầu
7. Chủ đầu tư mở thầu điện tử
8. Đánh giá E-HSDT (Điều 39-42):
   - B1: Tính hợp lệ (5 tiêu chí)
   - B2: Năng lực, kinh nghiệm (đạt/không đạt)
   - B3: Kỹ thuật (điểm hoặc đạt/không đạt)
   - B4: Giá (E-HSĐXTC)
9. Công khai, đối chiếu tài liệu
10. Thương thảo hợp đồng (≤ 28 ngày sau công khai)
11. Phê duyệt, công khai kết quả
12. Ký hợp đồng

## E-HSMT — Cấu trúc (NĐ 214/2025, Mẫu 1A)

| Phần | Chương | Nội dung |
| ---- | ------ | -------- |
| Phần 1 | I | Chỉ dẫn nhà thầu (E-CDNT) — text chuẩn cố định |
| Phần 1 | II | Bảng dữ liệu đấu thầu (E-BDL) — điền tham số cụ thể |
| Phần 1 | III | Tiêu chuẩn đánh giá E-HSDT (4 mục) |
| Phần 1 | IV | Biểu mẫu mời thầu và dự thầu |
| Phần 2 | V | Yêu cầu về kỹ thuật (thường là file đính kèm riêng) |
| Phần 3A | VI | Điều kiện chung hợp đồng (E-ĐKC) — text chuẩn |
| Phần 3A | VII | Điều kiện cụ thể hợp đồng (E-ĐKCT) — điền giá trị cụ thể |
| Phần 4 | VIII | Biểu mẫu hợp đồng |

**Chương III — 4 mục đánh giá (theo thứ tự):**
1. Tính hợp lệ của E-HSDT (5 tiêu chí gate)
2. Năng lực và kinh nghiệm (đạt/không đạt — Bảng 01 hoặc Bảng 02)
3. Kỹ thuật (thang điểm hoặc đạt/không đạt)
4. Tài chính — E-HSĐXTC

## Phương pháp đánh giá (Điều 39)

| Phương pháp    | Tiêu chí | Phù hợp cho |
| -------------- | -------- | ----------- |
| Giá thấp nhất  | Đạt kỹ thuật → giá thấp nhất | Hàng hóa thông dụng |
| Giá đánh giá   | Đạt kỹ thuật → so sánh giá đánh giá | Hàng hóa phức tạp |
| Kết hợp KT-Giá | Điểm TH = KT × w₁ + Giá × w₂ | Phần mềm, tư vấn |

## Biểu mẫu HSMT/HSDT (NĐ 214/2025)

| Mẫu | Tên | Bên điền |
|---|---|---|
| 01A | Phạm vi cung cấp hàng hóa | Chủ đầu tư |
| 01B/C | Dịch vụ liên quan | Chủ đầu tư |
| 01E | Vật tư phụ tùng thay thế | Chủ đầu tư |
| 02A | Đơn dự thầu (tổ chức) | Nhà thầu |
| 02B | Đơn dự thầu (cá nhân/nhóm đổi mới — NĐ 214/2025 Điều 6 khoản 4) | Nhà thầu |
| 03 | Thỏa thuận liên danh | Nhà thầu |
| 04A/B | Bảo lãnh dự thầu | Ngân hàng |
| 05-07 | Lịch sử HĐ, năng lực tài chính | Nhà thầu |
| 12.1A/B/C | Bảng giá dự thầu | Nhà thầu |

## Thời hạn và giá trị mốc quan trọng

| Mốc | Thời hạn/Giá trị |
| ---- | --------------- |
| Phát hành E-HSMT trước đóng thầu | ≥ 20 ngày |
| Hiệu lực E-HSDT (thông thường) | ≥ 120 ngày |
| Bảo lãnh dự thầu | ≤ 3% giá gói thầu |
| Thời hạn hiệu lực BL dự thầu | = Hiệu lực HSDT + 30 ngày |
| Bảo đảm thực hiện HĐ | 3-10% giá HĐ (thường 5%) |
| Tạm ứng (phần mềm) | 20-30% giá HĐ |
| Thương thảo → Ký HĐ | ≤ 28 ngày |
| Nhà thầu bị khóa tài khoản khi vi phạm | 06 tháng (NĐ 214/2025 Điều 20) |
| Chi phí nộp E-HSDT | 330.000 - 500.000 đồng |
```

---

## `khung-kien-truc-cpdt-summary.md` — Tạo khi ministry = BXD hoặc BTTTT

```markdown
# Khung Kiến trúc CPĐT Việt Nam phiên bản 3.0

**Căn cứ:** QĐ 2323/QĐ-BTTTT ngày 31/12/2024
**Thay thế:** Khung v2.0 (QĐ 2426/QĐ-BTTTT 2019)

## Tầng kiến trúc (6 tầng)

| Tầng                  | Nội dung                                     |
| --------------------- | -------------------------------------------- |
| 1. Nghiệp vụ          | Quy trình, dịch vụ công, thủ tục hành chính  |
| 2. Dữ liệu            | CSDL dùng chung, chia sẻ dữ liệu, dữ liệu mở |
| 3. Ứng dụng           | Ứng dụng nội bộ, dịch vụ công trực tuyến     |
| 4. Công nghệ          | Hạ tầng kỹ thuật, Cloud, ATTT                |
| 5. An toàn thông tin  | Theo 4 cấp (TCVN 11930)                      |
| 6. Chỉ đạo và quản lý | Tổ chức, nhân sự CPĐT                        |

## Yêu cầu khi lập TKCS/TKCT

Dự án CNTT phải mapping với Khung Kiến trúc CPĐT:

- Ứng dụng phải nằm trong kiến trúc ứng dụng của Bộ/ngành
- Dữ liệu phải kết nối LGSP (Local Government Service Platform)
- Hệ thống phải tuân thủ ATTT cấp 3+ (QCVN 109)
- API phải theo chuẩn kết nối NGSP (National Government Service Platform)
```

---

## `bcctdt-phap-ly.md` — Tạo khi doc-type = Báo cáo chủ trương đầu tư (DT-04)

```markdown
# Pháp lý cho Báo cáo đề xuất chủ trương đầu tư (BCCTDT)

**Căn cứ chính:** Luật Đầu tư công số 58/2024/QH15, Điều 33; NĐ 45/2026/NĐ-CP, Điều 10-11
**Thay thế:** Luật ĐTC 2019 (hết hiệu lực 01/01/2025), NĐ 73/2019 (hết 01/03/2026)

## Nội dung bắt buộc theo Luật 58/2024 Điều 33

| Khoản | Nội dung bắt buộc | Section trong outline |
|---|---|---|
| 1a | Sự cần thiết đầu tư | 2.1 |
| 1b | Các điều kiện để thực hiện đầu tư | 2.2 |
| 1c | Sự phù hợp với quy hoạch có liên quan | 2.3 |
| 2  | Mục tiêu, quy mô, địa điểm, phạm vi | 3.1-3.3 |
| 3  | Tổng mức đầu tư dự kiến và cơ cấu nguồn vốn | 4.1-4.2 |
| 4  | Dự kiến tiến độ và kế hoạch bố trí vốn | 5 |
| 5  | Sơ bộ chi phí vận hành sau khi hoàn thành | 6 |
| 6  | Tác động môi trường, xã hội; hiệu quả KT-XH | 7.1-7.4 |
| 7  | Phân chia các dự án thành phần (nếu có) | 8 |
| 8  | Giải pháp tổ chức thực hiện | 9.1-9.3 |

## Phương pháp xác định tổng mức đầu tư (NĐ 45/2026 Điều 10 khoản 2)

| Phương pháp | Khi nào dùng | Yêu cầu tài liệu |
|---|---|---|
| So sánh | Có dự án tương tự đã hoàn thành | Dẫn chiếu dự án, hệ số điều chỉnh |
| Chuyên gia | Không có dự án tương tự | Thành lập tổ chuyên gia, biên bản họp |
| Báo giá | Thiết bị/phần mềm xác định rõ | Ít nhất 3 báo giá từ nhà cung cấp |

## Phân loại nhóm dự án (Luật 58/2024, NĐ 45/2026 Điều 9)

| Nhóm | Tổng mức đầu tư CNTT | Cấp quyết định chủ trương | Cấp quyết định đầu tư |
|---|---|---|---|
| A | ≥ 1.600 tỷ đồng | Quốc hội / Thủ tướng | Thủ tướng |
| B | 90 tỷ – < 1.600 tỷ | Bộ trưởng / Chủ tịch HĐND tỉnh | Bộ trưởng / Chủ tịch tỉnh |
| C | < 90 tỷ đồng | Bộ trưởng / Chủ tịch HĐND tỉnh | Bộ trưởng / Chủ tịch tỉnh |

*Ngưỡng cũ NĐ 73/2019 (A≥200 tỷ, B 15-200 tỷ, C<15 tỷ) ĐÃ HẾT HIỆU LỰC*

## Danh mục căn cứ pháp lý mẫu cho BCCTDT CNTT (2026)

Thứ tự: Luật → NĐ → TT → QĐ → Văn bản chỉ đạo

**Pháp luật chuyên ngành CNTT (đã xác nhận hiệu lực):**
- Luật Công nghệ thông tin số 67/2006/QH11
- Luật An toàn thông tin mạng số 86/2015/QH13
- Luật Giao dịch điện tử số 20/2023/QH15
- Luật Dữ liệu số 60/2024/QH15
- Nghị định số 13/2023/NĐ-CP về bảo vệ dữ liệu cá nhân

**Pháp luật CNTT mới 2025 — [CẦN VERIFY trước khi viện dẫn]:**
- Luật Công nghiệp công nghệ số số 71/2025/QH15
- Luật Chuyển đổi số số 148/2025/QH15
- Luật Trí tuệ nhân tạo số 134/2025/QH15
- Luật An ninh mạng số 116/2025/QH15
- Luật Bảo vệ dữ liệu cá nhân số 91/2025/QH15
- Luật Bảo vệ bí mật nhà nước số 117/2025/QH15
- Luật Ngân sách nhà nước số 89/2025/QH15
*→ Tất cả luật 2025 này: doc-writer BẮT BUỘC WebSearch verify "còn hiệu lực" trước khi viện dẫn*

**Pháp luật đầu tư và quản lý dự án:**
- Luật Đầu tư công số 58/2024/QH15
- Luật Đấu thầu số 22/2023/QH15
- Nghị định số 45/2026/NĐ-CP về quản lý đầu tư ứng dụng CNTT

**Tài chính:**
- Thông tư số 04/2020/TT-BTTTT (lập dự toán phần mềm)

## Lưu ý quan trọng cho doc-writer

1. Tiêu đề section 2 phải đúng nguyên văn theo Luật 58/2024:
   "Sự cần thiết đầu tư, các điều kiện để thực hiện đầu tư, đánh giá về sự phù hợp với quy hoạch có liên quan theo quy định của pháp luật về quy hoạch"

2. Section 2.2 "Điều kiện thực hiện" — KHÔNG phải "Điều kiện cần thiết":
   Phân tích đủ 4 chiều: pháp lý / vốn / năng lực tổ chức / hạ tầng kỹ thuật

3. Section 6 "Chi phí vận hành" — nhiều đơn vị hay bỏ sót:
   Bắt buộc ước tính bảo hành + bảo trì + vận hành cho ít nhất 3-5 năm đầu

4. Phần B (Tổng mức đầu tư): phương pháp phải dẫn chiếu đúng NĐ 45/2026 Điều 10 khoản 2
```
