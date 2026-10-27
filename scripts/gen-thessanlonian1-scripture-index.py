#!/usr/bin/env python3
"""Generate the 1 Thessalonians volume's cross-book Scripture Index from the book's own text.

WHY THIS EXISTS
---------------
Like the Romans, John, Galatians and James indices,
`books/bible/thessanlonian1/98-appendix-indices.md` must carry a table derived
from the text, not hand-curated. Copied from scripts/gen-james-scripture-index.py
(2026-10-01); unlike that script, chapter files are DISCOVERED by glob, so a
chapter added later cannot silently fall out of the index (the James script's
hard-coded range(1, 6) did exactly that when chapters 6-12 were added).

WHAT IT DOES
------------
Walks the source files in the order `scripts/build-thessanlonian1-consolidated.sh`
concatenates them, extracts every NON-1-Thessalonians scripture reference, and writes
a Markdown table (reference -> chapters of this book) between the two marker
comments in 98-appendix-indices.md. Keyed to chapters, not page numbers.

Reuses the book-name tables and reference parser of the John generator.

Usage:  python3 scripts/gen-thessanlonian1-scripture-index.py --write   # update appendix
        python3 scripts/gen-james-scripture-index.py           # print table
        python3 scripts/gen-thessanlonian1-scripture-index.py --stats
"""
import importlib.util
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKDIR = ROOT / "books" / "bible" / "thessanlonian1"
APPENDIX = BOOKDIR / "98-appendix-indices.md"
START = "<!-- gen-scripture-index:start -->"
END = "<!-- gen-scripture-index:end -->"

_spec = importlib.util.spec_from_file_location(
    "john_index", ROOT / "scripts" / "gen-john-scripture-index.py")
john = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(john)
# The John generator leaves John itself out (it is that book's own text);
# this book cites John often, so put it back and rebuild the parser.
BOOKS = list(john.BOOKS)
BOOKS.insert(next(i for i, (f, _) in enumerate(BOOKS) if f == "路加福音") + 1,
             ("約翰福音", ["約翰福音", "約"]))
ORDER = {full: i for i, (full, _) in enumerate(BOOKS)}
ALIAS = {a: full for full, aliases in BOOKS for a in aliases}
MAXCHAP = dict(john.MAXCHAP, **{"約翰福音": 21})
_SHORT = "|".join(a for a in ALIAS if len(a) == 1)
_LONG = "|".join(sorted((a for a in ALIAS if len(a) > 1), key=len, reverse=True))
REF = re.compile(
    rf"(?:(?<![{john.CJK}A-Za-z0-9])({_SHORT})|(?<![A-Za-z0-9])({_LONG}))"
    rf"\s*(\d+)(?::{john.VERSES})?(?=\s*章?)"
)

AMBIGUOUS = set("但得該拿傳歌書")
LIST_PUNCT = set("（(、；;/ ")


def refs_in(text):
    for m in REF.finditer(text):
        alias = m.group(1) or m.group(2)
        if alias in AMBIGUOUS and m.start() > 0 and text[m.start() - 1] not in LIST_PUNCT:
            continue
        chap = int(m.group(3))
        full = ALIAS[alias]
        if chap < 1 or chap > MAXCHAP[full]:
            continue
        yield full, chap, m.group(4)

# Source files in build order -> the label the index should point at.
SOURCES = [
    ("000-preface.md",                 "前言"),
    ("00-overview.md",                 "卷首·概覽"),
    ("00a-1thess-position.md",         "卷首·定位"),
    ("00c-revelation-order.md",        "卷首·骨幹"),
    ("elder-wong-systematic-study.md", "卷首·領受總綱"),
] + [(p.name, f"第{int(p.name[:2])}章")
     for p in sorted(BOOKDIR.glob("[0-9][0-9]-*.md"))
     if 1 <= int(p.name[:2]) <= 95] + [
    ("999-afterword.md",               "跋"),
]

SKIP_PREFIX = ("> ^",)          # the chapter's own Scripture block


def source_path(name):
    if name.endswith(".md"):
        return BOOKDIR / name
    hits = sorted(BOOKDIR.glob(f"{name}-*.md"))
    return hits[0] if hits else None


def build_index():
    index = defaultdict(set)
    for fname, label in SOURCES:
        p = source_path(fname)
        if p is None or not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.lstrip().startswith(SKIP_PREFIX):
                continue
            # 1 Thessalonians itself is the book; drop its own references
            cleaned = re.sub(r"帖(?:撒羅尼迦)?前(?:書)?\s*\d+(?::\d+(?:[-–,，]\d+)*)?", "", line)
            # Its single-character aliases refuse a preceding CJK character
            # (so 「雅各書1:22」 is not read as 書=Joshua); this book's prose
            # often writes 「見於徒9:15」, so open a gap after such particles.
            cleaned = re.sub(r"([於見與和及參照即對到如])(?=[創出利民申士詩箴賽耶結但何珥摩彌哈番該亞瑪太可路約徒羅加弗腓西來雅猶啟]\s*\d+:)", r"\1 ", cleaned)
            for full, chap, _verses in refs_in(cleaned):
                index[(full, chap)].add(label)
    return index


def render(index):
    label_order = {lbl: i for i, (_, lbl) in enumerate(SOURCES)}
    keys = sorted(index, key=lambda k: (ORDER.get(k[0], 999), k[1]))
    # Separator row must be >= pandoc's --columns default (72) or the table
    # compiles to non-wrapping `lll` columns instead of wrapping `p{}` ones —
    # see .claude/skills/eat-bible/references/gotchas.md, "Overfull \hbox" entry.
    # Column ratio skewed toward the second column: the 本書討論之處 cell can
    # carry four-item lists ("卷首·概覽、卷首·定位、卷首·領受總綱、第5章") while
    # 經文 entries are always short ("馬太福音 5") — an even split left the long
    # lists overfull by ~32pt even after the row passed the 72-char threshold.
    out = ["| 經文 | 本書討論之處 |",
           "|--------------------------|------------------------------------------------------------------------------|"]
    for full, chap in keys:
        labels = sorted(index[(full, chap)], key=lambda l: label_order.get(l, 999))
        out.append(f"| {full} {chap} | {'、'.join(labels)} |")
    return "\n".join(out)


def main():
    index = build_index()
    keys = sorted(index, key=lambda k: (ORDER.get(k[0], 999), k[1]))
    if "--stats" in sys.argv:
        books = {k[0] for k in keys}
        print(f"{len(keys)} distinct book-chapters, across {len(books)} books; "
              f"OT {sum(1 for k in keys if ORDER[k[0]] < 39)}, "
              f"NT {sum(1 for k in keys if ORDER[k[0]] >= 39)}")
        return 0
    table = render(index)
    if "--write" in sys.argv:
        text = APPENDIX.read_text(encoding="utf-8")
        a, b = text.find(START), text.find(END)
        if a < 0 or b < 0:
            sys.exit(f"markers not found in {APPENDIX}")
        new = text[:a + len(START)] + "\n" + table + "\n" + text[b:]
        if new != text:
            APPENDIX.write_text(new, encoding="utf-8")
            print(f"updated {APPENDIX.name}: {len(keys)} rows")
        else:
            print(f"{APPENDIX.name} already current: {len(keys)} rows")
        return 0
    print(table)
    return 0


if __name__ == "__main__":
    sys.exit(main())
