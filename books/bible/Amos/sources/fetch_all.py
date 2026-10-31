import re,html,json,time,subprocess,os,urllib.parse
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"
def curl(u):
    for k in range(4):
        b=subprocess.run(['curl','-s','-L','-A',UA,u],capture_output=True).stdout
        if len(b)>1500 and b'Too many' not in b[:400]: return b
        time.sleep(4*(k+1))
    print('FAILED',u); return b''
def txt(h):
    h=re.sub(r'(?s)<(script|style).*?</\1>','',h)
    h=re.sub(r'</(p|div|h\d|li|tr)>','\n',h); h=re.sub(r'<br\s*/?>','\n',h)
    return re.sub(r'\n{3,}','\n\n',html.unescape(re.sub(r'<[^>]+>','',h)))
def roman(n):
    r=''
    for v,s in [(50,'l'),(40,'xl'),(10,'x'),(9,'ix'),(5,'v'),(4,'iv'),(1,'i')]:
        while n>=v: r+=s;n-=v
    return r
def save(path,b):
    if not os.path.exists(path): open(path,'wb').write(b)
for c in range(1,10):
    save(f'scripture/cuv-unv-{c}.json',curl('https://bible.fhl.net/json/qb.php?chineses='+urllib.parse.quote('摩')+f'&chap={c}&version=unv&gb=0')); time.sleep(.5)
    save(f'scripture/cuvmpt-{c}.html',curl(f'https://www.cnbible.com/cuvmpt/amos/{c}.htm')); time.sleep(1)
    save(f'scripture/nasb1995-{c}.html',curl(f'https://biblehub.com/nasb/amos/{c}.htm')); time.sleep(1)
    save(f'hebrew/amos-{c}.json',curl(f'https://www.sefaria.org/api/texts/Amos.{c}?context=0&lang=he')); time.sleep(.7)
for k in range(1,12):
    f=f'commentary/henry/amos-page-{roman(k)}.txt'
    if not os.path.exists(f): open(f,'w').write(txt(curl(f'https://www.ccel.org/ccel/henry/mhc4.Amos.{roman(k)}.html').decode('utf8','ignore'))); time.sleep(1)
save('commentary/calcom27.xml',curl('https://www.ccel.org/ccel/calvin/calcom27.xml'))
if os.path.exists('commentary/calcom27.xml'):
    open('commentary/calvin/calcom27.txt','w').write(txt(open('commentary/calcom27.xml',errors='ignore').read()))
print('done')
