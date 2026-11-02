#!/usr/bin/env python3
"""Generate the Worship Book markdown (敬拜與禱告手冊).

Every piece of Scripture is read verbatim from ai-eden's data/cuv.json (和合本).
Every hymn text is read verbatim from the PubHub chapters that already carry it
(the "配詩" blocks); nothing is retyped.  Usage counts are computed from those
same chapters.  Prayers and short introductions are original to this book and
are labelled as such.

Output: ../../../output/hymnworship-body.md  (the build script adds the header)
"""
import glob
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
BIBLE = os.path.dirname(HERE)                      # books/bible
CUV = os.environ.get("CUV_JSON", "/Users/jimxiao/dev/ai-eden/data/cuv.json")
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "hymnworship-body.md")

cuv = json.load(open(CUV, encoding="utf-8"))
# Known defect in ai-eden's cuv.json: Ps 46:4 lost the rare character 汊 (FHL 和合本, cnbible.com and this
# repo's other books all read 「這河的分汊使神的城歡喜」).  Corrected here; the site data is not touched.
_p46 = cuv["psalms-46"]["4"]
assert "這河的分使" in _p46 or "這河的分汊使" in _p46, _p46
cuv["psalms-46"]["4"] = _p46.replace("這河的分使", "這河的分汊使")

# ---------------------------------------------------------------- scripture
BOOKS = {
    "創": "genesis", "出": "exodus", "利": "leviticus", "民": "numbers", "申": "deuteronomy",
    "書": "joshua", "撒上": "1-samuel", "撒下": "2-samuel", "王上": "1-kings", "代下": "2-chronicles",
    "詩": "psalms", "箴": "proverbs", "賽": "isaiah", "耶": "jeremiah", "哀": "lamentations",
    "亞": "zechariah", "太": "matthew", "可": "mark", "路": "luke", "約": "john", "徒": "acts",
    "羅": "romans", "林前": "1-corinthians", "林後": "2-corinthians", "加": "galatians",
    "弗": "ephesians", "腓": "philippians", "西": "colossians", "帖前": "1-thessalonians",
    "提前": "1-timothy", "來": "hebrews", "雅": "james", "彼前": "1-peter", "約壹": "1-john",
    "猶": "jude", "啟": "revelation", "但": "daniel", "傳": "ecclesiastes", "尼": "nehemiah", "哈": "habakkuk",
}
FULL = {  # display names
    "詩": "詩篇", "約": "約翰福音", "太": "馬太福音", "路": "路加福音", "羅": "羅馬書", "弗": "以弗所書",
    "腓": "腓立比書", "西": "歌羅西書", "來": "希伯來書", "啟": "啟示錄", "賽": "以賽亞書", "民": "民數記",
    "猶": "猶大書", "林前": "哥林多前書", "林後": "哥林多後書", "加": "加拉太書", "提前": "提摩太前書",
    "彼前": "彼得前書", "雅": "雅各書", "約壹": "約翰一書", "亞": "撒迦利亞書", "哀": "耶利米哀歌",
    "撒上": "撒母耳記上", "創": "創世記", "出": "出埃及記", "申": "申命記", "傳": "傳道書", "可": "馬可福音", "徒": "使徒行傳", "書": "約書亞記", "帖前": "帖撒羅尼迦前書", "王上": "列王紀上",
}
USED = []           # every (ref) rendered, for the audit trail


def parse(ref):
    """'詩 23:1-3,5' -> (bookcode, chapter, [verse ints])  /  '詩 23' = whole chapter."""
    m = re.fullmatch(r"(\S+?)\s*(\d+)(?::([\d,\-]+))?", ref.strip())
    if not m:
        raise ValueError(ref)
    code, ch, spec = m.group(1), int(m.group(2)), m.group(3)
    key = f"{BOOKS[code]}-{ch}"
    chap = cuv[key]
    if spec is None:
        vs = sorted(int(v) for v in chap)
    else:
        vs = []
        for part in spec.split(","):
            if "-" in part:
                a, b = part.split("-")
                vs += list(range(int(a), int(b) + 1))
            else:
                vs.append(int(part))
    for v in vs:
        if str(v) not in chap:
            raise KeyError(f"{ref}: verse {v} missing in {key}")
    return code, ch, vs, chap


def label(ref):
    code, ch, vs, _ = parse(ref)
    spec = ref.split(":", 1)[1] if ":" in ref else None
    name = FULL.get(code, code)
    return f"{name} {ch}:{spec}" if spec else f"{name} {ch}"


AIEDEN_DIR = os.path.join(HERE, ".sources", "aieden")


def nasb_chapter(book, ch):
    f = os.path.join(AIEDEN_DIR, f"{book}-{ch}.json")
    if not os.path.exists(f):
        raise FileNotFoundError(f"NASB cache missing: {f} (run .sources/fetch_aieden.py)")
    return {v["verse"]: v["text"].strip() for v in json.load(open(f, encoding="utf-8"))["data"]["verses"]}


def nasb_block(ref, numbered=True):
    """NASB 1995 as served by ai-eden.com's /api/bible (cached by .sources/fetch_aieden.py).
    Brackets mark NASB's italic supplied words; typeset them as italics."""
    code, ch, vs, _ = parse(ref)
    verses = nasb_chapter(BOOKS[code], ch)
    paras, cur, prev = [], [], None
    for v in vs:
        txt = re.sub(r"\[([^\]]+)\]", r"*\1*", verses[v])
        if prev is not None and v != prev + 1:
            paras.append(" ".join(cur)); cur = []
        cur.append(f"\\textsuperscript{{{v}}}{{}}{txt}" if numbered else txt)
        prev = v
    paras.append(" ".join(cur))
    return "\n>\n".join("> " + p for p in paras) + "\n>\n> — NASB 1995\n"


def cuv_placeholder(s):
    s = s.strip()
    return len(s) <= 2 or "併入" in s or "合和譯本" in s


def scripture(ref, cite=True, numbered=True, english=True):
    """Verbatim CUV as a blockquote.  Gaps between ranges get a ⋯ marker."""
    code, ch, vs, chap = parse(ref)
    USED.append(ref)
    lines, prev, skipped = [], None, False
    for v in vs:
        if cuv_placeholder(chap[str(v)]):
            skipped = True
            continue
        if prev is not None and v != prev + 1:
            lines.append("⋯")
        txt = chap[str(v)].strip()
        lines.append(f"\\textsuperscript{{{v}}}{{}}{txt}" if numbered else txt)
        prev = v
    body = "\n".join(l if l == "⋯" else l for l in lines)
    # one paragraph, verse numbers inline; gaps start a new paragraph
    paras, cur = [], []
    for l in lines:
        if l == "⋯":
            paras.append(" ".join(cur)); cur = []
        else:
            cur.append(l)
    paras.append(" ".join(cur))
    out = "\n>\n".join("> " + p for p in paras)
    if skipped:
        out += "\n>\n> *（和合本此處有節號併入前後節，從略。）*"
    if cite:
        out += f"\n>\n> — {label(ref)}（和合本）"
    out += "\n"
    if english:
        out += "\n" + nasb_block(ref, numbered)
    return out


def inline(ref):
    """Short verbatim quotation, no verse numbers, for use inside prose."""
    code, ch, vs, chap = parse(ref)
    USED.append(ref)
    return "".join(chap[str(v)].strip() for v in vs)


# ------------------------------------------------------------------- hymns
ALIASES = {
    "rockofagescleftforme": ["rockofages"],
    "ogodourhelpinagespast": ["ourgodourhelpinagespast"],
    "justasiamwithoutoneplea": ["justasiam"],
    "andcanitbethatishouldgain": ["andcanitbe"],
}
DIRFIX = lambda d: re.sub(r"^gospel-of-john-.*$", "gospel-of-john", d)

best, uses, total_uses = {}, defaultdict(set), 0
pat = re.compile(r"^## (?:配詩|開篇詩歌|詩歌|聖詩|Opening Hymn)[^\n]*\n+((?:>[^\n]*\n?)+)", re.M)
for f in glob.glob(os.path.join(BIBLE, "**/*.md"), recursive=True):
    rel = os.path.relpath(f, BIBLE)
    if "/.sources/" in f or rel.startswith("hymnWorship"):
        continue
    t = open(f, encoding="utf-8", errors="ignore").read()
    for m in pat.finditer(t):
        blk = m.group(1)
        mt = re.match(r">\s*\*\*([^*\n]+)\*\*", blk)
        if not mt:
            continue
        key = re.sub(r"[^a-z]", "", mt.group(1).lower())
        total_uses += 1
        uses[key].add(DIRFIX(rel.split("/")[0]))
        if key not in best or len(blk) > len(best[key][0]):
            best[key] = (blk, mt.group(1).strip(), rel)


def n_books(key):
    # same hymn under spelling/title variants: group every key sharing the first 11 letters
    s = set()
    for k2, v in uses.items():
        if k2[:11] == key[:11]:
            s |= v
    return len(s)


def hymn_body(key):
    blk, title, rel = best[key]
    lines = blk.rstrip("\n").split("\n")
    body = "\n".join(lines[1:])          # drop the bold title line; heading carries it
    body = body.replace("祢", "你").replace("裡", "裏")
    # `\` at line end is a hard break in the source; keep as is.
    return body.rstrip() + "\n", title, rel


HN_DIR = os.path.join(HERE, ".sources", "hymns_hn")
try:
    CAL = json.load(open(os.path.join(HN_DIR, "calibration.json"), encoding="utf-8"))
except OSError:
    CAL = {}


OVERRIDES = {"amazinggrace": [("wretch; like me", "wretch like me")]}


def full_text(key):
    """Full English text from hymnal.net, only for hymns whose already-verified
    stanzas matched the fetched text (calibration.json ok).  Else None."""
    if not CAL.get(key, {}).get("ok"):
        return None
    d = json.load(open(os.path.join(HN_DIR, key + ".json"), encoding="utf-8"))
    out = []
    for s in d["stanzas"]:
        body = " \\\n> ".join(s["text"].split("\n"))
        out.append(("> **副歌 Refrain** \\\n> " if s["type"] == "chorus" else "> ") + body)
    txt = "\n>\n".join(out) + "\n"
    for a, b in OVERRIDES.get(key, []):
        assert a in txt, (key, a)
        txt = txt.replace(a, b)
    return txt, d["url"]


