"""Audit the assigned PDF, not a different manuscript build.

Recovered reference files are local research evidence, not clearance records.
Alphanumeric matches are deliberately NOT called verbatim verification.
"""
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import unicodedata
import fitz

ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT.parents[2]/'output/romans-consolidated.pdf'
REF = ROOT/'sources/reference'
CHAPTERS = [52,68,83,100,115,132,147,162,181,198,212,229,244,261,277,294,310]
FRESH = {
    'augustine-spirit-letter.html':('Augustine','https://www.newadvent.org/fathers/1502.htm'),
    'augustine-pelagians-1.html':('Augustine','https://www.newadvent.org/fathers/15091.htm'),
    'augustine-pelagians-4.html':('Augustine','https://www.newadvent.org/fathers/15094.htm'),
    'augustine-grace.html':('Augustine','https://www.newadvent.org/fathers/1510.htm'),
    'augustine-predestination.html':('Augustine','https://www.newadvent.org/fathers/15121.htm'),
    'augustine-perseverance.html':('Augustine','https://www.newadvent.org/fathers/15122.htm'),
    'calvin-institutes.html':('Calvin','https://www.ccel.org/c/calvin/institutes/cache/institutes.html3'),
    'luther-romans.html':('Luther','https://www.ccel.org/l/luther/romans/pref_romans.html'),
}

