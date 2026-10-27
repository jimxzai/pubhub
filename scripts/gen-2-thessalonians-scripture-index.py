#!/usr/bin/env python3
"""Generate the 2 Thessalonians volume's indices from the book's own text.

Mirrors scripts/gen-james-scripture-index.py, with two lessons applied:
  * chapter files are found by glob (James hard-coded range(1, 6) and
    silently left its seven later chapters out of the index);
  * the build script runs this with --write before every build, so the
    appendix cannot drift from the chapters (Deuteronomy's index went stale
    because regenerating it depended on someone remembering).

Writes two tables into books/bible/thessanlonian2/98-appendix-indices.md:
  - cross-book Scripture index (every non-2-Thessalonians reference -> where)
  - theme index (each theme's search terms -> chapters that use them)

Usage:  python3 scripts/gen-2-thessalonians-scripture-index.py --write
        python3 scripts/gen-2-thessalonians-scripture-index.py --check   # exit 1 if stale
        python3 scripts/gen-2-thessalonians-scripture-index.py --stats
"""
import importlib.util
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOKDIR = ROOT / "books" / "bible" / "thessanlonian2"
APPENDIX = BOOKDIR / "98-appendix-indices.md"
MARKS = {
    "scripture": ("<!-- gen-scripture-index:start -->", "<!-- gen-scripture-index:end -->"),
    "theme": ("<!-- gen-theme-index:start -->", "<!-- gen-theme-index:end -->"),
}

_spec = importlib.util.spec_from_file_location(
    "john_index", ROOT / "scripts" / "gen-john-scripture-index.py")
john = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(john)
ORDER, REF, ALIAS, MAXCHAP = john.ORDER, john.REF, john.ALIAS, john.MAXCHAP

AMBIGUOUS = set("但得該拿傳歌書")
LIST_PUNCT = set("（(、；;/ ")
SELF = re.compile(r"(?:帖後|帖撒羅尼迦後書)\s*\d+(?::\d+(?:[-–]\d+)?)?(?:[,，、；;]\s*\d+(?::\d+(?:[-–]\d+)?)?)*")

FRONT = [
    ("000-preface.md", "前言"),
    ("00-overview.md", "卷首·概覽"),
    ("00a-2thess-position.md", "卷首·定位"),
    ("00c-revelation-order.md", "卷首·骨幹"),
    ("elder-wong-systematic-study.md", "卷首·領受總綱"),
]
BACK = [("999-afterword.md", "跋")]

# theme -> search terms (any match in a chapter counts). Terms are the words
# the chapters actually use; a theme with no hits is reported by --stats.
THEMES = [
    ("主的日子／那日子", ["主的日子", "那日子"]),
    ("主的顯現與降臨", ["顯現", "降臨", "παρουσία", "ἀποκάλυψις"]),
    ("公義的審判", ["審判", "報應", "刑罰"]),
    ("那不法的人／大罪人", ["不法的人", "大罪人", "沉淪之子"]),
    ("那攔阻的", ["攔阻"]),
    ("離道反教", ["離道反教", "ἀποστασία"]),
    ("撒但的運動與迷惑", ["撒但", "迷惑", "虛謊", "生發錯誤"]),
    ("真理與愛真理的心", ["愛真理", "真道", "真理"]),
    ("揀選與呼召", ["揀選", "呼召", "所蒙的召"]),
    ("成聖與聖靈", ["成聖", "成為聖潔", "聖靈"]),
    ("榮耀", ["榮耀", "榮光"]),
    ("站立得穩與教訓（傳統）", ["站立得穩", "堅守", "παράδοσις"]),
    ("動心與驚慌", ["動心", "驚慌", "σαλεύω"]),
    ("冒名書信與親筆", ["冒我名", "親筆", "ἐπιστολή"]),
    ("禱告", ["禱告"]),
    ("主的信實", ["信實"]),
    ("忍耐", ["忍耐", "ὑπομονή"]),
    ("患難與逼迫", ["患難", "逼迫"]),
    ("不按規矩／失序", ["不按規矩", "ἀτάκτως", "失序"]),
    ("做工與吃飯", ["做工", "吃飯"]),
    ("教會紀律與勸戒", ["遠離他", "勸他如弟兄", "記下他"]),
    ("平安", ["平安"]),
    ("恩典", ["恩惠", "恩典", "的恩"]),
    ("兩個國度（塔與壇）", ["巴別", "塔與壇", "兩個國度"]),
    ("但以理書與橄欖山講論", ["但以理", "但9", "但11", "橄欖山"]),
]


