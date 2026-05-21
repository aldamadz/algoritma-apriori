from __future__ import annotations

import html
import json
import re
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs" / "BAB_I_II_III_REVISI.md"
OUTPUT = ROOT / "docs" / "BAB_I_II_III_REVISI_ZOTERO_FIELDS.docx"


REFS = {
    1: {
        "display": '[1] J. Han, M. Kamber, and J. Pei, Data Mining: Concepts and Techniques, 3rd ed. Waltham, MA: Morgan Kaufmann, 2012.',
        "itemData": {
            "id": "ref-1",
            "type": "book",
            "title": "Data Mining: Concepts and Techniques",
            "author": [{"family": "Han", "given": "Jiawei"}, {"family": "Kamber", "given": "Micheline"}, {"family": "Pei", "given": "Jian"}],
            "publisher": "Morgan Kaufmann",
            "publisher-place": "Waltham, MA",
            "edition": "3",
            "issued": {"date-parts": [[2012]]},
        },
    },
    2: {
        "display": '[2] R. Agrawal and R. Srikant, "Fast Algorithms for Mining Association Rules," in Proc. 20th Int. Conf. Very Large Data Bases, 1994, pp. 487-499.',
        "itemData": {
            "id": "ref-2",
            "type": "paper-conference",
            "title": "Fast Algorithms for Mining Association Rules",
            "author": [{"family": "Agrawal", "given": "Rakesh"}, {"family": "Srikant", "given": "Ramakrishnan"}],
            "container-title": "Proceedings of the 20th International Conference on Very Large Data Bases",
            "page": "487-499",
            "issued": {"date-parts": [[1994]]},
        },
    },
    3: {
        "display": '[3] I. H. Witten, E. Frank, M. A. Hall, and C. J. Pal, Data Mining: Practical Machine Learning Tools and Techniques, 4th ed. Cambridge, MA: Morgan Kaufmann, 2016.',
        "itemData": {
            "id": "ref-3",
            "type": "book",
            "title": "Data Mining: Practical Machine Learning Tools and Techniques",
            "author": [{"family": "Witten", "given": "Ian H."}, {"family": "Frank", "given": "Eibe"}, {"family": "Hall", "given": "Mark A."}, {"family": "Pal", "given": "Christopher J."}],
            "publisher": "Morgan Kaufmann",
            "publisher-place": "Cambridge, MA",
            "edition": "4",
            "issued": {"date-parts": [[2016]]},
        },
    },
    4: {
        "display": '[4] F. Ricci, L. Rokach, and B. Shapira, Recommender Systems Handbook, 2nd ed. New York: Springer, 2015.',
        "itemData": {
            "id": "ref-4",
            "type": "book",
            "title": "Recommender Systems Handbook",
            "editor": [{"family": "Ricci", "given": "Francesco"}, {"family": "Rokach", "given": "Lior"}, {"family": "Shapira", "given": "Bracha"}],
            "publisher": "Springer",
            "publisher-place": "New York",
            "edition": "2",
            "issued": {"date-parts": [[2015]]},
        },
    },
    5: {
        "display": '[5] M. Fitriani, G. F. Nama, and Mardiana, "Implementasi Association Rule Dengan Algoritma Apriori Pada Data Peminjaman Buku UPT Perpustakaan Universitas Lampung Menggunakan Metodologi CRISP-DM," Jurnal Informatika dan Teknik Elektro Terapan, vol. 10, no. 1, 2022.',
        "itemData": {
            "id": "ref-5",
            "type": "article-journal",
            "title": "Implementasi Association Rule Dengan Algoritma Apriori Pada Data Peminjaman Buku UPT Perpustakaan Universitas Lampung Menggunakan Metodologi CRISP-DM",
            "author": [{"family": "Fitriani", "given": "M."}, {"family": "Nama", "given": "G. F."}, {"literal": "Mardiana"}],
            "container-title": "Jurnal Informatika dan Teknik Elektro Terapan",
            "volume": "10",
            "issue": "1",
            "issued": {"date-parts": [[2022]]},
        },
    },
    6: {
        "display": '[6] Murdani, A. S. Sembiring, and T. S. Alasi, "Penerapan Data Mining Menggunakan Algoritma Apriori Pada Peminjaman Buku di Perpustakaan Pada Pesantren Babul Ulum," Jurnal Armada Informatika, vol. 7, no. 2, pp. 323-327, 2023.',
        "itemData": {
            "id": "ref-6",
            "type": "article-journal",
            "title": "Penerapan Data Mining Menggunakan Algoritma Apriori Pada Peminjaman Buku di Perpustakaan Pada Pesantren Babul Ulum",
            "author": [{"literal": "Murdani"}, {"family": "Sembiring", "given": "A. S."}, {"family": "Alasi", "given": "T. S."}],
            "container-title": "Jurnal Armada Informatika",
            "volume": "7",
            "issue": "2",
            "page": "323-327",
            "issued": {"date-parts": [[2023]]},
        },
    },
    7: {
        "display": '[7] Y. Andini, J. T. Hardinata, and Y. P. Purba, "Penerapan Data Mining Terhadap Tata Letak Buku di Perpustakaan Sintong Bingei Pematangsiantar Menggunakan Metode Apriori," Jurnal TIMES, vol. 11, no. 1, pp. 9-15, 2022.',
        "itemData": {
            "id": "ref-7",
            "type": "article-journal",
            "title": "Penerapan Data Mining Terhadap Tata Letak Buku di Perpustakaan Sintong Bingei Pematangsiantar Menggunakan Metode Apriori",
            "author": [{"family": "Andini", "given": "Y."}, {"family": "Hardinata", "given": "J. T."}, {"family": "Purba", "given": "Y. P."}],
            "container-title": "Jurnal TIMES",
            "volume": "11",
            "issue": "1",
            "page": "9-15",
            "issued": {"date-parts": [[2022]]},
        },
    },
    8: {
        "display": '[8] R. A. S. Prayoga, R. Basatha, M. S. Akbar, E. A. Elfaiz, and C. D. Putra, "Penerapan Data Mining untuk Peminjaman Buku dengan Menggunakan Algoritma Apriori," 2024.',
        "itemData": {
            "id": "ref-8",
            "type": "article-journal",
            "title": "Penerapan Data Mining untuk Peminjaman Buku dengan Menggunakan Algoritma Apriori",
            "author": [{"family": "Prayoga", "given": "R. A. S."}, {"family": "Basatha", "given": "R."}, {"family": "Akbar", "given": "M. S."}, {"family": "Elfaiz", "given": "E. A."}, {"family": "Putra", "given": "C. D."}],
            "issued": {"date-parts": [[2024]]},
        },
    },
    9: {
        "display": '[9] Haryono, Marisa, Carudin, and Ihsan, "Implementasi Algoritma Apriori dalam Memberikan Rekomendasi Buku pada Perpustakaan SMK Karya Guna 2 Bekasi," 2024.',
        "itemData": {
            "id": "ref-9",
            "type": "article-journal",
            "title": "Implementasi Algoritma Apriori dalam Memberikan Rekomendasi Buku pada Perpustakaan SMK Karya Guna 2 Bekasi",
            "author": [{"literal": "Haryono"}, {"literal": "Marisa"}, {"literal": "Carudin"}, {"literal": "Ihsan"}],
            "issued": {"date-parts": [[2024]]},
        },
    },
    10: {
        "display": '[10] M. Jannah, E. Yumami, A. Julianto, and E. Rahmi, "Sistem Rekomendasi Buku di Perpustakaan Menggunakan Machine Learning dan Algoritma Apriori," 2025.',
        "itemData": {
            "id": "ref-10",
            "type": "article-journal",
            "title": "Sistem Rekomendasi Buku di Perpustakaan Menggunakan Machine Learning dan Algoritma Apriori",
            "author": [{"family": "Jannah", "given": "M."}, {"family": "Yumami", "given": "E."}, {"family": "Julianto", "given": "A."}, {"family": "Rahmi", "given": "E."}],
            "issued": {"date-parts": [[2025]]},
        },
    },
}


