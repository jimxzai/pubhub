import re,html,time,subprocess,os,sys
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124 Safari/537.36"
def get(u): return subprocess.run(['curl','-s','-L','-A',UA,u],capture_output=True).stdout.decode('utf8','ignore')
def txt(h):
    h=re.sub(r'(?s)<(script|style).*?</\1>','',h)
    h=re.sub(r'</(p|div|h\d|li|tr)>','\n',h); h=re.sub(r'<br\s*/?>','\n',h)
    return re.sub(r'\n{3,}','\n\n',html.unescape(re.sub(r'<[^>]+>','',h)))
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'commentary'))
for k in ['i','ii','iii','iv','v','vi','vii','viii','ix']:
    f=f'henry/mic-page-{k}.txt'
    if not os.path.exists(f):
        open(f,'w').write(txt(get(f'https://www.ccel.org/ccel/henry/mhc4.Mic.{k}.html'))); time.sleep(1)
for n in (27,28):
    open(f'calvin/calcom{n}.txt','w').write(txt(open(f'calvin-{n}.xml',errors='ignore').read()))
