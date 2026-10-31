#!/usr/bin/env python3
"""Reproduce every Hebrew word count printed in the Zephaniah volume.

Reads sources/hebrew/wlc-zeph.xml (openscriptures/morphhb, WLC with OSHB lemma
tags). Counts are by OSHB lemma number (Strong's-based), so a count is of
tokens of that lemma, all forms. Run:
    python3 books/bible/Zapphaniah/sources/count_hebrew.py [lemma ...]
"""
import re, sys, collections
from pathlib import Path

XML = Path(__file__).resolve().parent / "hebrew" / "wlc-zeph.xml"
LEMMAS = {
    "3117": "יוֹם 日子", "7138": "קָרוֹב 近", "7126": "קָרַב 親近(動詞)", "7130": "קֶרֶב 中間",
    "622": "אָסַף 收取／聚集", "6908": "קָבַץ 聚集", "7197": "קָשַׁשׁ 聚集(2:1)", "1245": "בִּקֵּשׁ 尋求",
    "1875": "דָּרַשׁ 訪問", "3068": "יהוה", "5002": "נְאֻם 說", "6485": "פָּקַד 懲罰／眷顧",
    "6041": "עָנִי 困苦", "6035": "עָנָו 謙卑人", "6038": "עֲנָוָה 謙卑", "6664": "צֶדֶק 公義", "6662": "צַדִּיק 公義的",
    "7442": "רָנַן 歌唱", "7440": "רִנָּה 歡呼", "8055": "שָׂמֵחַ 歡喜", "5937": "עָלַז 歡欣", "1523": "גִּיל 喜樂",
    "2790": "חָרַשׁ 默然", "2013": "הָס 靜默", "1121": "בֵּן 子", "7611": "שְׁאֵרִית 餘剩", "7604": "שָׁאַר 留下",
    "8034": "שֵׁם 名", "1931": "הוּא 那", "5971": "עַם 民", "1471": "גּוֹי 國", "3372": "יָרֵא 懼怕",
    "1319": "בֹּשֶׁת/בּוֹשׁ 羞愧", "954": "בּוֹשׁ 羞愧", "1347": "גָּאוֹן 驕傲", "1363": "גָּבַהּ 高傲", "1361": "גָּבֹהַּ 高",
}

def load():
    text = XML.read_text(encoding="utf-8")
    return re.findall(r'<verse osisID="Zeph\.(\d+)\.(\d+)">(.*?)</verse>', text, re.S)

def lemma_key(lem):
    return re.sub(r"[a-z]$", "", lem.split("/")[-1].strip()).strip()

def main():
    verses = load()
    where = collections.defaultdict(list)
    total = 0
    for c, v, body in verses:
        total += len(re.findall(r"<w ", body))
        for lem, _w in re.findall(r'<w lemma="([^"]*)"[^>]*>(.*?)</w>', body):
            where[lemma_key(lem)].append(f"{c}:{v}")
    print(f"verses: {len(verses)}   word tokens: {total}")
    want = sys.argv[1:] or list(LEMMAS)
    for k in want:
        name = LEMMAS.get(k, k)
        v = where.get(k, [])
        cnt = collections.Counter(v)
        place = "、".join(n + (f"（{cnt[n]}）" if cnt[n] > 1 else "") for n in sorted(cnt, key=lambda x: tuple(map(int, x.split(":")))))
        print(f"{name:<22} {len(v):>3}   {place}")

if __name__ == "__main__":
    main()
