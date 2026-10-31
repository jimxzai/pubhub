#!/usr/bin/env python3
"""Reproduce every Hebrew word count printed in the Haggai volume.

Reads sources/hebrew/wlc-hag.xml (openscriptures/morphhb, WLC with OSHB
lemma tags) and prints, for each lemma the book cites, the count and the
verses it falls in. Run:  python3 books/bible/Haggai/sources/count_hebrew.py
"""
import re
import collections
from pathlib import Path

XML = Path(__file__).resolve().parent / "hebrew" / "wlc-hag.xml"
LEMMAS = {
    "7760": "שׂים 放（省察五次、壘石一次、立為印一次）", "3824": "לֵבָב 心（לבבכם）", "3068": "יהוה", "6635": "צְבָאוֹת 萬軍",
    "5002": "נְאֻם 這是…說的", "2088": "זֶה 這（הזה）", "1004": "בַּיִת 殿／家", "7307": "רוּחַ 靈",
    "3117": "יוֹם 日", "2720": "חָרֵב 荒涼（形容詞）", "2721": "חֹרֶב 乾旱（名詞）",
    "5782": "עוּר 激動", "3519": "כָּבוֹד 榮耀", "3513": "כָּבֵד 得榮耀", "7611": "שְׁאֵרִית 剩下的",
    "4397": "מַלְאָךְ 使者", "4399": "מְלָאכָה 工作", "7965": "שָׁלוֹם 平安", "977": "בָּחַר 揀選",
    "2368": "חוֹתָם 印", "2388": "חָזַק 剛強", "3372": "יָרֵא 懼怕／敬畏", "5971": "עָם 百姓",
    "1288": "בָּרַךְ 賜福", "854": "אֵת／עִם 與（אִתְּכֶם）", "7200": "רָאָה 看見",
}

text = XML.read_text(encoding="utf-8")
verses = re.findall(r'<verse osisID="Hag\.(\d+)\.(\d+)">(.*?)</verse>', text, re.S)
where = collections.defaultdict(list)
total = 0
for c, n, body in verses:
    total += len(re.findall(r'<w ', body))
    for lem, _w in re.findall(r'<w lemma="([^"]*)"[^>]*>(.*?)</w>', body):
        key = re.sub(r"[a-z]$", "", lem.split("/")[-1].strip()).strip()
        where[key].append(f"{c}:{n}")
print(f"verses: {len(verses)}   word tokens: {total}")
for k, name in LEMMAS.items():
    v = where.get(k, [])
    cnt = collections.Counter(v)
    place = "、".join(f"{n}" + (f"（{cnt[n]}）" if cnt[n] > 1 else "") for n in dict.fromkeys(v))
    print(f"{name:<24} {len(v):>3}   {place}")
