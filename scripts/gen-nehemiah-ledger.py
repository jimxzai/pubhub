#!/usr/bin/env python3
"""Generate the Nehemiah volume's citation ledger (99-appendix-references.md) from the book's own text.

The ledger is the honesty account for the promise 「不編造一段出處」. A hand-kept
ledger drifts from the chapters (Luke: declared zero Morgan quotes, carried 29),
so every count and every source line below is read back out of the chapter files.

Usage:  python3 scripts/gen-nehemiah-ledger.py --write
        python3 scripts/gen-nehemiah-ledger.py          # print
"""
import re
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "bible" / "nehemiah"
OUT = BOOK / "99-appendix-references.md"

WHO = OrderedDict([
    ("henry", ("Matthew Henry", "馬太·亨利（Matthew Henry），*Commentary on the Whole Bible*，尼希米記卷（原著 1706-1721）")),
    ("adeney", ("Walter F. Adeney", "阿德尼（Walter F. Adeney），*Ezra, Nehemiah, and Esther*（*The Expositor's Bible*，1893）")),
    ("kd", ("Keil", "凱爾與德利奇（C. F. Keil & F. Delitzsch），*The Books of Ezra, Nehemiah, and Esther*（1873 英譯本）")),
    ("morgan", ("G. Campbell Morgan", "摩根（G. Campbell Morgan），*The Message of Nehemiah*，載 *Living Messages of the Books of the Bible*, Old Testament（1912）")),
    ("macarthur", ("John MacArthur", "麥克阿瑟（John MacArthur），gty.org 講章與部落格")),
    ("fathers", ("", "教父三位：耶柔米、蘇比丟·西弗勒、耶路撒冷的區利羅")),
])
FATHER_KEYS = ["Jerome", "Sulpitius", "Cyril"]

SOURCE_FILE = {
    "henry": "`sources/commentary/henry/neh-N.txt`（ccel.org，*Commentary on the Whole Bible* vol. 2；檔無節號，整章全文）",
    "adeney": "`sources/commentary/adeney/neh-*.txt`（ccel.org，十六個檔，章次 XV-XXX）",
    "kd": "`sources/commentary/kd-raw.txt`（PDF 的 OCR 文字，雜訊多）",
    "morgan": "`sources/commentary/morgan-message-of-nehemiah.txt`（archive.org *Living Messages of the Books of the Bible* 的 OCR，頁碼取自頁眉記號，pp. 251-265）",
    "macarthur": "`sources/commentary/gty/`：80-197、B120524（另三篇 70-22、90-335、90-463 本書沒有引用）",
    "fathers": "`sources/commentary/jerome-ep53-s8.txt`、`sulpitius-sh-2-11.txt`、`fathers-raw/npnf207.txt`（NPNF 公有領域英譯）",
}


def classify(src):
    for k, n in [("Matthew Henry", "henry"), ("Walter F. Adeney", "adeney"), ("Keil", "kd"),
                 ("G. Campbell Morgan", "morgan"), ("John MacArthur", "macarthur")]:
        if k in src:
            return n
    if any(f in src for f in FATHER_KEYS):
        return "fathers"
    return None


def chapters():
    out = []
    for p in sorted(BOOK.glob("[01][0-9]-*.md")):
        n = int(p.name[:2])
        if 1 <= n <= 13:
            out.append((n, p))
    return out


def scan():
    rows = defaultdict(lambda: defaultdict(list))  # who -> ch -> [source lines]
    ref = {}
    for n, p in chapters():
        t = p.read_text(encoding="utf-8")
        m = re.search(r"^尼希米記\s*([\d:\-–]+)", t, re.M)
        ref[n] = m.group(1) if m else ""
        for m in re.finditer(r'^> "(.+?)"\s*\n> — (.+)$', t, re.M):
            who = classify(m.group(2))
            if who:
                rows[who][n].append(m.group(2).strip())
    return rows, ref


def short(src):
    src = re.sub(r"\*", "", src)
    return src


def table(who, rows, ref):
    head = ["| 章 | 尼希米記 | 逐字引文（條） | 出處行（各條，本書實印） |",
            "|--------|----------------|----------------|------------------------------------------------------|"]
    body = []
    for n in sorted(rows[who]):
        srcs = rows[who][n]
        distinct = list(OrderedDict.fromkeys(short(s) for s in srcs))
        body.append(f"| 第{n}章 | {ref[n]} | {len(srcs)} | " + "；".join(distinct) + " |")
    total = sum(len(v) for v in rows[who].values())
    return "\n".join(head + body), total


