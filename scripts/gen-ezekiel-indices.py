#!/usr/bin/env python3
"""Generate the Ezekiel volume's appendix of indices (98-appendix-indices.md) from the book's own text.

Same rationale as scripts/gen-joshua-scripture-index.py: a hand-kept index drifts
from the chapters. Three tables, all derived:

  附錄一  Chapter map  — 34 study units <-> the real chapters/verses of Ezekiel
          (the H1 numbering is a plain 1-34 on purpose; this table is where the
          correspondence lives — see eat-bible references/chapter-template.md).
  附錄二  Cross-book Scripture index — every non-Ezekiel reference the chapters make.
  附錄三  Subject index — fixed term list, counted in each chapter's own prose
          (Scripture blocks, hymn blocks and tables of references excluded).

Usage:  python3 scripts/gen-ezekiel-indices.py --write   # rewrite the three generated blocks
        python3 scripts/gen-ezekiel-indices.py           # print them
"""
import importlib.util
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKDIR = ROOT / "books" / "bible" / "ezekiel"
APPENDIX = BOOKDIR / "98-appendix-indices.md"

_spec = importlib.util.spec_from_file_location("john_index", ROOT / "scripts" / "gen-john-scripture-index.py")
john = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(john)
ORDER, REF, ALIAS, MAXCHAP = john.ORDER, john.REF, john.ALIAS, john.MAXCHAP

AMBIGUOUS = set("但得該拿傳歌書結")
LIST_PUNCT = set("（(、；;/ ")

VOLUME = {**{i: "卷一·榮耀臨到被擄之地" for i in (1, 2, 3)},
          **{i: "卷二·榮耀離開" for i in range(4, 9)},
          **{i: "卷三·審判的理由" for i in range(9, 19)},
          **{i: "卷四·列國也要知道" for i in range(19, 24)},
          **{i: "卷五·口開了，神自己來" for i in range(24, 30)},
          **{i: "卷六·榮耀回來" for i in range(30, 35)}}

SOURCES = [
    ("000-preface.md", "前言"), ("00-overview.md", "卷首·概覽"), ("00a-ezekiel-position.md", "卷首·定位"),
    ("00b-glory-spine.md", "卷首·骨幹"), ("00c-revelation-order.md", "卷首·啟示的次序"),
    ("elder-wong-systematic-study.md", "卷首·領受總綱"),
] + [(f"{i:02d}", f"第{i}章") for i in range(1, 35)] + [
    ("99-the-glory-returns.md", "卷末"), ("999-afterword.md", "跋"),
]

# subject -> regex counted in chapter prose
SUBJECTS = [
    ("榮耀／榮光", r"榮耀|榮光"), ("榮耀離開", r"離開|離棄"), ("基路伯與活物", r"基路伯|活物"),
    ("人子（神對先知的稱呼）", r"人子"), ("知道我是耶和華", r"知道我是"), ("耶和華的手", r"耶和華的手|靈（原文是手）|手降在"),
    ("靈（氣息、風）", r"新靈|我的靈|氣息|רוּחַ"), ("口／啞口／開口", r"啞口|開口|緘默"), ("守望", r"守望"),
    ("偶像與穢像", r"偶像|穢像|可憎"), ("假先知／假平安", r"假先知|假平安|假女先知"), ("牧人與羊", r"牧人|牧養|羊群"),
    ("新心新靈", r"新心|新靈|肉心|石心"), ("枯骨／骸骨", r"枯骨|骸骨"), ("殿／聖殿", r"聖殿|殿"),
    ("河與水", r"殿中流出|河水|活水"), ("東門／東方", r"東門|朝東|從東"), ("君王與王子", r"君王|王子"),
    ("大衛", r"大衛"), ("撒督與祭司", r"撒督|祭司"), ("歌革與瑪各", r"歌革|瑪各"), ("推羅", r"推羅"),
    ("埃及與法老", r"埃及|法老"), ("以東", r"以東"), ("耶路撒冷", r"耶路撒冷"), ("巴比倫與迦勒底", r"巴比倫|迦勒底"),
    ("被擄", r"被擄"), ("餘剩", r"餘剩|剩下的人|逃脫"), ("約（立約）", r"永遠的約|平安的約|立約"),
    ("安息日", r"安息日"), ("但以理、挪亞、約伯", r"但以理|挪亞|約伯"), ("度量", r"度量|量了|量度"),
    ("婚姻與淫亂的比喻", r"淫亂|淫行|妻子|婚姻"), ("日期", r"初一日|初五日|初十日"),
    ("耶和華的所在／在那裏", r"耶和華的所在|耶和華在那裏"), ("新耶路撒冷", r"新耶路撒冷"),
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


def prose_lines(path, keep_tables=False):
    """Chapter lines minus the Scripture block and hymn blocks (and table rows unless keep_tables)."""
    out, skip, skip3 = [], False, False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            skip = line.startswith(("## 經文", "## 配詩"))
            skip3 = False
        elif line.startswith("### "):
            # house-template boilerplate sections every chapter has; counting them
            # would make 壇 / 禱告 / 基督 appear to be subjects of every chapter
            skip3 = line.startswith(("### 今天的祭壇", "### 禱告回應", "### 默想問題"))
        if skip or skip3 or line.lstrip().startswith("> ^") or (not keep_tables and line.lstrip().startswith("|")):
            continue
        out.append(line)
    return out


def chapter_map():
    rows = ["| 章 | 以西結書 | 卷 | 章題 | 本章鑰詞 |",
            "|--------|----------------|------------------------|--------------------------------|------------------------------------------|"]
    for i in range(1, 35):
        p = source_path(f"{i:02d}")
        if not p:
            continue
        text = p.read_text(encoding="utf-8")
        h1 = re.search(r"^# (.+)$", text, flags=re.M)
        title = re.sub(r"\s*\(.*\)\s*$", "", h1.group(1)) if h1 else ""
        refline = re.search(r"^以西結書\s*([\d:\-–]+)", text, flags=re.M)
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
        for line in prose_lines(p, keep_tables=True):
            cleaned = re.sub(r"(?<![一-鿿])(?:以西結書|以西結|結)\s*\d+(?::\d+(?:[-–]\d+)?)?", "", line)
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
        for i in range(1, 35):
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
