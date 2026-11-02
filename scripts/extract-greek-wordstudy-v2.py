#!/usr/bin/env python3
"""Mine ALL NT books' Greek word-study tables and verify them against MorphGNT SBLGNT (v2, final).

Covers all 27 books (incl. pauline-epistles/<book>/), every table layout that has a Greek column (with or without a
verse column), single-chapter books, and verse references quoted inside a note. Each row is graded by what could be
checked:

  A   every headword word occurs in the cited verse(s) (from the location column, else from own-book N:M references
      in the note/gloss). Only the verses that really contain a headword word are listed.
  B   no usable verse, but every headword word occurs in 1-2 chapters that the source file discusses (the chapters of
      the file's own verse references). Only chapters that really contain the word are listed.
  C   no verse/chapter evidence (or a wider chapter set, which says nothing specific): the words occur in the book.
  X   fails the check for its strongest available level (dropped).

'lemmas' are the true corpus lemmas of the matched words (an inflected headword is mapped to its lemma using the
accented form first, so εἰς never becomes εἷς); 'key' is the rarest content lemma.
Writes docs/sources/biblegreek/wordstudy-ledger-v2.tsv.  Also prints chapter-inference quality measured on A rows.
"""
import collections, glob, json, os, re, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = os.path.join(ROOT, "books/bible")
CORPUS = os.path.join(ROOT, "docs/sources/biblegreek/morphgnt")
OUT = os.path.join(ROOT, "docs/sources/biblegreek/wordstudy-ledger-v2.tsv")

DIRS = {
    "matthew": "61-Mt", "gospel-of-matthew": "61-Mt",
    "gospel-of-mark": "62-Mk", "gospel-of-luke": "63-Lk",
    "gospel-of-john": "64-Jn", "gospel-of-john-nasb": "64-Jn", "gospel-of-john-niv": "64-Jn",
    "gospel-of-john-nkjv": "64-Jn", "gospel-of-john-translations": "64-Jn", "john-thursday-wong": "64-Jn",
    "acts": "65-Ac", "roman": "66-Ro", "pauline-epistles/romans": "66-Ro",
    "1cor": "67-1Co", "pauline-epistles/1-corinthians": "67-1Co", "cor2": "68-2Co", "pauline-epistles/2-corinthians": "68-2Co",
    "galatian": "69-Ga", "pauline-epistles/galatians": "69-Ga", "ephisian": "70-Eph", "pauline-epistles/ephesians": "70-Eph",
    "philipian": "71-Php", "pauline-epistles/philippians": "71-Php", "pauline-epistles/colossians": "72-Col",
    "thessanlonian1": "73-1Th", "pauline-epistles/1-thessalonians": "73-1Th",
    "thessanlonian2": "74-2Th", "pauline-epistles/2-thessalonians": "74-2Th",
    "pauline-epistles/1-timothy": "75-1Ti", "pauline-epistles/2-timothy": "76-2Ti", "pauline-epistles/titus": "77-Tit",
    "1philimon": "78-Phm", "pauline-epistles/philemon": "78-Phm", "hebrews": "79-Heb", "james": "80-Jas",
    "1-peter": "81-1Pe", "2-peter": "82-2Pe", "john1": "83-1Jn", "john2": "84-2Jn", "john3": "85-3Jn",
    "jude": "86-Jud", "revelation": "87-Re",
}
ONE_CHAPTER = {"78-Phm", "84-2Jn", "85-3Jn", "86-Jud"}
ABBR = {"61-Mt": "太馬太福音", "62-Mk": "可馬可福音", "63-Lk": "路路加福音", "64-Jn": "約約翰福音", "65-Ac": "徒使徒行傳",
        "66-Ro": "羅羅馬書", "67-1Co": "林前哥林多前書", "68-2Co": "林後哥林多後書", "69-Ga": "加加拉太書", "70-Eph": "弗以弗所書",
        "71-Php": "腓腓立比書", "72-Col": "西歌羅西書", "73-1Th": "帖前帖撒羅尼迦前書", "74-2Th": "帖後帖撒羅尼迦後書",
        "75-1Ti": "提前提摩太前書", "76-2Ti": "提後提摩太後書", "77-Tit": "多提多書", "78-Phm": "門腓利門書", "79-Heb": "來希伯來書",
        "80-Jas": "雅雅各書", "81-1Pe": "彼前彼得前書", "82-2Pe": "彼後彼得後書", "83-1Jn": "約壹約翰一書", "84-2Jn": "約貳約翰二書",
        "85-3Jn": "約參約翰三書", "86-Jud": "猶猶大書", "87-Re": "啟啟示錄"}
