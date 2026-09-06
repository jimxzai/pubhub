#!/usr/bin/env python3
"""Generate the Numbers volume's person-and-place index from the book's own text.

WHY THIS EXISTS
---------------
The volume had a Scripture index and a citation ledger, both generated, but no
way for a reader to answer "where does this book discuss Balaam?" or "which
chapter covers Kadesh?" — the 讀者可用性 row of the house rubric.

A hand-kept index would drift out of sync the moment a chapter is edited, the
same failure `gen-numbers-scripture-index.py` exists to prevent. So the TERM
LIST is curated by hand (which names matter in Numbers is an editorial
judgment a script cannot make) and the LOCATIONS are derived mechanically from
the chapter files every time it runs.

Only occurrences in the study text are counted — the `## 經文` blocks are
skipped, because a name appearing in the Bible text itself tells the reader
nothing about where the book *discusses* it.

Usage:  python3 scripts/gen-numbers-name-index.py --write
        python3 scripts/gen-numbers-name-index.py            # print
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKDIR = ROOT / "books" / "bible" / "numbers"
APPENDIX = BOOKDIR / "98-appendix-indices.md"
UBIQUITOUS = 15   # above this many chapters, list a note instead of every chapter
START = "<!-- gen-name-index:start -->"
END = "<!-- gen-name-index:end -->"

# Curated: the people and places this book actually turns on. Aliases share an
# entry (「老弟兄」 is not indexed — he is the method, not a subject).
PEOPLE = [
    ("摩西", ["摩西"]),
    ("亞倫", ["亞倫"]),
    ("米利暗", ["米利暗"]),
    ("以利亞撒", ["以利亞撒"]),
    ("約書亞", ["約書亞"]),
    ("迦勒", ["迦勒"]),
    ("可拉", ["可拉"]),
    ("大坍、亞比蘭", ["大坍", "亞比蘭"]),
    ("巴蘭", ["巴蘭"]),
    ("巴勒", ["巴勒"]),
    ("非尼哈", ["非尼哈"]),
    ("西羅非哈的女兒", ["西羅非哈"]),
    ("何巴", ["何巴"]),
]
PLACES = [
    ("西奈曠野", ["西奈"]),
    ("加低斯（巴尼亞）", ["加低斯"]),
    ("巴蘭曠野", ["巴蘭的曠野"]),
    ("他備拉", ["他備拉"]),
    ("基博羅哈他瓦（貪慾的墳墓）", ["基博羅哈他瓦"]),
    ("以實各谷", ["以實各"]),
    ("何珥山", ["何珥山"]),
    ("米利巴水", ["米利巴"]),
    ("摩押平原", ["摩押平原"]),
    ("巴力毘珥／什亭", ["毘珥", "什亭"]),
    ("約旦河", ["約旦河"]),
    ("逃城", ["逃城"]),
]


def chapter_files():
    out = []
    for f in sorted(BOOKDIR.glob("[0-9][0-9]-*.md")):
        n = int(f.name[:2])
        if 1 <= n <= 24:
            out.append((n, f))
    return out


def study_text(path):
    """The chapter minus its Scripture block — where the book *discusses*."""
    t = path.read_text(encoding="utf-8")
    return re.sub(r"^## 經文 \(Scripture\).*?(?=^## 背景)", "", t, flags=re.M | re.S)


def build():
    hits = {}
    for num, f in chapter_files():
        text = study_text(f)
        for label, aliases in PEOPLE + PLACES:
            if any(a in text for a in aliases):
                hits.setdefault(label, []).append(num)
    return hits


def render(hits):
    out = []
    for title, group in (("人物", PEOPLE), ("地名", PLACES)):
        out.append(f"\n**{title}**\n")
        out.append("| 名稱 | 本書討論之處 |")
        out.append("|--------------------|--------------------------------|")
        for label, _ in group:
            ch = hits.get(label)
            if not ch:
                continue
            # A name occurring in most chapters (摩西 is in 21 of 24) locates
            # nothing; a printed index says so rather than listing everything.
            if len(ch) > UBIQUITOUS:
                loc = f"全書多處（{len(ch)} 章），見目次與各章標題"
            else:
                loc = "、".join(f"第 {c} 章" for c in ch)
            out.append(f"| {label} | {loc} |")
    return "\n".join(out)


def main():
    hits = build()
    table = render(hits)
    if "--write" in sys.argv:
        text = APPENDIX.read_text(encoding="utf-8")
        a, b = text.find(START), text.find(END)
        if a < 0 or b < 0:
            sys.exit(f"markers not found in {APPENDIX}")
        new = text[:a + len(START)] + "\n" + table + "\n" + text[b:]
        if new != text:
            APPENDIX.write_text(new, encoding="utf-8")
            print(f"updated {APPENDIX.name}: {len(hits)} indexed terms")
        else:
            print(f"{APPENDIX.name} already current")
        return 0
    print(table)
    return 0


if __name__ == "__main__":
    sys.exit(main())
