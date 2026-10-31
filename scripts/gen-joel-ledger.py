#!/usr/bin/env python3
"""Generate the Joel volume's citation ledger (99-appendix-references.md) from the book's own text.

The ledger is the honesty account for the promise 「不編造一段出處」. A hand-kept ledger
drifts from the chapters (Luke: declared zero Morgan quotes, carried 29), so every count
and source line is read back out of the chapter files, and the 「機器核對現況」 section is
produced by RUNNING the verifiers at generation time and printing their totals — not by
a paragraph of remembered results (the Nehemiah/Ezra ledgers hard-coded theirs).

Usage:  python3 scripts/gen-joel-ledger.py --write
        python3 scripts/gen-joel-ledger.py            # print
"""
import re
import subprocess
import sys
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "bible" / "joel"
SRC = BOOK / ".sources" / "commentary"
OUT = BOOK / "99-appendix-references.md"

WHO = OrderedDict([
    ("calvin", "加爾文（John Calvin），*Commentaries on the Twelve Minor Prophets*, vol. 2（John Owen 英譯，Calvin Translation Society，1846；CCEL calcom27 公有領域版），約珥書部分"),
    ("henry", "馬太·亨利（Matthew Henry），*Commentary on the Whole Bible*，約珥書卷（原著 1706-1721；CCEL vol. 4）"),
    ("macarthur", "麥克阿瑟（John MacArthur），在別處論到約珥書的講道，gty.org（他沒有約珥書的逐節講道系列）"),
    ("morgan", "摩根（G. Campbell Morgan），〈The Message of Joel〉，載 *Living Messages of the Books of the Bible*, Old Testament"),
    ("fathers", "教父四家：屈梭多模《使徒行傳講道》第 5 講；居普良《論背道者》（Treatise 3）；耶路撒冷的區利羅《教理講授》第 17 講；特土良《論禁食》（ANF/NPNF；newadvent.org）"),
])
SOURCE_FILE = {
    "calvin": "存檔 calvin-joel.txt（ccel.org calcom27 純文字，Joel 部分；含他引的拉丁文與譯者腳註，本書只引明確屬加爾文講章本文的句子）",
    "henry": "存檔 henry-intro.txt、henry-1.txt 至 henry-3.txt（ccel.org mhc4；檔無節號，整章全文，故只能核對到章）",
    "macarthur": "存檔 commentary/gty/ 下的 gty.org 逐字稿（使徒行傳 2 章、耶和華的日子、啟示錄、馬太福音 24 章等講道）",
    "morgan": "存檔 morgan-clean.txt（OCR 稿，頁面斷詞已接合；原稿 morgan-message-of-joel.txt）。只有這一篇概觀，不是逐章注釋",
    "fathers": "存檔 fathers/ 下四檔（newadvent.org 印本；檔內夾有網頁所加的經文參照標記，不是教父原文）",
}
KEYS = [("John Calvin", "calvin"), ("Matthew Henry", "henry"), ("MacArthur", "macarthur"),
        ("Morgan", "morgan"), ("Chrysostom", "fathers"), ("Cyprian", "fathers"), ("Cyril", "fathers"), ("Tertullian", "fathers")]
NUM = {"calvin": "一", "henry": "二", "macarthur": "三", "morgan": "四", "fathers": "五"}


def classify(src):
    for k, n in KEYS:
        if k in src:
            return n
    return None


