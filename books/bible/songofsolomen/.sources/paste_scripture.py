"""paste_scripture.py <chapter.md> — replace the ## 經文 block with units/<name>.scripture.md verbatim."""
import re,sys,os
S='/Users/jimxiao/dev/pubhub/books/bible/songofsolomen/.sources'
f=sys.argv[1]; name=os.path.basename(f)[:-3]
t=open(f,encoding='utf8').read(); u=open(f'{S}/units/{name}.scripture.md',encoding='utf8').read().strip()
new,n=re.subn(r'(## 經文 \(Scripture\)\n\n).*?(\n\n---\n)',lambda m:m.group(1)+u+m.group(2),t,count=1,flags=re.S)
open(f,'w',encoding='utf8').write(new); print('replaced',n)
