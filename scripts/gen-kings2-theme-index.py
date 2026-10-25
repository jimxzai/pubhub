#!/usr/bin/env python3
"""Generate the 2 Kings volume's subject (theme) index from the book's own text.

WHY THIS EXISTS
---------------
`98-appendix-indices.md` is titled 「附錄：經文與主題索引 (Appendix: Scripture
& Theme Indices)」 and shipped with two Scripture indices and no theme index
at all — the same gap gen-job-theme-index.py fixed for the Job volume. A
287-page study volume with no subject index leaves a reader who remembers the
book said something about 不離開 or 耶戶 with no way back to it.

Same rationale as gen-kings2-scripture-index.py: a hand-kept index drifts out
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

Usage:  python3 scripts/gen-kings2-theme-index.py --write   # update appendix
        python3 scripts/gen-kings2-theme-index.py           # print table
"""
import argparse
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "bible" / "kings2"
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
    ("話與先知", [
        ("照……的話（成就公式）", ["所說的話", "照著", "應驗"]),
        ("神人", ["神人"]),
        ("以利亞", ["以利亞"]),
        ("以利沙", ["以利沙"]),
        ("先知", ["先知"]),
        ("律法書", ["律法書"]),
    ]),
    ("緊貼與不離開", [
        ("不離開", ["不離開", "總不離開"]),
        ("耶羅波安的罪", ["耶羅波安的罪", "耶羅波安所犯", "耶羅波安使"]),
        ("金牛犢", ["金牛犢"]),
        ("邱壇", ["邱壇"]),
        ("巴力", ["巴力"]),
        ("專靠", ["專靠", "倚靠"]),
    ]),
    ("王與國", [
        ("撒瑪利亞", ["撒瑪利亞"]),
        ("耶路撒冷", ["耶路撒冷"]),
        ("亞述", ["亞述"]),
        ("巴比倫", ["巴比倫"]),
        ("亞蘭", ["亞蘭"]),
        ("被擄", ["被擄", "擄去"]),
        ("大衛的燈", ["燈光", "大衛的燈", "那盞燈"]),
    ]),
    ("審判與憐憫", [
        ("審判", ["審判"]),
        ("憐憫", ["憐憫", "憐恤"]),
        ("悔改", ["悔改"]),
        ("禱告", ["禱告"]),
        ("逾越節", ["逾越節"]),
        ("立約", ["立約", "亞伯拉罕的約"]),
    ]),
    ("神蹟與醫治", [
        ("復活", ["復活", "活過來"]),
        ("大痲瘋", ["大痲瘋", "痲瘋"]),
        ("饑荒", ["饑荒"]),
        ("火", ["火車火馬", "火從天"]),
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


CT_START = "<!-- gen-chapter-table:start -->"
CT_END = "<!-- gen-chapter-table:end -->"


def chapter_table():
    import json
    meta = json.loads((BOOK / ".sources" / "chapters.json").read_text(encoding="utf-8"))
    rows = ["| 經文 | 章 | 標題 |", "|----------------------------------|-----------------------|-----------------------|"]
    for key, m in meta.items():
        rows.append(f"| {m['ref'].replace('列王紀下 ', '')} | {int(key):02d} | {m['zh']} ({m['en']}) |")
    return "\n".join(rows) + "\n"


def replace_block(text, start, end, body):
    if start not in text or end not in text:
        sys.exit(f"markers {start} / {end} not found in {APPENDIX}")
    pre, rest = text.split(start, 1)
    _old, post = rest.split(end, 1)
    return pre + start + "\n" + body + end + post


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    table = render(build_rows())
    if not args.write:
        print(table)
        return 0
    text = APPENDIX.read_text(encoding="utf-8")
    new = replace_block(text, START, END, table)
    new = replace_block(new, CT_START, CT_END, chapter_table())
    if new == text:
        print("theme index already current")
        return 0
    APPENDIX.write_text(new, encoding="utf-8")
    print(f"theme index written: {sum(len(r) for _, r in build_rows())} entries")
    return 0


if __name__ == "__main__":
    sys.exit(main())
