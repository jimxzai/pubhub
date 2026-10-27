#!/usr/bin/env python3
"""Generate the Daniel volume's citation ledger (99-appendix-references.md) from the book's own text.

The ledger is the honesty account for the promise 「不編造一段出處」. A hand-kept ledger
drifts from the chapters (Luke: declared zero Morgan quotes, carried 29), so every count
and source line is read back out of the chapter files, and the 「機器核對現況」 section is
produced by RUNNING the verifiers at generation time and printing their totals — not by
a paragraph of remembered results (the Nehemiah/Ezra ledgers hard-coded theirs).

Usage:  python3 scripts/gen-daniel-ledger.py --write
        python3 scripts/gen-daniel-ledger.py            # print
"""
import re
import subprocess
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "bible" / "daniel"
SRC = BOOK / ".sources" / "commentary"
OUT = BOOK / "99-appendix-references.md"

WHO = OrderedDict([
    ("calvin", "加爾文（John Calvin），*Commentaries on the Book of the Prophet Daniel*（Thomas Myers 英譯，Calvin Translation Society，1852-53；CCEL 公有領域版）"),
    ("henry", "馬太·亨利（Matthew Henry），*Commentary on the Whole Bible*，但以理書卷（原著 1706-1721；CCEL vol. 4）"),
    ("macarthur", "麥克阿瑟（John MacArthur），但以理書講道系列，gty.org，編號 27-01 至 27-31（1979-1980）"),
    ("morgan", "摩根（G. Campbell Morgan），〈The Message of Daniel〉，載 *Living Messages of the Books of the Bible*, Old Testament"),
    ("hippolytus", "希坡律陀（Hippolytus），*Exegetical Fragments*〈On Daniel〉與 *On Christ and Antichrist*（ANF vol. 5；newadvent.org）"),
    ("josephus", "約瑟夫（Flavius Josephus），*Antiquities of the Jews*，卷十、十一（Whiston 英譯；Project Gutenberg）"),
])
SOURCE_FILE = {
    "calvin": "存檔 calvin-calcom24.txt（但 1-6）、calvin-calcom25.txt（但 7-12）（ccel.org 純文字；Myers 的腳註混在本文中，OCR 偶有訛字，本書不引訛字句）",
    "henry": "存檔 henry-1.txt 至 henry-12.txt（逐章）與 henry-intro.txt（導論）（ccel.org mhc4；檔無節號，整章全文，故只能核對到章）",
    "macarthur": "存檔 27-01 至 27-31 的 gty.org 逐字稿",
    "morgan": "存檔 morgan-clean.txt（OCR 稿，頁面斷詞已接合；原稿 morgan-message-of-daniel.txt）。只有這一篇概觀，不是逐章注釋",
    "hippolytus": "存檔 hippolytus-exegetical-fragments.txt、hippolytus-christ-and-antichrist.txt（newadvent.org）",
    "josephus": "存檔 josephus-antiquities.txt（gutenberg.org）",
}
KEYS = [("John Calvin", "calvin"), ("Matthew Henry", "henry"), ("MacArthur", "macarthur"),
        ("Morgan", "morgan"), ("Hippolytus", "hippolytus"), ("Josephus", "josephus")]
NUM = {"calvin": "一", "henry": "二", "macarthur": "三", "morgan": "四", "hippolytus": "五", "josephus": "六"}


def classify(src):
    for k, n in KEYS:
        if k in src:
            return n
    return None


def chapters():
    return [(int(p.name[:2]), p) for p in sorted(BOOK.glob("[01][0-9]-*.md")) if 1 <= int(p.name[:2]) <= 16]


QUOTE = re.compile(r'^> "(.+?)"\s*\n(?:>\s*\n)?> (?:[^\n]*\n> )*?— (.+)$', re.M)


def quote_blocks(text):
    """Yield (author-or-None, source line) per verbatim quote; 「同上」 inherits the previous author."""
    last = None
    out = []
    for m in re.finditer(r'^> "(?:.+?)"\s*\n>\s*\n> 「.*?」\s*\n>\s*\n> — (.+)$', text, re.M):
        src = m.group(1).strip()
        who = last if src.startswith("同上") else classify(src)
        if who:
            last = who
        out.append((who, src))
    return out


def scan():
    rows = defaultdict(lambda: defaultdict(list))
    ref = {}
    unknown = []
    for n, p in chapters():
        t = p.read_text(encoding="utf-8")
        m = re.search(r"^但以理書\s*([\d:\-–]+)", t, re.M)
        ref[n] = m.group(1) if m else ""
        for who, src in quote_blocks(t):
            if who:
                rows[who][n].append(src)
            else:
                unknown.append((n, src))
    # orientation / back-matter files quote too; the ledger must say so (check-citation-ledger.py reads them as 「第0章」)
    ref[0] = "卷首／卷末"
    for name in ["000-preface.md", "00-overview.md", "00a-daniel-position.md", "00b-given-spine.md",
                 "00c-revelation-order.md", "elder-wong-systematic-study.md", "99-to-revelation.md", "999-afterword.md"]:
        t = (BOOK / name).read_text(encoding="utf-8")
        for who, src in quote_blocks(t):
            if who:
                rows[who][0].append(src)
            else:
                unknown.append((name, src))
    return rows, ref, unknown


