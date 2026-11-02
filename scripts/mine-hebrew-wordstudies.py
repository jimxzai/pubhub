#!/usr/bin/env python3
"""Mine the 原文研讀 / Word Study tables of every book under books/bible/ for Hebrew rows,
and match each Hebrew word to an OSHB lemma (Strong's number).

Writes docs/sources/biblehebrew/series-wordstudies.json:
  rows:   [{book, file, hebrew, translit, meaning, ref, note}]
  lemmas: {strongs: {books: [...], rows: n, glosses: {gloss: n}}}
Usage: mine-hebrew-wordstudies.py
"""
import collections, glob, json, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location("g", os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen-biblehebrew-data.py"))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)

ROOT = g.ROOT
HEB = re.compile(r"[֐-׿]")
NIQQUD_CANT = "[֑-ׇ]"


def pointed(s):  # drop cantillation only (keeps vowel points)
    return re.sub("[֑-ֽ֯׀ׅׄ]", "", s).replace("/", "")


def consonants(s):
    return re.sub(NIQQUD_CANT, "", s).replace("/", "")


def build_index():
    p, c = collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter)
    for _, lem, _, text in g.tokens():
        k = g.key_of(lem)
        for w in re.split(r"[־ ]", text):
            if not w: continue
            p[pointed(w)][k] += 1
            c[consonants(w)][k] += 1
    return p, c


def lemma_of(word, P, C):
    pw, cw = pointed(word), consonants(word)
    if pw in P: return P[pw].most_common(1)[0][0]
    if cw in C: return C[cw].most_common(1)[0][0]
    return None


# The OT books only. 1-2 Samuel live in a nested folder; the older Chronicles copies in that same
# folder duplicate chronicl1/chronicl2 and are deliberately NOT read (they would double-count).
OT_FOLDERS = ["genesis", "exodus", "leviticus", "numbers", "duetonomy", "joshua", "judges", "ruth", "kings",
              "kings2", "chronicl1", "chronicl2", "ezra", "nehemiah", "esther", "job", "psalm", "proverb",
              "ecclesiastes", "songofsolomen", "isaiah", "jeremiah", "lamentation", "ezekiel", "daniel", "hosea",
              "Joel", "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "habakkuk", "Zapphaniah", "Haggai",
              "zechariah", "malachi"]
OT_SOURCES = {b: [f"books/bible/{b}/*.md"] for b in OT_FOLDERS}
OT_SOURCES["1-samuel"] = ["books/bible/sam1-2-chroni1-2/1-samuel/*.md"]
OT_SOURCES["2-samuel"] = ["books/bible/sam1-2-chroni1-2/2-samuel/*.md"]


def source_files():
    for label, globs in OT_SOURCES.items():
        for g_ in globs:
            for f in sorted(glob.glob(os.path.join(ROOT, g_))):
                yield label, f


def parse_tables():
    out = []
    for label, f in source_files():
        t = open(f, encoding="utf-8").read()
        m = re.search(r"^##\s+[^\n]*(?:原文研讀|Word Study)[^\n]*\n(.*?)(?=^## |\Z)", t, re.S | re.M)
        if not m: continue
        lines = [l for l in m.group(1).split("\n") if l.startswith("|")]
        if len(lines) < 3 or not HEB.search("\n".join(lines)): continue
        cols = [c.strip() for c in lines[0].strip("|").split("|")]
        for l in lines[2:]:
            cells = [c.strip() for c in l.strip().strip("|").split("|")]
            if len(cells) != len(cols) or not HEB.search(cells[0]): continue
            d = dict(zip(cols, cells))
            ref = next((d[k] for k in d if k in ("經文", "出處", "節", "本章出現處", "出現位置") or k.startswith("經文")), "")
            base = os.path.basename(f)
            h1 = re.search(r"^# (.+)$", t, re.M)
            out.append({
                "book": label, "file": f.split("/books/bible/")[1],
                "chapter": (re.match(r"(\d{2,3}[a-z]?)-", base) or [None, ""])[1],
                "title": re.sub(r"\s*[(（].*$", "", h1.group(1)).strip() if h1 else "",
                "hebrew": cells[0], "translit": d.get("音譯", ""),
                "meaning": d.get("意義") or d.get("字義") or "", "ref": ref, "note": d.get("註解", ""),
            })
    return out


