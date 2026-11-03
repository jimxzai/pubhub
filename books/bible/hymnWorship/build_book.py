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
HEADINGS = []       # (level, text) of every heading emitted, in order (page lookup after the first build)
CITES = {}          # ref -> set of heading indices in force when it was cited


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
    CITES.setdefault(ref, set()).add(len(HEADINGS) - 1)
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
    CITES.setdefault(ref, set()).add(len(HEADINGS) - 1)
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
AUTHOR_LINES = defaultdict(list)     # every author line the repo prints for a hymn (to recover a missing year)
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
        _bl = blk.split("\n")
        if len(_bl) > 1:
            AUTHOR_LINES[key].append(re.sub(r"^>\s*", "", _bl[1]).strip())
        if key not in best or len(blk) > len(best[key][0]):
            best[key] = (blk, mt.group(1).strip(), rel)


def n_books(key):
    # same hymn under spelling/title variants: group every key sharing the first 11 letters
    s = set()
    for k2, v in uses.items():
        if k2[:11] == key[:11]:
            s |= v
    return len(s)



# Structured hymn credits.  Every Latin word and number in these values must occur in a credit line the repo itself
# prints for that hymn (AUTHOR_LINES, exported to .sources/hymn-credit-raw.json and verified by check-worship-book.py);
# nothing is added from memory.  "—" = the repo gives none; "庫中未註" = the repo does not say.
UNK = "庫中未註"
HYMN_META = {
 1: ("Reginald Heber, 1826", "—", "—", "The Army and Navy Hymnal (1920)", "1、3", "歌詞自該書樂譜的分音節排版還原；第3節第2行印本作 \"Through the eye\"，依通行本改為 \"Though\""),
 2: ("Walter Chalmers Smith, 1867", "—", "—", UNK, UNK, "—"),
 3: ("Joachim Neander, 1680", "Catherine Winkworth, 1862", "—", UNK, "第二節", "—"),
 4: ("Isaac Watts, 1719", "—", "—", UNK, UNK, "—"),
 5: ("Martin Luther, 1529", "Frederick H. Hedge, 1853", "—", "The Army and Navy Hymnal (1920)", "1、3", "—"),
 6: ("Robert Robinson（1758，據庫中他章）", "—", "—", "hymntime.com (Cyber Hymnal)", "1、4", "—"),
 7: ("Matthew Bridges, 1851", "—", "—", "The Army and Navy Hymnal (1920), no. 68", "1", "A&N 頁面未印作者與年份，依通行著錄"),
 8: ("Isaac Watts, 1719", "—", "—", "The Army and Navy Hymnal (1920), No. 167", "1、5", "原頁面轉錄成樂譜的分音節排版，歌詞依行序還原"),
 9: ("Aurelius Prudentius, c. 405", "John Mason Neale, 1851", "—", UNK, UNK, "—"),
 10: ("Charles Wesley, 1758", "—", "—", "A Selection of Hymns, Used in the Parish Church … Ulverston (1863), Hymn 65", "1、4", "—"),
 11: ("Isaac Watts（1707，據庫中他章）", "—", "—", "The Army and Navy Hymnal (1920), no. 60", "1、4", "—"),
 12: ("Attributed to Bernard of Clairvaux (Salve caput cruentatum)", "德譯 Paul Gerhardt, 1656；英譯 James W. Alexander, 1830", "—", UNK, UNK, "—"),
 13: ("Augustus M. Toplady（年份庫中記載不一：1763、1776）", "—", "—", "The Army and Navy Hymnal (1920), no. 91", "1-2", "A&N 頁面未印作者，依通行著錄"),
 14: ("William Cowper, 1772", "—", "—", "Conyers's Collection of Psalms and Hymns", UNK, "取材自亞13:1"),
 15: ("Charles Wesley, 1738", "—", "—", UNK, UNK, "—"),
 16: ("John Newton, 1779", "—", "—", "Olney Hymns (1779), Book I, Hymn 41；1840 年版（Wikisource）", "1-2", "—"),
 17: ("Charlotte Elliott, 1835", "—", "—", UNK, UNK, "—"),
 18: ("Elvina M. Hall, 1865", "—", "John T. Grape, 1868", UNK, UNK, "庫中標註公有領域"),
 19: ("Charles Wesley, 1739", "—", "—", UNK, UNK, "—"),
 20: ("Mary A. Lathbury, 1877", "—", "—", UNK, UNK, "中譯為編者試譯"),
 21: ("William Walsham How, 1867", "—", "—", UNK, UNK, "—"),
 22: ("George Croly（1854，據庫中他章）", "—", "—", "The Army and Navy Hymnal (1920), no. 29", "1-2", "A&N 頁面未印作者，依通行著錄；印本以音節斷字，今還原；第2節 angel visitant 後補逗號"),
 23: ("William W. Walford（1845，據庫中他章）", "—", "William Batchelder Bradbury", UNK, UNK, "—"),
 24: ("Joseph Scriven（1855，據庫中他章）", "—", "—", UNK, UNK, "—"),
 25: ("Sarah Flower Adams, 1841", "—", "—", UNK, UNK, "—"),
 26: ("Henry Francis Lyte, 1847", "—", "—", UNK, UNK, "—"),
 27: ("Katharina von Schlegel（1752，據庫中他章）", "Jane Borthwick", "—", "hymntime.com (Cyber Hymnal)", "1、2", "—"),
 28: ("Horatio G. Spafford, 1873", "—", "—", UNK, UNK, "中譯為編者試譯"),
 29: ("William Cowper, 1773", "—", "—", "John Newton, Twenty-six Letters on Religious Subjects; to which are added Hymns (1774)；後收入 Olney Hymns (1779)", UNK, "原題 \"Light Shining out of Darkness\""),
 30: ("Anonymous（John Rippon, A Selection of Hymns, 1787）", "—", "—", UNK, UNK, "—"),
 31: ("Thomas O. Chisholm, 1923", "—", "—", UNK, UNK, "—"),
 32: ("William Williams (Welsh, 1745)", "Peter Williams", "—", "The Army and Navy Hymnal (1920)", "1-2", "省略重複的行"),
 33: ("Dorothy A. Thrupp, 1836", "—", "—", UNK, UNK, "—"),
 34: ("Ancient Irish hymn（年份庫中未註）", "英譯 Mary E. Byrne, 1905；韻文改寫 Eleanor H. Hull, 1912", "—", UNK, UNK, "—"),
 35: ("George Matheson, 1882", "—", "—", "The Cyber Hymnal（公有領域本）", "1", "—"),
 36: ("John Henry Newman（1833，據庫中他章）", "—", "—", UNK, UNK, "—"),
 37: ("Frances Ridley Havergal, 1874", "—", "—", UNK, UNK, "—"),
 38: ("John H. Sammis, 1887", "—", "Daniel B. Towner", UNK, UNK, "—"),
 39: ("Adelaide A. Pollard, 1906", "—", "—", UNK, UNK, "—"),
 40: ("John E. Bode, 1868", "—", "—", UNK, UNK, "—"),
 41: ("George Duffield, 1858", "—", "—", UNK, UNK, "—"),
 42: ("Samuel J. Stone, 1866", "—", "Aurelia：Samuel S. Wesley, 1864", "The Army and Navy Hymnal", UNK, "—"),
 43: ("John Fawcett, 1782", "—", "—", UNK, UNK, "—"),
 44: ("John Newton（1779，據庫中他章）", "—", "—", "Army and Navy Hymnal, 1920", "第二節", "該本未印年份"),
 45: ("Martin Rinkart, c.1636", "Catherine Winkworth, 1858", "—", UNK, UNK, "—"),
 46: ("Henry Alford, 1844", "—", "—", "Army and Navy Hymnal, 1920", "第一節", "該書註明 Hugh Hartshorne 修改"),
}


