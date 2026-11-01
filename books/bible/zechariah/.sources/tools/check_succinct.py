#!/usr/bin/env python3
"""Compare trimmed chapters with the pre-succinct snapshot.
usage: check_succinct.py SNAPSHOT_DIR FILE.md [...]   (FILE paths relative to cwd = book dir)
Fails (exit 1) if: YAML/H1/ref line changed; the 11 '## ' headings changed; the 經文 block or 配詩 block changed;
any snapshot line that starts with '> "', '> — ', '> 中譯' or '> 體例說明' is missing (quotes may not be cut);
the 座標 line or '你看見耶穌了嗎' disappeared. Prints CJK ratio (prose before/after, quote blocks excluded)."""
import re, sys, os
snap = sys.argv[1]; bad = 0
def blocks(t):
    return {h.split('\n',1)[0]: h for h in re.split(r'\n(?=## )', t)[1:]}
def cjk(s): return len(re.findall(r'[一-鿿]', s))
def prose(t):
    out=[]; 
    for l in t.split('\n'):
        if l.startswith('> ') or l.startswith('|') or l.startswith('^') : continue
        out.append(l)
    return '\n'.join(out)
for p in sys.argv[2:]:
    a = open(os.path.join(snap, os.path.basename(p)), encoding='utf-8').read()
    b = open(p, encoding='utf-8').read()
    errs = []
    if a.split('\n## ')[0] != b.split('\n## ')[0]: errs.append('header (YAML/H1/ref/link) changed')
    ha = [x.split('\n',1)[0] for x in re.split(r'\n(?=## )', a)[1:]]
    hb = [x.split('\n',1)[0] for x in re.split(r'\n(?=## )', b)[1:]]
    if ha != hb: errs.append(f'## headings changed: {ha} -> {hb}')
    ba, bb = blocks(a), blocks(b)
    for k in ba:
        if k.startswith('## 經文') or k.startswith('## 配詩'):
            if ba[k].strip() != bb.get(k,'').strip(): errs.append(f'{k} block changed')
    la = [l for l in a.split('\n') if re.match(r'> ("|— |中譯|\*\*體例說明)', l)]
    sb = set(b.split('\n'))
    for l in la:
        if l not in sb: errs.append('quote line missing/changed: ' + l[:70])
    if '座標' not in b: errs.append('座標 line missing')
    if '你看見耶穌了嗎' not in b: errs.append('你看見耶穌了嗎 missing')
    ca, cb = cjk(prose(a)), cjk(prose(b))
    print(f'{os.path.basename(p)}: bytes {len(a.encode())}->{len(b.encode())}; prose CJK {ca}->{cb} ({cb*100//max(ca,1)}%)', 'OK' if not errs else 'FAIL')
    for e in errs[:12]: print('   -', e)
    bad += bool(errs)
sys.exit(1 if bad else 0)
