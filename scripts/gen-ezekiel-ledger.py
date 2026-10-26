#!/usr/bin/env python3
"""Generate the Ezekiel volume's citation ledger (99-appendix-references.md) from the book's own text.

The ledger is the honesty account for the promise 「不編造一段出處」. A hand-kept ledger
drifts from the chapters, so every count, every source file and every hymn line below
is read back out of the chapter files and out of `.sources/`.

For each `> "English quote"` block in a study chapter the script
  * classifies the commentator from the `> — source` line ("同上" inherits the last one),
  * finds the `.sources` file(s) that contain the quote verbatim (whitespace, case and
    punctuation ignored, as check_quotes.py does),
and prints one table per commentator.

Usage:  python3 scripts/gen-ezekiel-ledger.py --write
        python3 scripts/gen-ezekiel-ledger.py           # print
"""
import re
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "bible" / "ezekiel"
SRC = BOOK / ".sources"
OUT = BOOK / "99-appendix-references.md"

WHO = OrderedDict([
    ("fathers", "教父（Irenaeus、Origen、Tertullian、Justin、Clement of Rome、Cyril of Jerusalem、Augustine、Gregory Nazianzen、Chrysostom、Cyprian 等）"),
    ("calvin", "加爾文（John Calvin），*Commentary on Ezekiel*（僅第 1–20 章）"),
    ("henry", "馬太·亨利（Matthew Henry），*Commentary on the Whole Bible*，以西結書卷（原著 1706-1721）"),
    ("kd", "凱爾與德利奇（C. F. Keil & F. Delitzsch），*Biblical Commentary on the Old Testament*（1870）"),
    ("expositors", "司金納（J. Skinner），*Ezekiel*（*The Expositor's Bible*，1895）"),
    ("cambridge", "戴維森（A. B. Davidson），*The Cambridge Bible for Schools and Colleges: Ezekiel*（1892）"),
    ("pulpit", "《講壇釋經》（*The Pulpit Commentary*）"),
    ("jfb", "JFB（Jamieson, Fausset & Brown），*Commentary Critical and Explanatory*"),
    ("gill", "吉爾（John Gill），*Exposition of the Entire Bible*"),
    ("morgan", "摩根（G. Campbell Morgan），*The Analyzed Bible*（Job to Malachi 卷）以西結書分段大綱"),
])
PREFIX = {"calvin": "calvin-", "henry": "henry-", "kd": "kad-", "expositors": "expositors-", "cambridge": "cambridge-",
          "pulpit": "pulpit-", "jfb": "jfb-", "gill": "gill-"}
KEYS = [("Calvin", "calvin"), ("Matthew Henry", "henry"), ("Keil", "kd"), ("Cambridge", "cambridge"),
        ("Skinner", "expositors"), ("Expositor", "expositors"), ("Pulpit", "pulpit"), ("JFB", "jfb"),
        ("Jamieson", "jfb"), ("Gill", "gill"), ("Morgan", "morgan")]
FATHER_KEYS = ["Irenaeus", "Origen", "Tertullian", "Justin", "Clement", "Barnabas", "Cyril", "Augustine", "Jerome",
               "Gregory", "Chrysostom", "Cyprian", "Epistle", "Hippolytus", "Athanasius"]


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"[^a-z0-9]", "", s.lower())


def load_corpus():
    corp = {}
    for p in sorted((SRC / "commentary").glob("*.txt")):
        corp[p.name] = norm(p.read_text(encoding="utf8", errors="ignore"))
    for p in sorted((SRC / "fathers").glob("[0-9]*.txt")):
        t = p.read_text(encoding="utf8", errors="ignore")
        corp["fathers/" + p.name] = norm(t.split("\n---\n", 1)[1] if "\n---\n" in t else t)
    return corp


def classify(src):
    for k, n in KEYS:
        if k in src:
            return n
    if any(f in src for f in FATHER_KEYS):
        return "fathers"
    return None


def chapters():
    return [(int(p.name[:2]), p) for p in sorted(BOOK.glob("[0-3][0-9]-*.md")) if 1 <= int(p.name[:2]) <= 34]


def ref_line(text):
    m = re.search(r"^以西結書\s*([\d:\-–]+)", text, flags=re.M)
    return m.group(1) if m else ""


