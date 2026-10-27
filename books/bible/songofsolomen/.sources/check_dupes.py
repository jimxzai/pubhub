"""check_dupes.py — list English > "quotes" that appear in more than one chapter/front-matter file."""
import re,glob,collections
D='/Users/jimxiao/dev/pubhub/books/bible/songofsolomen'
seen=collections.defaultdict(set)
for f in sorted(glob.glob(D+'/[0-9]*.md')):
    for q in re.findall(r'^> "(.+?)"\s*$',open(f,encoding='utf8').read(),re.M):
        seen[re.sub(r'[^a-z0-9]+','',q.lower())].add(f.split('/')[-1])
d=[(k,v) for k,v in seen.items() if len(v)>1]
print(len(d),'duplicated quotes'); [print(sorted(v),k[:60]) for k,v in d]
