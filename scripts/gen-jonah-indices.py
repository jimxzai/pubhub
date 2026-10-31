#!/usr/bin/env python3
"""Generate books/bible/Jonah/98-appendix-indices.md from the chapter files.

The indices point to chapters, not pages: Jonah is short enough that a
chapter locator is precise, and a chapter locator cannot go stale when a
page moves (cf. build-2-peter-index.py, whose page numbers need a three-pass
rebuild). Re-run after any content edit:

    python3 scripts/gen-jonah-indices.py          # rewrite the appendix
    python3 scripts/gen-jonah-indices.py --check  # exit 1 if it is stale
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books/bible/Jonah"
OUT = BOOK / "98-appendix-indices.md"

# Files indexed, with the label printed in the index.
SOURCES = [
    ("00b-revelation-order.md", "骨幹"),
    ("01-arise-and-flee.md", "第一章"),
    ("02-the-lord-hurled-a-wind.md", "第二章"),
    ("03-throw-me-into-the-sea.md", "第三章"),
    ("04-the-appointed-fish.md", "第四章"),
    ("05-the-second-time.md", "第五章"),
    ("06-nineveh-turns.md", "第六章"),
    ("07-is-it-right-to-be-angry.md", "第七章"),
    ("08-the-last-question.md", "第八章"),
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
    ("安排（מנה）", ["安排", "מנה"]),
    ("下去（ירד）", ["下去", "下到", "ירד"]),
    ("起來（קום）", ["起來", "קום"]),
    ("大（גדול）", ["גדול"]),
    ("惡／災（רעה）", ["רעה", "רָעָה"]),
    ("後悔（נחם）", ["後悔", "נחם", "נִחַם"]),
    ("愛惜（חוס）", ["愛惜", "חוס"]),
    ("逃（ברח）", ["ברח", "逃"]),
    ("尼尼微", ["尼尼微"]),
    ("他施、約帕", ["他施", "約帕"]),
    ("水手與船主", ["水手", "船主"]),
    ("掣籤", ["掣籤", "籤"]),
    ("大魚、三日三夜", ["大魚", "三日三夜"]),
    ("魚腹中的禱告", ["魚腹", "禱告"]),
    ("救恩出於耶和華", ["救恩出於耶和華", "ישועתה"]),
    ("麻布、禁食", ["麻布", "禁食"]),
    ("蓖麻、蟲、東風", ["蓖麻", "東風"]),
    ("十二萬人、牲畜", ["十二萬", "牲畜"]),
    ("神的性情告白（出34:6）", ["出34:6", "有恩典", "不輕易發怒"]),
    ("約拿的神蹟", ["約拿的神蹟", "太12:39", "路11:29", "路11:30"]),
    ("加爾文", ["加爾文"]),
    ("亨利", ["亨利"]),
    ("摩根", ["摩根"]),
    ("奧古斯丁", ["奧古斯丁"]),
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
            if b == "拿":
                continue  # Jonah itself is indexed by section below
            key = (ORDER[b], int(c), int(v1) if v1 else 0, int(v2) if v2 else 0, b, c, v1 or '', v2 or '')
            refs[key].add(label)
        for name, words in TOPICS:
            if any(w in text for w in words):
                topics[name].append(label)

    order = [lab for _, lab in SOURCES]
    lines = [
        "---",
        "title: 約拿書研讀",
        "subtitle: The Book of Jonah Deep Study",
        "author: PubHub 三書精讀系統",
        "date: 2026年10月",
        "publisher: 三書精讀出版系統",
        "---",
        "",
        "# 附錄：經文與主題索引 (Appendix: Indices)",
        "",
        "> 本索引由 `scripts/gen-jonah-indices.py` 從各章正文自動產生，不是手工維護；"
        "改動任何一章之後重新執行即可。索引指向章，不指向頁碼——全書只有八章，"
        "章的定位已經足夠精確，也不會因排版移動而失效。「骨幹」指卷首〈啟示的次序與神的計劃〉。",
        "",
        "## 一、約拿書逐節索引",
        "",
        "| 經文 | 所在章 | 主題 |",
        "|------------|------------|--------------------------------------------------------|",
        "| 1:1-3 | 第一章 | 起來去，他卻起來逃 |",
        "| 1:4-10 | 第二章 | 耶和華使海中起大風 |",
        "| 1:11-16 | 第三章 | 將我拋在海中 |",
        "| 1:17-2:10 | 第四章 | 耶和華安排一條大魚 |",
        "| 3:1-4 | 第五章 | 話二次臨到約拿 |",
        "| 3:5-10 | 第六章 | 他們離開惡道，神就後悔 |",
        "| 4:1-4 | 第七章 | 你這樣發怒合乎理嗎 |",
        "| 4:5-11 | 第八章 | 我豈能不愛惜呢 |",
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
            print("STALE: 98-appendix-indices.md does not match the chapters; run scripts/gen-jonah-indices.py")
            sys.exit(1)
        print("indices current")
        return
    OUT.write_text(new, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({new.count(chr(10))} lines)")


if __name__ == "__main__":
    main()