# theme -> list of (hymn key, Chinese heading, paired scripture)
HYMNS = [
    ("讚美與敬拜 (Adoration)", "把榮耀歸給那位本來就配得的——先仰望祂是誰，再談我們要甚麼。", [
        ("holyholyholylordgodalmighty", "聖哉！聖哉！聖哉！", "啟 4:8-11"),
        ("immortalinvisiblegodonlywise", "不死、不見、獨一全智的神", "提前 1:17"),
        ("praisetothelordthealmighty", "讚美全能的主", "詩 103:1-5"),
        ("ogodourhelpinagespast", "神是我們歷代的保障", "詩 90:1-4"),
        ("amightyfortressisourgod", "堅固保障是我神", "詩 46:1-3"),
        ("comethoufountofeveryblessing", "恩泉的源頭", "撒上 7:12"),
        ("crownhimwithmanycrowns", "以許多冠冕為祂加冕", "啟 19:12,16"),
        ("jesusshallreignwhereerthesun", "耶穌必作王", "詩 72:8,11,17"),
    ]),
    ("道成肉身與基督的降臨", "道成了肉身；那來過的，必要再來。", [
        ("ofthefatherslovebegotten", "聖父愛子，太初所生", "約 1:1,14"),
        ("lohecomeswithcloudsdescending", "看哪，祂駕雲降臨", "啟 1:7"),
    ]),
    ("十字架與救恩 (The Cross)", "十字架不是敬拜的裝飾，是敬拜的理由。", [
        ("whenisurveythewondrouscross", "當我默想奇妙十架", "加 6:14"),
        ("osacredheadnowwounded", "受傷流血的聖首", "賽 53:3-5"),
        ("rockofagescleftforme", "萬古磐石為我開", "出 33:22"),
        ("thereisafountainfilledwithblood", "有一泉源充滿血", "亞 13:1"),
        ("andcanitbethatishouldgain", "我竟得分於救主之血", "羅 8:1"),
        ("amazinggrace", "奇異恩典", "弗 2:8-9"),
        ("justasiamwithoutoneplea", "照我本相", "約 6:37"),
        ("jesuspaiditall", "耶穌已經付清", "西 2:13-14"),
    ]),
    ("復活 (The Resurrection)", "空墳墓是基督徒敬拜的主日的由來。", [
        ("christthelordisrisentoday", "基督今日已復活", "林前 15:55-57"),
    ]),
    ("聖言 (The Word)", "先聽神說話，再開口回應。", [
        ("breakthouthebreadoflife", "求主擘開生命的糧", "約 6:35"),
        ("owordofgodincarnate", "道成肉身的神的話", "來 4:12"),
        ("spiritofgoddescenduponmyheart", "神的靈，求降在我心", "約 16:13"),
    ]),
    ("禱告 (Prayer)", "禱告是與神交談；這幾首詩教我們說甚麼。", [
        ("sweethourofprayer", "祈禱的時刻何等甘甜", "腓 4:6-7"),
        ("whatafriendwehaveinjesus", "我們有何等良友", "彼前 5:7"),
        ("nearermygodtothee", "更近我主", "詩 73:28"),
        ("abidewithme", "求主同住", "路 24:29"),
    ]),
    ("信靠、安慰與引導 (Trust)", "這一組的詩，多與患難、安慰和引導有關。", [
        ("bestillmysoul", "我心哪，要安靜", "詩 46:10"),
        ("itiswellwithmysoul", "我心靈得安寧", "羅 5:1"),
        ("godmovesinamysteriousway", "神行事奇妙", "羅 8:28"),
        ("howfirmafoundation", "信徒根基穩固", "賽 41:10"),
        ("greatisthyfaithfulness", "你的信實廣大", "哀 3:22-23"),
        ("guidemeothougreatjehovah", "求引導我，大耶和華", "詩 25:4-5"),
        ("saviorlikeashepherdleadus", "救主如牧者引導我們", "詩 23"),
        ("bethoumyvision", "願你是我異象", "詩 73:25-26"),
        ("olovethatwiltnotletmego", "愛，你不放我走", "詩 36:7-9"),
        ("leadkindlylight", "引領我，慈光", "詩 43:3"),
    ]),
    ("奉獻與跟隨 (Consecration)", "敬拜的最後一步，是把自己放在祭壇上。", [
        ("takemylifeandletitbe", "求主取我生命", "羅 12:1"),
        ("trustandobey", "信靠並順服", "約 14:15"),
        ("havethineownwaylord", "照你旨意行", "賽 64:8"),
        ("ojesusihavepromised", "主耶穌，我已許願", "約 12:26"),
        ("standupstandupforjesus", "為耶穌站立", "弗 6:10-13"),
    ]),
    ("教會與團契 (The Church)", "我們不是各自來敬拜，是作為一個身體來的。", [
        ("thechurchsonefoundation", "教會獨一的根基", "林前 3:11"),
        ("blestbethetiethatbinds", "愛主的心彼此相繫", "詩 133:1"),
        ("gloriousthingsoftheearespoken", "神的城啊，有榮耀的事", "詩 87:3"),
    ]),
    ("感恩 (Thanksgiving)", "凡事謝恩，是神在基督耶穌裏向你們所定的旨意。", [
        ("nowthankweallourgod", "現在我們都感謝神", "帖前 5:18"),
        ("comeyethankfulpeoplecome", "感恩的子民，來吧", "詩 65:9-13"),
    ]),
]
ALL = [h for _, _, hs in HYMNS for h in hs]
NUM = {h[0]: i + 1 for i, h in enumerate(ALL)}
TITLE = {}
for k, zh, _ in ALL:
    TITLE[k] = best[k][1]


def H(key):
    """Cross-reference text for a hymn: '聖詩 12 · When I Survey ...'"""
    return f"聖詩 {NUM[key]}《{TITLE[key]}》"


# ------------------------------------------------------------------ psalms
PSALMS = [
    ("讚美與敬拜", [
        (8, "人算甚麼——造物之榮與人的位分（來2:6-8 引用）。"),
        (19, "兩本書：天的見證，與律法的見證。"),
        (46, "「神是我們的避難所，是我們的力量。」"),
        (95, "宣召詩：來啊，我們要向耶和華歌唱；今天若聽祂的話，不可硬著心。"),
        (96, "向耶和華唱新歌。"),
        (98, "全地都要向耶和華歡呼。"),
        (100, "感恩的詩，也是進入聖殿的詩。"),
        (103, "「我的心哪，你要稱頌耶和華。」"),
        (145, "字母詩（各節大致依希伯來字母次序排列），全詩讚美王。"),
        (148, "天上、地上一切受造之物，一同讚美。"),
        (150, "全卷詩篇的結尾：凡有氣息的，都要讚美耶和華。"),
    ]),
    ("認罪與悔改", [
        (32, "「得赦免其過、遮蓋其罪的，這人是有福的。」（羅4:7-8 引用）"),
        (51, "悔改詩；標題記為先知拿單指責大衛與拔示巴之事後所作。"),
        (130, "深處的呼求：「但在你有赦免之恩，要叫人敬畏你。」"),
    ]),
    ("患難、信靠與安息", [
        (13, "「要到幾時呢」——哀求如何轉為歌唱。"),
        (16, "「不將我的靈魂撇在陰間」（16:10，徒2:27 引用）。"),
        (23, "牧者的詩。"),
        (27, "「耶和華是我的亮光，是我的拯救。」"),
        (42, "鹿渴慕溪水，人渴慕神。"),
        (62, "默默無聲，等候神。"),
        (63, "標題記為大衛在猶大曠野時所作；詩中說「我要切切地尋求你」。"),
        (84, "渴慕神的居所。"),
        (90, "摩西的祈禱：求你指教我們怎樣數算自己的日子。"),
        (91, "在至高者的隱密處。"),
        (121, "上行之詩：「我要向山舉目。」"),
        (131, "如斷過奶的孩子，在母親懷中。"),
        (139, "「耶和華啊，你已經鑒察我，認識我。」"),
    ]),
    ("感恩與盼望", [
        (67, "求神賜福，使萬國都認識祂的救恩。"),
        (116, "「我拿甚麼報答耶和華向我所賜的一切厚恩？」"),
        (118, "「這是耶和華所定的日子」；匠人所棄的石頭（太21:42 引用）。"),
        (133, "弟兄和睦同居。"),
        (134, "夜間站在耶和華殿中的僕人，彼此祝福。"),
    ]),
    ("聖言與彌賽亞", [
        (1, "兩條路：愛耶和華律法的人，與惡人的道路。"),
        (2, "受膏者與列邦：「你是我的兒子」（2:7，來1:5 引用）。"),
        (22, "耶穌在十字架上引用的一句（太27:46；可15:34）。"),
        (110, "「你坐在我的右邊」（太22:44 引用）。"),
    ]),
]
PSALM_SET = {n for _, ps in PSALMS for n, _ in ps}


