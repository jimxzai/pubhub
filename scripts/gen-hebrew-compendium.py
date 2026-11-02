#!/usr/bin/env python3
"""Generate the data-driven parts of Part 2 (卷二：各卷的希伯來文) of books/bible/Biblehebrew.

Inputs : docs/sources/biblehebrew/series-wordstudies.json   (mined by mine-hebrew-wordstudies.py)
         docs/sources/biblehebrew/oshb/*.xml + HebrewStrong.xml
         the OT books' own chapter files (chapter lists and the 「數一數」 sections, quoted verbatim)
Writes : books/bible/Biblehebrew/generated/{stats-part2.json, overview.md, books.md, index.md, index-once.md}
         (every stat is stored with a p2_ prefix: both parts of the book have their own "lemmas" and "rows")
"""
import collections, glob, importlib.util, json, os, re, sys, unicodedata
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "books/bible/Biblehebrew/generated")      # Part 2 (卷二) of the one Hebrew volume
os.makedirs(OUT, exist_ok=True)


def load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "scripts", fn))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


g = load("g", "gen-biblehebrew-data.py")
m = load("m", "mine-hebrew-wordstudies.py")

# label (series folder), 中文書名, 簡稱, OSHB book id(s)
BOOKS = [
    ("genesis", "創世記", "創", ["Gen"]), ("exodus", "出埃及記", "出", ["Exod"]), ("leviticus", "利未記", "利", ["Lev"]),
    ("numbers", "民數記", "民", ["Num"]), ("duetonomy", "申命記", "申", ["Deut"]), ("joshua", "約書亞記", "書", ["Josh"]),
    ("judges", "士師記", "士", ["Judg"]), ("ruth", "路得記", "得", ["Ruth"]), ("1-samuel", "撒母耳記上", "撒上", ["1Sam"]),
    ("2-samuel", "撒母耳記下", "撒下", ["2Sam"]), ("kings", "列王紀上", "王上", ["1Kgs"]), ("kings2", "列王紀下", "王下", ["2Kgs"]),
    ("chronicl1", "歷代志上", "代上", ["1Chr"]), ("chronicl2", "歷代志下", "代下", ["2Chr"]), ("ezra", "以斯拉記", "拉", ["Ezra"]),
    ("nehemiah", "尼希米記", "尼", ["Neh"]), ("esther", "以斯帖記", "斯", ["Esth"]), ("job", "約伯記", "伯", ["Job"]),
    ("psalm", "詩篇", "詩", ["Ps"]), ("proverb", "箴言", "箴", ["Prov"]), ("ecclesiastes", "傳道書", "傳", ["Eccl"]),
    ("songofsolomen", "雅歌", "歌", ["Song"]), ("isaiah", "以賽亞書", "賽", ["Isa"]), ("jeremiah", "耶利米書", "耶", ["Jer"]),
    ("lamentation", "耶利米哀歌", "哀", ["Lam"]), ("ezekiel", "以西結書", "結", ["Ezek"]), ("daniel", "但以理書", "但", ["Dan"]),
    ("hosea", "何西阿書", "何", ["Hos"]), ("Joel", "約珥書", "珥", ["Joel"]), ("Amos", "阿摩司書", "摩", ["Amos"]),
    ("Obadiah", "俄巴底亞書", "俄", ["Obad"]), ("Jonah", "約拿書", "拿", ["Jonah"]), ("Micah", "彌迦書", "彌", ["Mic"]),
    ("Nahum", "那鴻書", "鴻", ["Nah"]), ("habakkuk", "哈巴谷書", "哈", ["Hab"]), ("Zapphaniah", "西番雅書", "番", ["Zeph"]),
    ("Haggai", "哈該書", "該", ["Hag"]), ("zechariah", "撒迦利亞書", "亞", ["Zech"]), ("malachi", "瑪拉基書", "瑪", ["Mal"]),
]
ZH = {b[0]: b[1] for b in BOOKS}
AB = {b[0]: b[2] for b in BOOKS}

ORDER = "אבגדהוזחטיכלמנסעפצקרשת"
FINAL = {"ך": "כ", "ם": "מ", "ן": "נ", "ף": "פ", "ץ": "צ"}


def skeleton(s):
    s = re.sub(r"[^א-ת]", "", s)
    return [ORDER.index(FINAL.get(c, c)) for c in s]


# Strong's first clause is sometimes useless ("hence (the ox's head being the first letter…" for 'thousand'); these are the
# frequent ones, replaced by a plain English equivalent that says what the word means.
DEF_FIX = {"505": "a thousand", "518": "if (conditional particle)", "1696": "to speak", "853": "(not translated) sign of the definite direct object",
           "160": "love (noun)", "3069": "YHWH, pointed as Elohim after Adonai", "430": "God, gods"}


