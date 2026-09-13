#!/usr/bin/env python3
"""Generate the 2 Chronicles volume's citation ledger table from the book itself.

WHY THIS EXISTS
---------------
Same rationale as scripts/gen-numbers-citation-ledger.py: derive the ledger,
never hand-maintain it — a hand-kept ledger drifts from what the chapters
actually contain, and check-citation-ledger.py depends on this table being
accurate.

This walks the chapter files, counts `> "…"` verbatim quotes under each
commentator's `### ` subsection, and rewrites the table between the marker
comments in 99-appendix-references.md.

Usage:  python3 scripts/gen-chronicl2-citation-ledger.py --write
        python3 scripts/gen-chronicl2-citation-ledger.py            # print
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKDIR = ROOT / "books" / "bible" / "chronicl2"
LEDGER = BOOKDIR / "99-appendix-references.md"
START = "<!-- gen-citation-ledger:start -->"
END = "<!-- gen-citation-ledger:end -->"

HEADING = re.compile(r"^### (.+?)$", re.M)
QUOTE = re.compile(r'^> "', re.M)
COMMENTATORS = [("馬太·亨利", "亨利"), ("摩根", "摩根"), ("麥克阿瑟", "麥克阿瑟")]
# Patristic writers appear in a small number of chapters only; counted
# together so the ledger shows what the book actually carries rather than a
# column of zeros for writers this book barely cites.
FATHERS = ("居普良", "屈梭多模", "耶柔米", "區利羅", "俄利根", "奧古斯丁", "教父")


def count(text, name):
    heads = list(HEADING.finditer(text))
    n = 0
    for i, h in enumerate(heads):
        if name not in h.group(1):
            continue
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        nxt = text.find("\n## ", h.end())
        if nxt != -1:
            end = min(end, nxt)
        n += len(QUOTE.findall(text[h.end():end]))
    return n


def title_of(text):
    m = re.search(r"^# (.+?)\s*\(", text, re.M)
    return m.group(1).strip() if m else ""


def build():
    rows = ["| 章 | 章題 | 亨利引文 | 摩根引文 | 麥克阿瑟引文 | 教父引文 |",
            "|--------|--------------------|--------|--------|--------|--------|"]
    th = tm = tmc = tf = 0
    chapter_files = [f for f in sorted(BOOKDIR.glob("[0-9][0-9]-*.md"))
                      if 1 <= int(f.name[:2]) <= 36]
    for f in chapter_files:
        num = int(f.name[:2])
        text = f.read_text(encoding="utf-8")
        h, m, mc = count(text, "亨利"), count(text, "摩根"), count(text, "麥克阿瑟")
        fa = sum(count(text, name) for name in FATHERS)
        if not (h or m or mc or fa):
            continue
        th += h
        tm += m
        tmc += mc
        tf += fa
        rows.append(f"| 第 {num} 章 | {title_of(text)} | {h} | {m} | {mc or '—'} | {fa or '—'} |")
    rows.append(f"| **合計** | **{len(chapter_files)} 章** | **{th}** | **{tm}** | **{tmc}** | **{tf}** |")
    return "\n".join(rows)


def main():
    table = build()
    if "--write" in sys.argv:
        text = LEDGER.read_text(encoding="utf-8")
        a, b = text.find(START), text.find(END)
        if a < 0 or b < 0:
            sys.exit(f"markers not found in {LEDGER}")
        new = text[:a + len(START)] + "\n" + table + "\n" + text[b:]
        if new != text:
            LEDGER.write_text(new, encoding="utf-8")
            print(f"updated {LEDGER.name}")
        else:
            print(f"{LEDGER.name} already current")
        return 0
    print(table)
    return 0


if __name__ == "__main__":
    sys.exit(main())