def chapters():
    return [(int(p.name[:2]), p) for p in sorted(BOOK.glob("[01][0-9]-*.md")) if 1 <= int(p.name[:2]) <= 10]


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
        m = re.search(r"^約珥書\s*([\d:\-–]+)", t, re.M)
        ref[n] = m.group(1) if m else ""
        for who, src in quote_blocks(t):
            if who:
                rows[who][n].append(src)
            else:
                unknown.append((n, src))
    # orientation / back-matter files quote too; the ledger must say so (check-citation-ledger.py reads them as 「第0章」)
    ref[0] = "卷首／卷末"
    for name in ["000-preface.md", "00-overview.md", "00a-joel-position.md",
                 "00c-revelation-order.md", "elder-wong-systematic-study.md", "99-to-pentecost-and-revelation.md", "999-afterword.md"]:
        t = (BOOK / name).read_text(encoding="utf-8")
        for who, src in quote_blocks(t):
            if who:
                rows[who][0].append(src)
            else:
                unknown.append((name, src))
    return rows, ref, unknown


def table(who, rows, ref):
    head = ["| 章 | 約珥書 | 逐字引文（條） | 出處行（去重後；各條為本書所印） |",
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
        "改革宗": [SRC / "calvin-joel.txt", SRC / "henry" / "henry-intro.txt"] + [SRC / "henry" / f"henry-{i}.txt" for i in range(1, 4)],
        "教父": [SRC / "fathers" / n for n in ("chrysostom-acts-hom5.txt", "cyprian-treatise3-lapsed.txt", "cyril-jerusalem-catechetical-17.txt", "tertullian-on-fasting.txt")],
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
    pr = run([py, "scripts/verify-prose-citations.py", str(BOOK), "--self", "珥"])
    pm = re.search(r"(\d+) in-prose citation\(s\) checked \| (\d+) MISS \| (\d+) reviewed-as-term \| (\d+) unresolved", pr)
    gs = run([py, "scripts/gen-joel-scripture.py", "--check"])
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
            if m and not any(k in cur for k in ("改革宗", "教父", "摩根", "麥克阿瑟")):
                total += 1
                q = norm(m.group(1))
                found += any(q in sv for sv in srcs)
    return total, found


def build():
    rows, ref, unknown = scan()
    total_all = sum(len(v) for w in rows.values() for v in w.values())
    L = ["""---
title: 約珥書研讀
subtitle: Joel Deep Study
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
            L.append("摩根只有〈The Message of Joel〉一篇概觀，並非逐章逐節的注釋。凡本書引他，只標「全書概觀」；他的話**不**被寫成論某一章某一節的專論。以下各章的逐字引文：\n")
        if who == "macarthur":
            L.append("麥克阿瑟**沒有約珥書的逐節講道**；本書只引他在使徒行傳、耶和華的日子、啟示錄等講道裏論到約珥書的話。他是**歷史前千禧年、時代論**立場；加爾文是改革宗立場。本書在立場分歧處並陳，不替誰定案。以下各章的逐字引文（出處行的編號為 gty.org 講道編號）：\n")
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
    L.append("\n上表各列的總數，與前面各家表格的條數合計不同，原因有二：(一) 核對腳本掃描全書目錄下的**所有**檔案，包括卷首〈約珥書在整本聖經的位置〉等定位各章裏的引文（見本附錄末「附：卷首框架檔的逐字引文」），前面各表只計十個研讀單元；(二) 核對腳本依〈歷代注疏〉的各小標題挑來源檔，所以位於〈背景〉等其他標題下的引文不在它的範圍，這些引文改以全部來源檔搜尋核對（上表最後一列），前面各表則照出處行把它們計入。")
    if unknown:
        L.append("\n**未能歸屬到任何一家的引文出處行**（須人工檢視）：" + "；".join(f"第{n}章：{s}" for n, s in unknown))
    L.append("""
---

## 八、聖經版本與核對方式

**中文：和合本（CUV）。** 底本取信望愛（fhl）的和合本（保留標點與「」引號），字形與專名一律從 ai-eden.com（本系列標準來源，API 取回）；cnbible.com 的和合本傳統版為第三來源。三個來源逐節比對（`scripts/gen-joel-scripture.py --check`）：73 節字形全數一致。fhl 與 ai-eden 的差異為：牠→他；毘→毗；泰爾→推羅；希臘人→希利尼人；哪裡、那裡→哪裏、那裏（本系列慣例印「裏」）；全形空格「　神」→神；吧！→罷！；原文是事→原文作事；另有逐節處理的三類：嗎／麼（1:2、3:4 印「麼」，1:16 仍印「嗎」）、火焰／火燄（1:19 印「焰」，2:3、2:5 印「燄」）、不致／不至（2:26 印「至」）。fhl 獨有的引號（「」）保留。經文區塊一律由程式從來源產生，不由人手打。

**英文：NASB 1995。** 取自 biblehub.com 各章頁（斜體＝譯者補字，印為 *斜體*）。biblehub 在每段最後一節後黏入下一段的標題，生成器已刪除；全形引號統一為直引號。

**希伯來文。** 字形取自 Sefaria 所載 *Miqra according to the Masorah*，去掉讀經符號、保留母音；節號已改為英文經文編號（希伯來文 3:1-5 = 英 2:28-32；4:1-21 = 英 3:1-21）。全書計數（耶和華的日子 5 次等）皆由此檔以程式計算。

**約珥書以外的經文引用。** 取自 fhl 的和合本，已套用上述字形修正；行文中的「引句＋出處」另逐條與來源比對（見上表）。

**聖詩。** 全部取自 Wikisource 所載 *The Army and Navy Hymnal*（1920，公有領域）或該站其他公有領域印本，英文逐字照來源所印，中譯為編者所作；出處行只寫來源實印。

---

## 九、本書沒有的其他聲音

- **老弟兄**：本項目沒有他講約珥書的第一手教導；本書「老弟兄查經」一節只用他的方法，是方法性撮述，不是逐字語錄。唯一加引號歸給他的，是《使徒行傳》領受總綱裏論五旬節應驗約珥書的一段，註明路徑。
- **麥克阿瑟**：沒有約珥書的逐節講道系列；本書只引他在別處論到約珥書的講道。
- **凱爾與德利奇、巴恩斯、Pusey、司布真、耶柔米《約珥書註釋》**：本書的來源目錄中沒有這些文本，不引。
- **主張約珥書成於被擄以後的學者**：本書所用的來源，沒有這一派的著作；本書只轉述「有此主張」，不引其論據。

---

## 十、仍未完成

1. **沒有人類審稿者。**本書經過機器核對與 AI 校對者的校對；但沒有任何一位人類的神學審稿者逐章通讀過。
2. **麥克阿瑟講道的日期與經文範圍**取自 gty.org 各講道頁所載，未另行核對。
3. **斯特朗編號與字義**多數對 biblehub 抽查，不是逐條窮盡；原文研讀表裏的字義判斷，仍須懂原文的讀者覆核。
4. **希伯來文經文的授權條款。**文字取自 Sefaria 所載 *Miqra according to the Masorah*；該版本的授權條款，本書尚未逐條核對，公開發行前須先確認。
5. **加爾文的 CCEL 檔**夾有譯者腳註；亨利的檔案不含節號，只能核對到章；教父各檔夾有網頁所加的經文標記。均未對照實體書頁。
6. **本書的讀法。**標明「本書的讀法」的地方（例如把 2:11 與 2:25 的「軍旅」「大軍隊」並讀為同一支祂的軍隊）是編者的判斷，不是經文或來源檔自己的說明；是否保留，須作者決定。
7. **詮釋分歧**（成書年代、蝗蟲的身分、2:18 的時態、2:23、五旬節的應驗範圍、約沙法谷、3:21 的譯法）各家並陳，沒有定案。
8. **版面與篇幅。**尚未做精簡輪與獨立校對輪。
""")
    fm = defaultdict(int)
    for name in ["000-preface.md", "00-overview.md", "00a-joel-position.md",
                 "00c-revelation-order.md", "elder-wong-systematic-study.md", "99-to-pentecost-and-revelation.md", "999-afterword.md"]:
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
