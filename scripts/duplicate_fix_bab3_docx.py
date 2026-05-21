from __future__ import annotations

import copy
import html
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "LAPORAN AKHIR ANISA - REVISI.docx"
OUTPUT = ROOT / "LAPORAN AKHIR ANISA - REVISI BAB 3 FIX.docx"

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NAMESPACES = {
    "wpc": "http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas",
    "mc": "http://schemas.openxmlformats.org/markup-compatibility/2006",
    "o": "urn:schemas-microsoft-com:office:office",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
    "v": "urn:schemas-microsoft-com:vml",
    "wp14": "http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "w10": "urn:schemas-microsoft-com:office:word",
    "w": W,
    "w14": "http://schemas.microsoft.com/office/word/2010/wordml",
    "w15": "http://schemas.microsoft.com/office/word/2012/wordml",
    "w16cex": "http://schemas.microsoft.com/office/word/2018/wordml/cex",
    "w16cid": "http://schemas.microsoft.com/office/word/2016/wordml/cid",
    "w16": "http://schemas.microsoft.com/office/word/2018/wordml",
    "w16sdtdh": "http://schemas.microsoft.com/office/word/2020/wordml/sdtdatahash",
    "w16se": "http://schemas.microsoft.com/office/word/2015/wordml/symex",
    "wpg": "http://schemas.microsoft.com/office/word/2010/wordprocessingGroup",
    "wpi": "http://schemas.microsoft.com/office/word/2010/wordprocessingInk",
    "wne": "http://schemas.microsoft.com/office/word/2006/wordml",
    "wps": "http://schemas.microsoft.com/office/word/2010/wordprocessingShape",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
}

for prefix, uri in NAMESPACES.items():
    ET.register_namespace(prefix, uri)

NS = {"w": W}


IMAGE_REPLACEMENTS = {
    "word/media/image1.png": ROOT / "docs" / "diagrams" / "diagram_04.png",
    "word/media/image2.png": ROOT / "docs" / "diagrams" / "diagram_09.png",
    "word/media/image3.png": ROOT / "docs" / "diagrams" / "diagram_03.png",
    "word/media/image4.png": ROOT / "docs" / "diagrams" / "diagram_02.png",
    "word/media/image5.png": ROOT / "docs" / "diagrams" / "diagram_05.png",
    "word/media/image6.png": ROOT / "docs" / "diagrams" / "diagram_07.png",
    "word/media/image7.png": ROOT / "docs" / "diagrams" / "diagram_08.png",
}

NEW_REFERENCES = [
    '[23] A. Wibowo, V. I. Ivanoti, and M. H. P. Sari, "Employee Education and Training Recommendations using the Apriori Algorithm," Jurnal RESTI (Rekayasa Sistem dan Teknologi Informasi), vol. 7, no. 5, pp. 1118-1131, 2023, doi: 10.29207/resti.v7i5.4973.',
    '[24] N. T. S. Saptadi, P. Chyan, and J. M. Leda, "Analysis of Supermarket Product Purchase Transactions With the Association Data Mining Method," Jurnal RESTI (Rekayasa Sistem dan Teknologi Informasi), vol. 7, no. 3, pp. 618-627, 2023, doi: 10.29207/resti.v7i3.4844.',
    '[25] R. Hammad, M. Azwar, and M. A. Syarif, "Optimizing Tourism Recommendations with a Hybrid Model: Bridging User Preferences and Behavioral Patterns," Jurnal RESTI (Rekayasa Sistem dan Teknologi Informasi), vol. 9, no. 4, pp. 894-904, 2025, doi: 10.29207/resti.v9i4.6510.',
    '[26] N. Hafiz, O. C. Briliyant, D. F. Priambodo, M. Hasbi, and S. Siswanti, "Remote Penetration Testing with Telegram Bot," Jurnal RESTI (Rekayasa Sistem dan Teknologi Informasi), vol. 7, no. 3, pp. 705-714, 2023, doi: 10.29207/resti.v7i3.4870.',
]


def qn(tag: str) -> str:
    return f"{{{W}}}{tag}"


def text_of(element: ET.Element) -> str:
    return "".join((t.text or "") for t in element.findall(".//w:t", NS)).strip()


def esc(value: str) -> str:
    return html.escape(value, quote=False)


