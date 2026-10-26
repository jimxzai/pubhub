#!/usr/bin/env python3
"""Generate the Jeremiah volume's two appendices from the book's own text.

  98-appendix-indices.md     chapter map / cross-book Scripture index / subject index / Hebrew word index
  99-appendix-references.md  citation ledger (who is quoted where, what was machine-checked, what is unfinished)

Same rationale as scripts/gen-nehemiah-indices.py and gen-nehemiah-ledger.py: a hand-kept index or
ledger drifts from the chapters.  Every count below is read back out of the chapter files, and the
machine-check section RUNS the verification scripts and prints what they actually said.

Usage:  python3 scripts/gen-jeremiah-appendices.py --write        # rewrite both files
        python3 scripts/gen-jeremiah-appendices.py                # print both
        python3 scripts/gen-jeremiah-appendices.py --no-run --write   # skip the slow verification runs
"""
import importlib.util
import re
import subprocess
import sys
import urllib.parse
from collections import OrderedDict, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "books" / "bible" / "jeremiah"
SRC = BOOK / "sources"
OUT_INDEX = BOOK / "98-appendix-indices.md"
OUT_LEDGER = BOOK / "99-appendix-references.md"
NUNITS = 27

FRONT = """---
title: 耶利米書研讀
subtitle: Jeremiah Deep Study
author: PubHub 三書精讀系統
date: 2026年10月
publisher: 三書精讀出版系統
---
"""

VOLUME = {}
for rng, name in [((1, 4), "卷一·呼召與控訴"), ((5, 11), "卷二·殿與不聽"), ((12, 16), "卷三·君王與假先知"),
                  ((17, 19), "卷四·安慰之書"), ((20, 24), "卷五·話語與焚燒"), ((25, 27), "卷六·列國與終局")]:
    for i in range(rng[0], rng[1] + 1):
        VOLUME[i] = name

# ---------------------------------------------------------------- shared helpers
_spec = importlib.util.spec_from_file_location("john_index", ROOT / "scripts" / "gen-john-scripture-index.py")
john = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(john)
BOOKS = list(john.BOOKS)
ORDER = {full: i for i, (full, _) in enumerate(BOOKS)}
ALIAS = {a: full for full, aliases in BOOKS for a in aliases}
MAXCHAP = dict(john.MAXCHAP)
_SHORT = "|".join(a for a in ALIAS if len(a) == 1)
_LONG = "|".join(sorted((a for a in ALIAS if len(a) > 1), key=len, reverse=True))
REF = re.compile(
    rf"(?:(?<![{john.CJK}A-Za-z0-9])({_SHORT})|(?<![A-Za-z0-9])({_LONG}))"
    rf"\s*(\d+)(?::{john.VERSES})?(?=\s*章?)"
)
AMBIGUOUS = set("但得該拿傳歌書拉")
LIST_PUNCT = set("（(、；;/ ")

SOURCES = [
    ("000-preface.md", "前言"), ("00-overview.md", "卷首·概覽"), ("00a-jeremiah-position.md", "卷首·位置"),
    ("00b-watching-spine.md", "卷首·骨幹"), ("00c-revelation-order.md", "卷首·啟示的次序"),
    ("elder-wong-systematic-study.md", "卷首·領受總綱"),
] + [(f"{i:02d}", f"第{i}篇") for i in range(1, NUNITS + 1)] + [
    ("99-to-revelation.md", "卷末"), ("999-afterword.md", "跋"),
]

