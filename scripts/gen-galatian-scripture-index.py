#!/usr/bin/env python3
"""Generate the Galatians volume's cross-book Scripture Index from the book's own text.

WHY THIS EXISTS
---------------
Like the Romans and John indices, `books/bible/galatian/98-appendix-indices.md`
must carry a table derived from the text, not hand-curated. See
scripts/gen-romans-scripture-index.py, which this mirrors closely.

WHAT IT DOES
------------
Walks the source files in the order `scripts/build-galatian-consolidated.sh`
concatenates them, extracts every NON-Galatians scripture reference, and writes
a Markdown table (reference -> chapters of this book) between the two marker
comments in 98-appendix-indices.md. Keyed to chapters, not page numbers.

Reuses the book-name tables and reference parser of the John generator.

Usage:  python3 scripts/gen-galatian-scripture-index.py --write   # update appendix
        python3 scripts/gen-galatian-scripture-index.py           # print table
        python3 scripts/gen-galatian-scripture-index.py --stats
"""
import importlib.util
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKDIR = ROOT / "books" / "bible" / "galatian"
APPENDIX = BOOKDIR / "98-appendix-indices.md"
START = "<!-- gen-scripture-index:start -->"
END = "<!-- gen-scripture-index:end -->"

_spec = importlib.util.spec_from_file_location(
    "john_index", ROOT / "scripts" / "gen-john-scripture-index.py")
john = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(john)
ORDER, REF, ALIAS, MAXCHAP = john.ORDER, john.REF, john.ALIAS, john.MAXCHAP

# Galatians' own alias is the single character 加 — extremely common in
# ordinary prose (加添, 加上, 更加...), but REF only matches when it is
# immediately followed by "N:N", so false positives from prose are not a
# real risk. The genuine risk is the OPPOSITE: 路加 (Luke, person or book)
# ends in 加, so the self-citation stripper below must not eat a real
# 路加N:N reference — the lookbehind excludes any 加 preceded by a CJK
# character, which 路加's 加 always is.
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
    ("00a-galatians-position.md",      "卷首·定位"),
    ("00c-gospel-spine.md",            "卷首·骨幹"),
    ("elder-wong-systematic-study.md", "卷首·領受總綱"),
] + [(f"{i:02d}", f"第{i}章") for i in range(1, 9)] + [
    ("99-closing.md",                  "卷末"),
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
            # Galatians itself is the book; drop its own references before parsing.
            # Two passes, because the ambiguity differs by alias length:
            #  - the full name "加拉太書" is unambiguous (4 chars, never means
            #    anything else), so strip it regardless of what precedes it —
            #    the earlier CJK-lookbehind-only version missed almost every
            #    real occurrence, since "加拉太書" in running prose is nearly
            #    always preceded by another CJK character (呼應加拉太書1:4的...),
            #    which is exactly what the lookbehind was written to exclude.
            #    Confirmed: this book alone carries 40+ such mid-sentence
            #    occurrences, none previously stripped, all leaking into the
            #    cross-book index as if they cited another book's Galatians.
            #  - the bare one-character alias "加" only gets the lookbehind
            #    protection (against eating 路加's 加), same as before.
            cleaned = re.sub(r"加拉太書\s*\d+(?::\d+(?:[-–]\d+)?)?", "", line)
            cleaned = re.sub(r"(?<![一-鿿])加\s*\d+(?::\d+(?:[-–]\d+)?)?", "", cleaned)
            for full, chap, _verses in refs_in(cleaned):
                index[(full, chap)].add(label)
    return index


def render(index):
    label_order = {lbl: i for i, (_, lbl) in enumerate(SOURCES)}
    keys = sorted(index, key=lambda k: (ORDER.get(k[0], 999), k[1]))
    out = ["| 經文 | 本書討論之處 |", "|--------------------|--------------------------------|"]
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
