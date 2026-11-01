#!/usr/bin/env python3
"""Generate the 經文 blocks (CUV + NASB 1995) for each Malachi unit, and check chapter files against them.

  python3 sources/gen_scripture_blocks.py            # write sources/scripture/blocks/NN.md
  python3 sources/gen_scripture_blocks.py --check    # exit 1 if a chapter's 經文 block differs from the generated one

Inputs (built by gen_scripture.py): scripture/cuv-malachi.txt (ai-eden CUV, 裡→裏) and scripture/nasb1995-malachi.txt (biblehub NASB 1995).
Verse markers are English (和合本/NASB) numbering: ^v^ ; a unit never crosses a chapter boundary except 2:17|3:1-5 (then ^c:v^ is used).
NASB: the opening quotation mark that NASB re-prints at every verse of continuing speech is dropped inside an open quotation
(layout, not text), as in the Jonah and Obadiah volumes.
"""
import os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.dirname(D)
UNITS = {  # chapter-file prefix: [(chapter, v_from, v_to), ...]
    '01': [(1, 1, 5)],
    '02': [(1, 6, 14)],
    '03': [(2, 1, 9)],
    '04': [(2, 10, 16)],
    '05': [(2, 17, 17), (3, 1, 5)],
    '06': [(3, 6, 12)],
    '07': [(3, 13, 18)],
    '08': [(4, 1, 6)],
}


def load(name):
    out = {}
    for line in open(f'{D}/scripture/{name}', encoding='utf-8'):
        ref, txt = line.rstrip('\n').split('\t', 1)
        c, v = ref.split(':')
        out[(int(c), int(v))] = txt
    return out


CUV, NASB = load('cuv-malachi.txt'), load('nasb1995-malachi.txt')


def join_en(items):
    out, depth = [], 0
    for mk, t in items:
        if depth % 2 == 1 and t.startswith('"'):
            t = t[1:].lstrip()
        depth += t.count('"')
        out.append(mk + t)
    return ' '.join(out)


def block(spans):
    multi = len({c for c, _, _ in spans}) > 1
    zh, en = [], []
    for c, a, b in spans:
        for v in range(a, b + 1):
            mk = f'^{c}:{v}^' if multi else f'^{v}^'
            zh.append(mk + CUV[(c, v)])
            en.append((mk, NASB[(c, v)]))
    return ('### 中文 — 和合本 (CUV)\n\n> ' + ''.join(zh) + '\n\n### English — NASB 1995\n\n> ' + join_en(en) + '\n')


def chapter_block(path):
    t = open(path, encoding='utf-8').read()
    m = re.search(r'(### 中文 — 和合本 \(CUV\)\n.*?### English — NASB 1995\n.*?)(?=\n\n---|\n## )', t, re.S)
    return m.group(1).strip() + '\n' if m else None


if __name__ == '__main__':
    os.makedirs(f'{D}/scripture/blocks', exist_ok=True)
    bad = 0
    for u, spans in UNITS.items():
        b = block(spans)
        open(f'{D}/scripture/blocks/{u}.md', 'w', encoding='utf-8').write(b)
        if '--check' in sys.argv:
            files = [f for f in os.listdir(BOOK) if f.startswith(u + '-') and f.endswith('.md')]
            if not files:
                print(f'{u}: (no chapter file yet)'); continue
            got = chapter_block(f'{BOOK}/{files[0]}')
            if got is None:
                print(f'{u}: {files[0]}: no 經文 block found'); bad += 1
            elif got.strip() != b.strip():
                print(f'{u}: {files[0]}: 經文 block DIFFERS from generated sources/scripture/blocks/{u}.md'); bad += 1
            else:
                print(f'{u}: {files[0]}: ok')
        else:
            print(u, 'ok')
    sys.exit(1 if bad else 0)
