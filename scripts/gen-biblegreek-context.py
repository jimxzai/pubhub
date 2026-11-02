#!/usr/bin/env python3
"""Generate books/bible/Biblegreek/96-appendix-3-word-contexts.md  (phase 2-3 of the Greek volume).

Input : docs/sources/biblegreek/wordstudy-ledger-v2.tsv (from extract-greek-wordstudy-v2.py; only level=A rows, i.e. verse-verified, are used)
        docs/sources/biblegreek/morphgnt/*.txt
Output: the appendix + generated/context-stats.json
Every Greek form, lemma, count and verse excerpt comes from the corpus. Only the Chinese gloss/note
column is the repo's own word-study text, shown as such.
"""
import collections, csv, glob, json, os, re, unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "docs/sources/biblegreek")
OUT = os.path.join(ROOT, "books/bible/Biblegreek")
ZH = {"61-Mt": "馬太福音", "62-Mk": "馬可福音", "63-Lk": "路加福音", "64-Jn": "約翰福音", "65-Ac": "使徒行傳",
      "66-Ro": "羅馬書", "67-1Co": "哥林多前書", "68-2Co": "哥林多後書", "69-Ga": "加拉太書", "70-Eph": "以弗所書",
      "71-Php": "腓立比書", "72-Col": "歌羅西書", "73-1Th": "帖撒羅尼迦前書", "74-2Th": "帖撒羅尼迦後書",
      "75-1Ti": "提摩太前書", "76-2Ti": "提摩太後書", "77-Tit": "提多書", "78-Phm": "腓利門書", "79-Heb": "希伯來書",
      "80-Jas": "雅各書", "81-1Pe": "彼得前書", "82-2Pe": "彼得後書", "83-1Jn": "約翰一書", "84-2Jn": "約翰二書",
      "85-3Jn": "約翰三書", "86-Jud": "猶大書", "87-Re": "啟示錄"}
SHORT = {"61-Mt": "太", "62-Mk": "可", "63-Lk": "路", "64-Jn": "約", "65-Ac": "徒", "66-Ro": "羅", "67-1Co": "林前",
         "68-2Co": "林後", "69-Ga": "加", "70-Eph": "弗", "71-Php": "腓", "73-1Th": "帖前", "74-2Th": "帖後",
         "78-Phm": "門", "79-Heb": "來", "80-Jas": "雅", "81-1Pe": "彼前", "82-2Pe": "彼後", "83-1Jn": "約壹",
         "84-2Jn": "約貳", "85-3Jn": "約參", "86-Jud": "猶", "87-Re": "啟"}
CORE_N = 40
POS = {}
FUNCTION_POS = {"RA", "C-", "P-", "RP", "RD", "RR", "RI", "D-", "X-", "I-"}
PER_WORD = 6


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c)).replace("ς", "σ")


def load():
    verses = collections.defaultdict(list)  # (book,ch,v) -> [(text, lemma, normform)]
    counts = collections.defaultdict(collections.Counter)  # lemma -> book -> n
    POS[""] = None
    for f in sorted(glob.glob(os.path.join(SRC, "morphgnt/*.txt"))):
        book = os.path.basename(f)[:-4]
        for line in open(f, encoding="utf-8"):
            p = line.split()
            if len(p) != 7:
                continue
            verses[(book, int(p[0][2:4]), int(p[0][4:6]))].append((p[3], p[6], norm(re.sub(r"[^\w]", "", p[5]))))
            counts[p[6]][book] += 1
            POS[p[6]] = p[1]
    return verses, counts


def clean(s):
    s = re.sub(r"\{\\greekfont\s*([^}]*)\}`?\{?=?latex\}?", r"\1", s)
    s = re.sub(r"[`*]", "", s).replace("|", "／").strip()
    return s


DROPPED = {"conflict": 0, "number": 0}
CONFLICT = re.compile(r"無條件|不求回報|不計回報|情感上的熱度|神聖的愛|友誼的愛|dynamite|英文.{0,40}(?:字源|字根|來源|同源|衍生|相關)|(?:字源|字根).{0,15}英文|首次出現在此|罕見地與約翰福音同用")           # contradicts chapter 5 (agapao is not 'unconditional love')
NUMBER = re.compile(r"[\d一二三四五六七八九十百兩餘]+\s*(?:次|處|回)(?!的死)")  # counts quoted in a note are not re-verified here


CLAUSE_DROP = re.compile(NUMBER.pattern + r"|字根|字源|同源|由此而來|衍生|見(?:上文|下方|上方|下文)[^，；。]*|見「[^」]*」(?:一節|專節|專題)|Strong's\s*\d+")


def short_note(note):
    """Whole note is dropped if it contradicts chapter 5; otherwise only the offending CLAUSES (a count, a root/etymology claim,
    a pointer to a section Part Two does not have) are removed, so the rest of a useful note survives."""
    note = clean(note).lstrip("：: ")
    if CONFLICT.search(note):
        DROPPED["conflict"] += 1
        return ""
    keep = []
    for cl in re.split(r"(?<=[，；。,;])", note):
        if CLAUSE_DROP.search(cl):
            DROPPED["number"] += 1
            continue
        keep.append(cl)
    note = "".join(keep).strip("，；。,; ")
    if len(note) <= 100:
        return note
    cut = re.split(r"[。；]", note)[0]
    return cut if 12 <= len(cut) <= 110 else ""


def first_ref(loc):
    m = re.match(r"\s*(\d+):(\d+)", re.sub(r"[`*]", "", loc))
    return (int(m.group(1)), int(m.group(2))) if m else None


