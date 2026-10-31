#!/usr/bin/env python3
"""cuv.py '王下 14:25' '太 12:39-41' ... → 和合本 (fhl unv) text, 裡→裏. Caches in .sources/cuvcache.json.
Spaced out on purpose (fhl is a shared server). Use it to verify EVERY cross-reference you quote."""
import sys, json, os, re, time, urllib.parse, urllib.request
D = os.path.dirname(os.path.abspath(__file__)); CACHE = D + '/cuvcache.json'
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36'}
for ref in sys.argv[1:]:
    m = re.match(r'(\S+)\s+(\d+):(\d+)(?:-(\d+))?$', ref.strip())
    if not m: print('BAD REF', ref); continue
    book, ch, a, b = m.group(1), m.group(2), int(m.group(3)), int(m.group(4) or m.group(3))
    out = []
    for v in range(a, b + 1):
        key = f'{book} {ch}:{v}'
        if key not in cache:
            url = 'https://bible.fhl.net/json/qb.php?chineses=%s&chap=%s&sec=%d&version=unv&strong=0' % (urllib.parse.quote(book), ch, v)
            for _ in range(3):
                try:
                    d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30)); break
                except Exception as e:
                    time.sleep(3); d = {}
            rec = d.get('record') or []
            cache[key] = rec[0]["bible_text"].replace("裡", "裏").replace("　", "") if rec else None
            time.sleep(0.6)
        out.append(f'^{v}^{cache[key]}' if cache[key] else f'^{v}^<<NOT FOUND>>')
    print(f'{book}{ch}:{a}' + (f'-{b}' if b != a else '') + '  ' + ''.join(out))
json.dump(cache, open(CACHE, 'w'), ensure_ascii=False, indent=0)
