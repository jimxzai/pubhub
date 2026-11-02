#!/usr/bin/env python3
"""Generate the data-driven parts of books/bible/Biblehebrew from OSHB (Open Scriptures Hebrew Bible).

Corpus:  docs/sources/biblehebrew/oshb/*.xml   (WLC text + morphology, 39 books)
Lexicon: docs/sources/biblehebrew/HebrewStrong.xml (Strong's number -> pointed Hebrew + part of speech)

Writes (all under books/bible/Biblehebrew/):
  generated/stats.json            every number quoted in prose ({{key}} placeholders are filled from this)
  generated/genesis1-parse.md     word-by-word parse of Genesis 1:1-5
  generated/verb-stats.md         verb stem and verb form counts
  generated/prefix-stats.md       one-letter prefix counts
  96-appendix-top-words.md        the 100 commonest words
"""
import collections, glob, json, os, re, sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs/sources/biblehebrew")
OUT = os.path.join(ROOT, "books/bible/Biblehebrew")
OSIS = "{http://www.bibletechnologies.net/2003/OSIS/namespace}"
LEXNS = "{http://openscriptures.github.com/morphhb/namespace}"
PREFIXES = set("bcdklmsi")

FORM_FIX = {"413": "אֶל", "1696": "דָּבַר"}   # the Strong lexicon prints these two with the wrong vowel / missing dagesh
POS_FIX = {"5892": "n-f"}                     # the lexicon marks עִיר masculine; it is feminine

def pos_zh(pos):
    if pos.startswith("n-pr"): return "專有名詞"
    if pos == "n-m": return "陽性名詞"
    if pos == "n-f": return "陰性名詞"
    return POS.get(pos, pos)


POS = {"n": "名詞", "v": "動詞", "prep": "介系詞", "conj": "連接詞", "adv": "副詞", "prt": "小品詞", "r": "關係詞",
       "p": "人稱代名詞", "d": "指示詞", "i": "疑問詞", "a": "形容詞", "dp": "小品詞", "np": "小品詞", "inj": "感嘆詞",
       "pref": "前綴＋詞尾"}