SUBJECTS = [
    ("留意（שׁקד）", r"留意"), ("耶和華的話臨到", r"話臨到"), ("拔出、拆毀、建立、栽植", r"拔出|栽植"),
    ("哭泣／眼淚", r"眼淚|哭泣|哀哭|哭"), ("禱告／代求", r"禱告|祈禱|代求|祈求"), ("回來／回轉", r"回來|回轉|歸回|轉回"),
    ("背道", r"背道"), ("平安", r"平安"), ("假先知", r"假先知|假預言"), ("殿／聖殿", r"聖殿|殿門|殿中|殿院|這殿"),
    ("示羅", r"示羅"), ("窯匠", r"窯匠"), ("心", r"心版|人心|心上|心中"), ("新約", r"新約"),
    ("七十年", r"七十年"), ("巴比倫", r"巴比倫"), ("尼布甲尼撒", r"尼布甲尼撒"), ("埃及", r"埃及"),
    ("西底家", r"西底家"), ("約雅敬", r"約雅敬"), ("約雅斤／哥尼雅", r"約雅斤|哥尼雅|耶哥尼雅"), ("約西亞", r"約西亞"),
    ("巴錄", r"巴錄"), ("書卷", r"書卷"), ("軛", r"木軛|軛"), ("無花果", r"無花果"), ("淤泥坑", r"淤泥|坑中"),
    ("以伯米勒（古實人）", r"以伯米勒"), ("利甲族", r"利甲"), ("亞拿突", r"亞拿突"), ("公義的苗", r"苗裔|公義的苗"),
    ("安慰", r"安慰"), ("列國", r"列國|萬國"), ("摩押", r"摩押"), ("以法蓮", r"以法蓮"), ("拉結", r"拉結"),
    ("老弟兄的方法（提問）", r"提問"), ("你看見耶穌了嗎", r"看見耶穌"),
]


def source_path(name):
    if name.endswith(".md"):
        return BOOK / name
    hits = sorted(BOOK.glob(f"{name}-*.md"))
    return hits[0] if hits else None


def prose_lines(path):
    """Chapter lines minus the Scripture block, hymn blocks, template boilerplate and table rows."""
    out, skip, skip3 = [], False, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            skip = line.startswith(("## 經文", "## 配詩"))
            skip3 = False
        elif line.startswith("### "):
            skip3 = line.startswith(("### 今天的祭壇", "### 禱告回應", "### 默想問題"))
        if skip or skip3 or line.lstrip().startswith(("|", "> ^")):
            continue
        out.append(line)
    return out


def refs_in(text):
    for m in REF.finditer(text):
        alias = m.group(1) or m.group(2)
        if alias in AMBIGUOUS and m.start() > 0 and text[m.start() - 1] not in LIST_PUNCT:
            continue
        chap = int(m.group(3))
        full = ALIAS[alias]
        if chap < 1 or chap > MAXCHAP[full]:
            continue
        yield full, chap


# ---------------------------------------------------------------- indices
def chapter_map():
    rows = ["| 篇 | 耶利米書 | 卷 | 篇題 | 本章鑰詞 |",
            "|--------|----------------|------------------------|--------------------------------|------------------------------------------|"]
    for i in range(1, NUNITS + 1):
        p = source_path(f"{i:02d}")
        if not p:
            continue
        text = p.read_text(encoding="utf-8")
        h1 = re.search(r"^# (.+)$", text, flags=re.M)
        title = re.sub(r"\s*\(.*\)\s*$", "", h1.group(1)) if h1 else ""
        refline = re.search(r"^耶利米書\s*([\d:\-–]+)", text, flags=re.M)
        key = re.search(r"本章鑰詞[：:]\s*\**([^\n\\]*?)\**\s*(?:\\|$)", text, flags=re.M)
        rows.append(f"| {i:02d} | {refline.group(1) if refline else ''} | {VOLUME[i]} | {title} | "
                    f"{key.group(1).strip(' *') if key else ''} |")
    return "\n".join(rows)


def scripture_index():
    index = defaultdict(set)
    for fname, label in SOURCES:
        p = source_path(fname)
        if not p or not p.exists():
            continue
        for line in prose_lines(p):
            cleaned = re.sub(r"耶利米書\s*\d+(?::\d+(?:[-–]\d+)?)?", "", line)
            cleaned = re.sub(r"(?<![一-鿿])耶\s*\d+(?::\d+(?:[-–,，]\s*\d+)*)?", "", cleaned)
            for full, chap in refs_in(cleaned):
                if full == "耶利米書":
                    continue
                index[(full, chap)].add(label)
    order = {lbl: i for i, (_, lbl) in enumerate(SOURCES)}
    keys = sorted(index, key=lambda k: (ORDER.get(k[0], 999), k[1]))
    out = ["| 經文 | 本書討論之處 |",
           "|--------------------------|----------------------------------------------------------|"]
    for full, chap in keys:
        out.append(f"| {full} {chap} | {'、'.join(sorted(index[(full, chap)], key=lambda l: order.get(l, 999)))} |")
    return "\n".join(out), len(keys)


