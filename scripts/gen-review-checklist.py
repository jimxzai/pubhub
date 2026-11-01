#!/usr/bin/env python3
"""Generate a pastoral-review checklist for one book (roadmap item 3.5).

The aim is a document a reviewer can read in 1-2 hours instead of the whole book. It only EXTRACTS
what is already in the chapters -- it writes no theology of its own:

  * the book's spine (spine chapter title + first paragraph) and the 座標 line of every chapter
  * every 領受要點 heading (the claims the chapter says the reader should take away)
  * sentences in the 領受要點 / 老弟兄 sections that make absolute claims (必須/唯一/絕對/從來/永遠不...)
  * sentences where the book itself admits a limit (編者註, 查不到, 無法核實, 未取得)
  * passages with a known textual or interpretive dispute, when the chapter touches them
  * each chapter's closing line about Christ

    python3 scripts/gen-review-checklist.py books/bible/gospel-of-john [-o out.md]
"""
import argparse
import re
import sys
from pathlib import Path

ABSOLUTE = re.compile(r"必須|唯一|絕對|從來|永遠不|沒有任何|無一例外|毫無疑問|必然|斷然|惟獨|唯獨")
LIMIT = re.compile(r"編者註|編者比較|查不到|無法核實|無法查證|未取得|未能取得|尚未核實|待查")
CLOSING = re.compile(r"你看見耶穌了嗎")
DISPUTED = [  # text-critical items: relevant in any book that touches them
    (r"約\s?7:53|約\s?8:1-11", "約 7:53-8:11 行淫婦人段：古抄本有無爭議"),
    (r"可\s?16:9-20", "可 16:9-20 馬可福音長結尾：古抄本有無爭議"),
    (r"約壹\s?5:7", "約壹 5:7 逗號：後期抄本加入"),
    (r"提前\s?3:16", "提前 3:16「神/祂」異文"),
    (r"路\s?22:43-44", "路 22:43-44：古抄本有無爭議"),
]
BOOK_SPECIFIC = {  # interpretive disputes: only checked inside the book that is about them
    "isaiah": [(r"以賽亞書?\s?4\d|賽\s?(?:4[0-9]|5[0-5]):", "以賽亞書 40-55 章作者與寫作時間")],
    "daniel": [(r"但\s?(?:7|8|11):", "但以理書寫作年代與預言解法")],
    "revelation": [(r"啟\s?20:", "啟 20 章千禧年解法")],
    "roman": [(r"羅\s?9:", "羅 9 章揀選與預定的解法")],
    "hebrews": [(r"來\s?6:4|來\s?10:26", "來 6:4-8 與 10:26：失落與確據的解法")],
    "2-peter": [(r"彼後", "彼得後書的作者與寫作時間")],
    "genesis": [(r"創\s?1:", "創 1 章創造日的解法")],
}


def sections(text):
    """{'## heading': body} for level-2 sections."""
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        if line.startswith("## "):
            if cur is not None:
                out[cur] = "\n".join(buf)
            cur, buf = line[3:].strip(), []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf)
    return out


def sentences(block):
    flat = re.sub(r"\s+", " ", re.sub(r"^(?:>|\||#|\s*[-*] ).*$", "", block, flags=re.M))
    return [s.strip() for s in re.split(r"(?<=[。！？])", flat) if s.strip()]


def first_para(path):
    paras = [p.strip() for p in path.read_text(encoding="utf-8").split("\n\n")
             if p.strip() and not p.lstrip().startswith(("#", "---", "|", ">", "<", "\\"))]
    return paras[0] if paras else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("book_dir")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()
    book = Path(a.book_dir)
    if not book.is_dir():
        sys.exit(f"not a directory: {book}")

    chapters = sorted(p for p in book.glob("[0-9][0-9]*-*.md")
                      if re.match(r"\d{2}[a-z]?-", p.name) and not p.name.startswith("00")
                      and "## 基督焦點" in p.read_text(encoding="utf-8"))
    spine = [p for p in sorted(book.glob("00*.md")) if re.search(r"spine|order", p.name)]
    out = [f"# 審核清單：{book.name}", "",
           "本清單由 `scripts/gen-review-checklist.py` 從書稿**擷取**，不含任何新增的神學判斷。"
           "審核者逐項簽核；有疑義的標記後退回作者。", ""]

    out += ["## 1. 全書骨幹（先讀這一節）", ""]
    for s in spine:
        title = next((l[2:].strip() for l in s.read_text(encoding="utf-8").splitlines() if l.startswith("# ")), s.name)
        out += [f"- **{title}**（`{s.name}`）", f"  {first_para(s)[:300]}", ""]
    if not spine:
        out += ["（找不到骨幹章。）", ""]

    flagged_abs, flagged_limit, disputed, rows = [], [], {}, []
    out_ch = ["## 2. 逐章：座標、領受要點、收尾", ""]
    for ch in chapters:
        t = ch.read_text(encoding="utf-8")
        title = next((l[2:].strip() for l in t.splitlines() if l.startswith("# ")), ch.name)
        sec = sections(t)
        coord = next((l.lstrip("> ").strip() for l in t.splitlines() if "座標" in l and l.startswith(">")), "")
        points = re.findall(r"^### (\d+\..+)$", t[t.find("## 領受要點"):] if "## 領受要點" in t else "", re.M)
        closing = next((p.strip() for p in reversed(t.split("\n\n"))
                       if CLOSING.search(p) and not p.lstrip().startswith((">", "#", "|", "- ", "1.", "2."))), "")
        out_ch += [f"### {ch.name} — {title}", ""]
        out_ch += [f"- 座標：{coord or '（缺）'}"]
        for pt in points:
            out_ch += [f"- 領受要點：{pt}"]
        out_ch += [f"- 收尾：{closing or '（缺）'}", "- 簽核：☐ 通過　☐ 修改　備註：", ""]
        for h, body in sec.items():
            if h.startswith(("領受要點", "老弟兄")):
                for s in sentences(body):
                    if ABSOLUTE.search(s):
                        flagged_abs.append((ch.name, s))
        for s in sentences(t):
            if LIMIT.search(s):
                flagged_limit.append((ch.name, s))
        for pat, label in DISPUTED + BOOK_SPECIFIC.get(book.name, []):
            if re.search(pat, t):
                disputed.setdefault(label, []).append(ch.name)

    out += out_ch
    out += [f"## 3. 絕對性斷言（{len(flagged_abs)} 句，請逐句確認經文與注疏支持）", ""]
    out += [f"- `{n}`：{s[:200]}" for n, s in flagged_abs] or ["（無）"]
    out += ["", f"## 4. 書稿自己承認的限制（{len(flagged_limit)} 句）", ""]
    out += [f"- `{n}`：{s[:200]}" for n, s in flagged_limit] or ["（無）"]
    out += ["", "## 5. 已知爭議經文（章節觸及時列出；請確認書稿立場是否適當標示）", ""]
    out += [f"- {lbl}：{', '.join(sorted(set(v)))}" for lbl, v in disputed.items()] or ["（無）"]
    out += ["", "## 6. 審核者簽核", "",
            "審核者：＿＿＿＿　日期：＿＿＿＿　結論：☐ 可出版　☐ 修改後可出版　☐ 退回", ""]
    text = "\n".join(out)
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
        print(f"wrote {a.out}: {len(chapters)} chapters, {len(flagged_abs)} absolute claims, "
              f"{len(flagged_limit)} stated limits, {len(disputed)} disputed topics, {len(text.split())} tokens")
    else:
        print(text)


if __name__ == "__main__":
    main()
