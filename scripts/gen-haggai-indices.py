#!/usr/bin/env python3
"""Generate books/bible/Haggai/98-appendix-indices.md from the chapter files.

The indices point to chapters, not pages: Haggai is short enough that a
chapter locator is precise, and a chapter locator cannot go stale when a
page moves (cf. build-2-peter-index.py, whose page numbers need a three-pass
rebuild). Re-run after any content edit:

    python3 scripts/gen-haggai-indices.py          # rewrite the appendix
    python3 scripts/gen-haggai-indices.py --check  # exit 1 if it is stale
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books/bible/Haggai"
OUT = BOOK / "98-appendix-indices.md"

# Files indexed, with the label printed in the index.
SOURCES = [
    ("00-overview.md", "概覽"),
    ("00a-haggai-position.md", "位置"),
    ("00c-revelation-order.md", "骨幹"),
    ("01-consider-your-ways.md", "第一章"),
    ("02-i-am-with-you.md", "第二章"),
    ("03-like-nothing.md", "第三章"),
    ("04-from-this-day.md", "第四章"),
    ("05-the-signet.md", "第五章"),
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
    ("省察（שִׂימוּ לְבַבְכֶם）", ["省察", "追想", "שִׂימוּ"]),
    ("從今日", ["從今日", "這日", "מִן־הַיּוֹם"]),
    ("同在（אִתְּכֶם）", ["同在", "אִתְּכֶם", "以馬內利"]),
    ("激動（עוּר）", ["激動"]),
    ("剩下的百姓（שְׁאֵרִית）", ["剩下的", "餘剩", "שְׁאֵרִית"]),
    ("荒涼與乾旱（חרב）", ["荒涼", "乾旱", "חָרֵב", "חֹרֶב"]),
    ("天花板的房屋", ["天花板", "paneled"]),
    ("破漏的囊", ["破漏", "錢囊"]),
    ("我的殿／這殿", ["我的殿", "這殿", "耶和華殿"]),
    ("榮耀（כָּבוֹד）", ["榮耀", "כָּבוֹד"]),
    ("萬國的珍寶／萬國所羨慕的", ["珍寶", "所羨慕", "חֶמְדַּת"]),
    ("銀子金子都是我的", ["銀子", "金子"]),
    ("平安（שָׁלוֹם）", ["平安", "שָׁלוֹם"]),
    ("震動（רָעַשׁ）", ["震動"]),
    ("聖與污穢", ["污穢", "成聖", "聖肉", "死屍"]),
    ("祭司的律法（תּוֹרָה）", ["問律法", "תּוֹרָה"]),
    ("旱風、霉爛、冰雹", ["旱風", "霉爛", "冰雹"]),
    ("賜福（אֲבָרֵךְ）", ["賜福"]),
    ("所羅巴伯", ["所羅巴伯"]),
    ("印（חוֹתָם）", ["為印", "印記", "戒指", "חוֹתָם"]),
    ("揀選（בָּחַרְתִּי）", ["揀選", "בָּחַרְתִּי"]),
    ("約書亞（大祭司）", ["大祭司約書亞", "耶書亞"]),
    ("撒迦利亞", ["撒迦利亞"]),
    ("耶哥尼雅（哥尼雅）", ["耶哥尼雅", "哥尼雅"]),
    ("日期", ["六月", "七月", "九月", "二十四日", "二十一日"]),
    ("住棚節", ["住棚節"]),
    ("以斯拉記的背景", ["拉3", "拉4", "拉5", "拉6"]),
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
            if b == "該":
                continue  # Haggai itself is indexed by section below
            key = (ORDER[b], int(c), int(v1) if v1 else 0, int(v2) if v2 else 0, b, c, v1 or '', v2 or '')
            refs[key].add(label)
        for name, words in TOPICS:
            if any(w in text for w in words):
                topics[name].append(label)

    order = [lab for _, lab in SOURCES]
    lines = [
        "---",
        "title: 哈該書研讀",
        "subtitle: The Book of Haggai Deep Study",
        "author: PubHub 三書精讀系統",
        "date: 2026年10月",
        "publisher: 三書精讀出版系統",
        "---",
        "",
        "# 附錄：經文與主題索引 (Appendix: Indices)",
        "",
        "> 本索引由 `scripts/gen-haggai-indices.py` 從各章正文自動產生，不是手工維護；"
        "改動任何一章之後重新執行即可。索引指向章，不指向頁碼——全書只有五章，"
        "章的定位已經足夠精確，也不會因排版移動而失效。「概覽」「位置」「骨幹」指卷首三章。",
        "",
        "## 一、哈該書逐節索引",
        "",
        "| 經文 | 所在章 | 主題 |",
        "|------------|------------|--------------------------------------------------------|",
        "| 1:1-11 | 第一章 | 先翻開帳本：你們要省察自己的行為 |",
        "| 1:12-15 | 第二章 | 先同在，後作工：我與你們同在 |",
        "| 2:1-9 | 第三章 | 用同在回答比較：豈不在眼中看如無有 |",
        "| 2:10-19 | 第四章 | 祝福在收成之前：從今日起 |",
        "| 2:20-23 | 第五章 | 最後一句是揀選：我必以你為印 |",
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
            print("STALE: 98-appendix-indices.md does not match the chapters; run scripts/gen-haggai-indices.py")
            sys.exit(1)
        print("indices current")
        return
    OUT.write_text(new, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({new.count(chr(10))} lines)")


if __name__ == "__main__":
    main()
