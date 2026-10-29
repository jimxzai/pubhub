#!/usr/bin/env python3
"""Validate one or more finished chapters. Exit 1 on any ERROR.

  python3 .sources/check_chapter.py books/bible/ezekiel/05-to-the-mountains-of-israel.md [...]

ERROR: YAML changed; wrong H2 list/order; TODO marker left; 經文 block != units file; quote not found
       in .sources (check_quotes.py); no 座標 in 基督焦點; no 鑰詞 line; last paragraph of 老弟兄查經 lacks
       「你看見…了嗎」; Hebrew/Greek letter glued to a CJK char; >3 默想問題; emoji; tab characters;
       Hebrew in the word-study table not found in hebrew/ezekiel-he.tsv; `---` glued under a paragraph.
WARN : HYMN-PENDING left; size outside 15-40 KB; no 直接/間接 in 基督焦點; 活在今天 section present.
"""
import sys, re, subprocess, pathlib
SRC = pathlib.Path(__file__).resolve().parent
BOOK = SRC.parent
H2 = ["基督焦點 (Christ at the Center)","配詩 (Opening Hymn)","經文 (Scripture)","背景 (Context)","原文研讀 (Word Study)",
      "領受要點 (Truths Received)","歷代注疏 (Historical Commentary)","詩篇與聖詩 (Psalm & Hymn)",
      "老弟兄查經 (Reading with the Elder Brother)","生命應用 (Application)","與其他經文的關聯"]
YAML = "---\ntitle: 以西結書研讀\nsubtitle: Ezekiel Deep Study\nauthor: PubHub 三書精讀系統\ndate: 2026年10月\npublisher: 三書精讀出版系統\n---\n"
HEB_ALL = re.sub(r"[֑-ׇ\s]", "", "".join(l.split("\t")[2] for l in open(SRC/"hebrew/ezekiel-he.tsv",encoding="utf8") if not l.startswith("#")))
def sections(text):
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    return {parts[i].strip(): parts[i+1] for i in range(1, len(parts), 2)}
errs = warns = 0
for path in sys.argv[1:]:
    f = pathlib.Path(path); text = f.read_text(encoding="utf8"); name = f.name
    E = lambda m: print(f"ERROR {name}: {m}")
    W = lambda m: print(f"WARN  {name}: {m}")
    n0 = errs
    if not text.startswith(YAML): E("7-line YAML front matter altered"); errs += 1
    secs = sections(text)
    if list(secs) != H2: E(f"H2 list/order differs: {list(secs)}"); errs += 1
    for m in re.finditer(r"<!-- TODO:([^>]*)-->", text): E(f"TODO left: {m.group(1)}"); errs += 1
    if "HYMN-PENDING" in text: W("HYMN-PENDING left"); warns += 1
    stem = f.stem
    unit = SRC/"units"/f"{stem}.scripture.md"
    if unit.exists():
        have = secs.get("經文 (Scripture)", "").strip().rstrip("-").strip()
        if have != unit.read_text(encoding="utf8").strip(): E("## 經文 block differs from units file (paste it verbatim)"); errs += 1
    else: E("no units file for this stem"); errs += 1
    fc = secs.get("基督焦點 (Christ at the Center)", "")
    if "座標" not in fc: E("基督焦點 has no 座標 line"); errs += 1
    if "本章鑰詞" not in fc: E("基督焦點 has no 本章鑰詞 line"); errs += 1
    if "直接" not in fc and "間接" not in fc: W("基督焦點 does not say 直接/間接"); warns += 1
    el = secs.get("老弟兄查經 (Reading with the Elder Brother)", "")
    last = [p for p in el.strip().split("\n\n") if p.strip() and p.strip() != "---"]
    if not last or not re.search(r"你看見.{0,20}了嗎", last[-1]): E("last paragraph of 老弟兄查經 lacks 「你看見…了嗎」"); errs += 1
    if "活在今天" in el: W("活在今天 section present (spec: do not write)"); warns += 1
    ap = secs.get("生命應用 (Application)", "")
    q = re.search(r"### 默想問題(.*?)(?=###|\Z)", ap, flags=re.S)
    if q and len(re.findall(r"^\d+\.", q.group(1), flags=re.M)) > 3: E(">3 默想問題"); errs += 1
    if re.search(r"[֐-׿Ͱ-Ͽἀ-῿][一-鿿]|[一-鿿][֐-׿Ͱ-Ͽἀ-῿]", re.sub(r"\n\|.*", "", text.split("## 經文",1)[0]+text.split("## 背景",1)[1] if "## 背景" in text else text)):
        E("Hebrew/Greek glued to CJK without a space"); errs += 1
    if re.search(r"[\U0001F300-\U0001FAFF☀-➿]", text): E("emoji"); errs += 1
    if "\t" in text: E("tab character"); errs += 1
    if re.search(r"[^\n]\n---\n", text[len(YAML):]): E("`---` directly under a paragraph line (Setext trap): add a blank line before it"); errs += 1
    ws = secs.get("原文研讀 (Word Study)", "")
    for row in ws.splitlines():
        if row.startswith("|") and not row.startswith("|--") and "希伯來文" not in row and "亞蘭文" not in row:
            cell = row.split("|")[1] if row.count("|") > 2 else ""
            hb = re.sub(r"[֑-ׇ\s־־\-—,/（）()]", "", "".join(re.findall(r"[֐-׿]+", cell)))
            if hb and hb not in HEB_ALL: E(f"word-study Hebrew not found in ezekiel-he.tsv: {cell.strip()[:30]}"); errs += 1
    r = subprocess.run([sys.executable, str(SRC/"check_quotes.py"), path], capture_output=True, text=True)
    for line in r.stdout.splitlines():
        if line.startswith("MISS"): E(line); errs += 1
    size = len(text.encode("utf8")) / 1024
    if not 15 <= size <= 40: W(f"size {size:.1f} KB outside 15-40 KB"); warns += 1
    print(f"{'FAIL' if errs > n0 else 'ok  '} {name}  {size:.1f} KB  quotes={sum(1 for l in r.stdout.splitlines() if l[:2] in ('OK','SH'))}")
print(f"-- {errs} errors, {warns} warnings")
sys.exit(1 if errs else 0)
