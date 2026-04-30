# ref-interview-questions.md — Doc-Type-Specific Interview Questions

**Dùng bởi:** SKILL.md § Step 2, doc-orchestrator (DCB init)
**Nguyên tắc:** Interview phải: specific, prerequisite-aware, gate-blocking, VALIDATED.

---

## Quy tắc chung (áp dụng tất cả doc types)

**Khi hỏi — YÊU CẦU data thật, không chấp nhận câu mơ hồ:**
- Câu trả lời "hệ thống cũ không hiệu quả" → Hỏi lại: "Không hiệu quả cụ thể là sao? Bao nhiêu hồ sơ/tháng? Mất bao nhiêu ngày?"
- Câu trả lời "khoảng 3-4 module" → Hỏi: "Tên cụ thể từng module là gì? Chức năng chính của mỗi module?"
- Câu trả lời "ngân sách tầm vài tỷ" → Hỏi: "Con số cụ thể? Phân bổ sơ bộ PM/HT/ĐT?"

**Follow-up bắt buộc khi câu trả lời thiếu số liệu:**
```
"Bạn đề cập đến {vấn đề}, để tài liệu có sức thuyết phục, tôi cần:
 - Số liệu hiện tại: {cụ thể cần gì}
 - So sánh: {với SLA / với đơn vị tương đương / với yêu cầu pháp lý}
 Nếu chưa có số liệu chính xác, hãy ước tính và tôi sẽ đánh dấu [ƯỚC TÍNH — cần xác nhận]"
```

---

## Interview: TKCS (DT-01) — 12 câu

```
Prerequisite HARD: QĐ phê duyệt chủ trương [có → số QĐ, ngày, cơ quan ký / chưa → GATE BLOCK]
Prerequisite SOFT: NCKT [có → load phạm vi, phương án tech / chưa → OK, hỏi thêm]

═══ Bắt buộc (gate-blocking) ═══

1. Tên dự án đầy đủ + Đơn vị chủ đầu tư (tên đầy đủ, địa chỉ)?

2. Phạm vi: Bao nhiêu module/hệ thống?
   → MÔ TẢ TỪNG MODULE: (a) tên module, (b) chức năng chính, (c) người dùng chính
   → VALIDATE sau: "Bạn nói {N} modules — tôi đã ghi nhận {M}. {Bổ sung | OK}"

3. Vấn đề hiện tại cần giải quyết (cụ thể):
   a) Hệ thống/quy trình nào đang gây vấn đề? Tên, năm triển khai, nhà cung cấp?
   b) Vấn đề cụ thể là gì? (không hỗ trợ ký số / không tích hợp LGSP / quá tải / ...)
   c) Số liệu thiệt hại: bao nhiêu hồ sơ/văn bản/giao dịch mỗi tháng? Mất bao nhiêu ngày?
   d) Bao nhiêu CBCC/người dân bị ảnh hưởng trực tiếp?

4. Đối tượng sử dụng: CBCC nội bộ / người dân / doanh nghiệp / cả hai?
   → Nếu hỗn hợp: bao nhiêu % mỗi loại?

5. Yêu cầu tích hợp: LGSP? NDXP? VNeID? CSDLQG? Hệ thống legacy nào?
   → Với mỗi tích hợp: giao thức dự kiến? dữ liệu chia sẻ gì?

6. Yêu cầu phi chức năng:
   a) Concurrent users dự kiến (peak)?
   b) Uptime SLA (%)?
   c) Cấp ATTT (cấp 1/2/3 theo TCVN 11930)?
   d) Response time yêu cầu?

7. Hạ tầng: on-prem / cloud / hybrid? TTDL hiện có (tên, địa điểm, Tier)?

8. Tech stack dự kiến: Java / .NET / Python / Node.js?
   Database: PostgreSQL / Oracle / SQL Server?
   → Quan trọng cho K₁ trong Dự toán downstream

9. Ngân sách khung + phân bổ sơ bộ:
   a) Tổng mức dự kiến: {X đồng}
   b) PM (phần mềm): ~?%
   c) Hạ tầng/thiết bị: ~?%
   d) Đào tạo + triển khai: ~?%
   e) Quản lý dự án: ~?%
   f) Dự phòng: 10% hay tỷ lệ khác?

═══ Recommended (không block) ═══

10. Có kiến trúc tham khảo hoặc dự án tương tự ở đơn vị khác?
11. Timeline mong muốn: bắt đầu quý/năm nào? Kết thúc?
12. Migration từ hệ thống cũ? Volume data cần migrate?

═══ Section notes (cho orchestrator) ═══
Section 6 "Dự toán sơ bộ": CHỈ ước tính rough (% per hạng mục). KHÔNG dùng TT 04 formula.
```

