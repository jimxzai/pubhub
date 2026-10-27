#!/usr/bin/env python3 -I
"""Build scripture-NN.tsv, hebrew/song-he.tsv, speakers.tsv, units/*.scripture.md, CUV-DIFF-REPORT.txt."""
import json, re, html, collections, os
exec(open('parse_nasb.py').read().split("if __name__")[0])   # parse()

LABEL = re.compile(r'（(新娘|新郎|耶路撒冷的眾女子|新娘的兄弟)）')
VERSES = {1: 17, 2: 17, 3: 11, 4: 16, 5: 16, 6: 13, 7: 13, 8: 14}
UNITS = [
 ('01-let-him-kiss-me', (1,1), (1,4)), ('02-black-but-lovely', (1,5), (1,8)),
 ('03-rose-of-sharon', (1,9), (2,7)), ('04-the-voice-of-my-beloved', (2,8), (2,17)),
 ('05-by-night-on-my-bed', (3,1), (3,5)), ('06-solomons-litter', (3,6), (3,11)),
 ('07-you-are-altogether-beautiful', (4,1), (4,15)), ('08-the-garden-opened', (4,16), (5,1)),
 ('09-i-opened-but-he-was-gone', (5,2), (5,8)), ('10-white-and-ruddy', (5,9), (6,3)),
 ('11-fair-as-tirzah', (6,4), (6,13)), ('12-how-beautiful-and-pleasant', (7,1), (7,9)),
 ('13-his-desire-is-for-me', (7,10), (8,4)), ('14-set-me-as-a-seal', (8,5), (8,7)),
 ('15-make-haste-my-beloved', (8,8), (8,14))]
allv = [(c, v) for c in range(1, 9) for v in range(1, VERSES[c] + 1)]
idx = {k: i for i, k in enumerate(allv)}

# ---------- load ----------
ai, aien, fh, cn = {}, {}, {}, {}
for c in range(1, 9):
    for v in json.load(open(f'ai-eden/ch{c}.json'))['data']['verses']:
        ai[(c, v['verse'])] = v['textZh']; aien[(c, v['verse'])] = v['text']
    for r in json.load(open(f'fhl/ch{c}.json'))['record']: fh[(c, r['sec'])] = r['bible_text']
nb = {}
for c in range(1, 9):
    for n, s in parse(c).items():
        s = re.sub(r' \*(Solomon, the Lover, Speaks|Solomon’s Wedding Day|Admiration by the Bride|The Union of Love)\*$', '', s)
        s = re.sub(r'\bL ORD\b', 'LORD', s); s = re.sub(r'\bG OD\b', 'GOD', s); s = re.sub(r' ([.,;:!?])', r'\1', s); s = re.sub(r'\*\s*\*', ' ', s)
        s = s.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
        nb[(c, n)] = s
cuv = {k: LABEL.sub('', v).strip() for k, v in ai.items()}
assert len(ai) == len(fh) == len(nb) == 117

# ---------- scripture-NN.tsv ----------
for c in range(1, 9):
    with open(f'scripture-{c:02d}.tsv', 'w') as f:
        f.write('節\tai-eden和合本(去講者標題)\tfhl和合本\tai-eden NASB\tbiblehub NASB1995\n')
        for v in range(1, VERSES[c] + 1):
            k = (c, v)
            f.write(f'{v}\t{cuv[k]}\t{fh[k]}\t{aien[k]}\t{nb[k]}\n')

# ---------- Hebrew ----------
def hclean(s):
    s = re.sub(r'<[^>]+>', '', s); s = html.unescape(s).replace('\xa0', ' ')
    s = re.sub(r'[֑-ֽ֯׀׃]', '', s)
    return re.sub(r'\s+', ' ', s).strip()
HE = {}
for c in range(1, 9):
    for i, v in enumerate(json.load(open(f'sefaria/he{c}.json'))['versions'][0]['text']): HE[(c, i + 1)] = hclean(v)
def eng2heb(c, v):
    if c == 6 and v == 13: return (7, 1)
    if c == 7: return (7, v + 1)
    return (c, v)
with open('hebrew/song-he.tsv', 'w') as f, open('hebrew/hebrew-versification.tsv', 'w') as g:
    g.write('英文/和合本節號\t希伯來文節號\n')
    for (c, v) in allv:
        h = eng2heb(c, v); f.write(f'{c}:{v}\t{HE[h]}\n'); g.write(f'{c}:{v}\t{h[0]}:{h[1]}\n')
open('hebrew/README.txt', 'w').write(
 'song-he.tsv：Sefaria，Miqra according to the Masorah；已去讀經符號（U+0591-05AF、05BD、05C0、05C3），保留母音、maqaf(05BE)、(ketiv)[qere]、{פ}{ס}。\n'
 '第一欄用英文／和合本節號。希伯來節號不同處：英 6:13 = 希 7:1；英 7:n = 希 7:(n+1)（n=1..13）；其餘相同。對照見 hebrew-versification.tsv。\n'
 '章 6 希伯來文只有 12 節，章 7 有 14 節。\n')