def p(text: str = "", style: str | None = None, align: str | None = None) -> ET.Element:
    style_xml = f'<w:pStyle w:val="{style}"/>' if style else ""
    align_xml = f'<w:jc w:val="{align}"/>' if align else ""
    spacing = "" if style else '<w:spacing w:after="120" w:line="360" w:lineRule="auto"/>'
    indent = "" if style or not text else '<w:ind w:firstLine="720"/>'
    justify = "" if style or align or not text else '<w:jc w:val="both"/>'
    xml = f"""
    <w:p xmlns:w="{W}">
      <w:pPr>{style_xml}{align_xml}{spacing}{indent}{justify}</w:pPr>
      <w:r>
        <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr>
        <w:t xml:space="preserve">{esc(text)}</w:t>
      </w:r>
    </w:p>
    """
    return ET.fromstring(xml)


def field_p(instr: str, display: str) -> ET.Element:
    xml = f"""
    <w:p xmlns:w="{W}">
      <w:pPr><w:spacing w:after="120"/></w:pPr>
      <w:fldSimple w:instr="{html.escape(instr, quote=True)}">
        <w:r>
          <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="24"/></w:rPr>
          <w:t xml:space="preserve">{esc(display)}</w:t>
        </w:r>
      </w:fldSimple>
    </w:p>
    """
    return ET.fromstring(xml)


def caption_p(label: str, seq_name: str, number: int) -> ET.Element:
    # SEQ membuat caption dapat dibaca oleh fitur Table of Figures/Tables Word.
    chapter_prefix = "3."
    xml = f"""
    <w:p xmlns:w="{W}">
      <w:pPr><w:spacing w:after="120"/><w:jc w:val="center"/></w:pPr>
      <w:r>
        <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="22"/></w:rPr>
        <w:t xml:space="preserve">{seq_name} {chapter_prefix}</w:t>
      </w:r>
      <w:fldSimple w:instr=" SEQ {seq_name} \\* ARABIC ">
        <w:r>
          <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="22"/></w:rPr>
          <w:t>{number}</w:t>
        </w:r>
      </w:fldSimple>
      <w:r>
        <w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="22"/></w:rPr>
        <w:t xml:space="preserve"> {esc(label)}</w:t>
      </w:r>
    </w:p>
    """
    return ET.fromstring(xml)


def table(rows: list[list[str]], caption: str, number: int) -> list[ET.Element]:
    col_count = max(len(row) for row in rows)
    width = int(9000 / max(col_count, 1))
    parts = [
        f'<w:tbl xmlns:w="{W}"><w:tblPr><w:tblW w:w="0" w:type="auto"/>'
        '<w:tblBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:left w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:right w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="auto"/>'
        '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="auto"/></w:tblBorders></w:tblPr>'
    ]
    for idx, row in enumerate(rows):
        parts.append("<w:tr>")
        for cell in row:
            bold = "<w:b/>" if idx == 0 else ""
            parts.append(
                f'<w:tc><w:tcPr><w:tcW w:w="{width}" w:type="dxa"/></w:tcPr>'
                f'<w:p><w:pPr><w:spacing w:after="80"/></w:pPr><w:r><w:rPr>{bold}'
                '<w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:sz w:val="22"/>'
                f'</w:rPr><w:t xml:space="preserve">{esc(cell)}</w:t></w:r></w:p></w:tc>'
            )
        parts.append("</w:tr>")
    parts.append("</w:tbl>")
    return [ET.fromstring("".join(parts)), caption_p(caption, "Tabel", number)]


def find_body_child_index(body: ET.Element, target_text: str, start: int = 0) -> int:
    for idx, child in enumerate(list(body)[start:], start=start):
        if child.tag == qn("p") and text_of(child) == target_text:
            return idx
    raise ValueError(f"Text not found: {target_text}")


def replace_between(body: ET.Element, start_text: str, end_text: str, new_children: list[ET.Element]) -> None:
    children = list(body)
    start = find_body_child_index(body, start_text)
    end = find_body_child_index(body, end_text, start + 1)
    body[:] = children[:start] + new_children + children[end:]


def replace_list_sections(body: ET.Element) -> None:
    children = list(body)
    daftar_gambar = find_body_child_index(body, "DAFTAR GAMBAR")
    daftar_tabel = find_body_child_index(body, "DAFTAR TABEL", daftar_gambar + 1)
    abstrak = find_body_child_index(body, "ABSTRAK", daftar_tabel + 1)

    gambar_field = field_p(' TOC \\h \\z \\c "Gambar" ', "Klik kanan lalu pilih Update Field untuk memuat daftar gambar.")
    tabel_field = field_p(' TOC \\h \\z \\c "Tabel" ', "Klik kanan lalu pilih Update Field untuk memuat daftar tabel.")

    updated = (
        children[: daftar_gambar + 1]
        + [gambar_field, p()]
        + children[daftar_tabel : daftar_tabel + 1]
        + [tabel_field, p()]
        + children[abstrak:]
    )
    body[:] = updated


