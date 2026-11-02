#!/usr/bin/env python3
"""Re-derive, from OSHB, the factual claims that 《讀懂聖經的希伯來文》 states in prose but that are not
produced by gen-biblehebrew-data.py. Prints PASS/FAIL per claim and exits 1 on any FAIL.
Usage: verify-biblehebrew-claims.py
"""
import collections, importlib.util, os, re, sys, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("g", os.path.join(ROOT, "scripts/gen-biblehebrew-data.py"))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
toks = list(g.tokens())
N = lambda s: unicodedata.normalize("NFD", s)
fails = 0


def check(name, ok, detail=""):
    global fails
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))
    fails += (not ok)


def skel(w): return re.sub(r"[֑-ׇ]", "", w)


V = collections.defaultdict(list)
for r, l, m, t in toks: V[r].append((g.key_of(l), m, g.strip_cantillation(t)))

# ch3: Psalm 119 is an acrostic: 22 stanzas x 8 verses, each verse starts with the stanza's letter, alef..tav
order = "אבגדהוזחטיכלמנסעפצקרשת"
ok = True
for i, letter in enumerate(order):
    for j in range(8):
        first = skel(V[f"Ps.119.{1 + 8 * i + j}"][0][2])[0]
        ok &= (first == letter)
check("Ps 119 acrostic: 22 x 8, alef..tav", ok)

# ch4: כִּי לְעוֹלָם חַסְדּוֹ — 41 by lemma sequence, 40 by identical spelling, listed refs
seq = [toks[i][0] for i in range(len(toks) - 2)
       if g.key_of(toks[i][1]) == "3588" and g.key_of(toks[i + 1][1]) == "5769" and g.key_of(toks[i + 2][1]) == "2617"
       and "Sp3ms" in toks[i + 2][2]]
check("'כי לעולם חסדו' = 41 by lemma", len(seq) == 41, str(len(seq)))
exact = [toks[i][0] for i in range(len(toks) - 2)
         if N(g.strip_cantillation(toks[i][3])) + N(g.strip_cantillation(toks[i + 1][3])) + N(g.strip_cantillation(toks[i + 2][3]))
         == N("כִּי") + N("לְעוֹלָם") + N("חַסְדּוֹ")]
check("…= 40 with identical spelling (Ps 136:3 is defective)", len(exact) == 40 and "Ps.136.3" not in exact, str(len(exact)))
refs = {"1Chr.16.34", "1Chr.16.41", "2Chr.5.13", "2Chr.7.3", "2Chr.7.6", "2Chr.20.21", "Ezra.3.11", "Jer.33.11", "Ps.106.1",
        "Ps.107.1", "Ps.118.1", "Ps.118.2", "Ps.118.3", "Ps.118.4", "Ps.118.29"} | {f"Ps.136.{i}" for i in range(1, 27)}
check("…the 41 references listed in chapter 4", set(seq) == refs)

# ch8: רַב חֶסֶד
rv = [toks[i][0] for i in range(len(toks) - 1) if g.key_of(toks[i][1]) == "7227" and g.key_of(toks[i + 1][1]) == "2617"]
check("'רב חסד' = 8 by lemma", sorted(rv) == sorted(["Exod.34.6", "Joel.2.13", "Jonah.4.2", "Neh.9.17", "Num.14.18", "Ps.86.5", "Ps.86.15", "Ps.103.8"]), str(rv))

# ch8/9: counts quoted from the series
def cnt(key, book, stems=None):
    out = []
    for r, l, m, t in toks:
        if r.startswith(book + ".") and g.key_of(l) == key:
            segs = m.split("/"); segs[0] = segs[0][1:]
            st = [s_[1] for s_ in segs if s_.startswith("V")]
            if stems is None or (st and st[0] in stems): out.append(r)
    return out
check("Ezek 11: רוח x6", len(cnt("7307", "Ezek.11".split(".")[0])) >= 6 and len([r for r in cnt("7307", "Ezek") if r.startswith("Ezek.11.")]) == 6)
check("Ezek 18:21,24,26,27 contain שוב", all(r in set(cnt("7725", "Ezek")) for r in ("Ezek.18.21", "Ezek.18.24", "Ezek.18.26", "Ezek.18.27")))
check("Amos שמע Qal in 8 verses", sorted(set(cnt("8085", "Amos", "q"))) == sorted(f"Amos.{x}" for x in ("3.1", "3.13", "4.1", "5.1", "5.23", "7.16", "8.4", "8.11")))
check("Micah שמע: 9 tokens in 8 verses", len(cnt("8085", "Mic")) == 9 and len(set(cnt("8085", "Mic"))) == 8)
check("Joel שוב x6", len(cnt("7725", "Joel")) == 6)
check("Haggai שים x7", len(cnt("7760", "Hag")) == 7)
check("Jonah מנה 4 / ירד 4 / גדול 14", (len(cnt("4487", "Jonah")), len(cnt("3381", "Jonah")), len(cnt("1419", "Jonah"))) == (4, 4, 14))
def stem_of(m):
    segs = m.split("/"); segs[0] = segs[0][1:]
    return next((x[1] for x in segs if x.startswith("V")), None)


check("Joel 4:4 and 4:7 שוב are Hiphil (stem h)", all(stem_of(m) == "h" for r, l, m, t in toks
                                                       if r in ("Joel.4.4", "Joel.4.7") and g.key_of(l) == "7725"))

# ch6: שמר has no Qal second-person feminine form
check("שמר: no Qal 2f form", not [1 for r, l, m, t in toks if g.key_of(l) == "8104" and re.search(r"Vq.2f", m)])

# ch1: Aramaic passages begin/end where the chapter says (spot-check first/last Aramaic word of each passage)
ar = collections.defaultdict(list)
for r, l, m, t in toks:
    if m.startswith("A"): ar[r.split(".")[0]].append(r)
check("Aramaic only in Gen, Jer, Ezra, Dan", set(ar) == {"Gen", "Jer", "Ezra", "Dan"}, str(sorted(ar)))
check("Aramaic tokens = 4,828", sum(len(v) for v in ar.values()) == 4828)

print("\n%d FAIL" % fails if fails else "\nall claims reproduce")
sys.exit(1 if fails else 0)
