import re,glob,json,os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
SLUG={'亞':'zechariah','但':'daniel','來':'hebrews','利':'leviticus','加':'galatians','可':'mark','啟':'revelation','太':'matthew','帖後':'2-thessalonians','弗':'ephesians','彼前':'1-peter','彼後':'2-peter','徒':'acts','提後':'2-timothy','林前':'1-corinthians','林後':'2-corinthians','約':'john','約壹':'1-john','羅':'romans','耶':'jeremiah','腓':'philippians','西':'colossians','詩':'psalms','賽':'isaiah','路':'luke','雅':'james'}
def norm(s): return re.sub(r'[^一-鿿]','',re.sub(r'（[^）]*）','',s).replace('裡','裏'))
AE={}
for b,s in SLUG.items():
    for f in glob.glob(f'sources/aieden/{s}-*.json'):
        c=int(f.rsplit('-',1)[1][:-5]); AE[(b,c)]=json.load(open(f))['data']['verses']
AEn={k:norm(''.join(v['textZh'] for v in vs)) for k,vs in AE.items()}
TH=norm(''.join(json.load(open('sources/cuv-verified.json')).values()))
FH={k:norm(''.join(v)) for k,v in json.load(open('sources/fhlcache.json')).items()}
KEYS=sorted(list(SLUG)+['帖前'],key=len,reverse=True)
REF=re.compile(r'(?<![一-鿿])('+'|'.join(KEYS)+r')\s*(\d+):(\d+)')
PS={'01':[33],'02':[115],'03':[103,131],'04':[119],'05':[121],'06':[51],'07':[128],'08':[116],'09':[27],'10':[34],'11':[138]}
n=0;bad=[]
for f in sorted(glob.glob('[0-9]*.md'))+['elder-wong-systematic-study.md']:
    inps=False
    for ln,l in enumerate(open(f).read().split('\n'),1):
        if l.startswith('### 詩篇'): inps=True
        elif l.startswith('##'): inps=False
        if l.startswith('> ^'): continue
        refs=[(b,int(c)) for b,c,v in REF.findall(l) if b!='帖前']
        if inps and f[:2] in PS: refs+=[('詩',c) for c in PS[f[:2]]]
        if not refs: continue
        hay=TH+''.join(AEn.get(r,'') for r in refs)
        for q in re.findall(r'「([^」]{4,})」',l):
            pieces=[norm(p) for p in re.split(r'……|…',q) if len(norm(p))>=3]
            if not pieces: continue
            n+=1
            if not all(p in hay for p in pieces):
                infhl=all(any(p in FH.get(f'{b}{c}','') for b,c in refs) for p in pieces)
                bad.append((f,ln,q,refs,infhl))
print(n,'quotes checked vs ai-eden;',len(bad),'not found')
for f,ln,q,refs,infhl in bad: print(f'{f}:{ln} {"[fhl-wording]" if infhl else "[label/other]"} 「{q[:60]}」 {refs}')