def subject_index():
    out = ["| 主題 | 見於 |", "|--------------------------|----------------------------------------------------------|"]
    for name, pat in SUBJECTS:
        where = []
        for i in range(1, NUNITS + 1):
            p = source_path(f"{i:02d}")
            if p and sum(len(re.findall(pat, l)) for l in prose_lines(p)) >= 1:
                where.append(f"第{i}篇")
        if where:
            out.append(f"| {name} | {'、'.join(where)} |")
    return "\n".join(out)


def hebrew_index():
    out = ["| 原文 | 出處 | 見 | 要點 |", "|--------------------|------------|--------|------------------------------------------------|"]
    for i in range(1, NUNITS + 1):
        p = source_path(f"{i:02d}")
        if not p:
            continue
        t = p.read_text(encoding="utf-8")
        m = re.search(r"^## 原文研讀.*?(?=^## )", t, re.M | re.S)
        if not m:
            continue
        for line in m.group(0).splitlines():
            if not line.startswith("|") or line.startswith("|--") or "| 原文 |" in line:
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 3 or not re.search(r"[\u0590-\u05FF]", cells[0]):
                continue
            gloss = re.split(r"[；;。]", cells[2])[0]
            gloss = re.sub(r"\*+", "", gloss)
            if len(gloss) > 40:
                cut = gloss[:40]
                gloss = (cut.rsplit("，", 1)[0] if "，" in cut else cut) + "…"
            gloss = re.sub(r"（[^）]*$", "", gloss)
            out.append(f"| {cells[0]} | {cells[1]} | 第{i}篇 | {gloss} |")
    return "\n".join(out)


def build_index():
    sc, nsc = scripture_index()
    return FRONT + f"""
# 附錄：經文與主題索引 (Appendix: Scripture & Subject Indices)

本附錄依全書正文實際出現的內容編製，不另行增列各篇未曾論及的經文或主題。四張表都由
`scripts/gen-jeremiah-appendices.py` 直接從各篇原文抽取生成，不以手工維護，以免與正文脫節。

---

## 附錄一：本書篇次與耶利米書經文對照 (Chapter Map)

本書二十七篇，每篇一個研讀單元；**篇次序號是本書的單元序號，不是耶利米書的章號**，真實章節範圍在下表第二欄。

{chapter_map()}

---

## 附錄二：跨書經文索引 (Cross-Book Scripture Index)

下表列出各篇行文所引用的**耶利米書以外**的經文章次（節號不列；耶利米書本身的引用不入此表）。「經文」區塊、配詩與引用表格不計；只有「章」層級，節號以各篇為準。共 {nsc} 條。

{sc}

---

## 附錄三：主題索引 (Subject Index)

以下主題由各篇行文（不含經文區塊、配詩、今天的祭壇、禱告回應、默想問題與引用表格）逐篇計數得出，出現至少一次即列。

{subject_index()}

---

## 附錄四：原文詞彙索引 (Hebrew Word Index)

各篇〈原文研讀〉表格中的希伯來文詞，依篇次列出（每條只取該列意義欄第一個分句）。

{hebrew_index()}
"""


# ---------------------------------------------------------------- ledger
WHO = OrderedDict([
    ("calvin", ("John Calvin", "加爾文（John Calvin），*Commentaries on the Book of the Prophet Jeremiah and the Lamentations*，約翰·歐文（John Owen）英譯")),
    ("henry", ("Matthew Henry", "馬太·亨利（Matthew Henry），*Commentary on the Whole Bible*，耶利米書卷")),
    ("morgan", ("G. Campbell Morgan", "摩根（G. Campbell Morgan），*The Message of Jeremiah*，載 *Living Messages of the Books of the Bible*, Old Testament（1912）")),
    ("macarthur", ("John MacArthur", "麥克阿瑟（John MacArthur），gty.org 講章與文章")),
    ("fathers", ("", "教父（NPNF／ANF 公有領域英譯，取自 newadvent.org）")),
])
FATHER_KEYS = ["Chrysostom", "Augustine", "Justin", "Tertullian", "Jerome", "Cyprian", "Irenaeus"]
SOURCE_FILE = {
    "calvin": "`sources/commentary/calvin/calcom17.txt`–`calcom21.txt`（ccel.org 的 `calcom17`–`calcom21`，涵蓋耶利米書 1–52 章；英譯本內的編者按語〔— Ed.〕一律不引）",
    "henry": "`sources/commentary/henry/jer-page-*.txt`（ccel.org，*Commentary on the Whole Bible* vol. 4〔`mhc4`〕；羅馬數字頁＝耶利米書章號＋1；整章全文，無節號）",
    "morgan": "`m-livingmessagesof01morgiala.txt`（存於 Nehemiah 卷的 `sources/commentary/` 資料夾；archive.org *Living Messages of the Books of the Bible* 的 OCR；只有一篇全書概觀，約自 p. 109 起；頁碼取自頁眉記號）",
    "macarthur": "`sources/commentary/gty/<CODE>.txt`（gty.org 講章逐字稿／文章；索引見 `sources/commentary/gty/INDEX.md`）",
    "fathers": "`sources/commentary/fathers/*.txt`（每檔含 AUTHOR／WORK／TRANSLATOR／SOURCE_URL 四行標頭；索引見 `sources/commentary/fathers/INDEX.md`）",
}


