import re,sys,glob
f=glob.glob(f'{sys.argv[1]}-*.txt')[0]
t=open(f).read()
lines=[l.rstrip() for l in t.split('\n')]
out=[]
started=False
for l in lines:
    if l.startswith('.mw-') : 
        # css line may be followed by text on same line after '}'
        m=re.search(r'\}([^}]*)$',l)
        if m and m.group(1).strip(): out.append(m.group(1).strip())
        continue
    out.append(l)
txt='\n'.join(out)
txt=re.sub(r'\n\s*\n+','\n',txt)
i=txt.find('Layout 2')
print(txt if i<0 else txt[i:])
