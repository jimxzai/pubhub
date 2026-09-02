#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regenerate the Hebrews apparatus from the chapter sources.

    python3 scripts/gen-hebrews-apparatus.py

Writes books/bible/hebrews/99a-scripture-index.md and 99b-greek-glossary.md.
Both are derived, never hand-edited: run this after changing any chapter, or
the index will quietly disagree with the book. The build script does not call
it, so that a build never rewrites source files behind your back.
"""
import os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      '..', 'books', 'bible', 'hebrews'))

import re, io, glob, collections, unicodedata

CANON = [
 ('創世記','Genesis',['創世記','創']), ('出埃及記','Exodus',['出埃及記','出']),
 ('利未記','Leviticus',['利未記','利']), ('民數記','Numbers',['民數記','民']),
 ('申命記','Deuteronomy',['申命記','申']), ('約書亞記','Joshua',['約書亞記']),
 ('士師記','Judges',['士師記','士']), ('撒母耳記上','1 Samuel',['撒母耳記上','撒上']),
 ('撒母耳記下','2 Samuel',['撒母耳記下','撒下']), ('列王紀上','1 Kings',['列王紀上','王上']),
 ('列王紀下','2 Kings',['列王紀下','王下']), ('歷代志上','1 Chronicles',['歷代志上','代上']),
 ('歷代志下','2 Chronicles',['歷代志下','代下']), ('尼希米記','Nehemiah',['尼希米記']),
 ('約伯記','Job',['約伯記']), ('詩篇','Psalms',['詩篇','詩']), ('箴言','Proverbs',['箴言','箴']),
 ('傳道書','Ecclesiastes',['傳道書']), ('以賽亞書','Isaiah',['以賽亞書','賽']),
 ('耶利米書','Jeremiah',['耶利米書','耶']), ('耶利米哀歌','Lamentations',['耶利米哀歌','哀']),
 ('以西結書','Ezekiel',['以西結書','結']), ('但以理書','Daniel',['但以理書','但']),
 ('何西阿書','Hosea',['何西阿書','何']), ('阿摩司書','Amos',['阿摩司書','摩']),
 ('哈巴谷書','Habakkuk',['哈巴谷書','哈']), ('撒迦利亞書','Zechariah',['撒迦利亞書']),
 ('瑪拉基書','Malachi',['瑪拉基書','瑪']), ('馬太福音','Matthew',['馬太福音','太']),
 ('馬可福音','Mark',['馬可福音','可']), ('路加福音','Luke',['路加福音','路']),
 ('約翰福音','John',['約翰福音','約']), ('使徒行傳','Acts',['使徒行傳','徒']),
 ('羅馬書','Romans',['羅馬書','羅']), ('哥林多前書','1 Corinthians',['哥林多前書','林前']),
 ('哥林多後書','2 Corinthians',['哥林多後書','林後']), ('加拉太書','Galatians',['加拉太書','加']),
 ('以弗所書','Ephesians',['以弗所書','弗']), ('腓立比書','Philippians',['腓立比書','腓']),
 ('歌羅西書','Colossians',['歌羅西書','西']), ('帖撒羅尼迦前書','1 Thessalonians',['帖撒羅尼迦前書','帖前']),
 ('提摩太前書','1 Timothy',['提摩太前書','提前']), ('提摩太後書','2 Timothy',['提摩太後書','提後']),
 ('雅各書','James',['雅各書','雅']), ('彼得前書','1 Peter',['彼得前書','彼前']),
 ('彼得後書','2 Peter',['彼得後書','彼後']), ('約翰一書','1 John',['約翰一書','約壹']),
 ('猶大書','Jude',['猶大書']), ('啟示錄','Revelation',['啟示錄','啟']),
]
ALIAS = {a: c for c, _, al in CANON for a in al}
EN = {c: e for c, e, _ in CANON}
ORDER = {c: i for i, (c, _, _) in enumerate(CANON)}
names = sorted(ALIAS, key=len, reverse=True)
REF = re.compile(r'(?<![一-鿿])(' + '|'.join(map(re.escape, names)) + r')\s?(\d{1,3}):(\d{1,3}(?:-\d{1,3})?)')

def where(f):
    for pre, lab in (('000-','前言'),('00a','卷首·定位'),('00b','卷首·骨幹'),('00-','概覽'),
                     ('99-app','附錄'),('99-out','卷末'),('999','跋'),('elder','總綱')):
        if f.startswith(pre): return lab
    return '第%d章' % int(f[:2]) if f[:2].isdigit() else f

SORTKEY = {'前言':-6,'概覽':-5,'卷首·定位':-4,'卷首·骨幹':-3,'總綱':-2}
def loc_sort(l):
    if l in SORTKEY: return SORTKEY[l]
    if l.startswith('第'): return int(re.search(r'\d+', l).group())
    return {'卷末':90,'跋':91,'附錄':92}.get(l, 99)

idx = collections.defaultdict(set)
for f in sorted(glob.glob('*.md')):
    for m in REF.finditer(io.open(f, encoding='utf-8').read()):
        idx[(ALIAS[m.group(1)], int(m.group(2)), m.group(3))].add(where(f))

out = ["""---
title: 希伯來書研讀
subtitle: Hebrews Deep Study
author: PubHub 三書精讀系統
date: 2026年8月
publisher: 三書精讀出版系統
---

