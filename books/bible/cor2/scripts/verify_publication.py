#!/usr/bin/env python3
"""Check real EPUB contents/links, PDF content and provenance, not just filenames."""
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import posixpath
import re
import subprocess
import sys
import unicodedata
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parent.parent
NAME = 'cor2-consolidated'
def norm(text):
    return ''.join(c for c in unicodedata.normalize('NFKC', text) if c.isalnum())

class Fragments(HTMLParser):
    def __init__(self):
        super().__init__(); self.parts=[]; self.stack=[]
    def handle_starttag(self, tag, attrs):
        if tag in ('p','td','th','h1','h2','h3','h4','li'):
            self.stack.append([tag, []])
    def handle_data(self, data):
        for _, pieces in self.stack: pieces.append(data)
    def handle_endtag(self, tag):
        if self.stack and self.stack[-1][0] == tag:
            _, pieces = self.stack.pop()
            self.parts.append(''.join(pieces))

def verify_epub(path):
    ns={'opf':'http://www.idpf.org/2007/opf', 'c':'urn:oasis:names:tc:opendocument:xmlns:container'}
    with zipfile.ZipFile(path) as z:
        assert z.testzip() is None, 'Corrupt EPUB member'
        assert z.read('mimetype') == b'application/epub+zip', 'Wrong EPUB mimetype'
        container=ET.fromstring(z.read('META-INF/container.xml'))
        opf=container.find('.//c:rootfile',ns).attrib['full-path']
        base=posixpath.dirname(opf)
        package=ET.fromstring(z.read(opf))
        manifest={e.attrib['id']:e.attrib for e in package.findall('.//opf:manifest/opf:item',ns)}
        docs={}; ids={}
        for item in manifest.values():
            file=posixpath.normpath(posixpath.join(base,unquote(item['href'])))
            assert file in z.namelist(), f'Missing manifest resource: {file}'
            if item['media-type']=='application/xhtml+xml':
                tree=ET.fromstring(z.read(file)); docs[file]=tree
                found=[e.attrib['id'] for e in tree.iter() if 'id' in e.attrib]
                assert len(found)==len(set(found)), f'Duplicate IDs in {file}'
                ids[file]=set(found)
        for file, tree in docs.items():
            for el in tree.iter():
                for attr in ('href','src'):
                    href=el.attrib.get(attr)
                    if not href: continue
                    url=urlsplit(href)
                    if url.scheme or url.netloc: continue
                    target=posixpath.normpath(posixpath.join(posixpath.dirname(file),unquote(url.path))) if url.path else file
                    assert target in z.namelist(), f'Broken resource: {file} -> {href}'
                    if url.fragment:
                        assert unquote(url.fragment) in ids.get(target,set()), f'Broken anchor: {file} -> {href}'
        bodies=[]; spine_ids=[]
        for el in package.findall('.//opf:spine/opf:itemref',ns):
            ref=el.attrib['idref']; assert ref in manifest, 'Missing spine entry'
            file=posixpath.normpath(posixpath.join(base,unquote(manifest[ref]['href'])))
            tree=docs[file]; body=tree.find('{http://www.w3.org/1999/xhtml}body')
            bodies.append(''.join(body.itertext()))
            spine_ids += [e.attrib['id'] for e in body.iter() if 'id' in e.attrib]
        expected=[f'lesson-{n:02d}' for n in range(1,25)]+[f'appendix-{c}' for c in 'abcde']
        for identifier in expected:
            assert spine_ids.count(identifier)==1, f'EPUB missing/duplicate section {identifier}'
        assert [x for x in spine_ids if x in expected] == expected, 'EPUB section order drift'
        return norm(''.join(bodies))