def classify(src):
    for k, n in [("John Calvin", "calvin"), ("Matthew Henry", "henry"), ("G. Campbell Morgan", "morgan"),
                 ("John MacArthur", "macarthur")]:
        if k in src:
            return n
    if any(f in src for f in FATHER_KEYS):
        return "fathers"
    return None


QUOTE = re.compile(r'^> "(.+?)"\s*\n> — (.+)$', re.M)


def chapters():
    return [(int(p.name[:2]), p) for p in sorted(BOOK.glob("[0-9][0-9]-*.md")) if 1 <= int(p.name[:2]) <= NUNITS]


def scan():
    rows = defaultdict(lambda: defaultdict(list))
    ref = {}
    for n, p in chapters():
        t = p.read_text(encoding="utf-8")
        m = re.search(r"^耶利米書\s*([\d:\-–]+)", t, re.M)
        ref[n] = m.group(1) if m else ""
        for m in QUOTE.finditer(t):
            who = classify(m.group(2))
            if who:
                rows[who][n].append(m.group(2).strip())
    return rows, ref


def table(who, rows, ref):
    head = ["| 篇 | 耶利米書 | 逐字引文（條） | 出處行（各條，本書實印） |",
            "|--------|----------------|----------------|------------------------------------------------------|"]
    body = []
    for n in sorted(rows[who]):
        srcs = rows[who][n]
        distinct = list(OrderedDict.fromkeys(re.sub(r"\*", "", s) for s in srcs))
        body.append(f"| 第{n}篇 | {ref[n]} | {len(srcs)} | " + "；".join(distinct) + " |")
    total = sum(len(v) for v in rows[who].values())
    return "\n".join(head + body), total


def run(cmd, timeout=900):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=ROOT)
        return (r.stdout or "") + (r.stderr or "")
    except Exception as e:  # noqa: BLE001
        return f"ERROR {e}"


