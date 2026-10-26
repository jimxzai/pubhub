#!/usr/bin/env python3
"""Generate the Ecclesiastes volume's citation ledger (99-appendix-references.md) from the book's own text.

The ledger is the honesty account for the promise 「不編造一段出處」. A hand-kept
ledger drifts from the chapters (Luke: declared zero Morgan quotes, carried 29),
so every count and every source line below is read back out of the chapter files.
Model: scripts/gen-nehemiah-ledger.py.

Usage:  python3 scripts/gen-ecclesiastes-ledger.py --write
        python3 scripts/gen-ecclesiastes-ledger.py          # print
"""
import re
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "bible" / "ecclesiastes"
OUT = BOOK / "99-appendix-references.md"

WHO = OrderedDict([
    ("henry", "馬太·亨利（Matthew Henry），*Commentary on the Whole Bible*，傳道書卷（原著 1706-1721）"),
    ("bridges", "Charles Bridges，*An Exposition of the Book of Ecclesiastes*（1860）"),
    ("morgan", "摩根（G. Campbell Morgan），*The Message of Ecclesiastes*，載 *Living Messages of the Books of the Bible*, Old Testament（1912）"),
    ("gregory", "Gregory Thaumaturgus（傳為其作），*A Metaphrase of the Book of Ecclesiastes*，載 *Ante-Nicene Fathers* 第六冊"),
    ("macarthur", "麥克阿瑟（John MacArthur），《研讀本聖經》導論與 gty.org 講章、部落格"),
    ("talmud", "巴比倫塔木德 Shabbat 30b（William Davidson Edition 英譯，Sefaria.org，CC-BY-NC）"),
])

SOURCE_FILE = {
    "henry": "`sources/commentary/henry/henry-chNN.txt`、`henry-intro.txt`（ccel.org，mhc3 的 Ec 各頁；CCEL 頁碼比章次多一頁，第 12 章取 xiii 頁）",
    "bridges": "`sources/commentary/bridges/bridges.txt`（monergism 的 PDF 文字，已正規化；章界依 “CHAPTER N”）",
    "morgan": "`sources/commentary/morgan-message-of-ecclesiastes.txt`（*Living Messages of the Books of the Bible*, Old Testament 的 OCR 文字，頁碼取自頁眉，pp. 57-69）",
    "gregory": "`sources/commentary/fathers/gregory.txt`（ANF 6 英譯；連同英譯編者的註）",
    "macarthur": "`sources/commentary/gty/`：MSB21 導論、講章 70-2〈Bible Questions and Answers, Part 30〉、53-15〈Work: A Noble Christian Duty, Part 2〉、90-42〈Investing in Eternity, Part 2〉、部落格〈Life Under the Sun〉（B210118）",
    "talmud": "`sources/commentary/talmud/shabbat-30b.txt`（Sefaria 的 Bavli Shabbat 30b 英譯）",
}


def classify(src):
    for k, n in [("Matthew Henry", "henry"), ("Charles Bridges", "bridges"), ("G. Campbell Morgan", "morgan"),
                 ("Gregory Thaumaturgus", "gregory"), ("John MacArthur", "macarthur"),
                 ("Talmud", "talmud")]:
        if k in src:
            return n
    return None


def chapters():
    return [(int(p.name[:2]), p) for p in sorted(BOOK.glob("[01][0-9]-*.md")) if 1 <= int(p.name[:2]) <= 12]


def scan():
    rows = defaultdict(lambda: defaultdict(list))
    ref = {}
    for n, p in chapters():
        t = p.read_text(encoding="utf-8")
        m = re.search(r"^傳道書\s*([\d:\-–]+)", t, re.M)
        ref[n] = m.group(1) if m else ""
        for m in re.finditer(r'^> "(.+?)"\s*\n> — (.+)$', t, re.M):
            who = classify(m.group(2))
            if who:
                rows[who][n].append(m.group(2).strip())
    return rows, ref


def table(who, rows, ref):
    head = ["| 章 | 傳道書 | 逐字引文（條） | 出處行（各條，本書實印） |",
            "|--------|----------------|----------------|------------------------------------------------------|"]
    body = []
    for n in sorted(rows[who]):
        srcs = rows[who][n]
        distinct = list(OrderedDict.fromkeys(re.sub(r"\*", "", s) for s in srcs))
        body.append(f"| 第{n}章 | {ref[n]} | {len(srcs)} | " + "；".join(distinct) + " |")
    total = sum(len(v) for v in rows[who].values())
    return "\n".join(head + body), total