CITATION_RULES = [
    ("Perkembangan teknologi informasi telah membawa perubahan besar", " [1]"),
    ("Perpustakaan tidak hanya berfungsi sebagai tempat penyimpanan koleksi buku", " [4]"),
    ("Data transaksi peminjaman sebenarnya memiliki potensi besar untuk dianalisis", " [5]-[7]"),
    ("Salah satu metode yang dapat digunakan untuk menemukan pola dari data transaksi", " [1]"),
    ("Algoritma Apriori merupakan salah satu algoritma dalam data mining", " [2]"),
    ("Penelitian ini berfokus pada penerapan data mining", " [5], [8]-[10]"),
    ("Data mining merupakan proses untuk menggali informasi", " [1]"),
    ("association rule mining", " [2]"),
    ("Sistem rekomendasi merupakan sistem yang digunakan", " [4]"),
    ("algoritma Apriori digunakan untuk menganalisis data transaksi peminjaman buku", " [5]-[10]"),
    ("Support merupakan ukuran yang menunjukkan tingkat kemunculan", " [2]"),
    ("Confidence merupakan ukuran yang menunjukkan tingkat kepercayaan", " [2]"),
    ("Lift digunakan untuk mengetahui kekuatan hubungan antar item", " [2]"),
    ("Penelitian yang dilakukan oleh Prayoga", " [8]"),
    ("Penelitian Haryono", " [9]"),
    ("Penelitian Jannah", " [10]"),
]


