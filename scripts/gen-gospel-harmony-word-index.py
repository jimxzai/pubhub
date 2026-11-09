#!/usr/bin/env python3
"""Generate 98b-appendix-word-index.md for the Gospel Harmony volume.

Two indexes derived mechanically from the chapters (never by hand):

  (a) 希臘字詞索引 — every Greek headword in a station's 「原文研讀」 table
      (first column), with its transliteration, gloss and the stations that
      study it. Headwords written 「A ／ B」 are indexed under both.
  (b) 人名地名索引 — a FIXED, reviewable list of persons and places (below).
      A station is listed for a name when the name occurs in that chapter's
      prose or Scripture at least MIN times; counting is plain string match,
      so the list is reviewable and nothing is indexed that the author did
      not choose.

Usage:  gen-gospel-harmony-word-index.py --write | --check
"""
import re, sys, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "books/bible/gospel-harmony"
OUT = BOOK / "98b-appendix-word-index.md"
MIN = 2

PERSONS = ["亞伯拉罕", "以撒", "雅各", "摩西", "亞倫", "約書亞", "大衛", "所羅門", "以利亞", "以利沙",
           "以賽亞", "耶利米", "以西結", "但以理", "施洗約翰", "以利沙伯", "撒迦利亞", "馬利亞", "約瑟",
           "西面", "亞拿", "希律", "彼得", "安得烈", "腓力", "拿但業", "尼哥底母", "馬大", "拉撒路",
           "猶大", "多馬", "馬太", "彼拉多", "該亞法", "亞那", "巴拉巴", "抹大拉", "迦瑪列", "保羅",
           "撒但", "亞當", "撒該", "亞居拉", "亞波羅", "約翰福音的作者"]
PERSONS.remove("約翰福音的作者")
PLACES = ["伯利恆", "拿撒勒", "迦拿", "迦百農", "耶路撒冷", "伯大尼", "加利利", "撒馬利亞", "耶利哥",
          "以馬忤斯", "客西馬尼", "各各他", "橄欖山", "約但河", "西奈", "埃及", "巴比倫", "以弗所",
          "士每拿", "別迦摩", "推雅推喇", "撒狄", "非拉鐵非", "老底嘉", "拔摩", "錫安", "示劍",
          "提比哩亞", "伯賽大", "畢士大", "西羅亞", "該撒利亞腓立比", "何烈山", "曠野", "聖殿"]
GREEK = re.compile(r"[Ͱ-Ͽἀ-῿]")


def stations():
    for p in sorted(BOOK.glob("[0-3][0-9]-*.md")):
        n = int(p.name[:2])
        if n == 0:
            continue
        yield n, p.read_text(encoding="utf-8")


def strip_acc(s):
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def greek_entries():
    ent = {}
    for n, t in stations():
        a = t.find("## 原文研讀")
        if a < 0:
            continue
        b = t.find("\n## ", a + 5)
        for line in t[a:b].split("\n"):
            if not line.startswith("|") or set(line) <= set("|- "):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 3 or not GREEK.search(cells[0]):
                continue
            heads = [h.strip() for h in re.split(r"[／/]", cells[0]) if GREEK.search(h)]
            trans = [x.strip(" *") for x in re.split(r"[／/]", cells[1])] if len(cells) > 1 else []
            for i, h in enumerate(heads):
                h = re.sub(r"[()（）,.;·]", "", h).strip()
                if not h:
                    continue
                tr = trans[i] if i < len(trans) else (trans[0] if trans else "")
                gls = [x.strip() for x in re.split(r"[／/]", cells[2])]
                gl = gls[i] if len(heads) > 1 and len(gls) == len(heads) else cells[2]
                d = ent.setdefault(h, {"tr": tr, "gl": gl, "st": set()})
                d["st"].add(n)
    return ent


def name_entries():
    res = {}
    texts = list(stations())
    for name in PERSONS + PLACES:
        hit = [n for n, t in texts if t.count(name) >= MIN]
        if hit:
            res[name] = hit
    return res


def render():
    g = greek_entries()
    out = ["---", "title: 耶穌基督完整生平", "subtitle: The Complete Life of Jesus Christ",
           "author: PubHub 三書精讀系統", "date: 2026年11月", "publisher: 三書精讀出版系統", "---", "",
           "# 附錄：字詞與人名地名索引 (Appendix: Word and Name Index)", "",
           "本附錄由各章的「原文研讀」表格與固定的人名地名清單自動編製（建置時重新產生）。"
           f"人名地名只列出在該站出現至少 {MIN} 次者；數字是「站」。", "", "---", "",
           "## 附錄三：希臘字詞索引 (Greek Word Index)", "",
           "| 希臘字 | 音譯 | 意義 | 站 |", "|----------------|--------------|----------------------|--------|"]
    for h in sorted(g, key=strip_acc):
        d = g[h]
        gl = d["gl"].replace("|", "／")
        out.append(f"| {h} | {d['tr']} | {gl} | {'、'.join(map(str, sorted(d['st'])))} |")
    nm = name_entries()
    for title, lst in (("附錄四：人名索引 (Index of Persons)", PERSONS), ("附錄五：地名索引 (Index of Places)", PLACES)):
        out += ["", "---", "", "## " + title, "", "| 名 | 站 |", "|--------------|--------------------------------------------|"]
        for name in lst:
            if name in nm:
                out.append(f"| {name} | {'、'.join(map(str, nm[name]))} |")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--write"
    text = render()
    if mode == "--check":
        cur = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        print("current" if cur == text else "STALE")
        sys.exit(0 if cur == text else 1)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {text.count(chr(10))} lines")
