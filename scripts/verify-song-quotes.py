#!/usr/bin/env python3
"""Verify the verbatim English commentary quotes in books/bible/songofsolomen.

Each chapter quotes several works, so a quote is checked against the source
FAMILY named in its attribution line (the `> — …` line after it):

  Gill → commentary/gill-*.txt        Delitzsch / K&D → commentary/kd-*.txt
  Pulpit → pulpit-*   Cambridge → cambridge-*   JFB → jfb-*   Ellicott → ellicott-*
  Poole → poole-*     Benson → benson-*         Barnes → barnes-*   Geneva → geneva-*
  Henry → longform/henry-ch*.txt, commentary/henry-concise-*.txt
  Bernard → longform/bernard-sermon-*.txt   Taylor → longform/taylor-*.txt
  Spurgeon → longform/spurgeon-*.txt

Matching ignores case, punctuation, whitespace and curly quotes (OCR-unstable);
it is strict about words. A quote containing "…" or "..." is split and every
piece must match. Quotes that contain Hebrew/Greek letters are checked with
those letters removed from both sides (biblehub flattens them).

Usage: verify-song-quotes.py [book_dir] [-v]
Exit 1 if any quote is MISS.
"""
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books/bible/songofsolomen"
SRC = BOOK / ".sources"

FAMILIES = [
    (r"Gill|紀爾", ["commentary/gill-*.txt"]),
    (r"Delitzsch|Keil|K&D|凱爾", ["commentary/kd-*.txt"]),
    (r"Pulpit Commentary|講壇釋經", ["commentary/pulpit-*.txt"]),
    (r"Cambridge|劍橋", ["commentary/cambridge-*.txt"]),
    (r"JFB|Jamieson|Fausset|Brown", ["commentary/jfb-*.txt"]),
    (r"Ellicott|艾利考特", ["commentary/ellicott-*.txt"]),
    (r"Poole|波爾", ["commentary/poole-*.txt"]),
    (r"Benson|本森", ["commentary/benson-*.txt"]),
    (r"Barnes|巴恩斯", ["commentary/barnes-*.txt"]),
    (r"Geneva|日內瓦", ["commentary/geneva-*.txt"]),
    (r"Matthew Henry|亨利|Henry", ["longform/henry-ch*.txt", "commentary/henry-concise-*.txt"]),
    (r"Bernard|伯爾拿", ["longform/bernard-sermon-*.txt"]),
    (r"Taylor|戴德生", ["longform/taylor-*.txt"]),
    (r"Spurgeon|司布真", ["longform/spurgeon-*.txt"]),
    (r"Morgan|摩根", ["longform/morgan-*.txt"]),
]


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = re.sub(r"[Ͱ-Ͽἀ-῿֐-׿]", "", s)  # Greek, Hebrew
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "", s)
    return s


_cache = {}


def family_text(globs):
    key = tuple(globs)
    if key not in _cache:
        parts = []
        for g in globs:
            for f in sorted(SRC.glob(g)):
                parts.append(norm(f.read_text(encoding="utf8", errors="ignore")))
        _cache[key] = "".join(parts)
    return _cache[key]


def family_for(attr: str):
    for pat, globs in FAMILIES:
        if re.search(pat, attr):
            return globs
    return None


def blocks(md: str):
    """Yield (start_line, quote_text, attribution) for each `> "…"` block."""
    lines = md.split("\n")
    i = 0
    section = ""
    while i < len(lines):
        if lines[i].startswith("## "):
            section = lines[i]
        if section.startswith("## 配詩") and lines[i].startswith(">"):
            i += 1
            continue  # hymn stanzas are checked against .sources/hymns.md, not commentary
        if re.match(r'^>\s*["“]', lines[i]):
            start = i
            q = []
            while i < len(lines) and lines[i].startswith(">") and not re.match(r"^>\s*—", lines[i]):
                t = lines[i][1:].strip()
                if t:
                    q.append(t)
                else:
                    break
                i += 1
            # skip blank '>' line(s) to find the attribution
            j = i
            attr = ""
            while j < len(lines) and lines[j].startswith(">"):
                if re.match(r"^>\s*—", lines[j]):
                    attr = lines[j][1:].strip()
                    break
                j += 1
            yield start + 1, " ".join(q), attr
            i = max(i, j) + 1
        else:
            i += 1


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    verbose = "-v" in sys.argv
    book = Path(args[0]) if args else BOOK
    files = sorted(p for p in book.glob("*.md") if re.match(r"^\d", p.name))
    bad = 0
    total = 0
    for f in files:
        md = f.read_text(encoding="utf8")
        last_fam = None
        for ln, q, attr in blocks(md):
            if not re.search(r"[A-Za-z]{4,}", q):
                continue  # Chinese-only blockquote (hymn, psalm, prayer)
            if re.match(r'^>?\s*["“]?[一-鿿]', q):
                continue
            total += 1
            fam = family_for(attr)
            if fam is None and "同上" in attr:
                fam = last_fam
            if fam is not None:
                last_fam = fam
            if fam is None:
                # '同上' lines inherit; attribution-less quotes are errors
                print(f"NOSRC  {f.name}:{ln}  attribution not recognised: {attr[:60]!r}")
                bad += 1
                continue
            hay = family_text(fam)
            body = q.strip().strip('"“”')
            pieces = [p for p in re.split(r"…|\.\.\.", body) if norm(p)]
            miss = [p for p in pieces if norm(p) not in hay]
            if miss:
                bad += 1
                print(f"MISS   {f.name}:{ln}  [{attr[:48]}]  {miss[0][:90]!r}")
            elif verbose:
                print(f"OK     {f.name}:{ln}  [{attr[:48]}]")
    print(f"\n{total} quotes checked, {bad} problem(s)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
