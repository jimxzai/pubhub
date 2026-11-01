#!/usr/bin/env python3
"""Generate books/bible/malachi/98-appendix-indices.md from the chapter files.

The indices point to chapters, not pages: Malachi is short enough that a
chapter locator is precise, and a chapter locator cannot go stale when a
page moves (cf. build-2-peter-index.py, whose page numbers need a three-pass
rebuild). Re-run after any content edit:

    python3 scripts/gen-malachi-indices.py          # rewrite the appendix
    python3 scripts/gen-malachi-indices.py --check  # exit 1 if it is stale
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books/bible/malachi"
OUT = BOOK / "98-appendix-indices.md"

# Files indexed, with the label printed in the index.
SOURCES = [
    ("00-overview.md", "概覽"),
    ("00a-malachi-position.md", "位置"),
    ("00c-revelation-order.md", "骨幹"),
    ("01-i-have-loved-you.md", "第一章"),
    ("02-where-is-my-honor.md", "第二章"),
    ("03-the-covenant-with-levi.md", "第三章"),
    ("04-the-wife-of-your-covenant.md", "第四章"),
    ("05-the-messenger-of-the-covenant.md", "第五章"),
    ("06-return-to-me.md", "第六章"),
    ("07-the-book-of-remembrance.md", "第七章"),
    ("08-the-sun-of-righteousness.md", "第八章"),
    ("90-to-the-gospels.md", "通往福音書"),
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
    ("愛（אָהַב）", ["אָהַב", "我曾愛你們", "神先愛"]),
    ("在何事上（בַּמָּה）／八個問題", ["在何事上", "八個問題", "八問", "בַּמָּה"]),
    ("你們卻說（וַאֲמַרְתֶּם）", ["你們卻說", "וַאֲמַרְתֶּם"]),
    ("以掃、以東、雅各", ["以掃", "以東", "雅各"]),
    ("恨（שָׂנֵא）", ["שָׂנֵא", "恨以掃", "惡以掃"]),
    ("名（שֵׁם）", ["שֵׁם", "我的名", "輕看我的名"]),
    ("祭司、利未", ["祭司", "利未"]),
    ("供物、祭壇、瞎眼瘸腿的牲畜", ["供物", "祭壇", "瞎眼", "瘸腿"]),
    ("萬國中我的名為大（1:11）", ["1:11", "日出到日落", "萬國中"]),
    ("約（בְּרִית）", ["בְּרִית", "立約的使者", "盟約"]),
    ("詭詐（בָּגַד）", ["בָּגַד", "詭詐"]),
    ("婚姻、休妻", ["休妻", "離婚", "幼年所娶的妻"]),
    ("使者（מַלְאָךְ）", ["מַלְאָךְ", "我的使者", "使者"]),
    ("差遣（שָׁלַח）", ["שָׁלַח", "差遣"]),
    ("忽然進入殿的主", ["忽然", "進入他的殿"]),
    ("煉金之人的火", ["煉金", "漂布", "煉淨"]),
    ("回轉、歸回（שׁוּב）", ["שׁוּב", "歸向我", "歸回"]),
    ("不改變（3:6）", ["不改變"]),
    ("十分之一、奪取", ["十分之一", "奪取", "קָבַע"]),
    ("倉庫、試試我", ["倉庫", "試試我"]),
    ("紀念冊（3:16）", ["紀念冊"]),
    ("彼此談論（דבר）", ["彼此談論", "נִדְבַּרְנוּ", "נִדְבְּרוּ"]),
    ("特特歸我的產業（סְגֻלָּה）", ["特特歸我", "סְגֻלָּה"]),
    ("日子（יוֹם）", ["日子", "יוֹם"]),
    ("公義的日頭（4:2）", ["公義的日頭", "日頭"]),
    ("以利亞、摩西", ["以利亞", "摩西"]),
    ("咒詛（חֵרֶם）", ["咒詛", "חֵרֶם"]),
    ("施洗約翰", ["施洗約翰", "約翰"]),
    ("與尼希米記的對照", ["尼希米", "尼13"]),
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
            if b == "瑪":
                continue  # Malachi itself is indexed by section below
            key = (ORDER[b], int(c), int(v1) if v1 else 0, int(v2) if v2 else 0, b, c, v1 or '', v2 or '')
            refs[key].add(label)
        for name, words in TOPICS:
            if any(w in text for w in words):
                topics[name].append(label)

    order = [lab for _, lab in SOURCES]
    lines = [
        "---",
        "title: 瑪拉基書研讀",
        "subtitle: The Book of Malachi Deep Study",
        "author: PubHub 三書精讀系統",
        "date: 2026年10月",
        "publisher: 三書精讀出版系統",
        "---",
        "",
        "# 附錄：經文與主題索引 (Appendix: Indices)",
        "",
        "> 本索引由 `scripts/gen-malachi-indices.py` 從各章正文自動產生，不是手工維護；"
        "改動任何一章之後重新執行即可。索引指向章，不指向頁碼——全書只有八章，"
        "章的定位已經足夠精確，也不會因排版移動而失效。「概覽」「位置」「骨幹」指卷首三章。",
        "",
        "## 一、瑪拉基書逐節索引",
        "",
        "| 經文 | 所在章 | 主題 |",
        "|------------|------------|--------------------------------------------------------|",
        "| 1:1-5 | 第一章 | 愛：我曾愛你們——你在何事上愛我們呢？ |",
        "| 1:6-14 | 第二章 | 名：我的尊榮在哪裏 |",
        "| 2:1-9 | 第三章 | 名：我與利未所立的約 |",
        "| 2:10-16 | 第四章 | 約：你盟約的妻 |",
        "| 2:17–3:5 | 第五章 | 使者：忽然進入殿的主 |",
        "| 3:6-12 | 第六章 | 歸回：你們要歸向我 |",
        "| 3:13-18 | 第七章 | 日子：紀念冊 |",
        "| 4:1-6 | 第八章 | 日子：公義的日頭 |",
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
            print("STALE: 98-appendix-indices.md does not match the chapters; run scripts/gen-malachi-indices.py")
            sys.exit(1)
        print("indices current")
        return
    OUT.write_text(new, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({new.count(chr(10))} lines)")


if __name__ == "__main__":
    main()
