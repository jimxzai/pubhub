"""show_unit.py NN — print unit NN's CUV text, Hebrew lines, and speaker rows (compact)."""
import sys,re,glob
S='/Users/jimxiao/dev/pubhub/books/bible/songofsolomen/.sources'
n=sys.argv[1].zfill(2)
u=glob.glob(f'{S}/units/{n}-*.scripture.md')[0]
t=open(u,encoding='utf8').read()
print(u.split('/')[-1]); print(t.split('### English')[0])
verses=re.findall(r'\^(\d+(?::\d+)?)\^',t)
cur=None; keys=[]
for v in verses:
    if ':' in v: cur=int(v.split(':')[0]); keys.append(v)
    else:
        if cur is None:
            m=re.search(r'雅歌\s*(\d+)',open(glob.glob(f'{S}/PLAN.md')[0],encoding='utf8').read())
        keys.append(v)
# chapter inference from PLAN
plan=open(f'{S}/PLAN.md',encoding='utf8').read()
row=[l for l in plan.split('\n') if l.startswith(f'| {n} |')][0]
rng=re.search(r'歌 (\d+):(\d+)(?:-(?:(\d+):)?(\d+))?',row)
c1,v1=int(rng.group(1)),int(rng.group(2)); c2=int(rng.group(3) or c1); v2=int(rng.group(4) or v1)
he={}
for l in open(f'{S}/hebrew/song-he.tsv',encoding='utf8'):
    k,tx=l.rstrip('\n').split('\t',1); he[k]=tx
print('--- Hebrew (English verse numbering)')
for k,tx in he.items():
    c,v=map(int,k.split(':'))
    if (c,v)>=(c1,v1) and (c,v)<=(c2,v2): print(k,tx)
print('--- speakers')
for l in open(f'{S}/speakers.tsv',encoding='utf8'):
    if l.startswith(n+'\t'): print(l.rstrip()[:260])
