#!/usr/bin/env python3
"""Reproducible keyword counts for Zechariah from oshb-zechariah.xml (OSHB/WLC lemmas).
Run:  python3 count_hebrew.py > keyword-counts.md     (verse numbers = 和合本/NASB; MT-differing ones are marked 〔MT c:v〕)
Lemma = the last '/'-segment of @lemma, with the disambiguating letter stripped ('859 a' -> 859)."""
import re, os, sys
D = os.path.dirname(os.path.abspath(__file__))
x = open(f'{D}/oshb-zechariah.xml', encoding='utf-8').read()
EN = {1: 21, 2: 13, 3: 10, 4: 14, 5: 11, 6: 15, 7: 14, 8: 23, 9: 17, 10: 12, 11: 17, 12: 14, 13: 9, 14: 21}
def mt_to_en(c, v):
    if c == 2: return (1, v + 17) if v <= 4 else (2, v - 4)
    return (c, v)
def label(c, v):          # English ref, plus MT ref when they differ
    ec, ev = mt_to_en(c, v)
    return f'{ec}:{ev}' + ('' if (ec, ev) == (c, v) else f'〔MT {c}:{v}〕')
W = []                    # token list in book order
for m in re.finditer(r'<verse osisID="Zech\.(\d+)\.(\d+)">(.*?)</verse>', x, re.S):
    c, v, body = int(m.group(1)), int(m.group(2)), m.group(3)
    for t in re.finditer(r'<w lemma="([^"]*)"[^>]*?morph="([^"]*)"[^>]*>(.*?)</w>', body):
        lem = t.group(1).split('/')[-1].split(' ')[0]
        mor = t.group(2).split('/')[-1]
        txt = t.group(3).replace('/', '')
        W.append(dict(c=c, v=v, lem=lem, mor=mor, morfull=t.group(2), txt=txt, full=t.group(1)))
KET = x.count('type="x-ketiv"')
assert len(W) + KET == x.count('<w '), (len(W), KET, x.count('<w '))   # ketiv-only words are replaced by their qere (read) form, which sits inside <note>
strip = lambda s: re.sub('[֑-ׇ]', '', s)
def hasl(w, code): return code in w['full'].replace(' ', '|').replace('/', '|').split('|') or w['lem'] == code
def lst(items):
    return '、'.join(label(w['c'], w['v']) for w in items)
out = []
def show(title, items, note=''):
    out.append(f'- **{title}**：{len(items)} 次 — {lst(items) or "—"}' + (f'　（{note}）' if note else ''))
def lem(code): return [w for w in W if w['lem'] == code]
def seq(codes):           # consecutive lemma sequence within one verse; returns the first token of each hit
    hits = []
    for i in range(len(W) - len(codes) + 1):
        if all(W[i + k]['lem'] == codes[k] and W[i + k]['v'] == W[i]['v'] and W[i + k]['c'] == W[i]['c'] for k in range(len(codes))):
            hits.append(W[i])
    return hits
out.append('# 撒迦利亞書關鍵詞計數（OSHB/WLC 詞元；節號為和合本／NASB 節號，括號內為 MT 節號）\n')
out.append(f'- 全書詞元總數（按 qere 讀法）：{len(W)}（OSHB <w> 元素 {len(W)+KET} 個，其中 {KET} 個 ketiv 由其 qere 取代）；節數 211；英文節數與 MT 節數相同，但 1:18-21＝MT 2:1-4，2:1-13＝MT 2:5-17。\n')
out.append('## 神的名與稱呼\n')
show('יְהוָה（Strong 3068）全部', lem('3068'))
show('יהוה צבאות「萬軍之耶和華」（3068 緊接 6635）', seq(['3068', '6635']))
show('צְבָאוֹת（6635）全部', lem('6635'))
show('「萬軍之耶和華」前接 אֲדֹנָי/אדון（136/113）', [w for w in seq(['113', '3068', '6635']) + seq(['136', '3068', '6635'])])
show('אֱלֹהִים（430）', lem('430'))
show('אֲדֹנָי（136）', lem('136'))
show('אָדוֹן（113）', lem('113'))
show('נְאֻם「說／宣告」（5002）', lem('5002'))
show('נְאֻם־יהוה（5002 緊接 3068）', seq(['5002', '3068']))
show('「萬軍之耶和華說」נאם יהוה צבאות（5002+3068+6635）', seq(['5002', '3068', '6635']))
out.append('\n## 「那日」「在那時」\n')
yom = [W[i] for i in range(len(W) - 1) if W[i]['lem'] == '3117' and W[i + 1]['lem'] == '1931' and W[i + 1]['c'] == W[i]['c'] and W[i + 1]['v'] == W[i]['v'] and strip(W[i + 1]['txt']).startswith('ה')]
show('בַּיּוֹם הַהוּא「在那日」（יום 後接 הַהוּא）', yom)
show('יוֹם（3117）全部', lem('3117'))
show('עֵת הַהִיא「在那時」（עת 後接 הַהִיא）', [W[i] for i in range(len(W) - 1) if W[i]['lem'] == '6256' and strip(W[i + 1]['txt']).startswith('ה') and W[i + 1]['lem'] == '1931'])
out.append('\n## 回轉 שׁוב（7725）\n')
sh = lem('7725')
show('שׁוּב 全部', sh)
stems = {}
def stem(w):
    segs = w['morfull'].split('/')
    segs[0] = segs[0][1:] if segs[0].startswith('H') else segs[0]      # drop the language flag H
    for g in segs:
        if g.startswith('V'): return g[1]
    return '?'