---

## Interview: TKCT (DT-02) — 8 câu

```
Prerequisite HARD: TKCS được duyệt [có → load + auto-populate / chưa → GATE BLOCK]
  → Auto-load: kiến trúc, module list, NFR, tech stack, tích hợp từ TKCS dcb.md

═══ Bắt buộc ═══

1. TKCS path (để kế thừa data)?
   → VALIDATE: TKCS status = DONE trong _doc_state.md

2. Module nào trong TKCT đợt này?
   (có thể < tổng modules TKCS nếu phân kỳ)
   → Nếu phân kỳ: đợt sau gồm module nào?

3. Database engine: PostgreSQL / Oracle / SQL Server?
   (nếu TKCS đã ghi → xác nhận lại / nếu chưa → bắt buộc hỏi)

4. API standard: REST / SOAP / GraphQL?
   → Với từng integration endpoint?

5. Authentication: LDAP / SSO / VNeID / mixed?
   → Ma trận phân quyền: bao nhiêu vai trò? RBAC hay ABAC?

6. Có yêu cầu migration?
   → Từ hệ thống nào? Volume data (số bản ghi, dung lượng)?
   → Chiến lược: big bang / phased / parallel run?

7. Coding standards: có conventions riêng?
   (naming convention, branching strategy, code review process)

8. Test strategy:
   → Unit test: coverage target?
   → Integration test: automated hay manual?
   → UAT: ai thực hiện? bao nhiêu kịch bản?
   → CI/CD: công cụ gì? (Jenkins/GitLab CI/GitHub Actions?)

═══ Writing rules (cho orchestrator) ═══
Sections >10 trang (module design, DB) → CHIA NHỎ: 1 writer/module
Circular deps (module ↔ DB ↔ API) → 2-pass: rough draft → refine
```

---

## Interview: Dự toán (DT-03) — 9 câu

```
Prerequisite HARD: TKCS hoặc TKCT [có → auto-load module list / chưa → GATE BLOCK]

═══ Bắt buộc ═══

1. TKCS/TKCT path → auto-load: danh mục module + chức năng + tech stack

2. Phương pháp dự toán:
   A) Function Point (IFPUG) — chuẩn nhất, TT 04/2020
   B) Expert Judgment — ước tính chuyên gia
   C) Analogy — so sánh dự án tương tự
   → Cơ quan thẩm định yêu cầu phương pháp nào?

3. Ngôn ngữ lập trình → K₁:
   (nếu TKCS đã ghi → auto-load / nếu chưa → hỏi)
   → Java/C# = K₁ = 1.0 | Python = 1.2 | PHP = 0.8 | ...

4. Vùng lương (TT 04/2020, Phụ lục IV):
   Vùng I (Hà Nội, TP.HCM) / Vùng II / Vùng III / Vùng IV?

5. Năm đơn giá: {current year}
   → doc-writer PHẢI web search verify đơn giá thực tế năm này

6. Có hạng mục phần cứng/hạ tầng?
   → Nếu có: danh mục thiết bị từ TKCS Section 4 → auto-load

7. Có hạng mục đào tạo, triển khai, bảo hành?
   → Bao nhiêu ngày/người cho đào tạo?
   → Bảo hành: bao nhiêu năm sau go-live?

8. Dự phòng: 10% (mặc định theo TT 04) hay tỷ lệ khác?
   → Lý do nếu khác 10%?

9. Đơn vị thẩm định dự toán:
   → Ai thẩm định? Có yêu cầu format đặc biệt?

═══ Content rules ═══
Bảng FP: AI tạo TEMPLATE structure → flag [ƯỚC TÍNH — cần chuyên gia verify]
Hệ số K₁/K₂/K₃: CHÉP từ snippet Phụ lục TT 04/2020, KHÔNG tự sáng tạo
Đơn giá D: web search "{vùng} đơn giá nhân công CNTT {năm}" → verify
```

