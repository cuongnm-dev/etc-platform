# ref-export.md — DOCX Export Pipeline (NĐ 30/2020)

## Pipeline Overview

```
Markdown (content/*.md)
    │
    ▼
[create-reference-docx.py]   ← chạy 1 lần khi setup workspace
    │  Creates nd30-2020-template.docx với styles chuẩn
    ▼
[Pandoc]                     ← mỗi lần export
    │  --reference-doc=nd30-2020-template.docx
    │  --lua-filter=vn-gov-format.lua
    ▼
{slug}-draft.docx
    │
    ▼
[post-process.py]            ← fix font/table/spacing sau Pandoc
    │
    ▼
{slug}.docx  ← OUTPUT FINAL
```

**Lý do cần 3 bước:**
- Pandoc dùng reference-doc styles → styles phải đúng từ đầu (create-reference-docx.py)
- Pandoc đôi khi không áp dụng đúng font/spacing cho tất cả elements (post-process.py fix)
- `variables: fontsize, linestretch` trong YAML chỉ áp dụng cho PDF/LaTeX — KHÔNG cho DOCX

---

## `export/create-reference-docx.py` — Tạo Reference Template

```python
"""
create-reference-docx.py — Tạo reference.docx chuẩn NĐ 30/2020/NĐ-CP
Font: Times New Roman 13pt | Lề: 20/20/30/15mm | Dãn dòng: 1.5

Cài đặt: pip install python-docx
Sử dụng: python create-reference-docx.py [output.docx]
"""
from docx import Document
from docx.shared import Pt, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import sys, os

def set_vn_font(element):
    """Set Times New Roman cho Latin + East Asian (tiếng Việt) + CS"""
    rPr = element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:ascii'),     'Times New Roman')
    rFonts.set(qn('w:hAnsi'),     'Times New Roman')
    rFonts.set(qn('w:eastAsia'), 'Times New Roman')
    rFonts.set(qn('w:cs'),        'Times New Roman')

def setup_normal_style(doc):
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(13)
    style.paragraph_format.alignment         = WD_ALIGN_PARAGRAPH.JUSTIFY
    style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    style.paragraph_format.line_spacing      = Pt(13 * 1.5)   # = 19.5pt
    style.paragraph_format.space_before      = Pt(0)
    style.paragraph_format.space_after       = Pt(6)
    set_vn_font(style.element)

def setup_heading(doc, name, size, bold, italic=False, space_before=12):
    try:
        style = doc.styles[name]
    except KeyError:
        style = doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
    style.font.name   = 'Times New Roman'
    style.font.size   = Pt(size)
    style.font.bold   = bold
    style.font.italic = italic
    style.paragraph_format.alignment     = WD_ALIGN_PARAGRAPH.LEFT
    style.paragraph_format.space_before  = Pt(space_before)
    style.paragraph_format.space_after   = Pt(6)
    style.paragraph_format.keep_with_next = True
    # Line spacing same as Normal
    style.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    style.paragraph_format.line_spacing      = Pt(13 * 1.5)
    set_vn_font(style.element)

def setup_table_style(doc):
    try:
        style = doc.styles['Table Grid']
    except KeyError:
        style = doc.styles.add_style('Table Grid', WD_STYLE_TYPE.TABLE)
    # Table cell default font
    style.font.name = 'Times New Roman'
    style.font.size = Pt(12)

def add_page_number_footer(section):
    """Footer: số trang ở giữa"""
    footer = section.footer
    para = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    para.clear()
    para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    para.style.font.name = 'Times New Roman'
    para.style.font.size = Pt(13)
    run = para.add_run()
    # PAGE field
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = ' PAGE '
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)

def create_nd30_reference_docx(output_path):
    doc = Document()

    # ── Margins (NĐ 30/2020) ────────────────────────────────────
    section = doc.sections[0]
    section.top_margin    = Mm(20)
    section.bottom_margin = Mm(20)
    section.left_margin   = Mm(30)
    section.right_margin  = Mm(15)
    section.page_height   = Mm(297)   # A4
    section.page_width    = Mm(210)

    # ── Styles ──────────────────────────────────────────────────
    setup_normal_style(doc)

    # Heading 1: 14pt bold (số La Mã hoặc chữ số)
    setup_heading(doc, 'Heading 1', size=14, bold=True,  italic=False, space_before=12)
    # Heading 2: 13pt bold
    setup_heading(doc, 'Heading 2', size=13, bold=True,  italic=False, space_before=10)
    # Heading 3: 13pt bold italic (theo NĐ 30)
    setup_heading(doc, 'Heading 3', size=13, bold=True,  italic=True,  space_before=8)
    # Heading 4: 13pt normal (a) b) c) level)
    setup_heading(doc, 'Heading 4', size=13, bold=False, italic=False, space_before=6)

    setup_table_style(doc)
    add_page_number_footer(section)

    # ── Placeholder content (sẽ bị Pandoc ghi đè) ──────────────
    doc.add_paragraph('[Reference document — NĐ 30/2020/NĐ-CP]', style='Heading 1')
    doc.add_paragraph(
        'File này là template tham chiếu cho Pandoc. '
        'Không sửa trực tiếp. Chạy lại create-reference-docx.py nếu cần reset.',
        style='Normal'
    )

    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    doc.save(output_path)
    print(f"✓ Created reference template: {output_path}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "export/reference-docs/nd30-2020-template.docx"
    create_nd30_reference_docx(out)
```

