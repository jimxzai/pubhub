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
PLACES = ["伯利恆", "拿撒勒", "迦拿", "迦百農", "耶路撒冷", "伯大尼", "加利利", "撒瑪利亞", "耶利哥",
          "以馬忤斯", "客西馬尼", "各各他", "橄欖山", "約但河", "西奈", "埃及", "巴比倫", "以弗所",
          "士每拿", "別迦摩", "推雅推喇", "撒狄", "非拉鐵非", "老底嘉", "拔摩", "錫安", "示劍",
          "提比哩亞", "伯賽大", "畢士大", "西羅亞", "該撒利亞腓立比", "何烈山", "曠野", "聖殿"]
THEMES = [  # (主題, [比對字串]) — fixed, reviewable; a station is listed at >= THEME_MIN hits
    ("道與話語", ["神的話", "話語", "太初有道", "道成肉身"]),
    ("國度與天國", ["天國", "神的國", "國度"]),
    ("聖殿", ["聖殿", "進殿", "殿裏"]),
    ("逾越節", ["逾越節", "逾越"]),
    ("十字架", ["十字架", "釘十字"]),
    ("復活", ["復活", "復活了"]),
    ("聖靈", ["聖靈"]),
    ("保惠師", ["保惠師"]),
    ("新約與立約", ["新約", "立約", "聖約"]),
    ("赦罪", ["赦罪", "罪得赦", "赦免"]),
    ("重生", ["重生", "生出來"]),
    ("信心與信", ["信心", "相信", "信祂", "信他"]),
    ("懼怕與平安", ["不要怕", "懼怕", "平安"]),
    ("喜樂", ["喜樂", "歡喜"]),
    ("禱告", ["禱告", "祈求"]),
    ("試探", ["試探"]),
    ("悔改", ["悔改"]),
    ("安息日", ["安息日"]),
    ("律法", ["律法", "誡命"]),
    ("先知與預言", ["先知", "預言"]),
    ("彌賽亞與基督", ["彌賽亞", "基督"]),
    ("大衛的子孫", ["大衛的子孫", "大衛的後裔", "大衛的子"]),
    ("人子", ["人子"]),
    ("神的兒子", ["神的兒子", "愛子"]),
    ("羔羊", ["羔羊", "羊羔"]),
    ("牧人與羊", ["牧人", "牧羊", "好牧人"]),
    ("光", ["世界的光", "光明", "光照"]),
    ("生命與永生", ["永生", "生命的糧", "生命"]),
    ("餅與糧", ["餅", "糧", "嗎哪"]),
    ("水與活水", ["活水", "生命水"]),
    ("葡萄樹", ["葡萄樹", "葡萄園"]),
    ("門徒與跟從", ["門徒", "跟從"]),
    ("憐憫與慈心", ["憐憫", "慈心", "動了慈心"]),
    ("審判", ["審判"]),
    ("再來", ["再來", "駕雲", "降臨"]),
    ("榮耀", ["榮耀", "榮光"]),
    ("記號與神蹟", ["記號", "神蹟", "兆頭"]),
    ("見證", ["見證"]),
    ("差遣", ["差遣", "差我來"]),
    ("愛", ["愛心", "彼此相愛", "愛你們"]),
    ("真理", ["真理"]),
    ("僕人與服事", ["僕人", "服事"]),
    ("同住與同在", ["同住", "同在", "住在我們中間"]),
    ("應驗", ["應驗"]),
    ("以馬內利", ["以馬內利"]),
    ("我是（自稱）", ["我是生命的糧", "我是世界的光", "我是好牧人", "我是門", "我就是", "我是道路"]),
    ("受苦與捨命", ["受苦", "捨命", "必須被殺", "受死"]),
    ("門與路", ["窄門", "道路"]),
]
THEME_MIN = 3
GREEK = re.compile(r"[Ͱ-Ͽἀ-῿]")


def stations():
    for p in sorted(BOOK.glob("[0-4][0-9]-*.md")):
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


def theme_entries():
    res = {}
    texts = list(stations())
    for name, keys in THEMES:
        hit = []
        for n, tx in texts:
            body = tx.split("## 與其他經文的關聯")[0]
            if sum(body.count(k) for k in keys) >= THEME_MIN:
                hit.append(n)
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
    th = theme_entries()
    out += ["", "---", "", "## 附錄六：主題索引 (Subject Index)", "",
            f"主題與比對字詞是固定的清單；某站列入該主題，表示該站正文出現相關字詞至少 {THEME_MIN} 次。",
            "", "| 主題 | 站 |", "|--------------|--------------------------------------------|"]
    for name, _ in THEMES:
        if name in th:
            out.append(f"| {name} | {'、'.join(map(str, th[name]))} |")
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
