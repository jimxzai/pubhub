#!/usr/bin/env python3
"""Generate the James volume's cross-book Scripture Index from the book's own text.

WHY THIS EXISTS
---------------
Like the Romans, John and Galatians indices, `books/bible/james/98-appendix-indices.md`
must carry a table derived from the text, not hand-curated. See
scripts/gen-galatian-scripture-index.py, which this mirrors closely.

WHAT IT DOES
------------
Walks the source files in the order `scripts/build-james-consolidated.sh`
concatenates them, extracts every NON-James scripture reference, and writes
a Markdown table (reference -> chapters of this book) between the two marker
comments in 98-appendix-indices.md. Keyed to chapters, not page numbers.

Reuses the book-name tables and reference parser of the John generator.

Usage:  python3 scripts/gen-james-scripture-index.py --write   # update appendix
        python3 scripts/gen-james-scripture-index.py           # print table
        python3 scripts/gen-james-scripture-index.py --stats
"""
import importlib.util
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKDIR = ROOT / "books" / "bible" / "james"
APPENDIX = BOOKDIR / "98-appendix-indices.md"
START = "<!-- gen-scripture-index:start -->"
END = "<!-- gen-scripture-index:end -->"

_spec = importlib.util.spec_from_file_location(
    "john_index", ROOT / "scripts" / "gen-john-scripture-index.py")
john = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(john)
ORDER, REF, ALIAS, MAXCHAP = john.ORDER, john.REF, john.ALIAS, john.MAXCHAP

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
    ("00a-james-position.md",          "卷首·定位"),
    ("00c-revelation-order.md",        "卷首·骨幹"),
    ("elder-wong-systematic-study.md", "卷首·領受總綱"),
] + [(f"{i:02d}", f"第{i}章") for i in range(1, 6)] + [
    ("06-james-and-proverbs.md",       "專題·與箴言"),
    ("07-elijah-and-prayer.md",        "專題·以利亞與禱告"),
    ("08-james-and-1peter.md",         "專題·與彼得前書"),
    ("09-james-and-leviticus19.md",    "專題·與利未記19章"),
    ("10-james-and-amos.md",           "專題·與阿摩司書"),
    ("11-james-and-psalm1.md",         "專題·與詩篇1篇"),
    ("12-james-and-ecclesiastes.md",   "專題·與傳道書"),
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
            # James itself is the book; drop its own references before parsing
            cleaned = re.sub(r"(?<![一-鿿])雅(?:各書)?\s*\d+(?::\d+(?:[-–]\d+)?)?", "", line)
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
