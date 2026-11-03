#!/usr/bin/env python3
"""Generate Part 2 (各卷的希臘文) of books/bible/Biblegreek from MorphGNT + the verified ledger v2.

Writes books/bible/Biblegreek/p2-*.md :
  p2-00-divider.md            Part-2 opening page (what the tiers mean; totals computed from the ledger)
  p2-01..27-<book>.md         one section per NT book: corpus facts, commonest words, most 'concentrated' words,
                              and every word the series studied in that book (grouped by lemma, with evidence tier)
  p2-90-cross-book-index.md   lemmas studied in >=2 books, with verse-verified places
  p2-91-greek-term-index.md   every studied lemma in Greek alphabetical order -> books
Every Greek form, count, lemma and place comes from the corpus/ledger. The Chinese gloss and note columns are the
series' own word-study text, shown only for rows that passed their tier's check.
"""
import collections, csv, glob, importlib.util, json, os, re, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(ROOT, "docs/sources/biblegreek/morphgnt")
LEDGER = os.path.join(ROOT, "docs/sources/biblegreek/wordstudy-ledger-v2.tsv")
OUT = os.path.join(ROOT, "books/bible/Biblegreek")


def load_mod(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


gc = load_mod("gc", "scripts/gen-biblegreek-context.py")
gd = load_mod("gd", "scripts/gen-biblegreek-data.py")
ZH, SHORT = gc.ZH, gc.SHORT


def ab(b):
    """Book abbreviation as one unbreakable unit (a 2-character one like 約壹 must not split across lines)."""
    s = SHORT[b]
    return "`\\mbox{%s}`{=latex}" % s if len(s) > 1 else s

SHORT.setdefault("72-Col", "西"); SHORT.setdefault("75-1Ti", "提前"); SHORT.setdefault("76-2Ti", "提後"); SHORT.setdefault("77-Tit", "多")
EN = {"61-Mt": "Matthew", "62-Mk": "Mark", "63-Lk": "Luke", "64-Jn": "John", "65-Ac": "Acts", "66-Ro": "Romans",
      "67-1Co": "1 Corinthians", "68-2Co": "2 Corinthians", "69-Ga": "Galatians", "70-Eph": "Ephesians", "71-Php": "Philippians",
      "72-Col": "Colossians", "73-1Th": "1 Thessalonians", "74-2Th": "2 Thessalonians", "75-1Ti": "1 Timothy",
      "76-2Ti": "2 Timothy", "77-Tit": "Titus", "78-Phm": "Philemon", "79-Heb": "Hebrews", "80-Jas": "James",
      "81-1Pe": "1 Peter", "82-2Pe": "2 Peter", "83-1Jn": "1 John", "84-2Jn": "2 John", "85-3Jn": "3 John",
      "86-Jud": "Jude", "87-Re": "Revelation"}
SLUG = {b: b.split("-", 1)[1].lower() for b in EN}
ORDER = sorted(EN)
FUNCTION_POS = gc.FUNCTION_POS
HEAD = "---\ntitle: 卷二\nsubtitle: {sub}\nauthor: PubHub 三書精讀系統\ndate: 2026年11月\npublisher: 三書精讀出版系統\n---\n\n"


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c)).replace("ς", "σ")


def esc(s):
    return s.replace("|", "／").replace("\n", " ")


def load_corpus():
    tok = collections.Counter(); lem = collections.defaultdict(collections.Counter); pos = {}
    ntlem = collections.Counter()
    for f in sorted(glob.glob(os.path.join(CORPUS, "*.txt"))):
        b = os.path.basename(f)[:-4]
        for line in open(f, encoding="utf-8"):
            p = line.split()
            if len(p) == 7:
                tok[b] += 1; lem[b][p[6]] += 1; ntlem[p[6]] += 1; pos[p[6]] = p[1]
    return tok, lem, ntlem, pos


STOP_POS = {"RA", "C-", "P-", "RP", "RD", "RR", "RI"}   # articles, prepositions, conjunctions, pronouns: not 'studied words'
METRICS = json.load(open(os.path.join(ROOT, "docs/sources/biblegreek/wordstudy-metrics.json")))


def balance(g):
    """A gloss cut at a clause boundary may leave 「 or 」 unpaired; pair them (or drop the stray closer)."""
    if g.count("「") > g.count("」"):
        g += "」"
    while g.count("」") > g.count("「"):
        g = g.replace("」", "", 1)
    return g


