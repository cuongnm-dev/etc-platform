# ref-snippets.md — Reusable Content Snippets

Tạo files trong `reference/snippets/`. Level theo Phase 4 feature flag:

- **Full**: tất cả snippets
- **Minimal**: chỉ `can-cu-phap-ly` + `phuong-phap-tinh`
- **None**: không tạo

## TODO — Snippets cần tạo thêm (F-29)

| Snippet | Ưu tiên | Nguồn |
|---|---|---|
| `hsmt-template/chuong-I-chi-dan.md` | HIGH | Mẫu 1A NĐ 24/2024 Chương I |
| `hsmt-template/chuong-II-bang-du-lieu.md` | HIGH | Mẫu 1A Chương II |
| `hsmt-template/chuong-III-tieu-chuan.md` | HIGH | Mẫu 1A Chương III |
| `hsmt-template/chuong-IV-bieu-mau.md` | HIGH | Mẫu 1A Chương IV |
| `hsmt-template/chuong-VI-hop-dong.md` | MEDIUM | Mẫu 1A Chương VI |
| `du-toan/expert-judgment-template.md` | MEDIUM | TT 04/2020 phương pháp chuyên gia |
| `du-toan/analogy-template.md` | MEDIUM | TT 04/2020 phương pháp so sánh |

Khi snippets chưa có → doc-writer tự draft từ legal refs + web search.
Khi user cung cấp mẫu chuẩn → update snippets cho dự án sau.

---

## `can-cu-phap-ly/dau-tu-cntt.md`

```markdown
# Căn cứ pháp lý — Đầu tư ứng dụng CNTT

## Snippet (customize tên dự án + đơn vị)

Căn cứ các văn bản quy phạm pháp luật sau:

- Luật Công nghệ thông tin số 67/2006/QH11 ngày 29 tháng 6 năm 2006;
- Luật An toàn thông tin mạng số 86/2015/QH13 ngày 19 tháng 11 năm 2015;
- Nghị định số 73/2019/NĐ-CP ngày 05 tháng 9 năm 2019 của Chính phủ quy định quản lý đầu tư ứng dụng công nghệ thông tin sử dụng nguồn vốn ngân sách nhà nước;
- Thông tư số 04/2020/TT-BTTTT ngày 24 tháng 02 năm 2020 của Bộ Thông tin và Truyền thông quy định về lập và quản lý chi phí đầu tư ứng dụng công nghệ thông tin;
- Thông tư số 12/2020/TT-BTTTT ngày 29 tháng 5 năm 2020 của Bộ Thông tin và Truyền thông sửa đổi, bổ sung một số điều của Thông tư số 04/2020/TT-BTTTT;
- Quyết định số [CẦN BỔ SUNG: số QĐ phê duyệt chủ trương] ngày [CẦN BỔ SUNG] của [CẦN BỔ SUNG: cấp phê duyệt] về việc phê duyệt chủ trương đầu tư dự án [CẦN BỔ SUNG: tên dự án];

<!-- BXD: thêm -->
<!-- - Quyết định số 2323/QĐ-BTTTT ngày 31/12/2024 ban hành Khung Kiến trúc CPĐT VN v3.0; -->

<!-- BCA: thêm -->
<!-- - Luật An ninh mạng số 24/2018/QH14 ngày 12/6/2018; -->
<!-- - Thông tư số 31/2019/TT-BCA về bảo đảm ATTT trong CAND; -->
```

---

## `can-cu-phap-ly/dau-thau.md`

```markdown
# Căn cứ pháp lý — Đấu thầu

## Snippet

Căn cứ các văn bản quy phạm pháp luật sau:

- Luật Đấu thầu số 22/2023/QH15 ngày 23 tháng 6 năm 2023;
- Nghị định số 24/2024/NĐ-CP ngày 27 tháng 02 năm 2024 của Chính phủ quy định chi tiết một số điều và biện pháp thi hành Luật Đấu thầu về lựa chọn nhà thầu;
- Thông tư số [CẦN BỔ SUNG] của Bộ Kế hoạch và Đầu tư hướng dẫn việc cung cấp, đăng tải thông tin đấu thầu;
- Quyết định số [CẦN BỔ SUNG] phê duyệt kế hoạch lựa chọn nhà thầu gói thầu [CẦN BỔ SUNG: tên gói thầu];
```

---

## `gioi-thieu-don-vi/template.md`

```markdown
# Giới thiệu đơn vị — Template

## Snippet (customize hoàn toàn)

### Thông tin chung

[CẦN BỔ SUNG: Tên đơn vị] được thành lập theo Quyết định số [CẦN BỔ SUNG] ngày [CẦN BỔ SUNG] của [CẦN BỔ SUNG: cấp thành lập], hoạt động trong lĩnh vực [CẦN BỔ SUNG].

### Năng lực và kinh nghiệm

Đơn vị có đội ngũ [CẦN BỔ SUNG: số lượng] cán bộ, trong đó:

- [CẦN BỔ SUNG] tiến sĩ/thạc sĩ chuyên ngành CNTT;
- [CẦN BỔ SUNG] kỹ sư có chứng chỉ quốc tế (AWS, Azure, PMP...);
- [CẦN BỔ SUNG] năm kinh nghiệm triển khai dự án CNTT quy mô lớn.

### Dự án tiêu biểu

| STT | Tên dự án     | Chủ đầu tư    | Giá trị       | Thời gian     | Kết quả        |
| --- | ------------- | ------------- | ------------- | ------------- | -------------- |
| 1   | [CẦN BỔ SUNG] | [CẦN BỔ SUNG] | [CẦN BỔ SUNG] | [CẦN BỔ SUNG] | Nghiệm thu đạt |
| 2   | [CẦN BỔ SUNG] | [CẦN BỔ SUNG] | [CẦN BỔ SUNG] | [CẦN BỔ SUNG] | Nghiệm thu đạt |
```

