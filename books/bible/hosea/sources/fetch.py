import re,html,json,time,subprocess,os
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
def get(u): return subprocess.run(['curl','-s','-L','-A',UA,u],capture_output=True).stdout.decode('utf8','ignore')
def txt(h):
    h=re.sub(r'(?s)<(script|style).*?</\1>','',h)
    h=re.sub(r'</(p|div|h\d|li|tr)>','\n',h); h=re.sub(r'<br\s*/?>','\n',h)
    return re.sub(r'\n{3,}','\n\n',html.unescape(re.sub(r'<[^>]+>','',h)))
def roman(n):
    r=''
    for v,s in [(50,'l'),(40,'xl'),(10,'x'),(9,'ix'),(5,'v'),(4,'iv'),(1,'i')]:
        while n>=v: r+=s;n-=v
    return r
for d in ('commentary/henry','commentary/calvin','hebrew'): os.makedirs(d,exist_ok=True)
for k in range(1,16):  # Hos.i = intro, Hos.ii = ch1 ... Hos.xv = ch14
    f=f'commentary/henry/hos-page-{roman(k)}.txt'
    if not os.path.exists(f): open(f,'w').write(txt(get(f'https://www.ccel.org/ccel/henry/mhc4.Hos.{roman(k)}.html'))); time.sleep(1)
if not os.path.exists('commentary/calvin-26.xml'): open('commentary/calvin-26.xml','w').write(get('https://www.ccel.org/ccel/calvin/calcom26.xml'))
open('commentary/calvin/calcom26.txt','w').write(txt(open('commentary/calvin-26.xml',errors='ignore').read()))
for c in range(1,15):
    f=f'hebrew/hos-{c}.json'
    if not os.path.exists(f): open(f,'w').write(get(f'https://www.sefaria.org/api/texts/Hosea.{c}?context=0&lang=he')); time.sleep(0.8)
print('done')