---

## `export/post-process.py` — Fix Formatting Sau Pandoc

```python
"""
post-process.py — Fix font/table/spacing trong DOCX sau Pandoc conversion
Vấn đề Pandoc: không áp dụng đầy đủ font cho East Asian chars (tiếng Việt),
               không thêm borders cho tables, spacing đôi khi sai.

Cài đặt: pip install python-docx
Sử dụng: python post-process.py input.docx output.docx
"""
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import sys, re

BODY_FONT      = 'Times New Roman'
BODY_PT        = 13
TABLE_PT       = 12
LINE_SPACING   = Pt(BODY_PT * 1.5)   # 19.5pt

HEADING_STYLES = {'Heading 1', 'Heading 2', 'Heading 3', 'Heading 4',
                  'Title', 'Subtitle'}

def ensure_vn_font(element, font_name=BODY_FONT):
    rPr = element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:ascii'),    font_name)
    rFonts.set(qn('w:hAnsi'),    font_name)
    rFonts.set(qn('w:eastAsia'), font_name)
    rFonts.set(qn('w:cs'),       font_name)

def fix_run(run, size_pt, bold=None, italic=None):
    run.font.name = BODY_FONT
    run.font.size = Pt(size_pt)
    if bold   is not None: run.font.bold   = bold
    if italic is not None: run.font.italic = italic
    ensure_vn_font(run._r)

def fix_paragraph(para, is_table=False):
    pf = para.paragraph_format
    if not is_table:
        pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        pf.line_spacing      = LINE_SPACING
        pf.space_before      = Pt(0)
        pf.space_after       = Pt(6)
    else:
        pf.space_before = Pt(2)
        pf.space_after  = Pt(2)

def add_table_borders(table):
    """Thêm border 0.5pt đen cho tất cả ô"""
    border_attrs = {'val': 'single', 'sz': '4', 'space': '0', 'color': '000000'}
    for row in table.rows:
        for cell in row.cells:
            tc  = cell._tc
            tcPr = tc.get_or_add_tcPr()
            # Xóa border cũ
            for old in tcPr.findall(qn('w:tcBorders')):
                tcPr.remove(old)
            # Tạo border mới
            tcBorders = OxmlElement('w:tcBorders')
            for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
                el = OxmlElement(f'w:{edge}')
                for k, v in border_attrs.items():
                    el.set(qn(f'w:{k}'), v)
                tcBorders.append(el)
            tcPr.append(tcBorders)

def fix_document(input_path, output_path):
    doc = Document(input_path)
    issues = []

    # ── Fix paragraphs ───────────────────────────────────────────
    for para in doc.paragraphs:
        sname = para.style.name if para.style else 'Normal'
        is_heading = sname in HEADING_STYLES

        fix_paragraph(para)

        for run in para.runs:
            if is_heading:
                fix_run(run, BODY_PT, bold=True)
            else:
                fix_run(run, BODY_PT)

    # ── Fix tables ───────────────────────────────────────────────
    for tbl in doc.tables:
        add_table_borders(tbl)
        for row in tbl.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    fix_paragraph(para, is_table=True)
                    for run in para.runs:
                        fix_run(run, TABLE_PT)

    # ── Verify images embedded (warn if missing) ─────────────────
    for rel in doc.part.rels.values():
        if 'image' in rel.reltype:
            try:
                _ = rel.target_part.blob   # trigger load
            except Exception:
                issues.append(f"⚠ Image not embedded: {rel.target_ref}")

    doc.save(output_path)

    print(f"✓ Post-processed: {output_path}")
    if issues:
        print("Issues found:")
        for i in issues: print(f"  {i}")
    return len(issues) == 0

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python post-process.py input.docx output.docx")
        sys.exit(1)
    ok = fix_document(sys.argv[1], sys.argv[2])
    sys.exit(0 if ok else 1)
```

