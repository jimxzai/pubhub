#!/usr/bin/env python3
"""Reproduce every Hebrew word count printed in the Obadiah volume.

Reads sources/hebrew/wlc-obad.xml (openscriptures/morphhb, WLC with OSHB
lemma tags) and prints, for each lemma the book cites, the count and the
verses it falls in. Run:  python3 books/bible/Obadiah/sources/count_hebrew.py
"""
import re
import collections
from pathlib import Path

XML = Path(__file__).resolve().parent / "hebrew" / "wlc-obad.xml"
LEMMAS = {
    "3117": "יוֹם 日子", "408": "אַל 不可（禁止式）", "2022": "הַר 山", "6215": "עֵשָׂו 以掃",
    "3772": "כָּרַת 剪除", "3381": "יָרַד 拉下", "5377": "נָשָׁא（hiphil）欺騙", "5975": "עָמַד 站",
    "8394": "תְּבוּנָה 聰明", "6": "אָבַד 滅", "3423": "יָרַשׁ 承受", "3068": "יהוה", "8354": "שָׁתָה 喝",
    "343": "אֵיד 災", "8300": "שָׂרִיד 餘剩", "6413": "פְּלֵיטָה 逃脫", "6726": "צִיּוֹן 錫安",
}

text = XML.read_text(encoding="utf-8")
verses = re.findall(r'<verse osisID="Obad\.1\.(\d+)">(.*?)</verse>', text, re.S)
where = collections.defaultdict(list)
total = 0
for n, body in verses:
    total += len(re.findall(r'<w ', body))
    for lem, _w in re.findall(r'<w lemma="([^"]*)"[^>]*>(.*?)</w>', body):
        key = re.sub(r"[a-z]$", "", lem.split("/")[-1].strip()).strip()
        where[key].append(int(n))
print(f"verses: {len(verses)}   word tokens: {total}")
for k, name in LEMMAS.items():
    v = where.get(k, [])
    c = collections.Counter(v)
    place = "、".join(f"{n}" + (f"（{c[n]}）" if c[n] > 1 else "") for n in sorted(c))
    print(f"{name:<24} {len(v):>3}   {place}")