# ------------------------------------------------------------ enrichment data
SEE_JESUS = {  # psalm -> (one line, [NT / cross refs]); the kind label (引用/呼應/傳統) is assigned by CITED / TRADITION below
    1: ("本篇的「福人」，在新約裏最完整的實現是耶穌：祂用「經上記著」回答試探（太4:4引的是申命記8:3，不是本篇）。", ["太 4:4"]),
    2: ("「你是我的兒子」，新約兩次引用這一句：一次說基督的身分，一次說祂的復活。", ["來 1:5", "徒 13:33"]),
    8: ("詩人問「人算甚麼」；希伯來書引用這篇，然後說：現在還沒有看見萬物都服祂，只看見耶穌。", ["來 2:6-9"]),
    13: ("等候中的人不是孤單的：我們的大祭司能體恤我們的軟弱。", ["來 4:15"]),
    16: ("彼得在五旬節講道，把「不叫你的聖者見朽壞」指向基督的復活。", ["徒 2:25-31", "徒 13:35"]),
    19: ("羅馬書引用 19:4 說福音的傳揚；希伯來書雖未引用本篇，卻說神在這末世是藉著祂的兒子曉諭我們。", ["羅 10:18", "來 1:1-2"]),
    22: ("首句是耶穌在十字架上的呼喊；分衣、「傳揚你的名」，福音書與希伯來書都指向祂。", ["太 27:46", "約 19:24", "來 2:12"]),
    23: ("「耶和華是我的牧者」，耶穌說：「我是好牧人。」", ["約 10:11", "來 13:20"]),
    27: ("詩人說耶和華是我的亮光；耶穌說：「我是世界的光。」", ["約 8:12"]),
    32: ("保羅用這篇說明：不被算為有罪，是因信，不是因行為。", ["羅 4:6-8"]),
    42: ("詩人渴想活神；耶穌說：「人若渴了，可以到我這裏來喝。」", ["約 7:37", "約 4:14"]),
    46: ("「萬軍之耶和華與我們同在」與「以馬內利」是同一個應許；馬太引用的是以賽亞書7:14，沒有引用本篇。", ["太 1:23"]),
    51: ("認罪詩的盼望在於潔淨；新約說，神兒子耶穌的血洗淨我們一切的罪。", ["約壹 1:7", "弗 1:7"]),
    62: ("「默默無聲，專心等候神」；耶穌邀請勞苦擔重擔的人到祂這裏得安息。", ["太 11:28-29"]),
    63: ("詩人說「我的心渴想你」；耶穌說：「到我這裏來的，必定不餓。」", ["約 6:35"]),
    67: ("「使萬國都得知你的救恩」，這個盼望在大使命裏有了具體的差遣。", ["太 28:19-20"]),
    84: ("詩人渴慕神的居所；約翰福音說，耶穌所說的殿，就是祂的身體（約翰沒有引用本篇）。", ["約 2:19-21"]),
    90: ("摩西說神是歷代的居所；耶穌說，愛祂的人，父與祂要與他同住（沒有引用本篇）。", ["約 14:23"]),
    91: ("撒但曾引用這篇（91:11-12）試探耶穌；耶穌答：不可試探主你的神。這篇的應許不是拿來試探神的。", ["路 4:9-12"]),
    95: ("希伯來書花了兩章，從「今天若聽他的話」講進神所應許的安息。", ["來 3:7-11", "來 4:1-11"]),
    96: ("「向耶和華唱新歌」；啟示錄裏也有「新歌」，是向被殺的羔羊唱的（啟示錄沒有點明引用本篇）。", ["啟 5:9"]),
    98: ("「耶和華顯明了他的救恩」；西面抱著嬰孩耶穌說：我的眼睛已經看見你的救恩（路加沒有點明引用本篇）。", ["路 2:30-32"]),
    100: ("「你們當進他的門」；耶穌說：「我就是門，凡從我進來的，必然得救。」", ["約 10:9"]),
    103: ("「他赦免你的一切罪孽」；耶穌對癱子說「你的罪赦了」，並顯明祂有這權柄。", ["可 2:5-10"]),
    110: ("耶穌用這篇向法利賽人發問；新約說，祂已經坐在神的右邊，作永遠的祭司。", ["太 22:41-46", "徒 2:34-36", "來 5:6"]),
    116: ("福音書記載，耶穌與門徒吃完逾越節的筵席，「唱了詩，就出來」；新約沒有點名是哪一篇，傳統認為所唱的是逾越節的讚美詩（詩113-118）。", ["太 26:30"]),
    118: ("「匠人所棄的石頭」，耶穌親自引用，指自己；進城時群眾喊的「奉主名來的」也出自這篇。", ["太 21:9", "太 21:42", "徒 4:11"]),
    121: ("「他必保護你」；耶穌說，我的羊「誰也不能從我手裏把他們奪去」。", ["約 10:28"]),
    130: ("「但在你有赦免之恩」；新約說，我們藉著基督的血得蒙救贖，過犯得以赦免。", ["弗 1:7", "約壹 1:9"]),
    131: ("「如同斷過奶的孩子」；耶穌說，人若不回轉變成小孩子的樣式，斷不能進天國。", ["太 18:3-4"]),
    133: ("弟兄和睦同居；耶穌臨別禱告，求父使信祂的人都合而為一。", ["約 17:21-23"]),
    134: ("夜間站在耶和華殿中的人；耶穌也曾整夜禱告（兩處並非同一件事，只是一個對照）。", ["路 6:12"]),
    139: ("「你已經鑒察我」；約翰說耶穌認識萬人，不需要誰見證人怎樣，因祂知道人心裏所存的。", ["約 2:24-25"]),
    145: ("「你的國是永遠的國」；復活的主說：「天上地下所有的權柄都賜給我了。」", ["太 28:18"]),
    148: ("天上地上萬物都要讚美；歌羅西書說，萬有都是藉著祂造的，也靠祂而立。", ["西 1:16-17"]),
    150: ("全卷詩篇的結尾「凡有氣息的」；啟示錄裏，天上地下一切受造之物向坐寶座的和羔羊歌唱。", ["啟 5:11-13"]),
}
CITED = {2, 8, 16, 19, 22, 32, 91, 95, 110, 118}   # the NT text itself quotes or names the psalm
TRADITION = {116}                                    # the NT names no psalm; church tradition does
assert set(SEE_JESUS) == {n for _, ps in PSALMS for n, _ in ps}, set(SEE_JESUS) ^ {n for _, ps in PSALMS for n, _ in ps}

HQ = {  # hymn key -> meditation question (editor-written; questions only, no attributed speech)
    "holyholyholylordgodalmighty": "歌詞把「聖哉」說了三遍。你上一次單單站在祂的聖潔面前、甚麼也不求，是甚麼時候？",
    "immortalinvisiblegodonlywise": "「不死、不見」——祂既然看不見，你靠甚麼認識祂？這個答案，是你的經驗，還是祂的話？",
    "praisetothelordthealmighty": "這首詩呼召「我的靈魂」一同讚美（配經詩103也是對自己的心說話）。你今天的心，需要你對它說一句甚麼？",
    "ogodourhelpinagespast": "歷代的保障——想一件你的家族或教會過去被保守的事。它怎樣改變你今天對將來的看法？",
    "amightyfortressisourgod": "堅固保障不表示沒有仇敵。你現在面對的最大的「仇敵」，是人、處境，還是自己的恐懼？",
    "comethoufountofeveryblessing": "歌詞說「在此立下我的以便以謝」。撒母耳立這塊石頭，是為了記念「到如今耶和華都幫助我們」（撒上7:12）。你今天要為哪一件事立一塊石頭？",
    "crownhimwithmanycrowns": "為祂戴上許多冠冕——你生命裏有哪一個冠冕，還戴在別的東西頭上？",
    "jesusshallreignwhereerthesun": "「必作王」既是將來，也是今天。你生活中哪一個領域，還沒有讓祂作王？",
    "ofthefatherslovebegotten": "這首詩從「父的愛」開始，不是從「人的需要」開始。你的禱告，通常從哪裏開始？",
    "lohecomeswithcloudsdescending": "「看哪，祂駕雲降臨。」若今天就是那一天，你最想先對祂說的一句話是甚麼？",
    "whenisurveythewondrouscross": "歌詞把「最寶貴的得著」都算作虧損，把驕傲看為無有。你最寶貴的得著，是甚麼？",
    "osacredheadnowwounded": "這首詩停在那受傷的頭面前。你能不能單單看著，不急著解釋，停五分鐘？",
    "rockofagescleftforme": "歌詞說「我手裏一無所有」。你到神面前，是不是手裏還握著一點自己的功勞？",
    "thereisafountainfilledwithblood": "泉源是現在式。你上一次讓祂潔淨的，是哪一件具體的事？",
    "andcanitbethatishouldgain": "歌詞在確據與驚嘆之間來回：「現在不再有定罪」，卻仍問「怎能有這事」。你的確據，容得下驚嘆嗎？",
    "amazinggrace": "「何等甘甜」——恩典對你還甘甜嗎？還是已經成了一個熟悉的字？",
    "justasiamwithoutoneplea": "「照我本相」——你向神修飾過的那個樣子，今天可以不修飾地帶來嗎？",
    "jesuspaiditall": "「已經付清」——你有沒有哪一筆，仍在自己偷偷地還？",
    "christthelordisrisentoday": "「哈利路亞」在每一行都出現。復活對你是一個教義，還是今天早上起床的理由？",
    "breakthouthebreadoflife": "你最近讀經，是在吃，還是在檢查？",
    "owordofgodincarnate": "你今天讀的那一段經文，有沒有把你帶到那位「道成肉身」的面前？",
    "spiritofgoddescenduponmyheart": "你今天要聖靈改變你的哪一個「自然反應」？",
    "sweethourofprayer": "你一天裏有沒有一段時間，是別人找不到你的？",
    "whatafriendwehaveinjesus": "你有沒有把今天最小的一件煩惱，也帶到祂面前？",
    "nearermygodtothee": "「更近」常常從不舒服的地方開始。你現在被帶到了哪一個不舒服的地方？",
    "abidewithme": "天晚了。你願意讓祂進到你一天裏最亂的那個房間嗎？",
    "bestillmysoul": "你對自己的心說話，用的是甚麼口氣——責備，還是這首詩裏的口氣？",
    "itiswellwithmysoul": "你的「安寧」，是靠情況好轉，還是靠十字架上的那件事？",
    "godmovesinamysteriousway": "哪一件今天看來是烏雲的事，你願意先不下結論？",
    "howfirmafoundation": "歌詞問：祂已經對你說的，還要再說甚麼？你還在等祂多說一句甚麼？",
    "greatisthyfaithfulness": "信實是「每個早晨」的事。你昨天早上，記得祂的哪一樣恩惠？",
    "guidemeothougreatjehovah": "歌詞求祂引導「我一生的旅程」。你今天把哪一段交給祂帶領，哪一段還自己握著？",
    "saviorlikeashepherdleadus": "歌詞求牧人「領我」。你今天是在跟著祂走，還是自己找草場？",
    "bethoumyvision": "「願你是我異象」——你每天「看」得最多的是甚麼？",
    "olovethatwiltnotletmego": "有一個愛，是你逃不掉的。你現在是在逃，還是在歇息？",
    "leadkindlylight": "歌詞說「我不求看見遠景，一步已足」。你現在在求的，是遠景，還是下一步？",
    "takemylifeandletitbe": "歌詞把生命一項一項獻上：手、腳、聲音、時間、金銀。你今天只獻上其中哪一項？",
    "trustandobey": "信靠與順服，是同一件事的兩面。你這一週，哪一面比較弱？",
    "havethineownwaylord": "陶匠在泥上動手。你今天最不願意被捏的，是哪一處？",
    "ojesusihavepromised": "最近一次你兌現對祂的許諾，是甚麼時候？",
    "standupstandupforjesus": "這個星期，你在哪一個場合沉默了，而你知道該說一句話？",
    "thechurchsonefoundation": "你對教會的失望，是對「人」，還是對「根基」？",
    "blestbethetiethatbinds": "有哪一位弟兄姊妹，今天你可以用一句話、一通電話與他相繫？",
    "gloriousthingsoftheearespoken": "你怎樣看你所在的教會——一個活動，還是神的城？",
    "nowthankweallourgod": "感謝為甚麼不等事情好了再說？「現在」這兩個字，對你意味著甚麼？",
    "comeyethankfulpeoplecome": "收割有時候。今年你種下的，哪一樣快要收了？",
}
assert set(HQ) == {k for k, _, _ in ALL}, set(HQ) ^ {k for k, _, _ in ALL}