def append_new_references(body: ET.Element) -> None:
    existing_texts = [text_of(child) for child in list(body) if child.tag == qn("p")]
    refs_to_add = [ref for ref in NEW_REFERENCES if ref[:4] not in {text[:4] for text in existing_texts}]
    if not refs_to_add:
        return

    children = list(body)
    insert_at = len(children)
    for idx, child in enumerate(children):
        if child.tag == qn("sectPr"):
            insert_at = idx
            break

    body[:] = children[:insert_at] + [p(ref) for ref in refs_to_add] + children[insert_at:]


def ensure_document_namespaces(document_xml: bytes) -> bytes:
    text = document_xml.decode("utf-8")
    required = {
        "xmlns:wp14": NAMESPACES["wp14"],
        "xmlns:w16cex": NAMESPACES["w16cex"],
        "xmlns:w16cid": NAMESPACES["w16cid"],
        "xmlns:w16": NAMESPACES["w16"],
        "xmlns:w16sdtdh": NAMESPACES["w16sdtdh"],
        "xmlns:w16se": NAMESPACES["w16se"],
    }
    insertions = []
    for attr_name, uri in required.items():
        if attr_name not in text:
            insertions.append(f' {attr_name}="{uri}"')
    if insertions:
        text = text.replace("<w:document ", "<w:document " + "".join(insertions) + " ", 1)
    return text.encode("utf-8")


def collect_original_drawings(body: ET.Element) -> list[ET.Element]:
    start = find_body_child_index(body, "BAB III")
    end = find_body_child_index(body, "BAB IV", start + 1)
    drawings: list[ET.Element] = []
    for child in list(body)[start:end]:
        if child.findall(".//w:drawing", NS):
            drawings.append(copy.deepcopy(child))
    return drawings


