"""grab.py <src> <NN> [verse-tag e.g. 2:8] [maxchars] — print a commentary section (commentary/<src>-NN.txt) ; without verse: list verse tags and sizes."""
import sys,re
S='/Users/jimxiao/dev/pubhub/books/bible/songofsolomen/.sources/commentary'
src,nn=sys.argv[1],sys.argv[2].zfill(2)
t=open(f'{S}/{src}-{nn}.txt',encoding='utf8').read()
parts=re.split(r'\n(?====== \[Song of Solomon )',t)
secs={}
for p in parts:
    m=re.match(r'===== \[Song of Solomon ([^\]]+)\] =====\n(.*)',p,re.S)
    if m: secs[m.group(1)]=m.group(2).strip()
if len(sys.argv)<4:
    print({k:len(v) for k,v in secs.items()})
else:
    mx=int(sys.argv[4]) if len(sys.argv)>4 else 3000
    print(secs.get(sys.argv[3],'(none)')[:mx])
