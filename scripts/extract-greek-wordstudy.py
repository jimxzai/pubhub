#!/usr/bin/env python3
"""Mine the repo's Greek word-study tables and verify every row against MorphGNT SBLGNT.

For each table whose header has a Greek column and a verse-location column, each row is
classed:  pass  (every Greek word of the headword occurs, as lemma or surface form, in the cited verse(s))
          fail  (a cited verse parses but a headword word does not occur there)
          noref (no parseable chapter:verse in the location cell)
Only single-book directories are mined (multi-book harmonies are skipped: their refs carry book prefixes).

Writes docs/sources/biblegreek/wordstudy-ledger.tsv and prints a summary.
Usage: extract-greek-wordstudy.py
"""
import collections, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = os.path.join(ROOT, "books/bible")
CORPUS = os.path.join(ROOT, "docs/sources/biblegreek/morphgnt")
LEDGER = os.path.join(ROOT, "docs/sources/biblegreek/wordstudy-ledger.tsv")

DIR2BOOK = {
    "matthew": "61-Mt", "gospel-of-matthew": "61-Mt", "gospel-of-mark": "62-Mk", "gospel-of-luke": "63-Lk",
    "gospel-of-john": "64-Jn", "gospel-of-john-nasb": "64-Jn", "gospel-of-john-niv": "64-Jn",
    "gospel-of-john-nkjv": "64-Jn", "gospel-of-john-translations": "64-Jn", "john-thursday-wong": "64-Jn",
    "acts": "65-Ac", "roman": "66-Ro", "1cor": "67-1Co", "cor2": "68-2Co", "galatian": "69-Ga",
    "ephisian": "70-Eph", "philipian": "71-Php", "thessanlonian1": "73-1Th", "thessanlonian2": "74-2Th",
    "1philimon": "78-Phm", "hebrews": "79-Heb", "james": "80-Jas", "1-peter": "81-1Pe", "2-peter": "82-2Pe",
    "john1": "83-1Jn", "john2": "84-2Jn", "john3": "85-3Jn", "jude": "86-Jud", "revelation": "87-Re",
}
GREEK = re.compile(r"[\u0370-\u03FF\u1F00-\u1FFF]")
GWORD = re.compile(r"[\u0370-\u03FF\u1F00-\u1FFF]+")
HDR_G = ("希臘文", "原文")
HDR_L = ("出現位置", "出處", "經文", "本章出現處", "節")


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.replace("ς", "σ")


def load_corpus():
    verse = {}  # (book, ch, v) -> dict(lemmas:{norm:lemma}, forms:{norm}, text:str)
    for book in sorted(set(DIR2BOOK.values())):
        for line in open(os.path.join(CORPUS, book + "-morphgnt.txt" if False else book + ".txt"), encoding="utf-8"):
            p = line.split()
            if len(p) != 7:
                continue
            ch, v = int(p[0][2:4]), int(p[0][4:6])
            e = verse.setdefault((book, ch, v), {"lemmas": {}, "forms": set(), "words": []})
            e["lemmas"][norm(p[6])] = p[6]
            e["forms"].add(norm(re.sub(r"[^\w]", "", p[5])))
            e["words"].append(p[3])
    return verse


REF = re.compile(r"(?:(\d+):)?(\d+)(?:\s*[-–]\s*(?:(\d+):)?(\d+))?")


def parse_refs(loc):
    """Return a list of (chapter, verse) pairs, or [] if the cell has no ch:v."""
    loc = re.sub(r"[`*_]", "", loc)
    # cut at the first CJK ideograph/quote: what follows is commentary, not a reference
    m = re.search(r"[\u4e00-\u9fff「『（(]", loc)
    if m:
        loc = loc[: m.start()]
    loc = loc.replace("，", ",").replace("、", ",").replace("；", ";")
    refs, ch = [], None
    for part in re.split(r"[;,]", loc):
        part = part.strip()
        if not part:
            continue
        m = REF.fullmatch(part)
        if not m:
            continue
        c1, v1, c2, v2 = m.groups()
        if c1:
            ch = int(c1)
        if ch is None:
            continue
        v1 = int(v1)
        if v2:
            end_ch = int(c2) if c2 else ch
            if end_ch == ch:
                refs += [(ch, v) for v in range(v1, int(v2) + 1)]
            else:
                refs += [(ch, v) for v in range(v1, 80)] + [(end_ch, v) for v in range(1, int(v2) + 1)]
                ch = end_ch
        else:
            refs.append((ch, v1))
    return refs