# gloss by Strong's number (or pseudo-lemma b/l/k/m = a one-letter preposition that carries a pronoun ending)
GLOSS = {
    "853": "賓格記號（不譯出，標明受詞）", "3068": "耶和華（神的名）", "5921": "在……上、對著", "413": "向、到",
    "834": "……的（關係詞）", "3605": "全部、每一個", "559": "說", "3808": "不", "1121": "兒子", "3588": "因為、當……時",
    "l": "前綴 ל 帶詞尾：向他、給他", "1961": "是、成為、有", "6213": "做、造", "430": "神（複數形指獨一的神）",
    "935": "來、進去", "4428": "王", "3478": "以色列", "776": "地、土地", "3117": "日子", "376": "人、男人、丈夫",
    "6440": "面、臉、前面", "1004": "家、殿", "5414": "給、放置", "1931": "他、那個", "5971": "民、百姓", "3027": "手",
    "1697": "話語、事情", "b": "前綴 ב 帶詞尾：在他裏、用他", "7200": "看見", "5704": "直到", "4480": "從、比",
    "1": "父親", "8085": "聽、聽從", "1696": "說話", "5892": "城", "859": "你", "3427": "坐、住",
    "1732": "大衛", "518": "如果", "3318": "出去", "7725": "轉回、回來", "5973": "與、同在", "3212": "走、去",
    "259": "一", "3947": "拿", "3045": "知道", "5927": "上去、升上", "854": "與、同（介系詞，和 853 拼法相同）",
    "5869": "眼睛、泉源", "8141": "年", "589": "我", "8034": "名", "7971": "差遣、伸出", "2009": "看哪",
    "4191": "死", "8033": "那裏", "3063": "猶大", "398": "吃", "5650": "僕人", "369": "沒有", "802": "女人、妻子",
    "3651": "這樣", "1571": "也", "8147": "二", "4872": "摩西", "5315": "生命、魂、人", "3548": "祭司", "428": "這些",
    "4100": "甚麼？", "7121": "呼叫、稱呼", "408": "不要（禁止）", "310": "在……之後", "1870": "路、行為",
    "7451": "壞的、惡", "5375": "舉起、擔", "3389": "耶路撒冷", "4714": "埃及", "251": "弟兄", "6965": "起來、站起",
    "2063": "這個（陰性）", "7218": "頭", "3820": "心", "1323": "女兒", "7760": "放置、設立", "4325": "水",
    "3967": "一百", "3541": "這樣", "2896": "好的、美善", "1992": "他們", "1471": "國、列國", "5674": "越過、經過",
    "120": "人、亞當", "2022": "山", "1419": "大的", "5975": "站立", "6963": "聲音", "8478": "在……之下",
    "505": "一千", "1980": "行走",
    # Genesis 1:1-5 extras
    "7225": "起初、開端", "1254": "創造", "8064": "天", "8414": "空虛、荒涼", "922": "混沌、空空",
    "2822": "黑暗", "8415": "深淵", "7363": "盤旋、運行", "216": "光", "914": "分開",
    "996": "在……之間", "3915": "夜", "6153": "晚上", "1242": "早晨",
    # words quoted in prose
    "2617": "忠誠的愛、慈愛", "157": "愛（動詞）",
    "160": "愛（名詞）", "571": "真實、可靠", 
    "6944": "聖、聖潔", "2403": "罪", "5771": "罪孽", "6588": "過犯",
    # series vocabulary (words featured in the 原文研讀 tables of many books)
    "7307": "靈、風、氣息", "2142": "記念、記得", "2388": "剛強、堅固", "4941": "公義、判決", "3519": "榮耀、尊榮",
    "6030": "回答、回應", "5162": "後悔、轉意、安慰", "4397": "使者、天使", "3772": "剪除、立（約）", "8451": "律法、教導",
    "5769": "永遠、長久", "3372": "敬畏、懼怕", "1818": "血", "1350": "贖回、救贖", "784": "火", "5612": "書、書卷",
    "2428": "力量、軍力", "2416": "活的、生命", "8548": "常常、持續", "8104": "看守、遵守", "4853": "重擔、神諭",
    "4390": "充滿", "1245": "尋求", "7068": "熱心、嫉妒", "68": "石頭", "6635": "軍隊、萬軍", "5307": "落下、倒下",
    "4672": "找到、遇見", "6666": "公義", "6664": "公義、正直",
    "1285": "約、盟約", "7965": "平安、完整",
    "3824": "心（לֵב 的較長詞形）", "4886": "用油膏、膏立", "2398": "犯罪、錯過", "2451": "智慧", "7227": "多、大", "8199": "審判、治理", "4910": "統治、掌權", "1540": "揭開、被擄、流亡", "1875": "尋求、查問", "1486": "籤", "2764": "咒詛、完全獻上（毀滅）",
    # song words
    "3034": "稱謝、讚美", "1984": "讚美（歡呼）", "7623": "稱讚", "523": "民族", "5273": "美好、愉快", "3162": "一同",
    "7462": "牧養（分詞：牧者）", "2637": "缺乏", "4393": "充滿（的）", "7321": "歡呼", "6476": "發聲（歌唱）",
    "7442": "歡呼歌唱", "2167": "歌頌（彈奏）", "2088": "這個", "6918": "聖潔的",
}
SONGS = {
    "shema": dict(ref="Deut.6.4", zh="申命記 6:4（Shema）", start=0, chunks=[2, 2, 2], cuv=("deuteronomy-6", ["4"]),
                  translit=["shema yisra'el", "adonai eloheinu", "adonai echad"],
                  keys=["8085", "430", "259"], hymn=None),
    "hinei": dict(ref="Ps.133.1", zh="詩篇 133:1（Hinei ma tov）", start=3, chunks=[3, 2, 4], cuv=("psalms-133", ["1"]),
                  translit=["hinneh mah tov", "umah na'im", "shevet achim gam yachad"],
                  keys=["2009", "2896", "5273", "3427", "251", "3162"], hymn=None),
    "hallelu": dict(ref="Ps.117.1", zh="詩篇 117:1（Hallelu et-Adonai）", start=0, chunks=[5, 3], cuv=("psalms-117", ["1"]),
                    translit=["halelu et-adonai kol goyim", "shabbechuhu kol ha'ummim"],
                    keys=["1984", "3605", "1471", "7623", "523"], hymn="watts117"),
    "hodu": dict(ref="Ps.118.1", zh="詩篇 118:1／136:1（Hodu）", start=0, chunks=[2, 2, 3], cuv=("psalms-118", ["1"]),
                 translit=["hodu ladonai", "ki tov", "ki le'olam chasdo"],
                 keys=["3034", "2896", "5769", "2617"], hymn=None),
    "qadosh": dict(ref="Isa.6.3", zh="以賽亞書 6:3（Qadosh）", start=0, chunks=[5, 5, 4], cuv=("isaiah-6", ["3"]),
                   translit=["veqara zeh el zeh veamar", "qadosh qadosh qadosh adonai tseva'ot", "melo khol ha'arets kevodo"],
                   keys=["6918", "6635", "4393", "776", "3519"], hymn="heber"),
    "joy": dict(ref="Ps.98.4", zh="詩篇 98:4", start=0, chunks=[4, 3], cuv=("psalms-98", ["4"]),
                translit=["hari'u ladonai kol ha'arets", "pitschu veranenu vezameru"],
                keys=["7321", "3605", "776", "6476", "7442", "2167"], hymn="joy"),
    "shepherd": dict(ref="Ps.23.1", zh="詩篇 23:1", start=2, chunks=[2, 2], cuv=("psalms-23", ["1"]),
                     translit=["adonai ro'i", "lo echsar"], keys=["7462", "2637"], hymn="rous"),
}
FOLDER_ZH = {
    "genesis": "創世記", "exodus": "出埃及記", "leviticus": "利未記", "numbers": "民數記", "duetonomy": "申命記",
    "joshua": "約書亞記", "judges": "士師記", "ruth": "路得記", "kings": "列王紀上", "kings2": "列王紀下",
    "chronicl1": "歷代志上", "chronicl2": "歷代志下", "ezra": "以斯拉記", "nehemiah": "尼希米記", "esther": "以斯帖記",
    "job": "約伯記", "proverb": "箴言", "ecclesiastes": "傳道書", "songofsolomen": "雅歌", "isaiah": "以賽亞書",
    "jeremiah": "耶利米書", "lamentation": "耶利米哀歌", "ezekiel": "以西結書", "daniel": "但以理書", "hosea": "何西阿書",
    "Joel": "約珥書", "Amos": "阿摩司書", "Obadiah": "俄巴底亞書", "Jonah": "約拿書", "Micah": "彌迦書",
    "Nahum": "那鴻書", "habakkuk": "哈巴谷書", "Zapphaniah": "西番雅書", "Haggai": "哈該書", "zechariah": "撒迦利亞書",
    "malachi": "瑪拉基書", "psalm": "詩篇", "1-samuel": "撒母耳記上", "2-samuel": "撒母耳記下",
}