SITUATIONS = [  # (situation, [psalms in this book], [hymn keys])
    ("焦慮、擔憂", [23, 27, 131], ["whatafriendwehaveinjesus", "bestillmysoul", "itiswellwithmysoul", "leadkindlylight"]),
    ("罪疚、需要悔改", [32, 51, 130], ["rockofagescleftforme", "justasiamwithoutoneplea", "thereisafountainfilledwithblood", "andcanitbethatishouldgain"]),
    ("疲乏、軟弱", [62, 63, 121], ["abidewithme", "nearermygodtothee", "howfirmafoundation"]),
    ("病痛、困苦", [13, 42, 91], ["godmovesinamysteriousway", "bestillmysoul", "abidewithme"]),
    ("孤單、被離棄", [22, 27, 139], ["saviorlikeashepherdleadus", "olovethatwiltnotletmego"]),
    ("喪慟、送別", [23, 90, 121], ["itiswellwithmysoul", "abidewithme", "ogodourhelpinagespast"]),
    ("需要引導、作決定", [16, 121, 139], ["guidemeothougreatjehovah", "leadkindlylight", "bethoumyvision"]),
    ("爭戰、面對仇敵", [27, 46, 91], ["amightyfortressisourgod", "standupstandupforjesus", "howfirmafoundation"]),
    ("盼望、等候", [13, 62, 130], ["lohecomeswithcloudsdescending", "christthelordisrisentoday", "greatisthyfaithfulness"]),
    ("感恩", [100, 103, 116, 118, 145], ["nowthankweallourgod", "comeyethankfulpeoplecome", "praisetothelordthealmighty"]),
    ("敬拜、讚美", [95, 96, 98, 150], ["holyholyholylordgodalmighty", "immortalinvisiblegodonlywise", "crownhimwithmanycrowns"]),
    ("渴慕神的話", [1, 19], ["breakthouthebreadoflife", "owordofgodincarnate"]),
    ("教會、合一", [133, 134], ["thechurchsonefoundation", "blestbethetiethatbinds", "gloriousthingsoftheearespoken"]),
    ("奉獻、決志跟隨", [116, 139], ["takemylifeandletitbe", "havethineownwaylord", "trustandobey"]),
]
for _s, _ps, _hs in SITUATIONS:
    assert set(_ps) <= PSALM_SET and all(h in NUM for h in _hs), _s

SPECIAL = [  # (occasion, [scripture refs], [hymn keys], note)
    ("病中探訪", ["雅 5:14-15", "太 11:28-30", "林後 12:9"], ["abidewithme", "bestillmysoul"], "探訪者先聽，再讀。不要急著解釋病的原因，雅各書說的是禱告與膏抹。"),
    ("喪慟與安息禮拜", ["約 11:25-26", "帖前 4:13-14", "啟 21:3-4"], ["itiswellwithmysoul", "ogodourhelpinagespast"], "可配詩篇 23、90、121（卷四）。不要用空洞的話安慰，用經文安慰。"),
    ("婚禮", ["創 2:24", "林前 13:4-7", "傳 4:9-12"], ["blestbethetiethatbinds", "nowthankweallourgod"], "新人與會眾一同聆聽，然後由主婚者代禱，求神祝福。"),
    ("嬰孩奉獻", ["詩 127:3", "可 10:13-16", "申 6:5-7"], ["guidemeothougreatjehovah"], "奉獻的是父母的託付：把孩子交在神手中，並承諾在家中教導。"),
    ("洗禮", ["羅 6:3-4", "太 28:19-20", "加 3:26-27"], ["amazinggrace", "christthelordisrisentoday"], "受洗者作見證，會眾同聲唱詩，歡迎他進入神的家。"),
    ("新年與生日", ["詩 90:12", "哀 3:22-23", "詩 121:7-8"], ["greatisthyfaithfulness", "comethoufountofeveryblessing"], "數算日子，也數算恩典。可以請每個人說一件今年要記念的恩典。"),
    ("受差遣與離別", ["太 28:19-20", "民 6:24-26", "猶 1:24-25"], ["standupstandupforjesus", "takemylifeandletitbe"], "按手代禱，把差遣的人交在神手中。"),
]
for _o, _rs, _hs, _n in SPECIAL:
    for _r in _rs: parse(_r)
    assert all(h in NUM for h in _hs), _o

def closing(ref, line):
    return "**你看見耶穌了嗎？** " + line + "\n\n> " + inline(ref) + "（" + label(ref) + "）\n"

# --------------------------------------------------------------- the book
out = []
w = out.append


def vol(title, intro=None, step=None):
    w(f"# {title} {{.unnumbered}}\n")
    if intro:
        w(f"> {intro}\n")
    if step:
        w(f"> **啟示的次序·{step}**\n")
    w("\n\\newpage\n")


# ---- front matter ------------------------------------------------------
w("# 前言：這本手冊怎麼來的 {.unnumbered}\n")
w(f"""這本手冊不是新寫的詩歌集，是**整理**。三書精讀庫裏已經有數十卷書，每一章都以一首聖詩起頭、一篇詩篇回應、一段禱告收尾；ai-eden.com 的閱讀器也選了幾首公有領域的聖詩做配樂。把這些反覆被使用、而且已經逐字對過來源的材料收攏，編成一本能帶進晨更、主日和家庭祭壇的敬拜手冊，就是本書。

**經過甚麼驗證：**

- **聖詩**：統計庫中各卷 `配詩` 欄共 {total_uses} 處、{len(best)} 首不同的詩，本書依主題挑選其中公有領域的 {len(ALL)} 首（不是按使用次數的前 {len(ALL)} 名）。每首的歌詞**直接取自庫中已有的章節**（不重新打字），並保留原註明的作者、年份與底本；中譯若是編者試譯，作者行會直接寫明。每首附「見於本庫 N 個書目」：這首詩在庫中被選為配詩的書目數（同一詩的不同拼法已合併；列王紀上下、約翰一二三書等各算一個書目）。
- **經文**：全書的詩篇與經節，都從 ai-eden 的和合本資料（`data/cuv.json`）**逐節程式讀出**，不憑記憶抄寫；每段經文之後附英文 NASB 1995，取自同一網站的 `/api/bible`（每章快取一次，腳本見 `books/bible/hymnWorship/.sources/fetch_aieden.py`）。共 {{USED_COUNT}} 段不同的經文（不含行文中順帶提到的經節）。
- **禱告與導語**：各處的短禱、導語與使用說明，是本書編寫的，不歸給任何歷史人物；凡是引用聖經的禱告，經文照錄，標明出處。

**不收的：**仍在版權保護中的詩歌（所收聖詩皆為 1928 年前出版）。想唱的現代讚美詩，請按貴堂會的授權另行加入。

**為甚麼叫「照基督的心意」：**歌羅西書 3:16 說「用詩章、頌詞、靈歌」，以弗所書 5:19 說「口唱心和地讚美主」——本書也照這三個詞安排：**詩章**（詩篇，卷四）、**頌詞**（聖詩，卷五）、**靈歌**——聖靈感動、發自心裏的歌唱與禱告，貫穿在每日敬拜、主日程序與禱告各卷（卷二、三、六）。本書各部分的次序都照同一個原則，也是庫裏各書共用的骨幹：**神先開口，人才回應。**
""")
w("\n\\newpage\n")

