#!/usr/bin/env python3
"""Generate books/bible/jude/98-appendix-indices.md from the chapter files.

The indices point to chapters, not pages: Jude is short enough that a
chapter locator is precise, and a chapter locator cannot go stale when a
page moves (cf. build-2-peter-index.py, whose page numbers need a three-pass
rebuild). Re-run after any content edit:

    python3 scripts/gen-jude-indices.py          # rewrite the appendix
    python3 scripts/gen-jude-indices.py --check  # exit 1 if it is stale
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books/bible/jude"
OUT = BOOK / "98-appendix-indices.md"

# Files indexed, with the label printed in the index.
SOURCES = [
    ("00c-revelation-order.md", "骨幹"),
    ("01-greeting-purpose.md", "第一章"),
    ("02-historical-warnings.md", "第二章"),
    ("03-false-teachers.md", "第三章"),
    ("04-exhortations.md", "第四章"),
    ("05-doxology.md", "第五章"),
]

# Canonical order of CUV book abbreviations as used in this book's prose.
BOOKS = """創 出 利 民 申 書 士 得 撒上 撒下 王上 王下 代上 代下 拉 尼 斯 伯 詩 箴 傳 歌
賽 耶 哀 結 但 何 珥 摩 俄 拿 彌 鴻 哈 番 該 亞 瑪
太 可 路 約 徒 羅 林前 林後 加 弗 腓 西 帖前 帖後 提前 提後 多 門 來 雅
彼前 彼後 約壹 約貳 約參 猶 啟""".split()
ORDER = {b: i for i, b in enumerate(BOOKS)}
# Longest abbreviations first so 約壹 is not read as 約.
ALIAS = {"詩篇": "詩"}
BOOK_RE = "|".join(sorted(BOOKS + list(ALIAS), key=len, reverse=True))
REF = re.compile(rf"(?<![一-鿿])({BOOK_RE})(\d+)(?::(\d+)(?:[-–](\d+))?)?")

TOPICS = [
    ("保守（τηρέω／φυλάσσω）", ["保守", "τηρέω", "φυλάσσω"]),
    ("爭辯、真道", ["爭辯", "真道"]),
    ("一次交付（ἅπαξ）", ["一次交付", "ἅπαξ"]),
    ("不敬虔", ["不敬虔", "不虔誠"]),
    ("恩典與放縱", ["放縱"]),
    ("主宰（δεσπότης）", ["主宰", "δεσπότης"]),
    ("出埃及的百姓", ["出埃及"]),
    ("天使與「本位」", ["本位", "天使"]),
    ("所多瑪、蛾摩拉", ["所多瑪"]),
    ("米迦勒與摩西的屍首", ["米迦勒"]),
    ("該隱", ["該隱"]),
    ("巴蘭", ["巴蘭"]),
    ("可拉", ["可拉"]),
    ("以諾的預言", ["以諾"]),
    ("這些人（οὗτοι）", ["這些人", "οὗτοι"]),
    ("使徒的話", ["使徒"]),
    ("聖靈裏禱告", ["聖靈裏禱告", "在聖靈裏"]),
    ("憐憫（ἔλεος）", ["憐憫", "憐恤", "ἔλεος"]),
    ("從火中搶出來", ["火中"]),
    ("無瑕無疵、不失腳", ["無瑕", "不失腳"]),
    ("頌榮", ["頌榮", "榮耀、威嚴"]),
    ("約翰福音十七章的禱告", ["約17"]),
    ("古卷異文", ["古卷", "抄本"]),
    ("與彼得後書的平行", ["彼後2", "彼得後書"]),
]


def body(text):
    """Drop YAML and the Scripture section (the Jude text itself would make
    every Jude verse appear in every chapter)."""
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    return re.sub(r"\n## 經文 \(Scripture\)\n.*?(?=\n## )", "\n", text, flags=re.S)


def build():
    refs = defaultdict(set)
    topics = defaultdict(list)
    for fname, label in SOURCES:
        text = body((BOOK / fname).read_text(encoding="utf-8"))
        for m in REF.finditer(text):
            b, c, v1, v2 = m.groups()
            b = ALIAS.get(b, b)
            if b == "猶":
                continue  # Jude itself is indexed by section below
            key = (ORDER[b], int(c), int(v1) if v1 else 0, int(v2) if v2 else 0, b, c, v1 or '', v2 or '')
            refs[key].add(label)
        for name, words in TOPICS:
            if any(w in text for w in words):
                topics[name].append(label)

    order = [lab for _, lab in SOURCES]
    lines = [
        "---",
        "title: 猶大書研讀",
        "subtitle: Epistle of Jude Deep Study",
        "author: PubHub 三書精讀系統",
        "date: 2026年10月",
        "publisher: 三書精讀出版系統",
        "---",
        "",
        "# 附錄：經文與主題索引 (Appendix: Indices)",
        "",
        "> 本索引由 `scripts/gen-jude-indices.py` 從各章正文自動產生，不是手工維護；"
        "改動任何一章之後重新執行即可。索引指向章，不指向頁碼——全書只有五章，"
        "章的定位已經足夠精確，也不會因排版移動而失效。「骨幹」指卷首〈啟示的次序與神的計劃〉。",
        "",
        "## 一、猶大書逐節索引",
        "",
        "| 經文 | 所在章 | 主題 |",
        "|------------|------------|--------------------------------------------------------|",
        "| 1-4節 | 第一章 | 蒙保守的人被呼召爭辯 |",
        "| 5-7節 | 第二章 | 神已經在歷史中審判 |",
        "| 8-16節 | 第三章 | 主必帶千萬聖者降臨 |",
        "| 17-23節 | 第四章 | 你們卻要保守自己 |",
        "| 24-25節 | 第五章 | 那能保守你們的 |",
        "",
        "## 二、其他經卷索引",
        "",
        "| 經文 | 出現於 |",
        "|------------------------|--------------------------------------------------------|",
    ]
    for key in sorted(refs):
        _, _, _, _, b, c, v1, v2 = key
        ref = f"{b}{c}" + (f":{v1}" if v1 else "") + (f"-{v2}" if v2 else "")
        where = "、".join(lab for lab in order if lab in refs[key])
        lines.append(f"| {ref} | {where} |")
    lines += ["", "## 三、主題索引", "", "| 主題 | 出現於 |", "|--------------------------------|------------------------------------------------|"]
    for name, _ in TOPICS:
        if topics[name]:
            lines.append(f"| {name} | {'、'.join(topics[name])} |")
    return "\n".join(lines) + "\n"


def main():
    new = build()
    if "--check" in sys.argv:
        old = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if old != new:
            print("STALE: 98-appendix-indices.md does not match the chapters; run scripts/gen-jude-indices.py")
            sys.exit(1)
        print("indices current")
        return
    OUT.write_text(new, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({new.count(chr(10))} lines)")


if __name__ == "__main__":
    main()