---

## `defaults/vn-gov.yaml` — Pandoc Defaults

```yaml
# Pandoc defaults for Vietnamese government documents
# QUAN TRỌNG: 'variables' section chỉ apply cho PDF/LaTeX output.
# Với DOCX: font, margin, spacing đều từ reference-doc styles.

from: markdown+smart+pipe_tables+header_attributes+fenced_code_blocks+footnotes
to: docx

# Reference doc — định nghĩa toàn bộ styles (font, lề, spacing)
# Tạo bằng: python export/create-reference-docx.py
reference-doc: export/reference-docs/nd30-2020-template.docx

# Lua filters
filters:
  - export/filters/vn-gov-format.lua

# Table of contents
toc: true
toc-depth: 3

# Metadata
metadata:
  lang: vi
```

---

## `filters/vn-gov-format.lua` — Pandoc Lua Filter

```lua
-- vn-gov-format.lua
-- Pandoc Lua filter: xử lý caption bảng/hình, page break, ngày tháng tiếng Việt
-- Áp dụng cho DOCX output từ Markdown tài liệu hành chính VN

local chapter       = 0
local table_counter = 0
local figure_counter = 0

-- ── Reset counters tại mỗi heading cấp 1 ────────────────────────
function Header(el)
  if el.level == 1 then
    chapter       = chapter + 1
    table_counter = 0
    figure_counter = 0
  end
  return el
end

-- ── Tự động đánh số bảng: "Bảng X.Y: Title" ─────────────────────
function Table(el)
  table_counter = table_counter + 1
  if el.caption and el.caption.long and #el.caption.long > 0 then
    local caption_text = pandoc.utils.stringify(el.caption.long)
    if not caption_text:match("^Bảng%s+%d") then
      local prefix = string.format("Bảng %d.%d: ", chapter, table_counter)
      local prefix_inlines = pandoc.List({ pandoc.Strong({ pandoc.Str(prefix) }) })
      local existing = el.caption.long[1]
      if existing.t == 'Plain' then
        existing.content = prefix_inlines .. existing.content
      else
        table.insert(el.caption.long, 1, pandoc.Plain(prefix_inlines))
      end
    end
  end
  return el
end

-- ── Tự động đánh số hình: "Hình X.Y: Title" ─────────────────────
function Figure(el)
  figure_counter = figure_counter + 1
  if el.caption and el.caption.long and #el.caption.long > 0 then
    local caption_text = pandoc.utils.stringify(el.caption.long)
    if not caption_text:match("^Hình%s+%d") then
      local prefix = string.format("Hình %d.%d: ", chapter, figure_counter)
      local prefix_inlines = pandoc.List({ pandoc.Strong({ pandoc.Str(prefix) }) })
      local existing = el.caption.long[1]
      if existing.t == 'Plain' then
        existing.content = prefix_inlines .. existing.content
      else
        table.insert(el.caption.long, 1, pandoc.Plain(prefix_inlines))
      end
    end
  end
  return el
end

-- ── Page break: \newpage → DOCX page break ───────────────────────
function RawBlock(el)
  if el.text:match("\\newpage") or el.text:match("\\pagebreak") then
    if FORMAT:match("docx") then
      return pandoc.RawBlock("openxml",
        '<w:p><w:r><w:br w:type="page"/></w:r></w:p>')
    end
  end
  return el
end

-- ── Convert YYYY-MM-DD → "ngày dd tháng mm năm yyyy" ─────────────
function Meta(meta)
  if meta.date then
    local date_str = pandoc.utils.stringify(meta.date)
    local y, m, d = date_str:match("(%d%d%d%d)-(%d%d)-(%d%d)")
    if y then
      meta.date = pandoc.MetaInlines({
        pandoc.Str(string.format("ngày %d tháng %d năm %s",
          tonumber(d), tonumber(m), y))
      })
    end
  end
  return meta
end

-- ── Warn on unfilled placeholders ───────────────────────────────
function Str(el)
  if el.text:match("%[CẦN BỔ SUNG:") or el.text:match("{{content:") then
    io.stderr:write("WARNING: Unfilled placeholder: " .. el.text .. "\n")
  end
  return el
end
```

---

## `export.ps1` — One-Command Export Script

