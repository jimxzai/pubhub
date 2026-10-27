#!/usr/bin/env python3 -I
import re, html, json
def parse(c):
    t = open(f'biblehub/nasb{c}.html', encoding='utf-8', errors='ignore').read()
    s = t.find('<div class="chap">'); e = t.find('</div>', s)
    # chapter div may nest; cut at footnote marker if any
    body = t[s:]
    body = re.split(r'<div class="vheading2"|<div id="rightbox"|</div></div>', body)[0]
    parts = re.split(r'<span class="reftext"><a [^>]*><b>(\d+)</b></a></span>', body)
    out = {}
    for i in range(1, len(parts), 2):
        n = int(parts[i]); seg = parts[i+1]
        seg = re.sub(r'<i>(.*?)</i>', r'*\1*', seg, flags=re.S)
        seg = re.sub(r'<br\s*/?>', ' ', seg)
        seg = re.sub(r'<font[^>]*>.*?</font>', '', seg, flags=re.S) if '<b><i>' in seg else seg
        seg = re.sub(r'<[^>]+>', ' ', seg)
        seg = html.unescape(seg).replace('\xa0', ' ')
        seg = re.sub(r'\s+', ' ', seg).strip()
        out[n] = seg
    return out
if __name__ == '__main__':
    res = {}
    for c in range(1, 9):
        for n, s in parse(c).items(): res[f'{c}:{n}'] = s
    json.dump(res, open('_nasb95.json', 'w'), ensure_ascii=False, indent=0)
    print(len(res))
    ai = {}
    for c in range(1, 9):
        for v in json.load(open(f'ai-eden/ch{c}.json'))['data']['verses']: ai[f"{c}:{v['verse']}"] = v['text']
    N = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
    bad = 0
    for k in ai:
        if N(res.get(k, '')) != N(ai[k]):
            bad += 1; print(k, '\n BH', res.get(k), '\n AI', ai[k])
    print('diff', bad)
