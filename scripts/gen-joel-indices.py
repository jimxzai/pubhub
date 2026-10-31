#!/usr/bin/env python3
"""Generate the Joel volume's appendix of indices (98-appendix-indices.md) from the book's own text.

Same rationale as scripts/gen-joshua-scripture-index.py: a hand-kept index drifts
from the chapters. Three tables, all derived:

  附錄一  Chapter map  — 10 study units <-> the real chapters/verses of Joel
          (the H1 numbering is a plain 1-14 on purpose; this table is where the
          correspondence lives — see eat-bible references/chapter-template.md).
  附錄二  Cross-book Scripture index — every non-Joel reference the chapters make.
  附錄三  Subject index — fixed term list, counted in each chapter's own prose
          (Scripture blocks, hymn blocks and tables of references excluded).

Usage:  python3 scripts/gen-joel-indices.py --write   # rewrite the three generated blocks
        python3 scripts/gen-joel-indices.py           # print them
"""
import importlib.util
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKDIR = ROOT / "books" / "bible" / "joel"
APPENDIX = BOOKDIR / "98-appendix-indices.md"

_spec = importlib.util.spec_from_file_location("john_index", ROOT / "scripts" / "gen-john-scripture-index.py")
john = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(john)
# The John generator leaves John itself out (that book's own text); this book
# cites John often, so put it back and rebuild the parser (same fix as gen-nehemiah-indices.py).
BOOKS = list(john.BOOKS)
BOOKS.insert(next(i for i, (f, _) in enumerate(BOOKS) if f == "路加福音") + 1,
             ("約翰福音", ["約翰福音", "約"]))
ORDER = {full: i for i, (full, _) in enumerate(BOOKS)}
ALIAS = {a: full for full, aliases in BOOKS for a in aliases}
MAXCHAP = dict(john.MAXCHAP, **{"約翰福音": 21})
_SHORT = "|".join(a for a in ALIAS if len(a) == 1)
_LONG = "|".join(sorted((a for a in ALIAS if len(a) > 1), key=len, reverse=True))
REF = re.compile(
    rf"(?:(?<![{john.CJK}A-Za-z0-9])({_SHORT})|(?<![A-Za-z0-9])({_LONG}))"
    rf"\s*(\d+)(?::{john.VERSES})?(?=\s*章?)"
)

AMBIGUOUS = set("但得該拿傳歌書拉珥")
LIST_PUNCT = set("（(、；;/ ")

VOLUME = {1: "卷一·話臨到", 2: "卷一·話臨到", 3: "卷一·話臨到",
          4: "卷二·耶和華的日子", 5: "卷三·歸向", 6: "卷四·回答與澆灌", 7: "卷四·回答與澆灌",
          8: "卷五·列國與錫安", 9: "卷五·列國與錫安", 10: "卷五·列國與錫安"}

SOURCES = [
    ("000-preface.md", "前言"), ("00-overview.md", "卷首·概覽"), ("00a-joel-position.md", "卷首·定位"),
    ("00c-revelation-order.md", "卷首·啟示的次序"), ("elder-wong-systematic-study.md", "卷首·領受總綱"),
] + [(f"{i:02d}", f"第{i}章") for i in range(1, 11)] + [
    ("99-to-pentecost-and-revelation.md", "卷末"), ("999-afterword.md", "跋"),
]

