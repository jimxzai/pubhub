import os,subprocess,time,urllib.parse
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"
def get(u,out,minsize=500):
    if os.path.exists(out) and os.path.getsize(out)>minsize: return
    for k in range(5):
        b=subprocess.run(['curl','-s','-L','-A',UA,u],capture_output=True).stdout
        if len(b)>minsize and b'RATE_LIMITED' not in b[:400] and b'Too many' not in b[:400]: open(out,'wb').write(b); return
        time.sleep(6*(k+1))
    print('FAILED',u)
for c in range(1,6):
    get('https://bible.fhl.net/json/qb.php?chineses='+urllib.parse.quote('哀')+f'&chap={c}&version=unv&gb=0',f'cuv-unv-{c}.json'); time.sleep(0.5)
    get(f'https://www.cnbible.com/cuvmpt/lamentations/{c}.htm',f'cuvmpt-{c}.html',2000); time.sleep(1.2)
    get(f'https://biblehub.com/nasb/lamentations/{c}.htm',f'nasb1995-{c}.html',2000); time.sleep(1.2)
    get(f'https://www.ai-eden.com/api/bible/lamentations/{c}?t=CUV,NASB',f'aieden-{c}.json'); time.sleep(8)
print('done')
