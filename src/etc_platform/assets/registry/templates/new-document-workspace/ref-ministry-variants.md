# ref-ministry-variants.md — Ministry-Specific Configuration

Tạo files trong `reference/ministry/` khi ministry ≠ Generic.

---

## `bxd-specifics.md` — Bộ Xây dựng

```markdown
# Bộ Xây dựng (BXD) — Đặc thù

## Tiêu chuẩn bổ sung

| Tiêu chuẩn                  | Áp dụng khi                          |
| --------------------------- | ------------------------------------ |
| TCVN 9377-1:2012            | Hệ thống quản lý công trình xây dựng |
| QCVN 12:2014/BXD            | Phần mềm quản lý dự án xây dựng      |
| BIM Roadmap (QĐ 258/QĐ-BXD) | Dự án áp dụng BIM level 2+           |
| TCVN ISO 19650              | Quản lý thông tin BIM                |

## Hệ thống hiện hành BXD

| Hệ thống      | Vai trò                      | Kết nối                    |
| ------------- | ---------------------------- | -------------------------- |
| LGSP BXD      | Nền tảng tích hợp            | API gateway                |
| Cổng DVC BXD  | Dịch vụ công trực tuyến      | Cần tích hợp nếu liên quan |
| CSDL ngành XD | Dữ liệu quy hoạch, giấy phép | Kết nối nếu cần            |

## Quy trình phê duyệt

- TKCS: Cục CNTT BXD thẩm định (dự án nhóm B, C)
- TKCT: Chủ đầu tư tổ chức thẩm định, Cục CNTT tham gia
- Dự toán: Phải có ý kiến Cục CNTT trước khi phê duyệt

## Template overrides

| Section            | Override                                  |
| ------------------ | ----------------------------------------- |
| Kiến trúc hệ thống | Bắt buộc mapping với Kiến trúc CPĐT BXD   |
| Hạ tầng kỹ thuật   | Ưu tiên sử dụng TTDL của BXD              |
| Bảo mật            | ATTT cấp 3 (QCVN 109) cho hệ thống nội bộ |
| Kết nối            | API RESTful theo chuẩn LGSP               |

## Văn phong đặc thù

- Dùng "công trình" thay vì "project" khi nói về xây dựng
- Dùng "thiết kế bản vẽ thi công" song song với "thiết kế chi tiết CNTT"
- Viện dẫn Luật Xây dựng 2014 (sửa đổi 2020) khi liên quan
```

---

## `bca-specifics.md` — Bộ Công an

```markdown
# Bộ Công an (BCA) — Đặc thù

## Phân loại bảo mật

| Cấp       | Áp dụng                           | Yêu cầu                |
| --------- | --------------------------------- | ---------------------- |
| Mật       | Hệ thống nội bộ thông thường      | ATTT cấp 3+            |
| Tối mật   | Hệ thống nghiệp vụ, CSDL quốc gia | ATTT cấp 4, mạng riêng |
| Tuyệt mật | An ninh quốc gia                  | Cấp 4+, mạng cách ly   |

## Hạ tầng mạng

| Mạng                                    | Đặc điểm                                    |
| --------------------------------------- | ------------------------------------------- |
| Mạng truyền số liệu chuyên dùng (TSLCD) | Mạng riêng BCA, không kết nối Internet      |
| Mạng nội bộ ngành                       | Kết nối các đơn vị trực thuộc               |
| Mạng Internet                           | Chỉ cho hệ thống DVC, tách biệt mạng nội bộ |

## Quy định bổ sung

| Quy định               | Nội dung                               |
| ---------------------- | -------------------------------------- |
| TT 31/2019/TT-BCA      | Bảo đảm ATTT trong CAND                |
| QĐ nội bộ BCA          | Quy trình phát triển PM trong ngành CA |
| Luật An ninh mạng 2018 | Áp dụng cho mọi hệ thống               |

## Yêu cầu đặc biệt cho TKCS/TKCT

- **Đánh giá ATTT:** Bắt buộc trước khi phê duyệt TKCS
- **Kiểm tra mã nguồn:** Bắt buộc cho phần mềm tùy chỉnh
- **Triển khai trên mạng TSLCD:** Phần mềm nghiệp vụ không được triển khai trên Internet
- **Mã hóa dữ liệu:** AES-256+ cho dữ liệu lưu trữ, TLS 1.3 cho truyền tải
- **Xác thực:** PKI hoặc smart card, không dùng password đơn thuần
- **Log & Audit:** Bắt buộc ghi log mọi thao tác, lưu trữ ≥ 3 năm

## Template overrides

| Section   | Override                                                                 |
| --------- | ------------------------------------------------------------------------ |
| Bảo mật   | Mục riêng: "Phân tích rủi ro ATTT" + "Phương án bảo mật theo TT 31/2019" |
| Hạ tầng   | Phân biệt rõ: mạng Internet / mạng TSLCD / mạng nội bộ                   |
| Kiến trúc | Bắt buộc sơ đồ phân vùng mạng (DMZ, internal, isolated)                  |
| Vận hành  | Kế hoạch vận hành 24/7, SOC (Security Operations Center)                 |

## Văn phong đặc thù

- Dùng "Công an nhân dân" (CAND), không dùng "lực lượng công an"
- Dùng "đồng chí" khi nói về nhân sự BCA
- Viện dẫn Luật Công an nhân dân 2018 khi liên quan nhân sự/tổ chức
- Không ghi thông tin chi tiết về hệ thống an ninh trong tài liệu mật thấp
```

---

## Variant Application Rules

Khi scaffold, orchestrator áp dụng ministry variant như sau:

1. **Copy variant file** vào `reference/ministry/`
2. **Inject variant overrides** vào outline: thêm note dưới mỗi section header bị override
3. **Update DCB template**: thêm ministry-specific fields
4. **Update legal references**: thêm quy định đặc thù của bộ

Orchestrator đọc variant file trước mỗi dispatch → inject relevant overrides vào writer context.