# subject -> regex counted in chapter prose
SUBJECTS = [
    ("耶和華的日子", r"耶和華的日子|大而可畏的日子|這日|日子臨近"), ("蝗蟲", r"蝗蟲|蝻子|螞蚱|剪蟲"), ("軍旅／軍隊", r"軍旅|軍隊|隊伍"),
    ("雖然如此", r"雖然如此"), ("歸向／轉意", r"歸向|轉意|歸回"), ("撕裂心腸", r"撕裂"),
    ("禁食", r"禁食"), ("素祭與奠祭", r"素祭|奠祭"), ("吹角", r"吹角|角聲"),
    ("補還", r"補還"), ("澆灌", r"澆灌"), ("聖靈／靈", r"聖靈|我的靈"), ("凡有血氣的", r"血氣"),
    ("求告", r"求告"), ("知道", r"知道"), ("住在錫安", r"住在錫安|錫安"),
    ("列國", r"列國|萬民|外邦"), ("約沙法谷／斷定谷", r"約沙法|斷定谷"), ("伊甸園", r"伊甸"),
    ("孩子／後代", r"兒女|子孫|後代|孩童"), ("老年人", r"老年人|長老"), ("祭司", r"祭司"),
    ("酒／甜酒", r"甜酒|新酒|酒醡"), ("五旬節", r"五旬節"), ("使徒行傳", r"使徒行傳"), ("啟示錄", r"啟示錄"),
    ("加爾文", r"加爾文"), ("亨利", r"亨利"), ("摩根", r"摩根"), ("麥克阿瑟", r"麥克阿瑟"),
]


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


def source_path(name):
    if name.endswith(".md"):
        return BOOKDIR / name
    hits = sorted(BOOKDIR.glob(f"{name}-*.md"))
    return hits[0] if hits else None


def prose_lines(path):
    """Chapter lines minus the Scripture block, hymn blocks and table rows."""
    out, skip, skip3, in_altar = [], False, False, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            skip = line.startswith(("## 經文", "## 配詩"))
            skip3 = False
            in_altar = False
        elif line.startswith("### "):
            # house-template boilerplate sections every chapter has; counting them
            # would make 壇 / 禱告 / 基督 appear to be subjects of every chapter
            skip3 = line.startswith(("### 禱告回應", "### 默想問題"))
            in_altar = line.startswith("### 今天的祭壇")
        # 今天的祭壇: skip only its 早晨／晚上／一個行動 bullets; the 你看見耶穌了嗎 paragraph that closes it is prose
        if in_altar and line.startswith("- "):
            continue
        if skip or skip3 or line.lstrip().startswith(("|", "> ^")):
            continue
        out.append(line)
    return out


def chapter_map():
    rows = ["| 章 | 約珥書 | 卷 | 章題 | 本章鑰詞 |",
            "|--------|----------------|------------------------|--------------------------------|------------------------------------------|"]
    for i in range(1, 11):
        p = source_path(f"{i:02d}")
        if not p:
            continue
        text = p.read_text(encoding="utf-8")
        h1 = re.search(r"^# (.+)$", text, flags=re.M)
        title = re.sub(r"\s*\(.*\)\s*$", "", h1.group(1)) if h1 else ""
        refline = re.search(r"^約珥書\s*([\d:\-–]+)", text, flags=re.M)
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
            cleaned = re.sub(r"約珥書\s*第?\s*\d+(?::\d+(?:[-–]\d+)?)?|(?<![一-鿿])珥\s*\d+(?::\d+(?:[-–]\d+)?)?", "", line)
            for full, chap in refs_in(cleaned):
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
        for i in range(1, 11):
            p = source_path(f"{i:02d}")
            if p and sum(len(re.findall(pat, l)) for l in prose_lines(p)) >= 2:
                where.append(f"第{i}章")
        if where:
            out.append(f"| {name} | {'、'.join(where)} |")
    return "\n".join(out)


BLOCKS = {"chapter-map": chapter_map, "scripture-index": lambda: scripture_index()[0], "subject-index": subject_index}


def main():
    built = {k: f() for k, f in BLOCKS.items()}
    if "--write" not in sys.argv:
        for k, v in built.items():
            print(f"<!-- gen-{k} -->\n{v}\n")
        return 0
    text = APPENDIX.read_text(encoding="utf-8")
    for k, v in built.items():
        a, b = f"<!-- gen-{k}:start -->", f"<!-- gen-{k}:end -->"
        i, j = text.find(a), text.find(b)
        if i < 0 or j < 0:
            sys.exit(f"markers for {k} not found in {APPENDIX}")
        text = text[:i + len(a)] + "\n" + v + "\n" + text[j:]
    APPENDIX.write_text(text, encoding="utf-8")
    print(f"updated {APPENDIX.name}: map {built['chapter-map'].count(chr(10)) - 1} rows, "
          f"scripture {scripture_index()[1]} rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