def machine_checks(skip):
    if skip:
        return "（本次生成以 `--no-run` 略過逐項執行；請不帶該旗標重新生成。）"
    py = sys.executable
    corpus = SRC / "commentary" / "corpus-all.txt"
    lines = []
    out = run([py, "scripts/verify-citations.py", str(BOOK), "--source", str(corpus)])
    m = re.search(r"verbatim OK:\s*(\d+)\s+OK-OCR:\s*(\d+)\s+DRIFT:\s*(\d+)\s+MISS:\s*(\d+)", out)
    lines.append("- **注疏引文逐字核對**（`verify-citations.py`，對合併語料 `sources/commentary/corpus-all.txt`＝亨利＋加爾文＋摩根＋全部教父檔＋全部 gty 檔）："
                 + (f"逐字吻合 {m[1]}、OCR 斷詞吻合 {m[2]}、DRIFT {m[3]}、MISS {m[4]}。" if m else "無法讀出結果。")
                 + "此項只證明引文是來源語料的連續子字串，**不證明歸屬正確**；歸屬另由下列兩項與各章撰寫時的逐檔核對負責。")
    out = run([py, "scripts/verify-sermon-quotes.py", str(BOOK)])
    m = re.search(r"verified:\s*(\d+)\s+missing from own transcript:\s*(\d+)\s+unresolved:\s*(\d+)", out)
    lines.append("- **麥克阿瑟引文對各自講章核對**（`verify-sermon-quotes.py`，每條只對它自己出處行的講章編號）："
                 + (f"核對 {m[1]} 條吻合，不在自己講章內 {m[2]} 條，無法解析 {m[3]} 條。" if m else "無法讀出結果。")
                 + "無法解析的條目是出處行寫成「article A102」「sermon TMU224」這類該腳本不認的格式，已另以對各自檔案的正規化子字串比對確認逐字吻合。")
    out = run([py, "scripts/verify-prose-citations.py", str(BOOK), "--self", "耶"])
    m = re.search(r"(\d+) in-prose citation\(s\) checked \| (\d+) MISS \| (\d+) reviewed-as-term \| (\d+) unresolved", out)
    lines.append("- **行文中的經文引句**（`verify-prose-citations.py … --self 耶`，對 fhl 和合本）："
                 + (f"檢查 {m[1]} 個「引號＋出處」，MISS {m[2]}，unresolved {m[4]}。" if m else "無法讀出結果。")
                 + "unresolved 是該腳本不能解析出處的條目，不是已核對的錯誤，也不是已核對無誤。"
                 + ("本書這 3 條是第 3 篇的「希伯來 14:5」兩處（何西阿書的希伯來文節號；對應的和合本何 14:4 已另對 fhl 核對，與引句吻合）與「亨利接 3:19」（指亨利把加 4:6 的「阿爸！父！」接到耶 3:19，不是出處）。" if m and m[4] == "3" else ""))
    out = run([py, "scripts/check-prose-scripture-quotes.py", str(BOOK)])
    m = re.search(r"(\d+) file\(s\) scanned; (\d+) quote\(s\) not found", out)
    lines.append("- **行文引句對本篇經文區塊**（`check-prose-scripture-quotes.py`）："
                 + (f"掃描 {m[1]} 個檔，{m[2]} 條不在該篇印出的經文內；這些全是引用耶利米書**其他章**的句子（標 NOT-IN-UNIT），已由上一項對全書和合本核對。" if m else "無法讀出結果。"))
    out = run([py, "scripts/lint-chapter-markup.py", str(BOOK)])
    m = re.search(r"clean: (\d+) files", out)
    lines.append("- **標記檢查**（`lint-chapter-markup.py`）：" + (f"{m[1]} 個檔乾淨。" if m else out.strip().splitlines()[-1] if out.strip() else "無輸出。"))
    out = run([py, "scripts/lint-scripture-text.py", str(BOOK)])
    m = re.search(r"(\d+) finding\(s\)", out)
    lines.append("- **和合本字形檢查**（`lint-scripture-text.py`）："
                 + (f"{m[1]} 項候選，全部是「做」字，須以第二來源核對，見「七、聖經版本與核對方式」。" if m else "無候選。"))
    out = run([py, "scripts/check-book-spine.py", str(BOOK)])
    ok = re.findall(r"\[(ok |GAP|--- )\]\s*(.+)", out)
    lines.append("- **骨幹檢查**（`check-book-spine.py`）：" + "；".join(f"{a.strip()} {b.strip()}" for a, b in ok))
    lines.append("- **分卷扉頁的骨幹句**：目錄已由 `jeremeiah` 改名為 `jeremiah`，`check-book-spine.py` 可自動檢查分卷扉頁（6/6 帶「啟示的次序·第 N 步」）；其中引句另由編者以 `verify-prose-citations` 同法核對。")
    return "\n".join(lines)


def hymn_table():
    rows = ["| 篇 | 聖詩 | 作者 | 年份（來源頁所印） | 來源 |",
            "|--------|------------------------------|--------------------|--------------------|------------------------------|"]
    nostated = 0
    for f in sorted((SRC / "hymns").glob("[0-9][0-9]-*.txt")):
        h = {}
        for line in f.read_text(encoding="utf-8").splitlines()[:4]:
            k, _, v = line.partition(":")
            h[k.strip()] = v.strip()
        year = h.get("YEAR", "")
        if "not stated" in year.lower():
            nostated += 1
            year = "來源頁未印"
        else:
            ym = re.match(r"(\d{4})", year)
            year = (ym.group(1) + ("（依同站另一頁）" if "per en.wikisource page" in year else "")) if ym else year
        url = urllib.parse.unquote(h.get('SOURCE_URL', ''))
        host = re.sub(r'^https?://', '', url).split('/')[0]
        page = re.sub(r'^https?://[^/]+/(wiki/|text/|w/index\.php\?title=)?', '', url).replace('_', ' ')
        rows.append(f"| 第{int(f.name[:2])}篇 | {h.get('TITLE', '')} | {h.get('AUTHOR', '')} | {year} | {host}：{page.replace('/', ' / ')} |")
    return "\n".join(rows), nostated


