"""Usage: fix_hebrew.py <chapter.md>  — replace every Hebrew token in the file with the byte-exact form from hebrew/song-he.tsv
(match on consonants + set of combining marks, ignoring mark order). Reports tokens that match nothing."""
import re,sys,unicodedata
tsv=open('/Users/jimxiao/dev/pubhub/books/bible/songofsolomen/.sources/hebrew/song-he.tsv',encoding='utf8').read()
def key(w):
    d=unicodedata.normalize('NFD',w)
    cons=''.join(c for c in d if not unicodedata.combining(c))
    marks=''.join(sorted(c for c in d if unicodedata.combining(c)))
    return cons,marks
HEB=re.compile(r'[֐-׿]+')
idx={}
for tok in HEB.findall(tsv.replace('־',' ')):
    idx.setdefault(key(tok),tok)
f=sys.argv[1]; t=open(f,encoding='utf8').read(); miss=set()
def sub(m):
    w=m.group(0); k=key(w)
    if k in idx: return idx[k]
    # fall back: same consonants and mark SET ignoring cantillation
    miss.add(w); return w
t2=HEB.sub(sub,t)
open(f,'w',encoding='utf8').write(t2)
print('missing:',sorted(miss))