---

## Interview: Báo cáo chủ trương (DT-04) — 16 câu

```
Prerequisite: Không bắt buộc doc trước.
Prerequisite SOFT: Đề án CĐS [có → auto-load initiative + dedup / chưa → hỏi đủ]

Lưu ý: BCCTDT theo Luật 58/2024/QH15 có cấu trúc 2 phần (A: Thuyết minh + B: Tổng mức đầu tư)
+ Phụ lục kỹ thuật sơ bộ. Interview phải thu thập đủ data cho CẢ 2 phần.

═══ Nhóm 1: Định danh dự án (gate-blocking) ═══

1. Tên dự án/đề án đầy đủ (chính xác theo văn bản chỉ đạo nếu có)?

2. Thông tin tổ chức:
   a) Chủ đầu tư: tên đơn vị đầy đủ, địa chỉ?
   b) Ban Quản lý dự án (nếu có giao): tên, số QĐ thành lập?
   c) Đơn vị tư vấn lập báo cáo (nếu thuê): tên đơn vị?
   d) Cấp quyết định CHỦ TRƯƠNG đầu tư: (Thủ tướng / Bộ trưởng / Chủ tịch tỉnh / HĐND)
   e) Cấp quyết định ĐẦU TƯ: (Thủ tướng / Bộ trưởng / Chủ tịch tỉnh)

3. Địa điểm và thời gian:
   a) Địa điểm thực hiện: (Toàn quốc / tỉnh... / địa chỉ cụ thể)?
   b) Thời gian thực hiện dự kiến: năm nào đến năm nào?

═══ Nhóm 2: Sự cần thiết (YÊU CẦU SỐ LIỆU CỤ THỂ) ═══

4. Hiện trạng cụ thể (KHÔNG chấp nhận mô tả chung chung):
   a) Hệ thống/quy trình nào đang gây vấn đề? Tên hệ thống, năm triển khai?
   b) Vấn đề cụ thể: bao nhiêu hồ sơ/giao dịch/văn bản/tháng? Mất bao lâu?
   c) Bao nhiêu CBCC/người dân bị ảnh hưởng trực tiếp?
   d) Thiệt hại ước tính: chi phí thừa, thời gian lãng phí?

5. Sự phù hợp với quy hoạch (BẮT BUỘC theo Luật 58/2024):
   a) Dự án có trong Kế hoạch CĐS của Bộ/tỉnh không? Tên QĐ phê duyệt?
   b) Kiến trúc CPĐT/Chính phủ số Bộ/tỉnh phiên bản mấy? Dự án map vào đâu?
   c) Quy hoạch ngành liên quan nào đã xác định nhu cầu này?

6. Điều kiện thực hiện (BẮT BUỘC theo Luật 58/2024):
   a) Khung pháp lý: có đủ căn cứ pháp lý để đầu tư chưa?
   b) Hạ tầng sẵn có: TTDL hiện tại, đường truyền, có thể tận dụng?
   c) Nhân lực CNTT nội bộ: bao nhiêu người? đủ năng lực vận hành?
   d) Nếu cần tích hợp LGSP/NGSP: đơn vị đã đăng ký/kết nối chưa?

═══ Nhóm 3: Mục tiêu và phạm vi ═══

7. Mục tiêu chính (measurable — TỐI THIỂU 3 KPI có số):
   → Giảm X% thời gian xử lý (từ Y ngày → Z ngày)
   → Phục vụ N người dùng
   → Tiết kiệm M tỷ đồng/năm
   → Đạt cấp ATTT số [1/2/3]

8. Phạm vi và quy mô:
   a) Danh sách module/hệ thống dự kiến đầu tư (tên cụ thể từng cái)?
   b) Đầu tư MỚI / nâng cấp hệ thống hiện có / mở rộng?
   c) Đơn vị/địa bàn áp dụng?

═══ Nhóm 4: Tài chính ═══

9. Tổng mức đầu tư dự kiến: {X đồng}
   → Nhóm dự án: A (≥1.600 tỷ) / B (90-1.600 tỷ) / C (<90 tỷ)?

10. Phân bổ sơ bộ (quan trọng cho downstream NCKT/TKCS):
    PM/phần mềm ~?% | Hạ tầng thiết bị ~?% | ATTT ~?% | Triển khai+ĐT ~?% | QLDA ~?% | DP ~?%

11. Nguồn vốn: NSNN Trung ương / địa phương / ODA / PPP?
    → Giai đoạn bố trí: {YYYY}: X tỷ | {YYYY}: Y tỷ

12. Phương pháp ước tính tổng mức (NĐ 45/2026 Điều 10):
    So sánh dự án tương tự / Chuyên gia / Báo giá / Kết hợp?
    → Nếu báo giá: đã có chưa?
    → Nếu so sánh: dự án nào làm cơ sở?

═══ Nhóm 5: Vận hành và tổ chức ═══

13. Chi phí vận hành sau khi hoàn thành (BẮT BUỘC theo Luật 58/2024):
    a) Bảo hành: bao nhiêu năm?
    b) Bảo trì hàng năm: ước tính X đồng/năm?
    c) Nhân lực vận hành: bao nhiêu người?

14. Phân chia dự án thành phần: Có / Không?
    → Nếu có: bao nhiêu phần? Tên mỗi phần?

15. Hình thức quản lý dự án: Chủ đầu tư tự quản lý / Ban QLDA / Tư vấn quản lý?

═══ Nhóm 6: Pháp lý và tham chiếu ═══

16. Căn cứ pháp lý và chỉ đạo đặc thù:
    a) Văn bản nào chỉ đạo/giao nhiệm vụ thực hiện dự án này (số, ngày)?
    b) Nghiệp vụ có quy định pháp lý bắt buộc số hóa không? Văn bản nào?
    c) Dự án có kinh nghiệm tương tự để tham chiếu (trong nước/quốc tế)?

═══ Section notes (cho orchestrator) ═══
Phần A Section 2.1: viết theo cấu trúc phễu: Bối cảnh → Cơ quan → Hiện trạng → Đánh giá → Kết luận
Phần A Section 2.2: BẮT BUỘC phân tích đủ 4 điều kiện (pháp lý / vốn / năng lực / hạ tầng)
Phần A Section 2.3: phải chỉ ra từng QĐ quy hoạch cụ thể + điều khoản
Phần A Section 6: BẮT BUỘC ước tính chi phí vận hành 5 năm đầu
Phần B: thuyết minh tài chính riêng, phương pháp theo NĐ 45/2026 Điều 10
```

