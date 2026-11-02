#!/usr/bin/env python3
"""Recount, in OSHB, the word counts stated in the OT books' own 〈數一數〉 sections (the ones the companion volume
quotes verbatim). For every table row whose second cell is a plain integer:

    word / phrase in cell 1  ->  candidate dictionary words, exact forms, consecutive-token phrase
    stated count             ->  must equal one of the recounts in THAT book

Verdicts: MATCH (says which kind of recount agrees), MISMATCH (lists the recounts), SKIP (no plain integer, no
Hebrew word, or a cell that defines a pattern or a word family: "＋", "……", "（含", "同字根" - not mechanically
checkable). A section that says it counts "以字根計" (by root) is allowed a root-family recount: the sum over the
dictionary words that share the consonants. Cells such as "יָשַׁע、יֵשַׁע、יְשׁוּעָה" list ALTERNATIVES: the stated count
may be the sum of one reading of each. A mismatch is a finding about the source book, not an edit to it.

Writes books/bible/Biblehebrew/generated/verify-sections.{md,json} and adds p2_v_* to stats-part2.json.   Usage: verify-count-sections.py [-v]
"""
import collections, importlib.util, itertools, json, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "books/bible/Biblehebrew/generated")


def load(name, fn):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, "scripts", fn))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


m = load("m", "mine-hebrew-wordstudies.py")
g = m.g
HEBW = re.compile(r"[֐-׿]+")


def cons(s): return re.sub(r"[֑-ׇ־/]", "", s)