for w in sh: stems.setdefault(stem(w), []).append(w)
NAME = {'q': 'Qal', 'h': 'Hiphil', 'p': 'Piel', 'o': 'Polel', 'N': 'Niphal', 'H': 'Hophal', 'P': 'Pual', 't': 'Hithpael', 'O': 'Polal', '?': '(非動詞)'}   # OSHB stem codes
for k, v in sorted(stems.items()): show(f'　其中 {NAME.get(k, k)}', v)
out.append('\n## 同在、居住\n')
show('שָׁכַן 住（7931）', lem('7931'))
show('תָּוֶךְ「當中」（8432）全部', lem('8432'))
show('וִידַעְתֶּם כִּי־יהוה צבאות שְׁלָחַנִי「你們就知道萬軍之耶和華差遣了我」（3045…3588 3068 6635 7971）', [W[i] for i in range(len(W) - 5) if [W[i + k]['lem'] for k in range(6)] == ['3045', '3588', '3068', '6635', '7971', W[i + 5]['lem']] or [W[i + k]['lem'] for k in range(5)] == ['3045', '3588', '3068', '6635', '7971']])
show('יָדַע 知道（3045）', lem('3045'))
show('שָׁלַח 差（7971）', lem('7971'))
show('הִנְנִי / הִנְנוֹ（附人稱後綴的「看哪」，2005）', lem('2005'))
show('הִנֵּה「看哪」（2009）', lem('2009'))
out.append('\n## 靈、苗、王、牧人、嫉妒、憐憫\n')
show('רוּחַ 靈／風（7307）', lem('7307'))
show('צֶמַח 苗（6780）', lem('6780'))
show('מֶלֶךְ 王（4428）', lem('4428'))
show('מָלַךְ 作王（4427）', lem('4427'))
show('רָעָה 牧養／牧人（7462）', lem('7462'))
show('רָעָה 惡（7451）', lem('7451'))
show('רָעַע 行惡（7489）', lem('7489'))
show('רֵעַ 鄰舍（7453）', lem('7453'))
show('קָנָא 嫉妒（7065）', lem('7065'))
show('קִנְאָה 熱心／嫉妒（7068）', lem('7068'))
show('קַנּוֹא（7067）', lem('7067'))
show('חָמַל 顧惜（2550）', lem('2550'))
show('רָחַם 憐憫（7355）', lem('7355'))
show('רַחֲמִים 憐憫（7356）', lem('7356'))
show('חֵן 恩（2580）', lem('2580'))
show('תַּחֲנוּן 懇求（8469）', lem('8469'))
show('מַלְאָךְ 使者／天使（4397）', lem('4397'))
out.append('\n## 不要懼怕\n')
show('אַל־תִּירָאוּ／אַל־תִּירָא「不要懼怕」（408 後接 3372）', seq(['408', '3372']))
show('יָרֵא 懼怕（3372）', lem('3372'))
out.append('\n## 其他可能成為骨幹的詞\n')
show('קֹדֶשׁ／קָדוֹשׁ／קָדַשׁ 聖（6944/6918/6942）', lem('6944') + lem('6918') + lem('6942'))
show('שָׁלוֹם 平安（7965）', lem('7965'))
show('אֱמֶת 誠實／真理（571）', lem('571'))
show('עֶבֶד 僕人（5650）', lem('5650'))
show('שָׁמַע 聽（8085）', lem('8085'))
show('דָּבָר 話（1697）', lem('1697'))
show('חָזַק 堅固（2388）', lem('2388'))
show('כָּבוֹד 榮耀（3519）', lem('3519'))
show('אֶחָד 一（259）', lem('259'))
show('עַיִן 眼（5869）', lem('5869'))
show('יָד 手（3027）', lem('3027'))
show('בֹּא 來（935）', lem('935'))
out.append('\n## 地名\n')
show('יְרוּשָׁלִַם 耶路撒冷（3389）', lem('3389'))
show('צִיּוֹן 錫安（6726）', lem('6726'))
show('יְהוּדָה 猶大（3063）', lem('3063'))
show('יִשְׂרָאֵל 以色列（3478）', lem('3478'))
show('הַר 山（2022）', lem('2022'))
show('הַר הַזֵּיתִים 橄欖山（2022 + 2132）', [W[i] for i in range(len(W) - 1) if W[i]['lem'] == '2022' and W[i + 1]['lem'] == '2132'])
out.append('\n## 全書最後\n')
last = W[-3:]
out.append('- 全書最後三個詞：' + ' '.join(strip(w['txt']) for w in last) + f'（{label(last[-1]["c"], last[-1]["v"])}）；最後一個詞 {strip(last[-1]["txt"])}（lemma {last[-1]["lem"]}）。')
out.append('- 14:21 全節詞序：' + ' '.join(strip(w['txt']) for w in W if w['c'] == 14 and w['v'] == 21))
print('\n'.join(out))