def hymn_body(key):
    blk, title, rel = best[key]
    lines = blk.rstrip("\n").split("\n")
    body = "\n".join(lines[1:])          # drop the bold title line; heading carries it
    n_ = NUM[key]
    au, tr, tu, src, st, nt = HYMN_META[n_]
    body = ("> **詞**：" + au + "　**譯／改寫**：" + tr + "　**曲**：" + tu + " \\\n"
            "> **底本**：" + src + "　**節**：" + st + "　**校註**：" + nt + "\n" + "\n".join(lines[2:]))
    body = body.replace("祢", "你").replace("裡", "裏")
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
    13: ("詩人問「要到幾時」，沒有立刻得到回答；新約說，我們有一位大祭司，在各樣試探上與我們一樣，只是沒有犯罪，所以可以坦然帶著這個問題到祂面前。", ["來 4:15-16"]),
    16: ("彼得在五旬節講道，把「不叫你的聖者見朽壞」指向基督的復活。", ["徒 2:25-31", "徒 13:35"]),
    19: ("羅馬書引用 19:4 說福音的傳揚；希伯來書雖未引用本篇，卻說神在這末世是藉著祂的兒子曉諭我們。", ["羅 10:18", "來 1:1-2"]),
    22: ("首句是耶穌在十字架上的呼喊；分衣、「傳揚你的名」，福音書與希伯來書都指向祂。", ["太 27:46", "約 19:24", "來 2:12"]),
    23: ("「耶和華是我的牧者」，耶穌說：「我是好牧人。」", ["約 10:11", "來 13:20"]),
    27: ("詩人說耶和華是我的亮光；耶穌說：「我是世界的光。」", ["約 8:12"]),
    32: ("保羅用這篇說明：不被算為有罪，是因信，不是因行為。", ["羅 4:6-8"]),
    42: ("詩人渴想活神；耶穌說：「人若渴了，可以到我這裏來喝。」", ["約 7:37", "約 4:14"]),
    46: ("「萬軍之耶和華與我們同在」與「以馬內利」是同一個應許；馬太引用的是以賽亞書7:14，沒有引用本篇。", ["太 1:23"]),
    51: ("認罪詩的盼望在於潔淨；新約說，神兒子耶穌的血洗淨我們一切的罪。", ["約壹 1:7", "弗 1:7"]),
    62: ("詩人說「我的心默默無聲，專等候神」；耶穌說：「凡勞苦擔重擔的人，可以到我這裏來，我就使你們得安息。」詩人所等候的神，在耶穌裏向人開口（耶穌沒有引用本篇）。", ["太 11:28-29"]),
    63: ("詩人說「我的心渴想你」；耶穌說：「到我這裏來的，必定不餓。」", ["約 6:35"]),
    67: ("「使萬國都得知你的救恩」，這個盼望在大使命裏有了具體的差遣。", ["太 28:19-20"]),
    84: ("詩人渴慕神的居所；約翰福音說，耶穌所說的殿，就是祂的身體（約翰沒有引用本篇）。", ["約 2:19-21"]),
    90: ("摩西說神是歷代的居所；耶穌說，愛祂的人，父與祂要與他同住（沒有引用本篇）。", ["約 14:23"]),
    91: ("撒但曾引用這篇（91:11-12）試探耶穌；耶穌答：不可試探主你的神。這篇的應許不是拿來試探神的。", ["路 4:9-12"]),
    95: ("希伯來書從3:7到4:11，一路引用並解釋這篇：「今天若聽他的話，就不可硬著心」，並指向神所應許的安息。", ["來 3:7-11", "來 4:1-11"]),
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
    134: ("本篇是夜間站在殿中的人為會眾獻上祝福；希伯來書說，耶穌「長遠活著，為他們祈求」（希伯來書沒有引用本篇）。", ["來 7:25"]),
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
    "immortalinvisiblegodonlywise": "歌詞說我們如樹上的葉子，發旺又枯萎，唯有祂永不改變。這一週，有哪一件事讓你特別覺得自己像葉子？",
    "praisetothelordthealmighty": "歌詞說祂用翅膀庇護你。這一週，有哪一件事是你事後才看出祂在庇護的？",
    "ogodourhelpinagespast": "歷代的保障——想一件你的家族或教會過去被保守的事。它怎樣改變你今天對將來的看法？",
    "amightyfortressisourgod": "歌詞說仇敵「結局已定」，一個小小的字就能將他擊倒。你現在最怕的那件事，肯不肯放在這個「已定」之下？",
    "comethoufountofeveryblessing": "歌詞說憐憫的溪流永不止息，也坦白承認「我容易漂流」。你最近哪一次發覺自己在漂流，又是怎樣被帶回來的？",
    "crownhimwithmanycrowns": "歌詞為寶座上的羔羊戴上許多冠冕。你今天最看重的一項成就或身分，願意放在祂腳前嗎？",
    "jesusshallreignwhereerthesun": "歌詞盼望祂的國「從這岸擴展到那岸」。今天你走過的哪一個地方，你可以為祂的名開口祈求？",
    "ofthefatherslovebegotten": "歌詞從「未有世界以先」說起：祂是源頭，也是終結。今天你的禱告，能不能先停在這一句，再說自己的事？",
    "lohecomeswithcloudsdescending": "「看哪，祂駕雲降臨。」若今天就是那一天，你最想先對祂說的一句話是甚麼？",
    "whenisurveythewondrouscross": "歌詞說：若整個自然界都歸我，那份禮物也太小。你這一週最捨不得的那一樣，放在這座十字架旁邊，看起來是甚麼樣子？",
    "osacredheadnowwounded": "這首詩停在那受傷的頭面前。你能不能單單看著，不急著解釋，停五分鐘？",
    "rockofagescleftforme": "歌詞說：縱使熱心不歇、眼淚長流，也不能贖罪。你帶到神面前的，有哪一樣其實是在暗暗換取祂的接納？",
    "thereisafountainfilledwithblood": "泉源是現在式。你上一次讓祂潔淨的，是哪一件具體的事？",
    "andcanitbethatishouldgain": "歌詞在確據與驚嘆之間來回：「現在不再有定罪」，卻仍問「怎能有這事」。你的確據，容得下驚嘆嗎？",
    "amazinggrace": "歌詞說恩典既教我的心敬畏，也除去我的恐懼。這兩樣，你最近經歷到的是哪一樣？",
    "justasiamwithoutoneplea": "歌詞說「不等除去心中一點污穢」就來。你有哪一件事，是打算先整理好才向祂提起的？",
    "jesuspaiditall": "歌詞說：罪留下深紅的污痕，祂洗得白如雪。有哪一件舊事，祂已經洗過了，你卻仍在心裏留著那塊污痕？",
    "christthelordisrisentoday": "歌詞向死亡發問：「你的毒鉤如今在哪裏？」今天你要帶著這句話去面對哪一件事？",
    "breakthouthebreadoflife": "歌詞求主像在海邊擘餅那樣擘開生命的糧。你上一次讀經，有哪一句真的被擘開給你？",
    "owordofgodincarnate": "歌詞稱聖經為「作我們腳前的燈」。你今天要走的路上，有哪一步需要這盞燈照一照？",
    "spiritofgoddescenduponmyheart": "歌詞說不求夢境與異象，只求把心靈的昏暗除去。你心裏哪一處最暗？你願意單單求聖靈去照亮它嗎？",
    "sweethourofprayer": "歌詞說，這個時刻曾在憂傷中帶來釋放，也曾使人逃過試探者的網羅。你上一次是在哪一件事上經歷這樣的時刻？",
    "whatafriendwehaveinjesus": "歌詞說，我們失去平安，是因為沒有把一切帶到神面前。這一週，有哪一樣是你自己扛著、沒有帶去的？",
    "nearermygodtothee": "歌詞設想日落、黑暗、以石為枕，仍然唱「更近我主」。你現在的黑暗，是在把你推近祂，還是推遠？",
    "abidewithme": "天晚了。你願意讓祂進到你一天裏最亂的那個房間嗎？",
    "bestillmysoul": "歌詞對自己的靈魂說：「主站在你這一邊。」你對自己的心說話時，說得出這一句嗎？",
    "itiswellwithmysoul": "歌詞說：無論平安如江河或憂傷如海浪，因我的罪已全部釘在祂的十架上，仍可說「得安寧」。你今天要把這句話念給哪一處憂傷聽？",
    "godmovesinamysteriousway": "哪一件今天看來是烏雲的事，你願意先不下結論？",
    "howfirmafoundation": "歌詞說，祂在話語中已說得夠多。祂已經說過的哪一句，你還沒有放心倚靠？",
    "greatisthyfaithfulness": "信實是「每個早晨」的事。你昨天早上，記得祂的哪一樣恩惠？",
    "guidemeothougreatjehovah": "歌詞稱自己是走過荒涼之地的客旅，求天上的糧餵養。你現在的荒涼裏，最缺的是甚麼？",
    "saviorlikeashepherdleadus": "歌詞說：「我需你慈愛看顧。」你今天最需要祂看顧的一處是甚麼？",
    "bethoumyvision": "歌詞說：「財富我不看重，人的虛名我不看重。」這兩樣裏，哪一樣最容易在你心裏悄悄居首？",
    "olovethatwiltnotletmego": "歌詞說：「我把疲乏的靈魂安放在你裏面。」你現在最疲乏的一處是甚麼？今天能不能把它安放在這愛裏？",
    "leadkindlylight": "歌詞說「我不求看見遠景，一步已足」。你現在在求的，是遠景，還是下一步？",
    "takemylifeandletitbe": "歌詞從手、腳、聲音一路獻到金銀、心思，說「一文不留」。其中哪一項，你最難說出「取去」？",
    "trustandobey": "信靠與順服，是同一件事的兩面。你這一週，哪一面比較弱？",
    "havethineownwaylord": "歌詞求祂「鑒察我，試驗我」，又求「現在就洗淨我」。你有哪一處，是怕被祂鑒察的？",
    "ojesusihavepromised": "歌詞說：祂若在我身旁，我就不懼怕爭戰。你已立志要走的路上，眼前哪一段最需要祂在身旁？",
    "standupstandupforjesus": "歌詞說：穿上福音的軍裝，每一件都用禱告穿上。今天出門前，你最需要為哪一件事先禱告？",
    "thechurchsonefoundation": "歌詞說教會是祂「用自己的血買了」的新婦。把你在教會裏最難受的那件事放在這句話旁邊，它看起來有甚麼不同？",
    "blestbethetiethatbinds": "有哪一位弟兄姊妹，今天你可以用一句話、一通電話與他相繫？",
    "gloriousthingsoftheearespoken": "歌詞說有活水「從永恆的愛中湧出」，「除去一切匱乏的懼怕」。你在教會裏，最近從哪裏喝到過這活水？",
    "nowthankweallourgod": "歌詞說祂「從我們母親的懷抱起」就一路賜福，直到今天。你最早記得的一份恩惠是甚麼？",
    "comeyethankfulpeoplecome": "歌詞說神是我們的造物主，供應我們所需。今年有哪一樣收成，你收下時幾乎沒有想到是祂所賜的？",
}
assert set(HQ) == {k for k, _, _ in ALL}, set(HQ) ^ {k for k, _, _ in ALL}