w("# 怎麼用這本手冊 {.unnumbered}\n")
w(f"""| 你想要…… | 翻到 | 約需時間 |
|---|---|---|
| 每天早晚各花幾分鐘敬拜 | 卷二〈每日敬拜〉：一週七天，每天早晚各一篇詩篇、一首聖詩、一段短禱 | 每次 10-15 分鐘 |
| 預備主日聚會或小組敬拜 | 卷三〈主日敬拜程序〉：十一個環節，多數附經文與可以直接念的詞 | 約 60 分鐘 |
| 慢慢讀、慢慢禱一篇詩篇 | 卷四〈詩篇禱讀〉：{len(PSALM_SET)} 篇完整和合本詩篇，附一句導語 | 每篇 5-10 分鐘 |
| 選詩歌 | 卷五〈聖詩選〉：按主題排列，每首配一段經文 | — |
| 學習怎麼禱告 | 卷六〈禱告〉：主禱文逐句、四個方向、聖經裏的禱告 | — |
| 按教會年曆安排 | 附錄一〈教會年曆〉 | — |

**一個建議的次序**（晨更時）：安靜一分鐘 → 讀詩篇（出聲） → 唱或讀一首聖詩的歌詞 → 用詩篇的話禱告 → 一句話交託今天。

**詩篇怎麼讀：**讀出聲音。詩篇是寫來唱和念的，不是寫來默讀的。讀完一篇，挑一句話，用「我」來重念一遍，把它變成你自己的禱告。

**聖詩怎麼用：**書裏只印歌詞，不印曲譜（曲調請用貴堂會慣用的版本）。沒有曲子的時候，把歌詞當禱詞念，一樣有用。
""")
w("\n\\newpage\n")

# ---- 骨幹章 -----------------------------------------------------------
w("# 敬拜的次序：神先開口 {.unnumbered}\n")
w("> **全書座標**：本書每一卷的次序，都從這一章來——**召、說、答、差**。\n")
w("""問「我們可以獻上甚麼」，是從人這一邊問起。聖經裏的敬拜，通常是從另一邊開始的：神先動了，人才有可回應的東西。下面四個場景，次序都一樣。

---

## 一、以賽亞：先看見，才說話
""")
w(scripture("賽 6:1-8"))
w("""
以賽亞沒有計劃要敬拜。他先「見主坐在寶座上」（6:1），然後才說「禍哉」（6:5）；然後有一位撒拉弗拿炭沾他的口，說他的罪孽除掉了（6:6-7）；最後主問「我可以差遣誰呢」，他才回答「我在這裏，請差遣我」（6:8）。**每一步的起點，都在神那裏。**

| 人的軌跡 | 看見 | 承認 | 領受 | 回應 | 被差遣 |
|---|---|---|---|---|---|
| **神的次序** | 顯現 | 照出人的真相 | 潔淨 | 發問 | 差遣 |

本書的主日程序（卷三）有十一個環節，歸納成六個動作：宣召、讚美、認罪與赦免、聖言、回應、差遣；次序就是這個。

## 二、井邊的婦人：父要這樣的人拜祂

約翰福音 4:23-24 已經在卷一印出。這裏只補一件事：誰在做工？庫中約翰福音一書引老弟兄所引的 D.A. Carson：

> 「『用心靈和誠實敬拜』不是說敬拜必須是自發的、無結構的……真正的敬拜是三一神的工作：父尋找敬拜者，子啟示真理，靈使敬拜成為可能。」
> ——出處：老弟兄《生命之道——約翰福音》查經筆記，約翰福音四至五章（見庫中 `books/bible/gospel-of-john/04-samaritan-woman.md`〈敬拜線〉）。**這是中譯、轉引自老弟兄的筆記；Carson 原書頁碼待查。**

換句話說，敬拜的第一個動詞是**父要**（4:23），不是人要。

## 三、詩篇 95：召、跪、聽神說話

詩篇 95 全篇已收在卷四。它的結構本身就是一次敬拜：「來啊，我們要向耶和華歌唱」（1-2，**召**）；「因耶和華為大神」（3-5，**神是誰**）；「來啊，我們要屈身敬拜」（6，**跪**）；最後是：
""")
w(scripture("詩 95:7-8", cite=True))
w("""
7 節末句仍是詩人的呼籲：「惟願你們今天聽他的話。」從 8 節起，**神自己開口**，一直說到全篇結束（8-11）。所以這篇詩的次序是：召、神是誰、跪、然後聽神說話。**敬拜走到最後，是聽。**

## 四、啟示錄 5：天上的敬拜
""")
w(scripture("啟 5:11-13"))
w("""
天上的敬拜，中心是「曾被殺的羔羊」（5:12）。這就是敬拜的對象，也是敬拜的道路：我們不是靠自己的熱心進到寶座前，是靠羔羊。

---

## 三種常見的偏差

**一、以自己的感覺為中心。**問「今天唱得有沒有感動」，比問「神是不是被尊為聖」更多。主耶穌引用先知的話：
""")
w(scripture("太 15:8-9"))
w("""
這不是在說感動不重要，是說感動不能代替那位被敬拜的。

**二、只有熱情，沒有真理；或只有真理，沒有心靈。**「用心靈和誠實」是兩個一起，缺一不可（見卷一）。

**三、敬拜只剩下一個鐘頭。**羅馬書 12:1 說的「活祭」是整個生活（見卷一）。主日是整個星期的出發點，不是整個星期的全部。

## 本書的次序

| 卷 | 對應的環節 | 回答的問題 |
|---|---|---|
| 卷一 | 神召我們 | 為甚麼敬拜？怎樣的敬拜？ |
| 卷二 | 日復一日 | 一個人，每天怎樣走這個次序？ |
| 卷三 | 同聚一堂 | 教會一起，怎樣走這個次序？ |
| 卷四 | 神給的禱詞 | 開口沒詞的時候，用甚麼話？ |
| 卷五 | 用歌回應 | 歷代聖徒怎樣唱出回應？ |
| 卷六 | 與神說話 | 說話本身，怎樣學？ |

""")
w(closing("啟 5:12", "敬拜的全部次序，最後都指向同一位：被殺的羔羊。你今天的第一句敬拜，是對祂說的嗎？"))
w("\n\\newpage\n")

# ---- 卷一 --------------------------------------------------------------
vol("卷一 · 敬拜的根基 (Foundations)",
    "敬拜不是從我們獻上甚麼開始，而是神先說了話，我們才被帶到祂面前。",
    "第一步：神召我們——先有神的開口，才有人的敬拜。")
w("## 神要怎樣的敬拜\n")
w(scripture("約 4:23-24"))
w("""
耶穌這句話是對一個撒瑪利亞婦人說的，不是對祭司說的。**用心靈**，是敬拜出自裏面，不靠地點與儀式；**用誠實**（也可譯作「真理」），是照神所啟示的真相來敬拜，不是照自己喜歡的樣子。兩樣缺一不可：只有熱情沒有真理，容易變成自己的感覺；只有真理沒有心靈，容易變成冷冰冰的儀式。
""")
w("## 敬拜是整個人的獻上\n")
w(scripture("羅 12:1"))
w("""
「活祭」指的是平日的身體與生活，不只是主日的一個鐘頭。所以本書的聖詩有一整組放在「奉獻與跟隨」，用意就在這裏：唱完了，還要去活。
""")
w("## 詩章、頌詞、靈歌\n")
w(scripture("西 3:16"))
w(scripture("弗 5:18-20"))
w("""
這兩處經文給了敬拜三個要點：**基督的道理住在心裏**（先有神的話）、**彼此教導勸戒**（敬拜是會眾的事）、**感謝**（心態）。所以歌唱不只是向神，也是彼此對講。
""")
w("## 敬拜的六個環節\n")
w("""聖經裏許多關鍵的敬拜場景，次序都是這樣：**神召我們→神對我們說話→我們回應→神差我們出去。**以賽亞在異象裏見到主的榮耀（賽6:1-8），先是看見，然後說「禍哉」，然後蒙潔淨，最後才聽見「我可以差遣誰呢」而回答「我在這裏，請差遣我」。本書的主日程序（卷三）照這條線排：

| 環節 | 神做甚麼 | 我們做甚麼 | 本書用的詩篇 |
|---|---|---|---|
| 宣召 | 召我們來 | 靜默、聚集 | 詩 95、100 |
| 讚美 | 顯明祂是誰 | 歌唱、稱頌 | 詩 103、145、148-150 |
| 認罪與赦免 | 赦免、潔淨 | 承認、領受 | 詩 51、130 |
| 聖言 | 說話 | 聆聽 | 詩 19、119 |
| 回應 | 悅納 | 信仰告白、奉獻、代禱 | 詩 116 |
| 差遣 | 賜福、差遣 | 領受祝福、出去 | 民 6:24-26 |
""")
w(closing("約 4:26", "井邊的婦人問的是敬拜的地點；耶穌的回答，是把祂自己指給她。敬拜的對象不是一個觀念，是對你說話的那一位。"))
w("\n\\newpage\n")

# ---- 卷二 每日敬拜 ------------------------------------------------------
vol("卷二 · 每日敬拜 (Daily Worship)",
    "一週七天，每天早晚各一篇詩篇、一首聖詩、一段短禱。詩篇全文在卷四，聖詩歌詞在卷五。",
    "第二步：日復一日——把「召、說、答」縮成每天早晚的十分鐘。")
