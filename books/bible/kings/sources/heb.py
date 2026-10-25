#!/usr/bin/env python3
"""heb.py CH V[-V]  (ENGLISH numbering) -> pointed Hebrew (cantillation stripped, maqaf kept) from Sefaria cache
   heb.py --strong H1234 [...]  -> OpenScriptures Strong's entry (lemma, translit, gloss)"""
import sys, json, re, os
D = os.path.dirname(os.path.abspath(__file__))
def strip(s):
    s = s.replace('&thinsp;', ' ').replace('&nbsp;', ' ')
    s = re.sub(r'\{[\u05e4\u05e1]\}', '', s)
    s = re.sub('[\u0591-\u05AF\u05BD\u05C0\u05C3\u05C4\u05C5]', '', s)   # cantillation, meteg, paseq, sof pasuq
    s = re.sub(r'<[^>]+>', '', s)
    return re.sub(r'\s+', ' ', s).strip()
if sys.argv[1] == '--strong':
    import xml.etree.ElementTree as ET
    ns = {'x': 'http://openscriptures.github.com/morphhb/namespace'}
    root = ET.parse(f'{D}/HebrewStrong.xml').getroot()
    for e in root.iter('{http://openscriptures.github.com/morphhb/namespace}entry'):
        if e.get('id') in sys.argv[2:]:
            w = e.find('x:w', ns)
            m = e.find('x:meaning', ns); u = e.find('x:usage', ns)
            print(e.get('id'), w.text if w is not None else '', w.get('xlit') if w is not None else '', '|',
                  ''.join(m.itertext()).strip() if m is not None else '', '|', ''.join(u.itertext()).strip() if u is not None else '')
else:
    # English (CUV/NASB) chapter:verse numbering in, Hebrew text out.
    # Versification differs in 1 Kings: Heb 5:1-14 = Eng 4:21-34; Heb 5:15-32 = Eng 5:1-18;
    # Heb 22:44 = second half of Eng 22:43; Heb 22:45-54 = Eng 22:44-53.
    D2 = lambda n: json.load(open(f'{D}/heb/{n}.json', encoding='utf8'))['he']
    def get(ch, v):
        if ch == 4 and v >= 21: return [(5, v - 20)]
        if ch == 5: return [(5, v + 14)]
        if ch == 22 and v == 43: return [(22, 43), (22, 44)]
        if ch == 22 and v >= 44: return [(22, v + 1)]
        return [(ch, v)]
    ch = int(sys.argv[1]); a = sys.argv[2]
    lo, hi = a.split('-') if '-' in a else (a, a)
    for v in range(int(lo), int(hi) + 1):
        for c, hv in get(ch, v):
            print(f'{ch}:{v}', strip(D2(c)[hv - 1]))
