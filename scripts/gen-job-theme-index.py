#!/usr/bin/env python3
"""Generate the Job volume's subject (theme) index from the book's own text.

WHY THIS EXISTS
---------------
`98-appendix-indices.md` is titled 「經文與主題索引 (Scripture & Theme Indices)」
and shipped with two Scripture indices and no theme index at all. A 363-page
study volume with no subject index is the gap a reader hits first: they
remember the book said something about the 中保 and have no way back to it.

Same rationale as gen-job-scripture-index.py — a hand-kept index drifts out of
sync with the chapters. This derives the table from the chapter files.

WHAT IT DOES
------------
For each term in the controlled vocabulary below, counts occurrences per
chapter and lists the chapters where the term is actually DISCUSSED, not
merely mentioned. Two rules make the difference between an index and a
concordance:

  1. A term must clear a per-term threshold in a chapter to earn a
     reference: max(MIN_HITS, 10% of that term's busiest chapter). A flat
     floor is not enough. 「以利戶」 runs 22-28 hits in the three Elihu
     chapters and exactly 2 in two chapters that merely cross-reference him;
     a flat floor of 2 files those two alongside the real ones. Scaling to
     the term's own distribution keeps the entry pointing where the subject
     is actually treated.
  2. An entry is capped at MAX_REFS chapters, keeping the densest ones.
     「基督」 occurs in 32 of 35 files; an index entry pointing at 32 chapters
     tells a reader nothing. Selection is by density; DISPLAY is in chapter
     order, the way a reader expects to scan it.

Variants are load-bearing, not convenience. The book calls the two tests
考驗 in chapter 2, 試探 in chapter 3 and 試煉 in chapter 18; indexing only
試煉 produced an entry that pointed a reader at chapter 18 and away from the
two chapters that narrate the tests. An index built on one spelling of a
concept is worse than no index, because it looks authoritative.

The vocabulary is deliberately hand-chosen and deliberately small. A frequency
dump would be a concordance, not an index — choosing which concepts a reader
will look up is editorial work a script cannot do. What the script does is
guarantee the page references are true and stay true.

Usage:  python3 scripts/gen-job-theme-index.py --write   # update appendix
        python3 scripts/gen-job-theme-index.py           # print table
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "bible" / "job"
APPENDIX = BOOK / "98-appendix-indices.md"
START = "<!-- gen-theme-index:start -->"
END = "<!-- gen-theme-index:end -->"

MIN_HITS = 2      # floor: occurrences in one chapter before it earns a reference
REL_HITS = 0.10   # and at least this fraction of the term's busiest chapter
MAX_REFS = 6      # an entry pointing at more chapters than this is not useful
MIN_TOTAL = 8     # book-wide occurrences before a term is worth an entry

# Controlled vocabulary, grouped as a reader would look things up.
# (display term, [search variants]) — variants let one entry gather the
# spellings the book actually uses without inventing a synonym it never uses.
VOCAB = [
    ("神與祂的作為", [
        ("神的主權", ["主權"]),
        ("創造", ["創造"]),
        ("公義", ["公義"]),
        ("神的沉默", ["沉默"]),
        ("旋風", ["旋風"]),
        ("神的問話", ["問句", "發問"]),
    ]),
    ("苦難與報應", [
        ("苦難", ["苦難"]),
        ("試煉／試探", ["試煉", "試探", "試驗", "考驗"]),
        ("報應神學", ["報應"]),
        ("無辜受苦", ["無辜"]),
        ("哀歌", ["哀歌"]),
        ("咒詛", ["咒詛"]),
        ("忍耐", ["忍耐"]),
        ("安慰", ["安慰"]),
    ]),
    ("約伯所求的三樣", [
        ("中保", ["中保"]),
        ("聽訟的人", ["聽訟"]),
        ("救贖主 (go'el)", ["救贖主"]),
        ("代求", ["代求"]),
    ]),
    ("書中的人物", [
        ("撒但", ["撒但"]),
        ("三友", ["三友", "三個朋友"]),
        ("以利戶", ["以利戶"]),
        ("河馬 (behemoth)", ["河馬"]),
        ("鱷魚 (leviathan)", ["鱷魚"]),
    ]),
    ("敬虔與生命", [
        ("敬畏神", ["敬畏"]),
        ("敬虔", ["敬虔"]),
        ("完全正直", ["完全正直"]),
        ("信心", ["信心"]),
        ("盼望", ["盼望"]),
        ("悔改", ["悔改"]),
        ("恩典", ["恩典"]),
        ("申辯與控訴", ["申辯", "控訴"]),
    ]),
    ("智慧與結局", [
        ("智慧", ["智慧"]),
        ("風聞與親眼看見", ["風聞"]),
        ("塵土與爐灰", ["塵土", "爐灰"]),
        ("復原與加倍", ["加倍", "復原"]),
        ("復活的盼望", ["復活"]),
    ]),
    ("讀法與立場", [
        ("預表的界線", ["預表"]),
        ("十字架", ["十字架"]),
        ("律法之前", ["律法"]),
    ]),
]

CHAPTER_RE = re.compile(r"^(\d\d)-")


def chapter_files():
    out = []
    for p in sorted(BOOK.glob("*.md")):
        m = CHAPTER_RE.match(p.name)
        if m and not p.name.startswith(("98-", "99-", "00-")):
            out.append((int(m.group(1)), p))
    return out


def build_rows():
    files = [(n, p, p.read_text(encoding="utf-8")) for n, p in chapter_files()]
    sections = []
    for heading, terms in VOCAB:
        rows = []
        for display, variants in terms:
            counts = [(n, sum(text.count(v) for v in variants))
                      for n, _p, text in files]
            total = sum(c for _n, c in counts)
            peak = max((c for _n, c in counts), default=0)
            floor = max(MIN_HITS, -(-peak * 10 // 100))   # ceil(REL_HITS*peak)
            hits = [(n, c) for n, c in counts if c >= floor]
            if total < MIN_TOTAL or not hits:
                continue
            # select by density, display in chapter order
            keep = sorted(sorted(hits, key=lambda t: -t[1])[:MAX_REFS])
            refs = "、".join(f"第{n}章" for n, _ in keep)
            if len(hits) > len(keep):
                refs += " 等"
            rows.append((display, refs))
        if rows:
            sections.append((heading, rows))
    return sections


def render(sections):
    out = []
    for heading, rows in sections:
        out.append(f"\n**{heading}**\n")
        out.append("| 主題 | 集中討論之處 |")
        # A separator row shorter than pandoc's --columns threshold (72)
        # compiles to bare `l` columns: the table takes its natural width,
        # cannot wrap, and a long row of chapter references runs off the
        # text block with no warning. Keep this at or past the threshold.
        out.append("|--------------------------|----------------------------------------------------------|")
        for display, refs in rows:
            out.append(f"| {display} | {refs} |")
    return "\n".join(out) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    table = render(build_rows())
    if not args.write:
        print(table)
        return 0
    text = APPENDIX.read_text(encoding="utf-8")
    if START not in text or END not in text:
        sys.exit(f"markers {START} / {END} not found in {APPENDIX}")
    pre, rest = text.split(START, 1)
    _old, post = rest.split(END, 1)
    new = pre + START + "\n" + table + END + post
    if new == text:
        print("theme index already current")
        return 0
    APPENDIX.write_text(new, encoding="utf-8")
    print(f"theme index written: {sum(len(r) for _, r in build_rows())} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