# ---------- speakers ----------
S = [  # (ref, speaker, source, flag, note)
 ('1:1','（標題）','—','ok','歌的題辭'),
 ('1:2','新娘','ai-eden標題(1:1末)','ok','第一人稱陰性：願他與我親嘴'),
 ('1:4','新娘／眾女子','ai-eden標題(1:1末)','FLAG','希伯來文 1:4 同一節內 מָשְׁכֵנִי…אַחֲרֶיךָ(陽性「你」) 與 בָּךְ(陰性「你」) 並出，又有複數「我們」(נָגִילָה)；講者在節內是否轉為眾女子，經文語法不能定案'),
 ('1:8','新郎','ai-eden標題(1:7末)','FLAG','受話者陰性(תֵדְעִי, לָךְ)，講者性別語法上無標記；有人歸給眾女子，和合本標題歸新郎'),
 ('1:11','新郎／眾人','ai-eden標題(1:7末鏈)','FLAG','נַעֲשֶׂה־לָּךְ 為複數「我們要為你…」，講者是否為新郎一人不確定'),
 ('1:12','新娘','ai-eden標題(1:11末)','ok','陰性第一人稱「我的哪噠」'),
 ('1:15','新郎','ai-eden標題(1:14末)','ok','稱「我的佳偶」，受話者陰性'),
 ('1:16','新娘','ai-eden標題(1:15末)','ok','稱「我的良人」'),
 ('2:2','新郎','ai-eden標題(2:1末)','ok','稱「我的佳偶」'),
 ('2:3','新娘','ai-eden標題(2:2末)','ok','「我的良人」'),
 ('2:10','新郎（新娘轉述）','ai-eden標題(2:10節內)','ok','2:10a 為新娘的引言句「我良人對我說」；2:10b–14 是她所轉述的新郎的話'),
 ('2:15','（新郎／眾人）','ai-eden標題鏈：2:10 新郎，2:15 末轉新娘','FLAG','אֶחֱזוּ־לָנוּ 為複數命令「你們要為我們捉」；講者是新郎、新娘或家人，希伯來文不能定案；和合本標題未在此處另標'),
 ('2:16','新娘','ai-eden標題(2:15末)','ok','「我的良人屬我，我也屬他」'),
 ('3:1','新娘','ai-eden標題鏈','ok','第一人稱陰性：我夜間尋找我心所愛的'),
 ('3:6','（敘述者／眾女子）','ai-eden未標','FLAG','מִי זֹאת עֹלָה「這從曠野上來的是誰」無第一人稱；3:11 呼喚「錫安的女子」；ai-eden 標題鏈把 2:16–4:15 全歸新娘，與 4:1 起的陰性受話者不合，故此段標為不確定'),
 ('4:1','新郎','語法推定（ai-eden在此段無標題）','ok','受話者陰性(רַעְיָתִי, 稱「我的佳偶」「我妹子我新婦」)，講者必為男性；4:8 同'),
 ('4:16','新娘','ai-eden標題(4:15末)','ok','「願我良人進入自己的園」'),
 ('5:1','新郎','語法推定（ai-eden在此處無標題）','ok','5:1a「我妹子，我新婦，我入了我的園」'),
 ('5:1b','眾女子／朋友','ai-eden標題(5:1節內)','FLAG','אִכְלוּ רֵעִים שְׁתוּ「朋友們請吃」：講者可為新郎、眾人或呼應歌外之聲，希伯來文未標'),
 ('5:2','新娘','語法推定／ai-eden 5:2末','ok','「我身睡臥，我心卻醒」'),
 ('5:2b','新郎（新娘轉述）','ai-eden標題(5:2節內)','ok','「他敲門說：我的妹子，我的佳偶…」'),
 ('5:3','新娘','ai-eden標題(5:2末)','ok','第一人稱陰性'),
 ('5:9','眾女子','ai-eden標題(5:8末)','ok','מַה־דּוֹדֵךְ מִדּוֹד 受話者陰性單數'),
 ('5:10','新娘','ai-eden標題(5:9末)','ok','「我的良人白而且紅」'),
 ('6:1','眾女子','語法推定（ai-eden鏈把6:1歸新娘）','ok','אָנָה הָלַךְ דּוֹדֵךְ הַיָּפָה בַּנָּשִׁים 受話者陰性'),
 ('6:2','新娘','ai-eden標題(6:1末)','ok','「我的良人下到自己的園」'),
 ('6:4','新郎','語法推定（ai-eden在此段無標題）','ok','「我的佳偶，你美麗如得撒」受話者陰性'),
 ('6:10','（眾女子之語，新郎引述）','語法推定','FLAG','「這如晨光發現…的是誰」在 6:9 末句「眾女子見了就稱她有福」之後，似為被引述的眾女子之言；引號邊界希伯來文未標'),
 ('6:11','新郎或新娘','ai-eden無標題','FLAG','「我下到核桃園」第一人稱，講者性別無標記；6:12 「我不知不覺，我的心使我…」(עמי־נדיב) 是全卷公認難解處，講者不確定'),
 ('6:13','眾女子','ai-eden標題(6:12末)','ok','שׁוּבִי שׁוּבִי הַשּׁוּלַמִּית 複數「使我們得觀看你」(希伯來文 7:1)'),
 ('6:13b','新娘','ai-eden標題(6:13節內)','ok','「你們為何要觀看書拉密女」'),
 ('7:1','新郎（或眾女子）','語法推定（ai-eden在此段無標題）','FLAG','7:1–5 是對陰性受話者的讚美；7:5「王被髮綹纏住」以第三人稱稱王，講者是新郎抑或眾女子，經文語法不能定案；7:6–9 轉為第二人稱「我說我要爬上棕樹」可定為男性'),
 ('7:9b','新娘','ai-eden標題(7:9節內)','ok','7:9b–13 第一人稱陰性；稱「我的良人」'),
 ('8:1','新娘','ai-eden標題鏈','ok','「但願你像我的兄弟」'),
 ('8:5','眾人','ai-eden未標','FLAG','מִי זֹאת עֹלָה מִן־הַמִּדְבָּר מִתְרַפֶּקֶת עַל־דּוֹדָהּ 敘述句，講者希伯來文未標'),
 ('8:5b','新娘','ai-eden標題(8:5節內)','FLAG','עוֹרַרְתִּיךָ「我叫醒你」尾綴為陽性「你」，故講者應為對男子說話的女子；部分現代譯本與註釋另歸新郎，須存疑'),
 ('8:7b','新娘或編者之語','ai-eden標題鏈','FLAG','8:7b「若有人拿家中所有的財寶要換愛情」為箴言式斷語，講者語法上無標記'),
 ('8:8','新娘的兄弟','ai-eden標題(8:7末)','FLAG','אָחוֹת לָנוּ קְטַנָּה 複數「我們」；講者是兄弟或眾人，希伯來文未標'),
 ('8:10','新娘','ai-eden標題(8:9末)','ok','「我是牆」第一人稱陰性'),
 ('8:11','新郎（或新娘）','ai-eden標題(8:10末)','FLAG','8:11–12「所羅門有一葡萄園…我自己的葡萄園在我面前」：許多解經者歸新娘，ai-eden／和合本標題歸新郎；語法上無性別標記'),
 ('8:13','新郎','ai-eden標題鏈','ok','הַיּוֹשֶׁבֶת בַּגַּנִּים 受話者陰性，講者為男性'),
 ('8:14','新娘','ai-eden標題(8:13末)','ok','「我的良人哪，求你快來」'),
]
def unit_of(ref):
    c, v = [int(x) for x in re.match(r'(\d+):(\d+)', ref).groups()]
    for name, a, b in UNITS:
        if a <= (c, v) <= b: return name[:2]
