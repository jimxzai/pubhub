#!/usr/bin/env python3
"""Create reflowable digital proofs, preserving print Scripture macros."""
import argparse
import json
import subprocess
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]

def pandoc(text, *args):
    return subprocess.check_output(['pandoc', *args], input=text, text=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'digital')
    args = parser.parse_args()
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    combined = (REPO / 'output/gospel-of-john-consolidated.md').read_text()
    template = (REPO / 'output/gospel-of-john-generated.latex').read_text()
    body = json.loads(pandoc(combined, '-f', 'markdown-superscript-subscript', '-t', 'json', '--lua-filter', str(ROOT / 'digital.lua')))
    appendix = template.split('%% BACK MATTER — APPENDICES', 1)[1].split('%% BACK COVER PAGE', 1)[0]
    appendix = '\\newcommand{\\jesus}[1]{#1}\n' + appendix
    extra = json.loads(pandoc(appendix, '-f', 'latex', '-t', 'json'))
    headings = [b for b in extra['blocks'] if b['t'] == 'Header' and b['c'][0] == 1]
    if len(headings) != 9:
        raise ValueError(f'Expected nine appendix headings, found {len(headings)}')
    # Copyright metadata in the print template must become visible digital content.
    copyright = body['meta'].get('copyright', {}).get('c', [])
    body['blocks'] = copyright + body['blocks'] + extra['blocks']
    pdf = REPO / 'output/gospel-of-john-consolidated.pdf'
    reader = PdfReader(pdf)
    map_page = next(i + 1 for i, page in enumerate(reader.pages) if 'KeyLocationsintheGospelofJohn' in ''.join(page.extract_text().split()))
    subprocess.run(['pdftoppm','-f',str(map_page),'-l',str(map_page),'-singlefile','-scale-to','1800','-png',str(pdf),str(output / 'john-map')],check=True)
    map_blocks = json.loads(pandoc('## 約翰福音重要地點\n\n![約翰福音重要地點示意圖；地名及相關經文另見下段文字。](john-map.png)\n\n地點索引：迦拿（2:1–11）、迦百農（4:46–54）、伯賽大、拿撒勒、敘加（4:5）、約旦河外的伯大尼（1:28）、耶路撒冷附近的伯大尼（11:1）、耶路撒冷及伯利恆。圖中的水域為地中海、加利利海、約旦河與死海。\n', '-f','markdown','-t','json'))['blocks']
    body['blocks'] = map_blocks + body['blocks']
    body['meta']['lang'] = {'t':'MetaString','c':'zh-TW'}
    body['meta']['subtitle'] = {'t':'MetaString','c':'Gospel of John Deep Study — Edition 4.0'}
    serialized = json.dumps(body, ensure_ascii=False)
    if 'RawInline' in serialized or 'RawBlock' in serialized:
        raise ValueError('Unconverted raw markup remains; inspect before export')
    for fmt, suffix in [('epub3','epub'), ('html5','html')]:
        subprocess.run(['pandoc','-f','json','-t',fmt,'--standalone','--toc','--toc-depth=2',
                        '--resource-path',str(output), '--css',str(ROOT / 'digital.css'),
                        '--metadata', 'title=約翰福音研讀——生命之道',
                        '-o',str(output / ('gospel-of-john-consolidated.' + suffix))] + (['--embed-resources'] if fmt == 'html5' else []),input=serialized,text=True,check=True)
    print('Created EPUB 3 and HTML reading proofs with all nine appendices. Reader/device accessibility QA is still required.')

if __name__ == '__main__':
    main()