ABBR_RE = {b: re.compile(r"^\s*(?:" + "|".join(sorted(set(re.findall(r"[約林帖提彼][前後壹貳參一二三]|[\u4e00-\u9fff]{1,6}", v)), key=len, reverse=True)) + r")\s*(?=\d)") for b, v in ABBR.items()}

GREEK = re.compile(r"[\u0370-\u03FF\u1F00-\u1FFF]")
GWORD = re.compile(r"[\u0370-\u03FF\u1F00-\u1FFF]+")
HDR_G = ("希臘文", "原文", "希臘詞", "希臘字", "希臘文詞")
HDR_L = ("出現位置", "出處", "經文", "本章出現處", "節", "出現章節", "章節", "位置")
HDR_M = ("意義", "字義", "意思", "含義", "意義／用法")
HDR_N = ("註解", "說明", "備註", "註釋", "重點", "出現次數／說明", "出現次數")
# not treated as a studied word when choosing the 'key' lemma (articles, prepositions, conjunctions, pronouns)
STOP_POS = {"RA", "C-", "P-", "RP", "RD", "RR", "RI"}


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c)).replace("ς", "σ")


def acc(s):
    return unicodedata.normalize("NFC", re.sub(r"[^\w]", "", s).lower())


def new_pool():
    return {"lemmas": {}, "forms": set(), "facc": {}, "fnorm": {}}


def load():
    verse = {}
    lem_count = collections.Counter(); pos = {}
    book_pool = collections.defaultdict(new_pool); chap_pool = collections.defaultdict(new_pool)
    for f in sorted(glob.glob(os.path.join(CORPUS, "*.txt"))):
        b = os.path.basename(f)[:-4]
        for line in open(f, encoding="utf-8"):
            p = line.split()
            if len(p) != 7:
                continue
            ch, v = int(p[0][2:4]), int(p[0][4:6])
            nl, nf, af = norm(p[6]), norm(re.sub(r"[^\w]", "", p[5])), acc(p[5])
            for pool in (verse.setdefault((b, ch, v), new_pool()), book_pool[b], chap_pool[(b, ch)]):
                pool["lemmas"][nl] = p[6]; pool["forms"].add(nf); pool["facc"][af] = p[6]; pool["fnorm"][nf] = p[6]
            lem_count[p[6]] += 1; pos[p[6]] = p[1]
    return verse, book_pool, chap_pool, lem_count, pos


def merge(pools):
    out = new_pool()
    for p in pools:
        out["lemmas"].update(p["lemmas"]); out["forms"] |= p["forms"]; out["facc"].update(p["facc"]); out["fnorm"].update(p["fnorm"])
    return out


def match(words, pool):
    """All words found in the pool -> (True, [true lemmas]); accented form first, then lemma, then unaccented form."""
    out = []
    for w in words:
        a, n = acc(w), norm(w)
        if a in pool["facc"]: out.append(pool["facc"][a])
        elif n in pool["lemmas"]: out.append(pool["lemmas"][n])
        elif n in pool["fnorm"]: out.append(pool["fnorm"][n])
        else: return False, []
    return True, out


def has_any(words, pool):
    return any(acc(w) in pool["facc"] or norm(w) in pool["lemmas"] or norm(w) in pool["fnorm"] for w in words)