def build():
    rows, ref = scan()
    total_all = sum(len(v) for w in rows.values() for v in w.values())
    n_in = 0
    for n, p in chapters():
        t = p.read_text(encoding="utf-8")
        m = re.search(r"^## 歷代注疏.*?(?=^## )", t, re.M | re.S)
        if m:
            n_in += len(re.findall(r'^> "(.+?)"\s*\n> — (.+)$', m.group(0), re.M))
    L = []
    L.append(f"""---
title: 傳道書研讀
subtitle: Ecclesiastes Deep Study
author: PubHub 三書精讀系統
date: 2026年10月
publisher: 三書精讀出版系統
---

# 附錄：引用出處總表 (Appendix: Reference Ledger)

各章「歷代注疏」一節的體例說明指向本附錄。本附錄回答三件事：每條引文取自哪裏、如何核對、哪些地方只做到這一步為止。下列各表的章次與條數由 `scripts/gen-ecclesiastes-ledger.py` 直接從各章原文讀出，不是手寫的記憶；`scripts/check-citation-ledger.py` 再把它與各章對照。

全書各章帶引號並附「— 作者，書名」出處行的逐字引文共 **{total_all}** 條（其中 {n_in} 條在〈歷代注疏〉一節，其餘在〈背景〉等處）。

---""")
    sections = [("henry", "一"), ("bridges", "二"), ("morgan", "三"), ("gregory", "四"), ("macarthur", "五"), ("talmud", "六")]
    for who, num in sections:
        tbl, total = table(who, rows, ref)
        short = {"henry": "亨利", "bridges": "Bridges", "morgan": "摩根", "gregory": "Gregory Thaumaturgus",
                 "macarthur": "麥克阿瑟", "talmud": "巴比倫塔木德"}[who]
        L.append(f"\n## {num}、{short}：{WHO[who]}\n")
        L.append(f"來源檔：{SOURCE_FILE[who]}。本書引用 **{total}** 條，列如下；每條都是該來源檔的逐字子字串（見「七、機器核對現況」）。\n")
        if who == "morgan":
            L.append("摩根只有一篇全書概觀，並非逐章逐節的注釋。凡本書引他，只標頁碼；他的話不被寫成論某一章某一節的專論。以下各章的逐字引文：\n")
        if who == "macarthur":
            L.append("本書沒有麥克阿瑟的傳道書逐節講道（gty.org 站點地圖裏沒有以傳道書為題的講道系列）；本書引的是《研讀本聖經》導論、部落格〈Life Under the Sun〉，以及幾篇主題不在傳道書、卻引到傳道書的講章。以下各章的逐字引文：\n")
        if who == "gregory":
            L.append("本書引 Gregory 時，作者歸屬依 ANF 的標示（傳為 Gregory Thaumaturgus 之作），並參看 ANF 英譯編者的註；本書不替這個歸屬作斷語。以下各章的逐字引文：\n")
        if who == "talmud":
            L.append("塔木德的引文是猶太傳統對這卷書的讀法，不是傳道書自己的話；本書引它，作兩種用處：這卷書險些被收起來的史料，與它對 1:3「日光之下」的讀法。以下各章的逐字引文：\n")
        L.append(tbl)
    L.append("""
---

## 七、機器核對現況（誠實記錄）

**注疏引文。** 本書各章歸屬注疏者的逐字引文，以 `verify-citations.py` 對合併語料（`sources/commentary/corpus-all.txt`：亨利、Bridges、摩根、Gregory、麥克阿瑟、塔木德）逐條核對，結果為逐字吻合（OK）全部，DRIFT 0，MISS 0。

**講章編號。** `verify-sermon-quotes.py` 對有「sermon CODE」格式的 10 條講章引文，全部在該講章自己的逐字稿裏找到。其餘幾條（《研讀本聖經》導論與部落格）沒有講章編號，由 `verify-citations.py` 對語料核對。

**行文中的經文引句。** `verify-prose-citations.py`（「引號＋出處」的格式）與本書自寫的 `sources/verify_xref_quotes.py`（出處在引號前、後、或同一行任何位置），兩者都已檢查；凡引號內不是和合本逐字的，一律改為不加引號的轉述，或改成逐字。**本書的規則：「」只用於和合本逐字。**

**章節與骨幹。** `check-book-spine.py`：骨幹章、分卷扉頁、各章座標、章末回到基督，四項皆過。

---

## 八、聖經版本與核對方式

**中文：和合本（CUV）。** 底本取信望愛（fhl）的和合本，專有名詞與代名詞的取捨再以 ai-eden.com（本專案標準來源）與 cnbible.com 對校。

- **2:10**：fhl 作「不給它的」，依 ai-eden 改為「不給他的」；**7:26**：fhl 作「她」，依 ai-eden 改為「他」（同路得記 2:14 的先例）。
- **7:1**：ai-eden 自己有「美好的的膏油」重字，本書採 fhl。
- **7:27-28**：fhl、ai-eden、cnbible 三個和合本來源都把兩節併在 7:27，7:28 只是占位符；本書無法從任何來源拆開，所以經文區印作 ^27-28^，NASB 欄仍分 27 與 28 兩節。
- 經文區塊一律由 `sources/scripture/inject_scripture.py` 從 `cuv.tsv` 與 `nasb1995.tsv` 注入，沒有人手打一節經文。

**英文：NASB 1995。** 取自 biblehub.com 各章頁（斜體＝譯者補字，印為 *斜體*）。

**希伯來文與字頻。** 字頻與詞形取自 Sefaria 所載《Miqra according to the Masorah》（MAM，以亞勒坡抄本為本，CC-BY-SA；本地 `sources/hebrew/hebrew.tsv`，按英文節數計，計數腳本 `count.py`）。

- **虛空（הֶבֶל）38 次**：1:2 五次、12:8 三次，框架共 8 次，書體 30 次。麥克阿瑟的導論稱 37 次；差一的原因無從確定（他沒有列出所數的節；可能是詞形或 1:2 重複的計法不同）。本書從上述希伯來文逐字實算，書中一律用 38。
- **日光之下 29 次**，全在 1:3 至 10:5；亨利稱 28 次。差一的原因同樣無從確定；本書一律用 29。
- 其他字頻（捕風 9、神 40、耶和華 0、我見 18 等）見〈虛空的軌跡〉，皆由 `count.py` 重現。

**七十士譯本與其他傳統。** 提到 LXX 之處（12:1 的 κτίσαντα、12:11 的 ποιμένος ἑνός、3:11 的 αἰών、羅 8:20 的 ματαιότης 與傳道書 LXX 的同一個字）都是字形的對照，本書不以此立論；3:11 的 αἰών（LXX）與英王欽定本的 “world” 是翻譯傳統的差異，各章說明。2:25 的希伯來文本、七十士譯本、和合本與 NASB 讀法各有出入，第 2 章說明。

**聖詩。** 十二首全部取自 Wikisource 所載 *The Army and Navy Hymnal*（1920，公有領域）及其他公有領域來源，英文逐字照來源所印，中譯為編者所作；出處行只寫來源實印。

---

## 九、詮釋的張力（本書並陳，不調和）

1. **「虛空」的判語是誰的話。** Bridges 與亨利把全書讀為悔改的所羅門的話，神的話；摩根與麥克阿瑟把 1-11 章讀為沒有神的人生觀的紀錄，12 章才是智慧的陳述；Gregory 把 9:1-10 讀為愚昧人的思想。
2. **3:21 與 12:7。** 3:21 是問句，12:7 是陳述；本書並讀，不替 3:21 補答案。
3. **11:9 的「行你心所願行的」。** 命令、反話、傳道者自己的話，三種讀法並陳。
4. **12:11 的牧者。** Bridges 讀為主耶穌；Gregory 說的是一位好的牧者和教師。
5. **12:2-7 的圖。** 亨利與 Bridges 讀為衰老，Gregory 讀為神那大而可畏的日子；本書不選。

---

## 十、本書沒有的其他聲音

- **老弟兄**：沒有講傳道書的第一手教導；本書只用他的方法，不引他的話。
- **麥克阿瑟**：沒有傳道書逐節講道。
- **加爾文**：沒有寫過傳道書註釋。
- **其他教父與改教家**：沒有可查證的文本，不編造補位。

---

## 十一、仍未完成

1. **沒有人類審稿者。** 全書自評與機器核對，沒有另一位讀者逐章通讀。
2. **摩根的頁碼是推定的，誤差約一頁。** 由 OCR 稿的頁眉記號推出，沒有對照實體書頁。
3. **亨利與 Bridges 的章節對應**：取自檔名與章界標記，沒有對照實體書頁。
4. **塔木德引文**：是 Sefaria 的英譯，沒有對照阿拉米文原文。
5. **沒有第二個和合本版本對 7:27-28 的拆分**：本書如實併印，不另行推定。
""")
    return "\n".join(L)


def main():
    text = build()
    if "--write" in sys.argv:
        OUT.write_text(text + "\n", encoding="utf-8")
        print(f"wrote {OUT.name} ({len(text)} chars)")
    else:
        print(text)


if __name__ == "__main__":
    main()