w("""**用法：**早晨與晚間各一個十來分鐘的時段就夠。先安靜，再讀詩篇（出聲），然後讀或唱聖詩，最後念短禱，再用自己的話加上今天的事。

下面每一天都有一個主題。**短禱是本書編寫的**，你可以改成自己的話。

---
""")
DAYS = [
    ("主日 · 復活的日子", 118, "christthelordisrisentoday", 150, "crownhimwithmanycrowns",
     "主啊，今天是你所定的日子。你從死裏復活，我們就有了可以聚集的理由。求你叫我們今天的歌唱，不是出於習慣，而是出於看見了你。",
     "主啊，你是活著的王。今天一整天，我領受的一切，都請你收納，歸給你的名。"),
    ("週一 · 創造與全能", 8, "immortalinvisiblegodonlywise", 139, "bethoumyvision",
     "主啊，你造了天，也造了我。新的一週，我不知道前面有甚麼，但你都知道。求你讓我記得，我是你手所造的，不是自己的主人。",
     "鑒察我的神，今天我有許多沒有說出口的事，都在你面前。求你光照，也求你保守。"),
    ("週二 · 神的話", 1, "breakthouthebreadoflife", 19, "owordofgodincarnate",
     "主啊，求你開我的眼睛，使我今天讀你的話，不只是讀字，也是遇見你。",
     "今天我聽見的許多話，有的是你的，有的不是。求你叫我分辨，叫你的話在我心裏站得住。"),
    ("週三 · 悔改與赦免", 51, "rockofagescleftforme", 32, "justasiamwithoutoneplea",
     "神啊，求你按你的慈愛憐恤我。我不用找藉口，我的罪在你面前是明明白白的。求你潔淨我，使我再次能歌唱。",
     "主啊，今天的過錯我都帶來了。我領受你的赦免，也求你教我，把這赦免分給虧欠我的人。"),
    ("週四 · 感恩", 103, "nowthankweallourgod", 116, "praisetothelordthealmighty",
     "我的心哪，你要稱頌耶和華，不可忘記祂的一切恩惠。主啊，今天我要數一數你給我的，不只數我缺的。",
     "主啊，我拿甚麼報答你？我只能舉起你給我的杯，向你說謝謝。"),
    ("週五 · 十字架", 22, "whenisurveythewondrouscross", 130, "osacredheadnowwounded",
     "主耶穌，你曾為我被離棄，所以我能來到你面前。今天我不求你解釋，只求你讓我再看一次十字架。",
     "主啊，我從深處向你呼求。你有赦免之恩，我就有盼望。求你讓這個盼望，陪我走進週末。"),
    ("週六 · 信靠與安息", 23, "saviorlikeashepherdleadus", 91, "abidewithme",
     "耶和華是我的牧者，我必不致缺乏。主啊，這一週我走得很累，求你領我到可安歇的水邊。",
     "主啊，天晚了，求你同住。我把今天的事、明天的事，都交在你手裏，我要平安躺下。"),
]
for dname, am_ps, am_h, pm_ps, pm_h, am_pr, pm_pr in DAYS:
    assert am_ps in PSALM_SET and pm_ps in PSALM_SET, (am_ps, pm_ps)
    w(f"## {dname}\n")
    w(f"**早晨**：詩篇 {am_ps} · {H(am_h)}\n")
    w(f"> {am_pr}\n")
    w(f"**晚間**：詩篇 {pm_ps} · {H(pm_h)}\n")
    w(f"> {pm_pr}\n")

w("## 簡式晨禱（十分鐘）\n")
w("""1. **靜默一分鐘。**不要先看手機。
2. **讀詩篇，出聲。**照上面的日表，或照下面的三十日循環。
3. **住。**挑一句，讓它停在你心裏，再讀三遍。
4. **唱，或讀一節聖詩。**
5. **禱。**把那一句改成「你」，說回給神。
6. **交託今天。**把今天的事，一件一件放在祂手裏。

老弟兄這樣說過：

> 「每天早上起床，把當天的主權交給神；晚上省察。這不是每週一次的宗教行為，是每天的生命操練。」
> ——出處：老弟兄語，見庫中《詩篇》〈禱告版〉（`books/bible/psalm/13-prayer-testimony.md`）
""")
w("## 簡式晚禱（十分鐘）\n")
w("""1. **回顧今天的經文。**早上那一句，今天用上了嗎？
2. **三個問題**：今天哪一刻，我看見了神？哪一刻，我忘了祂？有沒有需要向誰認罪，或向誰感謝？
3. **讀晚間詩篇。**
4. **短禱，然後安睡：**
""")
w(scripture("詩 4:8"))
w("## 家庭祭壇（十五分鐘）\n")
w("""適合一家人，或兩三個人：

1. **唱一節聖詩**，或一起念一遍。（兩分鐘）
2. **讀一小段經文**，由大人或孩子輪流。（三分鐘）
3. **各說一件感恩、一件代禱。**（五分鐘）
4. **同念主禱文**（太6:9-13，見卷六）。（兩分鐘）
5. **彼此祝福。**（三分鐘）
""")
w(scripture("詩 134:3"))
w("""
兩三個人奉主的名，詩篇就有了會眾。
""")
w("## 小組敬拜（三十分鐘）\n")
w("""| 時間 | 環節 | 做法 |
|---|---|---|
| 3 分鐘 | 靜默與宣召 | 一人念詩 95:1-7（或詩 100），眾人靜默一分鐘 |
| 8 分鐘 | 唱詩兩首 | 一首讚美、一首與當晚主題有關（見卷五主題） |
| 5 分鐘 | 詩篇啟應 | 照詩 150 的方式：單數節一邊念、雙數節另一邊念，末節全體同聲 |
| 3 分鐘 | 聽神的話 | 讀一段經文，每人說一句「這句話對我說甚麼」 |
| 8 分鐘 | 禱告 | 認罪、感恩、代禱各一輪；每人一兩句 |
| 3 分鐘 | 祝福 | 民 6:24-26 |
""")
w("## 三十日詩篇循環\n")
w("""古老而簡單的辦法：**每天五篇，隔三十取一**。第 N 天讀詩 N、N+30、N+60、N+90、N+120，三十天讀完全卷詩篇一遍。（此法見庫中《詩篇》附錄〈牧養索引與讀經計劃〉，`books/bible/psalm/99b-appendix-pastoral-index-reading-plan.md`；本表依該法排出。）

""")
rows = []
for d in range(1, 11):
    cells = []
    for k in (d, d + 10, d + 20):
        cells.append(f"| {k} | {', '.join(str(k + 30 * i) for i in range(5))} ")
    rows.append("".join(cells) + "|")
w("| 日 | 詩篇 | 日 | 詩篇 | 日 | 詩篇 |\n|---|---|---|---|---|---|\n" + "\n".join(rows) + "\n")
w(closing("可 1:35", "早晨的敬拜不是我們發明的；耶穌自己就是這樣開始一天的。你的早晨，是從誰開始的？"))
w("\n\\newpage\n")

# ---- 卷三 主日敬拜程序 ----------------------------------------------------
vol("卷三 · 主日敬拜程序 (The Lord's Day)",
    "十一個環節，次序是：神召我們、神說話、我們回應、神差遣。",
    "第三步：同聚一堂——召、說、答、差，教會一起走完一次。")
w("""以下是一份可以直接用的程序。**經文都是和合本**；「眾」表示會眾同念；「領」表示司會或領禱的人。可依貴堂會的習慣增減環節。聖詩編號指卷五。
""")
w("## 一、靜默預備\n")
w("""開始之前先安靜一分鐘。不要先排練，也不要先檢查設備。
""")
w(scripture("詩 46:10", numbered=False))
w("## 二、宣召\n")
w("領：來啊，我們要向耶和華歌唱。\n")
w(scripture("詩 95:1-7"))
w("## 三、讚美\n")
w(f"""會眾起立同唱。建議：{H('holyholyholylordgodalmighty')}，或 {H('praisetothelordthealmighty')}，或 {H('crownhimwithmanycrowns')}。

讚美的次序是先稱頌神是誰，再感謝神做了甚麼。選詩時可以先問：這首詩的主詞是神還是我？
""")
w("## 四、認罪\n")
w(scripture("詩 51:1-4,10"))
w("""
**同聲認罪禱告**（本書編寫，形式沿用教會常見的認罪禱告；可改用貴堂會慣用的）：

> 全能的神，你知道我們心裏的一切，沒有甚麼能向你隱藏。我們承認，我們沒有愛你勝過一切，也沒有愛人如己。我們在思想、言語和行為上得罪了你。求你按你的慈愛憐恤我們，赦免我們的過犯，使我們重新歸向你。奉主耶穌的名禱告。阿們。
""")
w("## 五、赦免的宣告\n")
w(scripture("詩 130:3-4"))
w(scripture("約壹 1:9"))
w("領：弟兄姊妹，這是神的話。我們在基督裏蒙了赦免。\n\n眾：**感謝神。**\n")
w("## 六、聖言\n")
w(scripture("詩 119:105"))
w(f"""
讀經與講道。講道前可以先念：「{inline("詩 119:18")}」（詩119:18）
""")
w("## 七、信仰告白：使徒信經\n")
w("""使徒信經是古代教會的洗禮信仰告白，不是聖經經文。以下依通行譯文，用字依本書體例（「神」）；各堂會的通行本措辭略有不同，請依貴堂會用的版本。

> 我信神，全能的父，創造天地的主。 \\
> 我信我主耶穌基督，神的獨生子， \\
> 因聖靈感孕，由童貞女馬利亞所生， \\
> 在本丟彼拉多手下受難，被釘於十字架，受死，埋葬， \\
> 下到陰間；第三天從死人中復活， \\
> 升天，坐在全能父神的右邊； \\
> 將來必從那裏降臨，審判活人死人。 \\
> 我信聖靈； \\
> 我信聖而公之教會，聖徒相通， \\
> 罪得赦免，身體復活，並且永生。阿們。
>
> I believe in God the Father Almighty, Maker of heaven and earth; \\
> and in Jesus Christ His only Son our Lord; \\
> who was conceived by the Holy Ghost, born of the Virgin Mary, \\
> suffered under Pontius Pilate, was crucified, dead, and buried; \\
> He descended into hell; the third day He rose again from the dead; \\
> He ascended into heaven, and sitteth on the right hand of God the Father Almighty; \\
> from thence He shall come to judge the quick and the dead. \\
> I believe in the Holy Ghost; the holy catholic Church; \\
> the communion of saints; the forgiveness of sins; \\
> the resurrection of the body; and the life everlasting. Amen.
""")
w("## 八、奉獻與感恩\n")
w(scripture("詩 116:12-14"))
w("""
奉獻時可以同念羅馬書 12:1（見卷一）。獻上的不只是金錢，也是這一週的時間、才幹與人際。
""")
w("## 九、代禱與主禱文\n")
w("""領禱者依次為：教會與弟兄姊妹、病患與有需要的人、家庭與下一代、本地與國家（提前2:1-2）、宣教與未信的親友。每一項之後，眾人可以靜默或加上一句「主啊，求你垂聽」。最後同念主禱文：
""")
w(scripture("太 6:9-13", numbered=False))
w("""
（逐句說明見卷六。）
""")
w("## 十、聖餐（若有）\n")
w(scripture("林前 11:23-26"))
w("""
領餐前宣讀。詩篇 34:8「你們要嘗嘗主恩的滋味」，常被用作領餐前的邀請。
""")
w("## 十一、差遣與祝福\n")
w(scripture("民 6:24-26"))
w(scripture("猶 1:24-25"))
w("""
領禱者舉手宣告，會眾低頭領受，然後出去。最後一首詩，可以選卷五〈奉獻與跟隨〉裏的一首。
""")
w("## 特別場合的讀經與聖詩\n")
w("""下面是常見場合的選讀。經文照和合本印出；聖詩編號見卷五。**司會可只選其中一兩段**，不必全讀。
""")
for _occ, _refs, _hs, _note in SPECIAL:
    w(f"### {_occ}\n")
    for _r in _refs:
        w(scripture(_r))
    w("**可唱**：" + "、".join(H(h) for h in _hs) + "\n")
    w(f"*{_note}*\n")