def scan(corp):
    rows = defaultdict(lambda: defaultdict(lambda: {"n": 0, "files": set()}))
    unclassified, unfound, mismatch, refs = [], [], [], {}
    for n, p in chapters():
        text = p.read_text(encoding="utf8")
        refs[n] = ref_line(text)
        lines = text.splitlines()
        last = None
        i = 0
        while i < len(lines):
            m = re.match(r'^> "(.+)"\s*$', lines[i])
            if m:
                q = m.group(1)
                j = i + 1
                src = ""
                while j < len(lines) and lines[j].startswith(">"):
                    if lines[j].startswith("> —"):
                        src = lines[j]
                        break
                    j += 1
                explicit = None if (not src or "同上" in src) else classify(src)
                if explicit:
                    last = explicit
                pieces = [x for x in re.split(r"\s*(?:\.\.\.|…|\[…\])\s*", q) if norm(x)]
                allhits = None
                for piece in pieces:
                    k = norm(piece)
                    hit = {f for f, c in corp.items() if k in c}
                    allhits = hit if allhits is None else (allhits & hit if allhits & hit else allhits | hit)
                allhits = allhits or set()

                def owner(f):
                    if f.startswith("fathers/"):
                        return "fathers"
                    if f.startswith("morgan"):
                        return "morgan"
                    for w, pre in PREFIX.items():
                        if f.startswith(pre):
                            return w
                    return None
                owners = {owner(f) for f in allhits} - {None}
                who = explicit or last
                if who not in owners:
                    # attribution (explicit or inherited) is not supported by the corpus
                    if explicit:
                        mismatch.append(f"{p.name}:{i + 1} 標為 {explicit}，但該句只在 {sorted(owners) or '（任何來源檔都找不到）'}")
                        who = None
                    elif len(owners) == 1:
                        who = next(iter(owners))
                    else:
                        who = None
                if who is None:
                    (unfound if not allhits else unclassified).append(f"{p.name}:{i + 1}")
                else:
                    files = {f for f in allhits if owner(f) == who}
                    r = rows[who][n]
                    r["n"] += 1
                    r["files"] |= files
                    last = who
                i = j
            i += 1
    return rows, unclassified, unfound, mismatch, refs


def pick(files, who, n):
    """The file for this chapter's own Ezekiel chapter(s) first, else the lowest-numbered hit."""
    return sorted(files)[:3]


def table(who, rows, refs):
    out = ["| 章 | 以西結書 | 逐字引文（條） | 核對來源檔（`.sources/`） |",
           "|--------|----------------|----------------|------------------------------------------------------|"]
    tot_n = tot_c = 0
    for n in sorted(rows[who]):
        r = rows[who][n]
        files = "、".join(f"`{f}`" for f in pick(r["files"], who, n))
        more = f"（另 {len(r['files']) - 3} 檔含同文）" if len(r["files"]) > 3 else ""
        out.append(f"| 第{n}章 | {refs[n]} | {r['n']} | {files}{more} |")
        tot_n += r["n"]
        tot_c += 1
    return "\n".join(out), tot_c, tot_n


def _head(p):
    h = {}
    for line in p.read_text(encoding="utf8").split("\n---\n", 1)[0].splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            h[k.strip()] = v.strip()
    return h


def hymn_table():
    # bullet list, not a table: URLs in table cells cannot break and overflow the page
    out = []
    for p in sorted((SRC / "hymns").glob("[0-9][0-9]-*.txt")):
        h = _head(p)
        out.append(f"- 第{int(p.name[:2])}章 · {h.get('HYMN', '')}；{h.get('AUTHOR', '')}。取自 {h.get('SOURCE', '')}：<{h.get('URL', '')}>")
    return "\n".join(out)


def father_table():
    out = []
    for p in sorted((SRC / "fathers").glob("[0-9]*.txt")):
        h = _head(p)
        out.append(f"- `{p.name}` · {h.get('SOURCE', '')}（以西結書 {h.get('EZEKIEL', '')}）：<{h.get('URL', '')}>")
    return "\n".join(out)