def build():
    rows, ref = scan()
    L = []
    L.append("""---
title: 尼希米記研讀
subtitle: Nehemiah Deep Study
author: PubHub 三書精讀系統
date: 2026年10月
publisher: 三書精讀出版系統
---

# 附錄：引用出處總表 (Appendix: Reference Ledger)

各章「歷代注疏」一節的體例說明指向本附錄。本附錄回答三件事：每條引文取自哪裏、如何核對、哪些地方只做到這一步為止。下列各表的章次與條數由 `scripts/gen-nehemiah-ledger.py` 直接從各章原文讀出，不是手寫的記憶；`scripts/check-citation-ledger.py` 再把它與各章對照。

全書帶引號並附「— 作者，書名」出處行的逐字引文共 **%d** 條（其中 %d 條在〈歷代注疏〉一節，其餘在〈背景〉〈全經連線〉等處）。

---""" % (sum(len(v) for w in rows.values() for v in w.values()),
         0))
    # patch the second number below once we know it
    sections = [("henry", "一"), ("adeney", "二"), ("kd", "三"), ("morgan", "四"), ("macarthur", "五"), ("fathers", "六")]
    for who, num in sections:
        name = WHO[who][1]
        tbl, total = table(who, rows, ref)
        L.append(f"\n## {num}、{name}\n")
        L.append(f"來源檔：{SOURCE_FILE[who]}。本書引用 **{total}** 條，列如下；每條都是該來源檔的逐字子字串（見「七、機器核對現況」）。\n")
        if who == "morgan":
            L.append("摩根的 OCR 稿只有一篇概觀（約 pp. 251-265），並非逐章逐節的注釋。凡本書引他，只標頁碼；他的話**不**被寫成論某一章某一節的專論。以下各章的逐字引文：\n")
        if who == "macarthur":
            L.append("本書沒有麥克阿瑟的尼希米記逐節講道；以下五條，一條出自部落格〈Leadership Is Work〉（B120524，Grace to You，2012-05-24），其餘出自講章 80-197〈Characteristics of an Effective Leader〉（Acts 27，1998-11-15）中順帶提到尼希米之處。第 3 章的引文前，另有一句說明：該講章把差遣尼希米的詔命說成出自古列，經文是亞達薛西（尼 2:1），本書不採。以下各章的逐字引文：\n")
        L.append(tbl)
        if who == "kd":
            L.append("\n凱爾與德利奇的 OCR 稿雜訊很多，本書只在需要原文語意時才引，共 %d 條；其中有 3 條放在合併標題「十九世紀（Walter F. Adeney；Keil & Delitzsch）」之下，2 條放在第 12 章其他小節，各條出處行寫明作者。" % total)
        if who == "adeney":
            L.append("\n第 3 章〈十九世紀〉一節另有 1 條亨利的逐字引文（論 3:12 的「女兒們」），出處行寫的是亨利，已計入「一」。")
    L.append("""
---

## 七、機器核對現況（誠實記錄）

**注疏引文。** 本書各章全部 96 條歸屬注疏者的逐字引文（卷首框架檔另有數條，見附），已逐條與該作者自己的來源檔比對：把引文與來源檔都只留字母之後，引文必為來源檔的連續子字串。這個折法不怕 OCR 的斷詞、頁碼與頁眉，但它比 `verify-citations.py` 的逐字比對寬鬆，所以另以 `verify-citations.py`（先經 `normalize-ocr-source.py`）逐一核對各位作者在〈歷代注疏〉小節下的引文，結果為：亨利 30 條、麥克阿瑟 5 條、教父 5 條全部逐字吻合（OK）；摩根 14 條全部逐字吻合；阿德尼／凱爾與德利奇各條，除 1 條為 OCR 斷詞造成的 OK-OCR 外，皆逐字吻合；DRIFT 0，MISS 0。一條摩根引文原本橫跨頁眉（「… replied with THE MESSAGE OF NEHEMIAH 263 fine satire …」），機器判為 DRIFT，已改為只引頁眉之後的完整半句。

**經文。** 見「八、聖經版本與核對方式」。

**行文中的經文引句。** `check-prose-scripture-quotes.py` 比對每條行文引句與該章印出的經文；跨章引句（15 條，如第 6 章引 9:26）本機以全書 `cuv.tsv` 另行比對，皆吻合。`verify-prose-citations.py` 對全書 214 個「引號＋出處」檢出 15 項 MISS，逐一檢視：4 項是真缺陷，已修正（哈 2:4 誤作「義人必因信得生」，原文為「惟義人因信得生」；尼 10:39 引句漏「我們就……我們」；申 12:11 的「立為我名的居所」是尼 1:9 的改寫，原文作「立為他名的居所」；但 9:4 的引句混入了尼 1:5 的「你」）；另 2 項是檢查器把引句與相鄰的另一個出處配成一對（尼 1:8-9 與申 30 的並列、第 13 章後的對照表），已改寫句式避免誤配；其餘 9 項是檢查器的誤報（比對底本是未經本書正規化的 FHL 原文，帶有「─」與全形空格，或引句與相鄰的另一個出處被配成了一對）。

**跨書經文引句的第二來源。** 行文中「引句＋（書 章:節）」格式的跨書引句 72 條，另以 ai-eden.com 的和合本逐條比對（原本只有 fhl 單一來源）：67 條逐字相同；5 條只差字形（路 19:41 它／他、來 4:16 地／的、約 18:11 吧／罷、路 24:32 嗎／麼、路 23:42 啊／阿），與經文區同一政策（助詞與代名詞從 fhl／cnbible 的現代字形），不改。「章節在引句前」的寫法不在這個比對範圍內，那一類只經 fhl 與人工核對。

**講章編號。** `verify-sermon-quotes.py` 對 80-197 的 3 條引文全數核對吻合；對 B120524（部落格，無「sermon CODE」格式）的 2 條無法判讀，改以 `verify-citations.py` 對 `gty/B120524.txt` 核對，吻合。

**重複引文。** 各章 96 條引文，無一條在兩章重複；卷首框架檔的引文也不與各章重複（曾有 3 句摩根引文被三章各引一次，已換成各章各自的段落）。

**章節與骨幹。** `check-book-spine.py`：骨幹章、分卷扉頁、各章座標、章末回到基督，四項皆過。

---

## 八、聖經版本與核對方式

**中文：和合本（CUV）。** 底本取信望愛（fhl）的和合本，再與兩個獨立來源逐節對校：ai-eden.com（本專案標準來源，API 取回）與 cnbible.com（現代標點和合本）。

- fhl 與 cnbible 在 256 節有出入，其中 82 節超出標點與空格，多為字形與慣用詞（甚麼／什麼、貴冑／貴胄、橫樑／橫梁、毘／毗）。
- fhl 與 ai-eden 在 64 節有出入（不計標點）：其中 34 節只差「裏／裡」（本書各書一律印「裏」，不改），其餘 30 節是字詞差異；另 342 節完全相同。
- 本書改動 fhl 底本的 25 節：**ai-eden 與 cnbible 兩者都用另一種寫法者，從那一種**（毘→毗、橫樑→橫梁、泰爾→推羅〔13:16〕、米該亞→米該雅〔12:41〕、6:1 多出的「的」）；**專有名詞由 ai-eden 定案**（阿拉伯→亞拉伯〔2:19；4:7；6:1〕、撒馬利亞→撒瑪利亞〔4:2〕、西奈→西乃〔9:13〕）。「嗎／麼」「吧／罷」兩組助詞，cnbible 與 fhl 同形，且全庫各書印「嗎」，**不改**。「做／作」的用法 fhl 與 ai-eden 全部相同，不改。
- **來源缺陷一處**：fhl 與 ai-eden 都把 12:28 與 12:29 併成一節，12:29 只留一個字母 a；本書依 cnbible 在「伯·吉甲，」之後分開（12:28／12:29）。
- 全部改動由 `books/bible/nehemiah/sources/scripture/apply_name_fixes.py` 重現，未改的 fhl 底本保存為 `cuv.fhl-base.tsv`。經文區塊一律由 `inject_scripture.py` / `reinject.py` 從 `cuv.tsv` 與 `nasb1995.tsv` 注入，沒有人手打一節經文。

**英文：NASB 1995。** 取自 biblehub.com 各章頁（斜體＝譯者補字，印為 *斜體*）。與 ai-eden.com 的 NASB 逐節比對：406 節中 405 節相同；唯一不同的 12:46，ai-eden 的文字錯亂（混入 10:34 的片段 “cast lots for the supply of wood”），biblehub 為正確，本書從 biblehub。

**希伯來文。** 字頻與詞形取自 Sefaria 所載 *Miqra according to the Masorah*（本地 `hebrew.tsv`，按英文節數計）。注意：`hebrew.tsv` 的第 7 章用希伯來文節號，只有 72 節，缺和合本 7:68（馬、騾的數目），第 7 章引用時已另行對照。

**聖詩。** 十三首全部取自 Wikisource 所載 *The Army and Navy Hymnal*（1920，公有領域），英文逐字照來源所印，中譯為編者所作；出處行只寫來源實印。

---

## 九、本書沒有的其他聲音

- **老弟兄**：沒有講尼希米記的第一手教導；資料庫裏的《尼希米記·逐卷查經》是風格摹寫，本書不引。
- **麥克阿瑟**：沒有尼希米記逐節講道。
- **加爾文**：沒有寫過尼希米記註釋。
- **教父**：只有耶柔米《書信五十三》論以斯拉與尼希米、蘇比丟·西弗勒《聖史》簡述尼希米、區利羅《教理講授》引尼 9:20；其餘各章沒有可查證的教父文本，不編造補位。

---

## 十、仍未完成

1. **沒有人類審稿者。** 全書自評與機器核對，沒有另一位讀者逐章通讀。
2. **摩根的頁碼是推定的，誤差約一頁。** 由 OCR 稿的頁眉記號推出；另以三份不同掃描（`m-livingmessagesof*.txt`）交叉比對：多數引文四份一致（如 p. 252、255、256、262、263），少數落在頁界附近、各份差一頁（p. 259／258、260／261），本書標的是第一份掃描所示頁碼，使用時請以 ±1 頁看待。沒有對照實體書頁。
3. **阿德尼章次、區利羅的 NPNF 卷號**：取自檔頭／檔名，沒有核對實體書頁。
4. **凱爾與德利奇頁碼**：取自 OCR 頁眉，未對照實體書頁。
5. **多處標明的推測**（如 1:3 的「拆毀」與拉 4:23 的關係、2 章四個月的空白、11:1 的「強迫」）都已在正文標明是注疏者或編者的推測，本書沒有替經文補定論。
6. **需作者決定**：以斯拉與尼希米的先後（本書依經文次序、不定案）；12:10-11、22 的世系與「波斯王大利烏」是哪一位（本書不定案）。
""")
    # quotes in the orientation files (not chapters)
    fm = defaultdict(int)
    for name in ["000-preface.md", "00-overview.md", "00a-nehemiah-position.md", "00b-remember-spine.md",
                 "00c-revelation-order.md", "elder-wong-systematic-study.md", "99-remember-me.md", "999-afterword.md"]:
        t = (BOOK / name).read_text(encoding="utf-8")
        for m in re.finditer(r'^> "(.+?)"\s*\n> — (.+)$', t, re.M):
            w = classify(m.group(2))
            if w:
                fm[(name, w)] += 1
    n_fm = sum(fm.values())
    if n_fm:
        L.append("\n---\n\n## 附：卷首框架檔的逐字引文\n")
        L.append("卷首與卷末框架檔另有 **%d** 條帶出處行的逐字引文，已與章內引文同法核對：" % n_fm)
        for (name, w), n in sorted(fm.items()):
            L.append(f"- `{name}`：{WHO[w][0] or '教父'} {n} 條")
    text = "\n".join(L)
    # fix the "其中 N 條在〈歷代注疏〉" placeholder
    n_in = 0
    for n, p in chapters():
        t = p.read_text(encoding="utf-8")
        m = re.search(r"^## 歷代注疏.*?(?=^## )", t, re.M | re.S)
        if m:
            n_in += len(re.findall(r'^> "(.+?)"\s*\n> — (.+)$', m.group(0), re.M))
    text = text.replace("（其中 0 條在〈歷代注疏〉一節", f"（其中 {n_in} 條在〈歷代注疏〉一節")
    return text


def main():
    text = build()
    if "--write" in sys.argv:
        OUT.write_text(text + "\n", encoding="utf-8")
        print(f"wrote {OUT.name} ({len(text)} chars)")
    else:
        print(text)


if __name__ == "__main__":
    main()