w(closing("路 24:31", "主日聚集，是為了在話語與擘餅中，眼睛被打開，認出祂來。你這個主日，是來完成一個程序，還是來認出一個人？"))
w("\n\\newpage\n")

# ---- 卷四 詩篇禱讀 -----------------------------------------------------
vol("卷四 · 詩篇禱讀 (The Psalter)",
    "詩章：和合本全文。讀出聲，挑一句，用「我」重念一遍。",
    "第四步：神給的禱詞——詩篇是神給我們的話，也是我們還給神的話。")
w("""## 詩篇禱讀四步

老弟兄說過：詩篇是耶穌自己禱告用的書——客西馬尼園唱的是它，十字架上斷氣前說的是它。（見庫中《詩篇》〈禱告版〉）你不會禱告，不要緊，先用別人的禱告禱告，直到它成為你自己的。方法有四步：

1. **念**：把一篇詩篇出聲慢慢讀一遍，讀到「細拉」就停一停。老弟兄的話：「先把這章一口氣讀完，不要停。」
2. **住**：回頭再讀，在哪一句心裏動了，就停在哪一句，把它再讀三遍。
3. **禱**：把經文的「他」改成「你」，說回給神。
4. **行**：從這篇帶走一句話，寫在便條上，今天遇事就用它回應；晚上用同一句省察。

（以上四步及兩句引語，出自庫中 `books/bible/psalm/13-prayer-testimony.md`；該章第四節另有老弟兄講過的兩件事，與詩 27、詩 91 有關，不在這裏重述。）

每一篇之下，有一句「看見耶穌」。**分三種，各自標明**：「新約引用」是新約經文自己引用或點名這篇詩；「主題呼應」是同一個主題在新約裏有對應，但新約沒有引用這篇詩，是編者列出的對照；「傳統」是教會傳統的說法。三者不是同一回事，請別混為一談。

---
""")
w(f"""以下 {len(PSALM_SET)} 篇詩篇依用途分五組。每篇的導語只有一句，是幫你找到入口，不是講解。想看更完整的逐篇研讀，請見庫裏《詩篇》一書。
""")
for grp, ps in PSALMS:
    w(f"## {grp}\n")
    for n, note in ps:
        w(f"### 詩篇 {n}\n")
        w(f"*{note}*\n")
        w(scripture(f"詩 {n}", cite=False))
        _line, _refs = SEE_JESUS[n]
        for _r in _refs:
            parse(_r)
        _kind = "新約引用" if n in CITED else ("傳統" if n in TRADITION else "主題呼應")
        w(f"**看見耶穌**（{_kind}）：{_line}（{'；'.join(label(r) for r in _refs)}）\n")
w(closing("路 24:44", "詩篇是寫到祂的書。你讀詩篇，要讀到祂；讀不到祂的那一遍，等於沒有讀完。"))
w("\n\\newpage\n")

# ---- 卷五 聖詩選 -------------------------------------------------------
vol("卷五 · 聖詩選 (Hymns)",
    f"頌詞：{len(ALL)} 首公有領域聖詩，按主題排列；每首配一段經文、一個默想問題。",
    "第五步：用歌回應——歷代聖徒的回應，借我們的口唱出來。")
w("""**怎麼讀這一卷：**歌詞原文取自庫裏已核對的章節；作者行保留了當時註明的作者、年份與底本。**本書的中文歌詞多為編者所譯（各首的標示方式不一，如「編者試譯」「中譯：編者」），不是教會通行的詩歌本譯文**，只供對照理解；要唱的時候，請用貴堂會的詩歌本。「見於本庫 N 個書目」是這首詩被庫中多少個書目選為配詩，數字越大，表示越經得起不同書卷的使用。
""")
for theme, tag, hs in HYMNS:
    w(f"## {theme}\n")
    w(f"*{tag}*\n")
    for key, zh, ref in hs:
        body, title, rel = hymn_body(key)
        n = NUM[key]
        w(f"### {n}. {title}（{zh}）\n")
        w(body)
        ft = full_text(key)
        if ft:
            w("**更多詩節 (English)**\n")
            w(ft[0])
        w(f"**配經**：{label(ref)}\n")
        w(scripture(ref, cite=False))
        w(f"**默想**：{HQ[key]}\n")
        cnt = n_books(key)
        w(f"*見於本庫 {cnt} 個書目的配詩。*\n")
w("\n\\newpage\n")

w("## 現代讚美詩曲目（不附歌詞）\n")
w(f"""現代詩歌仍在版權保護中，**本書只列曲目與對應經文，不印歌詞**。教會內部使用，也請以貴堂會的詩歌授權（如 CCLI）為準，並用投影或自己的詩歌本。下表前四首是庫中或常見的曲目，其餘空列供貴堂會自行補充。

| 曲名 | 作者／年份 | 主題 | 配經 | 接在聖詩 |
|---|---|---|---|---|
| In Christ Alone | Keith Getty、Stuart Townend，2001 | 十字架與復活 | 加 6:14 | {H('whenisurveythewondrouscross')} |
| How Great Is Our God | Chris Tomlin 等，2004 | 讚美 | 詩 145:3 | {H('immortalinvisiblegodonlywise')} |
| 10,000 Reasons (Bless the Lord) | Matt Redman、Jonas Myrin，2011 | 讚美 | 詩 103:1-5 | {H('praisetothelordthealmighty')} |
| Because He Lives | Gloria 與 William Gaither，1971 | 復活的盼望 | 林前 15:55-57 | {H('christthelordisrisentoday')} |
| | | | | |
| | | | | |
""")
w(closing("太 26:30", "十字架前夜，祂與門徒唱了詩。我們唱的每一首，都是在跟著祂唱。你唱的時候，想到的是旋律，還是祂？"))
w("\n\\newpage\n")

# ---- 卷六 禱告 ---------------------------------------------------------
vol("卷六 · 禱告 (Prayer)",
    "禱告是與神說話。這一卷不教技巧，只把聖經裏現成的禱告放在你面前。",
    "第六步：與神說話——最後落在禱告，也落在那位在父右邊代求的基督。")
w("## 主禱文逐句\n")
w(scripture("太 6:9-13", numbered=False))
w("""
主禱文是耶穌給門徒的範本（路11:1-4 另有記載）。順序值得注意：**先是神的事**（名、國、旨意），**然後才是我們的事**（飯食、饒恕、保守）。

| 句子 | 我們在說甚麼 | 可以這樣禱告 |
|---|---|---|
| 我們在天上的父 | 先認父，再開口；用「我們」，不是「我」 | 為你所屬的團契與弟兄姊妹開頭 |
| 願人都尊你的名為聖 | 求神的名在我身上、在世上被看為聖 | 為我今天的言行是否榮耀祂禱告 |
| 願你的國降臨 | 求祂的掌權臨到我的家、教會與地方 | 為一件你仍未交託的事禱告 |
| 願你的旨意行在地上，如同行在天上 | 求我順服，而不是求祂順我 | 把一個你不願放下的計劃交出去 |
| 我們日用的飲食，今日賜給我們 | 承認天天都靠祂 | 數算今天一個實在的供應 |
| 免我們的債，如同我們免了人的債 | 領受赦免，也施出赦免 | 想一個你需要饒恕的人 |
| 不叫我們遇見試探，救我們脫離兇惡 | 承認自己軟弱 | 說出你最容易跌倒的地方 |
| 因為國度、權柄、榮耀，全是你的 | 以頌讚收尾（和合本注明有古卷無此句） | 以感謝結束 |
""")
w("## 禱告的四個方向\n")
w("""常見的禱告架構把禱告分成四個方向：**讚美、認罪、感恩、祈求**（英文常以 ACTS 幫助記憶）。你不用每次四樣都做，但長期缺了哪一樣，禱告就容易變成單向的清單。以下每一樣都用聖經現成的話。
""")
w("### 一、讚美\n")
w(scripture("詩 103:1-5"))
w("### 二、認罪\n")
w(scripture("詩 51:10-12"))
w("### 三、感恩\n")
w(scripture("帖前 5:16-18"))
w("### 四、祈求\n")
w(scripture("腓 4:6-7"))
w("## 聖經裏的禱告\n")
w("以下是使徒們為教會所寫的禱告。你可以直接代入，把「你們」換成你要為之禱告的人的名字。\n")
w("### 為人的認識與力量\n")
w(scripture("弗 3:14-19"))
w("### 為人的愛心與果子\n")
w(scripture("腓 1:9-11"))
w("### 為人的靈命長進\n")
w(scripture("西 1:9-12"))
w("### 頌讚收尾\n")
w(scripture("弗 3:20-21"))
w("## 為各樣事禱告\n")
w("""下表是禱告時遇到特定處境，可以立刻翻到的經文。
""")
w("| 處境 | 經文 | 經文全文 |\n|---|---|---|")
SITU = [
    ("焦慮、擔憂", "彼前 5:7", None),
    ("罪疚、虧欠", "約壹 1:9", None),
    ("疲乏、重擔", "太 11:28-30", None),
    ("疾病", "雅 5:14-15", None),
    ("孤單、被撇棄", "詩 27:10", None),
    ("為政府與領袖", "提前 2:1-2", None),
    ("為福音與工人", "太 9:37-38", None),
    ("缺乏智慧", "雅 1:5", None),
]
for s, ref, _ in SITU:
    w(f"| {s} | {label(ref)} | {inline(ref)} |")
