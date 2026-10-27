import re,glob,html,hashlib,collections,sys,os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
UNITS=[(1,(1,1),(1,4)),(2,(1,5),(1,8)),(3,(1,9),(2,7)),(4,(2,8),(2,17)),(5,(3,1),(3,5)),(6,(3,6),(3,11)),
(7,(4,1),(4,15)),(8,(4,16),(5,1)),(9,(5,2),(5,8)),(10,(5,9),(6,3)),(11,(6,4),(6,13)),(12,(7,1),(7,9)),
(13,(7,10),(8,4)),(14,(8,5),(8,7)),(15,(8,8),(8,14))]
def unit(c,v):
    for n,a,b in UNITS:
        if a<=(c,v)<=b: return n
SRC={"Ellicott":"ellicott","Matthew Henry":"henry-concise","Barnes":"barnes","Jamieson":"jfb","Gill":"gill","Geneva":"geneva",
"Cambridge":"cambridge","Keil":"kd","Pulpit":"pulpit","Poole":"poole","Benson":"benson","Clarke":"clarke","Expositor":"expositors","Wesley":"wesley","Coke":"coke","Guzik":"guzik","Darby":"darby","Kelly":"kelly","Lange":"lange","MacLaren":"maclaren","Scofield":"scofield"}
def slug(h):
    for k,v in SRC.items():
        if k in h: return v
    return None
def clean(s):
    s=re.sub(r'<span class="p"><br\s*/?><br\s*/?></span>','\n\n',s)
    s=re.sub(r'<br\s*/?>','\n',s)
    s=re.sub(r'<[^>]+>','',s)
    s=html.unescape(s)
    s=re.sub(r'[ \t\xa0]+',' ',s); s=re.sub(r'\n[ \t]+','\n',s); s=re.sub(r'\n{3,}','\n\n',s)
    return s.strip()
data=collections.defaultdict(lambda: collections.defaultdict(list))  # src->unit->[(c,v,text)]
seen=set(); names={}; cov=collections.defaultdict(set)
for f in sorted(glob.glob('[0-9]-[0-9]*.html'),key=lambda x:tuple(map(int,x[:-5].split('-')))):
    c,v=map(int,f[:-5].split('-'))
    t=open(f,errors='ignore').read()
    t=re.sub(r'<div class="comtype">[^<]*</div>','',t)
    parts=re.split(r'(?=<div class="vheading2">)',t)
    for p in parts[1:]:
        m=re.match(r'<div class="vheading2"><a [^>]*>(.*?)</a></div>',p)
        if not m: continue
        h=html.unescape(m.group(1)); s=slug(h)
        if not s: continue
        names[s]=h
        body=p[m.end():]
        k=body.find('<div id="mdd">')
        if k>=0: body=body[:k]
        txt=clean(body)
        if len(txt)<20: continue
        key=(s,hashlib.md5(txt.encode()).hexdigest())
        if key in seen: continue
        seen.add(key)
        data[s][unit(c,v)].append((c,v,txt)); cov[s].add((c,v))
ALL=[(c,v) for c,n in zip(range(1,9),[17,17,11,16,16,13,13,14]) for v in range(1,n+1)]
idx=[]
for s in sorted(data):
    tot=0; units=0
    for u in sorted(data[s]):
        with open(f'{s}-{u:02d}.txt','w') as fh:
            fh.write(f'# {names[s]} on Song of Solomon (unit {u:02d}); source: biblehub.com/commentaries/songs/<chapter>-<verse>.htm (public domain; fetched 2026-10-26). Sections repeated verbatim on several verse pages kept once, at first verse.\n\n')
            for c,v,txt in data[s][u]:
                fh.write(f'===== [Song of Solomon {c}:{v}] =====\n{txt}\n\n')
                tot+=len(txt.split())
        units+=1
    miss=[f'{c}:{v}' for c,v in ALL if (c,v) not in cov[s]]
    idx.append((s,names[s],units,len(cov[s]),tot,miss))
with open('_INDEX.txt','w') as fh:
    fh.write('# commentary/ index — Song of Solomon (S1, biblehub per-verse pages, fetched 2026-10-26)\n')
    fh.write('# columns: file-prefix | author/work | units covered /15 | verse pages with a NEW section /117 | words (whitespace-split)\n')
    for s,h,u,nv,w,miss in idx:
        fh.write(f'{s}-NN.txt | {h} | {u}/15 | {nv}/117 | {w}\n')
    fh.write('\n# verses with no new section (either not commented by that source, or section identical to an earlier verse page and kept once):\n')
    for s,h,u,nv,w,miss in idx:
        fh.write(f'{s}: {" ".join(miss) if miss else "(none)"}\n')
print(open('_INDEX.txt').read())