def main():
    toks = list(g.tokens())
    by_book = collections.defaultdict(list)                       # osis -> [(skeleton, pointed, lemma key)]
    cnt_lemma = collections.Counter()
    for ref, lem, _, text in toks:
        b = ref.split(".")[0]; k = g.key_of(lem)
        by_book[b].append((cons(text), unicodedata.normalize("NFC", m.pointed(text).replace("־", "")), k))
        cnt_lemma[(b, k)] += 1
    P, C = m.build_index()
    lexform = collections.defaultdict(set)
    for hid, (form, pos) in g.lexicon().items(): lexform[cons(form)].add(hid[1:])

    results = []
    for label, f in m.source_files():
        t = open(f, encoding="utf-8").read()
        for sec in re.finditer(r"^##\s+([^\n]*(?:數一數|鑰字|重複的字|關鍵詞)[^\n]*)\n(.*?)(?=^## |\Z)", t, re.S | re.M):
            if not m.HEB.search(sec.group(2)): continue
            osis = m.LABEL_OSIS[label]; book = by_book[osis]; root_mode = "以字根計" in sec.group(2)
            for line in sec.group(2).split("\n"):
                if not line.startswith("|") or re.match(r"^\|\s*:?-", line): continue
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                if len(cells) < 2 or not m.HEB.search(cells[0]): continue
                words = HEBW.findall(cells[0])
                row = {"book": label, "file": f.split("/books/bible/")[1], "cell": cells[0][:50], "stated": cells[1]}
                if not re.fullmatch(r"\d+", cells[1]) or not words:
                    row["verdict"] = "SKIP"; row["why"] = "no plain integer"; results.append(row); continue
                if re.search(r"＋|……|（含|同字根", cells[0]):
                    row["verdict"] = "SKIP"; row["why"] = "pattern or word family"; results.append(row); continue
                n = int(cells[1]); found = {}
                alts = "、" in re.sub(r"[^\u0590-\u05FF、 ]", "", cells[0].split(" ")[0]) or len(re.findall(r"[\u0590-\u05FF]+、[\u0590-\u05FF]+", cells[0])) > 0
                if len(words) > 1 and alts:                           # alternatives: try one reading of each
                    sets = []
                    for w in words:
                        cw = cons(w)
                        sets.append(sorted({cnt_lemma[(osis, k)] for k in (set(C.get(cw, {}).keys()) | lexform.get(cw, set()))}))
                    tot = {sum(c) for c in itertools.product(*sets)} if all(sets) else set()
                    found["幾個說法相加"] = tot
                elif len(words) == 1:
                    cw = cons(words[0])
                    cand = set(C.get(cw, {}).keys()) | lexform.get(cw, set())
                    for k in cand:
                        found.setdefault("字（詞目）", set()).add(cnt_lemma[(osis, k)])
                    if root_mode: found["字根（相關詞目合計）"] = {sum(cnt_lemma[(osis, k)] for k in cand)}
                    found["字（拼法完全相同）"] = {sum(1 for s, p, k in book if s == cw)}
                    found["字（含前綴的同一個字）"] = {sum(1 for s, p, k in book if s.endswith(cw) and len(s) - len(cw) <= 2)}
                else:
                    sk = [cons(w) for w in words]; cntp = 0
                    for i in range(len(book) - len(sk) + 1):
                        if all(book[i + j][0] == sk[j] or (j == 0 and book[i][0].endswith(sk[0]) and len(book[i][0]) - len(sk[0]) <= 2)
                               for j in range(len(sk))): cntp += 1
                    found["詞組"] = {cntp}
                hit = [kind for kind, vals in found.items() if n in vals]
                row["verdict"] = "MATCH" if hit else "MISMATCH"
                row["by"] = hit[0] if hit else ""
                row["recounts"] = {k: sorted(v) for k, v in found.items()}
                results.append(row)

    # the quoted sections must still be word-for-word the source text (only table-separator rows and # marks may differ)
    sepre = re.compile(r"^\|\s*:?-{2,}:?\s*(?:\|\s*:?-{2,}:?\s*)+\|\s*$")
    norm = lambda lines: [re.sub(r"^#{1,6} ", "", l).rstrip() for l in lines if l.strip() and not sepre.match(l)]
    gen_md = open(os.path.join(OUT, "books.md"), encoding="utf-8").read()
    v_ok = v_bad = 0
    for label, f in m.source_files():
        for sec in re.finditer(r"^##\s+([^\n]*(?:數一數|鑰字|重複的字|關鍵詞)[^\n]*)\n(.*?)(?=^## |\Z)", open(f, encoding="utf-8").read(), re.S | re.M):
            if not m.HEB.search(sec.group(2)): continue
            src = norm(sec.group(2).strip("\n").split("\n")); path = f.split("/books/bible/")[1]
            seg = gen_md[gen_md.index(path):]; seg = seg[seg.index("\n") + 1:]
            end = min([x for x in (seg.find("\n**系列原文**"), seg.find("\n# ")) if x >= 0] + [len(seg)])
            got = norm(seg[:end].split("\n"))
            if got == src or got[-len(src):] == src: v_ok += 1
            else: v_bad += 1; print("NOT VERBATIM:", path)
    if v_bad: sys.exit(f"{v_bad} quoted section(s) differ from their source")
    c = collections.Counter(r["verdict"] for r in results)
    per = collections.defaultdict(collections.Counter)
    for r in results: per[r["book"]][r["verdict"]] += 1
    json.dump({"summary": dict(c), "rows": results}, open(os.path.join(OUT, "verify-sections.json"), "w"), ensure_ascii=False, indent=1)
    bad = [r for r in results if r["verdict"] == "MISMATCH"]
    kinds = collections.Counter(r["by"] for r in results if r["verdict"] == "MATCH")
    strict = kinds["字（詞目）"] + kinds["字（拼法完全相同）"] + kinds["詞組"]
    md = [f"共 {len(results)} 列：**相符 {c['MATCH']}**、**不符 {c['MISMATCH']}**、無法核對 {c['SKIP']}。",
          f"相符的 {c['MATCH']} 列裏，{strict} 列是用最嚴的方式（同一個詞目、拼法完全相同、或連續兩個詞）重數得到相同次數；"
          f"{kinds['字（含前綴的同一個字）']} 列是把帶前綴的同一個字也算進去才相符；"
          f"{kinds['字根（相關詞目合計）'] + kinds['幾個說法相加']} 列要用較寬的算法（該卷自己說「以字根計」而加總相關詞目，或把幾個並列的說法相加）才相符，這幾列的「相符」可能有巧合的成分。\n"]
    if bad:
        md += ["不符的列（括號是我們在該卷 OSHB 重數的結果；這是對原書的發現，本書不改動它們的原文）：\n",
               "| 卷 | 字 | 原書寫的次數 | 我們重數的結果 |", "|--------|----------------|--------|------------------------------|"]
        for r in bad:
            md.append(f"| {m.LABEL_OSIS[r['book']]} | {r['cell']} | {r['stated']} | " + "；".join(f"{k} {'、'.join(map(str, v))}" for k, v in r["recounts"].items()) + " |")
    open(os.path.join(OUT, "verify-sections.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    sp = os.path.join(OUT, "stats-part2.json")                       # let the book print these numbers as {{placeholders}}
    st = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {}
    st.update({"p2_v_rows": len(results), "p2_v_match": c["MATCH"], "p2_v_mismatch": c["MISMATCH"], "p2_v_skip": c["SKIP"],
               "p2_v_strict": strict, "p2_v_loose": c["MATCH"] - strict, "p2_verbatim": v_ok})
    json.dump(st, open(sp, "w"), ensure_ascii=False, indent=1)
    print(dict(c), "| books:", {b: dict(v) for b, v in per.items()})
    if "-v" in sys.argv:
        for r in bad: print("MISMATCH", r["book"], r["cell"], r["stated"], r["recounts"])


if __name__ == "__main__":
    main()
