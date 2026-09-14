#!/usr/bin/env python3
"""Generate the Ephesians volume's subject (theme) index from the book's own text.

Same rationale as scripts/gen-job-theme-index.py: a hand-kept index drifts out
of sync with the chapters. This derives the table from the 11 chapter files
instead, using a controlled vocabulary grouped the way a reader would look
things up, with a per-term density threshold so an entry points at where a
subject is actually discussed, not everywhere it is merely mentioned.

Usage:  python3 scripts/gen-ephesians-theme-index.py --write
        python3 scripts/gen-ephesians-theme-index.py
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "bible" / "ephisian"
APPENDIX = BOOK / "98-appendix-indices.md"
START = "<!-- gen-theme-index:start -->"
END = "<!-- gen-theme-index:end -->"

MIN_HITS = 2
REL_HITS = 0.10
MAX_REFS = 6
MIN_TOTAL = 4

VOCAB = [
    ("在基督裏與神的計劃", [
        ("在基督裏", ["在基督裏", "在他裏面", "在祂裏面"]),
        ("揀選、預定", ["揀選", "預定"]),
        ("同歸於一", ["同歸於一"]),
        ("奧秘", ["奧秘", "奧祕"]),
        ("恩典", ["恩典"]),
    ]),
    ("教會論", [
        ("教會是基督的身體", ["身體"]),
        ("一個新人／猶太外邦合一", ["一個新人", "外邦人"]),
        ("教會是聖殿", ["聖殿", "居所"]),
        ("合一", ["合一"]),
        ("恩賜與職事", ["恩賜"]),
    ]),
    ("基督徒的行為", [
        ("坐、行、站", ["坐", "行事為人", "站立"]),
        ("脫舊穿新", ["舊人", "穿上新人"]),
        ("光明中的行事", ["光明"]),
        ("被聖靈充滿", ["充滿"]),
        ("家庭的次序", ["順服", "妻子", "丈夫"]),
        ("屬靈爭戰、全副軍裝", ["軍裝", "爭戰", "抵擋"]),
    ]),
    ("啟示的次序", [
        ("在天上", ["天上", "天空屬靈氣"]),
        ("三一神的工作", ["三一神", "父、子、靈"]),
        ("藉教會顯給天使看", ["執政的", "掌權的", "天使"]),
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
            refs = "、".join(f"第{n:02d}章" for n, _ in keep)
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
    sections = build_rows()
    table = render(sections)
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
    print(f"theme index written: {sum(len(r) for _, r in sections)} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