REF = re.compile(r"(?:(\d+):)?(\d+)(?:\s*[-–]\s*(?:(\d+):)?(\d+))?")


def parse_refs(loc, book, default_ch=None):
    loc = re.sub(r"[`*_]", "", loc)
    loc = ABBR_RE[book].sub("", loc, count=1)
    m = re.search(r"[\u4e00-\u9fff「『（(]", loc)
    if m:
        loc = loc[: m.start()]
    loc = loc.replace("，", ",").replace("、", ",").replace("；", ";")
    refs, ch = [], default_ch
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


NOTE_REF = re.compile(r"(?<![\u4e00-\u9fff\w:])(\d{1,3}):(\d{1,3})(?:\s*[-–]\s*(\d{1,3}))?(?![\d:])")


def note_refs(text, nchap):
    """Own-book N:M references quoted in a note (a leading book abbreviation such as 創 or 約 excludes it)."""
    out = []
    for m in NOTE_REF.finditer(re.sub(r"[`*_]", "", text)):
        c, v1, v2 = int(m.group(1)), int(m.group(2)), m.group(3)
        if 1 <= c <= nchap:
            out += [(c, v) for v in range(v1, (int(v2) if v2 and int(v2) >= v1 and int(v2) - v1 < 40 else v1) + 1)]
    return out


