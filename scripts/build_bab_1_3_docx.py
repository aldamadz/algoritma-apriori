from __future__ import annotations

import html
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "BAB_I_II_III_REVISI.md"
OUTPUT = ROOT / "docs" / "BAB_I_II_III_REVISI_DENGAN_SITASI.docx"


REFERENCES = [
    '[1] Y. Fayyad, G. Piatetsky-Shapiro, and P. Smyth, "From Data Mining to Knowledge Discovery in Databases," AI Magazine, vol. 17, no. 3, pp. 37-54, 1996.',
    '[2] R. Agrawal and R. Srikant, "Fast Algorithms for Mining Association Rules," Proceedings of the 20th International Conference on Very Large Data Bases, pp. 487-499, 1994.',
    '[3] R. A. S. Prayoga, R. Basatha, M. S. Akbar, E. A. Elfaiz, and C. D. Putra, "Penerapan Data Mining untuk Peminjaman Buku dengan Menggunakan Algoritma Apriori," 2024.',
    '[4] Haryono, Marisa, Carudin, and Ihsan, "Implementasi Algoritma Apriori dalam Memberikan Rekomendasi Buku pada Perpustakaan SMK Karya Guna 2 Bekasi," 2024.',
    '[5] Ilham, C. Wulandari, and B. Santoso, "Analisis Algoritma Apriori untuk Rekomendasi Penempatan Buku pada Perpustakaan Universitas Bina Insan," 2024.',
    '[6] A. Mugnia and M. M. Mutoffar, "Implementation of the Apriori Algorithm for Book Recommendation Systems in Digital Libraries," 2024.',
    '[7] M. Jannah, E. Yumami, A. Julianto, and E. Rahmi, "Sistem Rekomendasi Buku di Perpustakaan Menggunakan Machine Learning dan Algoritma Apriori," 2025.',
    '[8] M. Fitriani, G. F. Nama, and Mardiana, "Implementasi Association Rule Dengan Algoritma Apriori Pada Data Peminjaman Buku UPT Perpustakaan Universitas Lampung Menggunakan Metodologi CRISP-DM," Jurnal Informatika dan Teknik Elektro Terapan, vol. 10, no. 1, 2022.',
    '[9] Murdani, A. S. Sembiring, and T. S. Alasi, "Penerapan Data Mining Menggunakan Algoritma Apriori Pada Peminjaman Buku di Perpustakaan Pada Pesantren Babul Ulum," Jurnal Armada Informatika, vol. 7, no. 2, pp. 323-327, 2023.',
    '[10] Y. Andini, J. T. Hardinata, and Y. P. Purba, "Penerapan Data Mining Terhadap Tata Letak Buku di Perpustakaan Sintong Bingei Pematangsiantar Menggunakan Metode Apriori," Jurnal TIMES, vol. 11, no. 1, pp. 9-15, 2022.',
]


CITATION_RULES = [
    ("Perkembangan teknologi informasi telah membawa perubahan besar", " [1]"),
    ("Data mining merupakan proses penggalian informasi", " [1]"),
    ("Algoritma Apriori merupakan salah satu algoritma", " [2]"),
    ("Perpustakaan tidak hanya berfungsi sebagai tempat penyimpanan koleksi buku", " [3]"),
    ("Jumlah koleksi buku di perpustakaan perguruan tinggi terus bertambah", " [4]"),
    ("Data transaksi peminjaman sebenarnya memiliki potensi besar untuk dianalisis", " [8]"),
    ("Salah satu metode yang dapat digunakan untuk menemukan pola dari data transaksi", " [1]"),
    ("Association rules digunakan untuk melihat keterkaitan antar item", " [2]"),
    ("Penelitian yang dilakukan oleh Prayoga", " [3]"),
    ("Penelitian Haryono", " [4]"),
    ("Penelitian Ilham", " [5]"),
    ("Penelitian Ages Mugnia", " [6]"),
    ("Penelitian Jannah", " [7]"),
    ("Beberapa penelitian sebelumnya telah membahas", " [3]-[10]"),
    ("Data mining tidak hanya berfungsi untuk mengolah data", " [1]"),
    ("Salah satu teknik yang digunakan dalam data mining adalah association rule mining", " [2]"),
    ("Data transaksi peminjaman buku tidak hanya dapat digunakan sebagai arsip administrasi", " [8], [9]"),
    ("Sistem rekomendasi merupakan sistem yang digunakan", " [7]"),
    ("Salah satu pendekatan yang dapat digunakan adalah data mining", " [3], [4]"),
    ("Support merupakan ukuran yang menunjukkan tingkat kemunculan", " [2]"),
    ("Confidence merupakan ukuran yang menunjukkan tingkat kepercayaan", " [2]"),
    ("Lift digunakan untuk mengetahui kekuatan hubungan antar item", " [7]"),
    ("Dalam proses KDD, data mining menjadi salah satu tahapan penting", " [1]"),
    ("Secara umum, proses algoritma Apriori dimulai", " [2]"),
]


def esc(value: str) -> str:
    return html.escape(value, quote=False)


def add_citations(text: str) -> str:
    updated = text
    for marker, citation in CITATION_RULES:
        idx = updated.find(marker)
        if idx == -1:
            continue
        end = updated.find(".", idx)
        if end == -1:
            continue
        if citation not in updated[idx : end + 1]:
            updated = updated[:end] + citation + updated[end:]
    return updated