STEM = {"q": "Qal", "N": "Niphal", "p": "Piel", "P": "Pual", "h": "Hiphil", "H": "Hophal", "t": "Hithpael"}
STEM_EFFECT = {"q": "簡單的動作（說、看、來）", "N": "被動，或自己承受動作", "p": "加強；常把「狀態」變成「動作」",
               "P": "Piel 的被動", "h": "使役：使……去做", "H": "Hiphil 的被動", "t": "反身：自己對自己做"}
STEM_ZH = {"q": "基本", "N": "反身／被動", "p": "加強", "P": "加強的被動", "h": "使役", "H": "使役的被動", "t": "反身加強"}
ASPECT_ZH = {"p": "完成式", "q": "連續完成式", "i": "未完成式", "w": "連續未完成式", "h": "願意式", "j": "祈願式",
             "v": "命令式", "r": "主動分詞", "s": "被動分詞", "a": "不定詞（絕對）", "c": "不定詞（連接）"}
PERSON = {"1": "第一人稱", "2": "第二人稱", "3": "第三人稱"}
GEN = {"m": "陽性", "f": "陰性", "b": "陰陽皆可", "c": "通性"}
NUM = {"s": "單數", "p": "複數", "d": "雙數"}
STATE = {"a": "獨立", "c": "連續（接下一詞）", "d": "有定"}
NOUN_T = {"c": "普通名詞", "p": "專有名詞", "g": "族稱"}
PART_T = {"a": "肯定詞", "d": "定冠詞", "e": "感嘆詞", "i": "疑問詞", "j": "感嘆詞", "m": "指示詞", "n": "否定詞",
          "o": "賓格記號", "r": "關係詞"}
PRON_T = {"d": "指示代名詞", "f": "不定代名詞", "i": "疑問代名詞", "p": "人稱代名詞", "r": "關係代名詞"}
PREFIX_ZH = {"b": "ב「在、用」", "c": "ו「和、並且」", "d": "ה「那個」（定冠詞）", "k": "כ「如同」",
             "l": "ל「向、為」", "m": "מ「從」", "s": "ש「那……的」", "i": "ה（疑問）"}


