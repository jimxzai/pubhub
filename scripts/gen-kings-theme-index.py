#!/usr/bin/env python3
"""Generate the 1 Kings volume's subject (theme) index from the book's own text.

WHY THIS EXISTS
---------------
`98-appendix-indices.md` is titled 「附錄：經文與主題索引 (Appendix: Scripture
& Theme Indices)」 and shipped with two Scripture indices and no theme index
at all — the same gap gen-job-theme-index.py fixed for the Job volume. A
287-page study volume with no subject index leaves a reader who remembers the
book said something about 循環公式 or 拿細耳人 with no way back to it.

Same rationale as gen-kings-scripture-index.py: a hand-kept index drifts out
of sync with the chapters. This derives the table from the chapter files.

WHAT IT DOES
------------
For each term in the controlled vocabulary below, counts occurrences per
chapter and lists the chapters where the term is actually DISCUSSED, not
merely mentioned:

  1. A term must clear a per-term threshold in a chapter to earn a
     reference: max(MIN_HITS, 10% of that term's busiest chapter).
  2. An entry is capped at MAX_REFS chapters, keeping the densest ones,
     displayed in chapter order.

The vocabulary is deliberately hand-chosen and deliberately small — choosing
which concepts a reader will look up is editorial work a script cannot do.
What the script guarantees is that the page references are true and stay true.

Usage:  python3 scripts/gen-kings-theme-index.py --write   # update appendix
        python3 scripts/gen-kings-theme-index.py           # print table
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "bible" / "kings"
APPENDIX = BOOK / "98-appendix-indices.md"
START = "<!-- gen-theme-index:start -->"
END = "<!-- gen-theme-index:end -->"

MIN_HITS = 2      # floor: occurrences in one chapter before it earns a reference
REL_HITS = 0.10   # and at least this fraction of the term's busiest chapter
MAX_REFS = 6      # an entry pointing at more chapters than this is not useful
MIN_TOTAL = 8     # book-wide occurrences before a term is worth an entry

# Controlled vocabulary, grouped as a reader would look things up.
# (display term, [search variants])
VOCAB = [
    ("燈與約", [
        ("大衛的燈", ["燈光", "燈"]),
        ("為大衛的緣故", ["大衛的緣故"]),
        ("條件句（若）", ["你若", "倘若"]),
        ("永遠", ["永遠"]),
    ]),
    ("王與心", [
        ("能聽的心", ["聽的心"]),
        ("心偏離", ["偏離", "誘惑"]),
        ("誠實的心", ["誠實的心", "專一"]),
        ("只是（raq）", ["只是", "raq"]),
        ("埃及", ["埃及"]),
    ]),
    ("殿與同在", [
        ("聖殿", ["聖殿"]),
        ("榮耀", ["榮耀"]),
        ("邱壇", ["邱壇"]),
        ("禱告", ["禱告"]),
        ("名", ["我的名", "他的名", "你的名"]),
    ]),
    ("話與先知", [
        ("耶和華的話", ["耶和華的話", "耶和華所說的話"]),
        ("先知", ["先知"]),
        ("神人", ["神人"]),
        ("應驗", ["應驗"]),
        ("微小的聲音", ["微小的聲音"]),
    ]),
    ("王國分裂", [
        ("軛與徭役", ["軛", "徭役"]),
        ("金牛犢", ["金牛犢"]),
        ("耶羅波安", ["耶羅波安"]),
        ("羅波安", ["羅波安"]),
        ("王朝更迭", ["王朝"]),
    ]),
    ("以利亞與亞哈", [
        ("以利亞", ["以利亞"]),
        ("亞哈", ["亞哈"]),
        ("耶洗別", ["耶洗別"]),
        ("巴力", ["巴力"]),
        ("拿伯", ["拿伯"]),
        ("米該雅", ["米該雅"]),
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