# 附錄二：經文索引 (Appendix II: Scripture Index)

本索引收錄本書引用或討論過的**希伯來書以外**的一切經文，按聖經正典次序排列。
希伯來書本身的經文，請循目次的章次查閱；各章鑰詞另見〈附錄三：希臘文詞彙表〉。

「出現處」一欄標明該處經文在本書何章何節出現：數字為正文章次，其餘為卷首、卷末各篇。
"""]
books = sorted({k[0] for k in idx}, key=lambda b: ORDER[b])
for b in books:
    ents = sorted([k for k in idx if k[0] == b],
                  key=lambda k: (k[1], int(k[2].split('-')[0])))
    # A flowing list, not a table per book: 26 little two-row tables wasted most
    # of the page and repeated the same header 26 times.
    out.append(f"\n## {b} ({EN[b]})\n")
    items = []
    for _, ch, vs in ents:
        locs = '、'.join(sorted(idx[(b, ch, vs)], key=loc_sort))
        items.append(f"**{ch}:{vs}** {locs}")
    out.append('　·　'.join(items) + '\n')
io.open('99a-scripture-index.md', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print(f"經文索引：{len(books)} 卷、{len(idx)} 條")



GREEK = re.compile(r'[Ͱ-Ͽἀ-῿]')
def fold(g):
    s = unicodedata.normalize('NFD', g)
    return ''.join(c for c in s if not unicodedata.combining(c)).lower()
def chnum(s):
    m = re.search(r'[0-9]+', s)
    return int(m.group()) if m else 999

# Transliterations for the thirteen Key Words, which have no Word Study row
KEYTR = {
 'κρείττων':'kreittōn', 'παραρρέω':'pararrheō', 'σήμερον':'sēmeron',
 'κατάπαυσις':'katapausis', 'σαββατισμός':'sabbatismos',
 'ἔμαθεν ὑπακοήν':'emathen hypakoēn', 'ἄγκυρα':'ankyra',
 'ἀκατάλυτος':'akatalutos', 'καινή διαθήκη':'kainē diathēkē',
 'ἅπαξ':'hapax', 'ἐφάπαξ':'ephapax', 'ἐκάθισεν':'ekathisen',
 'ὑπόστασις':'hypostasis', 'ἀφορῶντες':'aphorōntes',
 'ἔξω τῆς παρεμβολῆς':'exō tēs parembolēs',
}

entries = {}                       # greek lemma -> [translit, gloss, {locations}]
for f in sorted(glob.glob('[01][0-9]-*.md')):
    ch = '%d' % int(f[:2])
    src = io.open(f, encoding='utf-8').read()

    m = re.search(r'## 原文研讀.*?(?=\n## )', src, re.S)
    if m:
        for line in m.group(0).split('\n'):
            if (not line.startswith('|') or '希臘文' in line
                    or re.match(r'\|[\s\-|]+\|$', line)):
                continue
            c = [x.strip() for x in line.split('|')[1:-1]]
            if len(c) < 3 or not GREEK.search(c[0]):
                continue
            gk = c[0].strip('* ')
            e = entries.setdefault(gk, [c[1], c[2], set()])
            e[2].add(ch)

    k = re.search(r'## 鑰詞深讀：(.+?)\s*\(Key Word — (.+?)\)', src)
    if k:
        gloss, greek = k.group(1).strip(), k.group(2).strip()
        for part in [p.strip() for p in greek.split('/')]:
            e = entries.setdefault(part, [KEYTR.get(part, ''), gloss, set()])
            e[0] = e[0] or KEYTR.get(part, '')
            e[1] = e[1] or gloss
            e[2].discard(ch)                      # the 鑰 marker supersedes a plain hit
            e[2].add(ch + '\\textsuperscript{鑰}')

hdr = """---
title: 希伯來書研讀
subtitle: Hebrews Deep Study
author: PubHub 三書精讀系統
date: 2026年8月
publisher: 三書精讀出版系統
---