def lexicon_defs():
    root = ET.parse(os.path.join(g.SRC, "HebrewStrong.xml")).getroot()
    out = {}
    for e in root.iter(g.LEXNS + "entry"):
        mm = e.find(g.LEXNS + "meaning"); us = e.find(g.LEXNS + "usage")
        txt = re.sub(r"\s+", " ", "".join(mm.itertext()).strip() if mm is not None else "")
        first = re.split(r";", txt)[0].strip(" .,")
        if not first and us is not None:                      # no definition: fall back to the KJV renderings listed under <usage>
            first = "KJV: " + re.sub(r"\s+", " ", "".join(us.itertext())).strip(" .,")
        first = re.sub(r"\s*\[[^\]]*\]", "", first)         # drop editorial bracket notes in the lexicon text
        out[e.get("id")] = (first[:80] + ("…" if len(first) > 80 else ""))
    out.update({"H" + k: v for k, v in DEF_FIX.items()})
    return out


def clean_gloss(s):
    # a cell that quotes several words ("「喜歡」「施恩」「好處」「善」") or states a count ("頸項三處", "全書七次") is a note
    # about the passage, not a gloss of one word: running the quotes together produced "喜歡施恩好處善"
    if s.count("「") >= 2 or re.search(r"[一二三四五六七八九十兩\d]+\s*(處|次|節)|全書|一節之內", s): return ""
    s = re.split(r"[；;。]", s)[0]
    s = re.sub(r"[「」『』]", "", s)
    s = re.sub(r"[（(][^）)]*[）)]", "", s).strip(" ，、:：")
    if not s or len(s) > 20 or re.search(r"[֐-׿]", s) or "NASB" in s or "和合本" in s: return ""
    return s


def widen_cols(body, minw=8):
    """Layout only: give every column of a quoted table at least `minw` dashes in its separator row, so a narrow
    column (the author's "次數" column) cannot overflow by a point or two. The quoted text is not touched."""
    def fix(m):
        cells = m.group(0).strip().strip("|").split("|")
        out = []
        for c in cells:
            c = c.strip(); l = c.startswith(":"); r = c.endswith(":")
            out.append((":" if l else "") + "-" * max(len(c.strip(":")), minw) + (":" if r else ""))
        return "|" + "|".join(out) + "|"
    return re.sub(r"^\|\s*:?-{2,}:?\s*(?:\|\s*:?-{2,}:?\s*)+\|\s*$", fix, body, flags=re.M)


def is_chapter(tok):
    """A chapter file is numbered 01-95. 00x (preface, overview, position) and 96-99 (appendices) are not chapters."""
    m = re.match(r"\d+", tok)
    return bool(m) and 1 <= int(m.group()) <= 95


def chap_no(c):
    """01 -> '1', 02a -> '2a'; a non-chapter file keeps its own token ('00c', '99a') so it is never shown as '0' or 'c'."""
    return re.sub(r"^0+", "", c) if is_chapter(c) else c


