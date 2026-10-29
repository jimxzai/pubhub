#!/usr/bin/env python3
"""Recompute every number in BOOK-SPEC §4 from aieden/*.json and print FACTS.md."""
import json, re, collections, pathlib
D = pathlib.Path(__file__).resolve().parent / "aieden"
V = {}
for ch in range(1, 49):
    for v in json.load(open(D / f"aieden-{ch:02d}.json"))["data"]["verses"]:
        V[(ch, v["verse"])] = (v["textZh"], v["text"])
def hits(pat, i=0):
    r = re.compile(pat, re.I); return [k for k in V if r.search(V[k][i])]
def fmt(ks):
    by = collections.OrderedDict()
    for c, v in ks: by.setdefault(c, []).append(v)
    return "; ".join(f"{c}:{','.join(map(str, vs))}" for c, vs in by.items())
out = ["# FACTS — computed from aieden/*.json (和合本 textZh / NASB text). Regenerate: python3 facts.py > FACTS.md\n"]
out.append(f"- chapters 48, verses {len(V)}")
ks = hits("知道我是")
out.append(f"- CUV regex `知道我是`: {len(ks)} verses; first {ks[0]}, last {ks[-1]}; in ch6-32: {sum(1 for k in ks if 6<=k[0]<=32)}, ch33-39: {sum(1 for k in ks if 33<=k[0]<=39)}, ch1-5 and 40-48: {sum(1 for k in ks if k[0]<6 or k[0]>39)}")
out.append(f"  - verses: {fmt(ks)}")
loose=[k for k in V if re.search(r"知道.{0,8}耶和華",V[k][0])]
out.append(f"- CUV loose regex `知道.{{0,8}}耶和華`: {len(loose)} verses; outside 6-39: {[k for k in loose if k[0]<6 or k[0]>39]}; not in strict set: {fmt(sorted(set(loose)-set(ks)))}")
out.append(f"- NASB regex `know that I am`: {len(hits('know that I am',1))} verses")
out.append(f"- CUV `人子`: {len(hits('人子'))} verses / {sum(V[k][0].count('人子') for k in V)} occurrences; first {hits('人子')[0]}, last {hits('人子')[-1]}; NASB `son of man`: {len(hits('son of man',1))} verses")
out.append(f"- NASB `hand of the (LORD|Lord GOD)`: {fmt(hits('hand of the (LORD|Lord GOD)',1))}  (CUV prints these as 靈（原文是手）)")
out.append(f"- NASB `glory of the LORD`: {fmt(hits('glory of the LORD',1))}")
out.append(f"- NASB `glory of the God of Israel`: {fmt(hits('glory of the God of Israel',1))}")
out.append(f"- CUV `榮耀|榮光` verses: {fmt(hits('榮耀|榮光'))}")
out.append(f"- CUV `彷彿`: {sum(V[k][0].count('彷彿') for k in V)} total, ch1: {sum(V[k][0].count('彷彿') for k in V if k[0]==1)}")
out.append(f"- CUV `形狀|形像` ch1: {sum(len(re.findall('形狀|形像', V[k][0])) for k in V if k[0]==1)}")
out.append(f"- CUV `牧人|牧養` ch34: {sum(len(re.findall('牧人|牧養', V[k][0])) for k in V if k[0]==34)}")
out.append(f"- CUV `殿` ch40-48: {sum(V[k][0].count('殿') for k in V if k[0]>=40)}; `水` ch47: {sum(V[k][0].count('水') for k in V if k[0]==47)}")
out.append(f"- CUV `耶和華的話臨到`: {len(hits('耶和華的話臨到'))} verses; `主耶和華說`: {len(hits('主耶和華說'))} verses")
out.append(f"- CUV `啞口|開口|口舌貼`: {fmt(hits('啞口|開口|口舌貼'))}")
out.append("- dated oracles (CUV v1-2/17/20-21 with 年…月…日): 1:1; 1:2; 8:1; 20:1; 24:1; 26:1; 29:1; 30:20; 31:1; 32:1; 32:17; 33:21; 40:1 (29:17 per the commentary list; check text)")
print("\n".join(out))
