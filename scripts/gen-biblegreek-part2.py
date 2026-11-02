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
    if gc.CONFLICT.search(g):                      # contradicts chapter 5: drop the offending parenthesis, else the gloss
        g = re.sub(r"[（(][^）)]*(?:無條件|不求回報|神聖的愛|友誼的愛)[^）)]*[）)]", "", g).strip()
        if gc.CONFLICT.search(g):
            return ""
    g = balance(re.split(r"[；;/／]", g)[0].strip())
    return g if 0 < len(g) <= 18 else ""


def display_head(row, lemma):
    ws = row["headword"].split()
    if len(ws) == 1:
        return lemma if norm(ws[0]) == norm(lemma) else f"{ws[0]}（{lemma}）"
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
                omitted["function"] += 1; continue
            single[lems[0]][r["book"]].append(r)
            g = short_gloss(r["gloss"])
            if g: gloss_by_lemma[lems[0]][g] += 1
        else:
            if all(pos.get(l) in STOP_POS or l == "εἰμί" for l in lems) and not (len(ws) == 2 and norm(ws[0]) == "εγω" and norm(ws[1]) == "ειμι"):
                omitted["function"] += 1; continue
        r["_lemma"] = lems[0] if len(ws) == 1 else ""
        by_book[r["book"]][r["headword"]].append(r)
    shown = sum(len(rs) for ent in by_book.values() for rs in ent.values())
    lvl_shown = collections.Counter(r["level"] for ent in by_book.values() for rs in ent.values() for r in rs)
    # vetted glossary only (series glosses for very common words are verse-specific); no vetted gloss -> a dash
    gl = lambda k: gd.GLOSS.get(k) or (gloss_by_lemma[k].most_common(1)[0][0] if gloss_by_lemma[k] else "—")
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

**不是每條通過的記錄都印出來。** 單一個字的記錄，若那個字是冠詞、介系詞、連接詞、代名詞或「是」動詞（εἰμί），不算「查過的字」，略去 {omitted['function']:,} 條；因此卷二各卷的表一共印出 {shown:,} 條（A {lvl_shown['A']:,}、B {lvl_shown['B']:,}、C {lvl_shown['C']:,}），合併同一卷內相同的詞目後是 {n_entries:,} 列。兩個以上的字組成的詞組（如 ἐγώ εἰμι）照原樣印出，意思與註解屬於整個詞組，不掛在單一個字上；兩份索引則只收單字詞目。

**怎麼讀這些級別：** 「通過」只保證那個希臘字確實出現在所標的位置，**不保證**中文意思或註解在神學上說得對。B 級的「章」，是從原稿自己引用的經節推出來的；若推出的章超過兩章，就說不出具體位置，一律降為 C 級。拿有經節的記錄回測這個推法（{METRICS['n']:,} 條，含重複）：推出一兩章且包含真正章次的占 {pct(METRICS['true'])}，推出的章太多而會降級的占 {pct(METRICS['wide'])}，推出的章都不含該字的占 {pct(METRICS['none'])}。註解欄是各卷作者當時寫的話，原文照錄（過長者只取第一句）；與第五章論證衝突的說法（如「無條件的愛」）、以及註解作者自己數出的次數或處數，一律略去，沒有逐條重算。涉及其他經卷或七十士譯本的說法，不在這份語料的核對範圍內。

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
        body += ["## 本卷最常見的字（不含冠詞、代名詞、介系詞、連接詞等小字）", "", "| 詞目 | 本卷次數 | 全新約次數 | 常見意思 |", "|------|---------|-----------|----------|"]
        for l, n in content[:12]:
            body.append(f"| {l} | {n:,} | {ntlem[l]:,} | {esc(vet(l))} |")
        body += ["", "## 本卷用得最集中的字", "",
                 f"（本卷次數至少 {thr} 次；依「本卷次數佔全新約次數的比例」排序。短卷的比例容易偏高，請對照次數看。）", "",
                 "| 詞目 | 本卷次數 | 全新約次數 | 常見意思 |", "|------|---------|-----------|----------|"]
        for l, n in conc[:10]:
            body.append(f"| {l} | {n:,} | {ntlem[l]:,} | {esc(vet(l))} |")
        ent = by_book.get(b, {})
        body += ["", "## 本系列在這卷查過的字", ""]
        if not ent:
            body += ["本系列對這一卷的研讀裏，沒有可讀取的「原文研讀」表格，所以這一節只有上面計算出來的部分。", ""]
        else:
            lv = collections.Counter(r["level"] for rs in ent.values() for r in rs)
            body += [f"共 {len(ent):,} 列（來自逐節 A 級 {lv['A']:,} 條、章 B 級 {lv['B']:,} 條、本卷 C 級 {lv['C']:,} 條記錄；同一詞目合併為一列）。"
                     "詞組的意思與註解屬於整個詞組。", "",
                     "| 詞目 | 意思（原註） | 位置 | 原註解 |", "|------------------------|------------------|----------------|------------------------------------------|"]
            def sortkey(item):
                k, rs = item
                refs = [x for r in rs for x in re.findall(r"(\d+):(\d+)", r["refs"])]
                chap = [int(c) for r in rs if r["level"] == "B" for c in re.findall(r"\d+", r["refs"])]
                first = min([int(c) for c, _ in refs] + chap) if (refs or chap) else 999
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
                g = next((short_gloss(r["gloss"]) for r in rs if short_gloss(r["gloss"])), "")
                note = next((n for n in (gc.short_note(r["note"]) for r in rs) if n and len(n) <= 70), "")
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
          "意思欄取自本書人工字彙表，沒有的取本系列單字記錄中最常見的一個。", "",
          "| 詞目 | 新約次數 | 意思（原註） | 被查過的卷與位置 |", "|----------------------|----------|------------------------|--------------------------------------------|"]
    for k, bs in multi:
        parts = []
        for b in ORDER:
            if b in bs:
                refs = bs[b][:2]
                parts.append(SHORT[b] + (" " + ", ".join(refs) if refs else ""))
        cb.append(f"| {k} | {ntlem[k]:,} | {esc(gl(k))} | {'；'.join(parts)} |")
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
        books = "、".join(SHORT[b] for b in ORDER if b in studied[k])
        gi.append(f"| {k} | {esc(gl(k))} | {books} |")
    write("p2-91-greek-term-index.md", "希臘字索引", "\n".join(gi))
    stats = {"ledger_rows": len(all_rows), "A": tiers["A"], "B": tiers["B"], "C": tiers["C"], "X": dropped, "omitted_function": omitted["function"],
             "shown_rows": shown, "shown_A": lvl_shown["A"], "shown_B": lvl_shown["B"], "shown_C": lvl_shown["C"], "entries": n_entries,
             "books_with_tables": books_with, "cross_book": len(multi), "index": len(studied)}
    json.dump(stats, open(os.path.join(OUT, "generated/part2-stats.json"), "w"), ensure_ascii=False, indent=1)
    print(stats)
    print("DROPPED notes:", gc.DROPPED)


if __name__ == "__main__":
    main()
