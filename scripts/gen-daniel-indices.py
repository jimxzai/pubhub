#!/usr/bin/env python3
"""Generate the Daniel volume's appendix of indices (98-appendix-indices.md) from the book's own text.

Same rationale as scripts/gen-joshua-scripture-index.py: a hand-kept index drifts
from the chapters. Three tables, all derived:

  附錄一  Chapter map  — 16 study units <-> the real chapters/verses of Daniel
          (the H1 numbering is a plain 1-14 on purpose; this table is where the
          correspondence lives — see eat-bible references/chapter-template.md).
  附錄二  Cross-book Scripture index — every non-Daniel reference the chapters make.
  附錄三  Subject index — fixed term list, counted in each chapter's own prose
          (Scripture blocks, hymn blocks and tables of references excluded).

Usage:  python3 scripts/gen-daniel-indices.py --write   # rewrite the three generated blocks
        python3 scripts/gen-daniel-indices.py           # print them
"""
import importlib.util
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKDIR = ROOT / "books" / "bible" / "daniel"
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

AMBIGUOUS = set("但得該拿傳歌書拉")
LIST_PUNCT = set("（(、；;/ ")

VOLUME = {1: "卷一·在巴比倫立志",
          2: "卷二·列國之王與天上的神", 3: "卷二·列國之王與天上的神", 4: "卷二·列國之王與天上的神",
          5: "卷二·列國之王與天上的神", 6: "卷二·列國之王與天上的神", 7: "卷二·列國之王與天上的神",
          8: "卷三·四獸與人子", 9: "卷三·四獸與人子", 10: "卷三·四獸與人子",
          11: "卷四·禱告與七十個七", 12: "卷四·禱告與七十個七",
          13: "卷五·看不見的爭戰與結局", 14: "卷五·看不見的爭戰與結局", 15: "卷五·看不見的爭戰與結局", 16: "卷五·看不見的爭戰與結局"}

SOURCES = [
    ("000-preface.md", "前言"), ("00-overview.md", "卷首·概覽"), ("00a-daniel-position.md", "卷首·定位"),
    ("00b-given-spine.md", "卷首·骨幹"), ("00c-revelation-order.md", "卷首·啟示的次序"),
    ("elder-wong-systematic-study.md", "卷首·領受總綱"),
] + [(f"{i:02d}", f"第{i}章") for i in range(1, 17)] + [
    ("99-to-revelation.md", "卷末"), ("999-afterword.md", "跋"),
]

# subject -> regex counted in chapter prose
SUBJECTS = [
    ("賜與／賜給", r"賜與|賜給"), ("交付", r"交付"), ("至高者", r"至高者|至高的神"), ("天上的神", r"天上的神|天上的主"),
    ("國度／國", r"國度"), ("權柄", r"權柄"), ("人子", r"人子"), ("聖民", r"聖民"),
    ("尼布甲尼撒", r"尼布甲尼撒"), ("伯沙撒", r"伯沙撒"), ("大利烏", r"大利烏"), ("古列", r"古列"),
    ("沙得拉、米煞、亞伯尼歌", r"沙得拉|米煞|亞伯尼歌"), ("加百列", r"加百列"), ("米迦勒", r"米迦勒"),
    ("亞蘭文", r"亞蘭"), ("巨像與石頭", r"巨像|石頭"), ("四獸／四國", r"四獸|四國"),
    ("小角", r"小角"), ("安提阿古", r"安提阿古"), ("敵基督", r"敵基督"),
    ("七十個七", r"七十個七|七十個"), ("受膏者", r"受膏者|彌賽亞"), ("可憎／毀壞", r"可憎|毀壞"),
    ("禱告", r"禱告"), ("認罪", r"認罪"), ("禁食", r"禁食"), ("立志", r"立志"),
    ("復活／復醒", r"復醒|復活"), ("冊／書", r"真確書|冊上|案卷"), ("末期／結局", r"末期|結局"),
    ("耶利米", r"耶利米"), ("以斯拉記", r"以斯拉記"), ("啟示錄", r"啟示錄"),
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
    rows = ["| 章 | 但以理書 | 卷 | 章題 | 本章鑰詞 |",
            "|--------|----------------|------------------------|--------------------------------|------------------------------------------|"]
    for i in range(1, 17):
        p = source_path(f"{i:02d}")
        if not p:
            continue
        text = p.read_text(encoding="utf-8")
        h1 = re.search(r"^# (.+)$", text, flags=re.M)
        title = re.sub(r"\s*\(.*\)\s*$", "", h1.group(1)) if h1 else ""
        refline = re.search(r"^但以理書\s*([\d:\-–]+)", text, flags=re.M)
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
            cleaned = re.sub(r"但以理書\s*第?\s*\d+(?::\d+(?:[-–]\d+)?)?|(?<![一-鿿])但\s*\d+(?::\d+(?:[-–]\d+)?)?", "", line)
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
        for i in range(1, 17):
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
