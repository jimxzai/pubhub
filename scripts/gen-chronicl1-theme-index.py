#!/usr/bin/env python3
"""Generate the 1 Chronicles volume's subject (theme) index from the book's own text.

Same rationale as gen-job-theme-index.py — a hand-kept index drifts out of
sync with the chapters. This derives the table from the chapter files.

Usage:  python3 scripts/gen-chronicl1-theme-index.py --write
        python3 scripts/gen-chronicl1-theme-index.py
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "bible" / "chronicl1"
APPENDIX = BOOK / "98-appendix-indices.md"
START = "<!-- gen-theme-index:start -->"
END = "<!-- gen-theme-index:end -->"

MIN_HITS = 2
REL_HITS = 0.10
MAX_REFS = 6
MIN_TOTAL = 8

VOCAB = [
    ("家譜與名字", [
        ("家譜", ["家譜"]),
        ("按家譜計算", ["按家譜", "按著家譜"]),
        ("名字被記念", ["記念", "記下他們的名字", "記錄他們的名字"]),
        ("被擄與歸回", ["被擄", "歸回"]),
    ]),
    ("約與應許", [
        ("大衛之約", ["大衛之約"]),
        ("永遠的家／國／寶座", ["直到永遠"]),
        ("求問耶和華", ["求問"]),
        ("預備", ["預備"]),
    ]),
    ("敬拜與聖殿", [
        ("約櫃", ["約櫃"]),
        ("聖殿／殿宇", ["聖殿", "殿宇"]),
        ("祭司班次", ["班次", "掣籤"]),
        ("利未人", ["利未人"]),
        ("歌唱者與音樂", ["歌唱", "詩班", "頌讚"]),
        ("守門者", ["守門"]),
        ("分別為聖", ["分別為聖"]),
    ]),
    ("君王與國度", [
        ("掃羅", ["掃羅"]),
        ("大衛", ["大衛"]),
        ("所羅門", ["所羅門"]),
        ("一心／合一", ["一心"]),
        ("勇士", ["勇士"]),
    ]),
    ("讀法與立場", [
        ("預表", ["預表"]),
        ("彌賽亞", ["彌賽亞"]),
        ("基督焦點", ["基督"]),
        ("十字架", ["十字架"]),
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
            floor = max(MIN_HITS, -(-peak * 10 // 100))
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
