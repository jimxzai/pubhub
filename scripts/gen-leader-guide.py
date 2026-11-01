#!/usr/bin/env python3
"""Generate leader guides and student handouts from a book's chapters (roadmap items 5.1 and 5.2).

Nothing here is written by the generator: every question, verse and prayer is lifted from the chapter.
The generator only fixes the order and the time blocks.

    python3 scripts/gen-leader-guide.py books/bible/gospel-of-john [--out docs/leader-guides]

For each chapter it writes <out>/<book>/<chapter>.md with
  * a 60-minute and a 90-minute plan for the leader (questions in the chapter's own order, ladder first)
  * the chapter's 提問式對話 ladder, 默想問題, 禱告回應 and closing line for the leader
  * a handout section for students: passage, key word and the same questions with NO commentary or answers
"""
import argparse
import re
import sys
from pathlib import Path

PLAN = {  # minutes per block; 60 and 90 minute versions
    60: [("開場禱告與讀經", 10), ("看見基督：焦點與鑰詞", 10), ("提問式對話（階梯）", 20), ("默想問題分享", 15), ("禱告回應與結束", 5)],
    90: [("開場禱告與讀經", 10), ("看見基督：焦點與鑰詞", 15), ("背景與原文（選讀）", 15),
         ("提問式對話（階梯）", 25), ("默想問題分享", 20), ("禱告回應與結束", 5)],
}


def section(text, heading):
    m = re.search(rf"^#{{2,3}} {re.escape(heading)}[^\n]*\n(.*?)(?=^#{{2,3}} |^---\s*$|\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def bullets(block):
    return [re.sub(r"^[-*]\s+", "", l).strip() for l in block.splitlines() if re.match(r"^[-*]\s+", l)]


def numbered(block):
    items, cur = [], None
    for l in block.splitlines():
        if re.match(r"^\d+\.\s+", l):
            cur = re.sub(r"^\d+\.\s+", "", l).strip()
            items.append(cur)
        elif cur is not None and l.strip() and not l.startswith("#"):
            items[-1] += " " + l.strip()
    return items


def prayer(block):
    return "\n".join(l.lstrip("> ").rstrip(" \\").rstrip() for l in block.splitlines() if l.startswith(">"))


def build(ch):
    t = ch.read_text(encoding="utf-8")
    title = next((l[2:].strip() for l in t.splitlines() if l.startswith("# ")), ch.name)
    lines = t.splitlines()
    h1 = next((i for i, l in enumerate(lines) if l.startswith("# ")), 0)
    passage = next((l.strip() for l in lines[h1 + 1:h1 + 6] if re.search(r"\d+[:：]\d+", l) and not l.startswith(("**", ">"))), "")
    focus_block = section(t, "基督焦點")
    key = next((l.lstrip("> ").rstrip(" \\").replace("**", "") for l in focus_block.splitlines() if "鑰詞" in l), "")
    focus = next((p for p in focus_block.split("\n\n") if p.strip() and not p.lstrip().startswith(">")), "").strip()
    ladder = bullets(section(t, "提問式對話"))
    meditate = numbered(section(t, "默想問題"))
    pr = prayer(section(t, "禱告回應"))
    closing = next((p.strip() for p in reversed(t.split("\n\n"))
                    if "你看見耶穌了嗎" in p and not p.lstrip().startswith((">", "#", "|", "- "))), "")
    if not (ladder or meditate):
        return title, None
    o = [f"# 帶領者指引：{title}", "", f"經文：{passage or '（見章首）'}", ""]
    for mins, blocks in PLAN.items():
        o += [f"## {mins} 分鐘版", "", "| 時間 | 內容 |", "|---|---|"]
        o += [f"| {m} 分 | {name} |" for name, m in blocks]
        o += [""]
    o += ["## 帶領者材料（皆摘自本章）", "", f"**{key}**" if key else "", "", "### 看見基督（先讀給大家）", "", focus[:700], "",
          "### 提問式對話（由淺入深，一層一層問，不急著給答案）", ""]
    o += [f"{i}. {q}" for i, q in enumerate(ladder, 1)] or ["（本章無提問階梯）"]
    o += ["", "### 默想問題（分組或個人分享）", ""]
    o += [f"{i}. {q}" for i, q in enumerate(meditate, 1)] or ["（無）"]
    o += ["", "### 禱告回應（結束時一起禱告）", "", *(f"> {l}" for l in pr.splitlines()), ""]
    if closing:
        o += ["### 帶回家的一句", "", closing[:300], ""]
    o += ["\\newpage", "", f"# 學員講義：{title}", "", f"經文：{passage or '（見章首）'}", ""]
    if key:
        o += [f"**{key}**", ""]
    o += ["### 討論", ""] + [f"{i}. {q}" for i, q in enumerate(ladder, 1)]
    o += ["", "### 默想", ""] + [f"{i}. {q}" for i, q in enumerate(meditate, 1)]
    o += ["", "### 我的筆記", "", "&nbsp;", "", "&nbsp;", ""]
    return title, "\n".join(o)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_dir")
    ap.add_argument("--out", default="docs/leader-guides")
    a = ap.parse_args()
    book = Path(a.book_dir)
    if not book.is_dir():
        sys.exit(f"not a directory: {book}")
    dest = Path(a.out) / book.name
    dest.mkdir(parents=True, exist_ok=True)
    n = skipped = 0
    for ch in sorted(book.glob("[0-9][0-9]*-*.md")):
        if ch.name.startswith("00") or not re.match(r"\d{2}[a-z]?-", ch.name):
            continue
        if "## 基督焦點" not in ch.read_text(encoding="utf-8"):
            continue
        title, md = build(ch)
        if md is None:
            skipped += 1
            print(f"  skip {ch.name}: no 提問式對話 or 默想問題")
            continue
        (dest / ch.name).write_text(md, encoding="utf-8")
        n += 1
    print(f"wrote {n} guides to {dest} ({skipped} skipped)")


if __name__ == "__main__":
    main()
