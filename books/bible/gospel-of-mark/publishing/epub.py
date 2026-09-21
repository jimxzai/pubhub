#!/usr/bin/env python3
"""Preserve manuscript text and template appendices; promote only after checks."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import tempfile
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
import posixpath
from urllib.parse import unquote

BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[2]

def group(text, pos):
    while pos < len(text) and text[pos].isspace(): pos += 1
    if pos == len(text) or text[pos] != '{':
        raise ValueError('Expected TeX argument: ' + text[pos:pos+60])
    start, depth = pos + 1, 1
    pos += 1
    while pos < len(text):
        if text[pos] == '\\':
            pos += 2; continue
        depth += (text[pos] == '{') - (text[pos] == '}')
        if not depth: return text[start:pos], pos + 1
        pos += 1
    raise ValueError('Unclosed TeX argument')

def convert(text, counts=None):
    counts = counts if counts is not None else Counter()
    out, pos = [], 0
    while pos < len(text):
        m = re.match(r'\\([A-Za-z]+)', text[pos:])
        if not m:
            out.append(text[pos]); pos += 1; continue
        name = m[1]; pos += len(m[0]); counts[name] += 1
        if name in ('newpage', 'clearpage', 'large'):
            out.append('\n' if name != 'large' else ''); continue
        arg, pos = group(text, pos)
        if name in ('begin', 'end'):
            if arg != 'center': raise ValueError('Unsupported environment: ' + arg)
            continue
        if name == 'vspace': continue
        if name == 'textcolor':
            arg, pos = group(text, pos)
            out.append(convert(arg, counts)); continue
        if name not in ('jesus', 'textsuperscript', 'textbf', 'textit'):
            raise ValueError('Unsupported macro: ' + name)
        inner = convert(arg, counts)
        tag = {'jesus': 'span', 'textsuperscript': 'sup', 'textbf': 'strong', 'textit': 'em'}[name]
        attr = ' class="jesus"' if name == 'jesus' else ''
        out.append('<' + tag + attr + '>' + inner + '</' + tag + '>')
    return ''.join(out)

def pandoc(text, source, target):
    return subprocess.run(['pandoc', '-f', source, '-t', target], input=text,
                          text=True, check=True, capture_output=True).stdout

def appendices(template):
    text = '\\chapter*{附錄三：' + template.split('\\chapter*{附錄三：', 1)[1].split('%% BACK COVER PAGE', 1)[0]
    text = re.sub(r'(?m)^%.*$', '', text)
    text = re.sub(r'\\addcontentsline\{toc\}\{chapter\}\{[^\n]*\}', '', text)
    text = text.replace('\\markboth{}{}', '')
    while '\\fcolorbox' in text:
        start = text.index('\\fcolorbox'); pos = start + len('\\fcolorbox')
        _, pos = group(text, pos); _, pos = group(text, pos)
        content, pos = group(text, pos)
        text = text[:start] + content + text[pos:]
    text = re.sub(r'\\begin\{minipage\}(?:\[[^]]*\])?\{[^}]*\}', '', text)
    text = text.replace('\\end{minipage}', '')
    text = re.sub(r'\\renewcommand\{\\arraystretch\}\{[^}]*\}', '', text)
    text = re.sub(r'\\(?:vspace|hspace)\*?\{[^}]*\}', '', text)
    return re.sub(r'\\(?:small|footnotesize|scriptsize|noindent|centering|pagebreak|cleardoublepage)\b', '', text)

def normalized(text):
    return ''.join(unicodedata.normalize('NFKC', text).split())

def validate(epub, expected_html, counts):
    with zipfile.ZipFile(epub) as z:
        if z.namelist()[0] != 'mimetype' or z.read('mimetype') != b'application/epub+zip':
            raise ValueError('Invalid EPUB container')
        opf = ET.fromstring(z.read('EPUB/content.opf'))
        if not any(e.get('property') == 'schema:accessibilitySummary' and e.text for e in opf.iter()):
            raise ValueError('Missing accessibility summary')
        docs = [ET.fromstring(z.read(n)) for n in z.namelist() if n.endswith('.xhtml') and '/text/' in n]
        actual = ''.join(''.join(d.itertext()) for d in docs)
        actual_normal = normalized(actual)
        source = ET.fromstring('<root>' + expected_html + '</root>')
        checked = 0
        for el in source.iter():
            if el.tag in ('p', 'h1', 'h2', 'h3', 'h4', 'td', 'th', 'li'):
                value = normalized(''.join(el.itertext()))
                if value and value not in actual_normal:
                    raise ValueError('EPUB lost text: ' + value[:150])
                checked += 1
        red = [el for d in docs for el in d.iter() if 'jesus' in el.get('class', '').split()]
        supers = [el for d in docs for el in d.iter() if el.tag.endswith('}sup')]
        if len(red) != counts['jesus'] or len(supers) < counts['textsuperscript']:
            raise ValueError(f'Red-letter / verse-marker count mismatch: {len(red)}/{counts["jesus"]}, {len(supers)}/{counts["textsuperscript"]}')
        for number in ('三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二'):
            if '附錄' + number + '：' not in actual: raise ValueError('Missing appendix: ' + number)
        if re.search(r'\\(?:jesus|textsuperscript|textcolor|textbf)\b', actual):
            raise ValueError('Raw TeX leaked into EPUB')
        names = set(z.namelist())
        for name in names:
            if not name.endswith('.xhtml'): continue
            for el in ET.fromstring(z.read(name)).iter():
                href = el.get('href', '')
                if not href or re.match(r'[a-zA-Z][\w+.-]*:', href): continue
                file, _, fragment = unquote(href).partition('#')
                target = posixpath.normpath(posixpath.join(posixpath.dirname(name), file)) if file else name
                if target not in names: raise ValueError('Missing link target: ' + href)
                if fragment and fragment not in {e.get('id') for e in ET.fromstring(z.read(target)).iter()}:
                    raise ValueError('Missing link fragment: ' + href)
        return {'text_blocks_checked': checked, 'red_letter_spans': len(red), 'superscripts': len(supers),
                'appendices': 12, 'internal_links': 'PASS', 'accessibility_certification': 'NOT CLAIMED'}

def build(input_md, template, output, cover=None):
    counts = Counter()
    ast = json.loads(pandoc(convert(input_md.read_text(), counts), 'markdown-superscript-subscript', 'json'))
    copyright_meta = ast['meta'].get('copyright', {})
    if copyright_meta.get('t') == 'MetaBlocks': ast['blocks'] = copyright_meta['c'] + ast['blocks']
    appendix_ast = json.loads(pandoc(appendices(template.read_text()), 'latex', 'json'))
    def prefix_appendix_ids(node):
        if isinstance(node, dict):
            if node.get('t') == 'Header': node['c'][1][0] = 'appendix-' + node['c'][1][0]
            for value in node.values(): prefix_appendix_ids(value)
        elif isinstance(node, list):
            for value in node: prefix_appendix_ids(value)
    prefix_appendix_ids(appendix_ast['blocks'])
    ast['blocks'].extend(appendix_ast['blocks'])
    ast['meta']['date'] = {'t': 'MetaString', 'c': '2026-08'}
    summary = ET.parse(BOOK / 'publishing/epub-metadata.xml').getroot()[0].text
    ast['meta']['accessibilitySummary'] = {'t': 'MetaString', 'c': summary}
    # Mark predominantly English paragraphs (including all NASB scripture blocks).
    def language_blocks(node):
        if isinstance(node, dict):
            if node.get('t') in ('Para', 'Plain'):
                words = []
                def collect(value):
                    if isinstance(value, dict):
                        if value.get('t') == 'Str': words.append(value['c'])
                        else:
                            for v in value.values(): collect(v)
                    elif isinstance(value, list):
                        for v in value: collect(v)
                collect(node['c'])
                text = ''.join(words)
                if re.search(r'[A-Za-z]{3}', text) and not re.search(r'[\u3400-\u9fff]', text):
                    node['c'] = [{'t': 'Span', 'c': [['', [], [['lang', 'en']]], node['c']]}]
                return
            for value in node.values(): language_blocks(value)
        elif isinstance(node, list):
            for value in node: language_blocks(value)
    language_blocks(ast['blocks'])
    def no_raw(node):
        if isinstance(node, dict):
            if node.get('t') in ('RawBlock', 'RawInline') and node['c'][0] in ('tex', 'latex'):
                raise ValueError('Unconverted appendix TeX: ' + str(node['c']))
            for v in node.values(): no_raw(v)
        elif isinstance(node, list):
            for v in node: no_raw(v)
    no_raw(ast)
    expected = pandoc(json.dumps(ast), 'json', 'html5')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.mark-epub-', dir=output.parent) as tmp:
        staged = Path(tmp) / output.name
        cover_args = ['--epub-cover-image=' + str(cover)] if cover else []
        subprocess.run(['pandoc', '-f', 'json', '-t', 'epub3', '-o', str(staged), '--toc', '--toc-depth=2',
                        '--metadata=lang:zh-TW',
                        '--css=' + str(BOOK / 'publishing/epub.css')] + cover_args,
                       input=json.dumps(ast), text=True, check=True)
        report = validate(staged, expected, counts)
        staged.replace(output)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=Path, default=ROOT / 'output/gospel-of-mark-consolidated.md')
    parser.add_argument('--template', type=Path, default=ROOT / 'templates/pdf/gospel-of-mark.latex')
    parser.add_argument('--output', type=Path, default=ROOT / 'output/gospel-of-mark-consolidated-accessible.epub')
    args = parser.parse_args()
    build(args.input, args.template, args.output)
