#!/usr/bin/env python3
"""heb.py <Book> <chap> [verse]  — print Sefaria Miqra Hebrew (cached in hebrew/other/)."""
import json,re,subprocess,sys,os,time
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
here=os.path.dirname(os.path.abspath(__file__)); os.makedirs(here+'/hebrew/other',exist_ok=True)
def S(s): return re.sub(r'<[^>]+>','',s).replace('&nbsp;',' ').replace('&thinsp;',' ')
def chapter(book,c):
    f=f'{here}/hebrew/other/{book}-{c}.json'
    if not os.path.exists(f):
        b=subprocess.run(['curl','-s','-A',UA,f'https://www.sefaria.org/api/texts/{book}.{c}?context=0&lang=he'],capture_output=True).stdout
        if not b.startswith(b'{'): sys.exit('blocked: '+b[:80].decode('utf8','ignore'))
        open(f,'wb').write(b); time.sleep(1)
    return [S(v) for v in json.load(open(f))['he']]
if __name__=='__main__':
    h=chapter(sys.argv[1],sys.argv[2])
    for i,v in enumerate(h,1):
        if len(sys.argv)<4 or str(i) in sys.argv[3].split(','): print(f'{sys.argv[1]} {sys.argv[2]}:{i}\t{v}')