def file_chapters(text, nchap):
    cnt = collections.Counter()
    for m in re.finditer(r"(?<![\d:.])(\d{1,3}):(\d{1,3})(?![\d:])", re.sub(r"[`*_]", "", text)):
        c = int(m.group(1))
        if 1 <= c <= nchap:
            cnt[c] += 1
    if not cnt:
        return set()
    top = cnt.most_common(1)[0][1]
    return {c for c, n in cnt.items() if n >= max(2, top // 3)} or {cnt.most_common(1)[0][0]}


def clean_head(cell):
    cell = re.sub(r"\{\\greekfont\s*([^}]*)\}`?\{?=?latex\}?", r"\1", cell)
    cell = re.sub(r"[`*_]", "", cell)
    return re.sub(r"[（(].*?[）)]", " ", cell)


def tables(path):
    lines = open(path, encoding="utf-8", errors="ignore").read().split("\n")
    i = 0
    while i < len(lines) - 2:
        if lines[i].startswith("|") and re.match(r"^\|[\s:\-|]+\|\s*$", lines[i + 1]):
            hdr = [c.strip() for c in lines[i].strip().strip("|").split("|")]
            gi = next((k for k, c in enumerate(hdr) if c in HDR_G), None)
            if gi is not None:
                li = next((k for k, c in enumerate(hdr) if c in HDR_L), None)
                mi = next((k for k, c in enumerate(hdr) if c in HDR_M), None)
                ni = next((k for k, c in enumerate(hdr) if c in HDR_N and k != li), None)
                j = i + 2
                while j < len(lines) and lines[j].startswith("|"):
                    c = [x.strip() for x in lines[j].strip().strip("|").split("|")]
                    if len(c) > gi:
                        yield (c[gi], c[li] if li is not None and li < len(c) else "",
                               c[mi] if mi is not None and mi < len(c) else "",
                               c[ni] if ni is not None and ni < len(c) else "")
                    j += 1
                i = j
                continue
        i += 1


def key_lemma(lemmas, lem_count, pos):
    cand = [l for l in lemmas if l in lem_count and pos.get(l) not in STOP_POS and l != "εἰμί"]
    return min(cand, key=lambda l: lem_count[l]) if cand else ""


def main():
    verse, book_pool, chap_pool, lem_count, pos = load()
    nchap = collections.defaultdict(int)
    for (b, ch, _v) in verse:
        nchap[b] = max(nchap[b], ch)
    seen, rows = set(), []
    inf_tot = inf_true = inf_wide = inf_none = 0     # chapter-inference quality, measured on A rows
    for d, book in DIRS.items():
        base = os.path.join(BOOKS, d)
        if not os.path.isdir(base):
            continue
        for r, _, fs in os.walk(base):
            for f in sorted(fs):
                if not f.endswith(".md"):
                    continue
                path = os.path.join(r, f)
                text = open(path, encoding="utf-8", errors="ignore").read()
                chs = file_chapters(text, nchap[book])
                for head, loc, gloss, note in tables(path):
                    if not GREEK.search(head):
                        continue
                    words = GWORD.findall(clean_head(head))
                    if not words:
                        continue
                    refs = parse_refs(loc, book, 1 if book in ONE_CHAPTER else None)
                    refs = list(dict.fromkeys(refs + note_refs(loc, nchap[book]))) or note_refs(note + " " + gloss, nchap[book])
                    refs_ok = [(c, v) for c, v in refs if (book, c, v) in verse]
                    level, lemmas, shown = "C", [], ""
                    if refs_ok:
                        ok, lems = match(words, merge(verse[(book, c, v)] for c, v in refs_ok))
                        level, lemmas = ("A" if ok else "X"), (lems if ok else [])
                        if ok:
                            hits = [(c, v) for c, v in refs_ok if has_any(words, verse[(book, c, v)])]
                            shown = ";".join(f"{c}:{v}" for c, v in (hits or refs_ok)[:3])
                    chs_ok = sorted(c for c in chs if match(words, chap_pool[(book, c)])[0])
                    if level == "A" and chs:
                        inf_tot += 1
                        true_chs = {c for c, _ in refs_ok}
                        if len(chs_ok) > 2: inf_wide += 1
                        elif not chs_ok: inf_none += 1
                        elif true_chs & set(chs_ok): inf_true += 1
                    if level == "C" and 1 <= len(chs_ok) <= 2:
                        ok, lems = match(words, merge(chap_pool[(book, c)] for c in chs_ok))
                        if ok:
                            level, lemmas, shown = "B", lems, ",".join(map(str, chs_ok))
                    if level == "C":
                        ok, lems = match(words, book_pool[book])
                        level, lemmas = ("C" if ok else "X"), (lems if ok else [])
                    dedupe = (book, " ".join(words), shown.split(";")[0] if shown else (",".join(map(str, chs_ok[:1]))))
                    if dedupe in seen:
                        continue
                    seen.add(dedupe)
                    rows.append((book, " ".join(words), ";".join(lemmas), key_lemma(lemmas, lem_count, pos), level,
                                 shown, gloss, note, os.path.relpath(path, BOOKS)))
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("book\theadword\tlemmas\tkey\tlevel\trefs\tgloss\tnote\tsource\n")
        for r in rows:
            fh.write("\t".join(x.replace("\t", " ").replace("\n", " ") for x in r) + "\n")
    c = collections.Counter(r[4] for r in rows)
    print("rows", len(rows), dict(c))
    pb = collections.defaultdict(collections.Counter)
    for r in rows:
        pb[r[0]][r[4]] += 1
    for b in sorted(ABBR):
        print(f"{b:8s}", dict(pb[b]))
    if inf_tot:
        json.dump({"n": inf_tot, "true": round(inf_true / inf_tot, 3), "wide": round(inf_wide / inf_tot, 3), "none": round(inf_none / inf_tot, 3), "miss": round(1 - (inf_true + inf_wide + inf_none) / inf_tot, 3)},
                  open(os.path.join(os.path.dirname(OUT), "wordstudy-metrics.json"), "w"))
        print(f"chapter inference on {inf_tot} A rows with an inferred chapter set: "
              f"1-2 chapters incl. a true one: {inf_true/inf_tot:.1%}; too wide (>2, demoted to C): {inf_wide/inf_tot:.1%}; "
              f"no chapter contains the word: {inf_none/inf_tot:.1%}")


if __name__ == "__main__":
    main()