MIN_HITS = 2


def chapters():
    return [(p, f"第{int(p.name[:2])}章") for p in sorted(BOOKDIR.glob("0[1-9]-*.md"))]


def sources():
    out = [(BOOKDIR / n, l) for n, l in FRONT]
    out += chapters()
    out += [(BOOKDIR / n, l) for n, l in BACK]
    return [(p, l) for p, l in out if p.exists()]


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


def scripture_index():
    index = defaultdict(set)
    for p, label in sources():
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.lstrip().startswith("> ^"):     # the chapter's own Scripture block
                continue
            for full, chap in refs_in(SELF.sub("", line)):
                if full == "帖撒羅尼迦後書":
                    continue
                index[(full, chap)].add(label)
    return index


def discussion(path):
    """A chapter's own discussion: drop headings, the ## 經文 block (the
    verses themselves) and ## 生命應用 (every chapter has a 禱告回應, which
    made 禱告 match all seven chapters and told the reader nothing)."""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^## 經文.*?(?=^## )", "", text, flags=re.S | re.M)
    text = re.sub(r"^## 配詩.*?(?=^## )", "", text, flags=re.S | re.M)  # hymn lyrics
    text = re.sub(r"^## 生命應用.*?(?=^## )", "", text, flags=re.S | re.M)
    # also drop the 全書座標 line: it summarises the whole book's spine, so it
    # names every theme and would credit every chapter with all of them
    return "\n".join(l for l in text.splitlines()
                     if not l.startswith("#") and "**全書座標**" not in l)


def theme_index():
    rows = []
    for theme, terms in THEMES:
        # a chapter counts only if its own discussion uses the theme's terms
        # at least MIN_HITS times: one passing mention is not a discussion
        hits = [label for p, label in chapters()
                if sum(discussion(p).count(t) for t in terms) >= MIN_HITS]
        rows.append((theme, terms, hits))
    return rows


def render_scripture(index):
    order = {l: i for i, (_, l) in enumerate(sources())}
    keys = sorted(index, key=lambda k: (ORDER.get(k[0], 999), k[1]))
    # separator rows >= 72 chars: pandoc --columns trap, see eat-bible gotchas
    out = ["| 經文 | 本書討論之處 |",
           "|--------------------------|------------------------------------------------------------------------------|"]
    for full, chap in keys:
        labels = sorted(index[(full, chap)], key=lambda l: order.get(l, 999))
        out.append(f"| {full} {chap} | {'、'.join(labels)} |")
    return "\n".join(out)


def render_theme(rows):
    out = ["| 主題 | 本書章 |",
           "|------------------------------------------|----------------------------------------------------------|"]
    for theme, _terms, hits in rows:
        out.append(f"| {theme} | {'、'.join(hits) if hits else '—'} |")
    return "\n".join(out)


def updated_text():
    text = APPENDIX.read_text(encoding="utf-8")
    for key, table in (("scripture", render_scripture(scripture_index())),
                       ("theme", render_theme(theme_index()))):
        start, end = MARKS[key]
        a, b = text.find(start), text.find(end)
        if a < 0 or b < 0:
            sys.exit(f"markers for {key} not found in {APPENDIX}")
        text = text[:a + len(start)] + "\n" + table + "\n" + text[b:]
    return text


def main():
    if "--stats" in sys.argv:
        idx = scripture_index()
        print(f"{len(idx)} book-chapters across {len({k[0] for k in idx})} books")
        for theme, terms, hits in theme_index():
            print(f"  {theme}: {len(hits)} chapters" + ("  <-- no hits" if not hits else ""))
        return 0
    new = updated_text()
    old = APPENDIX.read_text(encoding="utf-8")
    if "--check" in sys.argv:
        if new != old:
            print(f"STALE: {APPENDIX.name} differs from the chapters; run with --write")
            return 1
        print(f"{APPENDIX.name} is current")
        return 0
    if "--write" in sys.argv:
        if new != old:
            APPENDIX.write_text(new, encoding="utf-8")
            print(f"updated {APPENDIX.name}")
        else:
            print(f"{APPENDIX.name} already current")
        return 0
    print(new)
    return 0


if __name__ == "__main__":
    sys.exit(main())
