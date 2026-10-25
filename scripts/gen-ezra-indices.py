#!/usr/bin/env python3
"""Generate the Ezra volume's appendix of indices (98-appendix-indices.md) from the book's own text.

Same rationale as scripts/gen-joshua-scripture-index.py: a hand-kept index drifts
from the chapters. Three tables, all derived:

  附錄一  Chapter map  — 14 study units <-> the real chapters/verses of Ezra
          (the H1 numbering is a plain 1-14 on purpose; this table is where the
          correspondence lives — see eat-bible references/chapter-template.md).
  附錄二  Cross-book Scripture index — every non-Ezra reference the chapters make.
  附錄三  Subject index — fixed term list, counted in each chapter's own prose
          (Scripture blocks, hymn blocks and tables of references excluded).

Usage:  python3 scripts/gen-ezra-indices.py --write   # rewrite the three generated blocks
        python3 scripts/gen-ezra-indices.py           # print them
"""
import importlib.util
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKDIR = ROOT / "books" / "bible" / "ezra"
APPENDIX = BOOKDIR / "98-appendix-indices.md"

_spec = importlib.util.spec_from_file_location("john_index", ROOT / "scripts" / "gen-john-scripture-index.py")
john = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(john)
ORDER, REF, ALIAS, MAXCHAP = john.ORDER, john.REF, john.ALIAS, john.MAXCHAP

AMBIGUOUS = set("但得該拿傳歌書拉")
LIST_PUNCT = set("（(、；;/ ")

VOLUME = {1: "卷一·激動與歸回", 2: "卷一·激動與歸回", 3: "卷一·激動與歸回",
          4: "卷二·攔阻與完工", 5: "卷二·攔阻與完工", 6: "卷二·攔阻與完工", 7: "卷二·攔阻與完工",
          8: "卷三·神的手與定志的心", 9: "卷三·神的手與定志的心", 10: "卷三·神的手與定志的心", 11: "卷三·神的手與定志的心",
          12: "卷四·污穢與認罪", 13: "卷四·污穢與認罪", 14: "卷四·污穢與認罪"}

SOURCES = [
    ("000-preface.md", "前言"), ("00-overview.md", "卷首·概覽"), ("00a-ezra-position.md", "卷首·定位"),
    ("00b-hand-spine.md", "卷首·骨幹"), ("00c-revelation-order.md", "卷首·啟示的次序"),
    ("elder-wong-systematic-study.md", "卷首·領受總綱"),
] + [(f"{i:02d}", f"第{i}章") for i in range(1, 15)] + [
    ("99-the-unfinished-return.md", "卷末"), ("999-afterword.md", "跋"),
]

# subject -> regex counted in chapter prose
SUBJECTS = [
    ("激動（神激動人心）", r"激動"), ("神的手／施恩的手", r"神的手|施恩的手|手幫助"),
    ("古列與詔書", r"古列|詔書"), ("大利烏", r"大利烏"), ("亞達薛西", r"亞達薛西"),
    ("所羅巴伯", r"所羅巴伯"), ("耶書亞（大祭司）", r"耶書亞"), ("設巴薩", r"設巴薩"),
    ("哈該與撒迦利亞", r"哈該|撒迦利亞"), ("尼希米", r"尼希米"), ("以斯帖", r"以斯帖"),
    ("祭壇與燔祭", r"祭壇|燔祭|築壇"), ("根基", r"根基"), ("殿", r"聖殿|神殿|殿"),
    ("名冊／譜系", r"名冊|譜系|族譜"), ("利未人", r"利未人"), ("烏陵和土明", r"烏陵|土明"),
    ("撒瑪利亞人／河西", r"撒瑪利亞|河西|達乃"), ("亞蘭文", r"亞蘭"),
    ("律法（摩西）", r"律法"), ("考究遵行教訓", r"考究|遵行|教訓"), ("文士", r"文士"),
    ("禁食", r"禁食"), ("認罪", r"認罪"), ("罪與污穢", r"污穢|可憎|干犯|罪孽"),
    ("外邦女子／分別", r"外邦女子|外邦妻"), ("餘剩／逃脫的人", r"餘剩|逃脫|剩下"),
    ("指望", r"指望"), ("歡喜／歡呼", r"歡喜|歡呼"), ("逾越節", r"逾越"),
    ("新耶路撒冷", r"新耶路撒冷"),
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
    out, skip, skip3 = [], False, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            skip = line.startswith(("## 經文", "## 配詩"))
            skip3 = False
        elif line.startswith("### "):
            # house-template boilerplate sections every chapter has; counting them
            # would make 壇 / 禱告 / 基督 appear to be subjects of every chapter
            skip3 = line.startswith(("### 今天的祭壇", "### 禱告回應", "### 默想問題"))
        if skip or skip3 or line.lstrip().startswith(("|", "> ^")):
            continue
        out.append(line)
    return out


def chapter_map():
    rows = ["| 章 | 以斯拉記 | 卷 | 章題 | 本章鑰詞 |",
            "|--------|----------------|------------------------|--------------------------------|------------------------------------------|"]
    for i in range(1, 15):
        p = source_path(f"{i:02d}")
        if not p:
            continue
        text = p.read_text(encoding="utf-8")
        h1 = re.search(r"^# (.+)$", text, flags=re.M)
        title = re.sub(r"\s*\(.*\)\s*$", "", h1.group(1)) if h1 else ""
        refline = re.search(r"^以斯拉記\s*([\d:\-–]+)", text, flags=re.M)
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
            cleaned = re.sub(r"(?<![一-鿿])(?:以斯拉記|拉)\s*\d+(?::\d+(?:[-–]\d+)?)?", "", line)
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
        for i in range(1, 15):
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
