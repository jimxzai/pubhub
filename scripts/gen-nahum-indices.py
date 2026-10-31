#!/usr/bin/env python3
"""Generate books/bible/Nahum/98-appendix-indices.md from the chapter files.

The indices point to chapters, not pages: Nahum is short enough that a
chapter locator is precise, and a chapter locator cannot go stale when a
page moves (cf. build-2-peter-index.py, whose page numbers need a three-pass
rebuild). Re-run after any content edit:

    python3 scripts/gen-nahum-indices.py          # rewrite the appendix
    python3 scripts/gen-nahum-indices.py --check  # exit 1 if it is stale
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books/bible/Nahum"
OUT = BOOK / "98-appendix-indices.md"

# Files indexed, with the label printed in the index.
SOURCES = [
    ("000-preface.md", "前言"),
    ("00-overview.md", "概覽"),
    ("00a-nahum-position.md", "位置"),
    ("00c-revelation-order.md", "骨幹"),
    ("01-who-can-stand.md", "第一章"),
    ("02-feet-on-the-mountains.md", "第二章"),
    ("03-i-am-against-you.md", "第三章"),
    ("04-who-will-grieve.md", "第四章"),
    ("05-no-healing.md", "第五章"),
]

# Canonical order of CUV book abbreviations as used in this book's prose.
BOOKS = """創 出 利 民 申 書 士 得 撒上 撒下 王上 王下 代上 代下 拉 尼 斯 伯 詩 箴 傳 歌
賽 耶 哀 結 但 何 珥 摩 俄 拿 彌 鴻 哈 番 該 亞 瑪
太 可 路 約 徒 羅 林前 林後 加 弗 腓 西 帖前 帖後 提前 提後 多 門 來 雅
彼前 彼後 約壹 約貳 約參 猶 啟""".split()
ORDER = {b: i for i, b in enumerate(BOOKS)}
# Longest abbreviations first so 約壹 is not read as 約.
ALIAS = {"詩篇": "詩", "約一": "約壹", "啟示錄": "啟"}
BOOK_RE = "|".join(sorted(BOOKS + list(ALIAS), key=len, reverse=True))
REF = re.compile(rf"(?:(?<![一-鿿])|(?<=參)|(?<=見))({BOOK_RE})(\d+)(?::(\d+)(?:[-–](\d+)(?!\d|:))?)?")

TOPICS = [
    ("耶和華（יהוה，十三次）", ["十三次", "יְהוָה", "יהוה", "耶和華的名"]),
    ("尼尼微（原文只點名三次）", ["三次「尼尼微」", "尼尼微只", "尼尼微的名", "點名三次", "原文只有三次", "只被點名"]),
    ("忌邪（קַנּוֹא）、施報（נֹקֵם）", ["忌邪", "施報"]),
    ("不輕易發怒、大有能力", ["不輕易發怒", "大有能力"]),
    ("立得住、誰（מִי）", ["立得住", "站得住", "四個「誰」", "兩個「誰」"]),
    ("保障：מָעוֹז（神）與 מְצֻרָה／מִבְצָר（城）", ["מָעוֹז", "מְצֻרָה", "מִבְצָר", "保障"]),
    ("不再（עוֹד）", ["「不再」", "不再使你受苦", "不再從你", "עוֹד"]),
    ("我與你為敵（הִנְנִי אֵלַיִךְ）", ["我與你為敵", "הִנְנִי"]),
    ("報好信、傳平安", ["報好信", "好信", "傳平安"]),
    ("安慰、悲傷（נחם）", ["安慰", "悲傷"]),
    ("彼列（בְּלִיַּעַל）", ["彼列", "בְּלִיַּעַל"]),
    ("軛", ["軛"]),
    ("獅子", ["獅子"]),
    ("沒有盡頭（וְאֵין קֵצֶה）", ["沒有盡頭", "無窮"]),
    ("流人血的城", ["流人血的城"]),
    ("妓女與邪術", ["妓女", "邪術"]),
    ("挪亞們（No-amon，底比斯）", ["挪亞們", "No-amon", "底比斯"]),
    ("蝗蟲、蝻子", ["蝗蟲", "蝻子"]),
    ("牧人與羊", ["牧人"]),
    ("損傷、醫治", ["損傷", "醫治"]),
    ("拍掌", ["拍掌"]),
    ("約拿書與尼尼微的悔改", ["約拿書", "約拿", "拿4"]),
    ("啟示錄", ["啟示錄", "啟6", "啟7", "啟18", "啟19"]),
    ("加爾文", ["加爾文"]),
    ("亨利", ["亨利"]),
    ("摩根", ["摩根"]),
    ("老弟兄", ["老弟兄"]),
]


def body(text):
    """Drop YAML and the Scripture section (the Nahum text itself would make
    every Nahum verse appear in every chapter)."""
    text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)
    return re.sub(r"\n## 經文 \(Scripture\)\n.*?(?=\n## )", "\n", text, flags=re.S)


def build():
    refs = defaultdict(set)
    topics = defaultdict(list)
    for fname, label in SOURCES:
        path = BOOK / fname
        if not path.exists():
            print(f"WARNING: missing {fname}; skipped", file=sys.stderr)
            continue
        text = body(path.read_text(encoding="utf-8"))
        for m in REF.finditer(text):
            b, c, v1, v2 = m.groups()
            b = ALIAS.get(b, b)
            if b == "鴻":
                continue  # Nahum itself is indexed by section below
            key = (ORDER[b], int(c), int(v1) if v1 else 0, int(v2) if v2 else 0, b, c, v1 or '', v2 or '')
            refs[key].add(label)
        for name, words in TOPICS:
            if any(w in text for w in words):
                topics[name].append(label)

    order = [lab for _, lab in SOURCES]
    lines = [
        "---",
        "title: 那鴻書研讀",
        "subtitle: The Book of Nahum Deep Study",
        "author: PubHub 三書精讀系統",
        "date: 2026年10月",
        "publisher: 三書精讀出版系統",
        "---",
        "",
        "# 附錄：經文與主題索引 (Appendix: Indices)",
        "",
        "> 本索引由 `scripts/gen-nahum-indices.py` 從各章正文自動產生，不是手工維護；"
        "改動任何一章之後重新執行即可。索引指向章，不指向頁碼——全書只有五章，"
        "章的定位已經足夠精確，也不會因排版移動而失效。「前言」「概覽」「位置」「骨幹」指卷首四章。",
        "",
        "## 一、那鴻書逐節索引",
        "",
        "| 經文 | 所在章 | 主題 |",
        "|------------|------------|--------------------------------------------------------|",
        "| 1:1-8 | 第一章 | 先認識這位神：他發忿恨，誰能立得住呢？ |",
        "| 1:9-15 | 第二章 | 先安慰，後宣判：報好信之人的腳登山 |",
        "| 2:1-13 | 第三章 | 戰事：我與你為敵 |",
        "| 3:1-7 | 第四章 | 然後才說罪名：有誰為你悲傷呢？ |",
        "| 3:8-19 | 第五章 | 沒有出路：你的損傷無法醫治 |",
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
    zero = [n for n, _ in TOPICS if not topics[n]]
    print("zero-hit topics:", zero or "none", file=sys.stderr)
    return "\n".join(lines) + "\n"


def main():
    new = build()
    if "--check" in sys.argv:
        old = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if old != new:
            print("STALE: 98-appendix-indices.md does not match the chapters; run scripts/gen-nahum-indices.py")
            sys.exit(1)
        print("indices current")
        return
    OUT.write_text(new, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({new.count(chr(10))} lines)")


if __name__ == "__main__":
    main()
