#!/usr/bin/env python3
"""End-to-end NCKT validate + render smoke test."""
import sys, json, tempfile, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, "src")

from pathlib import Path
from etc_platform.engines import docx as docx_engine
from etc_platform.data.validation import validate_content_data
from etc_platform.data.quality_checks import MINIMUMS

prose = (
    "Hệ thống được triển khai theo quy định tại Nghị định số 45/2026/NĐ-CP "
    "ngày 15 tháng 02 năm 2026 của Chính phủ về quản lý đầu tư ứng dụng "
    "công nghệ thông tin sử dụng nguồn vốn ngân sách nhà nước. Quy mô triển "
    "khai bao gồm 54 trại giam và 163 phân trại trên toàn quốc, phục vụ "
    "khoảng 12.500 cán bộ chiến sĩ và xử lý ước tính 250.000 hồ sơ thi hành "
    "án mỗi năm. Đầu tư mới hệ thống nhằm thay thế các quy trình thủ công "
    "với thời gian xử lý trung bình 8 ngày/hồ sơ xuống còn 3 ngày, đồng thời "
    "bảo đảm an toàn thông tin cấp độ 3 theo Nghị định số 85/2016/NĐ-CP."
)

required = MINIMUMS["nckt"]["required_sections"]
overrides = MINIMUMS["nckt"]["sections_min_words_overrides"]