with open('speakers.tsv', 'w') as f:
    f.write('單元\t節\t講者（自此起）\t依據\t確定度\t說明\n')
    for ref, sp, src, flag, note in S: f.write(f'{unit_of(ref)}\t{ref}\t{sp}\t{src}\t{flag}\t{note}\n')

# paragraph breaks: before verses at which speaker changes (only whole-verse boundaries)
breaks = set()
for ref, *_ in S:
    m = re.fullmatch(r'(\d+):(\d+)', ref)
    if m: breaks.add((int(m.group(1)), int(m.group(2))))

def para_groups(a, b):
    ks = [k for k in allv if a <= k <= b]
    groups, cur = [], []
    for k in ks:
        if cur and (k in breaks or k[1] == 1 or len(cur) >= 5): groups.append(cur); cur = []
        cur.append(k)
    groups.append(cur); return groups

def render(a, b, text, sep=''):
    out = []
    for g in para_groups(a, b):
        out.append('> ' + sep.join((f'^{c}:{v}^' if (v == 1 and (c, v) != a) else f'^{v}^') + text[(c, v)] for c, v in g))
    return '\n\n'.join(out)
for name, a, b in UNITS:
    with open(f'units/{name}.scripture.md', 'w') as f:
        f.write('### 中文 — 和合本 (CUV)\n\n' + render(a, b, cuv) + '\n\n### English — NASB\n\n' + render(a, b, nb, ' ') + '\n')

# ---------- verification ----------
cnt = collections.Counter(c for c, v in allv)
assert [cnt[c] for c in range(1, 9)] == [17,17,11,16,16,13,13,14]
covered = [k for _, a, b in UNITS for k in allv if a <= k <= b]
assert covered == allv, 'units gap/overlap'
for name, a, b in UNITS:
    t = open(f'units/{name}.scripture.md').read()
    zh, en = t.split('### English — NASB')
    for blk, label in ((zh, 'zh'), (en, 'en')):
        nums = [int(x.split(':')[-1]) for x in re.findall(r'\^([\d:]+)\^', blk)]
        exp = [v for c, v in allv if a <= (c, v) <= b]
        assert nums == exp, (name, label, nums, exp)
print('OK units', len(UNITS))