def lexicon():
    root = ET.parse(os.path.join(SRC, "HebrewStrong.xml")).getroot()
    out = {}
    for e in root.iter(LEXNS + "entry"):
        w = e.find(LEXNS + "w")
        out[e.get("id")] = (w.text, (w.get("pos") or "").split()[0])
    return out


def key_of(lemma):
    parts = lemma.split("/")
    for p in parts:
        p = p.strip()
        if re.match(r"\d", p):
            return re.sub(r"[\s+a-z]+$", "", p)
    return parts[-1]


def tokens():
    for f in sorted(glob.glob(os.path.join(SRC, "oshb/*.xml"))):
        for v in ET.parse(f).getroot().iter(OSIS + "verse"):
            for w in v.findall(OSIS + "w"):
                yield v.get("osisID"), w.get("lemma"), w.get("morph"), "".join(w.itertext())


def strip_cantillation(s):
    s = re.sub("[֑-ֽ֯׀ׅׄ]", "", s)
    return s.replace("/", "")


def seg_desc(seg):
    t = seg[0]
    r = seg[1:]
    if t == "R": return "介系詞"
    if t == "C": return "連接詞"
    if t == "D": return "副詞"
    if t == "T": return PART_T.get(r[:1], "小品詞")
    if t == "P": return PRON_T.get(r[:1], "代名詞") + _pgn(r[1:])
    if t == "N":
        d = NOUN_T.get(r[:1], "名詞")
        g, n, s = (r[1:2], r[2:3], r[3:4])
        return d + "：" + "·".join(x for x in [GEN.get(g, ""), NUM.get(n, ""), STATE.get(s, "")] if x)
    if t == "A":
        g, n, s = (r[1:2], r[2:3], r[3:4])
        kind = {"c": "基數（數字）", "o": "序數（數字）", "g": "族稱形容詞"}.get(r[:1], "形容詞")
        return kind + "：" + "·".join(x for x in [GEN.get(g, ""), NUM.get(n, ""), STATE.get(s, "")] if x)
    if t == "S":
        k = r[:1]
        if k == "p": return "詞尾（代名詞）" + _pgn(r[1:])
        return {"d": "詞尾（表方向的 ה）", "h": "詞尾（附加的 ה）", "n": "詞尾（附加的 נ）"}.get(k, "詞尾")
    if t == "V":
        stem, asp = r[:1], r[1:2]
        bits = [STEM.get(stem, "其他詞幹") + "（" + STEM_ZH.get(stem, "") + "）" if stem in STEM else "其他詞幹",
                ASPECT_ZH.get(asp, asp)]
        rest = r[2:]
        if asp in "rs":
            bits += [GEN.get(rest[0:1], ""), NUM.get(rest[1:2], "")]
        elif asp in "ac":
            pass
        else:
            bits += [PERSON.get(rest[0:1], ""), GEN.get(rest[1:2], ""), NUM.get(rest[2:3], "")]
        return "動詞：" + "·".join(x for x in bits if x)
    return seg


def _pgn(r):
    if not r: return ""
    return "：" + "·".join(x for x in [PERSON.get(r[0:1], ""), GEN.get(r[1:2], ""), NUM.get(r[2:3], "")] if x)


def morph_desc(m):
    segs = m.split("/")
    segs[0] = segs[0][1:]  # drop language letter
    return "＋".join(seg_desc(s) for s in segs)