LABEL_OSIS = {"genesis": "Gen", "exodus": "Exod", "leviticus": "Lev", "numbers": "Num", "duetonomy": "Deut",
              "joshua": "Josh", "judges": "Judg", "ruth": "Ruth", "1-samuel": "1Sam", "2-samuel": "2Sam", "kings": "1Kgs",
              "kings2": "2Kgs", "chronicl1": "1Chr", "chronicl2": "2Chr", "ezra": "Ezra", "nehemiah": "Neh", "esther": "Esth",
              "job": "Job", "psalm": "Ps", "proverb": "Prov", "ecclesiastes": "Eccl", "songofsolomen": "Song",
              "isaiah": "Isa", "jeremiah": "Jer", "lamentation": "Lam", "ezekiel": "Ezek", "daniel": "Dan", "hosea": "Hos",
              "Joel": "Joel", "Amos": "Amos", "Obadiah": "Obad", "Jonah": "Jonah", "Micah": "Mic", "Nahum": "Nah",
              "habakkuk": "Hab", "Zapphaniah": "Zeph", "Haggai": "Hag", "zechariah": "Zech", "malachi": "Mal"}
PREFIX_LETTERS = "והבלמכש"


def parse_refs(ref):
    """'5:6, 10, 14-15；6:2' -> [(5,6),(5,10),(5,14),(5,15),(6,2)]. Bare numbers inherit the current chapter."""
    out = []
    for seg in re.split(r"[；;]", ref):
        ch = None
        for part in re.split(r"[,，、]", seg):
            part = part.strip()
            m = re.match(r"(?:(\d+):)?(\d+)(?:\s*[-–]\s*(\d+))?", part)
            if not m: continue
            if m.group(1): ch = int(m.group(1))
            if ch is None: continue
            a_, b_ = int(m.group(2)), int(m.group(3) or m.group(2))
            if b_ - a_ <= 30: out += [(ch, v) for v in range(a_, b_ + 1)]
    return out


def main():
    P, C = build_index()
    # verse -> [(pointed form, consonants, lemma key)]  (prefixes included, as printed in the text)
    V = collections.defaultdict(list)
    for ref, lem_, _, text in g.tokens():
        V[ref].append((unicodedata.normalize("NFC", pointed(text).replace("\u05BE", "")), consonants(text).replace("\u05BE", ""), g.key_of(lem_)))
    # consonantal skeleton of every dictionary form -> key (last-resort lookup for prefixed/unmatched forms)
    lexform = collections.defaultdict(set)
    for hid, (form, pos) in g.lexicon().items():
        lexform[consonants(form)].add(hid[1:])
    rows = parse_tables()
    lem = collections.defaultdict(lambda: {"books": set(), "rows": 0, "glosses": collections.Counter()})
    how = collections.Counter()
    for r in rows:
        words = [re.sub(r"[^֐-׿]", "", w) for w in re.split(r"[\s־/／、,，（）()]+", r["hebrew"]) if HEB.search(w)]
        cands = [f"{LABEL_OSIS.get(r['book'], '?')}.{c}.{v}" for c, v in parse_refs(r["ref"])]
        keys = set(); amb = False; methods = []
        for w in words:
            pw = unicodedata.normalize("NFC", pointed(w).replace("\u05BE", "")); cw = consonants(w).replace("\u05BE", "")
            k = None
            for vid in cands:                                    # 1. the very verse the table cites
                for form, cons, key in V.get(vid, ()):
                    if form == pw or cons == cw: k = key; break
                if k: break
            if k: methods.append("verse")
            if not k:                                            # 2. whole-text frequency of this exact form
                d = P.get(pointed(w)) or C.get(cw)
                if d:
                    k = d.most_common(1)[0][0]; methods.append("freq")
                    if d.most_common(1)[0][1] / sum(d.values()) < 0.75: amb = True
            if not k:                                            # 3. strip a prefix letter or two and look the stem up
                for n in (1, 2):
                    if len(cw) > n + 1 and all(ch in PREFIX_LETTERS for ch in cw[:n]):
                        stem = cw[n:]
                        d = C.get(stem)
                        if d: k = d.most_common(1)[0][0]; methods.append("stem"); break
                        if len(lexform.get(stem, ())) == 1: k = next(iter(lexform[stem])); methods.append("stem"); break
            if k: keys.add(k)
            else: methods.append("none")
        r["lemmas"] = sorted(keys); r["amb"] = amb; r["methods"] = methods
        for m_ in methods: how[m_] += 1
        for k in keys:
            e = lem[k]; e["books"].add(r["book"]); e["rows"] += 1
            if len(words) == 1 and r["meaning"]:
                e["glosses"][re.split(r"[；;。]", r["meaning"])[0].strip()] += 1
    out = {"rows": rows, "match_methods": dict(how),
           "lemmas": {k: {"books": sorted(v["books"]), "rows": v["rows"],
                          "glosses": v["glosses"].most_common(5)} for k, v in lem.items()}}
    dst = os.path.join(ROOT, "docs/sources/biblehebrew/series-wordstudies.json")
    json.dump(out, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(rows), "rows;", len(lem), "lemmas;", sum(1 for v in lem.values() if len(v["books"]) >= 5), "in >=5 books;", dict(how))


if __name__ == "__main__":
    main()