def build():
    corp = load_corpus()
    rows, unclassified, unfound, mismatch, refs = scan(corp)
    parts = []
    totals = {}
    # Sections in the order of WHO, numbered 一..
    nums = "一二三四五六七八九十"
    sec = 0
    for who, label in WHO.items():
        if not rows[who]:
            continue
        t, c, n = table(who, rows, refs)
        totals[who] = (c, n)
        head = f"## {nums[sec]}、{label}"
        sec += 1
        if who == "morgan":
            head = f"## {nums[sec - 1]}、摩根（G. Campbell Morgan），*The Analyzed Bible*，以西結書分段大綱"
        note = {
            "fathers": "教父段落由協助編輯的 AI 代理從 newadvent.org 的 ANF／NPNF 印本逐字抓取，每檔已與重新下載的頁面逐字比對（檔頭有作者、版本、網址）；共收集 42 段，各章只引其中與本章相關者。檔內夾有網頁所加的經文交叉參照標記（如「Ezekiel 33:11」），引用時已用省略號跳過，不當作教父原文。",
            "calvin": "取自 biblehub.com 的 *Calvin's Commentaries* 章頁（只有以西結書第 1–20 章）。第 21–48 章沒有加爾文，書中不引。",
            "henry": "取自 biblehub.com 的 *Matthew Henry's Commentary on the Whole Bible*（`mhcw`）章頁全文。",
            "kd": "取自 biblehub.com 的公有領域全文，依章拆成 `kad-NN.txt`；行文中夾的希伯來文與腳註不引，引文均取其英文行文。",
            "expositors": "司金納的《解經者聖經》以專題文章寫成，biblehub 把同一篇文章放在相鄰幾章的檔裏（例如 `expositors-12`／`-17`／`-19`），所以「含同文」的檔不止一個；本表列出前三個。",
            "cambridge": "取自 biblehub.com 的 *Cambridge Bible for Schools and Colleges* 章頁全文。",
            "pulpit": "`pulpit-NN.txt` 多為 biblehub 章頁上的逐節「摘錄」，部分在句子中間被截斷；本書只引完整出現在摘錄內、有頭有尾的句子。",
            "jfb": "取自 biblehub.com 的 JFB 章頁全文。",
            "gill": "`gill-NN.txt` 為 biblehub 章頁上的逐節摘錄，部分在句子中間被截斷；本書只引完整的句子，多數處只以釋義方式提及並註明檔名。",
            "morgan": "《分析聖經》（archive.org `bwb_T3-BNU-740` 的 OCR）是**分段大綱與短評，不是逐章講章**；檔內有頁碼與頁眉夾雜。本書只引描述本章的短句，標「分析聖經·以西結書」，不寫成論某節。",
        }[who]
        parts.append(f"{head}\n\n{note}\n\n{t}\n\n合計：{c} 章、{n} 條逐字引文。\n")
    return "\n---\n\n".join(parts), totals, unclassified, unfound, mismatch


HEAD = """---
title: 以西結書研讀
subtitle: Ezekiel Deep Study
author: PubHub 三書精讀系統
date: 2026年10月
publisher: 三書精讀出版系統
---

# 附錄：引用出處總表 (Appendix: Reference Ledger)

各章「歷代注疏」一節的體例說明指向本附錄。本附錄回答三件事：每條引文取自哪裏、如何核對、哪些地方只做到這一步為止。下列各表的章次與條數由 `scripts/gen-ezekiel-ledger.py` 從各章原文與 `.sources/` 反向讀出，並由 `scripts/check-citation-ledger.py` 對照，不是手寫的記憶。

---

"""

