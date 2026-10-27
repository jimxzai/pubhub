import html,json,re,sys,time,urllib.parse,urllib.request
UA={'User-Agent':'pubhub-research/1.0 (bible study book build)'}
def get(title):
    url='https://en.wikisource.org/w/api.php?'+urllib.parse.urlencode({'action':'parse','page':title,'prop':'text','format':'json','redirects':1})
    d=json.load(urllib.request.urlopen(urllib.request.Request(url,headers=UA)))
    h=d['parse']['text']['*']
    h=re.sub(r'<br\s*/?>','\n',h); h=re.sub(r'</(p|div|tr|li)>','\n',h)
    t=html.unescape(re.sub(r'<[^>]+>','',h)); return re.sub(r'\n\s*\n+','\n\n',t).strip()
def search(q):
    url='https://en.wikisource.org/w/api.php?'+urllib.parse.urlencode({'action':'query','list':'search','srsearch':q,'format':'json','srlimit':8})
    return [r['title'] for r in json.load(urllib.request.urlopen(urllib.request.Request(url,headers=UA)))['query']['search']]
if __name__=='__main__':
    for arg in sys.argv[1:]:
        key,title=arg.split('=',1)
        if key=='?': print(title,search(title)); time.sleep(3); continue
        t=get(title); open(f'{key}.txt','w').write(f'SOURCE: Wikisource, "{title}"\n\n{t}\n'); print('==',key,len(t)); time.sleep(3)