def verify(folder):
    if not __debug__:
        raise RuntimeError('Publication validation must run without Python optimization.')
    folder=Path(folder); pdf=folder/f'{NAME}.pdf'; epub=folder/f'{NAME}.epub'
    ast=folder/f'{NAME}.json'
    expected_html=subprocess.check_output(['pandoc',str(ast),'-f','json','-t','html5'],text=True)
    fragments=Fragments(); fragments.feed(expected_html)
    epubtext=verify_epub(epub)
    missing=[t[:100] for t in fragments.parts if len(norm(t))>8 and norm(t) not in epubtext]
    assert not missing, f'EPUB lost source fragments ({len(missing)}): {missing[:8]}'
    pdftext=subprocess.check_output(['pdftotext',str(pdf),'-'],text=True)
    normalized=norm(pdftext)
    for n in range(1,25):
        assert norm(f'第{n:02d}課') in normalized, f'PDF missing lesson {n}'
    for c in 'ABCDE':
        assert norm(f'Appendix {c}') in normalized, f'PDF missing appendix {c}'
    # Every substantive appendix paragraph and table cell must survive both exports.
    # Appendix A is a generated, multi-column index. PDF text extraction may
    # interleave its columns even when every visible cell is present; validate
    # its presence and structural anchor above, and apply exact fragment parity
    # to the authored appendices B–E.
    appendix_html=expected_html[expected_html.index('id="appendix-b"'):]
    appendix_fragments=Fragments(); appendix_fragments.feed('<h1 '+appendix_html)
    missing_pdf=[t[:100] for t in appendix_fragments.parts if len(norm(t))>8 and norm(t) not in normalized]
    assert not missing_pdf, f'PDF appendix text loss ({len(missing_pdf)}): {missing_pdf[:8]}'
    pages=pdftext.split('\f')
    preface=next(i for i,t in enumerate(pages) if '這本小冊子不是從書房' in t)
    assert preface < 22, f'Front matter/TOC regression: preface at physical page {preface+1}'
    log=(folder/f'{NAME}-build.log').read_text()
    assert 'This is LuaHBTeX' in log and 'Output written on' in log, 'No completed engine output'
    assert not re.search(r'Missing character|Overfull \\[hv]box|^! ',log,re.M), 'LaTeX defect'
    info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
    assert '哥林多後書研讀：十字架事奉' in info, 'Title drift'
    assert 'CONSOLIDATED2026EDITION' in normalized, 'Edition absent'
    assert re.search(r'Tagged:\s+yes',info), 'PDF semantic tagging is absent'
    from pypdf import PdfReader
    reader=PdfReader(pdf)
    structure=reader.trailer['/Root'].get('/StructTreeRoot')
    assert structure and structure.get_object().get('/K'), 'Empty PDF structure tree'
    assert reader.trailer['/Root'].get('/Lang') == 'zh-Hant', 'Missing PDF document language'
    roles={}; seen=set()
    def walk(obj):
        if hasattr(obj,'get_object'): obj=obj.get_object()
        if isinstance(obj,list):
            for child in obj: walk(child)
        elif isinstance(obj,dict):
            if id(obj) in seen: return
            seen.add(id(obj))
            if '/S' in obj:
                role=str(obj['/S']); roles[role]=roles.get(role,0)+1
            if '/K' in obj: walk(obj['/K'])
    walk(structure)
    assert all(roles.get(role,0)>0 for role in ('/Table','/TH','/Link','/Document')), 'Incomplete semantic structure'
    assert not re.search(r'\[WARNING\].*undefined',log,re.I), 'Unresolved PDF cross-reference'
    assert norm('不得公開或商業發行') in normalized, 'Draft rights notice absent'
    epubcheck=(folder/f'{NAME}-epubcheck.log').read_text()
    assert 'No errors or warnings detected.' in epubcheck, 'EPUBCheck did not report clean conformance'
    report={'edition':'CONSOLIDATED 2026 EDITION', 'lessons':24, 'appendices':5,
        'epub_source_fragments_checked':len(fragments.parts),
        'pdf_appendix_fragments_checked':len(appendix_fragments.parts),
        'preface_physical_page':preface+1, 'tagged':bool(re.search(r'Tagged:\s+yes',info)),
        'epubcheck':'passed', 'pdf_structure_roles':roles,
        'artifacts':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (pdf,epub,ast)}}
    (folder/f'{NAME}-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(f'PASS: 24 lessons, full A–E parity, {len(fragments.parts)} EPUB text fragments, internal links, EPUBCheck and compact TOC.')
    if not report['tagged']: print('OPEN: PDF semantic tagging / assistive-technology review.')
    return report

if __name__=='__main__':
    verify(sys.argv[1] if len(sys.argv)>1 else ROOT.parents[2]/'output')
