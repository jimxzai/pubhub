#!/usr/bin/env python3
"""Fetch hymn texts from Wikisource (public domain). Tries candidate page titles, falls back to search."""
import html, json, re, sys, urllib.parse, urllib.request
UA = {'User-Agent': 'pubhub-research/1.0 (sales@xwire.ai)'}
WANT = {
 '01-abide-with-me': ['The Army and Navy Hymnal/Hymns/Abide with Me! Fast Falls the Eventide', 'The Army and Navy Hymnal/Hymns/Abide with Me'],
 '02-jesus-thou-joy': ['Jesus, Thou Joy of Loving Hearts', 'Jesus, Thou Joy of loving hearts'],
 '03-our-help': ['The Army and Navy Hymnal/Hymns/Our God, Our Help in Ages Past'],
 '04-blest-be-the-tie': ['Blest Be the Tie That Binds', 'Blest be the tie that binds'],
 '05-holy-holy-holy': ['The Army and Navy Hymnal/Hymns/Holy, Holy, Holy, Lord God Almighty', 'The Army and Navy Hymnal/Hymns/Holy, Holy, Holy', 'Holy, Holy, Holy, Lord God Almighty'],
 '06-jesus-lover': ['The Army and Navy Hymnal/Hymns/Jesus, Lover of My Soul'],
 '07-it-is-well': ['It Is Well with My Soul', 'It is well with my soul'],
 '08-mysterious-way': ['Olney Hymns (1840)/Book 3/Hymn 15', 'The Army and Navy Hymnal/Hymns/God Moves in a Mysterious Way', 'Light Shining out of Darkness'],
 '09-work-for-the-night': ['The Army and Navy Hymnal/Hymns/Work for the Night Is Coming'],
 '10-god-of-earth-and-altar': ['Poems (Chesterton, 1915)/A Hymn'],
 '11-sowing-in-the-morning': ['Sowing in the Morning', 'Sowing in the morning'],
 '12-saviour-like-a-shepherd': ['Saviour, Like a Shepherd Lead Us', 'Savior, Like a Shepherd Lead Us', 'Saviour, like a shepherd lead us'],
}
def api(**kw):
    url = 'https://en.wikisource.org/w/api.php?' + urllib.parse.urlencode(dict(kw, format='json'))
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))
def render(title):
    d = api(action='parse', page=title, prop='text', redirects=1)
    h = d['parse']['text']['*']
    h = re.sub(r'(?is)<(style|script)[^>]*>.*?</\1>', '', h)
    h = re.sub(r'<br\s*/?>', '\n', h); h = re.sub(r'</(p|div|tr|li|dd|dt)>', '\n', h)
    t = html.unescape(re.sub(r'<[^>]+>', '', h))
    return d['parse']['title'], re.sub(r'\n\s*\n+', '\n\n', t).strip()
for key, cands in WANT.items():
    if len(sys.argv) > 1 and sys.argv[1] not in key: continue
    got = None
    for c in cands:
        try:
            title, t = render(c)
            if len(t) > 300: got = (title, t); break
        except Exception as e:
            pass
    if not got:
        s = api(action='query', list='search', srsearch=cands[0] + ' hymn', srlimit=5)
        print('!!', key, 'no direct page; search hits:', [r['title'] for r in s['query']['search']])
        continue
    open(f'{key}.txt', 'w').write(f'SOURCE: Wikisource, "{got[0]}"\n\n{got[1]}\n')
    print('==', key, got[0], len(got[1]))