```powershell
# export.ps1 — Export DOCX chuẩn NĐ 30/2020
# Pipeline: Pandoc → post-process.py → output
# Usage: .\export\export.ps1 -DocPath projects\{slug} [-Open] [-SkipPostProcess]

param(
    [Parameter(Mandatory=$true)]
    [string]$DocPath,
    [switch]$Open,
    [switch]$SkipPostProcess,
    [ValidateSet('docx')]
    [string]$Format = 'docx'
)

$ErrorActionPreference = 'Stop'
$ProgressPreference    = 'SilentlyContinue'
$ScriptDir = $PSScriptRoot

# ── Paths ────────────────────────────────────────────────────────
$markdownDir   = Join-Path $DocPath "content"
$exportDir     = Join-Path $ScriptDir "output"
$template      = Join-Path $ScriptDir "defaults\vn-gov.yaml"
$filter        = Join-Path $ScriptDir "filters\vn-gov-format.lua"
$refDoc        = Join-Path $ScriptDir "reference-docs\nd30-2020-template.docx"
$createRefPy   = Join-Path $ScriptDir "create-reference-docx.py"
$postProcessPy = Join-Path $ScriptDir "post-process.py"

$docName  = Split-Path $DocPath -Leaf
$draftOut = Join-Path $exportDir "${docName}-draft.docx"
$finalOut = Join-Path $exportDir "${docName}.docx"

New-Item -ItemType Directory -Force -Path $exportDir | Out-Null

# ── Prerequisite checks ──────────────────────────────────────────
Write-Host "=== Export: $docName ===" -ForegroundColor Cyan

# Pandoc
try {
    $pandocVer = pandoc --version 2>&1 | Select-String "pandoc (\d+\.\d+)" |
                 ForEach-Object { $_.Matches[0].Groups[1].Value }
    Write-Host "✓ Pandoc $pandocVer"
} catch {
    Write-Error "❌ Pandoc not found. Install from https://pandoc.org/"
}

# Python
try {
    $pyVer = python --version 2>&1
    Write-Host "✓ $pyVer"
} catch {
    Write-Error "❌ Python not found. Install Python 3.10+."
}

# python-docx
$hasDocx = python -c "import docx; print('ok')" 2>$null
if ($hasDocx -ne 'ok') {
    Write-Host "Installing python-docx..." -ForegroundColor Yellow
    pip install python-docx -q
}

# Content dir
if (-not (Test-Path $markdownDir)) {
    Write-Error "❌ Content dir not found: $markdownDir"
}

$mdFiles = Get-ChildItem -Path $markdownDir -Filter "*.md" |
           Sort-Object Name |
           ForEach-Object { $_.FullName }
if (-not $mdFiles) {
    Write-Error "❌ No .md files in $markdownDir"
}

# ── Step 1: Create/verify reference.docx ─────────────────────────
Write-Host "`n[1/3] Reference template..." -ForegroundColor Cyan
if (-not (Test-Path $refDoc)) {
    Write-Host "  Creating nd30-2020-template.docx..."
    python $createRefPy $refDoc
} else {
    Write-Host "  ✓ Template exists: $refDoc"
}

# ── Step 2: Pandoc → draft.docx ──────────────────────────────────
Write-Host "`n[2/3] Pandoc conversion..." -ForegroundColor Cyan

$pandocArgs = @(
    "-t", "docx",
    "-o", $draftOut,
    "--reference-doc", $refDoc,
    "--lua-filter", $filter,
    "--toc",
    "--toc-depth=3",
    "--from", "markdown+smart+pipe_tables+header_attributes+fenced_code_blocks"
)
$pandocArgs += $mdFiles

Write-Host "  Running Pandoc ($($mdFiles.Count) files)..."
& pandoc @pandocArgs 2>&1 | Where-Object { $_ } | ForEach-Object { Write-Host "  $_" }

if ($LASTEXITCODE -ne 0) { Write-Error "❌ Pandoc failed." }
Write-Host "  ✓ Draft: $draftOut"

# ── Step 3: post-process.py → final.docx ─────────────────────────
if ($SkipPostProcess) {
    Copy-Item $draftOut $finalOut -Force
    Write-Host "`n[3/3] Post-process skipped." -ForegroundColor Yellow
} else {
    Write-Host "`n[3/3] Post-processing (font/table/spacing)..." -ForegroundColor Cyan
    python $postProcessPy $draftOut $finalOut 2>&1 | ForEach-Object { Write-Host "  $_" }
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ⚠ Post-process failed — using draft as output" -ForegroundColor Yellow
        Copy-Item $draftOut $finalOut -Force
    }
    # Clean up draft
    Remove-Item $draftOut -ErrorAction SilentlyContinue
}

