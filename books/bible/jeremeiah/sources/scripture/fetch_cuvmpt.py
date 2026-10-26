import os,subprocess,time
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"
for c in range(1,53):
    out=f'cuvmpt-{c}.html'
    for k in range(4):
        b=subprocess.run(['curl','-s','-L','-A',UA,f'https://www.cnbible.com/cuvmpt/jeremiah/{c}.htm'],capture_output=True).stdout
        if len(b)>2000: open(out,'wb').write(b); break
        time.sleep(4)
    else: print('FAILED',c)
    time.sleep(1)
print('done')
