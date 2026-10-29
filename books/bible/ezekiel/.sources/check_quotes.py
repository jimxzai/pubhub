#!/usr/bin/env python3
"""Check every English commentary quote in a chapter against the .sources corpus.

  python3 .sources/check_quotes.py books/bible/ezekiel/01-by-the-river-chebar.md [more.md ...]

A quote line looks like:   > "…English text…"
It must appear, ignoring case, punctuation, spacing and curly/straight quotes, as a
substring of some file under commentary/ or fathers/ (text after the --- line in fathers/).
Exit 1 if any quote is not found. A quote that is found only because it is very short
(< 8 words) is reported as SHORT (a short quote proves little): lengthen it or drop the quotes.
Hymn lines and scripture blocks are not checked (they are not `> "…"` lines).
"""
import re, sys, glob, pathlib
SRC = pathlib.Path(__file__).resolve().parent
def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"[^a-z0-9]", "", s.lower())
corpus = {}
for f in sorted(glob.glob(str(SRC / "commentary" / "*.txt")) + glob.glob(str(SRC / "fathers" / "[0-9]*.txt"))):
    t = pathlib.Path(f).read_text(encoding="utf8", errors="ignore")
    if "/fathers/" in f and "\n---\n" in t: t = t.split("\n---\n", 1)[1]
    corpus[f] = norm(t)
bad = 0
for chapter in sys.argv[1:]:
    n = 0
    for i, line in enumerate(pathlib.Path(chapter).read_text(encoding="utf8").splitlines(), 1):
        m = re.match(r'^> "(.+)"\s*$', line)
        if not m: continue
        q = m.group(1); n += 1
        # ellipsis-joined quotes: every piece must be found
        pieces = [p for p in re.split(r"\s*(?:\.\.\.|…|\[…\]|\[\.\.\.\])\s*", q) if norm(p)]
        hits = []
        for p in pieces:
            k = norm(p)
            found = [pathlib.Path(f).name for f, c in corpus.items() if k in c]
            hits.append(found)
        if all(hits):
            words = len(q.split())
            tag = "SHORT" if words < 8 else "OK   "
            if tag == "SHORT": bad += 0
            print(f"{tag} {pathlib.Path(chapter).name}:{i} -> {', '.join(sorted(set(hits[0]))[:3])}")
        else:
            bad += 1
            print(f"MISS  {pathlib.Path(chapter).name}:{i}  {q[:90]}…")
    print(f"-- {pathlib.Path(chapter).name}: {n} quotes")
sys.exit(1 if bad else 0)
