#!/usr/bin/env python3
"""Generate books/bible/Zapphaniah/98-appendix-indices.md from the chapter files.

The indices point to chapters, not pages: Obadiah is short enough that a
chapter locator is precise, and a chapter locator cannot go stale when a
page moves (cf. build-2-peter-index.py, whose page numbers need a three-pass
rebuild). Re-run after any content edit:

    python3 scripts/gen-zephaniah-indices.py          # rewrite the appendix
    python3 scripts/gen-zephaniah-indices.py --check  # exit 1 if it is stale
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books/bible/Zapphaniah"
OUT = BOOK / "98-appendix-indices.md"

# Files indexed, with the label printed in the index.
SOURCES = [
    ("00-overview.md", "概覽"),
    ("00a-zephaniah-position.md", "位置"),
    ("00c-revelation-order.md", "骨幹"),
    ("01-i-will-sweep-away-everything.md", "第一章"),
    ("02-be-silent-before-the-lord.md", "第二章"),
    ("03-the-great-day-is-near.md", "第三章"),
    ("04-gather-and-seek.md", "第四章"),
    ("05-the-four-directions.md", "第五章"),
    ("06-woe-to-the-rebellious-city.md", "第六章"),
    ("07-wait-for-me.md", "第七章"),
    ("08-the-lord-in-your-midst.md", "第八章"),
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
    ("耶和華的日子", ["耶和華的日子", "耶和華的大日", "耶和華發怒的日子"]),
    ("近（קָרוֹב）", ["近了", "臨近", "快到"]),
    ("親近（קָרַב）", ["親近"]),
    ("在你中間（קֶרֶב）", ["中間"]),
    ("尋求（בִּקֵּשׁ）", ["尋求"]),
    ("或者（אוּלַי）", ["或者"]),
    ("靜默（הַס）", ["靜默"]),
    ("燈、巡查", ["用燈", "巡查"]),
    ("除滅、聚集（אסף）", ["除滅", "聚集", "招聚"]),
    ("火與嫉妒（קִנְאָה）", ["烈火", "忿怒如火", "嫉妒", "熱心"]),
    ("巴力、基瑪林、瑪勒堪", ["巴力", "基瑪林", "瑪勒堪"]),
    ("約西亞的改革", ["約西亞"]),
    ("非利士（迦薩、亞實基倫、亞實突、以革倫）", ["非利士", "迦薩", "亞實基倫", "亞實突", "以革倫"]),
    ("摩押、亞捫", ["摩押", "亞捫"]),
    ("古實", ["古實"]),
    ("亞述、尼尼微", ["亞述", "尼尼微"]),
    ("那座城（3:1）", ["悖逆、污穢", "欺壓的城", "沒有名字"]),
    ("每早晨", ["早晨"]),
    ("清潔的言語（שָׂפָה בְּרוּרָה）", ["清潔的言語"]),
    ("餘民、困苦貧寒的民", ["餘民", "困苦貧寒", "餘剩"]),
    ("名（שֵׁם）", ["名字", "耶和華的名", "名聲"]),
    ("躺臥（רָבַץ）", ["躺臥"]),
    ("歌唱、歡呼", ["歌唱", "歡呼", "歡欣"]),
    ("默然愛你（3:17）", ["默然"]),
    ("以色列的王", ["以色列的王"]),
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
            if b == "番":
                continue  # Zephaniah itself is indexed by section below
            key = (ORDER[b], int(c), int(v1) if v1 else 0, int(v2) if v2 else 0, b, c, v1 or '', v2 or '')
            refs[key].add(label)
        for name, words in TOPICS:
            if any(w in text for w in words):
                topics[name].append(label)

    order = [lab for _, lab in SOURCES]
    lines = [
        "---",
        "title: 西番雅書研讀",
        "subtitle: The Book of Zephaniah Deep Study",
        "author: PubHub 三書精讀系統",
        "date: 2026年10月",
        "publisher: 三書精讀出版系統",
        "---",
        "",
        "# 附錄：經文與主題索引 (Appendix: Indices)",
        "",
        "> 本索引由 `scripts/gen-zephaniah-indices.py` 從各章正文自動產生，不是手工維護；"
        "改動任何一章之後重新執行即可。索引指向章，不指向頁碼——全書只有八章，"
        "章的定位已經足夠精確，也不會因排版移動而失效。「概覽」「位置」「骨幹」指卷首三章。",
        "",
        "## 一、西番雅書逐節索引",
        "",
        "| 經文 | 所在章 | 主題 |",
        "|------------|------------|--------------------------------------------------------|",
        "| 1:1-6 | 第一章 | 神先開口：我必從地上除滅萬類 |",
        "| 1:7-13 | 第二章 | 日子近了：靜默無聲，用燈巡查 |",
        "| 1:14-18 | 第三章 | 日子近了：六個「……的日子」 |",
        "| 2:1-3 | 第四章 | 先開一道門：尋求耶和華 |",
        "| 2:4-15 | 第五章 | 推向四方：西、東、南、北 |",
        "| 3:1-7 | 第六章 | 回到那座城：她不親近，祂在中間 |",
        "| 3:8-13 | 第七章 | 等候：清潔的言語，困苦貧寒的民 |",
        "| 3:14-20 | 第八章 | 歌唱：祂在你中間 |",
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
            print("STALE: 98-appendix-indices.md does not match the chapters; run scripts/gen-zephaniah-indices.py")
            sys.exit(1)
        print("indices current")
        return
    OUT.write_text(new, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({new.count(chr(10))} lines)")


if __name__ == "__main__":
    main()
