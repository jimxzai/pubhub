import json,re,sys,html
def clean(s):
    s=re.sub(r'<sup class="footnote-marker">.*?</sup>','',s); s=re.sub(r'<i class="footnote">.*?</i>','',s)
    s=re.sub(r'<[^>]+>','',s); return html.unescape(s).replace(' ',' ').strip()
def chapter(c):
    d=json.load(open(f'/Users/jimxiao/dev/pubhub/books/bible/lamentation/sources/hebrew/lam-{c}.json'))
    return [clean(v) for v in d['he']]
def strip(s): return re.sub(r'[֑-ׇ]','',s).replace('־',' ')
if __name__=='__main__':
    c=int(sys.argv[1]); vs=chapter(c)
    for i,v in enumerate(vs,1):
        if len(sys.argv)<3 or str(i) in sys.argv[2].split(','): print(c,i,v)