# 附錄三：希臘文詞彙表 (Appendix III: Greek Glossary)

本表彙集本書各章〈原文研讀〉與〈鑰詞深讀〉處理過的全部希臘文詞條，按希臘字母次序排列
（排序不計氣號與重音）。字形採詞典形（lemma）；經文中的實際變化形見各章正文。

「出現章」為正文章次；標 \\textsuperscript{鑰} 者，是該章專設〈鑰詞深讀〉一節深入處理的字。
十三個鑰詞連起來讀，就是一條走完全書的路——另見卷首〈十三章鑰詞〉一覽。

"""
# The separator row must clear pandoc's --columns threshold (72), or the table
# compiles to bare `l` columns that cannot wrap and silently overflow the text
# block. See scripts/widen-table-separators.py and gotchas.md.
rows = ["| 希臘文 | 音譯 | 意義 | 出現章 |",
        "|----------------------|----------------------|--------------|------------|"]
# A lemma the book uses in two distinct senses needs both shown; taking
# whichever chapter was read first would hide the other.
DUAL = {'ὑπόστασις': '本體、實質（1:3）／實底、把握（11:1）'}

for gk in sorted(entries, key=fold):
    tr, gloss, locs = entries[gk]
    gloss = DUAL.get(gk, gloss)
    tr = tr.strip('* ')
    # a chapter listed both plainly and with the 鑰 marker needs only the marker
    marked = {l for l in locs if '鑰' in l}
    locs = {l for l in locs if l in marked or l + '\\textsuperscript{鑰}' not in marked}
    where = '、'.join(sorted(locs, key=chnum))
    rows.append(f"| *{gk}* | {tr} | {gloss} | {where} |")
rows.append(f"\n共 {len(entries)} 條詞目。")
io.open('99b-greek-glossary.md', 'w', encoding='utf-8').write(hdr + '\n'.join(rows) + '\n')
print(f"{len(entries)} entries")


# ------------------------------------------------------------------ name index
# Curated, not harvested: an auto-scan for "Chinese (Latin)" pairs returned the
# section headings (基督焦點 (Christ at the Center) …) far more often than any
# person. Ambiguous forms carry a lookahead — 亞伯 otherwise matches inside
# 亞伯拉罕, 利未 inside 利未記, 雅各 inside 雅各書.
BIBLE = [
    ('麥基洗德', None), ('亞伯拉罕', None), ('摩西', None), ('亞倫', None),
    ('約書亞', None), ('大衛', None), ('以撒', None), ('雅各', r'雅各(?!書)'),
    ('以掃', None), ('挪亞', None), ('以諾', None), ('亞伯', r'亞伯(?!拉罕)'),
    ('該隱', None), ('撒拉', None), ('喇合', None), ('基甸', None), ('巴拉', None),
    ('參孫', None), ('耶弗他', None), ('撒母耳', None), ('利未', r'利未(?!記)'),
    ('羅得', None), ('烏西雅', None), ('司提反', None), ('提摩太', None),
    ('保羅', None), ('彼得', None), ('巴拿巴', None), ('亞波羅', None),
    ('路加', None), ('西拉', None), ('馬可', None),
]
HIST = [
    ('亞他那修', None), ('俄利根', None), ('屈梭多模', None), ('奧古斯丁', None),
    ('特土良', None), ('加爾文', None), ('歐文', None), ('路德', None),
    ('摩根', None), ('麥克阿瑟', None), ('布魯斯', None), ('連恩', None),
    ('休斯', None), ('老弟兄', None),
    ('尼祿', None), ('提多', None), ('維斯帕先', None), ('班超', None),
    ('迦膩色伽', None), ('明帝', None),
]

def _where(fn):
    for pre, lab in (('000-', '前言'), ('00a', '卷首·定位'), ('00b', '卷首·骨幹'),
                     ('00-', '概覽'), ('99-app', '附錄一'), ('99a', '附錄二'),
                     ('99b', '附錄三'), ('99c', '附錄四'), ('99-out', '卷末'),
                     ('999', '跋'), ('elder', '總綱')):
        if fn.startswith(pre):
            return lab
    return '第%d章' % int(fn[:2]) if fn[:2].isdigit() else fn

_ORD = {'前言': -6, '概覽': -5, '卷首·定位': -4, '卷首·骨幹': -3, '總綱': -2}
def _lsort(l):
    if l in _ORD: return _ORD[l]
    if l.startswith('第'): return int(re.search(r'\d+', l).group())
    return {'卷末': 90, '跋': 91, '附錄一': 92, '附錄二': 93,
            '附錄三': 94, '附錄四': 95}.get(l, 99)

def _find(entries):
    hits = {}
    for name, pat in entries:
        rx = re.compile(pat or re.escape(name))
        locs = set()
        for fn in sorted(glob.glob('*.md')):
            if fn.startswith('99d'):
                continue                      # don't index the index
            if rx.search(io.open(fn, encoding='utf-8').read()):
                locs.add(_where(fn))
        if locs:
            hits[name] = sorted(locs, key=_lsort)
    return hits

out = ["""---
title: 希伯來書研讀
subtitle: Hebrews Deep Study
author: PubHub 三書精讀系統
date: 2026年8月
publisher: 三書精讀出版系統
---

