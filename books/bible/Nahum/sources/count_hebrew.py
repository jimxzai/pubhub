#!/usr/bin/env python3
"""Reproduce every Hebrew word count printed in the Nahum volume.

Reads sources/hebrew/wlc-nah.xml (openscriptures/morphhb, WLC with OSHB lemma
tags). The XML uses the Hebrew verse numbering (Heb 2:1 = English 1:15;
Heb 2:n = English 2:n-1); this script prints ENGLISH (CUV/NASB) numbering.
Run:  python3 books/bible/Nahum/sources/count_hebrew.py [lemma ...]
"""
import re, sys, collections
from pathlib import Path

XML = Path(__file__).resolve().parent / "hebrew" / "wlc-nah.xml"
LEMMAS = {
    "3068": "יהוה 耶和華", "5210": "נִינְוֵה 尼尼微", "5750": "עוֹד 再／仍", "4310": "מִי 誰",
    "4581": "מָעוֹז 保障", "5162": "נחם 安慰（含 מְנַחֲמִים）", "369": "אַיִן 無", "784": "אֵשׁ 火",
    "2009": "הִנֵּה 看哪", "1319": "בשׂר 報好信", "7965": "שָׁלוֹם 平安", "2620": "חָסָה 投靠",
    "3045": "יָדַע 認得", "5358": "נָקַם 施報（動詞）", "5359": "נָקָם 報仇（名詞）", "7072": "קַנּוֹא 忌邪",
    "2534": "חֵמָה 忿怒", "639": "אַף 怒", "750": "אָרֵךְ 長", "7451": "רַע 惡", "1100": "בְּלִיַּעַל 邪惡",
    "1818": "דָּם 血", "2183": "זְנוּנִים 淫行", "3785": "כְּשָׁפִים 邪術", "2719": "חֶרֶב 刀", "738": "אַרְיֵה 獅子",
    "3772": "כָּרַת 剪除", "1961": "הָיָה", "7451": "רָעָה 惡", "5674": "עָבַר 經過", "3117": "יוֹם 日子",
    "6440": "פָּנִים 面前", "5975": "עָמַד 站", "2388": "חָזַק 堅固", "6862": "צַר／צָרָה 患難", "4692": "מָצוֹר 保障（圍困）",
    "4013": "מִבְצָר 保障（堅壘）", "8085": "שָׁמַע 聽", "7200": "רָאָה 看", "3605": "כֹּל 全", "3808": "לֹא 不",
}

def eng(c, v):
    c, v = int(c), int(v)
    if c == 2: return (1, 15) if v == 1 else (2, v - 1)
    return (c, v)

text = XML.read_text(encoding="utf-8")
verses = re.findall(r'<verse osisID="Nah\.(\d+)\.(\d+)">(.*?)</verse>', text, re.S)
where = collections.defaultdict(list)
surface = collections.defaultdict(list)
total = 0
for c, v, body in verses:
    ec, ev = eng(c, v)
    total += len(re.findall(r'<w ', body))
    for lem, w in re.findall(r'<w lemma="([^"]*)"[^>]*>(.*?)</w>', body, re.S):
        for part in lem.split("/"):
            key = re.sub(r"[a-z]$", "", part.strip()).strip()
            where[key].append(f"{ec}:{ev}")
            surface[key].append((f"{ec}:{ev}", w.replace("/", "")))
print(f"verses: {len(verses)}   word tokens: {total}")
want = sys.argv[1:] or list(LEMMAS)
for k in want:
    v = where.get(k, [])
    c = collections.Counter(v)
    place = "、".join(n + (f"（{c[n]}）" if c[n] > 1 else "") for n in sorted(c, key=lambda s: tuple(map(int, s.split(":")))))
    print(f"{LEMMAS.get(k, k):<28} {len(v):>3}   {place}")
    if len(sys.argv) > 1:
        for ref, w in surface[k]: print("      ", ref, w)