def build_bab3(drawings: list[ET.Element]) -> list[ET.Element]:
    flow, architecture, usecase, erd, activity, sequence, deployment = drawings[:7]
    children: list[ET.Element] = [
        p("BAB III", "Heading1", "center"),
        p("METODE PENELITIAN", "Heading1", "center"),
        p(),
        p("3.1 Prosedur Penelitian", "Heading2"),
        p("Penelitian ini merupakan penelitian rancang bangun sistem analisis pola peminjaman buku berbasis web dengan menerapkan algoritma Apriori. Sistem yang dibangun digunakan untuk mengolah data transaksi peminjaman perpustakaan, menemukan pola keterkaitan antara asal peminjam dan buku yang dipinjam, serta menampilkan hasil analisis dalam bentuk association rules yang mudah dibaca. Penggunaan Apriori relevan karena algoritma ini dapat digunakan untuk membentuk rekomendasi berdasarkan data historis dan pola keterkaitan antar item [23]."),
        p("Secara umum, penelitian dilakukan melalui tahapan identifikasi masalah, pengumpulan data, analisis kebutuhan, preprocessing data, penerapan algoritma Apriori, perancangan sistem, implementasi sistem, dan pengujian. Tahapan tersebut disusun agar penelitian tidak hanya menghasilkan perhitungan algoritma, tetapi juga menghasilkan sistem yang dapat digunakan untuk membantu pengguna membaca pola peminjaman buku. Pendekatan association data mining digunakan karena mampu menemukan pola transaksi dan hubungan antar item berdasarkan data yang tersedia [24]."),
        flow,
        caption_p("Prosedur penelitian rancang bangun sistem analisis pola peminjaman buku", "Gambar", 1),
    ]
    children += table(
        [
            ["No", "Tahapan", "Uraian"],
            ["1", "Identifikasi masalah", "Menentukan masalah belum optimalnya pemanfaatan data transaksi peminjaman buku."],
            ["2", "Pengumpulan data", "Mengumpulkan dataset peminjaman buku dalam format CSV."],
            ["3", "Preprocessing data", "Membersihkan data dan membentuk transaksi dari no_mhs, tgl_pinjam, dan tgl_kembali."],
            ["4", "Penerapan Apriori", "Menghitung frequent itemset dan association rules."],
            ["5", "Implementasi sistem", "Membangun frontend, backend API, database, dan engine Apriori."],
            ["6", "Pengujian", "Menguji import CSV, run analisis, filter rules, detail aturan, dan riwayat analisis."],
        ],
        "Tahapan prosedur penelitian",
        1,
    )
    children += [
        p("3.2 Analisis Sistem", "Heading2"),
        p("3.2.1 Analisis Sistem yang Berjalan", "Heading3"),
        p("Pada sistem yang berjalan, data peminjaman buku berfungsi sebagai catatan transaksi. Data tersebut menyimpan informasi mengenai peminjam, buku yang dipinjam, dan tanggal transaksi. Namun, data peminjaman belum dimanfaatkan secara optimal untuk menemukan pola kecenderungan peminjaman."),
        p("3.2.2 Analisis Sistem yang Diusulkan", "Heading3"),
        p("Sistem yang diusulkan adalah sistem berbasis web untuk menganalisis pola peminjaman buku menggunakan algoritma Apriori. Pengguna dapat mengunggah dataset peminjaman dalam format CSV, kemudian sistem melakukan validasi, preprocessing, penyimpanan data, dan analisis Apriori. Sistem rekomendasi dapat memanfaatkan pola perilaku pengguna dan hubungan antar item untuk menghasilkan rekomendasi yang lebih sesuai dengan konteks data [25]."),
        architecture,
        caption_p("Arsitektur komponen sistem yang diusulkan", "Gambar", 2),
        p("3.3 Perancangan Sistem", "Heading2"),
        p("Perancangan sistem menggambarkan fungsi utama, rancangan data, alur aktivitas, urutan komunikasi, dan rancangan antarmuka sistem yang dibangun. Sistem dibagi menjadi frontend React, backend FastAPI, database PostgreSQL, dan engine Apriori. Perancangan ini dibuat agar proses import data, analisis Apriori, penyimpanan hasil, dan penyajian association rules dapat berjalan secara terstruktur."),
        p("3.3.1 Use Case", "Heading3"),
        p("Use case diagram digunakan untuk menggambarkan interaksi aktor dengan sistem. Aktor utama pada sistem ini adalah pengguna atau admin perpustakaan. Fungsi utama yang tersedia meliputi import dataset CSV, menjalankan analisis Apriori, melihat riwayat analisis, memfilter hasil rules, melihat detail aturan, dan menghapus riwayat analisis yang tidak diperlukan."),
        usecase,
        caption_p("Use case sistem analisis pola peminjaman buku", "Gambar", 3),
        p("3.3.2 Arsitektur Data", "Heading3"),
        p("Data yang digunakan dalam penelitian ini adalah data transaksi peminjaman buku perpustakaan dalam format CSV. Struktur data memuat no_barcode, no_mhs, nama, fakultas, kd_buku, judul, tgl_pinjam, dan tgl_kembali."),
        p("Dalam proses preprocessing, satu transaksi dibentuk dari gabungan no_mhs, tgl_pinjam, dan tgl_kembali. Penggabungan ini dilakukan karena seorang peminjam dapat meminjam lebih dari satu buku pada tanggal yang sama. Setelah transaksi terbentuk, sistem menyusun item transaksi menjadi dua jenis item utama, yaitu item asal peminjam dan item buku. Proses pembentukan transaksi seperti ini diperlukan agar association rule mining dapat membaca data sebagai himpunan item yang saling berhubungan [24]."),
    ]
    children += table(
        [
            ["Transaksi", "Item"],
            ["T1", "Jurusan: Teknik Informatika; Buku: Sistem Informasi Manajemen; Buku: Basis Data"],
            ["T2", "Jurusan: Sistem Informasi; Buku: Algoritma dan Struktur Data"],
            ["T3", "Jurusan: Manajemen Informatika; Buku: Sistem Informasi Manajemen"],
        ],
        "Contoh pembentukan transaksi untuk algoritma Apriori",
        2,
    )
    children += [
        p("Arsitektur data dirancang menggunakan tabel departments, students, books, loan_transactions, loan_transaction_items, analysis_runs, dan association_rules. Tabel departments menyimpan data fakultas atau jurusan, tabel students menyimpan data peminjam, tabel books menyimpan data buku, sedangkan tabel loan_transactions dan loan_transaction_items menyimpan data transaksi peminjaman. Tabel analysis_runs dan association_rules digunakan untuk menyimpan riwayat analisis dan hasil rules."),
        erd,
        caption_p("Entity Relationship Diagram sistem", "Gambar", 4),
        p("3.3.3 Activity Diagram", "Heading3"),
        p("Activity diagram menggambarkan alur kerja pengguna dan sistem mulai dari import CSV sampai rules ditampilkan. Pengguna memilih file CSV, sistem memvalidasi data, menyimpan transaksi, pengguna mengisi parameter analisis, backend menjalankan Apriori, lalu hasil rules ditampilkan pada frontend."),
        activity,
        caption_p("Activity diagram proses analisis Apriori", "Gambar", 5),
        p("3.3.4 Sequence Diagram", "Heading3"),
        p("Sequence diagram digunakan untuk menggambarkan urutan komunikasi antar komponen saat pengguna menjalankan analisis. Frontend mengirim permintaan ke backend API, backend mengambil transaksi dari database, engine Apriori memproses data, kemudian hasil association rules disimpan dan dikembalikan ke frontend."),
        sequence,
        caption_p("Sequence diagram proses run analisis Apriori", "Gambar", 6),
        p("3.3.5 Perancangan Antar Muka", "Heading3"),
        p("Perancangan antarmuka dibuat agar pengguna dapat menjalankan proses analisis tanpa berinteraksi langsung dengan kode program. Komponen utama antarmuka terdiri atas panel import dataset CSV, panel jalankan analisis, riwayat analisis, perbandingan run, ringkasan rules, filter rules, tabel rules, dan detail aturan. Detail aturan ditampilkan dalam bentuk kalimat agar hasil analisis lebih mudah dipahami oleh pengguna."),
        deployment,
        caption_p("Deployment diagram sistem", "Gambar", 7),
        p("Penerapan algoritma Apriori pada sistem dilakukan setelah data transaksi berhasil dibentuk. Algoritma menghitung frequent itemset berdasarkan minimum support, kemudian membentuk association rules berdasarkan minimum confidence dan minimum lift. Pada sistem ini, rules yang ditampilkan difokuskan pada pola Jurusan -> Buku agar hasil analisis sesuai dengan tujuan rekomendasi buku berdasarkan asal peminjam. Apriori banyak digunakan untuk menemukan pola asosiasi dan membentuk rekomendasi berdasarkan data historis [23]."),
        p("Algoritma Apriori digunakan untuk menemukan pola asosiasi dari data transaksi. Proses dimulai dengan membaca seluruh transaksi yang sudah berbentuk itemset. Selanjutnya sistem menghitung nilai support dari setiap item dan kombinasi item. Itemset yang memenuhi nilai minimum support dipertahankan sebagai frequent itemset, sedangkan itemset yang tidak memenuhi nilai minimum support dieliminasi. Dalam association rule, support digunakan untuk melihat frekuensi kemunculan kombinasi item, sedangkan confidence digunakan untuk melihat tingkat keyakinan aturan yang terbentuk [24]."),
        p("Setelah frequent itemset ditemukan, sistem membentuk association rules dan menghitung nilai confidence serta lift. Pada sistem ini, association rules yang ditampilkan dibatasi pada pola Jurusan -> Buku. Pembatasan ini dilakukan agar hasil analisis sesuai dengan tujuan penelitian, yaitu mengetahui kecenderungan peminjaman buku berdasarkan asal peminjam. Nilai lift digunakan untuk menilai kekuatan hubungan antar item sehingga rule yang terbentuk tidak hanya dilihat dari frekuensi, tetapi juga dari kekuatan keterkaitannya [24]."),
        p("Pengujian sistem dilakukan untuk memastikan setiap fitur berjalan sesuai kebutuhan. Pengujian dilakukan pada fitur import CSV, proses penyimpanan data, proses analisis Apriori, tampilan rules, filter hasil, riwayat analisis, detail aturan, dan dokumentasi sistem. Selain pengujian fungsional, hasil algoritma juga divalidasi melalui Jupyter Notebook. Pendekatan black box testing digunakan karena pengujian berfokus pada kesesuaian input dan output dari fungsi sistem [26]."),
    ]
    return children


def main() -> None:
    with zipfile.ZipFile(SOURCE, "r") as zin:
        document_xml = zin.read("word/document.xml")
        root = ET.fromstring(document_xml)
        body = root.find("w:body", NS)
        assert body is not None

        original_drawings = collect_original_drawings(body)
        replace_list_sections(body)
        replace_between(body, "BAB III", "BAB IV", build_bab3(original_drawings))
        append_new_references(body)
        new_document_xml = ensure_document_namespaces(
            ET.tostring(root, encoding="utf-8", xml_declaration=True)
        )

        with zipfile.ZipFile(OUTPUT, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "word/document.xml":
                    data = new_document_xml
                if item.filename in IMAGE_REPLACEMENTS:
                    data = IMAGE_REPLACEMENTS[item.filename].read_bytes()
                zout.writestr(item, data)

    print(OUTPUT)


if __name__ == "__main__":
    main()
