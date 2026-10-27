import json,os,time,urllib.request
SLUG={'亞':'zechariah','但':'daniel','來':'hebrews','利':'leviticus','加':'galatians','可':'mark','啟':'revelation','太':'matthew','帖後':'2-thessalonians','弗':'ephesians','彼前':'1-peter','彼後':'2-peter','徒':'acts','提後':'2-timothy','林前':'1-corinthians','林後':'2-corinthians','約':'john','約壹':'1-john','羅':'romans','耶':'jeremiah','腓':'philippians','西':'colossians','詩':'psalms','賽':'isaiah','路':'luke','雅':'james'}
UA={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36'}
for b,c in json.load(open('other-chapters.json')):
    out=f'aieden/{SLUG[b]}-{c}.json'
    if os.path.exists(out) and os.path.getsize(out)>200: continue
    for attempt in range(4):
        try:
            d=urllib.request.urlopen(urllib.request.Request(f'https://www.ai-eden.com/api/bible/{SLUG[b]}/{c}?t=CUV',headers=UA),timeout=60).read()
            j=json.loads(d)
            if j.get('success') and j['data']['verses']: open(out,'wb').write(d); print('ok',b,c,flush=True); break
            print('bad',b,c,str(j)[:120],flush=True)
        except Exception as e: print('err',b,c,e,flush=True)
        time.sleep(30)
    time.sleep(11)
print('DONE')