def short_gloss(g):
    g = gc.clean(g)
    if re.search(r"字根|字源|同源|英文", g):         # root / etymology claims are not carried into Part Two (chapter 5's warning)
        return ""
    if gc.CONFLICT.search(g):                      # contradicts chapter 5: drop the offending parenthesis, else the gloss
        g = re.sub(r"[（(][^）)]*(?:無條件|不求回報|神聖的愛|友誼的愛)[^）)]*[）)]", "", g).strip()
        if gc.CONFLICT.search(g):
            return ""
    g = gc.fix_brackets(balance(re.split(r"[；;/／]", g)[0].strip()))
    return g if 0 < len(g) <= 18 else ""


def phrase_gloss(g):
    """Phrase / contrast headwords keep the whole gloss (cutting at '／' would give only the first word's meaning)."""
    g = gc.clean(g)
    if re.search(r"字根|字源|同源|英文", g):
        return ""
    if gc.CONFLICT.search(g):
        g = re.sub(r"[（(][^）)]*(?:無條件|不求回報|神聖的愛|友誼的愛)[^）)]*[）)]", "", g).strip()
        if gc.CONFLICT.search(g):
            return ""
    if len(g) > 40:
        g = balance(re.split(r"[；;]", g)[0].strip())
    g = gc.fix_brackets(g)
    return g if 0 < len(g) <= 40 else ""


IDX_OVERRIDE = {   # lemmas whose series glosses mix senses or hide the lemma's main one (found in independent review)
    "κοινωνία": "團契、相交（羅 15:26 指捐助）",
    "δέω": "捆綁（語料的詞目 δέω 也收 δεῖ「必須」與 δέομαι「祈求」的部分形式）",
    "σημεῖον": "記號、神蹟（啟示錄的 σημεῖον 和合本多譯「異象」）",
}


def display_head(row, lemma):
    ws = row["headword"].split()
    if len(ws) == 1:
        return lemma if norm(ws[0]) == norm(lemma) else f"{lemma}（{ws[0]}）"   # show the form the series studied
    return row["headword"]