def excerpt(words, lemma, span=7):
    idx = next((i for i, w in enumerate(words) if w[1] == lemma), None)
    if idx is None:
        return None
    lo, hi = max(0, idx - span), min(len(words), idx + span + 1)
    txt = re.sub("[\u2e00-\u2e0d]", "", " ".join(w[0] for w in words[lo:hi]))  # drop SBLGNT apparatus sigla
    return ("… " if lo else "") + txt + (" …" if hi < len(words) else "")


def main():
    verses, counts = load()
    rows = list(csv.DictReader(open(os.path.join(SRC, "wordstudy-ledger-v2.tsv"), encoding="utf-8"), delimiter="\t"))
    for r in rows:   # v2 columns -> the names this script uses
        r["lemma"], r["location"] = r["lemmas"], r["refs"]
    total = len(rows)
    stat = collections.Counter(r["level"] for r in rows)
    ok = [r for r in rows if r["level"] == "A" and r["lemma"] and first_ref(r["location"]) and len(r["headword"].split()) == 1]
    by = collections.defaultdict(list)
    for r in ok:
        # a phrase headword matches several lemmas: file the row under the rarest one in the NT
        # (the content word), never under an article, preposition or conjunction
        lems = [l for l in r["lemma"].split(";") if l in counts and POS.get(l) not in FUNCTION_POS and l != "εἰμί"]
        if not lems:
            continue
        key = min(lems, key=lambda l: sum(counts[l].values()))
        r["lemma"] = key
        by[key].append(r)
    ranked = sorted(by, key=lambda l: (-len({r["book"] for r in by[l]}), -len(by[l])))
    core = [l for l in ranked if len({r["book"] for r in by[l]}) >= 2][:CORE_N]

    out = ["---", "title: 附錄", "subtitle: 核心字在各卷的用法", "author: PubHub 三書精讀系統", "date: 2026年11月",
           "publisher: 三書精讀出版系統", "---", "",
           "# 附錄：核心字在各卷的用法 (Core Words in Context) {.unnumbered}", "",
           f"> 本附錄蒐集本系列各卷「原文研讀」表格裏被研讀最多的希臘字。原有 {total:,} 條不重複的字詞記錄，"
           f"逐條對照 SBLGNT 語料：**{stat['A']:,} 條逐節通過**（標示的每個希臘字都出現在所引經節，本附錄只用這一級）；"
           f"另有 {stat['B']:,} 條只能核對到章、{stat['C']:,} 條只能核對到本卷（這兩級見卷二）；**{stat['X']:,} 條不符而剔除**。"
           "「希臘文」欄的經節摘錄、次數與詞目，全由語料計算；「本系列的註解」欄是各卷作者當時寫的中文註解，"
           "只在通過核對的條目中引用，**其中涉及其他經卷或七十士譯本的說法，不在本語料的核對範圍內**。"
           "另有註解因下列兩種原因略去：含「無條件的愛」一類與第五章論證衝突的說法；含註解作者自己數出的次數或處數（未逐一重算）。本附錄只收單字詞目，片語的註解不掛在單一個字上。"
           "略去的註解數見下方。", ""]
    n_used = 0
    for lemma in core:
        tot = sum(counts[lemma].values())
        top = counts[lemma].most_common(3)
        gl = collections.Counter(clean(r["gloss"]).split("、")[0] for r in by[lemma] if 0 < len(clean(r["gloss"])) <= 12)
        title = lemma + (" — " + gl.most_common(1)[0][0] if gl else "")
        out += [f"## {title}", "",
                f"全新約 {tot:,} 次；最多的三卷：" + "、".join(f"{ZH[b]} {n}" for b, n in top) +
                f"。本系列有 {len({r['book'] for r in by[lemma]})} 卷的原文研讀表格逐節核對過這個字（下表每卷只列一處，最多 6 卷）。", "",
                "| 卷 | 節 | 希臘文（摘錄） | 本系列的註解 |", "|---------|--------|------------------------------|------------------------|"]
        seen_books, picked = set(), []
        cand = sorted(by[lemma], key=lambda r: (r["book"] in seen_books, 0 if short_note(r["note"]) else 1))
        for r in sorted(by[lemma], key=lambda r: (0 if short_note(r["note"]) else 1, r["book"])):
            if r["book"] in seen_books:
                continue
            seen_books.add(r["book"]); picked.append(r)
            if len(picked) == PER_WORD:
                break
        for r in picked:
            ch, v = first_ref(r["location"])
            ex = excerpt(verses[(r["book"], ch, v)], lemma)
            if not ex:
                continue
            gloss = clean(r["gloss"])
            if CONFLICT.search(gloss):
                gloss = re.sub(r"[（(][^）)]*(?:無條件|不求回報)[^）)]*[）)]", "", gloss)
                DROPPED["conflict"] += 1
            note = short_note(r["note"])
            text = "：".join(x for x in (gloss, note) if x)
            out.append(f"| {SHORT[r['book']]} | {ch}:{v} | {ex} | {text} |")
            n_used += 1
        out.append("")
    out.append(f"> 略去的註解：與第五章衝突 {DROPPED['conflict']} 則、含自數次數 {DROPPED['number']} 則（計算時每則可能被檢查不只一次）。")
    open(os.path.join(OUT, "96-appendix-3-word-contexts.md"), "w", encoding="utf-8").write("\n".join(out))
    json.dump({"ledger_rows": total, **{"level_" + k: v for k, v in stat.items()}, "core_words": len(core), "rows_printed": n_used},
              open(os.path.join(OUT, "generated/context-stats.json"), "w"), ensure_ascii=False, indent=1)
    print("core words", len(core), "rows printed", n_used, dict(stat))


if __name__ == "__main__":
    main()
