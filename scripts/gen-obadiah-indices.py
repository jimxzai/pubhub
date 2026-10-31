#!/usr/bin/env python3
"""Generate books/bible/Obadiah/98-appendix-indices.md from the chapter files.

The indices point to chapters, not pages: Obadiah is short enough that a
chapter locator is precise, and a chapter locator cannot go stale when a
page moves (cf. build-2-peter-index.py, whose page numbers need a three-pass
rebuild). Re-run after any content edit:

    python3 scripts/gen-obadiah-indices.py          # rewrite the appendix
    python3 scripts/gen-obadiah-indices.py --check  # exit 1 if it is stale
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books/bible/Obadiah"
OUT = BOOK / "98-appendix-indices.md"

# Files indexed, with the label printed in the index.
SOURCES = [
    ("00-overview.md", "概覽"),
    ("00a-obadiah-position.md", "位置"),
    ("00c-revelation-order.md", "骨幹"),
    ("01-the-report-and-the-pride.md", "第一章"),
    ("02-everything-you-trusted.md", "第二章"),
    ("03-the-day-of-your-brother.md", "第三章"),
    ("04-as-you-have-done.md", "第四章"),
    ("05-the-kingdom-is-the-lords.md", "第五章"),
]

# Canonical order of CUV book abbreviations as used in this book's prose.
BOOKS = """創 出 利 民 申 書 士 得 撒上 撒下 王上 王下 代上 代下 拉 尼 斯 伯 詩 箴 傳 歌
賽 耶 哀 結 但 何 珥 摩 俄 拿 彌 鴻 哈 番 該 亞 瑪
太 可 路 約 徒 羅 林前 林後 加 弗 腓 西 帖前 帖後 提前 提後 多 門 來 雅
彼前 彼後 約壹 約貳 約參 猶 啟""".split()
ORDER = {b: i for i, b in enumerate(BOOKS)}
# Longest abbreviations first so 約壹 is not read as 約.
ALIAS = {"詩篇": "詩", "約一": "約壹"}
BOOK_RE = "|".join(sorted(BOOKS + list(ALIAS), key=len, reverse=True))
REF = re.compile(rf"(?<![一-鿿])({BOOK_RE})(\d+)(?::(\d+)(?:[-–](\d+))?)?")

TOPICS = [
    ("日子（יוֹם）", ["日子", "יוֹם"]),
    ("耶和華的日子", ["耶和華的日子", "耶和華降罰的日子"]),
    ("站在一旁", ["站在一旁", "旁觀"]),
    ("弟兄（אָח）", ["弟兄", "兄弟"]),
    ("以掃、以東、西珥山", ["以掃", "以東", "西珥"]),
    ("雅各、約瑟家", ["雅各家", "約瑟家"]),
    ("提幔", ["提幔"]),
    ("山穴、磐石", ["山穴", "磐石"]),
    ("狂傲、驕傲", ["狂傲", "驕傲"]),
    ("自欺、被欺", ["自欺", "欺騙"]),
    ("拉下（יָרַד）", ["拉下"]),
    ("財寶", ["財寶"]),
    ("盟友、同桌的人", ["盟友", "同桌", "結盟"]),
    ("智慧、聰明（תְּבוּנָה）", ["智慧", "聰明"]),
    ("勇士", ["勇士"]),
    ("剪除（כָּרַת）", ["剪除"]),
    ("八個「不當」（אַל）", ["不當"]),
    ("你怎樣行，他也必照樣向你行", ["照樣", "量器"]),
    ("杯", ["苦杯", "那杯", "這杯", "酒杯", "忿怒之杯"]),
    ("萬國", ["萬國"]),
    ("逃脫、餘剩（פלט／שריד）", ["逃脫", "餘剩", "剩下"]),
    ("成聖", ["成聖"]),
    ("承受產業（יָרַשׁ）", ["承受", "產業"]),
    ("火與碎秸", ["碎秸"]),
    ("拯救者（מוֹשִׁעִים）", ["拯救者"]),
    ("國度（הַמְּלוּכָה）", ["國度"]),
    ("與耶利米書四十九章的平行", ["耶49", "耶利米書49", "耶利米書4"]),
    ("與阿摩司書的對照", ["摩1:11", "摩9:11", "阿摩司書"]),
    ("詩篇一三七篇", ["詩137"]),
    ("以土買、希律", ["以土買", "希律"]),
    ("年代與作者", ["年代", "作者"]),
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
            if b == "俄":
                continue  # Obadiah itself is indexed by section below
            key = (ORDER[b], int(c), int(v1) if v1 else 0, int(v2) if v2 else 0, b, c, v1 or '', v2 or '')
            refs[key].add(label)
        for name, words in TOPICS:
            if any(w in text for w in words):
                topics[name].append(label)

    order = [lab for _, lab in SOURCES]
    lines = [
        "---",
        "title: 俄巴底亞書研讀",
        "subtitle: The Book of Obadiah Deep Study",
        "author: PubHub 三書精讀系統",
        "date: 2026年10月",
        "publisher: 三書精讀出版系統",
        "---",
        "",
        "# 附錄：經文與主題索引 (Appendix: Indices)",
        "",
        "> 本索引由 `scripts/gen-obadiah-indices.py` 從各章正文自動產生，不是手工維護；"
        "改動任何一章之後重新執行即可。索引指向章，不指向頁碼——全書只有五章，"
        "章的定位已經足夠精確，也不會因排版移動而失效。「概覽」「位置」「骨幹」指卷首三章。",
        "",
        "## 一、俄巴底亞書逐節索引",
        "",
        "| 經文 | 所在章 | 主題 |",
        "|------------|------------|--------------------------------------------------------|",
        "| 1-4節 | 第一章 | 先聽見：誰能將我拉下地去呢？ |",
        "| 5-9節 | 第二章 | 一件一件取走：所倚靠的 |",
        "| 10-14節 | 第三章 | 然後才說罪名：你兄弟遭難的日子 |",
        "| 15-16節 | 第四章 | 日子擴大：你怎樣行，他也必照樣向你行 |",
        "| 17-21節 | 第五章 | 最後一句屬於國度 |",
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
            print("STALE: 98-appendix-indices.md does not match the chapters; run scripts/gen-obadiah-indices.py")
            sys.exit(1)
        print("indices current")
        return
    OUT.write_text(new, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({new.count(chr(10))} lines)")


if __name__ == "__main__":
    main()