---

## Interview: Thuyết minh (DT-05) — 8 câu

```
Prerequisite SOFT: Báo cáo chủ trương [có → skip Q1-Q6 / chưa → hỏi tương tự DT-04]

Nếu đã có Báo cáo CT → auto-load: sự cần thiết, mục tiêu, kinh phí, phạm vi
Bắt đầu từ Q7:

7. Giải pháp kỹ thuật sơ bộ:
   a) Kiến trúc dự kiến? (monolithic / microservices / ...)
   b) Tech stack sơ bộ?
   c) Tích hợp với hệ thống nào?

8. Đối tượng thụ hưởng:
   a) Trực tiếp: ai được dùng hệ thống? Bao nhiêu người?
   b) Gián tiếp: ai hưởng lợi từ kết quả hệ thống?
```

---

## Interview: HSMT (DT-06) — 17 câu

```
Prerequisite HARD: QĐ kế hoạch lựa chọn nhà thầu [có → số QĐ, ngày / chưa → GATE]
Prerequisite HARD: TKCS hoặc scope kỹ thuật [có → auto-load Chapter V / chưa → GATE]
  → Chapter V HSMT = yêu cầu kỹ thuật, PHẢI có nguồn. Nếu TKCT có → ưu tiên TKCT
Lưu ý: E-HSMT phát hành trên Hệ thống e-GP. Chapter I + VI là text chuẩn NĐ 214/2025.
Chapter V thường là file đính kèm riêng (RAR/PDF từ TKCT) — không viết inline.

═══ Nhóm 1: Định danh (gate-blocking) ═══

1. Thông tin gói thầu:
   a) Tên gói thầu đầy đủ?
   b) Số hiệu gói thầu (E-TBMT) nếu đã tạo trên hệ thống?
   c) Số QĐ ban hành E-HSMT?
   d) Ngày phát hành dự kiến?

2. Chủ đầu tư:
   a) Tên đầy đủ, địa chỉ, MST?
   b) Người nhận thông báo (họ tên + chức vụ + email)?

3. Dự án/dự toán mua sắm liên quan (tên chính xác)?

═══ Nhóm 2: Cấu trúc đấu thầu ═══

4. Loại gói thầu: Phần mềm / Hàng hóa thiết bị / EPC / Hỗn hợp?
   → Phần mềm: Chapter V viết inline
   → Hàng hóa: Chapter V thường đính kèm từ hồ sơ thiết kế TKCT

5. Phương thức LCNT:
   a) Đấu thầu rộng rãi / hạn chế / chỉ định thầu / chào hàng cạnh tranh?
   b) Số túi hồ sơ: Một túi / Hai túi (kỹ thuật + tài chính)?
   → Mặc định CNTT: một giai đoạn hai túi hồ sơ

6. Loại hợp đồng:
   → Trọn gói / Đơn giá cố định / Đơn giá điều chỉnh?
   → Phần mềm: thường Trọn gói hoặc Đơn giá cố định

═══ Nhóm 3: Tham số tài chính (fill vào E-BDL) ═══

7. Giá gói thầu: {X đồng} (từ dự toán đã duyệt)
   → Nguồn vốn: NSNN / vốn tự có / vốn vay?

8. Bảo đảm dự thầu:
   a) Giá trị: {N}% × giá gói thầu (thường 1-3%, tối đa 1,5% theo Điều 61 Luật 22)?
   b) Thời hạn hiệu lực E-HSDT: ≥ [120] ngày?

9. Điều kiện hợp đồng cụ thể (E-ĐKCT):
   a) Tỷ lệ tạm ứng: {30}% giá HĐ? (thường 20-30%)
   b) Tỷ lệ bảo đảm thực hiện HĐ: {5}%? (thường 3-10%)
   c) Hình thức thanh toán: chuyển khoản theo khối lượng nghiệm thu?
   d) Phạt chậm tiến độ: {X}%/tuần, tối đa {Y}% tổng giá HĐ?

10. Thời gian thực hiện hợp đồng: {N} ngày từ ký HĐ

11. Thời gian bảo hành: {N} năm kể từ ngày nghiệm thu
    SLA bảo hành: phản hồi trong {X} giờ?

12. Thời hạn sử dụng dự kiến thiết bị (nếu có phần cứng): {N} năm
    → Yêu cầu vật tư phụ tùng thay thế: Có / Không?

═══ Nhóm 4: Tiêu chuẩn đánh giá (Chapter III) ═══

13. Phương pháp đánh giá kỹ thuật:
    → Kết hợp KT+Giá / Giá thấp nhất / Giá đánh giá?
    → Nếu Kết hợp: KT: {X}% — Giá: {Y}% (phần mềm thường: KT=70%, Giá=30%)

14. Yêu cầu năng lực nhà thầu (Mục 2 - Chương III):
    a) Kinh nghiệm: ≥{N} HĐ tương tự trong {M} năm gần nhất?
       → Định nghĩa "HĐ tương tự": [tên hàng hóa/phần mềm tương tự, giá trị tối thiểu]
    b) Doanh thu tối thiểu: {X tỷ/năm} trong {N} năm gần nhất?
    c) Giá trị tài sản ròng: > 0?
    d) Nhân sự chủ chốt (nếu có): số lượng, vị trí, chứng chỉ yêu cầu?

15. Tiêu chí đánh giá kỹ thuật (Mục 3 - Chương III):
    → LIỆT KÊ đầy đủ hoặc PASTE bảng tiêu chí
    → VALIDATE: trọng số cộng = 100% | điểm tối thiểu đạt = [70]/100
    → Nếu dùng đạt/không đạt: liệt kê yêu cầu tối thiểu từng tiêu chí

═══ Nhóm 5: Yêu cầu kỹ thuật (Chapter V) ═══

16. Nguồn dữ liệu Chapter V:
    a) Từ TKCT đã phê duyệt → path?
    b) Từ TKCS → path?
    c) Không có → phải viết từ đầu (alert: cần dữ liệu kỹ thuật đầy đủ)
    
    [Nếu gói thầu hàng hóa thiết bị:]
    → Danh mục thiết bị: STT | Tên | Đơn vị | Khối lượng | Tiêu chuẩn áp dụng?
    → Yêu cầu xuất xứ: Có / Không?
    → Dịch vụ đi kèm: lắp đặt / tích hợp / đào tạo / vận hành thử?

17. Hội nghị tiền đấu thầu: Có / Không?
    → Nếu có: ngày, địa điểm dự kiến?

═══ Content rules (cho orchestrator) ═══
Chapter I: text chuẩn NĐ 214/2025 — chỉ điền tên gói thầu, tham chiếu E-BDL
Chapter II (E-BDL): điền mapping E-CDNT X.X → giá trị cụ thể từ Q1-Q17
Chapter III Mục 1: 5 tiêu chí hợp lệ cố định theo NĐ 214/2025
Chapter III Mục 2: Bảng 01 (không phải NSX) hoặc Bảng 02 (là NSX)
Chapter V: nếu có TKCT → extract + reformat. Nếu không → viết đầy đủ
Chapter VI (E-ĐKC): text chuẩn cố định
Chapter VII (E-ĐKCT): điền giá trị cụ thể từ Q9
```

