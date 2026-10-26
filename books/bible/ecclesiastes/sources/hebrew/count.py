#!/usr/bin/env python3
"""Reproducible word counts for the Ecclesiastes spine (Leningrad text via Sefaria,
hebrew.tsv keyed by ENGLISH verse numbers; Heb 4:17 = Eng 5:1, Heb 5:n = Eng 5:n+1).

usage: python3 count.py            # prints the standard table
       python3 count.py 'regex'    # one ad-hoc root/word regex (consonants, prefixes allowed)
Tokenisation: niqqud/cantillation stripped, maqqef -> space, sof pasuq removed.
"""
import re, sys, unicodedata, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROWS = [l.rstrip('\n').split('\t', 1) for l in open(f'{HERE}/hebrew.tsv', encoding='utf-8')]

def toks(s):
    s = s.replace('־', ' ').replace('׃', ' ')
    s = ''.join(ch for ch in s if not unicodedata.category(ch).startswith('M'))
    return s.split()

TOK = [(k, toks(t)) for k, t in ROWS]

def words(pat):
    r = re.compile(pat)
    return [(k, w) for k, ws in TOK for w in ws if r.search(w)]

def phrase(first, second):
    a, b = re.compile(first), re.compile(second)
    return [k for k, ws in TOK for i in range(len(ws) - 1) if a.search(ws[i]) and b.search(ws[i + 1])]

def show(label, hits, refs=True):
    ks = [h if isinstance(h, str) else h[0] for h in hits]
    print(f'{label:34s}{len(ks):4d}' + ('  ' + ' '.join(ks) if refs else ''))
    return ks

if __name__ == '__main__':
    if len(sys.argv) > 1:
        show(sys.argv[1], words(sys.argv[1])); sys.exit()
    show('הֶבֶל hebel (all forms)', words('הבל'))
    show('תַּחַת הַשָּׁמֶשׁ under the sun', phrase(r'^תחת$', r'^השמש$'))
    show('רְעוּת/רַעְיוֹן רוּחַ chasing wind', phrase(r'^ו?ר(עות|עיון)$', r'^רוח$'))
    show('עָמָל toil (any word with עמל)', words('עמל'))
    show('יִתְרוֹן advantage', words('יתרון'))
    show('חֵלֶק portion', words('^[ובכלמה]*חלק'))
    show('שִׂמְחָה/שָׂמַח joy', words('שמח'))
    show('אֱלֹהִים (any word containing)', words('אלהים'), refs=False)
    show('הָאֱלֹהִים (with the article)', words('^[ולבמכ]*האלהים$'), refs=False)
    show('יהוה / אדני', words('^[ולבמכ]*(יהוה|אדני|ה)$'))
    show('מִקְרֶה fate', words('מקרה'))
    show('רָאִיתִי I saw', words('ראיתי'))
    show('יָדַעְתִּי I know', words('ידעתי'))
    show('קֹהֶלֶת', words('קהלת'))
    show('נָתַן give (all forms)', words('^[ולבמכש]*(נתן|נתתי|נתנו|נתנה|יתן|תתן|לתת|נתת|תת)$'), refs=False)
    show('יָרֵא/יִרְאָה fear', words('^[ולבמכש]*(ירא|יראי|יראו|יראה|יראת|ירא־)'))
    show('אָכַל eat', words('^[ולבמכש]*(אכל|אכול|אוכל|יאכל|תאכל|נאכל|אכלו|אכלת)'))
    show('שָׁתָה drink', words('^[ולבמכש]*(שתה|שתות|ישתה|שתו)'))
    show('טוֹב good', words('^[ובכלמה]*טוב'), refs=False)
    show('חָכָם/חָכְמָה wise/wisdom', words('חכם|חכמ'), refs=False)
    show('כְּסִיל fool', words('כסיל'), refs=False)
    show('שְׁאוֹל Sheol', words('שאול'))
    show('עוֹלָם eternity/forever', words('^[ובכלמה]*עולם'))
    show('רוּחַ wind/spirit', words('^[ובכלמה]*רוח'))
    show('מַה־יִּתְרוֹן "what advantage"', phrase(r'^מה$', r'^יתרון$'))
    show('הַכֹּל הָבֶל "all is vanity"', phrase(r'^הכל$', r'^הבל$'))
    show('אֶחָד רֹעֶה one shepherd', words('^[ובכלמה]*רועה'))
