import re,glob,json,sys,time,urllib.parse,urllib.request,os
sys.path.insert(0,'sources')
ABBR={'創':'創','出':'出','利':'利','民':'民','申':'申','書':'書','詩':'詩','箴':'箴','賽':'賽','耶':'耶','結':'結','但':'但','亞':'亞','太':'太','可':'可','路':'路','約':'約','徒':'徒','羅':'羅','林前':'林前','林後':'林後','加':'加','弗':'弗','腓':'腓','西':'西','帖前':'帖前','帖後':'帖後','提前':'提前','提後':'提後','來':'來','雅':'雅','彼前':'彼前','彼後':'彼後','約壹':'約壹','猶':'猶','啟':'啟','王下':'王下','王上':'王上','撒下':'撒下'}
KEYS=sorted(ABBR,key=len,reverse=True)
REF=re.compile(r'(?<![一-鿿])('+'|'.join(KEYS)+r')\s*(\d+):(\d+)')
CACHE='sources/fhlcache.json'
cache=json.load(open(CACHE)) if os.path.exists(CACHE) else {}
UA={'User-Agent':'Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/128.0 Safari/537.36'}
def chapter(b,c):
    b={'約壹':'約一'}.get(b,b)
    k=f'{b}{c}'
    if k not in cache:
        u=f"https://bible.fhl.net/json/qb.php?chineses={urllib.parse.quote(b)}&chap={c}&sec=1-200&version=unv&gb=0"
        d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers=UA)))
        cache[k]=[r['bible_text'] for r in d.get('record',[])]; time.sleep(0.4)
        if not cache[k]: print('EMPTY FETCH',b,c)
        json.dump(cache,open(CACHE,'w'),ensure_ascii=False)
    return ''.join(cache[k])
def norm(s):
    s=re.sub(r'（[^）]*）','',s)
    s=s.replace('裡','裏').replace('　','').replace('─','—')
    return re.sub(r'[^一-鿿A-Za-z0-9]','',s)
bad=0;n=0
for f in sorted(glob.glob('[0-9][0-9]-*.md'))+['00-overview.md','00a-1thess-position.md','00c-revelation-order.md','elder-wong-systematic-study.md','000-preface.md','999-afterword.md']:
    inblock=False
    for ln,l in enumerate(open(f).read().split('\n'),1):
        if l.startswith('>'): continue
        refs=set(REF.findall(l.replace('帖前','帖前')))
        quotes=re.findall(r'「([^」]{4,})」',l)
        if not quotes or not refs: continue
        hay=''
        for b,c,v in refs:
            try: hay+=chapter(b,c)
            except Exception as e: hay+=''
        hay+=''.join(chapter('帖前',c) for c in range(1,6))
        hay=norm(hay)
        for q in quotes:
            pieces=[norm(p) for p in re.split(r'…+|……|⋯',q) if len(norm(p))>=3]
            n+=1
            if pieces and not all(p in hay for p in pieces):
                bad+=1; print(f'{f}:{ln} refs={sorted({b+c+":"+v for b,c,v in refs})}\n   「{q[:70]}」')
print(n,'quotes with in-line refs;',bad,'not found in any cited chapter')
