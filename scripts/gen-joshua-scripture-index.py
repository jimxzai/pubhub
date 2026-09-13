#!/usr/bin/env python3
"""Generate the Joshua volume's cross-book Scripture Index from the book's own text.

WHY THIS EXISTS
---------------
Same rationale as scripts/gen-job-scripture-index.py and
scripts/gen-john-scripture-index.py: a hand-curated cross-book index drifts out
of sync with the actual chapter text. This walks the real chapter files and
derives the table instead. The house rubric's row 9 (讀者可用性) asks for indices
that are generated, not hand-kept.

WHAT IT DOES
------------
Walks the source files in the order scripts/build-joshua-consolidated.sh
concatenates them, extracts every NON-Joshua scripture reference, and writes a
Markdown table (reference -> chapters of this book) between the two marker
comments in 98-appendix-indices.md. Keyed to chapters, not page numbers.

Reuses the book-name tables and reference parser of the John generator.

Usage:  python3 scripts/gen-joshua-scripture-index.py --write   # update appendix
        python3 scripts/gen-joshua-scripture-index.py           # print table
        python3 scripts/gen-joshua-scripture-index.py --stats
"""
import importlib.util
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKDIR = ROOT / "books" / "bible" / "joshua"
APPENDIX = BOOKDIR / "98-appendix-indices.md"
START = "<!-- gen-scripture-index:start -->"
END = "<!-- gen-scripture-index:end -->"

_spec = importlib.util.spec_from_file_location(
    "john_index", ROOT / "scripts" / "gen-john-scripture-index.py")
john = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(john)
ORDER, REF, ALIAS, MAXCHAP = john.ORDER, john.REF, john.ALIAS, john.MAXCHAP

# Joshua's own abbreviation 書 is the tail character of many other book names
# (但以理書, 以賽亞書, 傳道書 …), so it is only ever a Joshua reference when it
# is NOT preceded by another CJK character — the same guard the Job generator
# uses for 伯. Bare chapter:verse ("21:45") carries no book name and so is
# already ignored by REF.
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
    ("00a-joshua-position.md",         "卷首·定位"),
    ("00b-conquest-spine.md",          "卷首·骨幹"),
    ("00c-revelation-order.md",        "卷首·啟示的次序"),
    ("elder-wong-systematic-study.md", "卷首·領受總綱"),
] + [(f"{i:02d}", f"第{i}章") for i in range(1, 21)] + [
    ("99-covenant-and-legacy.md",      "卷末"),
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
            # Joshua is the book itself; drop explicit self-references
            # ("書 1:9", "約書亞記 21:45") before parsing cross-book hits.
            cleaned = re.sub(r"(?<![一-鿿])(?:約書亞記|書)\s*\d+(?::\d+(?:[-–]\d+)?)?", "", line)
            for full, chap, _verses in refs_in(cleaned):
                index[(full, chap)].add(label)
    return index


def render(index):
    label_order = {lbl: i for i, (_, lbl) in enumerate(SOURCES)}
    keys = sorted(index, key=lambda k: (ORDER.get(k[0], 999), k[1]))
    # separator width is load-bearing: a short separator row compiles to bare
    # `l` columns that cannot wrap. See references/gotchas.md.
    out = ["| 經文 | 本書討論之處 |",
           "|--------------------------|----------------------------------------------------------|"]
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
