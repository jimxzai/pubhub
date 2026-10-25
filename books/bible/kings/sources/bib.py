#!/usr/bin/env python3
"""bib.py "王下 8:19" "約 2:19-21" ...  -> 和合本 (fhl unv; 裡->裏), ^n^ verse markers.
Book = fhl short name (王下 代下 約 太 路 啟 申 詩 來 ...)."""
import sys, json, urllib.request, urllib.parse, re
for ref in sys.argv[1:]:
    m = re.match(r'(\S+)\s+(\d+):([\d,-]+)$', ref)
    b, ch, v = m.groups()
    u = ('https://bible.fhl.net/json/qb.php?chineses=%s&chap=%s&sec=%s&version=unv'
         % (urllib.parse.quote(b), ch, v))
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/124 Safari/537.36'})
    import time
    for _try in range(6):
        try:
            d = json.load(urllib.request.urlopen(req, timeout=20)); break
        except Exception:
            time.sleep(2 + 2 * _try)
    else:
        raise SystemExit('fhl unreachable: ' + ref)
    print('== ' + ref)
    for r in d['record']:
        print('^%d^%s' % (r['sec'], r['bible_text'].strip().replace('裡', '裏')))