class Plain(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style'): self.skip+=1
    def handle_endtag(self,tag):
        if tag in ('script','style'): self.skip=max(0,self.skip-1)
    def handle_data(self,data):
        if not self.skip: self.parts.append(data)

def plain(s):
    p=Plain(); p.feed(s); return ' '.join(p.parts)

def fold(s):
    s=unicodedata.normalize('NFKC',html.unescape(s)).replace('裏','裡').replace('衞','衛')
    return ''.join(c.lower() for c in s if c.isalnum())

def body(page):
    return '\n'.join(b[4] for b in page.get_text('blocks') if b[1]>=43 and b[3]<=680)

def reference(chapter,lang):
    if lang=='zh':
        data=json.loads((REF/f'cuv{chapter}.json').read_text())
        assert data['status']=='success' and data['version']=='unv'
        return {r['sec']:r['bible_text'] for r in data['record']}
    raw=(REF/f'nasb{chapter}.html').read_text()
    assert f'Romans {chapter} NASB 1995' in raw
    raw=raw.split('<div class="chap">',1)[1].split('NASB 1995 Copyright',1)[0]
    raw=re.sub(r'<b><i>.*?</i></b>','',raw,flags=re.S)
    return {int(n):plain(t).strip() for n,t in re.findall(r'<span class="reftext">.*?<b>(\d+)</b>.*?</span>(.*?)(?=<span class="reftext">|\Z)',raw,re.S)}

def source_records():
    records=[]
    for path in sorted(REF.iterdir()):
        if path.suffix not in ('.html','.txt'): continue
        name=path.name
        if name.startswith('nasb'): continue
        raw=path.read_text()
        if name in FRESH:
            author,url=FRESH[name]
        elif name.startswith('chrysostom'):
            url='https://www.newadvent.org/fathers/2102'+path.stem[-2:]+'.htm'
            author='Chrysostom'
        elif name.startswith('gty'):
            url='https://www.gty.org/library/sermons-library/'+path.stem[4:]+'/'
            author='MacArthur'
        elif name=='morgan.txt':
            url='https://www.classicchristianlibrary.com/library/morgan_g_campbell/Morgan-Romans.pdf'
            author='Morgan'
        elif name=='calvin-full.txt':
            url='https://ccel.org/ccel/c/calvin/calcom38/cache/calcom38.txt'
            author='Calvin'
        else: continue
        records.append(dict(file=name,url=url,author=author,acquisition='retrieved 2026-09-21' if name in FRESH else 'recovered 2026-09-21; retrieval date unknown',sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                            folded=fold(plain(raw) if path.suffix=='.html' else raw)))
    return records

def audit(path=PDF):
    doc=fitz.open(path)
    fonts={f[0]:f[3] for page in doc for f in page.get_fonts()}
    production=dict(fonts=len(fonts),unembedded=[name for xref,name in fonts.items() if not doc.extract_font(xref)[3]],
                    bookmarks=len(doc.get_toc()),language=doc.xref_get_key(doc.pdf_catalog(),'Lang')[1])
    sources=source_records()
    quotation_rows=[]
    # Page mapping excludes running furniture, includes cross-page quotations.
    whole=''; ranges=[]
    for n in range(20,310):
        start=len(whole); whole+=body(doc[n])+'\n'; ranges.append((start,len(whole),n+1))
    for match in re.finditer(r'“([A-Za-z][^”]{20,2200})”',whole):
        quote=match[1]
        prior=whole[:match.start()]
        # Scriptural speech is already checked verse-by-verse below; do not
        # misreport it as an unresolved commentator quotation.
        if prior.rfind('English — NASB') > prior.rfind('背景(Context)'): continue
        if len(re.findall(r'[A-Za-z]+',quote))<6: continue
        if re.search(r'[\u4e00-\u9fff]',quote): continue
        found=[s for s in sources if fold(quote) in s['folded']]
        pages=[p for a,b,p in ranges if a<match.end() and b>match.start()]
        quotation_rows.append(dict(pages=pages,opening=' '.join(quote.split())[:100],
            quote_sha256=hashlib.sha256(quote.encode()).hexdigest(),
            status='normalized-wording-match' if found else 'unresolved',
            source_candidates=[{k:v for k,v in s.items() if k!='folded'} for s in found],
            attribution_context=whole[match.end():match.end()+300]))
    scripture_rows=[]
    for ch in range(1,17):
        combined='\n'.join(body(doc[n]) for n in range(CHAPTERS[ch-1]-1,CHAPTERS[ch]-1))
        blocks=combined.split('中文— 和合本(CUV)',1)[1].split('English — NASB',1)
        zh=blocks[0]; zh=zh[re.search(r'(?<!\d)1(?=[\u4e00-\u9fff])',zh).start():]
        en=blocks[1].split('背景(Context)',1)[0].split('經文小記',1)[0]
        for lang,block in [('zh',zh),('en',en)]:
            verses={int(m[1]):m[2] for m in re.finditer(r'(?<!\d)(\d{1,2})(?!\d)(.*?)(?=(?<!\d)\d{1,2}(?!\d)|\Z)',block,re.S)}
            ref=reference(ch,lang)
            rows=[]
            for v in sorted(verses.keys()|ref.keys()):
                actual=verses.get(v,''); expected=ref.get(v,'')
                rows.append(dict(verse=v,match=bool(actual and expected) and fold(actual)==fold(expected),
                    actual_sha256=hashlib.sha256(fold(actual).encode()).hexdigest(),
                    reference_sha256=hashlib.sha256(fold(expected).encode()).hexdigest(),
                    **({'actual':actual.strip(),'reference':expected} if fold(actual)!=fold(expected) else {})))
            source=REF/(f'cuv{ch}.json' if lang=='zh' else f'nasb{ch}.html')
            scripture_rows.append(dict(chapter=ch,language=lang,source_file=source.name,
                source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),verses=rows))
    result=dict(pdf=str(path),sha256=hashlib.sha256(Path(path).read_bytes()).hexdigest(),pages=len(doc),
        method='Actual PDF extraction; NFKC, case, punctuation and whitespace ignored; 裏/裡 and 衞/衛 folded. Not verbatim, context, translation or rights certification. Quote source candidates require attribution review. Scripture mismatches include possible extraction artifacts.',
        provenance='Reference caches recovered from /tmp/romans-edit.x22HaE on 2026-09-21; original retrieval metadata was not preserved. Source URLs reconstructed from prior research code and file metadata. Do not treat recovery date as retrieval date.',
        scripture=scripture_rows,quotations=quotation_rows,production=production)
    return result

def main():
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--pdf',type=Path,default=PDF)
    args=parser.parse_args()
    result=audit(args.pdf)
    out=ROOT/'sources/audits/actual-pdf-evidence.json'
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    catalog=[{k:v for k,v in source.items() if k!='folded'} for source in source_records()]
    (ROOT/'sources/audits/reference-catalog.json').write_text(json.dumps(catalog,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(dict(scripture_verses=sum(len(r['verses']) for r in result['scripture']),
        scripture_matches=sum(v['match'] for r in result['scripture'] for v in r['verses']),
        scripture_differences=[f"{r['chapter']}:{v['verse']} {r['language']}" for r in result['scripture'] for v in r['verses'] if not v['match']],
        quote_candidates=len(result['quotations']),wording_matches=sum(r['status']=='normalized-wording-match' for r in result['quotations'])),indent=2))

if __name__=='__main__': main()
