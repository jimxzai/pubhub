#!/usr/bin/env python3
"""Reproduce every Hebrew word count printed in the Malachi volume.

Reads sources/hebrew/wlc-mal.xml (openscriptures/morphhb, WLC with OSHB lemma tags).
Verse labels are converted to ENGLISH (和合本/NASB) numbering: Hebrew 3:19-24 = English 4:1-6.
Run:  python3 books/bible/malachi/sources/count_hebrew.py [lemma_number ...]  (no args = the book's table)
"""
import re, sys, collections
from pathlib import Path

XML = Path(__file__).resolve().parent / "hebrew" / "wlc-mal.xml"
LEMMAS = {  # Strong number: label  (OSHB lemma numbers; trailing letters stripped)
    "3068": "יהוה 耶和華", "6635": "צְבָאוֹת 萬軍", "559": "אָמַר 說", "157": "אָהַב 愛", "8130": "שָׂנֵא 恨",
    "8034": "שֵׁם 名", "8121": "שֶׁמֶשׁ 日頭", "1285": "בְּרִית 約", "898": "בָּגַד 詭詐", "7725": "שׁוּב 回轉／歸回",
    "7971": "שָׁלַח 差遣／休", "4397": "מַלְאָךְ 使者", "4401": "מַלְאָכִי 瑪拉基", "3117": "יוֹם 日子",
    "779": "אָרַר 咒詛（動）", "3994": "מְאֵרָה 咒詛（名）", "2764": "חֵרֶם 咒詛（名）", "3372": "יָרֵא 敬畏",
    "4172": "מוֹרָא 敬畏（名）", "3519": "כָּבוֹד 尊榮", "959": "בָּזָה 藐視", "1351": "גָּאַל 玷污", "3021": "יָגַע 煩瑣",
    "1497": "גָּזַל 搶奪", "6906": "קָבַע 奪取", "2490": "חָלַל 褻瀆", "4941": "מִשְׁפָּט 公平", "8451": "תּוֹרָה 訓誨／律法",
    "1": "אָב 父", "1121": "בֵּן 子", "7200": "רָאָה 看", "3820": "לֵב 心", "1696": "דָּבַר 說（Niphal 彼此談論）",
    "3548": "כֹּהֵן 祭司", "4503": "מִנְחָה 供物", "4196": "מִזְבֵּחַ 壇", "3878": "לֵוִי 利未", "3290": "יַעֲקֹב 雅各",
    "6215": "עֵשָׂו 以掃", "113": "אָדוֹן 主", "430": "אֱלֹהִים 神", "4643": "מַעֲשֵׂר 十分之一", "214": "אוֹצָר 倉庫",
    "5459": "סְגֻלָּה 特特歸我的產業", "5612": "סֵפֶר 冊", "2142": "זָכַר 記念", "1293": "בְּרָכָה 福",
    "6213": "עָשָׂה 行／做", "6666": "צְדָקָה 公義", "6662": "צַדִּיק 義人", "7563": "רָשָׁע 惡人", "2086": "זֵד 狂傲",
    "5927": "עָלָה 上", "935": "בּוֹא 來", "4994": "נָא", "3045": "יָדַע 知道", "5414": "נָתַן 賜／使", "4687": "מִצְוָה 命令", "6944": "קֹדֶשׁ 聖",
}

def conv(ch, v):  # Hebrew chapter/verse -> English chapter:verse
    return (4, v - 18) if (ch == 3 and v >= 19) else (ch, v)

text = XML.read_text(encoding="utf-8")
verses = re.findall(r'<verse osisID="Mal\.(\d+)\.(\d+)">(.*?)</verse>', text, re.S)
where = collections.defaultdict(list); forms = collections.defaultdict(list)
total = 0
for ch, v, body in verses:
    ec, ev = conv(int(ch), int(v))
    total += len(re.findall(r'<w ', body))
    for lem, w in re.findall(r'<w lemma="([^"]*)"[^>]*>(.*?)</w>', body):
        key = re.sub(r"[a-z]$", "", lem.split("/")[-1].strip()).strip()
        where[key].append(f"{ec}:{ev}"); forms[key].append((f"{ec}:{ev}", w.replace("/", "")))
print(f"verses: {len(verses)}   word tokens: {total}")
want = sys.argv[1:] or list(LEMMAS)
for k in want:
    name = LEMMAS.get(k, k)
    v = where.get(k, [])
    c = collections.Counter(v)
    order = sorted(c, key=lambda s: tuple(map(int, s.split(":"))))
    place = "、".join(n + (f"（{c[n]}）" if c[n] > 1 else "") for n in order)
    print(f"{name:<22} {len(v):>3}   {place}")
if len(sys.argv) > 1:
    for k in want:
        for ref, w in forms[k]: print(k, ref, w)
