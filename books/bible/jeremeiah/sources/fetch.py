import re,html,json,time,subprocess,sys,os
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"
def get(u):
    return subprocess.run(['curl','-s','-A',UA,u],capture_output=True).stdout.decode('utf8','ignore')
def txt(h):
    h=re.sub(r'(?s)<(script|style).*?</\1>','',h)
    h=re.sub(r'</(p|div|h\d|li|tr)>','\n',h); h=re.sub(r'<br\s*/?>','\n',h)
    return re.sub(r'\n{3,}','\n\n',html.unescape(re.sub(r'<[^>]+>','',h)))
def roman(n):
    r='';
    for v,s in [(50,'l'),(40,'xl'),(10,'x'),(9,'ix'),(5,'v'),(4,'iv'),(1,'i')]:
        while n>=v: r+=s;n-=v
    return r
os.makedirs('commentary/henry',exist_ok=True); os.makedirs('commentary/calvin',exist_ok=True); os.makedirs('hebrew',exist_ok=True)
# Henry: Jer.i = intro, Jer.ii = ch1 ... verify later by headings
for k in range(1,54):
    f=f'commentary/henry/jer-page-{roman(k)}.txt'
    if os.path.exists(f): continue
    open(f,'w').write(txt(get(f'https://www.ccel.org/ccel/henry/mhc4.Jer.{roman(k)}.html'))); time.sleep(1)
# Calvin vol 17 (Jer 1-9); 18-21 already as xml
if not os.path.exists('commentary/calvin-17.xml'):
    open('commentary/calvin-17.xml','w').write(get('https://www.ccel.org/ccel/calvin/calcom17.xml'))
for n in range(17,22):
    t=open(f'commentary/calvin-{n}.xml',errors='ignore').read()
    open(f'commentary/calvin/calcom{n}.txt','w').write(txt(t))
# Sefaria Hebrew
for c in range(1,53):
    f=f'hebrew/jer-{c}.json'
    if os.path.exists(f): continue
    open(f,'w').write(get(f'https://www.sefaria.org/api/texts/Jeremiah.{c}?context=0&lang=he')); time.sleep(0.7)
print('done')
