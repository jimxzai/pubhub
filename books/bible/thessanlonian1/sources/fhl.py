import json,sys,urllib.parse,urllib.request
from cuvconv import conv
def get(book,ch,secs):
    u=f"https://bible.fhl.net/json/qb.php?chineses={urllib.parse.quote(book)}&chap={ch}&sec={secs}&version=unv&gb=0"
    d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/128.0 Safari/537.36"})))
    return [(r['chap'],r['sec'],conv(r['bible_text'])) for r in d['record']]
if __name__=='__main__':
    for a in sys.argv[1:]:
        b,c,s=a.split(':')
        for ch,sec,t in get(b,c,s): print(f'{b}{ch}:{sec} {t}')
