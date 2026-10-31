#!/usr/bin/env python3
"""fill-verses.py <file.md>   — also expands {{xref 徒 2:16-17}} (verbatim 和合本 from xref.py, as a block quote with the reference in bold).
Expands {{cuv 4:17}} / {{cuv 4:17-18}} / {{nasb 7:14}} markers in place with the exact
Daniel text from scripture-all.tsv (CUV keeps ^n^ verse markers off; output is plain text joined with no spaces,
NASB joined with a space). Use it for orientation/back-matter chapters so Scripture is never typed by hand."""
import re, sys
from pathlib import Path
tsv = {}
for l in (Path(__file__).parent / "scripture-all.tsv").read_text().splitlines():
    if l.startswith("#"): continue
    k, c, n = l.split("\t"); tsv[k] = (c, n)
def expand(m):
    kind, ch, v1, v2 = m.group(1), m.group(2), int(m.group(3)), int(m.group(4) or m.group(3))
    parts = [tsv[f"{ch}:{v}"][0 if kind == "cuv" else 1] for v in range(v1, v2 + 1)]
    return ("" if kind == "cuv" else " ").join(parts)
import importlib.util, re as _re
_spec = importlib.util.spec_from_file_location("xref", Path(__file__).parent / "xref.py"); xref = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(xref)
def expand_xref(m):
    ref = m.group(1).strip()
    mm = _re.match(r"^(\S+?)\s*(\d+):(\d+)(?:[-–](\d+))?$", ref)
    book, ch, v1 = mm.group(1), int(mm.group(2)), int(mm.group(3)); v2 = int(mm.group(4) or v1)
    verses = xref.cuv_chapter(book, ch)
    body = "".join((f"^{v}^" if v2 > v1 else "") + verses[v] for v in range(v1, v2 + 1))
    return f"> **{ref}**　{body}"
p = Path(sys.argv[1]); t = p.read_text()
t = _re.sub(r"\{\{xref ([^}]+)\}\}", expand_xref, t)
new = re.sub(r"\{\{(cuv|nasb) (\d+):(\d+)(?:-(\d+))?\}\}", expand, t)
p.write_text(new); print("filled", len(re.findall(r"\{\{(?:cuv|nasb) ", t)), "markers in", p.name)
