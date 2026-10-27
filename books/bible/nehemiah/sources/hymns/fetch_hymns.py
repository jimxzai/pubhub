#!/usr/bin/env python3
"""Fetch rendered hymn texts from Wikisource (The Army and Navy Hymnal, 1920, public domain)."""
import html, json, re, urllib.parse, urllib.request
P = 'The Army and Navy Hymnal/Hymns/'
PAGES = {
    '01-sweet-hour': P + 'Sweet Hour of Prayer',
    '02-guide-me': P + 'Guide Me, O Thou Great Jehovah',
    '03-churchs-one-foundation': P + "The Church's One Foundation",
    '04-mighty-fortress': P + 'A Mighty Fortress is Our God',
    '05-crowded-ways': P + 'Where Cross the Crowded Ways of Life',
    '06-soldier-of-the-cross': P + 'Am I a Soldier of the Cross',
    '07-blest-be-the-tie': P + 'Blest Be the Tie That Binds',
    '08-break-thou': P + 'Break Thou the Bread of Life',
    '09-our-help': P + 'Our God, Our Help in Ages Past',
    '10-take-my-life': P + 'Take My Life, and Let It Be',
    '11-glorious-things': P + 'Glorious Things of Thee are Spoken',
    '12-o-worship-the-king': P + 'O Worship the King, All-Glorious Above',
    '13-come-thou-fount': P + 'Come, Thou Fount of Every Blessing',
}
UA = {'User-Agent': 'pubhub-research/1.0 (sales@xwire.ai)'}
for key, title in PAGES.items():
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