---

## Interview: HSDT (DT-07) — 8 câu

```
Prerequisite HARD: HSMT [có → auto-load yêu cầu, tiêu chí / chưa → GATE BLOCK]
Prerequisite HARD: TKCS + Dự toán [có → auto-load giải pháp + giá / chưa → GATE]

═══ Bắt buộc ═══

1. HSMT path → auto-load: yêu cầu kỹ thuật, tiêu chí đánh giá

2. TKCS path → auto-load: giải pháp kỹ thuật (sẽ reframe sang voice nhà thầu)

3. Dự toán path → auto-load: bảng giá (để tạo bảng giá dự thầu template)

4. Thông tin đơn vị dự thầu:
   a) Tên đầy đủ (theo giấy phép kinh doanh)
   b) Mã số thuế
   c) Đại diện pháp luật: họ tên + chức danh
   d) Địa chỉ đăng ký

5. Có liên danh?
   → Có: tên các thành viên, tỷ lệ phần công việc, đơn vị đứng đầu liên danh
   → Không: bỏ qua

6. Giá dự thầu: [CẦN QUYẾT ĐỊNH kinh doanh]
   → AI gợi ý: ≤ giá gói thầu, thường 92-97% giá gói
   → User phải quyết định con số cuối

7. Nhân sự chủ chốt đề xuất:
   → Số lượng, vị trí từng người, kinh nghiệm tóm tắt
   → User PHẢI cung cấp CV thật → AI tạo template từ CV

8. Danh mục hợp đồng tương tự (≥3 hợp đồng):
   → User PHẢI cung cấp: tên HĐ, chủ đầu tư, giá trị, năm, kết quả
   → AI tạo bảng template

═══ Section flags ═══
Section 4 (Năng lực): AI tạo structure → user PHẢI tự điền 100% data nội bộ
Section 7 (Bảng giá): copy dự toán + [CẦN QUYẾT ĐỊNH: giá dự thầu]
```

