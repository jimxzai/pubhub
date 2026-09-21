#!/usr/bin/env python3
"""Check release artifacts for content and navigation regressions."""
from pathlib import Path
import re
import zipfile
from html.parser import HTMLParser
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
NAME = "1cor-consolidated"
pdf = PdfReader(ROOT / "output/pdf" / (NAME + ".pdf"))
text = "\n".join(p.extract_text() or "" for p in pdf.pages)
assert len(pdf.outline) >= 30, "PDF bookmarks missing"
assert pdf.metadata.title.startswith("哥林多前書研讀"), "Incorrect title"
assert "哥林多前書" in (pdf.pages[0].extract_text() or ""), "Cover text lost"
for letter in "ABCDEF":
    assert f"Appendix {letter}:" in text, f"Missing appendix {letter}"
for phrase in ["Systematic Reception", "卷一", "卷二", "卷三", "卷四", "卷五"]:
    assert phrase in text, f"Missing section: {phrase}"
for p in pdf.pages:
    assert abs(float(p.mediabox.width) - 504) < 1
    assert abs(float(p.mediabox.height) - 720) < 1
def destinations(items):
    for item in items:
        if isinstance(item, list):
            yield from destinations(item)
        else:
            yield pdf.get_destination_page_number(item)
assert all(n is not None and 0 <= n < len(pdf.pages) for n in destinations(pdf.outline))

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        self.links.extend(attrs[k] for k in ("href", "src") if k in attrs)

html = ROOT / "output/html" / (NAME + ".html")
content = html.read_text()
content = re.sub(r"\s+", " ", content)
parsed = Links()
parsed.feed(content)
for ref in parsed.links:
    if ref.startswith("#"):
        assert ref[1:] in parsed.ids, f"Broken HTML anchor: {ref}"
    elif not re.match(r"[a-zA-Z]+:", ref):
        assert (html.parent / ref.split("#")[0]).exists(), f"Missing HTML asset: {ref}"
for letter in "ABCDEF":
    assert f"Appendix {letter}:" in content
with zipfile.ZipFile(ROOT / "output/epub" / (NAME + ".epub")) as archive:
    assert archive.testzip() is None
    names = archive.namelist()
    assert any(n.endswith("nav.xhtml") for n in names)
    body = re.sub(r"\s+", " ", "\n".join(archive.read(n).decode() for n in names if n.endswith(".xhtml")))
    for letter in "ABCDEF":
        assert f"Appendix {letter}:" in body
log = (ROOT / "build/1cor-consolidated.log").read_text(errors="replace")
assert "Missing character:" not in log, "Missing glyphs"
assert "Overfull" not in log, "Overflow requires visual review"
print(f"PASS: {len(pdf.pages)} PDF pages, {len(pdf.outline)} top-level bookmarks; A-F appendices in all formats; HTML assets/anchors and EPUB archive valid.")