sections = {}
for k in required:
    target = overrides.get(k, 80)
    n_repeats = max(1, (target // 50) + 1)
    sections[k] = (prose + " ") * n_repeats

# §1.2 — 8 văn bản pháp lý
sections["1.2"] = (
    "Căn cứ Luật Đầu tư công số 58/2024/QH15. "
    "Căn cứ Luật Đấu thầu số 22/2023/QH15. "
    "Căn cứ Nghị định số 45/2026/NĐ-CP ngày 15 tháng 02 năm 2026 của Chính phủ. "
    "Căn cứ Nghị định số 214/2025/NĐ-CP ngày 04 tháng 8 năm 2025 của Chính phủ. "
    "Căn cứ Nghị định số 85/2016/NĐ-CP ngày 01 tháng 7 năm 2016 của Chính phủ. "
    "Căn cứ Thông tư số 04/2020/TT-BTTTT ngày 24 tháng 02 năm 2020 của Bộ TTTT. "
    "Căn cứ Thông tư số 12/2022/TT-BTTTT ngày 12 tháng 8 năm 2022 của Bộ TTTT. "
    "Căn cứ Quyết định số 749/QĐ-TTg ngày 03 tháng 6 năm 2020 của Thủ tướng. "
) * 2

# §9.1 ATTT cấp độ + 5 nhóm
sections["9.1"] = (
    "Hệ thống thông tin được xác định cấp độ 3 theo Nghị định số 85/2016/NĐ-CP "
    "và Thông tư số 12/2022/TT-BTTTT. Năm nhóm biện pháp bảo đảm an toàn theo "
    "TCVN 11930:2017 được triển khai đầy đủ: "
    "(1) quản lý — chính sách an toàn thông tin và đánh giá rủi ro định kỳ; "
    "(2) kỹ thuật — firewall, ids, ips, waf, mã hoá dữ liệu, mfa; "
    "(3) vật lý — phòng máy chủ có ups, hệ thống pccc tự động, camera giám sát; "
    "(4) con người — đào tạo nhân viên, phân quyền rbac theo nguyên tắc tối thiểu; "
    "(5) vận hành — backup hàng ngày, kế hoạch dr, log tập trung, sla 99,5%. "
) * 2

data = {
    "project": {
        "display_name": "Hệ thống chuyển đổi số thi hành án hình sự",
        "client": "Cục C10 — Bộ Công an",
        "code": "CDS-THAHS-2026",
    },
    "meta": {"today": "01/05/2026", "version": "1.0"},
    "dev_unit": "Công ty CP Hệ thống Công nghệ ETC",
    "overview": {
        "purpose": "Tài liệu nghiên cứu khả thi dự án CĐS THAHS tại Cục C10.",
        "scope": "Toàn bộ hệ thống tại Cục C10 và 54 trại giam, 163 phân trại.",
    },
    "nckt": {
        "sections": sections,
        "overall_architecture_diagram": "nckt_overall_architecture_diagram.png",
        "business_architecture_diagram": "nckt_business_architecture_diagram.png",
        "risk_matrix": [
            {"stt": "1", "risk": "Ngân sách vượt dự kiến", "probability": "Trung bình", "impact": "Cao", "level": "Cao", "mitigation": "Lập dự phòng 10%, kiểm soát chi phí theo tháng"},
            {"stt": "2", "risk": "Tiến độ chậm", "probability": "Cao", "impact": "Trung bình", "level": "Cao", "mitigation": "Phân kỳ + milestone gates hàng quý"},
            {"stt": "3", "risk": "Thay đổi yêu cầu", "probability": "Trung bình", "impact": "Trung bình", "level": "Trung bình", "mitigation": "Quy trình change request + freeze 60 ngày trước UAT"},
            {"stt": "4", "risk": "Rủi ro ATTT", "probability": "Thấp", "impact": "Cao", "level": "Trung bình", "mitigation": "Pentest trước UAT + TCVN 11930 cấp độ 3"},
            {"stt": "5", "risk": "Năng lực nhà thầu", "probability": "Thấp", "impact": "Cao", "level": "Trung bình", "mitigation": "Đánh giá năng lực HSMT + bảo lãnh thực hiện hợp đồng"},
        ],
        "investment_summary": [
            {"stt": "1", "item": "Phần cứng — máy chủ vùng trong", "unit": "chiếc", "qty": "6", "unit_price": "250.000.000", "amount": "1.500.000.000", "note": ""},
            {"stt": "2", "item": "Phần cứng — máy chủ vùng ngoài", "unit": "chiếc", "qty": "4", "unit_price": "250.000.000", "amount": "1.000.000.000", "note": ""},
            {"stt": "3", "item": "Lưu trữ SAN", "unit": "hệ", "qty": "2", "unit_price": "500.000.000", "amount": "1.000.000.000", "note": ""},
            {"stt": "4", "item": "Phần mềm thương mại (OS, ảo hoá, backup)", "unit": "gói", "qty": "1", "unit_price": "800.000.000", "amount": "800.000.000", "note": ""},
            {"stt": "5", "item": "Phần mềm nội bộ (phát triển)", "unit": "gói", "qty": "1", "unit_price": "4.500.000.000", "amount": "4.500.000.000", "note": "TT 04/2020"},
            {"stt": "6", "item": "Đào tạo + chuyển giao", "unit": "khoá", "qty": "10", "unit_price": "30.000.000", "amount": "300.000.000", "note": ""},
            {"stt": "7", "item": "Quản lý dự án + tư vấn giám sát", "unit": "gói", "qty": "1", "unit_price": "500.000.000", "amount": "500.000.000", "note": ""},
            {"stt": "8", "item": "Dự phòng 10%", "unit": "gói", "qty": "1", "unit_price": "960.000.000", "amount": "960.000.000", "note": ""},
        ],
    },
    "diagrams": {
        "nckt_overall_architecture_diagram": "graph TD\n  A-->B\n  B-->C",
        "nckt_business_architecture_diagram": "graph LR\n  X-->Y\n  Y-->Z",
    },
}

# Validate
result = validate_content_data(data)
print("=== Validation ===")
print("valid:", result.valid)
print("errors:", len(result.errors))
print("warnings:", len(result.warnings))
nckt_warnings = [w for w in result.warnings if "nckt" in w.lower()]
print("nckt-specific warnings:", len(nckt_warnings))
for w in nckt_warnings[:8]:
    print("  -", w[:180])

# Render
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    dp = tmp / "data.json"
    dp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    out = tmp / "out.docx"
    rep = docx_engine.render(
        Path("src/etc_platform/assets/templates/nghien-cuu-kha-thi.docx"), dp, out
    )
    print("\n=== Render ===")
    print("errors:", rep.errors)
    print("warnings:", rep.warnings)
    print("output bytes:", out.stat().st_size if out.exists() else "MISSING")
