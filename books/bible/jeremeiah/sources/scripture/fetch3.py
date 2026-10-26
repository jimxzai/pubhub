import os,subprocess,time,urllib.parse
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"
def get(u,out):
    if os.path.exists(out) and os.path.getsize(out)>2000: return
    for k in range(4):
        b=subprocess.run(['curl','-s','-L','-A',UA,u],capture_output=True).stdout
        if len(b)>2000 and b'Too many' not in b[:400]: open(out,'wb').write(b); return
        time.sleep(5*(k+1))
    print('FAILED',u)
for c in range(1,53):
    get('https://bible.fhl.net/json/qb.php?chineses='+urllib.parse.quote('耶')+f'&chap={c}&version=unv&gb=0',f'cuv-unv-{c}.json'); time.sleep(0.5)
    get(f'https://www.cnbible.com/jeremiah/{c}.htm',f'cuvmpt-{c}.html'); time.sleep(1.2)
    get(f'https://biblehub.com/nasb/jeremiah/{c}.htm',f'nasb1995-{c}.html'); time.sleep(1.2)
print('fetch3 done')
