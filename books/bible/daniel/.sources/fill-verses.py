#!/usr/bin/env python3
"""fill-verses.py <file.md>   — expand {{cuv 4:17}} / {{cuv 4:17-18}} / {{nasb 7:14}} markers in place with the exact
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
p = Path(sys.argv[1]); t = p.read_text()
new = re.sub(r"\{\{(cuv|nasb) (\d+):(\d+)(?:-(\d+))?\}\}", expand, t)
p.write_text(new); print("filled", len(re.findall(r"\{\{(?:cuv|nasb) ", t)), "markers in", p.name)
