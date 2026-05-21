from __future__ import annotations

import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / "LAPORAN AKHIR ANISA - REVISI.docx"
NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


root = ET.fromstring(zipfile.ZipFile(DOCX).read("word/document.xml"))
paras = root.findall(".//w:body/w:p", NS)
rels_root = ET.fromstring(zipfile.ZipFile(DOCX).read("word/_rels/document.xml.rels"))
rels = {
    rel.attrib.get("Id"): rel.attrib.get("Target")
    for rel in rels_root
}

for i, para in enumerate(paras):
    text = "".join((t.text or "") for t in para.findall(".//w:t", NS))
    drawings = len(para.findall(".//w:drawing", NS))
    if 145 <= i <= 245 or drawings:
        print(f"{i}\tDRAW={drawings}\t{text[:220]}")
        blips = para.findall(".//a:blip", NS)
        for blip in blips:
            rid = blip.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
            print(f"\timage_rid={rid}\ttarget={rels.get(rid)}")
