#!/usr/bin/env python3
"""Reproduce every Hebrew word count printed in the Habakkuk volume.
Reads sources/hebrew/wlc-hab.xml (openscriptures/morphhb, WLC + OSHB lemma tags).
Run: python3 books/bible/habakkuk/sources/count_hebrew.py   (verse numbers are 和合本/MT-identical in Habakkuk)"""
import re, collections
from pathlib import Path
XML = Path(__file__).resolve().parent / "hebrew" / "wlc-hab.xml"
LEMMAS = {
    "8085": "שָׁמַע 聽見（動詞）", "8088": "שֵׁמַע 風聲／名聲（名詞）", "3467": "יָשַׁע 拯救（動詞）", "3468": "יֵשַׁע 拯救（名詞）", "3444": "יְשׁוּעָה 拯救",
    "7200": "רָאָה 看見", "5027": "נָבַט 看／觀望", "6822": "צָפָה 守望", "2372": "חָזָה 看見（異象）", "2377": "חָזוֹן 異象",
    "2555": "חָמָס 強暴", "1945": "הוֹי 禍哉", "6662": "צַדִּיק 義人", "7563": "רָשָׁע 惡人", "530": "אֱמוּנָה 信（誠實）", "2421": "חָיָה 活／復興",
    "2442": "חָכָה 等候", "935": "בּוֹא 來", "776": "אֶרֶץ 地", "5542": "סֶלָה 細拉", "3778": "כַּשְׂדִּי 迦勒底人", "1471": "גּוֹי 列國", "5971": "עַם 眾民",
    "4941": "מִשְׁפָּט 公理／審判", "5937": "עָלַז 歡欣", "2013": "הָס 肅靜", "4100": "מָה 為何（לָמָּה）", "3068": "יהוה", "430": "אֱלֹהִים", "4899": "מָשִׁיחַ 受膏者",
    "7355": "רָחַם 憐憫", "3372": "יָרֵא 懼怕", "3519": "כָּבוֹד 榮耀", "3045": "יָדַע 知道", "1471b": "", 
}
text = XML.read_text(encoding="utf-8")
verses = re.findall(r'<verse osisID="Hab\.(\d+)\.(\d+)">(.*?)</verse>', text, re.S)
where = collections.defaultdict(list); total = 0
for c, v, body in verses:
    total += len(re.findall(r'<w ', body))
    for lem in re.findall(r'<w lemma="([^"]*)"', body):
        key = re.sub(r"[a-z]$", "", lem.split("/")[-1].strip()).strip()
        where[key].append(f"{c}:{v}")
print(f"verses: {len(verses)}   word tokens: {total}")
for k, name in LEMMAS.items():
    if not name: continue
    v = where.get(k, [])
    cnt = collections.Counter(v)
    place = "、".join(n + (f"（{cnt[n]}）" if cnt[n] > 1 else "") for n in dict.fromkeys(v))
    print(f"{name:<22} {len(v):>3}   {place}")