def main():
    tok, lem, ntlem, pos = load_corpus()
    all_rows = list(csv.DictReader(open(LEDGER, encoding="utf-8"), delimiter="\t"))
    rows = [r for r in all_rows if r["level"] in ("A", "B", "C")]
    tiers = collections.Counter(r["level"] for r in rows)
    dropped = sum(1 for r in all_rows if r["level"] == "X")
    by_book = collections.defaultdict(lambda: collections.defaultdict(list))   # book -> headword -> rows
    single = collections.defaultdict(lambda: collections.defaultdict(list))    # lemma -> book -> single-word rows
    gloss_by_lemma = collections.defaultdict(collections.Counter)
    omitted = collections.Counter()
    for r in rows:
        lems = [l for l in r["lemmas"].split(";") if l]
        ws = r["headword"].split()
        if not lems or any(l not in ntlem for l in lems):
            omitted["nolemma"] += 1; continue
        if len(ws) == 1:
            if pos.get(lems[0]) in STOP_POS or lems[0] == "εἰμί":
                omitted["function"] += 1; omitted["single"] += 1; continue
            single[lems[0]][r["book"]].append(r)
            g = short_gloss(r["gloss"])
            if g: gloss_by_lemma[lems[0]][g] += 1
        else:
            if all(pos.get(l) in STOP_POS or l == "εἰμί" for l in lems) and not (len(ws) == 2 and norm(ws[0]) == "εγω" and norm(ws[1]) == "ειμι"):
                omitted["function"] += 1; omitted["phrase"] += 1; continue
        r["_lemma"] = lems[0] if len(ws) == 1 else ""
        by_book[r["book"]][lems[0] if len(ws) == 1 else r["headword"]].append(r)
    shown = sum(len(rs) for ent in by_book.values() for rs in ent.values())
    lvl_shown = collections.Counter(r["level"] for ent in by_book.values() for rs in ent.values() for r in rs)
    # vetted glossary only (series glosses for very common words are verse-specific); no vetted gloss -> a dash
    gl = lambda k: gd.GLOSS.get(k) or "—"   # a lemma meaning comes only from the vetted glossary; series glosses are verse-specific
    series_gl = collections.defaultdict(collections.Counter)
    for k, bs in single.items():
        for b, rs0 in bs.items():
            for r0 in rs0:
                if norm(r0["headword"]) != norm(k):      # only rows whose headword IS the lemma: glosses of inflected forms are verse-specific
                    continue
                g0 = re.split(r"[；;/／、]", gc.clean(r0["gloss"]))[0].strip()
                if 0 < len(g0) <= 8 and not gc.CONFLICT.search(g0) and not re.search(r"[你我他她們要就已必將被了罷祢（(「]", g0):
                    series_gl[k][g0] += 1

    def idx_gl(k):
        """Index meaning: the vetted glossary if it has the word, else the distinct short meanings the series tables gave it (up to 3), so context-dependence stays visible."""
        if gd.GLOSS.get(k):
            return gd.GLOSS[k]
        if k in IDX_OVERRIDE:
            return IDX_OVERRIDE[k]
        alts = [g0 for g0, _ in series_gl[k].most_common(3)]
        return "／".join(alts) if alts else "—"
    vet = lambda k: gd.GLOSS.get(k) or "—"
    n_entries = sum(len(v) for v in by_book.values())
    books_with = sum(1 for b in ORDER if by_book.get(b))
    pct = lambda x: f"{round(x * 100)}%"

    def write(name, sub, body):
        open(os.path.join(OUT, name), "w", encoding="utf-8").write(HEAD.format(sub=sub) + body.rstrip("\n") + "\n")

    # ---------- divider
    div = f"""# 卷二：各卷的希臘文 (Part Two: The Greek of Each Book) {{.unnumbered}}

卷一教你怎麼讀、怎麼查。卷二把本系列二十七卷新約研讀裏，**真的查過的希臘字**，按書卷整理出來，並附兩份索引。

> **座標**：本書骨幹〈啟示的次序〉——第五步：人怎麼讀。卷二是這個「人怎麼查」的實例：同一個方法，二十七卷各查了甚麼。

## 這一卷的材料從哪裏來

各卷研讀裏都有「原文研讀」一類的表格：一個希臘字、一個中文意思、有時附經節與一句註解。我們把這些表格全部讀出來（{len(all_rows):,} 條不重複的記錄），逐條對 SBLGNT 語料核對，再依**核對得到的證據強弱**分三級：

| 級 | 證據 | 通過的條數 | 卷二裏怎麼標 |
|----|------|-----------|--------------|
| A | 標示的每個希臘字都出現在所引的**經節** | {tiers['A']:,} | 列出經節（只列真的含該字的節） |
| B | 原記錄沒有經節，但每個字都出現在該篇所討論的一兩個**章** | {tiers['B']:,} | 標「第 N 章」（只列真的含該字的章） |
| C | 原記錄沒有經節或章，字確實出現在**本卷**的某處 | {tiers['C']:,} | 標「（本卷）」 |
| 剔除 | 通不過所屬級別的核對 | {dropped:,} | 不收入 |

**不是每條通過的記錄都印出來。** 單一個字的記錄，若那個字是冠詞、介系詞、連接詞、代名詞或「是」動詞（εἰμί），不算「查過的字」，略去 {omitted['single']:,} 條；另有 {omitted['phrase']:,} 條詞組整個都是這類小字（如 ἐντὸς ὑμῶν），也略去；因此卷二各卷的表一共印出 {shown:,} 條（A {lvl_shown['A']:,}、B {lvl_shown['B']:,}、C {lvl_shown['C']:,}），合併同一卷內相同的詞目後是 {n_entries:,} 列。其餘兩個以上的字組成的詞組（如 ἐγώ εἰμι）照原樣印出，意思與註解屬於整個詞組，不掛在單一個字上，對照式的詞組（如 περιτομή ἀκροβυστία）意思欄印完整的對照；兩份索引則只收單字詞目，意思欄見該表開頭說明。

**怎麼讀這些級別：** 「通過」只保證那個希臘字確實出現在所標的位置，**不保證**中文意思或註解在神學上說得對。B 級的「章」，是從原稿自己引用的經節推出來的；若推出的章超過兩章，就說不出具體位置，一律降為 C 級。拿有經節的記錄回測這個推法（{METRICS['n']:,} 條，含重複）：推出一兩章且包含真正章次的占 {pct(METRICS['true'])}，推出的章太多而會降級的占 {pct(METRICS['wide'])}，推出的章都不含該字的占 {pct(METRICS['none'])}，推出一兩章但沒有一章是真正章次的占 {pct(METRICS['miss'])}。註解欄是各卷作者當時寫的話，原文照錄（過長者只取第一句）；與第五章論證衝突的說法（如「無條件的愛」）、以及註解欄裏作者自己數出的次數或處數、字根與英文字源的說法（這與第五章的警告同一精神），一律逐子句略去；**意思欄裏偶爾留有的次數說法照錄，沒有逐條重算**（抽查都與語料相符，但不是全部核對）。涉及其他經卷或七十士譯本的說法，不在這份語料的核對範圍內。

每卷開頭的兩張表，詞數、次數、詞目與排序由語料計算；「常見意思」欄則取自本書的人工字彙表，沒有的就留破折號。

## 卷二的內容

1. 〈馬太福音〉到〈啟示錄〉二十七節：每卷一節；
2. 〈跨卷字表〉：被兩卷以上查過的字，附逐節位置；
3. 〈希臘字索引〉：全部查過的單字詞目，依希臘字母排序，指向各卷。

〈歌羅西書〉、〈提摩太前書〉、〈提摩太後書〉的研讀裏沒有可讀取的希臘文表格，〈提多書〉只有 {sum(len(v) for v in by_book.get('77-Tit', {}).values())} 條，所以這幾卷主要是計算出來的部分。
"""
    write("p2-00-divider.md", "各卷的希臘文", div)

    # ---------- per-book sections
    for bi, b in enumerate(ORDER, 1):
        t = tok[b]; ll = lem[b]
        thr = 3 if t < 3000 else 6
        excl = sum(1 for l, n in ll.items() if n == ntlem[l])
        hapax = sum(1 for l, n in ll.items() if ntlem[l] == 1)
        content = [(l, n) for l, n in ll.most_common() if pos[l] not in FUNCTION_POS and l != "εἰμί"]
        conc = sorted(((l, n) for l, n in ll.items() if pos[l] not in FUNCTION_POS and n >= thr),
                      key=lambda x: (-(x[1] / ntlem[x[0]]), -x[1]))
        body = [f"# {ZH[b]} ({EN[b]}) {{.unnumbered}}", "",
                "> 本節前兩張表的數字與排序由 SBLGNT 語料計算；「本系列查過的字」依三級證據標示（A 逐節、B 章、C 本卷，說明見卷二開頭）。", "",
                "## 這一卷的詞彙概況", "",
                "| 項目 | 數字 |", "|------|------|",
                f"| 詞數（SBLGNT） | {t:,} |", f"| 不同的詞目 | {len(ll):,} |",
                f"| 只在本卷出現的詞目 | {excl:,} |", f"| 全新約只出現一次、且在本卷的詞目 | {hapax:,} |", ""]
        body += ["## 本卷最常見的字（不含冠詞、代名詞、介系詞、連接詞等小字）", "",
                 f"（「是」動詞 εἰμί 也不列入；它在本卷出現 {ll['εἰμί']:,} 次，全新約 {ntlem['εἰμί']:,} 次。）", "", "| 詞目 | 本卷次數 | 全新約次數 | 常見意思 |", "|------|---------|-----------|----------|"]
        for l, n in content[:12]:
            body.append(f"| {l} | {n:,} | {ntlem[l]:,} | {esc(vet(l))} |")
        body += ["", "## 本卷用得最集中的字", "",
                 f"（本卷次數至少 {thr} 次；依「本卷次數佔全新約次數的比例」排序。短卷的比例容易偏高，請對照次數看。）", "",
                 "| 詞目 | 本卷次數 | 全新約次數 |", "|--------------------------|--------------------------|--------------------------|"]
        for l, n in conc[:10]:
            body.append(f"| {l} | {n:,} | {ntlem[l]:,} |")
        ent = by_book.get(b, {})
        body += ["", "## 本系列在這卷查過的字", ""]
        if not ent:
            body += ["本系列對這一卷的研讀裏，沒有可讀取的「原文研讀」表格，所以這一節只有上面計算出來的部分。", ""]
        else:
            lv = collections.Counter(r["level"] for rs in ent.values() for r in rs)
            body += [f"共 {len(ent):,} 列（來自逐節 A 級 {lv['A']:,} 條、章 B 級 {lv['B']:,} 條、本卷 C 級 {lv['C']:,} 條記錄；同一詞目合併為一列）。"
                     "詞組的意思與註解屬於整個詞組；意思欄標「（字彙表）」者，是原表格沒有給意思，改取本書的精選字彙表。", "",
                     "| 詞目 | 意思（原註） | 位置 | 原註解 |", "|------------------------|------------------|----------------|------------------------------------------|"]
            def sortkey(item):
                k, rs = item
                refs = [x for r in rs if r["level"] == "A" for x in re.findall(r"(\d+):(\d+)", r["refs"])]
                chap = [int(c) for r in rs if r["level"] == "B" for c in re.findall(r"\d+", r["refs"])]
                first = min([int(c) for c, _ in refs]) if refs else (min(chap) if chap else 999)
                return (first, norm(k))
            for k, rs in sorted(ent.items(), key=sortkey):
                a = sorted({x for r in rs if r["level"] == "A" for x in r["refs"].split(";") if x},
                           key=lambda s: tuple(int(i) for i in s.split(":")))
                bch = sorted({int(c) for r in rs if r["level"] == "B" for c in re.findall(r"\d+", r["refs"])})
                if a:
                    place = "; ".join(a[:4]) + (" …" if len(a) > 4 else "")
                elif bch:
                    place = "第 " + "、".join(map(str, bch[:4])) + " 章"
                else:
                    place = "（本卷）"
                top = "A" if a else ("B" if bch else "C")
                rs_top = [r for r in rs if r["level"] == top]       # gloss and note come from the rows that give the place shown
                gf = short_gloss if rs[0]["_lemma"] else phrase_gloss
                g = next((gf(r["gloss"]) for r in rs_top if gf(r["gloss"])), "")
                note = next((n for n in (gc.short_note(r["note"]) for r in rs_top) if n and len(n) <= 70), "")
                if not g:   # the source's meaning cell is a whole sentence (too long for the meaning column): show it as the note, clause-filtered
                    alt = next((n for n in (gc.short_note(r["gloss"]) for r in rs_top) if n and len(n) <= 70), "")
                    note = note or alt
                if not g and not note and rs[0]["_lemma"] and gd.GLOSS.get(rs[0]["_lemma"]):
                    g = gd.GLOSS[rs[0]["_lemma"]] + "（字彙表）"   # the series table gave no meaning: use the book's vetted glossary, labelled
                body.append(f"| {display_head(rs[0], rs[0]['_lemma'])} | {esc(g)} | {place} | {esc(note)} |")
            body.append("")
        write(f"p2-{bi:02d}-{SLUG[b]}.md", f"{ZH[b]}的希臘文", "\n".join(body))

    # ---------- cross-book index (single-word headwords only)
    studied = collections.defaultdict(dict)   # lemma -> book -> [A refs]
    for k, bs in single.items():
        for b, rs in bs.items():
            studied[k][b] = sorted({x for r in rs if r["level"] == "A" for x in r["refs"].split(";") if x},
                                   key=lambda s: tuple(int(i) for i in s.split(":")))
    multi = sorted(((k, bs) for k, bs in studied.items() if len(bs) >= 2), key=lambda kv: (-len(kv[1]), norm(kv[0])))
    cb = ["# 跨卷字表 (Words Studied in More Than One Book) {.unnumbered}", "",
          f"單字詞目中，被兩卷以上列過的字，共 {len(multi):,} 個。「位置」只列 A 級（逐節核對）的經節，每卷最多兩處；沒有經節的卷只列卷名。"
          "意思欄：本書人工字彙表有的取字彙表；沒有的，列出本系列表格給過的簡短意思（至多三個，用「／」分開）——同一個字的幾個意思不同，正是它依上下文而定的樣子，不要當成詞典定義。", "",
          "| 詞目 | 新約次數 | 意思（原註） | 被查過的卷與位置 |", "|----------------------|----------|------------------------|--------------------------------------------|"]
    for k, bs in multi:
        parts = []
        for b in ORDER:
            if b in bs:
                refs = bs[b][:2]
                parts.append(ab(b) + (" " + ", ".join(refs) if refs else ""))
        cb.append(f"| {k} | {ntlem[k]:,} | {esc(idx_gl(k))} | {'；'.join(parts)} |")
    nb = {k: len(bs) for k, bs in studied.items()}
    cb += ["", "## 你看見耶穌了嗎？", "",
           "這份字表裏，與耶穌最直接相關的幾個字，本系列研讀表格列過它們的卷數是：" +
           "、".join(f"`{k}` {nb[k]} 卷" for k in ("Ἰησοῦς", "Χριστός", "κύριος", "υἱός", "πνεῦμα") if nb.get(k)) +
           f"。這只是表格裏被列為「查過的字」的次數，不是這些字在新約出現的多寡（例如 Ἰησοῦς 在新約有 {ntlem['Ἰησοῦς']:,} 次）。"
           "字表會過時，問題不會：這段經文裏，耶穌是誰？"]
    write("p2-90-cross-book-index.md", "跨卷字表", "\n".join(cb))

    # ---------- Greek-term index
    gi = ["# 希臘字索引 (Index of Greek Terms) {.unnumbered}", "",
          f"本系列研讀表格裏列過的單字詞目（{len(studied):,} 個），依希臘字母排序；右欄是列過它的卷。位置見卷二各卷的一節。詞組不在這份索引裏。", "",
          "| 詞目 | 意思（原註） | 卷 |", "|--------------------------|--------------------------------------------|------------------------------|"]
    for k in sorted(studied, key=norm):
        books = "、".join(ab(b) for b in ORDER if b in studied[k])
        gi.append(f"| {k} | {esc(idx_gl(k))} | {books} |")
    write("p2-91-greek-term-index.md", "希臘字索引", "\n".join(gi))
    G = os.path.join(OUT, "generated")
    open(os.path.join(G, "ledger-98-collect.md"), "w", encoding="utf-8").write(
        "| 蒐集 | `scripts/extract-greek-wordstudy-v2.py` 讀取二十七卷新約研讀（含 `pauline-epistles/` 下的歌羅西書、提摩太前後書、提多書）裏所有含「希臘文／原文」欄的表格，不論有沒有經節欄；去除各譯本版本的重複後得 %s 條記錄（本列與下兩列的數字由程式從帳目產生） |" % format(len(all_rows), ","))
    open(os.path.join(G, "ledger-98-grade.md"), "w", encoding="utf-8").write(
        "| 核對與分級 | 逐條對 SBLGNT 語料核對，依證據強弱分級：**A** 標示的希臘字都在所引經節（%s 條；經節取自位置欄，位置欄是空的則取自註解裏引用的本卷經節）；**B** 沒有經節，但都在該篇所討論的章（%s 條；章由原稿自己引用的經節推出，且只列真的含該字的章；用有經節的記錄回測，推出一兩章且包含真正章次的占 %s，推出的章多於兩章而降為 C 的占 %s）；**C** 沒有經節或章，字確實出現在本卷（%s 條）；**剔除** 通不過所屬級別（%s 條）。帳目存於 `docs/sources/biblegreek/wordstudy-ledger-v2.tsv` |"
        % (format(tiers["A"], ","), format(tiers["B"], ","), pct(METRICS["true"]), pct(METRICS["wide"]), format(tiers["C"], ","), format(dropped, ",")))
    open(os.path.join(G, "ledger-98-adopt.md"), "w", encoding="utf-8").write(
        "| 採用 | 卷二：A、B、C 三級中，單字詞目若是冠詞、介系詞、連接詞、代名詞或 `εἰμί` 則略去（%d 條），詞組整個都是這類小字的也略去（%d 條），其餘 %s 條各標明級別，詞組照原樣印出、意思不掛在單一個字上，索引只收單字詞目；附錄〈核心字在各卷的用法〉：只收 A 級的單字詞目；詞目、次數、經節摘錄由語料計算（已去掉 SBLGNT 的版本校勘記號）；「意思」與「註解」欄是各卷作者當時寫的原文（過長者只取第一句），含「無條件的愛」一類與第五章衝突的說法、註解中含作者自己數出的次數或處數（「N 次」「N 處」「N 回」）、字根或英文字源說法、指向卷二沒有的章節（「見下方說明」）的子句，逐子句略去、其餘保留，未逐條重算；意思欄裏偶爾留有的次數說法照錄 |"
        % (omitted["single"], omitted["phrase"], format(shown, ",")))
    stats = {"ledger_rows": len(all_rows), "A": tiers["A"], "B": tiers["B"], "C": tiers["C"], "X": dropped, "omitted_function": omitted["function"],
             "shown_rows": shown, "shown_A": lvl_shown["A"], "shown_B": lvl_shown["B"], "shown_C": lvl_shown["C"], "entries": n_entries,
             "books_with_tables": books_with, "cross_book": len(multi), "index": len(studied)}
    json.dump(stats, open(os.path.join(OUT, "generated/part2-stats.json"), "w"), ensure_ascii=False, indent=1)
    print(stats)
    print("DROPPED notes:", gc.DROPPED)


if __name__ == "__main__":
    main()