# 附錄五：人名索引 (Appendix V: Index of Names)

「出現處」為正文章次，其餘為卷首、卷末與各附錄。同名而異人者另加註記。
所引著作之版本資料，見〈附錄四：徵引書目〉。
"""]
for title, entries in [('一、聖經人物 (Biblical Figures)', BIBLE),
                       ('二、解經者與歷史人物 (Commentators and Historical Figures)', HIST)]:
    hits = _find(entries)
    out.append(f"\n## {title}\n")
    out.append('　·　'.join(f"**{n}** {'、'.join(l)}" for n, l in hits.items()) + '\n')
out.append("""
> **兩位約翰·歐文**：清教徒神學家歐文（John Owen, 1616-1683），《希伯來書註釋》七卷的作者；
> 與十九世紀英國聖公會牧師歐文（John Owen, Vicar of Thrussington），加爾文希伯來書註釋的英譯者。
> 本書兩處均有引用，詳見〈附錄四〉。

---

*三書精讀項目 · 希伯來書研讀 · 附錄五：人名索引*
""")
io.open('99d-name-index.md', 'w', encoding='utf-8').write('\n'.join(out))
print(f"人名索引：{len(_find(BIBLE))} 聖經人物 + {len(_find(HIST))} 解經者／歷史人物")