def esc(value: str) -> str:
    return html.escape(value, quote=False)


def attr(value: str) -> str:
    return html.escape(value, quote=True)


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


def citation_numbers(label: str) -> list[int]:
    nums: list[int] = []
    parts = re.findall(r"\d+(?:\s*-\s*\d+)?", label)
    for part in parts:
        if "-" in part:
            left, right = [int(x.strip()) for x in part.split("-", 1)]
            nums.extend(range(left, right + 1))
        else:
            nums.append(int(part))
    return [n for n in nums if n in REFS]


def zotero_citation_field(label: str) -> str:
    nums = citation_numbers(label)
    citation = {
        "citationID": "apriori-" + "-".join(str(n) for n in nums),
        "properties": {"formattedCitation": label, "plainCitation": label, "noteIndex": 0},
        "citationItems": [
            {
                "id": REFS[n]["itemData"]["id"],
                "uris": [f"http://zotero.org/users/local/apriori/items/REF{n}"],
                "itemData": REFS[n]["itemData"],
            }
            for n in nums
        ],
        "schema": "https://github.com/citation-style-language/schema/raw/master/csl-citation.json",
    }
    instr = " ADDIN ZOTERO_ITEM CSL_CITATION " + json.dumps(citation, ensure_ascii=False, separators=(",", ":"))
    return f'<w:fldSimple w:instr="{attr(instr)}">{run_xml(label)}</w:fldSimple>'


def zotero_bibliography_field() -> str:
    bibliography = {
        "uncited": [],
        "omitted": [],
        "custom": [],
    }
    instr = " ADDIN ZOTERO_BIBL " + json.dumps(bibliography, ensure_ascii=False, separators=(",", ":"))
    return f'<w:p>{paragraph_props(None, "center")}<w:fldSimple w:instr="{attr(instr)}">{run_xml("DAFTAR PUSTAKA")}</w:fldSimple></w:p>'


def run_xml(text: str) -> str:
    return (
        '<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>'
        f'<w:sz w:val="24"/></w:rPr><w:t xml:space="preserve">{esc(text)}</w:t></w:r>'
    )


def runs_with_citations(text: str) -> str:
    parts: list[str] = []
    pattern = re.compile(r"\[(?:\d+(?:\s*-\s*\d+)?)(?:,\s*\d+(?:\s*-\s*\d+)?)*\]")
    last = 0
    for match in pattern.finditer(text):
        if match.start() > last:
            parts.append(run_xml(text[last : match.start()]))
        parts.append(zotero_citation_field(match.group(0)))
        last = match.end()
    if last < len(text):
        parts.append(run_xml(text[last:]))
    return "".join(parts)


def paragraph_props(style: str | None = None, align: str | None = None) -> str:
    ppr_parts = []
    if style:
        ppr_parts.append(f'<w:pStyle w:val="{style}"/>')
    if align:
        ppr_parts.append(f'<w:jc w:val="{align}"/>')
    if style is None:
        ppr_parts.append('<w:spacing w:after="120" w:line="360" w:lineRule="auto"/>')
        ppr_parts.append('<w:ind w:firstLine="720"/>')
        ppr_parts.append('<w:jc w:val="both"/>')
    return f"<w:pPr>{''.join(ppr_parts)}</w:pPr>"


def para_xml(text: str, style: str | None = None, align: str | None = None) -> str:
    return f"<w:p>{paragraph_props(style, align)}{runs_with_citations(text)}</w:p>"


def heading_xml(text: str, level: int) -> str:
    if level == 1:
        return para_xml(text, "Heading1", "center")
    if level == 2:
        return para_xml(text, "Heading2")
    return para_xml(text, "Heading3")


def list_xml(text: str, ordered: bool = False) -> str:
    bullet = "" if ordered else "\u2022 "
    cleaned = re.sub(r"^\d+\.\s+", "", text)
    return f'<w:p><w:pPr><w:spacing w:after="80"/><w:ind w:left="720" w:hanging="360"/></w:pPr>{runs_with_citations(bullet + cleaned)}</w:p>'


def table_xml(rows: list[list[str]]) -> str:
    col_count = max(len(row) for row in rows)
    cell_width = int(9000 / max(col_count, 1))
    body = ['<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:tblBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/><w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/></w:tblBorders></w:tblPr>']
    for row_index, row in enumerate(rows):
        body.append("<w:tr>")
        for cell in row:
            body.append(f'<w:tc><w:tcPr><w:tcW w:w="{cell_width}" w:type="dxa"/></w:tcPr>')
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
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <dc:title>BAB I-III Revisi Zotero Fields</dc:title>
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
    blocks.append(zotero_bibliography_field())
    for ref in REFS.values():
        blocks.append(para_xml(ref["display"]))
    write_docx("\n".join(blocks))
    print(OUTPUT)


if __name__ == "__main__":
    main()