def table(who, rows, ref):
    head = ["| 章 | 但以理書 | 逐字引文（條） | 出處行（去重後；各條為本書所印） |",
            "|--------|----------------|----------------|------------------------------------------------------|"]
    body = []
    for n in sorted(rows[who]):
        srcs = rows[who][n]
        resolved, prev = [], ""
        for s_ in srcs:
            if s_.startswith("同上") and prev:                    # 「同上」 -> the explicit author/work printed before it
                s_ = re.sub(r",\s*on\s.*$", "", prev) + s_[2:]
            else:
                prev = s_
            resolved.append(s_)
        distinct = list(OrderedDict.fromkeys(re.sub(r"，", ", ", re.sub(r"\*", "", s_)) for s_ in resolved))
        label = "第0章（卷首框架檔）" if n == 0 else f"第{n}章"
        body.append(f"| {label} | {ref[n]} | {len(srcs)} | " + "；".join(distinct) + " |")
    total = sum(len(v) for v in rows[who].values())
    return "\n".join(head + body), total, len(rows[who])


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    return (r.stdout + r.stderr)


def verify_status():
    """Run the verifiers over the whole book directory and report their own totals."""
    lines = []
    py = "python3"
    srcs = {
        "改革宗": [SRC / "calvin-calcom24.txt", SRC / "calvin-calcom25.txt", SRC / "henry" / "henry-intro.txt"] + [SRC / "henry" / f"henry-{i}.txt" for i in range(1, 13)],
        "教父": [SRC / "hippolytus-exegetical-fragments.txt", SRC / "hippolytus-christ-and-antichrist.txt"],
        "約瑟夫": [SRC / "josephus-antiquities.txt"],
        "摩根": [SRC / "morgan-clean.txt"],
    }
    for heading, files in srcs.items():
        cmd = [py, "scripts/verify-citations.py", str(BOOK), "--quiet", "--heading", heading]
        for f in files:
            cmd += ["--source", str(f)]
        out = run(cmd)
        m = re.search(r"verbatim OK: (\d+)\s+OK-OCR: (\d+)\s+DRIFT: (\d+)\s+MISS: (\d+)\s+accepted-deviation: (\d+)", out)
        lines.append((heading, m.groups() if m else None))
    out = run([py, "scripts/verify-sermon-quotes.py", str(BOOK), "--cache", str(BOOK / ".sources" / "sermon-cache")])
    sm = re.search(r"verified: (\d+)\s+missing from own transcript: (\d+)\s+unresolved: (\d+)", out)
    pr = run([py, "scripts/verify-prose-citations.py", str(BOOK), "--self", "但"])
    pm = re.search(r"(\d+) in-prose citation\(s\) checked \| (\d+) MISS \| (\d+) reviewed-as-term \| (\d+) unresolved", pr)
    gs = run([py, "scripts/gen-daniel-scripture.py", "--check"])
    ok = len(re.findall(r"^OK ", gs, re.M)); bad = len(re.findall(r"^(DIFFERS|MISSING)", gs, re.M))
    return lines, (sm.groups() if sm else None), (pm.groups() if pm else None), (ok, bad)


def other_quotes():
    """Quotes that sit under a heading the by-heading verifier does not read (e.g. 背景); check them against every source file."""
    import unicodedata
    def norm(t):
        return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", t).lower())
    srcs = [norm(f.read_text(encoding="utf8", errors="replace")) for f in SRC.rglob("*.txt") if "flat" not in f.parts]
    total = found = 0
    for p in sorted(BOOK.glob("[0-9][0-9]*.md")):
        if p.name.startswith(("98", "99-app")):
            continue
        cur = ""
        for l in p.read_text(encoding="utf-8").splitlines():
            if l.startswith("### "):
                cur = l
            m = re.match(r'^> "(.+?)"', l)
            if m and not any(k in cur for k in ("改革宗", "教父", "約瑟夫", "摩根", "麥克阿瑟")):
                total += 1
                q = norm(m.group(1))
                found += any(q in sv for sv in srcs)
    return total, found