def main():
    mined = json.load(open(os.path.join(g.SRC, "series-wordstudies.json"), encoding="utf-8"))
    rows = mined["rows"]
    lex = {k: (g.FORM_FIX.get(k[1:], v[0]), v[1]) for k, v in g.lexicon().items()}; defs = lexicon_defs()
    toks = list(g.tokens())
    oshb_ids = {t[0].split(".")[0] for t in toks}
    for _, _, _, ids in BOOKS:
        for i in ids:
            assert i in oshb_ids, f"OSHB has no book id {i}"
    cnt_all = collections.Counter(); cnt_book = collections.Counter()
    for ref, l, mo, t in toks:
        k = g.key_of(l); cnt_all[k] += 1; cnt_book[(ref.split(".")[0], k)] += 1

    # --- how reliable is the form -> lemma matching? (the miner records, per row, how each word was matched)
    amb_rows = sum(1 for r in rows if r.get("amb"))
    methods = collections.Counter(x for r in rows for x in r.get("methods", []))
    # --- per lemma / per book aggregation
    lem = collections.defaultdict(lambda: {"loc": collections.defaultdict(set), "gl": collections.Counter(),
                                            "cf": collections.Counter(),
                                            "bgl": collections.defaultdict(collections.Counter), "rows": 0})
    NF = lambda x: unicodedata.normalize("NFC", m.pointed(x).replace("\u05BE", ""))
    perbook_ch = collections.defaultdict(lambda: collections.defaultdict(set))
    perbook_rows = collections.Counter(); perbook_tblchap = collections.defaultdict(set)
    for r in rows:
        perbook_rows[r["book"]] += 1
        if is_chapter(r["chapter"]): perbook_tblchap[r["book"]].add(r["chapter"])      # same rule as the chapter list
        words = [w for w in re.split(r"[\s־/／、,，（）()]+", r["hebrew"]) if m.HEB.search(w)]
        for k in r["lemmas"]:
            e = lem[k]; e["loc"][r["book"]].add(r["chapter"]); e["rows"] += 1
            perbook_ch[r["book"]][k].add(r["chapter"])
            if len(words) == 1:
                gl = clean_gloss(r["meaning"])
                if gl:
                    e["gl"][gl] += 1; e["bgl"][r["book"]][gl] += 1
                    if "H" + k in lex and NF(words[0]) == NF(lex["H" + k][0]): e["cf"][gl] += 1

    def series_gloss(k, book=None):
        """book given: that book's own wording (context-bound); otherwise only a bare-dictionary-form row."""
        if book:
            return lem[k]["bgl"][book].most_common(1)[0][0] if lem[k]["bgl"].get(book) else ""
        return lem[k]["cf"].most_common(1)[0][0] if lem[k]["cf"] else ""

    def content(k):
        e = lex.get("H" + k)
        return bool(e) and (e[1] == "v" or e[1] == "a" or (e[1].startswith("n") and not e[1].startswith("n-pr")))

    # --- chapter lists and 數一數 sections, straight from the books
    chapters = collections.defaultdict(list); sections = collections.defaultdict(list)
    for label, f in m.source_files():
        base = os.path.basename(f)
        mo = re.match(r"(\d{2,3}[a-z]?)-", base)
        t = open(f, encoding="utf-8").read()
        if mo and is_chapter(mo.group(1)):
            h1 = re.search(r"^# (.+)$", t, re.M)
            lines = t.split("\n")
            hi = next((i for i, l in enumerate(lines) if l.startswith("# ")), None)
            # the passage line right under the title, e.g. 「約書亞記 6:1-27」 -> "6:1-27"
            pl = next((l.strip() for l in (lines[hi + 1:hi + 8] if hi is not None else [])
                       if re.match(r"^[\u4e00-\u9fff]{1,8}\s*\d+(?:[:：]\d+)?[\s\-–—~～至,，、;；:：\d]*$", l.strip()) and len(l.strip()) < 40), "")
            passage = re.sub(r"^[\u4e00-\u9fff]+\s*", "", pl).replace("：", ":")
            chapters[label].append((mo.group(1), re.sub(r"\s*[(（].*$", "", h1.group(1)).strip() if h1 else "", passage))
        for mm in re.finditer(r"^##\s+([^\n]*(?:數一數|鑰字|重複的字|關鍵詞)[^\n]*)\n(.*?)(?=^## |\Z)", t, re.S | re.M):
            if m.HEB.search(mm.group(2)):
                sections[label].append((f.split("/books/bible/")[1], mm.group(1).strip(), mm.group(2).strip("\n")))

    n_tbl_books = sum(1 for v in perbook_tblchap.values() if v)
    n_tbl_chap = sum(len(v) for v in perbook_tblchap.values())
    # --- overview table
    ov = ["| 書卷 | 本系列章數 | 有原文研讀表的章 | 研讀列數 | 討論過的詞目 |", "|----------------|--------|--------|--------|--------|"]
    tot_rows = 0
    for label, zh, ab, ids in BOOKS:
        nlem = sum(1 for k, e in lem.items() if label in e["loc"])
        ov.append(f"| {zh} | {len(chapters[label])} | {len(perbook_tblchap[label])} | {perbook_rows[label]:,} | {nlem:,} |")
        tot_rows += perbook_rows[label]
    open(os.path.join(OUT, "overview.md"), "w", encoding="utf-8").write("\n".join(ov) + "\n")

    # --- per-book digest
    bk = []
    for n, (label, zh, ab, ids) in enumerate(BOOKS, 1):
        bk.append(f"# {zh} {{.unnumbered}}\n")
        nch = len(chapters[label]); nt = len(perbook_tblchap[label])
        if nt == 0:
            bk.append(f"本系列《{zh}》共 {nch} 章；章節裏沒有帶希伯來文的〈原文研讀〉表格，所以這一卷在下面的詞目總索引裏沒有條目。\n")
        else:
            bk.append(f"本系列《{zh}》共 {nch} 章，其中 {nt} 章有〈原文研讀〉表格，共 {perbook_rows[label]:,} 列。\n")
        if chapters[label]:
            bk.append("**章次（括號是這一章研讀的經文）：** " + "；".join(f"{chap_no(c)} {t}" + (f"（{ps}）" if ps else "") for c, t, ps in chapters[label]) + "\n")
        cand = []
        for k, chs in perbook_ch[label].items():
            if len(chs) >= 2 and content(k):
                inb = sum(cnt_book[(i, k)] for i in ids)
                cand.append((len(chs), inb, k))
        cand.sort(key=lambda x: (-x[0], -x[1], x[2]))
        if cand[:8]:
            bk.append("**這一卷討論最多的字**（至少在兩章被討論過，專有名詞不列；依討論的章數排序）：\n")
            bk.append("| 原文 | 系列在這卷的說法（隨上下文） | 本卷出現 | 全舊約 | 討論的章 |")
            bk.append("|------------|--------------------|--------|--------|------------------|")
            for nchs, inb, k in cand[:8]:
                chs = sorted(perbook_ch[label][k], key=lambda c: (len(re.sub(r"\D", "", c)), c))
                bk.append(f"| {lex['H' + k][0]} | {series_gloss(k, label) or '—'} | {inb:,} | {cnt_all[k]:,} | {'、'.join(chap_no(c) for c in chs)} |")
            bk.append("")
        for path, title, body in sections.get(label, []):
            bk.append(f"**系列原文**（`{path}`，〈{re.sub(chr(10), ' ', title)}〉一節，原樣收錄）：\n")
            body = widen_cols(re.sub(r"^(#{1,6}) ", "", body, flags=re.M))
            bk.append(body + "\n")
    open(os.path.join(OUT, "books.md"), "w", encoding="utf-8").write("\n".join(bk))

    # --- alphabetical lemma index
    entries = []
    for k, e in lem.items():
        if "H" + k not in lex: continue            # the pseudo-lemmas l/b/k/m have no dictionary entry
        form, pos = lex["H" + k]
        entries.append((skeleton(form), k, form, pos, e))
    entries.sort(key=lambda x: (x[0], x[1]))
    hdr = ["| 原文 | 意思 | 全舊約 | 見（書 章次） |", "|--------------|----------------------------------|----------|--------------------------|"]
    ix, ix1 = list(hdr), ["| 原文 | 強氏編號，全舊約次數，系列怎麼說 | 見（書 章次） |", "|----------------|--------------------------------|------------------------------|"]
    multi = 0; locators = 0
    for _, k, form, pos, e in entries:
        loc = []
        for label, *_ in BOOKS:
            if label in e["loc"]:
                chs = sorted(e["loc"][label], key=lambda c: (len(re.sub(r"\D", "", c)), c))
                loc.append(f"{AB[label]} {'、'.join(chap_no(c) for c in chs)}")
        nchap = sum(len(v) for v in e["loc"].values()); locators += nchap
        sg = series_gloss(k)
        sd = defs.get("H" + k, "")
        if nchap >= 2:
            multi += 1
            mean = (f"系列：{sg}；" if sg else "") + (f"Strong H{k}：{sd}" if sd else f"H{k}")
            ix.append(f"| {form} | {mean} | {cnt_all[k]:,} | {'；'.join(loc)} |")
        else:                                           # discussed in one chapter only: ONE line, no English definition
            ix1.append(f"| {form} | H{k}，{cnt_all[k]:,} 次" + (f"，{sg}" if sg else "") + f" | {'；'.join(loc)} |")
    open(os.path.join(OUT, "index.md"), "w", encoding="utf-8").write("\n".join(ix) + "\n")
    open(os.path.join(OUT, "index-once.md"), "w", encoding="utf-8").write("\n".join(ix1) + "\n")

    stats = {"rows": len(rows), "lemmas": len(entries), "lemmas_multi": multi, "lemmas_once": len(entries) - multi, "books_with_tables": n_tbl_books,
             "books_total": len(BOOKS), "chapters_total": sum(len(v) for v in chapters.values()),
             "tblchapters_total": n_tbl_chap,
             "sections": sum(len(v) for v in sections.values()), "sections_books": len(sections),
             "ambiguous_rows": amb_rows, "ambiguous_pct": round(amb_rows / len(rows) * 100),
             "m_verse": methods["verse"], "m_form": methods["form"], "m_vcons": methods["verse-consonants"], "m_freq": methods["freq"],
             "m_stem": methods["stem"], "m_none": methods["none"], "locators": locators,
             "m_total": sum(methods.values()), "m_verse_pct": round(methods["verse"] / sum(methods.values()) * 100),
             "m_exact_pct": round((methods["verse"] + methods["form"]) / sum(methods.values()) * 100),
             "unmatched_rows": sum(1 for r in rows if not r["lemmas"]),
             "tokens": len(toks), "lemmas_oshb": len(cnt_all)}
    json.dump({"p2_" + k: v for k, v in stats.items()}, open(os.path.join(OUT, "stats-part2.json"), "w"), ensure_ascii=False, indent=1)
    print(stats)


if __name__ == "__main__":
    main()