---

## Interview: NCKT (DT-08) — 10 câu

```
Prerequisite SOFT: QĐ chủ trương hoặc Đề án CĐS
  → Từ Đề án: auto-load initiative-portfolio + dedup-report → ~40% pre-filled

═══ Bắt buộc ═══

1. Tên dự án + Mục tiêu chính (1 câu, measurable)?

2. Phạm vi: module, hệ thống, đơn vị áp dụng?

3. Phương án 1 — mô tả ĐỦ:
   a) Tên phương án
   b) Approach kỹ thuật (mua sản phẩm COTS / phát triển mới / tùy biến OSS)
   c) Tech stack chính
   d) Ước tính chi phí sơ bộ

4. Phương án 2 — mô tả ĐỦ (tương tự)
   → GATE: ≥2 phương án MÔ TẢ ĐỦ. "Sẽ bổ sung sau" = GATE BLOCK

5. Tiêu chí so sánh phương án:
   → Chi phí / Timeline / Rủi ro kỹ thuật / Khả năng mở rộng / Phù hợp chính sách?
   → Trọng số mỗi tiêu chí?

6. Nguồn vốn dự kiến: NSNN (cấp Bộ/tỉnh) / ODA / PPP?

7. Timeline sơ bộ: năm bắt đầu — năm kết thúc?

8. Hiệu quả dự kiến (ĐỊNH LƯỢNG — bắt buộc):
   a) Số hồ sơ/giao dịch hiện tại xử lý/tháng?
   b) Thời gian trung bình hiện tại?
   c) Sau dự án: ước tính giảm bao nhiêu % thời gian / nhân lực?
   d) Số người dân/doanh nghiệp thụ hưởng?
   → Nếu chưa có số liệu → ước tính và đánh dấu [ƯỚC TÍNH — cần xác nhận]

9. Rủi ro chính: kỹ thuật / tổ chức / tài chính?
   → Biện pháp giảm thiểu cho từng rủi ro?

10. Cơ quan thẩm định dự án? Đã thẩm định chưa?
```

---

## Post-Interview Validation (TẤT CẢ doc types)

```
Sau interview, VALIDATE trước khi tạo project:

1. Prerequisite check: PASS / FAIL
2. Module count: khai báo {N} → mô tả {M} → {match / MISMATCH — hỏi bổ sung}
3. Phương án count (NCKT): khai báo {N} → mô tả {M}
4. Số liệu cụ thể: có ít nhất 2 data point có số thật trong § Sự cần thiết?
5. Inherited data: loaded {X} fields từ {source doc}
6. Critical fields: {K} / {total} filled → nếu <80% → cảnh báo
7. Human-fill sections: {list} → user biết trước phải tự điền

Output validation card:
━━━ Interview Summary ━━━
  Doc type:      {type}
  Questions:     {N} answered
  Prerequisites: {PASS / FAIL: {reason}}
  Inherited:     {M} fields từ {source}
  Số liệu thật:  {có / THIẾU: {fields}}
  Critical gaps: {list hoặc "none"}
  Human-fill:    {list hoặc "none"}
  
  Proceed? (yes / bổ sung {field})
━━━━━━━━━━━━━━━━━━━━━━━━
```
