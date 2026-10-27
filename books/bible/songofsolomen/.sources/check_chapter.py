"""check_chapter.py <chapter.md> — mechanical checks every chapter must pass (run from anywhere).
 1. every English  > "quote"  is a verbatim substring (case/punct/whitespace-insensitive) of some file in .sources/commentary, longform, xref(NASB col) or scripture tsv
 2. the ## 經文 block equals units/<same name>.scripture.md
 3. every Hebrew token in the chapter appears byte-exact in hebrew/song-he.tsv (lemma forms listed as 'lemma' are tolerated if consonants+marks match a tsv word)
 4. 11 H2 sections in order, 座標 present, 你看見…了嗎 present, 7-line YAML
"""
import re,sys,os,glob
S='/Users/jimxiao/dev/pubhub/books/bible/songofsolomen/.sources'
f=sys.argv[1]; name=os.path.basename(f)[:-3]
t=open(f,encoding='utf8').read()
def norm(s): return re.sub(r'[^a-z0-9Ͱ-Ͽ֐-׿]+','',re.sub(r'-\s*\n\s*','',s).lower())
print('chapter',name,len(t.encode('utf8')),'bytes')
# 1 quotes
corpus={}
for p in glob.glob(S+'/commentary/*.txt')+glob.glob(S+'/longform/*.txt')+glob.glob(S+'/xref/*.tsv')+glob.glob(S+'/scripture-0*.tsv'):
    corpus[p]=norm(open(p,encoding='utf8',errors='ignore').read())
qs=re.findall(r'^> "(.+?)"\s*$',t,re.M)
bad=0
for q in qs:
    parts=[x for x in re.split(r'\s*(?:\.\.\.|…)\s*',q) if x.strip()]
    ok=all(any(norm(x) in c for c in corpus.values()) for x in parts)
    if not ok: bad+=1; print('  QUOTE NOT FOUND:',q[:110])
print(f'quotes: {len(qs)} checked, {bad} not found')
# 2 scripture block
unit=f'{S}/units/{name}.scripture.md'
if os.path.exists(unit):
    m=re.search(r'## 經文 \(Scripture\)\n\n(.*?)\n\n---\n',t,re.S)
    u=open(unit,encoding='utf8').read().strip()
    print('scripture block == unit file:', bool(m) and m.group(1).strip()==u)
else: print('no unit file for',name)
# 3 hebrew
heb=open(S+'/hebrew/song-he.tsv',encoding='utf8').read().replace('־',' ')
import unicodedata
def key(w):
    d=unicodedata.normalize('NFD',w); return ''.join(c for c in d if not unicodedata.combining(c)),''.join(sorted(c for c in d if unicodedata.combining(c)))
tsvk={key(w) for w in re.findall(r'[֐-׿]+',heb)}
lit=[w for w in set(re.findall(r'[֐-׿]+',t)) if w not in heb]
nomatch=[w for w in lit if key(w) not in tsvk]
print('hebrew tokens not byte-exact in tsv (lemma forms etc.):',lit,'| consonant+mark mismatch:',nomatch)
# 4 structure
h2=re.findall(r'^## (.+)$',t,re.M)
want=['基督焦點','配詩','經文','背景','原文研讀','領受要點','歷代注疏','詩篇與聖詩','老弟兄查經','生命應用','與其他經文的關聯']
okh=len(h2)==11 and all(w in h for w,h in zip(want,h2))
print('11 sections in order:',okh, '' if okh else h2)
print('座標:','座標' in t,'| 你看見…了嗎:',bool(re.search(r'你看見[^\n]{0,12}了嗎',t)),'| YAML 7 lines:',t.split('\n')[6]=='---' and t.startswith('---\n'))
