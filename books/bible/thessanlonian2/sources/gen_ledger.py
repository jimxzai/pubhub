#!/usr/bin/env python3
"""Write the per-commentator citation tables into 99-appendix-references.md.

Reads every chapter's ## 歷代注疏 section, collects each `> "..."` quote with
its attribution line, and writes one H2 per commentator between the
<!-- ledger:start --> / <!-- ledger:end --> markers. Each H2 contains the
commentator's Chinese name so scripts/check-citation-ledger.py can isolate
it, and lists chapters as separate 第N章 tokens (the parser's verbatim form).

usage: python3 sources/gen_ledger.py [--check]
"""
import glob, os, re, sys

BOOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(BOOK, '99-appendix-references.md')
START, END = '<!-- ledger:start -->', '<!-- ledger:end -->'

PEOPLE = [  # (heading keyword, H2 title, source description, verification command)
    ('屈梭多模', '一、屈梭多模 (John Chrysostom)',
     '*Homilies on Second Thessalonians*，NPNF¹ 第13冊（Philip Schaff 編，公有領域），CCEL 全文 `ccel.org/ccel/s/schaff/npnf113/cache/npnf113.txt`，本地切出 `sources/commentary/chrysostom-2thess.txt`。',
     'scripts/verify-citations.py --source sources/commentary/chrysostom-2thess.txt --heading 屈梭多模'),
    ('奧古斯丁', '二、奧古斯丁 (Augustine)',
     '*The City of God*，卷二十第19章（Marcus Dods 英譯，NPNF¹ 第2冊，公有領域），CCEL `ccel.org/ccel/s/schaff/npnf102/cache/npnf102.txt`，本地切出 `sources/commentary/augustine-civdei-20-19.txt`。',
     'scripts/verify-citations.py --source sources/commentary/augustine-civdei-20-19.txt --heading 奧古斯丁'),
    ('加爾文', '三、加爾文 (John Calvin)',
     '*Commentary on the Second Epistle to the Thessalonians*（John Pringle 英譯，公有領域），CCEL `ccel.org/ccel/c/calvin/calcom42/cache/calcom42.txt`，本地切出 `sources/commentary/calvin-2thess.txt`。',
     'scripts/verify-citations.py --source sources/commentary/calvin-2thess.txt --heading 加爾文'),
    ('亨利', '四、梅友 (Daniel Mayo，馬太·亨利《聖經全註》續作者)',
     '*Commentary on the Whole Bible*，第六冊（公有領域）。此冊書信部分多在亨利去世後由他人續寫，據該冊序言所列（引 J. B. Williams《馬太·亨利傳》p. 308），帖撒羅尼迦前後書出自 Daniel Mayo 之手，故本書署梅友之名而不署亨利。CCEL `ccel.org/ccel/h/henry/mhc6/cache/mhc6.txt`，本地切出 `sources/commentary/henry-2thess.txt`。',
     'scripts/verify-citations.py --source sources/commentary/henry-2thess.txt --heading 亨利'),
    ('摩根', '五、摩根 (G. Campbell Morgan)',
     '〈The Message of II. Thessalonians〉，*Living Messages of the Books of the Bible*, New Testament, Book Two (New York: Fleming H. Revell, 1912)，公有領域，archive.org `livingmessagesof0000gcam`（OCR 全文），本地切出 `sources/commentary/morgan-message-of-2thess.txt`；頁碼依掃描頁眉。這是一篇貫通全卷的信息，不是逐節註釋，凡某章未收摩根，是因為該文沒有討論那一段，不勉強湊引。',
     'scripts/verify-citations.py --source sources/commentary/morgan-message-of-2thess.txt --heading 摩根'),
    ('麥克阿瑟', '六、麥克阿瑟 (John MacArthur)',
     '帖撒羅尼迦後書系列講道（講道編號 53-1 至 53-17，1992年1月5日至7月26日），逐字稿取自 `gty.org/library/sermons-library/53-N`，本地保存於 `sources/commentary/gty/`；講題、經文與日期依各頁所印。',
     'scripts/verify-sermon-quotes.py --cache sources/commentary/gty-cache'),
]

def commentary(text):
    m = re.search(r'^## 歷代注疏.*?\n(.*?)(?=^## )', text, re.S | re.M)
    return m.group(1) if m else ''

def sections(block):
    parts = re.split(r'^### (.*)$', block, flags=re.M)
    return list(zip(parts[1::2], parts[2::2]))

def quotes(body):
    out, lines = [], body.splitlines()
    for i, l in enumerate(lines):
        if l.startswith('> "'):
            attr = next((x for x in lines[i + 1:i + 3] if x.startswith('> —')), '')
            out.append((l[3:60].rstrip().rstrip('"'), attr[4:].strip()))
    return out

def build():
    rows = {k: [] for k, *_ in PEOPLE}
    for f in sorted(glob.glob(os.path.join(BOOK, '0[1-9]-*.md'))):
        ch = int(os.path.basename(f)[:2])
        for head, body in sections(commentary(open(f, encoding='utf-8').read())):
            for key, *_ in PEOPLE:
                if key in head:
                    for q, attr in quotes(body):
                        loc = re.search(r'(on 2 Thess\. [\d:\-–]+|Homily [IVX]+|Book XX, ch\. 19|p+\. [\d\-–]+|sermon 53-\d+|The Argument)', attr)
                        rows[key].append((ch, loc.group(1) if loc else attr, q))
    out = []
    for key, title, desc, cmd in PEOPLE:
        r = rows[key]
        if not r:
            continue
        chs = sorted({c for c, _, _ in r})
        out += [f'## {title}', '', desc, '',
                f'逐字引文出現的章：{"、".join(f"第{c}章" for c in chs)}。共 {len(r)} 條，'
                f'全部以 `{cmd}` 機器核校。', '',
                '| 章 | 出處 | 引文開頭 |',
                '|--------|------------------------------------|----------------------------------------------------------|']
        for c, loc, q in r:
            out.append(f'| {c} | {loc} | {q.replace("|", "/")}… |')
        out.append('')
    return '\n'.join(out)

def main():
    text = open(REF, encoding='utf-8').read()
    a, b = text.find(START), text.find(END)
    new = text[:a + len(START)] + '\n' + build() + '\n' + text[b:]
    if '--check' in sys.argv:
        print('current' if new == text else 'STALE'); return 0 if new == text else 1
    open(REF, 'w', encoding='utf-8').write(new)
    print('ledger written')

if __name__ == '__main__':
    sys.exit(main())