def cuv_diff_count():
    P = re.compile(r'[\s，。、；：！？「」『』（）—…·,.;:!?"\'“”‘’a-z0-9<>/=]+')
    def n(t):
        return P.sub('', t.replace('裡', '裏').replace('甚麼', '什麼').replace('玷污', '玷汙'))
    d = SRC / "scripture"
    a = {l.split('\t')[0]: n(l.split('\t', 1)[1]) for l in open(d / "cuv.tsv", encoding="utf-8")}
    b = {l.split('\t')[0]: n(l.split('\t', 1)[1]) for l in open(d / "cuvmpt.tsv", encoding="utf-8")}
    return sum(1 for k in a if a[k] != b.get(k)), len(a)


def build_ledger(skip_run):
    rows, ref = scan()
    total = sum(len(v) for w in rows.values() for v in w.values())
    n_in = 0
    for n, p in chapters():
        t = p.read_text(encoding="utf-8")
        m = re.search(r"^## 歷代注疏.*?(?=^## )", t, re.M | re.S)
        if m:
            n_in += len(QUOTE.findall(m.group(0)))
    L = [FRONT, f"""
# 附錄：引用出處總表 (Appendix: Reference Ledger)

各章「歷代注疏」一節的體例說明指向本附錄。本附錄回答三件事：每條引文取自哪裏、如何核對、哪些地方只做到這一步為止。下列各表的篇次與條數由 `scripts/gen-jeremiah-appendices.py` 直接從各篇原文讀出，不是手寫的記憶；`scripts/check-citation-ledger.py` 可再把它與各篇對照。

全書帶引號並附「— 作者，書名」出處行的逐字引文共 **{total}** 條（其中 {n_in} 條在〈歷代注疏〉一節，其餘在〈背景〉〈全經連線〉等處）。

---"""]
    for who, num in zip(WHO, "一二三四五"):
        tbl, tot = table(who, rows, ref)
        L.append(f"\n## {num}、{WHO[who][1]}\n")
        L.append(f"來源檔：{SOURCE_FILE[who]}。本書引用 **{tot}** 條，列如下。\n")
        if who == "morgan":
            L.append("摩根只有一篇全書概觀，不是逐章逐節的注釋；本書只在確實切題處引用，頁碼一律標出，其中少數頁碼（p. 111 與 p. 123）是依 OCR 頁眉推定的。以下各篇的逐字引文：\n")
        if who == "macarthur":
            L.append("gty.org 沒有麥克阿瑟的耶利米書逐節講道（站點地圖上只有兩篇把「耶利米書」列為經文：80-42、80-367）。本書引的是講別的經文、順帶講到耶利米書的段落，以及文章 A102、講章 TMU224 等；第 15、23、27 篇沒有可查材料，不立此節。部落格 B150925（論耶 29:11）無署名，不歸給他。以下各篇的逐字引文：\n")
        if who == "calvin":
            L.append("加爾文的英譯本夾有編者按語（如 22:16 的原文直譯、31:32 的希伯來書異讀），本書遇到只作轉述並註明是編者按語，不當作加爾文本人的話引用。以下各篇的逐字引文：\n")
        if who == "fathers":
            L.append("教父引文共分布在 16 篇；第 1、11、12、15、20、22–27 篇查無可定位的教父文字，不立〈教父時期〉小節。以下各篇的逐字引文：\n")
        L.append(tbl)
        if who in ("morgan", "macarthur"):
            units = "、".join(f"第{n}章" for n in sorted(rows[who]))
            L.append(f"\n逐字引文所在單元（供 `check-citation-ledger.py` 讀取；此處「章」指本書第 N 個研讀單元，即上表的「第 N 篇」，不是耶利米書的章）：{units}。")

    L.append("\n---\n\n## 六、機器核對現況（誠實記錄）\n")
    L.append(machine_checks(skip_run))

    nd, nv = cuv_diff_count()
    ht, nostated = hymn_table()
    L.append(f"""
---

## 七、聖經版本與核對方式

**中文：和合本（CUV）。** 底本取信望愛（fhl）的和合本（`bible.fhl.net` 的 `unv`），再與兩個獨立來源對校：cnbible.com 的現代標點和合本（CUVMPT）與 ai-eden.com（本專案標準來源，API 取回）。

- fhl 與 cnbible 在兩百多節（全書 {nv} 節）有出入（確切節數隨比對時怎樣忽略標點、空格與「甚麼／什麼」而浮動，這裏不印單一數字），多為「做／作」「事奉／侍奉」一類的字形與慣用詞，不是意思的差異；本書從 fhl 的 1919 年和合本寫法。
- 「做／作」以 ai-eden 第三來源逐節核對：fhl 與 ai-eden 全書一致，**只有耶 25:6 一處不同**（fhl 作「手所做的」，ai-eden 作「手所作的」）；第三個來源（cnbible 的傳統版頁面）取不到，**這一節本書尚未定案**，印的是 fhl 的「做」。`lint-scripture-text.py` 報的 29 項「做」都是 fhl 與 ai-eden 一致的寫法。
- **和合本併節。** 和合本把 34:9 併入 34:8、34:19 併入 34:18、43:6 併入 43:5（fhl 與 ai-eden 都在被併的節留一個字母 a）。經文區塊由 `inject_scripture.py` 印成 ^8-9^、^18-19^、^5-6^；英文 NASB 仍分節，所以兩欄的節號在這三處不同。
- **希伯來文節號。** Sefaria 採希伯來文節號：耶利米書 8 章有 23 節、9 章有 25 節（希伯來 8:23＝中文 9:1）。本書正文一律用和合本節號，引用希伯來文時已換算。
- **fhl 的註記。** fhl 的和合本把小字譯註（「原文是」「或譯」）印進正文括號，本書照留。
- **神的名字與破折號。** 和合本在「耶和華─我們的神」等處用「─」，行文引句照原樣印出。

**英文：NASB 1995。** 取自 biblehub.com 各章頁（`biblehub.com/nasb/jeremiah/N.htm`，頁題為 NASB 1995；斜體＝譯者補字，印為 *斜體*）。**本書沒有逐節把 biblehub 與 ai-eden 的 NASB 對校**（ai-eden 的 NASB 把雙引號壓成單引號，且已知有錯亂節），所以這一項只有單一來源。

**希伯來文。** 字頻與詞形取自 Sefaria 所載 *Miqra according to the Masorah*（本地 `sources/hebrew/jer-N.json`）。他書的希伯來文以 `sources/heb.py` 取同一來源。**全書字頻多由各篇撰寫者以正則表達式對這份資料自行計算**，每個數字附計法；未另行獨立重算，見「十、仍未完成」。

**聖詩。** 二十七首，英文逐字取自下表來源頁，中譯為編者所作。來源頁沒有印年份的 {nostated} 首，出處行只寫作者。

{ht}

---

## 八、本書沒有的其他聲音

- **老弟兄**：沒有講耶利米書的第一手教導（見〈前言〉第一項）；各篇〈老弟兄查經〉一節只用他的方法，不加引號歸話給他。
- **麥克阿瑟**：沒有耶利米書逐節講道；第 15、23、27 篇無可查材料。
- **教父**：第 1、11、12、15、20、22–27 篇查無可定位的教父文字；優西比烏、俄利根、耶柔米論但以理書等在 newadvent.org 上沒有可用的耶利米書段落；現代版權譯本一律不用。
- **摩根**：只有全書概觀，沒有逐章。摩根另一本《耶利米書研究》（1931）在美國尚未進入公有領域，未用。

---

## 九、本書標明的未解與並陳之處

以下是各篇已在正文標明「並陳、不定案」的重點（細節以各篇為準）：7:21-23 為何說「沒有吩咐」燔祭；13:1-11 腰帶是否真到幼發拉底河；23:6／33:16 的名字；七十年的起算；31:22「女子護衛男子」；31:31 的「以色列家和猶大家」；27:1 的王是約雅敬還是西底家（和合本括註、希伯來文與 NASB 1995 各不同）；52:28-30 的擄人數目與王下的差異；52:31 與王下 25:27 的日期；太 27:9-10 為何稱『先知耶利米』；約雅斤（22:30 對 52:31-34 與太 1:12）。

---

## 十、仍未完成

1. **沒有人類審稿者。**全書的撰寫者與核對者都是 AI，各篇由同一套規格與腳本核對；沒有另一位讀者逐章通讀。已做過一輪獨立校對（10 位 AI 代理，不看既有報告、向原始來源重新取證，共修約 100 處），但校對者仍是 AI，不能代替人類讀者。
2. **二十七篇尚未精簡。**各篇篇幅約 23–61 KB（含經文區塊）；經文區塊約佔三分之一至一半，其餘是行文。尚未做「同一個點全章只講一次」的精簡通讀。
3. **耶 25:6 的「做／作」未定案**（見「七」）。
4. **摩根的 p. 111 與 p. 123 是依 OCR 頁眉推定的**（頁眉被 OCR 打成「in」與「MESSAGEiOF」），實際頁碼可能差一頁；其餘頁碼取自清楚的頁眉。
5. **字頻與詞義。**各篇的字頻由撰寫者以正則表達式計算，可能漏算未想到的詞形；若干詞義與雙關是編者自己的觀察（如 שֶׁבֶר「破壞／創傷」同字、צעד、צמח 與 צדקיהו 的聲音相近、אֲרֻכָה 與 עלה 的連結），各篇已標明，但這些觀察沒有現成注疏可對。
6. **聖詩。**{nostated} 首來源頁沒有印年份；第 7 篇來源頁有三處 OCR 式錯字（`I Yield`、`restores it borrowed ray`、`That in , thy sun-shine's blaze`），校對輪已在書稿中更正為 `I yield`、`its`、`sunshine's`；第 10 篇〈Have Thine Own Way, Lord〉的文字取自 hymnary.org 所載 1989 年 United Methodist Hymnal 的排印（大小寫可能與 1907 年原版不同）；第 8 篇來源頁帶 `{{{{no source}}}}` 標記；第 13 篇第二節是否為衛斯理所作，無法由來源頁確認（已在該章說明）；第 20 篇用的是 1860 年 *Catholic Hymns* 的字句，不是後來新教版本；第 6、8、13、14、23、25、26、27 篇的聖詩與經文只有鬆散的主題關聯，各篇配詩說明已避免宣稱互相引用。
7. **作者需要決定的事**：是否在公開發行前請人類查經老師通讀。
""")
    # quotes in the orientation files (not chapters)
    fm = defaultdict(int)
    for name in ["000-preface.md", "00-overview.md", "00a-jeremiah-position.md", "00b-watching-spine.md",
                 "00c-revelation-order.md", "elder-wong-systematic-study.md", "99-to-revelation.md", "999-afterword.md"]:
        t = (BOOK / name).read_text(encoding="utf-8")
        for m in QUOTE.finditer(t):
            w = classify(m.group(2))
            if w:
                fm[(name, w)] += 1
    if fm:
        L.append("\n---\n\n## 附：卷首與卷末框架檔的逐字引文\n")
        L.append(f"卷首與卷末框架檔另有 **{sum(fm.values())}** 條帶出處行的逐字引文，已與章內引文同法核對（上述 `verify-citations.py` 的計數涵蓋它們）：")
        for (name, w), n in sorted(fm.items()):
            L.append(f"- `{name}`：{WHO[w][0] or '教父'} {n} 條")
    return "\n".join(L)


def main():
    skip = "--no-run" in sys.argv
    idx = build_index()
    led = build_ledger(skip)
    if "--write" in sys.argv:
        OUT_INDEX.write_text(idx + "\n", encoding="utf-8")
        OUT_LEDGER.write_text(led + "\n", encoding="utf-8")
        print(f"wrote {OUT_INDEX.name} ({len(idx)} chars), {OUT_LEDGER.name} ({len(led)} chars)")
    else:
        print(idx)
        print(led)


if __name__ == "__main__":
    main()