SITUATIONS = [  # (situation, [psalms in this book], [hymn keys])
    ("焦慮、擔憂", [23, 27, 131], ["whatafriendwehaveinjesus", "bestillmysoul", "itiswellwithmysoul", "leadkindlylight"]),
    ("罪疚、需要悔改", [32, 51, 130], ["rockofagescleftforme", "justasiamwithoutoneplea", "thereisafountainfilledwithblood", "andcanitbethatishouldgain"]),
    ("疲乏、軟弱", [62, 63, 121], ["abidewithme", "nearermygodtothee", "howfirmafoundation"]),
    ("病痛、困苦", [13, 22, 42], ["godmovesinamysteriousway", "bestillmysoul", "abidewithme"]),
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

COORD_P = {  # psalm group -> its place in the order 召、說、答、差
    "讚美與敬拜": "「答」的第一步：讚美。宣召之後，先稱頌神是誰。",
    "認罪與悔改": "「答」的第二步：認罪。看見神的聖潔之後，才看見自己。",
    "患難、信靠與安息": "「答」在日常裏的樣子：在患難中，仍把自己交在神手中。",
    "感恩與盼望": "「答」的回應：記念已經領受的恩典，並向前盼望。",
    "聖言與彌賽亞": "「說」的核心：神的話，最終指向那位說話的基督。",
}
COORD_H = {  # hymn theme (text before " (") -> its place in the order
    "讚美與敬拜": "「答」的第一步：讚美。把榮耀歸給那位本來就配得的。",
    "道成肉身與基督的降臨": "「說」：神的話成了肉身，並且要再來。",
    "十字架與救恩": "「答」的根據：認罪與領受赦免，都站在十字架上。",
    "復活": "「差」的起點：從空墳墓出去，基督是活的。",
    "聖言": "「說」：先聽神說話，再開口回應。",
    "禱告": "「答」：與神說話；這幾首詩教我們說甚麼。",
    "信靠、安慰與引導": "「答」在日常裏的樣子：患難中的信靠與引導。",
    "奉獻與跟隨": "「答」的最後一步，也是「差」的預備：把自己放在祭壇上，然後出去。",
    "教會與團契": "「答」是一個身體的事：我們不是各自來敬拜。",
    "感恩": "「答」：感謝，不等事情好了才說。",
}
assert set(COORD_P) == {g_ for g_, _ in PSALMS}, set(COORD_P) ^ {g_ for g_, _ in PSALMS}
assert set(COORD_H) == {th.split(" (")[0] for th, _, _ in HYMNS}, set(COORD_H) ^ {th.split(" (")[0] for th, _, _ in HYMNS}


def closing(ref, line):
    return "**你看見耶穌了嗎？** " + line + "\n\n> " + inline(ref) + "（" + label(ref) + "）\n"

# --------------------------------------------------------------- the book
out = []


def w(s):
    out.append(s)
    for m in re.finditer(r"(?m)^(#{1,3}) (.+?)(?: \{\.unnumbered\})?$", s):
        HEADINGS.append((len(m.group(1)), m.group(2).strip()))



def vol(title, intro=None, step=None, coord=None):
    w(f"# {title} {{.unnumbered}}\n")
    if intro:
        w(f"> {intro}\n")
    if step:
        w(f"> **啟示的次序·{step}**\n")
    if coord:
        w(f"> **全書座標**：{coord}\n")
    w("\n\\newpage\n")


# ---- front matter ------------------------------------------------------
w("# 前言：這本手冊怎麼來的 {.unnumbered}\n")
w(f"""這本手冊不是新寫的詩歌集，是**整理**。三書精讀庫裏已經有數十卷書，每一章都以一首聖詩起頭、一篇詩篇回應、一段禱告收尾；ai-eden.com 的閱讀器也選了幾首公有領域的聖詩做配樂。把這些反覆被使用、而且已經逐字對過來源的材料收攏，編成一本能帶進晨更、主日和家庭祭壇的敬拜手冊，就是本書。

**經過甚麼驗證：**

- **聖詩**：統計庫中各卷 `配詩` 欄共 {total_uses} 處、{len(best)} 首不同的詩，本書依主題挑選其中公有領域的 {len(ALL)} 首（不是按使用次數的前 {len(ALL)} 名）。每首的歌詞**直接取自庫中已有的章節**（不重新打字），並保留原註明的作者、年份與底本；中譯若是編者試譯，作者行會直接寫明。每首附「見於本庫 N 個書目」：這首詩在庫中被選為配詩的書目數（同一詩的不同拼法已合併；列王紀上下、約翰一二三書等各算一個書目）。
- **經文**：全書的詩篇與經節，都從 ai-eden 的和合本資料（`data/cuv.json`）**逐節程式讀出**，不憑記憶抄寫；每段經文之後附英文 NASB 1995，取自同一網站的 `/api/bible`（每章快取一次，腳本見 `books/bible/hymnWorship/.sources/fetch_aieden.py`）。共 {{USED_COUNT}} 段不同的經文（不含行文中順帶提到的經節）。
- **前輩與同工**：卷三的〈司會與領唱的預備〉、卷五的兩張清單、卷六的補充，採用了約翰·衛斯理〈唱詩指引〉與 Grace Community Church 官方講義〈The Role of Music in Worship〉的做法；英文引語與事實都已重新抓取原頁面逐字核對，見附錄七。
- **禱告與導語**：各處的短禱、導語與使用說明，是本書編寫的，不歸給任何歷史人物；凡是引用聖經的禱告，經文照錄，標明出處。

**不收的：**仍在版權保護中的詩歌（所收聖詩皆為 1928 年前出版）。想唱的現代讚美詩，請按貴堂會的授權另行加入。

**為甚麼叫「照基督的心意」：**歌羅西書 3:16 說「用詩章、頌詞、靈歌」，以弗所書 5:19 說「口唱心和地讚美主」——這三個詞是否各指一類，解經者有不同看法；本書只是借它們來安排：**詩篇**（卷四）、**聖詩**（卷五）、**聖靈感動、發自心裏的歌唱與禱告**（貫穿卷二、三、六）。本書各部分的次序都照同一個原則，也是庫裏各書共用的骨幹：**神先開口，人才回應。**
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
| 看前輩與同工怎樣談唱詩、敬拜與禱告 | 附錄七（Wesley〈唱詩指引〉、Grace Community Church 的官方講義、Graham 與 Barrows；逐字核對過的才收） | — |

**一個建議的次序**（晨更時）：安靜一分鐘 → 讀詩篇（出聲） → 唱或讀一首聖詩的歌詞 → 用詩篇的話禱告 → 一句話交託今天。

**詩篇怎麼讀：**讀出聲音。詩篇是寫來唱和念的，不是寫來默讀的。讀完一篇，挑一句話，用「我」來重念一遍，把它變成你自己的禱告。

**聖詩怎麼用：**書裏只印歌詞，不印曲譜（曲調請用貴堂會慣用的版本）。沒有曲子的時候，把歌詞當禱詞念，一樣有用。
""")
w("\n\\newpage\n")

EXT = {  # id -> (English text printed in the book, source label, [urls that must each contain it])
    "wesley7": ("Above all sing spiritually. Have an eye to God in every word you sing. Aim at pleasing him more than yourself, or any other creature.",
                "John Wesley, Directions for Singing（1761）",
                ["https://bachlund.org/Directions_for_Singing.htm", "https://www.wholesomewords.org/resources/singinghymns.html"]),
    "erb_questions": ("Are the words doctrinally sound? Is the text Biblical? Does it stimulate spiritual thought? Does it properly instruct? Does it inspire high spiritual ideals? Does the music fit the text? Is it excellent? Does it fit the need? Does it produce a wholesome response? Do harmful associations come to mind because of the musical style or the composer's name?",
                      "Clayton Erb, The Role of Music in Worship, Part One D",
                      ["https://s3.amazonaws.com/static.gracechurch.org/music/RoleofMusicinWorship.pdf"]),
    "erb_first": ("The first step in planning a worship service is to have a quiet time with the Lord, asking Him to lead and direct you as to what should be accomplished",
                  "Clayton Erb, The Role of Music in Worship, Part Three A",
                  ["https://s3.amazonaws.com/static.gracechurch.org/music/RoleofMusicinWorship.pdf"]),
    "erb_format": ("Many times a familiar format for the service is more effective than a program that is different merely for the sake of variety.",
                   "Clayton Erb, The Role of Music in Worship, Part Three A",
                   ["https://s3.amazonaws.com/static.gracechurch.org/music/RoleofMusicinWorship.pdf"]),
    "erb_peaks": ("Emotional peaks occur naturally (and should not be artificially manipulated)",
                  "Clayton Erb, The Role of Music in Worship, Part Three A",
                  ["https://s3.amazonaws.com/static.gracechurch.org/music/RoleofMusicinWorship.pdf"]),
    "erb_theme": ("It is easier to start with the theme of the message and work your music from that.",
                  "Clayton Erb, The Role of Music in Worship, Part Three B",
                  ["https://s3.amazonaws.com/static.gracechurch.org/music/RoleofMusicinWorship.pdf"]),
    "mac_music_not_worship": ("Music will play on your emotion, music will stir your emotion, but that is not necessarily worship. Music will give expression to love, it will give expression to adoration, it will give expression to honor, it will give expression to worship, but it doesn't produce it. What produces it is the truth in the heart and the work of the Spirit of God.",
          "John MacArthur, \"Spirit-Filled Music\"（gty.org 講道 90-377）", ["https://www.gty.org/sermons/90-377/spirit-filled-music"]),
    "mac_music_means": ("Music is a means to express worship, but it is not worship.",
          "John MacArthur, \"Is Music Worship?\"（gty.org 講道 80-428）", ["https://www.gty.org/sermons/80-428/is-music-worship"]),
    "mac_congregational": ("congregational singing is simply all of us stimulating one another to love and good works.",
          "John MacArthur, \"Music: The Expression of a Worshiping Heart\"（gty.org 講道 81-54）", ["https://www.gty.org/sermons/81-54/music-the-expression-of-a-worshiping-heart"]),
    "mac_scripture_worship": ("the more Scripture you know, the more doctrine you know, the more worship you give.",
          "John MacArthur, \"The Critical Elements of True Worship\"（gty.org 講道 80-323）", ["https://www.gty.org/sermons/80-323/the-critical-elements-of-true-worship"]),
    "mac_prayer_highest": ("If prayer is anything, it is the highest form of worship that an individual can participate in, because prayer is saying, \"God, Your name, Your kingdom, Your will be elevated, not my will, not my kingdom, not my name.\"",
          "John MacArthur, \"Prayer: The Highest Form of Worship\"（gty.org 講道 90-447）", ["https://www.gty.org/sermons/90-447/prayer-the-highest-form-of-worship"]),
    "barrows_hymn": ("There is not a situation in life where there isn't a hymn and a Scripture to meet the need.",
          "BGEA 官網 Cliff Barrows 人物頁（引在他的名字之下）", ["https://billygraham.org/cliff-barrows"]),
    "graham_thank": ("Begin when you pray by thanking and praising God for His love and goodness.",
          "Billy Graham, My Answer: \"How do I pray properly?\"（BGEA 官網）", ["https://billygraham.org/answers/how-do-i-pray-properly"]),
    "graham_confess": ("Then confess your sins and ask for His forgiveness. Finally, bring your concerns to Him. You may find it helpful to keep a list of people for whom you are praying.",
          "Billy Graham, My Answer: \"How do I pray properly?\"（BGEA 官網）", ["https://billygraham.org/answers/how-do-i-pray-properly"]),
    "graham_talking": ("Prayer is simply talking to God\u2014and the most important thing I can say about this is that God wants you to talk to Him!",
          "Billy Graham, My Answer: \"Is there a secret to praying?\"（BGEA 官網）", ["https://billygraham.org/answers/is-there-a-secret-to-praying"]),
    "graham_privilege": ("don't look on prayer as a burden or obligation; instead, look on it as a privilege.",
          "Billy Graham, My Answer: \"How often should I pray?\"（BGEA 官網）", ["https://billygraham.org/answers/how-often-should-i-pray-2"]),
    "sankey_gospel": ("D. L. Moody of Chicago will preach the gospel, and Ira D. Sankey of Chicago will sing the gospel in Bethesda Chapel every afternoon and evening this week, except Saturday, at 3 and 7 o'clock.",
                      "Ira D. Sankey, My Life and the Story of the Gospel Hymns（1907）",
                      ["https://archive.org/download/mylifest00sank/mylifest00sank_djvu.txt",
                       "https://archive.org/download/mylifestoryofgos0000irad_s4i2/mylifestoryofgos0000irad_s4i2_djvu.txt"]),
    "spurgeon_praise": ("There is no engagement under heaven that is more exalting than praising God, and however great may be the work which is committed to the charge of any of us, we shall always do well if we pause awhile to spend a time in sacred praise.",
                        "C. H. Spurgeon, \"Holy Song from Happy Saints\"（Metropolitan Tabernacle Pulpit 3476，講於 1871-03-05）",
                        ['https://www.spurgeon.org/sermons/holy-song-from-happy-saints', 'https://ccel.org/ccel/spurgeon/sermons61.xxxvii.html']),
    "spurgeon_nuance": ("I would not wish to prefer one spiritual exercise before another, else I think I would endorse the saying of an old divine who said that a line of praise was better than even a leaf of prayer",
                        "C. H. Spurgeon, \"Holy Song from Happy Saints\"（Metropolitan Tabernacle Pulpit 3476，講於 1871-03-05）",
                        ['https://www.spurgeon.org/sermons/holy-song-from-happy-saints', 'https://ccel.org/ccel/spurgeon/sermons61.xxxvii.html']),
    "calvin_heart": ("spiritual songs cannot be sung well but with the heart; but the heart requires the understanding",
                     "John Calvin, Preface to the Genevan Psalter（1543；英譯：J. W. Macmeeken, History of the Scottish Metrical Psalms, 1872）",
                     ['https://archive.org/download/historyofscottis00macm/historyofscottis00macm_djvu.txt', 'https://archive.org/download/historyofscottis00macm_0/historyofscottis00macm_0_djvu.txt']),
    "calvin_gift": ("the peculiar gift of man is to sing knowing what he says.",
                    "John Calvin, Preface to the Genevan Psalter（1543；英譯：J. W. Macmeeken, History of the Scottish Metrical Psalms, 1872）",
                    ['https://archive.org/download/historyofscottis00macm/historyofscottis00macm_djvu.txt', 'https://archive.org/download/historyofscottis00macm_0/historyofscottis00macm_0_djvu.txt']),
    "graham_barrows": ("His uncanny ability to lead a Crusade choir of thousands of voices or an audience of a hundred thousand voices in a great hymn or Gospel chorus is absolutely unparalleled",
                       "Billy Graham 評 Cliff Barrows，載於 Graham 自傳 Just As I Am，轉引自 BGEA 官網",
                       ["https://billygraham.org/cliff-barrows"]),
}
EXT_FACTS = {  # facts stated in Chinese, each with a needle that must occur in the source
    "erb_activities": (["Praise and adoration", "Thanksgiving", "Reading of Scripture", "Confession", "Prayer", "Intercession", "Ordinances of baptism", "Giving", "Instruction in the Word", "Application of the Word", "Fellowship"],
                       "https://s3.amazonaws.com/static.gracechurch.org/music/RoleofMusicinWorship.pdf"),
    "erb_author": (["Dr. Clayton Erb", "Minister of Worship & Music, Grace Community Church"], "https://s3.amazonaws.com/static.gracechurch.org/music/RoleofMusicinWorship.pdf"),
    "erb_planning": (["Ask the soloist or group to submit three choices", "rehearse all musical numbers and multimedia in the manner in which they will occur in the service", "Know what music you have used in the past", "Brief scripture and prayer", "Don't call them", "Church hymnal"],
                     "https://s3.amazonaws.com/static.gracechurch.org/music/RoleofMusicinWorship.pdf"),
    "erb_refs": (["Confession (repentance, submission; Leviticus 26:40-42, Nehemiah 9:2, Proverbs 28:13, Acts 19:18, James 4:7, 5:16; 1 John 1:9)",
                  "Intercession (2 Corinthians 1:11, 1 Thessalonians 5:25, James 5:14-16)", "Fellowship (Acts 2:42, Galatians 2:9)",
                  "Giving (Acts 2:45, 11:29; 1 Corinthians 16:2, 2 Corinthians 9:5, 7; Philippians 4:16)", "Reading of Scripture (Exodus 24:7, Deuteronomy 31:11, Nehemiah 8:1-8"],
                 "https://s3.amazonaws.com/static.gracechurch.org/music/RoleofMusicinWorship.pdf"),
    "calvin_augustine_a": (["saith St. Augustine, lies the difference between the song of man and that of birds", "a linnet, a nightingale, and a jay (papegay), may sing well"], "https://archive.org/download/historyofscottis00macm/historyofscottis00macm_djvu.txt"),
    "calvin_augustine_b": (["saith St. Augustine, lies the difference between the song of man and that of birds", "a linnet, a nightingale, and a jay (papegay), may sing well"], "https://archive.org/download/historyofscottis00macm_0/historyofscottis00macm_0_djvu.txt"),
    "hog": (["In 2016, Grace Community Church and The Master", "Psalms of Grace", "The official hymnal of Grace Community Church"], "https://www.gracechurch.org/hymnsofgrace"),
    "gcc_music": (["The Role of Music in Worship", "Copyright FAQ", "Hymn Accompaniments", "Celebrating 45 Years of Worship with Stephen Sturz"], "https://www.gracechurch.org/music/resources"),
    "barrows": (["first sang at a Billy Graham campaign in 1945 in Asheville", "took the reins of the Hour of Decision radio program"], "https://www.christianhistoryinstitute.org/magazine/article/an-evangelistic-band-of-brothers"),
    "shea": (["oldest of Graham"], "https://www.christianhistoryinstitute.org/magazine/article/an-evangelistic-band-of-brothers"),
    "bgea_hod": (["host of The Hour of Decision radio program for more than 60 years"], "https://billygraham.org/cliff-barrows"),
}

# ---- 骨幹章 -----------------------------------------------------------
w("# 敬拜的次序：神先開口 {.unnumbered}\n")
w("> **全書座標**：本書每一卷的次序，都從這一章來——**召、說、答、差**。\n")
w("""問「我們可以獻上甚麼」，是從人這一邊問起。聖經裏的敬拜，通常是從另一邊開始的：神先動了，人才有可回應的東西。下面四個場景，次序不完全相同，但起點都一樣：神先動，人才回應。

---

## 一、以賽亞：先看見，才說話
""")
w(scripture("賽 6:1-8"))
w("""
以賽亞沒有計劃要敬拜。他先「見主坐在寶座上」（6:1），然後才說「禍哉」（6:5）；然後有一位撒拉弗拿炭沾他的口，說他的罪孽除掉了（6:6-7）；最後主問「我可以差遣誰呢」，他才回答「我在這裏，請差遣我」（6:8）。**每一步的起點，都在神那裏。**

| 人的軌跡 | 看見 | 承認 | 領受 | 回應 | 被差遣 |
|---|---|---|---|---|---|
| **神的次序** | 顯現（6:1-4） | 照出人的真相（6:5） | 潔淨（6:6-7） | 發問（6:8） | 差遣（6:9「你去」） |

本書的主日程序（卷三）有十一個環節，歸納成六個動作：宣召、讚美、認罪與赦免、聖言、回應、差遣；次序就是這個。

## 二、井邊的婦人：父要這樣的人拜祂

約翰福音 4:23-24 已經在卷一印出。這裏只補一件事：誰在做工？庫中約翰福音一書引老弟兄所引的 D.A. Carson：

> 「『用心靈和誠實敬拜』不是說敬拜必須是自發的、無結構的……真正的敬拜是三一神的工作：父尋找敬拜者，子啟示真理，靈使敬拜成為可能。」
> ——出處：老弟兄《生命之道——約翰福音》查經筆記，約翰福音四至五章（見庫中 `books/bible/gospel-of-john/04-samaritan-woman.md`〈敬拜線〉）。**這是中譯、轉引自老弟兄的筆記；Carson 原書頁碼待查。**

約翰福音 4:23 說「父要這樣的人拜他」：敬拜先是回應父的尋找，不是人先發起的。

## 三、詩篇 95：召、跪、聽神說話

詩篇 95 全篇已收在卷四。它的結構本身就是一次敬拜：「來啊，我們要向耶和華歌唱」（1-2，**召**）；「因耶和華為大神」（3-5，**神是誰**）；「來啊，我們要屈身敬拜」（6，**跪**）；最後是：
""")
w(scripture("詩 95:7-8", cite=True))
w("""
7 節末句是呼籲：「惟願你們今天聽他的話。」希伯來書 3:7-8 把這句連同下一節當作「聖靈有話說」；第 9-11 節更明顯是神的第一人稱。所以這篇詩的次序是：召、神是誰、跪、然後聽神說話。**敬拜走到最後，是聽。**

## 四、啟示錄 5：天上的敬拜
""")
w(scripture("啟 5:11-13"))
w("""
天上的敬拜，中心是「曾被殺的羔羊」（5:12）。這就是敬拜的對象，也是敬拜的道路：我們不是靠自己的熱心進到寶座前，是靠羔羊。

---

## 三種常見的偏差

**一、以自己的感覺為中心。**問「今天唱得有沒有感動」，比問「神是不是被尊為聖」更多。約翰福音 4:24 說：「""" + inline("約 4:24") + """要拜的是神，不是自己的感覺。這不是說感動不重要，是說感動不能代替那位被敬拜的。

**二、有熱情或有形式，心卻遠離。**主耶穌引用先知的話，責備口唇尊敬、心卻遠離的人：
""")
w(scripture("太 15:8-9"))
w("""
「用心靈和誠實」是兩個一起，缺一不可（見卷一）：只有熱情沒有真理，容易變成自己的感覺；只有形式沒有心靈，容易變成冷冰冰的儀式。

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
    "第一步：神召我們——先有神的開口，才有人的敬拜。",
    "這一卷是「召」：先看神怎樣把人帶到祂面前；後面五卷，都是人的回應。")
w("## 神要怎樣的敬拜\n")
w(scripture("約 4:23-24"))
w("""
耶穌這句話是對一個撒瑪利亞婦人說的，不是對祭司說的。**用心靈**，是敬拜出自裏面，不靠地點與儀式；**用誠實**（也可譯作「真理」），是照神所啟示的真相來敬拜，不是照自己喜歡的樣子。兩樣缺一不可：只有熱情沒有真理，容易變成自己的感覺；只有真理沒有心靈，容易變成冷冰冰的儀式。
""")
w("""
John MacArthur 在談真敬拜的要素時，把「話語」與「敬拜」連在一起（講道逐字稿；英文引語已逐字核對）：
""")
w("> " + EXT["mac_scripture_worship"][0] + "\n>\n> — " + EXT["mac_scripture_worship"][1] + "\n")
w("""
與「用誠實」同一個方向：認識神的話越多、越深，敬拜越有內容。（編者概述。）
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
w("## 音樂不是敬拜，是敬拜的表達\n")
w("""John MacArthur 在 gty.org 的講道逐字稿裏講得很直接（五篇講道的篇名與代碼見附錄七）。他先說，音樂會牽動情緒，但那不一定是敬拜：
""")
w("> " + EXT["mac_music_not_worship"][0] + "\n>\n> — " + EXT["mac_music_not_worship"][1] + "\n")
w("""
再用一句話說清楚音樂的位置：
""")
w("> " + EXT["mac_music_means"][0] + "\n>\n> — " + EXT["mac_music_means"][1] + "\n")
w("""
在講歌羅西書 3:16 的另一篇講道裏，他把會眾歌唱說成互相的服事：
""")
w("> " + EXT["mac_congregational"][0] + "\n>\n> — " + EXT["mac_congregational"][1] + "\n")
w("""
與本書放在一起：**敬拜的來源是心裏的真理與聖靈的工作（約 4:24），音樂是表達它的方式**；所以司會不必製造感覺（見卷三〈司會與領唱的預備〉），會眾也不必唱完才算敬拜。（以上是編者的中文概述；這幾段只代表 MacArthur 在這些講道裏的主張，不代表他所有的看法。）
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
    "第二步：日復一日——把「召、說、答」縮成每天早晚的十分鐘。",
    "這一卷是個人的「答」：一個人，每天早晚怎樣走完「召、說、答」。")
w("""**用法：**早晨與晚間各一個十來分鐘的時段就夠。先安靜，再讀詩篇（出聲），然後讀或唱聖詩，最後念短禱，再用自己的話加上今天的事。

下面每一天都有一個主題。**短禱是本書編寫的**，你可以改成自己的話。

---
""")
DAYS = [
    ("主日 · 復活的日子", 118, "christthelordisrisentoday", 150, "crownhimwithmanycrowns",
     "主啊，今天是你所定的日子。你從死裏復活，所以我們能聚集。求你叫我們今天的歌唱，出於看見了你。",
     "主啊，你是活著的王。我這口氣息是你所賜；今天一整天我所領受的一切，都歸給你的名。"),
    ("週一 · 創造與全能", 8, "immortalinvisiblegodonlywise", 139, "bethoumyvision",
     "主啊，你造了天，也造了我。我算甚麼，你竟顧念我？新的一週，求你讓我記得，我是你手所造的，我的日子在你手中。",
     "鑒察我的神，今天我有許多沒有說出口的事，都在你面前。求你光照，也求你保守。"),
    ("週二 · 神的話", 1, "breakthouthebreadoflife", 19, "owordofgodincarnate",
     "主啊，你的話是我的喜愛。求你叫我今天思想它，像栽在溪水旁的樹，到了時候結出果子。",
     "主啊，你的話是完全的，能蘇醒人心。今天我聽見許多別的聲音，求你叫你的話在我心裏站得住，也赦免我隱而未現的過錯。"),
    ("週三 · 悔改與赦免", 51, "rockofagescleftforme", 32, "justasiamwithoutoneplea",
     "神啊，求你按你的慈愛憐恤我。我不再為自己找藉口，我的罪我自己知道。求你潔淨我，使我再次開口述說你的讚美。",
     "主啊，今天的過錯我不再隱瞞，都帶到你面前。你是我的藏身處，我領受你的赦免，我要歡呼。"),
    ("週四 · 感恩", 103, "nowthankweallourgod", 116, "praisetothelordthealmighty",
     "我的心哪，你要稱頌耶和華，不可忘記祂的一切恩惠。主啊，今天我要數一數你給我的，不只數我缺的。",
     "主啊，我拿甚麼報答你向我所賜的一切恩惠？我要舉起救恩的杯，求告你的名。"),
    ("週五 · 十字架", 22, "whenisurveythewondrouscross", 130, "osacredheadnowwounded",
     "主耶穌，你在十字架上喊說「我的神，我的神」，是替我被離棄，所以我能來到父面前。今天求你讓我再看一次十字架。",
     "耶和華啊，我從深處向你求告。你有赦免之恩，所以我等候你；我的心等候，勝過守夜的等候天亮。"),
    ("週六 · 信靠與安息", 23, "saviorlikeashepherdleadus", 91, "abidewithme",
     "耶和華是我的牧者，我必不致缺乏。主啊，這一週我走得很累，求你領我到可安歇的水邊。",
     "主啊，天晚了。我投靠在你的翅膀底下，求你保守；今天的事、明天的事，都交在你手裏，我要憑著你安睡。"),
]
for dname, am_ps, am_h, pm_ps, pm_h, am_pr, pm_pr in DAYS:
    assert am_ps in PSALM_SET and pm_ps in PSALM_SET, (am_ps, pm_ps)
    w(f"## {dname}\n")
    w(f"**早晨**：詩篇 {am_ps} · {H(am_h)}\n")
    w(f"> {am_pr}\n")
    w(f"**晚間**：詩篇 {pm_ps} · {H(pm_h)}\n")
    w(f"> {pm_pr}\n")

w("## 為甚麼每天停下來讚美\n")
w("""Spurgeon 在一篇講以賽亞書 5:1「我要為我所親愛的唱歌」的講章裏，這樣說（講章全文在 spurgeon.org 與 CCEL 兩處都有，英文引語在這兩處逐字相同、已核對）：
""")
w("> " + EXT["spurgeon_praise"][0] + "\n>\n> — " + EXT["spurgeon_praise"][1] + "\n")
w("""
他緊接著說（完整的一句，沒有截斷）：
""")
w("> " + EXT["spurgeon_nuance"][0] + "\n>\n> — " + EXT["spurgeon_nuance"][1] + "\n")
w("""
（編者概述：Spurgeon 自己有傾向，卻節制不偏重某一種操練。本書每日敬拜把「讚美」放在前面，是編者的編排，**Spurgeon 並沒有談每日的次序**。以下是簡式晨禱與晚禱。）
""")
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
    "第三步：同聚一堂——召、說、答、差，教會一起走完一次。",
    "這一卷是教會一起的「召、說、答、差」：同一個次序，由一個人放大成一群人。")
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

> 全能的神，你知道我們心裏的一切，沒有甚麼能向你隱藏。我們承認，我們沒有愛你勝過一切，也沒有愛人如己。我們在思想、言語和行為上得罪了你。求你因基督的緣故，按你的慈愛憐恤我們，赦免我們的過犯，使我們重新歸向你。奉主耶穌的名禱告。阿們。
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
w("""
公開讀經是聖經裏敬拜的一部分（尼 8:1-8；講義另列西 4:16、提前 4:13）。尼希米記記載他們怎樣讀：
""")
w(scripture("尼 8:8"))
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
w(scripture("林後 9:7"))
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
w("## 附：彼此問安與團契（可選）\n")
w("""Grace Community Church 講義把「團契」列為聖經中教會敬拜的活動之一（引徒 2:42、加 2:9；見附錄七）；本書的十一個環節沒有專設，可以放在宣召之前或差遣之後：問候、歡迎新朋友、彼此交接。
""")
w(scripture("徒 2:42"))
w(scripture("來 10:24-25"))
w("## 司會與領唱的預備\n")
w("""下面的做法，取自 Grace Community Church 官方網站上的講義〈The Role of Music in Worship〉（作者 Dr. Clayton Erb，該教會的 Minister of Worship & Music；12 頁的課程講義，不是教會的信仰宣言，也不是 MacArthur 本人的著作）。**英文引語都已重新抓取原文逐字核對**（見附錄七）；其餘是編者的中文概述，不加引號。

**一、先與主同在，再排程序。**
""")
w("> " + EXT["erb_first"][0] + "\n>\n> — " + EXT["erb_first"][1] + "\n")
w(f"""
講義接著標出雅各書 1:5（和合本：「{inline("雅 1:5")}」；講義沒有引出經文）。本書卷三的〈靜默預備〉，用意相同：司會先安靜，再開口。

**二、凡事規規矩矩，按著次序。**講義引了哥林多前書 14:40 的英文（和合本：「{inline("林前 14:40")}」），並且說：
""")
w("> " + EXT["erb_format"][0] + "\n>\n> — " + EXT["erb_format"][1] + "\n")
w("""
這也是小組可以放心沿用同一個次序的理由：**熟悉的次序，往往勝過為變化而變化。**

**三、感動會自然發生，不要人為操弄。**講義在談程序安排時提醒：
""")
w("> " + EXT["erb_peaks"][0] + "\n>\n> — " + EXT["erb_peaks"][1] + "\n")
w("""
編者的理解：司會的責任是排好次序、把路讓開，不是用音樂、燈光或話語去「製造」感覺。這與骨幹章所說「神先開口」是同一個方向。

**四、從講道的主題起頭選詩。**講義說：
""")
w("> " + EXT["erb_theme"][0] + "\n>\n> — " + EXT["erb_theme"][1] + "\n")
w("""
**五、獻唱的人先交三首備選**，由負責的人從中挑一首，避免曲風、歌詞或音域不合（講義 Part Two D 的建議，編者概述）。

**六、音響與投影照實際流程排練一次**，負責那天音響的人也參加排練；否則麥克風、線路、投影的問題會發生在聚會當中（講義 Part Two D，編者概述）。

**七、留下每次敬拜的紀錄**：唱了甚麼、何時唱、誰參與；以後重用最好的（講義 Part Three A，編者概述）。

**八、開頭與結尾**：講義的流程藍圖中，宣召可用「簡短的經文與禱告」；結束時可以有禱告、詩歌與祝福（編者概述）。

**九、報告事項改稱「事工參與的機會」**：講義的理由是，這是在告訴會眾這一週與往後可以怎樣參與事工（編者概述）。

**十、版權**：受版權保護的詩歌不能擅自投影、錄製、印在週報或詩歌本裏；講義介紹以 CCLI 的授權處理（編者概述）。這也是本書「現代詩歌只列曲目、不印歌詞」的原因。

帶領會眾唱詩是一種服事。關於 Billy Graham 如何評價他的詩歌領唱 Cliff Barrows，見附錄七。
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
    "第四步：神給的禱詞——詩篇是神給我們的話，也是我們還給神的話。",
    "這一卷是「說」與「答」之間的橋：神先給了禱詞，我們用祂給的話回應祂。")
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

Grace Community Church 的官方網頁說，他們除了詩歌本 *Hymns of Grace*，也透過 *Psalms of Grace* 推廣唱詩篇（見附錄七）。本書不附曲調，把詩篇當作可以念、可以啟應、可以禱讀的詞：啟應與每日時辰的用法，見庫裏《詩篇》一書〈禮儀使用指南〉。
""")
for grp, ps in PSALMS:
    w(f"## {grp}\n")
    w(f"**座標**：{COORD_P[grp]}\n")
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
    "第五步：用歌回應——歷代聖徒的回應，借我們的口唱出來。",
    "這一卷是「答」的歌唱：同一個回應，歷代聖徒已經唱過，我們接著唱。")
w("""**怎麼讀這一卷：**歌詞原文取自庫裏已核對的章節；作者行保留了當時註明的作者、年份與底本。**本書的中文歌詞多為編者所譯（各首的標示方式不一，如「編者試譯」「中譯：編者」），不是教會通行的詩歌本譯文**，只供對照理解；要唱的時候，請用貴堂會的詩歌本。「見於本庫 N 個書目」是這首詩被庫中多少個書目選為配詩，數字越大，表示越經得起不同書卷的使用。

**唱詩之前的兩張清單**（來源與英文原文見附錄七；以下是編者的中文概述）：

**會眾唱詩七要**（約翰·衛斯理，1761）：一、先學詩集裏的曲調；二、照印的唱，不自己改；三、全體都唱，軟弱疲倦也要唱；四、要有力量、有勇氣；五、要謙和，不蓋過會眾；六、要合拍，不快不慢；七、**最要緊的是用靈性唱**，一字一句都對著神。

**選詩十問**（Grace Community Church 講義〈The Role of Music in Worship〉）：這首詩的歌詞合乎教義嗎？文本有聖經根據嗎？能激發屬靈的思想嗎？能正確地教導嗎？能激勵高尚的屬靈理想嗎？曲調與歌詞相配嗎？夠出色、夠精緻嗎？合乎這次聚會的需要嗎？能帶來健康的回應嗎？會不會因為曲風或作曲者的名字，讓人聯想到有害的事？
""")
w("""
**用心、用領會地唱**：Calvin 在 1543 年日內瓦詩篇集的序裏，與衛斯理說的是同一件事。以下英譯取自 J. W. Macmeeken 1872 年的 *History of the Scottish Metrical Psalms*（公有領域；兩份不同的掃描逐字相同）。Calvin 在這段裏說，人與鳥唱歌的分別是「聖奧古斯丁」所指出的——鳥可以唱得好聽，卻不知道自己唱的是甚麼。另一個網站（Christian History Institute）轉載的英譯措辭不同（例如把其中一種鳥寫成 parrot，並省略奧古斯丁的歸屬），本書以 Macmeeken 的譯文為準；法文原文本輪未核對：
""")
w("> " + EXT["calvin_gift"][0] + "\n>\n> — " + EXT["calvin_gift"][1] + "\n")
w("> " + EXT["calvin_heart"][0] + "\n>\n> — " + EXT["calvin_heart"][1] + "\n")
w("""
（編者概述：鳥可以唱得好聽，但唱的人要知道自己唱的是甚麼，並且從心裏出來。）
""")
for theme, tag, hs in HYMNS:
    w(f"## {theme}\n")
    w(f"*{tag}*\n")
    w(f"**座標**：{COORD_H[theme.split(' (')[0]]}\n")
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
    "第六步：與神說話——最後落在禱告，也落在那位在父右邊代求的基督。",
    "這一卷是「答」的最後一步，也是整個次序的落點：禱告，並且是在那位代求的基督裏禱告。")
w("## 禱告是最高形式的敬拜\n")
w("""John MacArthur 在一篇講道裏這樣說（英文引語已逐字核對）：
""")
w("> " + EXT["mac_prayer_highest"][0] + "\n>\n> — " + EXT["mac_prayer_highest"][1] + "\n")
w("""
這與主禱文的次序相合：**先是神的事**（名、國、旨意），然後才是我們的事（見下）。（編者概述。）
""")
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
w("### 一個簡單的次序（Billy Graham）\n")
w("""BGEA 官網上有 Graham 在〈My Answer〉專欄裏回答「怎樣禱告」的文字（英文引語已逐字核對）。他給的次序是三步：先感謝並稱頌，再認罪求赦免，最後把所關心的事帶到神面前；與下面的四個方向大致相近，只是他把感恩與讚美合在開頭：
""")
w("> " + EXT["graham_thank"][0] + "\n>\n> — " + EXT["graham_thank"][1] + "\n")
w("> " + EXT["graham_confess"][0] + "\n>\n> — " + EXT["graham_confess"][1] + "\n")
w("""
他也說，禱告就是和神說話，不要把它看成負擔，而要看成特權：
""")
w("> " + EXT["graham_talking"][0] + "\n>\n> — " + EXT["graham_talking"][1] + "\n")
w("> " + EXT["graham_privilege"][0] + "\n>\n> — " + EXT["graham_privilege"][1] + "\n")
w("""
（以上都是 BGEA 官網上以 Graham 之名發表的專欄文字，不是講章；中文概述是編者所寫。）
""")
w("### 一、讚美\n")
w(scripture("詩 103:1-5"))
w("### 二、認罪\n")
w(scripture("詩 51:10-12"))
w("### 三、感恩\n")
w(scripture("帖前 5:16-18"))
w("### 四、祈求\n")
w(scripture("腓 4:6-7"))
w("### 補充：彼此認罪與代禱\n")
w("""Grace Community Church 的講義把「認罪」「禱告」「代禱」分開，列為聖經中教會敬拜的三項活動，各附經文依據（見附錄七）。以下照錄和合本：
""")
w(scripture("箴 28:13"))
w(scripture("雅 5:16"))
w(scripture("林後 1:11"))
w(scripture("帖前 5:25"))
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
PREFIX_LEN = len(HEADINGS)
PAGES = {}
try:
    _pj = json.load(open(os.path.join(HERE, ".sources", "pages.json"), encoding="utf-8"))
    import hashlib
    _sig = hashlib.sha1("\n".join(f"{a}|{b}" for a, b in HEADINGS[:PREFIX_LEN]).encode()).hexdigest()
    if _pj.get("sig") == _sig and _pj.get("n") == PREFIX_LEN:
        PAGES = {i: pg for i, pg in enumerate(_pj["pages"][:PREFIX_LEN])}
except OSError:
    pass


def pg(i):
    return str(PAGES[i]) if i in PAGES else "—"


def hidx(level, text_start, exact=False):
    """index of the first heading (at or before PREFIX_LEN) of this level that starts with text_start
    (or equals it when exact=True: 詩篇 1 must not match 詩篇 19)"""
    for i, (lv, tx) in enumerate(HEADINGS[:PREFIX_LEN]):
        if lv == level and (tx == text_start if exact else tx.startswith(text_start)):
            return i
    return -1


w("頁碼為該首聖詩標題所在頁（印出的頁碼）。\n")
w("| 編號 | 曲名 | 主題 | 書目數 | 頁 |\n|---|---|---|---|---|")
for theme, _, hs in HYMNS:
    short = theme.split(" (")[0]
    for key, zh, ref in hs:
        w(f"| {NUM[key]} | {TITLE[key]} | {short} | {n_books(key)} | {pg(hidx(3, f'{NUM[key]}. '))} |")
w("")
w("\n## 附錄三 · 來源與核對說明\n")
w(f"""**這一節如實交代本書每一類材料怎麼來，以及哪些事沒有做。**

1. **聖詩歌詞**：逐字取自庫中章節的「配詩」欄（共 {total_uses} 處、{len(best)} 首），沒有重新打字。庫中各章節當時如何核對（Army and Navy Hymnal 1920、Cyber Hymnal、Wikisource 等），作者行已照錄。**本書沒有重新對照原始詩歌本**；若某首歌詞有疑問，以作者行所註明的底本為準。
2. **中文歌詞**：多為編者所譯，標示方式不一致（有「編者試譯」「中譯：編者」「編者直譯」，也有未標示者），一律視為非通行譯本。詩歌本裏的通行中譯版權各異，本書不收。
3. **經文**：全部由 ai-eden 的 `data/cuv.json`（和合本）逐節讀出，共 {{USED_COUNT}} 段不同的經文。程式在建置時會檢查每個節號是否存在，缺節即中止。**本書沒有另行對照紙本和合本**；和合本資料本身若有排印問題，會一併帶入。**英文 NASB 1995 取自 ai-eden.com 的 API**；建置前已把本書用到的 116 章、617 節抓回，並把網站回傳的中文與 `cuv.json` 逐節比對（0 處不同）——但兩者本來就是同一個網站的資料，**和合本另以 FHL 信望愛和合本（`unv`）逐節比對**：617 節中 552 節完全相同、24 節只差標點、41 節有字形差異。這 41 節的差異全屬 FHL 把 1919 年和合本現代化（的→地、麼→嗎、罷→吧、那→哪、阿→啊、他→它／牠／她等，ai-eden 保留 1919 原貌），或校注文字不同（「或作」「或譯」）；**唯一的真缺字是詩 46:4**：ai-eden 資料作「這河的分使」，FHL、cnbible.com 與庫裡其他書都作「這河的分汊使」，本書已在生成器裡補上「汊」，網站資料本身未改（腳本 `.sources/check_cuv_fhl.py`）。另把網站全本 31,101 節都對 FHL 掃過一遍，找出約 60 節疑似漏字（32 節有 cnbible.com 佐證），清單見 `docs/build-reports/ai-eden-cuv-dropped-chars-2026-11-01.md`；**本書所引經文只受詩 46:4 一處影響**。**英文 NASB 另以 biblehub.com（頁面標題 NASB 1995）逐節比對**：617 節中 535 節字母完全相同；27 節是 ai-eden 在詩篇第 1 節多放了標題（如 “A Psalm of David.”，biblehub 把標題另列）；55 節是 biblehub 頁面尾端多出的下一段標題或版權行；**內文有差異的 0 節**。比對只看字母，不比標點與大小寫（腳本 `.sources/check_nasb_biblehub.py`）。英文裏方括號標示的補充詞已改排成斜體。NASB 版權屬 The Lockman Foundation，本書為教會內部使用，公開發行前須確認授權。
4. **更多詩節**：{{FULL_N}} 首附有全詩（English），取自 hymnal.net（人工打字、按詩節分段），採用前先做校準：庫中已核對的英文詩節，必須與 hymnal.net 對應詩節的相似度達 0.97 以上，全部通過才採用。其餘 {{NOFULL_N}} 首沒有全詩：{{FAIL_N}} 首抓到了但校準未通過（版本不同，或庫中的節錄本來就是選句），{{MISS_N}} 首在 hymnal.net 沒有配對到可用頁面，**只印庫中已核對的節錄，不印全詩**。通過校準只證明版本與詩節吻合，**沒有逐字對照紙本詩歌本**；這些詩節是 hymnal.net 的版本，不一定包含該詩最常唱的全部詩節（例如 Amazing Grace 缺 “Through many dangers”，第四節是後人所加，不是 Newton 1779 的原文），用字也可能與上方節錄略有差異（如 thee／you、標點）。校準不比對標點。歌詞抓取腳本與校準結果在 `books/bible/hymnWorship/.sources/`。
5. **導語與短禱**：編寫的內容；除了第 9、12 項所列、已註明出處的老弟兄原話、Carson 轉引與外部來源引語外，沒有引用歷史人物的話。
6. **使徒信經**：依通行譯文，不是聖經經文，各堂會用字略有出入。
7. **ai-eden 閱讀器的配樂曲目**（Be Thou My Vision、Nearer, My God, to Thee、Just As I Am、Jesus Paid It All、Joy to the World）：前四首已收入本書（{H('bethoumyvision')}、{H('nearermygodtothee')}、{H('justasiamwithoutoneplea')}、{H('jesuspaiditall')}）。*Joy to the World* 在庫中沒有逐字核對過的歌詞，所以本書未收。
8. **曲譜**：本書不含曲譜。
9. **老弟兄的話**：本書引用的老弟兄原話，只有庫中既有檔案裏已有的（《詩篇》〈禱告版〉的兩句與一段方法；約翰福音第 4 章所引 D.A. Carson 的洞見），並註明檔案路徑。其餘各處的提問與導語，是編者用同樣的方式寫的，**不是老弟兄說的**。
10. **「看見耶穌」與「默想」**：每篇詩篇的「看見耶穌」分「新約引用」「主題呼應」「傳統」三種標示（只有前者是新約自己指出的連結）；每首聖詩的「默想」是編者寫的問題，不含任何歸給歷史人物的話。這兩項都沒有經過神學審閱，請牧者過目。
12. **前輩與同工的材料**（附錄七及卷三、五、六相關段落）：英文引語與事實由 `.sources/verify_external_quotes.py` 重新抓取原頁面核對，結果記錄在 `external-quotes-verified.json`；中文是編者概述，不加引號。講義是課程講義，不是教會的信仰宣言。
11. **各卷扉頁的「啟示的次序」**：照庫中各書的體例（`scripts/check-book-spine.py` 所檢查的項目），本書是由程式生成的單一檔案，該腳本不能直接檢查；骨幹章、扉頁句與各卷收尾，是人工對照該腳本的四項要求寫入的。

**版權**：所收聖詩皆為 1928 年前出版；依美國法律屬公有領域。其他地區若以作者卒後 70 年計，個別作品（如 Great Is Thy Faithfulness 的作者卒於 1960 年）可能尚未屆滿，本書為教會內部使用，公開發行前須重新確認。和合本為公有領域。

**已知的底本差異**：聖詩 {H('thechurchsonefoundation')} 的節錄「Is Jesus Christ our Lord」依庫中所引 A&N 1920 底本，通行本作 “her Lord”（見下方更多詩節）；本書沒有改動底本。
""")


w("\n## 附錄四 · 處境索引\n")
w("""BGEA 官網的 Cliff Barrows 人物頁（他是 Billy Graham 福音協會的音樂與節目主任，與 Graham 並肩事奉六十年，曾帶領聚會中的會眾與詩班唱詩），在他的名字下引了一句話；這張索引做的就是這件事（頁面沒有另註這句話的場合）：
""")
w("> " + EXT["barrows_hymn"][0] + "\n>\n> — " + EXT["barrows_hymn"][1] + "\n")
w("""
""")
w("""遇到某個處境，不知道讀甚麼、唱甚麼，從這裏開始。詩篇編號指卷四；聖詩編號指卷五；括號內是所在頁。

| 處境 | 詩篇 | 聖詩 |
|---|---|---|""")
for _s, _ps, _hs in SITUATIONS:
    w(f"| {_s} | {', '.join(f'{x}（{pg(hidx(3, f'詩篇 {x}', exact=True))}）' for x in _ps)} | " + ", ".join(f"{NUM[h]}（{pg(hidx(3, f'{NUM[h]}. '))}）" for h in _hs) + " |")
w("\n詩篇 91 放在「爭戰」而不放在「病痛」：它說的是神的同在與看顧，不是不會生病的保證；病痛中的人請讀詩 13、22、42，並參看雅各書 5:14-15。\n")
w("")

# ---- 附錄五、六：詩篇索引、經文索引（頁碼來自上一次建置；第一次建置顯示「—」）
w("\n## 附錄五 · 詩篇索引\n")
w("本書收錄的詩篇與所在頁。\n")
w("| 詩篇 | 組別 | 頁 |\n|---|---|---|")
for _grp, _ps in PSALMS:
    for _n, _ in _ps:
        w(f"| {_n} | {_grp} | {pg(hidx(3, f'詩篇 {_n}', exact=True))} |")
w("")
w("\n## 附錄六 · 經文索引\n")
w("本書引用的經文，依聖經書卷次序排列。頁碼是該段引用**所在小節標題的起始頁**，引用本身可能在其後一、兩頁。同一節出現在不同處，頁碼並列。\n")
_canon = list(cuv)
_slug_order = {}
for _i, _k in enumerate(_canon):
    _slug_order.setdefault(_k.rsplit("-", 1)[0], _i)
_rows = []
for _ref, _idxs in CITES.items():
    _code, _ch, _vs, _ = parse(_ref)
    _pgs = sorted({PAGES[i] for i in _idxs if i in PAGES})
    _rows.append((_slug_order[BOOKS[_code]], _ch, _vs[0], label(_ref), _pgs))
_seen = {}
for _o, _ch, _v0, _lab, _pgs in sorted(_rows):
    _seen.setdefault((_o, _ch, _v0, _lab), set()).update(_pgs)
w("| 經文 | 頁 |\n|---|---|")
for (_o, _ch, _v0, _lab), _pgs in sorted(_seen.items()):
    w(f"| {_lab} | {'、'.join(str(x) for x in sorted(_pgs)) if _pgs else '—'} |")
w("")

# Guard: no verse cited in this book may sit on ai-eden's dropped-character candidate list unless it was reviewed.
# psalms-46:4 is patched above; 1-thessalonians-4:14 was reviewed (FHL modernises 他 -> 他們; not a site error).
_DROPPED = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(HERE))), "docs", "build-reports", "ai-eden-cuv-dropped-chars-2026-11-01.md")
if os.path.exists(_DROPPED):
    _cand = set(re.findall(r"(?m)^\| ([a-z0-9-]+:\d+) \|", open(_DROPPED, encoding="utf-8").read()))
    _cited = set()
    for _ref in set(USED) | {f"詩 {n}" for n in PSALM_SET}:
        _c, _ch, _vs, _ = parse(_ref)
        _cited |= {f"{BOOKS[_c]}-{_ch}:{v}" for v in _vs}
    _unreviewed = sorted((_cand & _cited) - {"psalms-46:4", "1-thessalonians-4:14"})
    if _unreviewed:
        raise SystemExit(f"cited verses on ai-eden's dropped-character list, not reviewed: {_unreviewed}")

# ---- 附錄七：外部來源（逐字核對）
w("\n## 附錄七 · 前輩與同工怎樣談唱詩、禱告與敬拜\n")
w("""本附錄只收**編者實際讀到原文、並且能逐字核對**的材料。英文引語與事實都登記在 `books/bible/hymnWorship/.sources/`，由 `verify_external_quotes.py` 重新抓取原頁面比對（結果見 `external-quotes-verified.json`）；中文概述是編者所寫，不加引號。沒有核對到的，列在本附錄最後，**不寫進正文**。
""")
w("### 一、約翰·衛斯理〈唱詩指引〉（1761）\n")
w("""衛斯理在 1761 年出版的衛理詩歌集（*Select Hymns: with Tunes Annext*）後面附了七條唱詩的指引（有資料說出自同年的 *Sacred Melody* 序言，出處待核原書）。七條的內容在三個網頁上相同；第 7 條的**英文原文以兩個網頁逐字相同的文字為準**（第三個網頁把 “Above all sing” 改寫為 “Above all else, sing”）。以下中文是編者概述：

| 條 | 要點（編者概述） |
|---|---|
| 1 | 先學詩集裏的曲調，再學別的 |
| 2 | 照印的唱，不要自己改 |
| 3 | 全體都唱；軟弱疲倦也不要因此不唱，這是一個十字架，背起來就成了祝福 |
| 4 | 要有力量、有勇氣地唱，不要半死不活 |
| 5 | 要謙和：不要大聲到蓋過會眾，要使眾人的聲音合成一個清楚的聲音 |
| 6 | 要合拍：不跑在前、不拖在後；別唱得太慢 |
| 7 | **最要緊的是用靈性唱**（原文如下） |

""")
w("> " + EXT["wesley7"][0] + "\n>\n> — " + EXT["wesley7"][1] + "\n")
w("""
這與骨幹章〈敬拜的次序〉所說「以自己的感覺為中心」的偏差同一個方向：第 7 條要人留心所唱的意思，使心不被聲音帶走，而是獻給神。
""")
w("### 二、Grace Community Church 的敬拜與音樂事工\n")
w("""**來源**：以下取自該教會官方網站（gracechurch.org）上的官方資源：音樂事工頁列出的講義〈The Role of Music in Worship〉，作者標明為 Dr. Clayton Erb（Grace Community Church 的 Minister of Worship & Music）；這是一份 12 頁的課程講義（檔案標題為 2012 PM612 Syllabus；是哪一所學校的課程，講義沒有寫），**不是教會的信仰宣言，也不是 MacArthur 本人的著作**。

**1. 聖經中教會敬拜的十一項活動**（講義 Part One C；每項都附經文依據，此處只列項目與本書對應的位置）：

| 講義的項目 | 本書的對應位置 |
|---|---|
| 讚美與頌讚（Praise and adoration） | 卷三〈讚美〉；卷五 |
| 感恩（Thanksgiving） | 卷三〈奉獻與感恩〉；卷五〈感恩〉 |
| 讀經（Reading of Scripture） | 卷三〈聖言〉 |
| 認罪（Confession） | 卷三〈認罪〉〈赦免的宣告〉；詩 51、130 |
| 禱告（Prayer） | 卷三〈代禱與主禱文〉；卷六 |
| 代禱（Intercession） | 卷三〈代禱與主禱文〉 |
| 洗禮與聖餐（Ordinances of baptism and communion） | 卷三〈聖餐〉；〈特別場合〉的洗禮 |
| 奉獻（Giving） | 卷三〈奉獻與感恩〉 |
| 話語的教導（Instruction in the Word） | 卷三〈聖言〉（講道） |
| 話語的應用（Application of the Word） | 本書沒有專設；由卷五每首聖詩後的〈默想〉、卷二的簡式晨禱／晚禱部分承擔 |
| 團契（Fellowship） | 卷三〈附：彼此問安與團契（可選）〉（十一個環節之外的可選項，可放在宣召前或差遣後） |

**2. 怎樣判斷一首詩適不適合敬拜**（講義 Part One D 的十問，原文）：
""")
w("> " + EXT["erb_questions"][0] + "\n>\n> — " + EXT["erb_questions"][1] + "\n")
w("""
講義接著提醒（編者概述）：標準要出於聖經，不是出於傳統或個人喜好；可用腓立比書 4:8 判斷一首曲子的價值，用哥林多前書 14:26「凡事都當造就人」判斷它是否適合會眾使用。

**3. 怎樣安排一次敬拜**（講義 Part Three A，原文）：
""")
w("> " + EXT["erb_first"][0] + "\n>\n> — " + EXT["erb_first"][1] + "\n")
w("> " + EXT["erb_format"][0] + "\n>\n> — " + EXT["erb_format"][1] + "\n")
w("""
前一句與本書卷三的〈靜默預備〉同方向：先與主同在，再排程序。後一句可以幫助小組不必為求變化而改次序。講義另外提到（編者概述）：先定敬拜的流程，再配程序；留下每次敬拜的紀錄，日後重用最好的；版權歌曲須有授權（講義介紹 CCLI），這與本書「現代詩歌只列曲目、不印歌詞」的做法一致。

**4. 該教會公開的資源**（官方網頁所列）：
- **Hymns of Grace**：Grace Community Church 與 The Master's Seminary 於 2016 年合作出版的詩歌本，官方稱為該教會的詩歌本；官網另說他們也出版 Spanish 版（Himnos de Gracia），並透過 *Psalms of Grace* 推廣唱詩篇。官方網站：hymnsofgrace.org。
- **音樂事工資源頁**（gracechurch.org/music）：列有〈The Role of Music in Worship〉、〈Copyright FAQ〉、〈CCLI〉、詩歌伴奏（Hymn Accompaniments）、〈Celebrating 45 Years of Worship with Stephen Sturz〉等檔案。
- **YouTube 官方頻道**：youtube.com/@GraceChurchSunValley（頻道名稱 Grace Community Church）；音樂資源頁的檔案清單裏有一項〈Celebrating 45 Years of Worship with Stephen Sturz〉，連結到 YouTube 上的一支影片（YouTube 上的影片標題是《Stephen Sturz' 45 Year Anniversary》，頻道為 Grace Community Church）。該頁面上沒有嵌入影片，只有連結。
""")
w("### 三、John MacArthur（gty.org 講道逐字稿）\n")
w("""本書讀了他的五篇講道逐字稿（gty.org 的講道頁面，英文引語已重新抓取原頁面逐字核對）：

| 講道 | 代碼 | 本書用在 |
|---|---|---|
| Music: The Expression of a Worshiping Heart | 81-54 | 卷一：會眾歌唱是彼此服事 |
| Spirit-Filled Music | 90-377 | 卷一：音樂不是敬拜，是表達 |
| Is Music Worship? | 80-428 | 卷一：音樂是表達敬拜的方式 |
| The Critical Elements of True Worship | 80-323 | 卷一：話語與敬拜 |
| Prayer: The Highest Form of Worship | 90-447 | 卷六：禱告是最高形式的敬拜 |

這些是**口頭講道的逐字稿**，每處都只引一兩句；它們代表他在這幾篇講道裏的主張，不代表他所有的看法。他的書（如 *Worship: The Ultimate Priority*）與其他講道本輪沒有讀。
""")
w("### 四、Billy Graham 與 Cliff Barrows\n")
w("""取自 Billy Graham Evangelistic Association（BGEA）官網與 Christian History Institute 的人物介紹（兩處都是機構／雜誌的介紹文，**不是 Graham 或 Barrows 本人的講章**）：

- Cliff Barrows 與 Graham 的初次相遇在 1945 年的 Asheville 一帶：BGEA 官網說他當時在蜜月旅行中遇見 Graham；Christian History Institute 說他在那一年首次於 Graham 的聚會中獻唱。兩個來源說法不同，本書兩說並列。他後來全職加入 Graham 的事工，在福音協會成立時是創始董事之一，並接手 *Hour of Decision* 廣播節目；BGEA 官網說他擔任這個節目的主持人超過六十年。
- George Beverly Shea 是 Graham 核心團隊中年紀最長的一位（Christian History Institute）。
- Graham 在自傳 *Just As I Am* 裏這樣評論 Barrows（BGEA 官網轉引）：
""")
w("> " + EXT["graham_barrows"][0] + "…\n>\n> — " + EXT["graham_barrows"][1] + "\n")
w("""
- **禱告**：BGEA 官網的〈My Answer〉專欄有多篇 Graham 回答「怎樣禱告」的文字；本書卷六引了其中三篇（*How do I pray properly?*、*Is there a secret to praying?*、*How often should I pray?*）。這些是報紙專欄式的短答，**不是講章**。
- **詩歌**：Barrows 在 BGEA 官網人物頁上的一句話，本書放在附錄四〈處境索引〉開頭。
""")
w("""
（編者的看法，不是 BGEA 或衛斯理的話：帶領會眾唱詩是一種服事，目標是眾人一起唱，不是一個人唱得好；這與衛斯理第三、四條要求全體都唱、要有力量地唱，方向相近。）
""")
w("### 五、Dwight Moody 與 Ira Sankey（1870 年代的搭檔）\n")
w("""Moody 是講道的，Sankey 是領唱與獨唱的，兩人搭檔的方式與後來的 Graham 與 Barrows 很像。Sankey 在回憶錄裏記下他們在英國 Sunderland 一座教會看到的海報（據 Sankey 自己的記述，「唱福音」〔sing the gospel〕這個說法就是從這張海報來的）：
""")
w("> " + EXT["sankey_gospel"][0] + "\n>\n> — " + EXT["sankey_gospel"][1] + "\n")
w("""
**來源說明**：Sankey 的回憶錄是公有領域；這句話在兩份**不同的掃描／OCR**（Princeton 神學院藏本與另一份掃描，兩者都是 1907 年版）裏逐字相同，已用腳本核對。OCR 的錯誤因此不太可能同時出現在兩份，但**兩份掃描是同一個版本，若該版本本身有誤，這個核對看不出來**。書中其他 Sankey 的故事本書沒有引用。
""")
w("### 六、Calvin 與 Spurgeon\n")
w("""**Calvin**（日內瓦詩篇集序，1543）：卷五引了兩句。英譯取自 J. W. Macmeeken 的 *History of the Scottish Metrical Psalms*（Glasgow, 1872），archive.org 上**兩份不同的掃描**（`historyofscottis00macm`、`historyofscottis00macm_0`）逐字相同，已用腳本核對；**兩份是同一個版本，版本本身若有誤，這個核對看不出來**。Calvin 在這段裏把「人與鳥唱歌的分別」歸給聖奧古斯丁（原文：“saith St. Augustine, lies the difference between the song of man and that of birds”）。Christian History Institute 轉載的另一個英譯措辭不同（如 parrot、並省略奧古斯丁），本書不採用。**法文原文與 *Opera Calvini* 本輪沒有讀**，所以這只是「這個英譯如此說」。

**Spurgeon**（講章 *Holy Song from Happy Saints*，Metropolitan Tabernacle Pulpit 第 3476 號，1871-03-05）：卷二引了兩句；同一段文字在 spurgeon.org 與 CCEL 兩個網站逐字相同；Answers in Genesis 的版本把措辭現代化了（例如 “pause for a while to spend time”），所以不算數。他在這篇裏引了一位老神學家「讚美的一行勝過禱告的一頁」的說法，並說若不是不願偏重某一種屬靈操練，他會贊同這句話：他有傾向，但自我節制；所以本書兩句並引，而且第二句引完整句，不截斷。他談會眾歌唱的其他講章與《Our Own Hymn-Book》的序，本輪沒有取得可核對的全文。
""")
w("### 七、馬丁·路德（轉引，未加引號）\n")
w("""路德在 1538 年為 Georg Rhau 的《*Symphoniae iucundae*》寫序，把音樂放在神的話之後，評價極高（《路德著作集》第 53 卷，頁碼待核）。本書只讀到轉引這段的網頁，沒有讀到原書，所以**不引原文、不加引號**。
""")
w("### 八、沒有找到、或不能核對的部分\n")
w("""下面這些，本書編者要求自己：**沒有逐字核對到，就不寫進正文**。

- **John MacArthur 的其他論述**：本書只讀了上表五篇講道；他的書（如 *Worship: The Ultimate Priority*）與其他講道本輪沒有讀。搜尋結果中有一句據說出自他、談「復興被遺忘的偉大聖詩」的話，只見於二手網頁，在 Hymns of Grace 官網找不到，**未引用**。
- **Grace Community Church 詩班在 YouTube 的個別詩歌錄影**：官方頁面能確認的是 YouTube 頻道與一支音樂事工影片；詩班唱詩的具體影片網址，本輪沒有逐一核對，不列。
- **Billy Graham 以〈Just As I Am〉作為招收決志的詩歌**：多篇報導這樣說，但本輪沒有讀到原文，不寫進正文（書名《Just As I Am》則屬事實）。
- **Spurgeon 與 Calvin 的其他材料**：Spurgeon《Our Own Hymn-Book》的序在 archive.org 只有借閱版；他談會眾歌唱的其他講章本輪沒有取得可核對的全文。Calvin 的法文原文與 *Opera Calvini* 本輪沒有讀（英譯已讀 Macmeeken 1872 的節譯）。**Sankey** 的回憶錄只引了上面一句，書中其他故事沒有讀完。**Graham 之外的前輩對「禱告」的教導**，本輪只取得 MacArthur 的一篇（卷六引用）。
""")


text = "\n".join(out)
nfull = sum(1 for k, _, _ in ALL if full_text(k))
nfail = sum(1 for k, _, _ in ALL if k in CAL and not CAL[k]["ok"])
text = text.replace("{FAIL_N}", str(nfail)).replace("{MISS_N}", str(len(ALL) - nfull - nfail)).replace("{FULL_N}", str(nfull)).replace("{NOFULL_N}", str(len(ALL) - nfull))
text = text.replace("{USED_COUNT}", str(len(set(USED))))
open(OUT, "w", encoding="utf-8").write(text)
_raw = {str(NUM[k]): sorted(set(AUTHOR_LINES.get(k, [])) | {re.sub(r"^>\s*", "", best[k][0].split("\n")[1]).strip()}) for k, _, _ in ALL}
json.dump(_raw, open(os.path.join(HERE, ".sources", "hymn-credit-raw.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"prefix_len": PREFIX_LEN, "headings": HEADINGS}, open(os.path.join(HERE, ".sources", "headings.json"), "w", encoding="utf-8"), ensure_ascii=False)
print(f"wrote {OUT}: {len(text)} chars, {len(ALL)} hymns, {len(PSALM_SET)} psalms, {len(USED)} scripture refs, {total_uses} hymn uses/{len(best)} titles")
