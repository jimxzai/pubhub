#!/usr/bin/env python3
"""Unify single-character 和合本 spelling variants in a book's CUV scripture
blocks to ai-eden's cuv.json (the project's standard source).

SAFE BY CONSTRUCTION: a verse is touched only when its ENTIRE difference from
cuv.json (ignoring punctuation) consists of single-character replacements from
the allowed pair set below. Verses that differ in any other way (footnotes,
inserted/deleted words, wrong chapter mapping) are left alone and reported.

Usage: unify-cuv-variants.py <book-dir> [--write]
"""
import difflib, glob, json, re, sys
from pathlib import Path

CUV = Path('/Users/jimxiao/dev/ai-eden/data/cuv.json')
BK = {'太': 'matthew', '可': 'mark', '路': 'luke', '約': 'john', '徒': 'acts', '啟': 'revelation'}
BN = {'馬太福音': 'matthew', '馬可福音': 'mark', '路加福音': 'luke', '約翰福音': 'john',
      '使徒行傳': 'acts', '啟示錄': 'revelation'}
PUNCT = '，。；：、！？「」『』（）〔〕—…·　 ,.;:!?"\'()'
ALLOWED = {('啊', '阿'), ('吧', '罷'), ('嗎', '麼'), ('地', '的'), ('的', '地'), ('哪', '那'), ('它', '他'),
           ('牠', '他'), ('癒', '愈'), ('覆', '復'), ('姊', '姐'), ('做', '作'), ('作', '做'), ('資', '貲'),
           ('預', '豫'), ('裡', '裏'), ('裏', '裡'), ('她', '他'), ('麼', '嗎'), ('罷', '吧')}
MACRO = re.compile(r'\\jesus\{|\\textbf\{|\\textit\{|\}')


def stripped_with_map(seg):
    """Return (chars, positions) of non-punctuation, non-macro characters."""
    skip = set()
    for m in MACRO.finditer(seg):
        skip.update(range(m.start(), m.end()))
    chars, pos = [], []
    for i, c in enumerate(seg):
        if i in skip or c in PUNCT:
            continue
        chars.append(c); pos.append(i)
    return ''.join(chars), pos


def main():
    book = Path(sys.argv[1]); write = '--write' in sys.argv
    cuv = json.loads(CUV.read_text(encoding='utf-8'))
    touched = left = 0
    for p in sorted(glob.glob(str(book / '[0-3][0-9]-*.md'))):
        text = Path(p).read_text(encoding='utf-8')
        a = text.find('### 中文'); b = text.find('### English')
        if a < 0 or b < 0:
            continue
        lines = text[a:b].split('\n'); cur = None; changed = False
        for li, line in enumerate(lines):
            mm = re.search(r'(馬太福音|馬可福音|路加福音|約翰福音|使徒行傳|啟示錄|太|可|路|約|徒|啟)\s*(\d+)', line)
            if mm and (line.startswith('**') or line.startswith('#')):
                cur = ((BN.get(mm.group(1)) or BK.get(mm.group(1))), int(mm.group(2)))
            if not line.startswith('>') or cur is None:
                continue
            key = f'{cur[0]}-{cur[1]}'
            ch = cuv.get(key)
            if not isinstance(ch, dict):
                continue
            parts = re.split(r'(\^\d+\^)', line)
            for i in range(1, len(parts), 2):
                v = parts[i].strip('^'); seg = parts[i + 1]
                e = ch.get(v)
                if not e:
                    continue
                e = e.replace('裡', '裏')
                s1, pos = stripped_with_map(seg)
                s2 = ''.join(c for c in e if c not in PUNCT)
                if s1 == s2:
                    continue
                ops = [o for o in difflib.SequenceMatcher(None, s1, s2).get_opcodes() if o[0] != 'equal']
                if ops and all(o[0] == 'replace' and o[2] - o[1] == 1 and o[4] - o[3] == 1
                               and (s1[o[1]], s2[o[3]]) in ALLOWED for o in ops):
                    chars = list(seg)
                    for o in ops:
                        chars[pos[o[1]]] = s2[o[3]]
                    parts[i + 1] = ''.join(chars); touched += 1; changed = True
                else:
                    left += 1
            lines[li] = ''.join(parts)
        if changed and write:
            Path(p).write_text(text[:a] + '\n'.join(lines) + text[b:], encoding='utf-8')
    print(f'verses unified: {touched}; verses differing in other ways (left alone): {left}')


if __name__ == '__main__':
    main()