w("")
w(closing("羅 8:34", "你不知道怎麼禱告的時候，有一位已經在父的右邊替你說了。你的禱告，不是從零開始的。"))
w("\n\\newpage\n")

# ---- 附錄 -------------------------------------------------------------
vol("附錄 (Appendices)", "教會年曆、聖詩索引、來源與核對說明、處境索引。")
w("## 附錄一 · 教會年曆\n")
w("""教會年曆把耶穌的一生走成一年。下表的詩篇依庫裏《詩篇》一書〈禮儀使用指南〉所列的歷代通行主線；各宗派經課略有出入。聖詩一欄為本書編排的建議。詩篇若不在卷四，請翻聖經。
""")
w(f"""| 節期 | 主題 | 詩篇 | 聖詩 |
|---|---|---|---|
| 將臨期 | 等候君王 | 24、80、130 | {H('lohecomeswithcloudsdescending')} |
| 聖誕期 | 道成肉身 | 98、96、2 | {H('ofthefatherslovebegotten')} |
| 大齋期 | 悔改的四十天 | 6, 32, 38, 51, 102, 143 | {H('rockofagescleftforme')}、{H('justasiamwithoutoneplea')} |
| 受難週 | 十字架 | 22、31、69 | {H('whenisurveythewondrouscross')}、{H('osacredheadnowwounded')} |
| 復活節 | 空墳墓 | 16、118、30 | {H('christthelordisrisentoday')} |
| 升天日 | 坐在右邊 | 24、47、110 | {H('crownhimwithmanycrowns')}、{H('jesusshallreignwhereerthesun')} |
| 五旬節 | 聖靈降臨 | 104 | {H('spiritofgoddescenduponmyheart')} |
| 感恩節期 | 收割與數算 | 65、67、100、103 | {H('nowthankweallourgod')}、{H('comeyethankfulpeoplecome')} |
""")
w("\n## 附錄二 · 聖詩索引\n")
w("| 編號 | 曲名 | 主題 | 書目數 |\n|---|---|---|---|")
for theme, _, hs in HYMNS:
    short = theme.split(" (")[0]
    for key, zh, ref in hs:
        w(f"| {NUM[key]} | {TITLE[key]} | {short} | {n_books(key)} |")
w("")
w("\n## 附錄三 · 來源與核對說明\n")
w(f"""**這一節如實交代本書每一類材料怎麼來，以及哪些事沒有做。**

1. **聖詩歌詞**：逐字取自庫中章節的「配詩」欄（共 {total_uses} 處、{len(best)} 首），沒有重新打字。庫中各章節當時如何核對（Army and Navy Hymnal 1920、Cyber Hymnal、Wikisource 等），作者行已照錄。**本書沒有重新對照原始詩歌本**；若某首歌詞有疑問，以作者行所註明的底本為準。
2. **中文歌詞**：多為編者所譯，標示方式不一致（有「編者試譯」「中譯：編者」「編者直譯」，也有未標示者），一律視為非通行譯本。詩歌本裏的通行中譯版權各異，本書不收。
3. **經文**：全部由 ai-eden 的 `data/cuv.json`（和合本）逐節讀出，共 {{USED_COUNT}} 段不同的經文。程式在建置時會檢查每個節號是否存在，缺節即中止。**本書沒有另行對照紙本和合本**；和合本資料本身若有排印問題，會一併帶入。**英文 NASB 1995 取自 ai-eden.com 的 API**；建置前已把本書用到的 109 章、607 節抓回，並把網站回傳的中文與 `cuv.json` 逐節比對（0 處不同）——但兩者本來就是同一個網站的資料，**和合本另以 FHL 信望愛和合本（`unv`）逐節比對**：607 節中 542 節完全相同、24 節只差標點、41 節有字形差異。這 41 節的差異全屬 FHL 把 1919 年和合本現代化（的→地、麼→嗎、罷→吧、那→哪、阿→啊、他→它／牠／她等，ai-eden 保留 1919 原貌），或校注文字不同（「或作」「或譯」）；**唯一的真缺字是詩 46:4**：ai-eden 資料作「這河的分使」，FHL、cnbible.com 與庫裡其他書都作「這河的分汊使」，本書已在生成器裡補上「汊」，網站資料本身未改（腳本 `.sources/check_cuv_fhl.py`）。另把網站全本 31,101 節都對 FHL 掃過一遍，找出約 60 節疑似漏字（32 節有 cnbible.com 佐證），清單見 `docs/build-reports/ai-eden-cuv-dropped-chars-2026-11-01.md`；**本書所引經文只受詩 46:4 一處影響**。**英文 NASB 另以 biblehub.com（頁面標題 NASB 1995）逐節比對**：607 節中 529 節字母完全相同；27 節是 ai-eden 在詩篇第 1 節多放了標題（如 “A Psalm of David.”，biblehub 把標題另列）；51 節是 biblehub 頁面尾端多出的下一段標題或版權行；**內文有差異的 0 節**。比對只看字母，不比標點與大小寫（腳本 `.sources/check_nasb_biblehub.py`）。英文裏方括號標示的補充詞已改排成斜體。NASB 版權屬 The Lockman Foundation，本書為教會內部使用，公開發行前須確認授權。
4. **更多詩節**：{{FULL_N}} 首附有全詩（English），取自 hymnal.net（人工打字、按詩節分段），採用前先做校準：庫中已核對的英文詩節，必須與 hymnal.net 對應詩節的相似度達 0.97 以上，全部通過才採用。其餘 {{NOFULL_N}} 首沒有全詩：{{FAIL_N}} 首抓到了但校準未通過（版本不同，或庫中的節錄本來就是選句），{{MISS_N}} 首在 hymnal.net 沒有配對到可用頁面，**只印庫中已核對的節錄，不印全詩**。通過校準只證明版本與詩節吻合，**沒有逐字對照紙本詩歌本**；這些詩節是 hymnal.net 的版本，不一定包含該詩最常唱的全部詩節（例如 Amazing Grace 缺 “Through many dangers”，第四節是後人所加，不是 Newton 1779 的原文），用字也可能與上方節錄略有差異（如 thee／you、標點）。校準不比對標點。歌詞抓取腳本與校準結果在 `books/bible/hymnWorship/.sources/`。
5. **導語與短禱**：編寫的內容；除了第 9 項所列、已註明出處的老弟兄原話與 Carson 轉引外，沒有引用歷史人物的話。
6. **使徒信經**：依通行譯文，不是聖經經文，各堂會用字略有出入。
7. **ai-eden 閱讀器的配樂曲目**（Be Thou My Vision、Nearer, My God, to Thee、Just As I Am、Jesus Paid It All、Joy to the World）：前四首已收入本書（{H('bethoumyvision')}、{H('nearermygodtothee')}、{H('justasiamwithoutoneplea')}、{H('jesuspaiditall')}）。*Joy to the World* 在庫中沒有逐字核對過的歌詞，所以本書未收。
8. **曲譜**：本書不含曲譜。
9. **老弟兄的話**：本書引用的老弟兄原話，只有庫中既有檔案裏已有的（《詩篇》〈禱告版〉的兩句與一段方法；約翰福音第 4 章所引 D.A. Carson 的洞見），並註明檔案路徑。其餘各處的提問與導語，是編者用同樣的方式寫的，**不是老弟兄說的**。
10. **「看見耶穌」與「默想」**：每篇詩篇的「看見耶穌」分「新約引用」「主題呼應」「傳統」三種標示（只有前者是新約自己指出的連結）；每首聖詩的「默想」是編者寫的問題，不含任何歸給歷史人物的話。這兩項都沒有經過神學審閱，請牧者過目。
11. **各卷扉頁的「啟示的次序」**：照庫中各書的體例（`scripts/check-book-spine.py` 所檢查的項目），本書是由程式生成的單一檔案，該腳本不能直接檢查；骨幹章、扉頁句與各卷收尾，是人工對照該腳本的四項要求寫入的。

**版權**：所收聖詩皆為 1928 年前出版；依美國法律屬公有領域。其他地區若以作者卒後 70 年計，個別作品（如 Great Is Thy Faithfulness 的作者卒於 1960 年）可能尚未屆滿，本書為教會內部使用，公開發行前須重新確認。和合本為公有領域。

**已知的底本差異**：聖詩 {H('thechurchsonefoundation')} 的節錄「Is Jesus Christ our Lord」依庫中所引 A&N 1920 底本，通行本作 “her Lord”（見下方更多詩節）；本書沒有改動底本。
""")


w("\n## 附錄四 · 處境索引\n")
w("""遇到某個處境，不知道讀甚麼、唱甚麼，從這裏開始。詩篇編號指卷四；聖詩編號指卷五。

| 處境 | 詩篇 | 聖詩 |
|---|---|---|""")
for _s, _ps, _hs in SITUATIONS:
    w(f"| {_s} | {'、'.join(str(x) for x in _ps)} | " + "、".join(f"{NUM[h]}" for h in _hs) + " |")
w("")

text = "\n".join(out)
nfull = sum(1 for k, _, _ in ALL if full_text(k))
nfail = sum(1 for k, _, _ in ALL if k in CAL and not CAL[k]["ok"])
text = text.replace("{FAIL_N}", str(nfail)).replace("{MISS_N}", str(len(ALL) - nfull - nfail)).replace("{FULL_N}", str(nfull)).replace("{NOFULL_N}", str(len(ALL) - nfull))
text = text.replace("{USED_COUNT}", str(len(set(USED))))
open(OUT, "w", encoding="utf-8").write(text)
print(f"wrote {OUT}: {len(text)} chars, {len(ALL)} hymns, {len(PSALM_SET)} psalms, {len(USED)} scripture refs, {total_uses} hymn uses/{len(best)} titles")
