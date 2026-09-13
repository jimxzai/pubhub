#!/usr/bin/env python3
"""Generate the Proverbs volume's subject (theme) index from the book's own text.

WHY THIS EXISTS
---------------
Same rationale as scripts/gen-job-theme-index.py: a hand-kept index drifts out
of sync with the chapters. This derives the table from the chapter files
instead of trusting a hand-curated list.

WHAT IT DOES
------------
For each term in the controlled vocabulary below, counts occurrences per
chapter and lists the chapters where the term is actually DISCUSSED, not
merely mentioned. Two rules make the difference between an index and a
concordance:

  1. A term must clear a per-term threshold in a chapter to earn a
     reference: max(MIN_HITS, 10% of that term's busiest chapter).
  2. An entry is capped at MAX_REFS chapters, keeping the densest ones.
     Proverbs repeats core terms (智慧, 愚昧, 耶和華) across nearly every
     chapter; an entry pointing at all 31 would tell a reader nothing.
     Selection is by density; DISPLAY is in chapter order.

Variants are load-bearing, not convenience: the book uses 愚昧人／愚妄人／
愚蒙人 for roughly the same figure, and 賙濟／賙貧／施捨 for the same act of
generosity — indexing only one spelling misses real occurrences of the theme.

The vocabulary is deliberately hand-chosen and deliberately small. A
frequency dump would be a concordance, not an index — choosing which
concepts a reader will look up is editorial work a script cannot do. What
the script does is guarantee the page references are true and stay true.

Usage:  python3 scripts/gen-proverb-theme-index.py --write   # update appendix
        python3 scripts/gen-proverb-theme-index.py           # print table
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "bible" / "proverb"
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
    ("智慧位格化與根基", [
        ("敬畏耶和華", ["敬畏耶和華", "敬畏主", "敬畏神"]),
        ("智慧的呼喚", ["呼喊", "呼叫"]),
        ("智慧與神同在", ["創造之先", "與神同在", "被立"]),
        ("兩條路", ["兩條路", "義人的路", "惡人的道"]),
    ]),
    ("智慧與愚昧", [
        ("智慧人", ["智慧人", "智慧之子"]),
        ("愚昧人", ["愚昧人", "愚妄人", "愚蒙人"]),
        ("褻慢人", ["褻慢人", "褻慢"]),
        ("懶惰人", ["懶惰人", "懶惰"]),
        ("謹慎人／精明人", ["謹慎人", "精明人"]),
    ]),
    ("言語與人際", [
        ("言語的權柄", ["舌頭", "口舌"]),
        ("柔和的回答", ["柔和的回答", "柔和的舌頭"]),
        ("傳舌與爭競", ["傳舌", "爭競", "爭端"]),
        ("朋友與鄰舍", ["朋友", "鄰舍"]),
        ("真話與謊言", ["真話", "謊言", "詭詐"]),
    ]),
    ("財富、公道與治理", [
        ("財富與貧窮", ["財富", "貧窮", "富足"]),
        ("公道的天平", ["天平", "法碼", "度量衡"]),
        ("賙濟與慷慨", ["賙濟", "賙貧", "施捨"]),
        ("君王與治理", ["君王", "王的心"]),
        ("神的主權", ["耶和華指引", "隨意流轉", "主權"]),
    ]),
    ("家庭與教養", [
        ("管教兒女", ["管教", "杖打"]),
        ("智慧建造家室", ["建立家室", "拆毀"]),
        ("淫婦與情慾的警戒", ["淫婦", "淫亂", "外女"]),
        ("才德的婦人", ["才德的婦人", "敬畏耶和華的婦女"]),
    ]),
    ("書中的人物", [
        ("亞古珥", ["亞古珥"]),
        ("利慕伊勒", ["利慕伊勒"]),
        ("智慧（位格化）", ["智慧在街市", "智慧站在"]),
        ("愚昧的婦人", ["愚昧的婦人"]),
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