def clean_head(cell):
    cell = re.sub(r"\{\\greekfont\s*([^}]*)\}`?\{?=?latex\}?", r"\1", cell)
    cell = re.sub(r"[`*_]", "", cell)
    cell = re.sub(r"[（(].*?[）)]", " ", cell)
    return cell


def tables(path):
    lines = open(path, encoding="utf-8", errors="ignore").read().split("\n")
    i = 0
    while i < len(lines) - 2:
        if lines[i].startswith("|") and re.match(r"^\|[\s:\-|]+\|\s*$", lines[i + 1]):
            hdr = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            gi = next((k for k, c in enumerate(hdr) if c in HDR_G), None)
            li = next((k for k, c in enumerate(hdr) if c in HDR_L), None)
            if gi is not None and li is not None:
                mi = next((k for k, c in enumerate(hdr) if c in ("意義", "字義", "意思")), None)
                ni = next((k for k, c in enumerate(hdr) if c in ("註解", "說明")), None)
                j = i + 2
                while j < len(lines) and lines[j].startswith("|"):
                    c = [x.strip() for x in lines[j].strip().strip("|").split("|")]
                    if len(c) >= len(hdr) - 1 and len(c) > max(gi, li):
                        yield (c[gi], c[li], c[mi] if mi is not None and mi < len(c) else "",
                               c[ni] if ni is not None and ni < len(c) else "")
                    j += 1
                i = j
                continue
        i += 1


def main():
    verse = load_corpus()
    seen, rows = set(), []
    for d, book in DIR2BOOK.items():
        base = os.path.join(BOOKS, d)
        if not os.path.isdir(base):
            continue
        for r, _, fs in os.walk(base):
            for f in sorted(fs):
                if not f.endswith(".md"):
                    continue
                for head, loc, gloss, note in tables(os.path.join(r, f)):
                    if not GREEK.search(head):
                        continue
                    h = clean_head(head)
                    words = [w for w in GWORD.findall(h)]
                    refs = parse_refs(loc)
                    status, lemma = "noref", ""
                    if words and refs:
                        pool_l, pool_f = {}, set()
                        for ch, v in refs:
                            e = verse.get((book, ch, v))
                            if e:
                                pool_l.update(e["lemmas"]); pool_f |= e["forms"]
                        if not pool_l:
                            status = "noref"
                        else:
                            lems = []
                            ok = True
                            for w in words:
                                n = norm(w)
                                if n in pool_l:
                                    lems.append(pool_l[n])
                                elif n in pool_f:
                                    lems.append(w)
                                else:
                                    ok = False
                            status = "pass" if ok else "fail"
                            lemma = ";".join(lems) if ok and lems else ""
                    key = (book, " ".join(words), tuple(refs[:1]))
                    if key in seen:
                        continue
                    seen.add(key)
                    rows.append((book, " ".join(words), lemma, loc.strip()[:60], status, gloss, note, f"{d}/{f}"))
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    with open(LEDGER, "w", encoding="utf-8") as fh:
        fh.write("book\theadword\tlemma\tlocation\tstatus\tgloss\tnote\tsource\n")
        for r in rows:
            fh.write("\t".join(x.replace("\t", " ").replace("\n", " ") for x in r) + "\n")
    c = collections.Counter(r[4] for r in rows)
    print("rows", len(rows), dict(c), "pass-rate-of-checkable", round(c["pass"] / max(1, c["pass"] + c["fail"]) * 100, 1))


if __name__ == "__main__":
    main()