---

## `phuong-phap-tinh-chi-phi/tt04-2020.md`

```markdown
# Phương pháp tính chi phí — TT 04/2020

## Snippet (customize số liệu)

### Phương pháp xác định chi phí

Chi phí phần mềm nội bộ được xác định theo phương pháp điểm chức năng (Function Point) quy định tại Thông tư số 04/2020/TT-BTTTT.

#### Công thức tổng quát

$$G_{PM} = G_{NC} + G_{CDPM}$$

Trong đó:

- $G_{PM}$: Tổng chi phí phần mềm
- $G_{NC}$: Chi phí xây dựng, phát triển phần mềm
- $G_{CDPM}$: Chi phí chỉnh sửa, chuyển đổi phần mềm

#### Chi phí xây dựng phát triển

$$G_{NC} = \sum_{i=1}^{n} (S_i \times K_1 \times K_2 \times K_3 \times D)$$

| Ký hiệu | Ý nghĩa                     | Giá trị áp dụng                             |
| ------- | --------------------------- | ------------------------------------------- |
| $S_i$   | Điểm chức năng module thứ i | [CẦN BỔ SUNG: bảng FP]                      |
| $K_1$   | Hệ số ngôn ngữ lập trình    | [CẦN BỔ SUNG: theo Phụ lục I]               |
| $K_2$   | Hệ số phức tạp kỹ thuật     | [CẦN BỔ SUNG: theo Phụ lục II]              |
| $K_3$   | Hệ số đặc thù               | [CẦN BỔ SUNG: theo Phụ lục III, TT 12/2020] |
| $D$     | Đơn giá nhân công           | [CẦN BỔ SUNG: đ/người-tháng, năm {year}]    |

#### Bảng tổng hợp chi phí

| STT | Nội dung                       | Thành tiền (đồng) | Ghi chú               |
| --- | ------------------------------ | ----------------- | --------------------- |
| I   | Chi phí xây dựng PM ($G_{NC}$) | [CẦN BỔ SUNG]     | Theo bảng FP          |
| II  | Chi phí chỉnh sửa ($G_{CDPM}$) | [CẦN BỔ SUNG]     | Nếu có                |
| III | Chi phí quản lý dự án          | [CẦN BỔ SUNG]     | 5-10% × I             |
| IV  | Chi phí tư vấn                 | [CẦN BỔ SUNG]     | Theo hợp đồng         |
| V   | Dự phòng                       | [CẦN BỔ SUNG]     | ≤ 10% × (I+II+III+IV) |
|     | **Tổng cộng**                  | **[CẦN BỔ SUNG]** |                       |
```

---

## `tieu-chuan-ky-thuat/cntt-chung.md`

```markdown
# Tiêu chuẩn kỹ thuật CNTT — Snippet chung

## Snippet

### Tiêu chuẩn áp dụng

Hệ thống tuân thủ các tiêu chuẩn, quy chuẩn kỹ thuật sau:

| STT | Tiêu chuẩn              | Nội dung                                                  |
| --- | ----------------------- | --------------------------------------------------------- |
| 1   | QCVN 109:2017/BTTTT     | Quy chuẩn kỹ thuật quốc gia về tiếp cận web               |
| 2   | TCVN 11930:2017         | CNTT — Kỹ thuật an toàn — Yêu cầu cơ bản về ATTT hệ thống |
| 3   | TCVN ISO/IEC 27001:2019 | Hệ thống quản lý an toàn thông tin                        |
| 4   | TCVN ISO/IEC 25010:2015 | Mô hình chất lượng phần mềm                               |
| 5   | TCVN 8709               | Tiêu chí đánh giá an toàn CNTT                            |

### Yêu cầu an toàn thông tin

Hệ thống được thiết kế đáp ứng yêu cầu bảo đảm an toàn thông tin cấp [CẦN BỔ SUNG: 1-5] theo TCVN 11930:2017, bao gồm:

- Xác thực: [CẦN BỔ SUNG: phương thức]
- Phân quyền: Theo mô hình RBAC (Role-Based Access Control)
- Mã hóa: TLS 1.2+ cho truyền tải, AES-256 cho lưu trữ
- Ghi log: Mọi thao tác người dùng, lưu trữ ≥ [CẦN BỔ SUNG] tháng
- Sao lưu: [CẦN BỔ SUNG: tần suất], lưu trữ ≥ [CẦN BỔ SUNG] năm
```