def run_xml(text: str, bold: bool = False, italic: bool = False) -> str:
    props = []
    if bold:
        props.append("<w:b/>")
    if italic:
        props.append("<w:i/>")
    props.append('<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>')
    props.append('<w:sz w:val="24"/>')
    rpr = f"<w:rPr>{''.join(props)}</w:rPr>"
    return f"<w:r>{rpr}<w:t xml:space=\"preserve\">{esc(text)}</w:t></w:r>"


def para_xml(text: str, style: str | None = None, align: str | None = None) -> str:
    ppr_parts = []
    if style:
        ppr_parts.append(f'<w:pStyle w:val="{style}"/>')
    if align:
        ppr_parts.append(f'<w:jc w:val="{align}"/>')
    if style is None:
        ppr_parts.append('<w:spacing w:after="120" w:line="360" w:lineRule="auto"/>')
        ppr_parts.append('<w:ind w:firstLine="720"/>')
        ppr_parts.append('<w:jc w:val="both"/>')
    ppr = f"<w:pPr>{''.join(ppr_parts)}</w:pPr>" if ppr_parts else ""
    return f"<w:p>{ppr}{run_xml(text)}</w:p>"


def heading_xml(text: str, level: int) -> str:
    if level == 1:
        return para_xml(text, "Heading1", "center")
    if level == 2:
        return para_xml(text, "Heading2")
    return para_xml(text, "Heading3")


def list_xml(text: str, ordered: bool = False) -> str:
    bullet = "" if ordered else "\u2022 "
    cleaned = re.sub(r"^\d+\.\s+", "", text)
    return f'<w:p><w:pPr><w:spacing w:after="80"/><w:ind w:left="720" w:hanging="360"/></w:pPr>{run_xml(bullet + cleaned)}</w:p>'


def table_xml(rows: list[list[str]]) -> str:
    col_count = max(len(row) for row in rows)
    cells_width = int(9000 / max(col_count, 1))
    body = ['<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:tblBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/></w:tblBorders></w:tblPr>']
    for row_index, row in enumerate(rows):
        body.append("<w:tr>")
        for cell in row:
            body.append(f'<w:tc><w:tcPr><w:tcW w:w="{cells_width}" w:type="dxa"/></w:tcPr>')
            body.append(para_xml(cell, None if row_index else "TableHeader"))
            body.append("</w:tc>")
        body.append("</w:tr>")
    body.append("</w:tbl>")
    return "".join(body)


def parse_markdown(md: str) -> list[str]:
    blocks: list[str] = []
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("|"):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            rows = []
            for table_line in table_lines:
                if re.fullmatch(r"\|[\s:\-]+\|", table_line):
                    continue
                cells = [cell.strip(" `") for cell in table_line.strip("|").split("|")]
                if cells and not all(re.fullmatch(r":?-+:?", cell) for cell in cells):
                    rows.append(cells)
            if rows:
                blocks.append(table_xml(rows))
            continue
        if line.startswith("# "):
            blocks.append(heading_xml(line[2:].strip(), 1))
        elif line.startswith("## "):
            blocks.append(heading_xml(line[3:].strip(), 2))
        elif line.startswith("### "):
            blocks.append(heading_xml(line[4:].strip(), 3))
        elif re.match(r"^\d+\.\s+", line):
            blocks.append(list_xml(line, ordered=True))
        elif line.startswith("- "):
            blocks.append(list_xml(line[2:], ordered=False))
        else:
            blocks.append(para_xml(line.replace("`", "")))
        i += 1
    return blocks


def document_xml(body: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <w:body>
    {body}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1440" w:right="1440" w:bottom="1440" w:left="1440" w:header="708" w:footer="708" w:gutter="0"/>
    </w:sectPr>
  </w:body>
</w:document>'''


def styles_xml() -> str:
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading1">
    <w:name w:val="heading 1"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="240" w:after="120"/><w:jc w:val="center"/></w:pPr>
    <w:rPr><w:b/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="28"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading2">
    <w:name w:val="heading 2"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="220" w:after="100"/></w:pPr>
    <w:rPr><w:b/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="26"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="Heading3">
    <w:name w:val="heading 3"/>
    <w:basedOn w:val="Normal"/>
    <w:pPr><w:spacing w:before="180" w:after="80"/></w:pPr>
    <w:rPr><w:b/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr>
  </w:style>
  <w:style w:type="paragraph" w:styleId="TableHeader">
    <w:name w:val="Table Header"/>
    <w:basedOn w:val="Normal"/>
    <w:rPr><w:b/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="22"/></w:rPr>
  </w:style>
</w:styles>'''


def write_docx(body: str) -> None:
    content_types = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''
    rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''
    doc_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''
    core = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>BAB I-III Revisi</dc:title>
  <dc:creator>Apriori Engine Project</dc:creator>
</cp:coreProperties>'''
    app = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties"><Application>Python OpenXML</Application></Properties>'''
    settings = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:zoom w:percent="100"/></w:settings>'''

    with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", content_types)
        docx.writestr("_rels/.rels", rels)
        docx.writestr("word/_rels/document.xml.rels", doc_rels)
        docx.writestr("word/document.xml", document_xml(body))
        docx.writestr("word/styles.xml", styles_xml())
        docx.writestr("word/settings.xml", settings)
        docx.writestr("docProps/core.xml", core)
        docx.writestr("docProps/app.xml", app)


def main() -> None:
    md = add_citations(SOURCE.read_text(encoding="utf-8"))
    blocks = parse_markdown(md)
    blocks.append(heading_xml("DAFTAR PUSTAKA", 1))
    for reference in REFERENCES:
        blocks.append(para_xml(reference))
    write_docx("\n".join(blocks))
    print(OUTPUT)


if __name__ == "__main__":
    main()