def main():
    lex = lexicon()
    toks = list(tokens())
    total = len(toks)
    cnt = collections.Counter(key_of(l) for _, l, _, _ in toks)
    nlem = len(cnt)
    aramaic = sum(1 for _, _, m, _ in toks if m.startswith("A"))

    def cover(k):
        return round(sum(n for _, n in cnt.most_common(k)) / total * 100, 1)

    pref = collections.Counter()
    verbs = collections.Counter()
    asp = collections.Counter()
    for ref, l, m, t in toks:
        if m.startswith("A"): continue            # prefix counts, like the verb counts, are Hebrew only
        lp = l.split("/")
        for p in lp[:-1] if len(lp) > 1 else []:
            if p.strip() in PREFIXES: pref[p.strip()] += 1
        if m.startswith("A"): continue            # Aramaic words are not counted under Hebrew stem names
        segs = m.split("/"); segs[0] = segs[0][1:]
        for s in segs:
            if s.startswith("V"):
                verbs[s[1:2]] += 1
                asp[s[2:3]] += 1
    nverb = sum(verbs.values())
    ex = collections.Counter()
    for ref, l, m, t in toks:
        k = key_of(l)
        if k in ("3925", "935") and not m.startswith("A"):
            segs = m.split("/"); segs[0] = segs[0][1:]
            for sg in segs:
                if sg.startswith("V"): ex[(k, sg[1])] += 1
    stats = {
        "tokens": total, "lemmas": nlem, "hapax": sum(1 for n in cnt.values() if n == 1), "aramaic": aramaic,
        "hapax_pct": round(sum(1 for n in cnt.values() if n == 1) / nlem * 100), "aramaic_pct": round(aramaic / total * 100, 1),
        "nverb": nverb,
        "cover10": cover(10), "cover25": cover(25), "cover50": cover(50), "cover100": cover(100),
        "cover200": cover(200), "cover300": cover(300), "cover500": cover(500), "cover1000": cover(1000),
        "n_ge50": sum(1 for n in cnt.values() if n >= 50),
        "cover_ge50": round(sum(n for n in cnt.values() if n >= 50) / total * 100, 1),
        "n_ge100": sum(1 for n in cnt.values() if n >= 100),
        "pref_c": pref["c"], "pref_d": pref["d"], "pref_l": pref["l"], "pref_b": pref["b"], "pref_m": pref["m"],
        "pref_k": pref["k"], "pref_s": pref["s"], "pref_i": pref["i"],
        "verb_qal_pct": round(verbs["q"] / nverb * 100), "verb_niphal_pct": round(verbs["N"] / nverb * 100),
        "verb_piel_pct": round(verbs["p"] / nverb * 100), "verb_hiphil_pct": round(verbs["h"] / nverb * 100),
        "verb_wayyiqtol": asp["w"], "verb_wayyiqtol_pct": round(asp["w"] / nverb * 100),
        "verb_perfect": asp["p"], "verb_imperfect": asp["i"], "verb_imperative": asp["v"],
        "verb_ptc": asp["r"] + asp["s"],
        "lamad_qal": ex[("3925", "q")], "lamad_piel": ex[("3925", "p")], "bo_qal": ex[("935", "q")], "bo_hiphil": ex[("935", "h")],
    }
    for k in ["430", "3068", "559", "2617", "1285", "8451", "7965", "157", "160", "3519", "571", "6666", "6664",
              "7307", "5315", "1697", "1696", "7725", "8085", "6944", "2403", "5771", "6588", "3478", "1254",
              "6213", "7225", "7121", "853", "854", "5921", "3605", "413", "4480", "5973", "5704", "8478",
              "3808", "408", "369", "4310", "4100", "3588", "8104", "5162", "3069", "3071"]:
        stats["n_" + k] = cnt[k]
    # Exod 17:15 "יְהוָה נִסִּי" is two tokens under H3071; only the first ("3071+") is the divine name
    stats["lemmas_strong"] = sum(1 for k in cnt if k.isdigit())
    stats["yhwh_total"] = cnt["3068"] + cnt["3069"] + sum(1 for _, l, _, _ in toks if l.strip() == "3071+")
    os.makedirs(os.path.join(OUT, "generated"), exist_ok=True)
    json.dump(stats, open(os.path.join(OUT, "generated/stats.json"), "w"), ensure_ascii=False, indent=1)

    # ---------- top-100 appendix
    top = cnt.most_common(100)
    miss = [k for k, _ in top if k not in GLOSS]
    if miss: sys.exit(f"missing gloss: {miss}")

    def lemma_form(k):
        if k in PREFIXES: return {"l": "לְ", "b": "בְּ", "k": "כְּ", "m": "מִן"}.get(k, k), "pref"
        return lex["H" + k]

    rows = ["---", "title: 附錄：最常見的一百個希伯來字", "subtitle: Top 100 Hebrew Words", "author: PubHub 三書精讀系統",
            "date: 2026年11月", "publisher: 三書精讀出版系統", "---", "",
            "# 附錄：最常見的一百個希伯來字 (The Hundred Commonest Words) {.unnumbered}", "",
            f"> 次數由 OSHB 希伯來文舊約（列寧格勒抄本 WLC，附詞形標注）逐詞目實際計數：全舊約 {total:,} 個詞、{nlem:,} 個詞目。"
            "「累計」欄是這些字合起來佔全舊約的百分比。中文意思只列最常見的一種，不是詞典定義。", "",
            "> 注意：前綴（和、在、向、從、那個）依詞目標注是分開計算的，所以像「和」(ו) 這種字不在本表；"
            "「前綴 ל／ב 帶詞尾」兩列，是指前綴本身接了代名詞詞尾的詞（如 לוֹ），見第五章；מִן 一列只計獨立的 מִן，貼在字前的前綴 מִ 不在內。", "",
            "| # | 原文 | 詞類 | 次數 | 累計 | 常見意思 |", "|-----|------------|--------|----------|----------|-----------------------------------|"]
    cum = 0
    for i, (k, n) in enumerate(top, 1):
        cum += n
        form, pos = lemma_form(k)
        form = FORM_FIX.get(k, form); pos = POS_FIX.get(k, pos)
        rows.append(f"| {i} | {form} | {pos_zh(pos)} | {n:,} | {cum / total * 100:.1f}% | {GLOSS[k]} |")
    rows.append("")
    open(os.path.join(OUT, "96-appendix-top-words.md"), "w", encoding="utf-8").write("\n".join(rows))

    # ---------- Genesis 1:1-5 parse
    want = {f"Gen.1.{v}" for v in range(1, 6)}
    lines = [(r, l, m, t) for r, l, m, t in toks if r in want]
    miss = sorted({key_of(l) for _, l, _, _ in lines if key_of(l) not in GLOSS})
    if miss: sys.exit(f"missing gloss (Gen): {miss}")
    out = ["| 節 | 原文 | 詞目 | 形態 | 意思 |", "|----|--------------|--------------|----------------------------------------|----------------------|"]
    for r, l, m, t in lines:
        k = key_of(l)
        parts = l.split("/")
        pre = [PREFIX_ZH[p.strip()] for p in parts if p.strip() in PREFIX_ZH]
        form = lex["H" + k][0]
        desc = morph_desc(m)
        if pre: desc = "前綴 " + "、".join(pre) + "＋" + desc.split("＋", len(pre))[-1] if "＋" in desc else desc
        out.append(f"| {r.split('.')[-1]} | {strip_cantillation(t)} | {form} | {desc} | {GLOSS[k]} |")
    open(os.path.join(OUT, "generated/genesis1-parse.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")

    # ---------- verb stats
    vr = ["| 詞幹 | 名稱 | 大致作用 | 次數 | 佔動詞 |", "|--------------|--------------|-----------------------------------|------------|------------|"]
    other = nverb - sum(verbs[s] for s in STEM)
    for s in "qNpPhHt":
        vr.append(f"| {STEM[s]} | {STEM_ZH[s]} | {STEM_EFFECT[s]} | {verbs[s]:,} | {verbs[s] / nverb * 100:.1f}% |")
    vr.append(f"| 其他 | 較罕見的詞幹 | | {other:,} | {other / nverb * 100:.1f}% |")
    ar = ["| 動詞形式 | 次數 | 佔動詞 |", "|----------|------|------|"]
    for a in "pwiqvrsach j".replace(" ", ""):
        ar.append(f"| {ASPECT_ZH[a]} | {asp[a]:,} | {asp[a] / nverb * 100:.1f}% |")
    open(os.path.join(OUT, "generated/verb-stats.md"), "w", encoding="utf-8").write(
        "\n".join(vr) + "\n\n" + "\n".join(ar) + "\n")

    # ---------- prefix stats
    pr = ["| 前綴 | 意思 | 次數 |", "|----|----------|------|"]
    for p, n in sorted(pref.items(), key=lambda x: -x[1]):
        letter, _, meaning = PREFIX_ZH[p].partition("「") if "「" in PREFIX_ZH[p] else (PREFIX_ZH[p], "", "（疑問）")
        pr.append(f"| {letter} | {meaning.split('」')[0] if '」' in meaning else meaning} | {n:,} |")
    open(os.path.join(OUT, "generated/prefix-stats.md"), "w", encoding="utf-8").write("\n".join(pr) + "\n")
    # ---------- grammar paradigm tables (commonest attested form per slot, straight from OSHB)
    import unicodedata
    forms = collections.defaultdict(collections.Counter)  # (key, morph) -> Counter(form)
    pron = collections.defaultdict(collections.Counter)
    for ref, l, m, t in toks:
        k = key_of(l)
        form = strip_cantillation(t)
        forms[(k, m)][unicodedata.normalize("NFC", form)] += 1
        if "/" not in m and m.startswith("HPp"):
            pron[m][unicodedata.normalize("NFC", form)] += 1

    def best(k, m):
        c = forms.get((k, m))
        return c.most_common(1)[0][0] if c else "—"

    ROWS = [("他", "3ms", "3ms", None), ("她", "3fs", "3fs", None), ("你（男）", "2ms", "2ms", "2ms"),
            ("你（女）", "2fs", "2fs", "2fs"), ("我", "1cs", "1cs", None), ("他們", "3cp", "3mp", None),
            ("你們（男）", "2mp", "2mp", "2mp"), ("你們（女）", "2fp", "2fp", "2fp"), ("我們", "1cp", "1cp", None)]
    vt = ["| 人稱 | 完成式 | 未完成式 | 命令式 |", "|------|----------|----------|----------|"]
    for zh, pc, ic, vc in ROWS:
        pf = best("8104", f"HVqp{pc}"); im = best("8104", f"HVqi{ic}")
        iv = best("8104", f"HVqv{vc}") if vc else ""
        vt.append(f"| {zh} | {pf} | {im} | {iv} |")
    open(os.path.join(OUT, "generated/gram-verb.md"), "w", encoding="utf-8").write("\n".join(vt) + "\n")
    nt = ["| 詞 | 意思 | 單數 | 複數 |", "|------|--------|------|------|"]
    for k, zh in [("4428", "王"), ("1697", "話語"), ("3117", "日子"), ("1121", "兒子"), ("776", "地"), ("5892", "城"),
                  ("802", "女人")]:
        row = None
        for g in "mfbc":
            a, b = best(k, f"HNc{g}sa"), best(k, f"HNc{g}pa")
            if a != "—" and b != "—": row = (a, b); break
        nt.append(f"| {lex['H' + k][0]} | {zh} | {row[0] if row else '—'} | {row[1] if row else '—'} |")
    open(os.path.join(OUT, "generated/gram-noun.md"), "w", encoding="utf-8").write("\n".join(nt) + "\n")
    at = ["| | 單數 | 複數 |", "|------|------|------|", f"| 陽性 | {best('2896','HAamsa')} | {best('2896','HAampa')} |",
          f"| 陰性 | {best('2896','HAafsa')} | {best('2896','HAafpa')} |"]
    open(os.path.join(OUT, "generated/gram-adj.md"), "w", encoding="utf-8").write("\n".join(at) + "\n")
    ZH = {"1cs": "我", "2ms": "你（男）", "2fs": "你（女）", "3ms": "他", "3fs": "她", "1cp": "我們", "2mp": "你們（男）",
          "3mp": "他們", "3fp": "她們", "1cc": "我"}
    pt = ["| 人稱 | 形式 | 次數 |", "|------|------|------|"]
    for code in ["1cs", "2ms", "2fs", "3ms", "3fs", "1cp", "2mp", "3mp", "3fp"]:
        c = pron.get("HPp" + code)
        if c:
            pt.append(f"| {ZH[code]} | {c.most_common(1)[0][0]} | {sum(c.values()):,} |")
    open(os.path.join(OUT, "generated/gram-pron.md"), "w", encoding="utf-8").write("\n".join(pt) + "\n")
    st = ["| 詞尾 | 加上詞尾的形式 | 意思 |", "|------|------|------|"]
    for code, zh in [("1cs", "我的話"), ("2ms", "你（男）的話"), ("2fs", "你（女）的話"), ("3ms", "他的話"), ("3fs", "她的話"),
                     ("1cp", "我們的話"), ("2mp", "你們的話"), ("3mp", "他們的話")]:
        f = best("1697", f"HNcmsc/Sp{code}")
        if f == "—": f = best("1697", f"HNcmsa/Sp{code}")
        if f != "—": st.append(f"| {ZH[code]} | {f} | {zh} |")
    open(os.path.join(OUT, "generated/gram-suffix.md"), "w", encoding="utf-8").write("\n".join(st) + "\n")

    # ---------- song cards
    hymns = json.load(open(os.path.join(SRC, "hymns.json"), encoding="utf-8"))
    # CUV text for the song cards comes from the ai-eden project (the repo's standard Bible source).
    # Default: the sibling checkout ../ai-eden; override with AI_EDEN_DIR.
    cuv_path = os.path.join(os.environ.get("AI_EDEN_DIR", os.path.join(os.path.dirname(ROOT), "ai-eden")), "data/cuv.json")
    if not os.path.exists(cuv_path):
        sys.exit(f"CUV not found at {cuv_path} - set AI_EDEN_DIR to your ai-eden checkout")
    cuvd = json.load(open(cuv_path, encoding="utf-8"))
    byref = collections.defaultdict(list)
    for r, l, m, t in toks: byref[r].append((l, m, t))
    for sid, sg in SONGS.items():
        words = [strip_cantillation(t) for _, _, t in byref[sg["ref"]]][sg["start"]:]
        assert sum(sg["chunks"]) == len(words), (sid, len(words))
        i = 0; hl = []
        for c in sg["chunks"]:
            hl.append("| " + " ".join(words[i:i + c])); i += c
        tl = ["| " + t for t in sg["translit"]]
        cv = cuvd[sg["cuv"][0]][sg["cuv"][1][0]]
        cv = re.sub(r"^（[^）]*）", "", cv)
        for k in sg["keys"]:
            if k not in GLOSS: sys.exit(f"missing gloss (song {sid}): {k}")
        card = [f"> **唱一唱：{sg['zh']}**", ">", "> " + "\n> ".join(hl), ">", "> *讀音（簡化，可跟著錄音唱）*", ">",
                "> " + "\n> ".join(tl), ">", f"> 和合本：{cv}", ">",
                "> | 字 | 意思 | 全舊約次數 |", "> |------|------------|------|"]
        for k in sg["keys"]:
            card.append(f"> | {lex['H' + k][0]} | {GLOSS[k]} | {cnt[k]:,} |")
        if sg["hymn"]:
            h = hymns[sg["hymn"]]
            card += [">", "> 同主題的公有領域聖詩（英文）：", ">", f"> {h['title']}", ">", f"> {h['author']}"]
        open(os.path.join(OUT, f"generated/song-{sid}.md"), "w", encoding="utf-8").write("\n".join(card) + "\n")
    # hymn texts for the songs appendix
    hy = []
    for hid, h in hymns.items():
        hy.append(f"### {h['title']}\n\n作者：{h['author']}\n\n曲調：{h['tune']}\n")
        for st in h["stanzas"]:
            hy.append("\n".join("| " + ln for ln in st) + "\n")
        hy.append(f"來源：{h['source']}\n")
    open(os.path.join(OUT, "generated/hymns.md"), "w", encoding="utf-8").write("\n".join(hy))

    # ---------- series vocabulary (needs scripts/mine-hebrew-wordstudies.py output)
    ws_path = os.path.join(SRC, "series-wordstudies.json")
    if os.path.exists(ws_path):
        ws = json.load(open(ws_path, encoding="utf-8"))
        perbook = collections.defaultdict(collections.Counter)
        for r in ws["rows"]:
            for k in r["lemmas"]: perbook[k][r["book"]] += 1
        cand = []
        for k, v in ws["lemmas"].items():
            e = lex.get("H" + k)
            if not e or not e[1] or e[1].startswith("n-pr") or e[1] not in ("v", "a") and not e[1].startswith("n"): continue
            if len(v["books"]) >= 9 and k not in ("1961", "1121", "259", "5414", "1419", "8147", "935", "369", "1471"):
                cand.append((len(v["books"]), cnt[k], k))
        cand.sort(key=lambda x: (-x[0], -x[1]))
        miss = [k for _, _, k in cand if k not in GLOSS]
        if miss: sys.exit(f"missing gloss (series): {miss}")
        sv = ["| 原文 | 詞類 | 意思 | 全舊約次數 | 本系列幾卷 | 最常出現在 |", "|------------|--------|----------------------|----------|--------|----------------------------|"]
        for nb, n, k in cand:
            top3 = "、".join(FOLDER_ZH.get(b, b) for b, _ in perbook[k].most_common(3))
            f, pos = lex["H" + k]
            f = FORM_FIX.get(k, f); pos = POS_FIX.get(k, pos)
            sv.append(f"| {f} | {pos_zh(pos)} | {GLOSS[k]} | {n:,} | {nb} | {top3} |")
        open(os.path.join(OUT, "generated/series-vocab.md"), "w", encoding="utf-8").write("\n".join(sv) + "\n")
        stats["series_words"] = len(cand)
        stats["series_rows"] = len(ws["rows"])
        stats["series_files"] = len({r["file"] for r in ws["rows"]})
        stats["series_books"] = len({r["book"] for r in ws["rows"]})
        json.dump(stats, open(os.path.join(OUT, "generated/stats.json"), "w"), ensure_ascii=False, indent=1)
    print("ok", total, nlem, len(lines), "tokens in Gen 1:1-5;", dict(verbs), dict(asp))


if __name__ == "__main__":
    main()