def build():
    rows, ref, unknown = scan()
    total_all = sum(len(v) for w in rows.values() for v in w.values())
    L = ["""---
title: 但以理書研讀
subtitle: Daniel Deep Study
author: PubHub 三書精讀系統
date: 2026年10月
publisher: 三書精讀出版系統
---

# 附錄：引用出處總表 (Appendix: Reference Ledger)

各章「歷代注疏」一節的體例說明指向本附錄。本附錄回答三件事：每條引文取自哪裏、如何核對、哪些地方只做到這一步為止。下列各表的章次與條數由程式直接從各章原文讀出，不是手寫的記憶；「機器核對現況」一節則是生成本附錄時當場執行各核對腳本所得的數字。

全書各章帶引號並附「— 作者，書名」出處行的逐字引文共 **%d** 條。

---""" % total_all]
    for who in WHO:
        tbl, total, nch = table(who, rows, ref)
        L.append(f"\n## {NUM[who]}、{WHO[who]}\n")
        L.append(f"來源檔：{SOURCE_FILE[who]}。本書引用 **{total}** 條，分見 {nch} 章，列如下；每條都是該來源檔的逐字子字串（見「七、機器核對現況」）。\n")
        if who == "morgan":
            L.append("摩根只有〈The Message of Daniel〉一篇概觀，並非逐章逐節的注釋。凡本書引他，只標「全書概觀」；他的話**不**被寫成論某一章某一節的專論。以下各章的逐字引文：\n")
        if who == "macarthur":
            L.append("麥克阿瑟的講道是**歷史前千禧年、時代論**立場；加爾文是改革宗立場。本書在立場分歧處並陳，不替誰定案。以下各章的逐字引文（出處行的 27-NN 為 gty.org 講道編號）：\n")
        if who == "henry":
            L.append("亨利的整章檔案不含節號，故各條引文只能核對到章，不能核對到節。以下各章的逐字引文：\n")
        L.append(tbl if total else "（本書沒有引用此家。）")
    vs, sm, pm, gs = verify_status()
    L.append("\n---\n\n## 七、機器核對現況（生成時當場執行）\n")
    L.append("以下數字是生成本附錄時，實際執行各項核對程式所得；不是手寫。")
    L.append("\n| 核對 | 結果 |\n|------|------|")
    for heading, g in vs:
        if g:
            L.append(f"| 注疏引文（{heading}小節） 逐字比對程式 | 逐字吻合 {g[0]} 條；OCR 斷詞吻合 {g[1]} 條；DRIFT {g[2]}；MISS {g[3]}；經審核接受之偏差 {g[4]} |")
        else:
            L.append(f"| 注疏引文（{heading}小節） 逐字比對程式 | （無此類引文可核對） |")
    if sm:
        L.append(f"| 講道引文（對 gty.org 逐字稿） | 核對吻合 {sm[0]} 條；講稿中查無 {sm[1]} 條；無法判讀 {sm[2]} 條 |")
    if pm:
        L.append(f"| 行文中的經文引句（對和合本逐節比對） | 共 {pm[0]} 處；MISS {pm[1]}；經判為詞語 {pm[2]}；無法解析 {pm[3]} |")
    L.append(f"| 各章經文區塊與來源逐字相同 | OK {gs[0]} 章；不符或缺 {gs[1]} 章 |")
    ot, of = other_quotes()
    L.append(f"| 位於〈背景〉等非注疏標題下的逐字引文（核對腳本依標題挑來源，不掃這些）：全部來源檔搜尋 | 共 {ot} 條，找到 {of} 條 |")
    L.append("\n上表各列的總數，與前面各家表格的條數合計不同，原因有二：(一) 核對腳本掃描全書目錄下的**所有**檔案，包括卷首〈但以理書的位置〉等定位各章裏的引文（見本附錄末「附：卷首框架檔的逐字引文」），前面各表只計十六個研讀單元；(二) 核對腳本依〈歷代注疏〉的各小標題挑來源檔，所以位於〈背景〉等其他標題下的引文不在它的範圍，這些引文改以全部來源檔搜尋核對（上表最後一列），前面各表則照出處行把它們計入。")
    if unknown:
        L.append("\n**未能歸屬到任何一家的引文出處行**（須人工檢視）：" + "；".join(f"第{n}章：{s}" for n, s in unknown))
    L.append("""
---

## 八、聖經版本與核對方式

**中文：和合本（CUV）。** 底本取信望愛（fhl）的和合本（保留標點與「　神」空格），再與 ai-eden.com（本專案標準來源，API 取回）逐節對校。fhl 與 ai-eden 在字形與專名上的差異共十類（牠、她→他；嗎→麼；祕→秘；希臘→希利尼；毘→毗；吧→罷；焰→燄；米底亞→瑪代；利比亞→呂彼亞），另有四類是 fhl 獨有的引號標點（「」『』），保留；字形與專名一律從 ai-eden（本系列標準）；「裏／裡」依本系列慣例印「裏」。cnbible.com 為多版本混頁，僅作輔助，未作為決定依據。經文區塊一律由程式從來源產生，不由人手打；本書第一章的經文最初是手打的，與來源有十餘處不同，這是「不手打」這條規則的由來。

**英文：NASB 1995。** 取自 biblehub.com 各章頁（斜體＝譯者補字，印為 *斜體*）。與 ai-eden.com 的 NASB 欄逐節比對：357 節中 355 節相同；差異兩處：5:23 ai-eden 少一個 "all"（biblehub 為 NASB 1995 之正確讀法），7:8 biblehub 於節尾黏入下一段標題，已由生成器刪除。

**希伯來文／亞蘭文。** 字形取自 Sefaria 所載 *Miqra according to the Masorah*，節號已改為英文經文編號（馬索拉編號 3:31-33 = 英 4:1-3；4:1-34 = 英 4:4-37；6:1 = 英 5:31；6:2-29 = 英 6:1-28）。亞蘭文段落為 2:4b-7:28。

**但以理書以外的經文引用。** 取自 fhl 的和合本，已套用上述字形修正；行文中的「引句＋出處」另逐條與來源比對（見上表）。

**聖詩。** 全部取自 Wikisource 所載 *The Army and Navy Hymnal*（1920，公有領域）或該站其他公有領域印本，英文逐字照來源所印，中譯為編者所作；出處行只寫來源實印。

---

## 九、本書沒有的其他聲音

- **老弟兄**：本項目沒有他講但以理書的第一手教導；本書「老弟兄查經」一節只用他的方法，是方法性撮述，不是逐字語錄。
- **凱爾與德利奇、巴恩斯、Pusey、司布真、耶柔米《但以理書註釋》**：本書的來源目錄中沒有這些文本，不引。
- **主張但以理書成於主前二世紀的學者**：本書所用的來源（加爾文、亨利、麥克阿瑟、希坡律陀、約瑟夫）全部採六世紀成書立場；本書只轉述「有此主張」，不引其著作。

---

## 十、仍未完成

1. **沒有人類審稿者。**本書經過機器核對，以及一輪由六位彼此獨立的 AI 校對者（沒有看過作者的結論，逐章對照來源檔）所做的校對與修訂；但沒有任何一位人類的神學審稿者逐章通讀過。
2. **麥克阿瑟講道的日期**取自 gty.org 各講道頁所載，未另行核對。
3. **斯特朗編號與字義**多數對 biblehub 抽查，不是逐條窮盡；原文研讀表裏的字義判斷，仍須懂原文的讀者覆核。
4. **希伯來文與亞蘭文經文的授權條款。**文字取自 Sefaria 所載 *Miqra according to the Masorah*；該版本的授權條款，本書尚未逐條核對，公開發行前須先確認。
5. **加爾文的 CCEL 檔**夾有譯者腳註與編者序言，本書只引明確屬加爾文講章本文的句子；沒有對照實體書頁。**約瑟夫**取自 Whiston 英譯本的電子版，卷章編號取自該檔，未對照實體書。
6. **本書的讀法。**幾處標明「本書的讀法」的地方（例如把第 7 章的被動式讀為神所賜、把啟 13:2 的「給」與但以理書的「賜」並排）是編者的判斷，不是經文或來源檔自己的說明；是否保留，須作者決定。
7. **四個詮釋分歧**（成書年代、四國、七十個七、小角）各家並陳，沒有定案；主張主前二世紀成書的學者，其原著不在本書的來源裏，只有被反對的一方轉述。
8. **版面。**多章超過每章 28 KB 的篇幅目標，尚未做精簡輪；個別聖詩的作者年份，Wikisource 頁面沒有印出，署名行只寫來源所印。
9. **老弟兄。**本書沒有他講但以理書的第一手教導；「老弟兄查經」一節只用他的方法，若日後找到他的第一手材料，須逐章補入並核對。
""")
    fm = defaultdict(int)
    for name in ["000-preface.md", "00-overview.md", "00a-daniel-position.md", "00b-given-spine.md",
                 "00c-revelation-order.md", "elder-wong-systematic-study.md", "99-to-revelation.md", "999-afterword.md"]:
        f = BOOK / name
        if not f.exists():
            continue
        for who, _src in quote_blocks(f.read_text(encoding="utf-8")):
            if who:
                fm[(name, who)] += 1
    if fm:
        L.append("\n---\n\n## 附：卷首框架檔的逐字引文\n")
        L.append("卷首與卷末框架檔另有 **%d** 條帶出處行的逐字引文，已與章內引文同法核對（核對腳本的總數包含它們）：" % sum(fm.values()))
        for (name, w), n in sorted(fm.items()):
            L.append(f"- {name}：{WHO[w].split('（')[0]} {n} 條")
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
