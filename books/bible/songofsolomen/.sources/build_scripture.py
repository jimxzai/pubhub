#!/usr/bin/env python3 -I
"""Load ai-eden (CUV+NASB), fhl unv, cnbible CUVMPT; strip speaker labels; diff; write tsv + report."""
import json, re, html, sys, difflib
LABEL = re.compile(r'（(新娘|新郎|耶路撒冷的眾女子|新娘的兄弟)）')
PUNCT = re.compile(r'[\s，。、；：！？「」『』（）　．·—─…\-,.;:!?"\'()]')
ai, fh, cn = {}, {}, {}
for c in range(1, 9):
    for v in json.load(open(f'ai-eden/ch{c}.json'))['data']['verses']:
        ai[(c, v['verse'])] = (v['textZh'], v['text'])
    for r in json.load(open(f'fhl/ch{c}.json'))['record']:
        fh[(c, r['sec'])] = r['bible_text']
    t = open(f'cnbible/ch{c}.htm', encoding='utf-8', errors='ignore').read()
    # CUVMPT column: first <td>-like block per verse; locate via marker structure
    i = t.find('CUVMPT')
    # verse rows: "NN||||text||||||NN||||simplified" ; take first occurrence of each verse number's text
    body = re.sub(r'<[^>]+>', '|', t)
    for m in re.finditer(r'\|(\d{1,2})\|+([^|]+?)\|+\1\|+', body):
        n = int(m.group(1)); txt = html.unescape(m.group(2)).strip()
        if (c, n) not in cn: cn[(c, n)] = txt
labels = {}
def strip(s):
    found = LABEL.findall(s)
    return LABEL.sub('', s).strip(), found
def norm(s): return PUNCT.sub('', LABEL.sub('', s))
rep = []
out = {}
for k in sorted(ai):
    z, lab = strip(ai[k][0]); labels[k] = lab
    out[k] = (z, ai[k][1])
    a, f, n = norm(ai[k][0]), norm(fh.get(k, '')), norm(cn.get(k, ''))
    for name, o in (('fhl', f), ('cnbible', n)):
        if o != a:
            sm = difflib.SequenceMatcher(None, a, o)
            d = [f"{op[0]}:{a[op[1]:op[2]]!r}->{o[op[3]:op[4]]!r}" for op in sm.get_opcodes() if op[0] != 'equal']
            rep.append(f"{k[0]}:{k[1]}\tai-eden vs {name}\t{'; '.join(d)}")
missing = [k for k in ai if k not in fh or k not in cn]
json.dump({f"{k[0]}:{k[1]}": v for k, v in labels.items() if v}, open('_labels.json', 'w'), ensure_ascii=False)
with open('_cuv_diffs.txt', 'w') as fo: fo.write('\n'.join(rep))
print(len(ai), len(fh), len(cn), 'missing', missing)
print(len(rep), 'diffs')
