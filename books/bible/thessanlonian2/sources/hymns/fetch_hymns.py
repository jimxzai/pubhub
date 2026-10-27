#!/usr/bin/env python3
"""Fetch rendered hymn texts from Wikisource (public-domain printed hymnals)."""
import html, json, re, sys, urllib.parse, urllib.request
PAGES = {
    'mighty-fortress': 'The Army and Navy Hymnal/Hymns/A Mighty Fortress is Our God',
    'churchs-one-foundation': "The Army and Navy Hymnal/Hymns/The Church's One Foundation",
    'work-for-the-night': 'The Army and Navy Hymnal/Hymns/Work for the Night Is Coming',
    'guide-me': 'The Army and Navy Hymnal/Hymns/Guide Me, O Thou Great Jehovah',
    'faith-of-our-fathers': 'The Army and Navy Hymnal/Hymns/Faith of Our Fathers, Living Still',
    'how-firm': 'The Army and Navy Hymnal/Hymns/How Firm a Foundation',
    'lo-he-comes': 'The English Hymnal (1906)',
}
UA = {'User-Agent': 'pubhub-research/1.0 (sales@xwire.ai)'}
for key, title in PAGES.items():
    if key == 'lo-he-comes':
        continue
    url = 'https://en.wikisource.org/w/api.php?' + urllib.parse.urlencode(
        {'action': 'parse', 'page': title, 'prop': 'text', 'format': 'json', 'redirects': 1})
    d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA)))
    h = d['parse']['text']['*']
    h = re.sub(r'<br\s*/?>', '\n', h)
    h = re.sub(r'</(p|div|tr|li)>', '\n', h)
    t = html.unescape(re.sub(r'<[^>]+>', '', h))
    t = re.sub(r'\n\s*\n+', '\n\n', t).strip()
    open(f'{key}.txt', 'w').write(f'SOURCE: Wikisource, "{title}"\n\n{t}\n')
    print('==', key, len(t))