TAIL = """
---

## {n1}、麥克阿瑟——本書沒有逐字引文

麥克阿瑟沒有以西結書的逐節講道系列（gty.org 的站點地圖與 Monergism 的麥克阿瑟系列清單都查無）。本書沒有任何一條麥克阿瑟的逐字引文，也不以他人冒充，更不憑記憶引他。

---

## {n2}、老弟兄——本書沒有第一手引文

本項目沒有老弟兄講以西結書的第一手錄影或筆記。各章「老弟兄查經」一節是依 ask-elder-wong 方法所作的**方法性撮述**，不加引號、不宣稱是逐字語錄；加引號的老弟兄語句只有 `.claude/skills/ask-elder-wong/references/voice.md` 白名單內的句子。倉庫中老弟兄約翰福音材料裏確實出現的以西結連結，各處已註明路徑與行數，並標示為倉庫材料，而不是他講過以西結書。

---

## {n3}、配詩的出處

每章一節配詩，歌詞由協助編輯的 AI 代理從印本或公有領域歌詞網站逐字抓取（一節）；中譯由撰寫各章的 AI 代理所作。作者與年份依來源所印，因此與一般通行的說法偶有出入（如 Kelly 1804、Watts 1709、Bernard of Morlaix），以下表為準。

{hymns}

---

## {n4}、教父段落清單

{fathers}

---

## {n5}、聖經版本與核對方式

- **中文：**和合本（1919）。以 fhl（bible.fhl.net，`unv`）為底，專有名詞與字形在 ai-eden 與 cnbible 兩者一致處從舊形（推羅、撒瑪利亞、利巴嫩、大馬色、毗、呂彼亞、亞拉伯、約但、燒燬、火燄、可作）；經文區由 `scripts/gen-ezekiel-scripture.py` 自來源檔印出，章內經文與 `.sources/units/` 逐字一致，由 `.sources/check_chapter.py` 逐章核對。
- **一個刻意的字形例外：**47:3-5 的「蹚」字。ai-eden 與 cnbible 的和合本欄都作一個罕見字形，本書印刷字體沒有它，故取 fhl 的「蹚」。
- **三節來源缺陷：**16:57、18:11、39:27 三節，和合本在 fhl、ai-eden、cnbible 三個來源裏都只有一個字母 `a`，內容已併入上一節；經文區在這三節印出一行說明，不自行補寫和合本字句。NASB 這三節俱全。
- **英文：**NASB 1995。取自 biblehub.com 的 NASB 章頁，因為 ai-eden 的 NASB 檔在兩處與 1995 版不符（11:3 為 1977 措辭，13:15 字串錯亂）。
- **希伯來文：**Sefaria 的 JPS 希伯來底本（Miqra according to the Masorah），去掉讀經符號、保留母音；原文研讀表的字形須能在 `.sources/hebrew/ezekiel-he.tsv` 中找到。希伯來文 21:1-37 的節號與和合本不同（希伯來 21:1-5 = 和合本 20:45-49），表內以和合本節號為準。
- **跨卷經文：**一律由 `.sources/xref.py`（ai-eden，有快取）逐節印出，只做「裡」→「裏」一項改動。
- **注疏引文：**每條英文引文都是 `.sources/commentary/` 或 `.sources/fathers/` 內檔案的逐字子字串（忽略大小寫與標點），由 `.sources/check_quotes.py` 逐條核對；同一句全書只引一次，由 `QUOTE-LEDGER.tsv` 與全書掃描雙重把關。

---

## {n6}、機器核對現況

- 逐章驗證：`.sources/check_chapter.py` 對 34 章的結果為 0 errors（YAML、十一節順序、經文區、引文子字串、座標與鑰詞、「你看見…了嗎」等）。**通過它只證明形式正確，不證明內容為真。**
- 全書掃描：{dupes}
- 本表的條數由腳本自各章讀出；分類無法歸屬者 {unclassified} 條，在來源檔中找不到者 {unfound} 條。
- 歷代注疏中文譯文是編者所譯，沒有另行校對。
- 配詩中，第 4、8、9、15、17、26、27、28 章只有單一來源可對；第 31 章另有一頁底本不明的同文；其餘已與第二來源比對。

---

## {n7}、仍未完成

以下各項是誠實的缺口，不是已完成事項：

1. 已執行一輪獨立校對：九位沒有看過本書的 AI 校對者各自向原始來源重新取證，共提出 A 級（錯誤）24 條、B 級（無法查證或過度斷言）76 條、C 級（錯字、文風等）116 條；修訂者逐條向原始來源重新查證後才修改，個別條目經查證不成立者未改。**尚未有人類校對者通讀全書**，這是仍未完成的最重要一項。
2. 各章字數偏多（多數章在 35–60 KB 之間），尚未做精簡輪；各章中同一個論點重複 3–13 次，校對者已記錄，尚未處理。
3. 配詩第 16 章第四行「Son of man」前是否有「O」，兩個來源不一致，待查 1903 年原版。
4. 40–48 章的解釋傳統（字面、象徵、基督裏應驗）、28:11-19 的所指、38–39 章的歌革，本書一律並陳而不定案；這是刻意的，需要作者決定的只是是否在日後的版本加上本書自己的立場。
5. 老弟兄對以西結書沒有第一手材料；「老弟兄查經」各節是方法性撮述。
"""


def main():
    body, totals, unclassified, unfound, mismatch = build()
    # duplicate scan
    seen = defaultdict(set)
    for n, p in chapters():
        for line in p.read_text(encoding="utf8").splitlines():
            m = re.match(r'^> "(.+)"\s*$', line)
            if m:
                for piece in re.split(r"\s*(?:\.\.\.|…|\[…\])\s*", m.group(1)):
                    k = norm(piece)
                    if len(k) > 40:
                        seen[k[:60]].add(n)
    dupes = [k for k, v in seen.items() if len(v) > 1]
    dtxt = (f"同一句注疏出現在兩章以上者 {len(dupes)} 處。" if dupes else "同一句注疏跨章重複者 0 處（對 `> \"…\"` 引文的前 60 個字元逐條比對）。")
    k = len([w for w in WHO if totals.get(w)])
    base = k  # sections already numbered 一..k
    names = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十"]
    sec = [names[base + i] for i in range(7)]
    tail = TAIL.format(n1=sec[0], n2=sec[1], n3=sec[2], n4=sec[3], n5=sec[4], n6=sec[5], n7=sec[6],
                       hymns=hymn_table(), fathers=father_table(), dupes=dtxt,
                       unclassified=len(unclassified), unfound=len(unfound))
    text = HEAD + body + tail
    total_quotes = sum(n for c, n in totals.values())
    summary = "\n".join(f"- {WHO[w][:20]}…：{c} 章、{n} 條" for w, (c, n) in totals.items())
    if "--write" in sys.argv:
        OUT.write_text(text, encoding="utf-8")
        print(f"wrote {OUT.name}: {total_quotes} verbatim quotes; unclassified={len(unclassified)} unfound={len(unfound)} dupes={len(dupes)}")
        print(summary)
        for u in unclassified + unfound:
            print("  !", u)
        for u in mismatch:
            print("  MISMATCH", u)
    else:
        print(text)


if __name__ == "__main__":
    main()
