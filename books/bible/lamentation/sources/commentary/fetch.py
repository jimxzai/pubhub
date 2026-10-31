import re,html,json,time,subprocess,os
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"
def get(u):
    return subprocess.run(['curl','-s','-L','-A',UA,u],capture_output=True).stdout.decode('utf8','ignore')
def txt(h):
    h=re.sub(r'(?s)<(script|style).*?</\1>','',h)
    h=re.sub(r'</(p|div|h\d|li|tr)>','\n',h); h=re.sub(r'<br\s*/?>','\n',h)
    return re.sub(r'\n{3,}','\n\n',html.unescape(re.sub(r'<[^>]+>','',h)))
def roman(n):
    r=''
    for v,s in [(50,'l'),(40,'xl'),(10,'x'),(9,'ix'),(5,'v'),(4,'iv'),(1,'i')]:
        while n>=v: r+=s;n-=v
    return r
os.makedirs('henry',exist_ok=True)
for k in range(1,9):
    f=f'henry/lam-page-{roman(k)}.txt'
    if os.path.exists(f): continue
    open(f,'w').write(txt(get(f'https://www.ccel.org/ccel/henry/mhc4.Lam.{roman(k)}.html'))); time.sleep(1)
for c in range(1,6):
    f=f'../hebrew/lam-{c}.json'
    if os.path.exists(f) and os.path.getsize(f)>200: continue
    open(f,'w').write(get(f'https://www.sefaria.org/api/texts/Lamentations.{c}?context=0&lang=he')); time.sleep(0.8)
print('done')