# ── Checks ────────────────────────────────────────────────────────
Write-Host "`n── Checks ──" -ForegroundColor Gray

# Unfilled placeholders
$phCount = Select-String -Path (Join-Path $markdownDir "*.md") `
    -Pattern "\[CẦN BỔ SUNG:|{{content:|{{optional:" -ErrorAction SilentlyContinue |
    Measure-Object | Select-Object -ExpandProperty Count
if ($phCount -gt 0) {
    Write-Host "  ⚠ $phCount unfilled placeholders remain" -ForegroundColor Yellow
} else {
    Write-Host "  ✓ No unfilled placeholders"
}

# Missing diagrams
$diagramDir = Join-Path $markdownDir "diagrams"
$missingDiagrams = Select-String -Path (Join-Path $markdownDir "*.md") `
    -Pattern "\[DIAGRAM:" -ErrorAction SilentlyContinue | Measure-Object | Select-Object -ExpandProperty Count
if ($missingDiagrams -gt 0) {
    Write-Host "  ⚠ $missingDiagrams [DIAGRAM:] placeholders — export before diagrams ready" -ForegroundColor Yellow
} elseif (Test-Path $diagramDir) {
    $pngCount = (Get-ChildItem $diagramDir -Filter "*.png" -ErrorAction SilentlyContinue).Count
    Write-Host "  ✓ Diagrams: $pngCount PNG files embedded"
}

# File size sanity
$fileSize = (Get-Item $finalOut).Length / 1KB
Write-Host "  ✓ Output size: $([Math]::Round($fileSize, 0)) KB"
if ($fileSize -lt 10) {
    Write-Host "  ⚠ File suspiciously small — check content" -ForegroundColor Yellow
}

Write-Host "`n✓ Export complete: $finalOut" -ForegroundColor Green
Write-Host "Next:"
Write-Host "  1. Open DOCX → Ctrl+A → F9 (update TOC/fields)"
Write-Host "  2. Check headers, tables, images"
Write-Host "  3. Save as final"

if ($Open) {
    Start-Process $finalOut
}
```

---

## Setup Instructions

### Lần đầu tiên (1 lần duy nhất)

```powershell
# 1. Cài python-docx
pip install python-docx

# 2. Tạo reference template NĐ 30/2020
python export/create-reference-docx.py

# 3. Verify template
# Mở export/reference-docs/nd30-2020-template.docx → kiểm tra font, lề
```

### Mỗi lần export

```powershell
# Export nhanh
.\export\export.ps1 -DocPath projects\tkcs-quan-ly-van-ban -Open

# Export không post-process (debug Pandoc output)
.\export\export.ps1 -DocPath projects\tkcs-abc -SkipPostProcess
```

---

## Test Checklist

Sau mỗi lần chỉnh pipeline, test với doc type này:

```
□ Mở DOCX → font = Times New Roman 13pt (kiểm tra đoạn bình thường)
□ Heading 1 = 14pt Bold | Heading 2 = 13pt Bold | Heading 3 = 13pt Bold Italic
□ Lề: trái 3cm, phải 1.5cm, trên/dưới 2cm
□ Dãn dòng = 1.5 (đúng với NĐ 30/2020)
□ Bảng: có border, font đều, không tràn trang
□ Hình (PNG): hiển thị đúng, có caption "Hình X.Y: ..."
□ Mục lục tự động: update sau Ctrl+A → F9
□ Số trang: ở giữa footer
□ Tiếng Việt: không bị thay font, không bị tofu (□□□)
□ Placeholder [CẦN BỔ SUNG] không xuất hiện trong file cuối (nếu đã điền đủ)
```

### Lỗi thường gặp

| Lỗi | Nguyên nhân | Fix |
|---|---|---|
| Font không phải Times New Roman | reference.docx chưa đúng | Chạy lại create-reference-docx.py |
| Tiếng Việt bị □□□ | East Asian font không set | post-process.py đã fix, kiểm tra lại |
| Bảng không có border | Pandoc không tự thêm | post-process.py đã fix |
| Ảnh thiếu | Path PNG không đúng | Kiểm tra content/diagrams/*.png |
| Heading sai size | reference.docx style chưa đúng | Chạy lại create-reference-docx.py |
| Spacing khác 1.5 | Pandoc override | post-process.py đã fix |
| TOC trống | Chưa update fields | Ctrl+A → F9 trong Word |
