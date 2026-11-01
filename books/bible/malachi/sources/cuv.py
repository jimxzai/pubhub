#!/usr/bin/env python3
"""cuv.py '創 25:23' '太 11:10-14' ... -> 和合本 (ai-eden.com, the project's standard CUV), 裡→裏.

One request per chapter, cached in sources/cuvcache/. Use it to look up EVERY verse you quote
in prose from outside Malachi (never type a verse from memory).
Output: 書章:節  ^v^text^v+1^text ...   ('<<NOT FOUND>>' if the reference does not exist)
Book names are the abbreviations the book's prose uses (創 出 ... 啟; 約壹 約貳 約參; 林前 林後 帖前 帖後 提前 提後 彼前 彼後;
撒上 撒下 王上 王下 代上 代下); '詩篇' is accepted for 詩.
"""
import sys, json, os, re, time, urllib.request

D = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(D, 'cuvcache')
os.makedirs(CACHE, exist_ok=True)
UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36'}
SLUG = dict(zip(
    "創 出 利 民 申 書 士 得 撒上 撒下 王上 王下 代上 代下 拉 尼 斯 伯 詩 箴 傳 歌 賽 耶 哀 結 但 何 珥 摩 俄 拿 彌 鴻 哈 番 該 亞 瑪 "
    "太 可 路 約 徒 羅 林前 林後 加 弗 腓 西 帖前 帖後 提前 提後 多 門 來 雅 彼前 彼後 約壹 約貳 約參 猶 啟".split(),
    "genesis exodus leviticus numbers deuteronomy joshua judges ruth 1-samuel 2-samuel 1-kings 2-kings 1-chronicles 2-chronicles "
    "ezra nehemiah esther job psalms proverbs ecclesiastes song-of-solomon isaiah jeremiah lamentations ezekiel daniel hosea joel amos "
    "obadiah jonah micah nahum habakkuk zephaniah haggai zechariah malachi matthew mark luke john acts romans 1-corinthians "
    "2-corinthians galatians ephesians philippians colossians 1-thessalonians 2-thessalonians 1-timothy 2-timothy titus philemon "
    "hebrews james 1-peter 2-peter 1-john 2-john 3-john jude revelation".split()))
SLUG['詩篇'] = 'psalms'


def chapter(book, ch):
    path = os.path.join(CACHE, f'{SLUG[book]}-{ch}.json')
    if not os.path.exists(path):
        url = f'https://www.ai-eden.com/api/bible/{SLUG[book]}/{ch}?t=CUV'
        d = None
        for _ in range(3):
            try:
                d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))
                break
            except Exception:
                time.sleep(3)
        if not d or not d.get('success'):
            return {}
        verses = {v['verse']: v['textZh'].replace('裡', '裏').replace('　', '') for v in d['data']['verses']}
        json.dump(verses, open(path, 'w'), ensure_ascii=False)
        time.sleep(0.5)
        return verses
    return {int(k): v for k, v in json.load(open(path)).items()}


for ref in sys.argv[1:]:
    m = re.match(r'(\S+)\s+(\d+):(\d+)(?:-(\d+))?$', ref.strip())
    if not m or m.group(1) not in SLUG:
        print('BAD REF', ref)
        continue
    book, ch, a, b = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4) or m.group(3))
    vs = chapter(book, ch)
    out = ''.join(f'^{v}^{vs[v]}' if v in vs else f'^{v}^<<NOT FOUND>>' for v in range(a, b + 1))
    print(f'{book}{ch}:{a}' + (f'-{b}' if b != a else '') + '  ' + out)
