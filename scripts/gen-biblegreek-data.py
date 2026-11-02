#!/usr/bin/env python3
"""Generate the data-driven parts of books/bible/Biblegreek from MorphGNT SBLGNT.

Writes:
  generated/stats.json            numbers quoted in prose (checked by --check)
  07-data-john1-parse.md          (included by chapter 07 build step)
  96-appendix-4-top-words.md        top-100 lemma table
Usage: gen-biblegreek-data.py [--check]
"""
import collections, glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(ROOT, "docs/sources/biblegreek/morphgnt")
OUT = os.path.join(ROOT, "books/bible/Biblegreek")

TENSE = {"P": "現在", "I": "未完成", "F": "將來", "A": "簡單過去", "X": "完成", "Y": "過完"}
VOICE = {"A": "主動", "M": "中間", "P": "被動"}
MOOD = {"I": "直述", "D": "命令", "S": "虛擬", "O": "願望", "N": "不定詞", "P": "分詞"}
CASE = {"N": "主格", "G": "屬格", "D": "與格", "A": "賓格", "V": "呼格"}
NUM = {"S": "單", "P": "複"}
GEN = {"M": "陽", "F": "陰", "N": "中"}
POS = {"N-": "名詞", "V-": "動詞", "A-": "形容詞", "P-": "介系詞", "C-": "連接詞", "D-": "副詞",
       "RA": "冠詞", "RP": "人稱代名詞", "RD": "指示代名詞", "RR": "關係代名詞", "RI": "疑問／不定代名詞",
       "X-": "小品詞", "I-": "感嘆詞"}

GLOSS = {
    "ὁ": "這／那（定冠詞）", "καί": "和、並且、也", "αὐτός": "他、她、它；自己", "σύ": "你", "δέ": "但、而",
    "ἐν": "在……裏", "ἐγώ": "我", "εἰμί": "是、有", "λέγω": "說", "εἰς": "進入、到", "οὐ": "不", "ὅς": "（關係代名詞）那……的",
    "οὗτος": "這個", "θεός": "神", "ὅτι": "因為、……這件事", "πᾶς": "全部、每一個", "γάρ": "因為", "μή": "不（非直述）",
    "ἐκ": "出自", "Ἰησοῦς": "耶穌", "ἐπί": "在……上", "κύριος": "主", "ἔχω": "有", "πρός": "朝向、與……同在",
    "γίνομαι": "成為、發生", "διά": "藉著、因為", "ἵνα": "為要", "ἀπό": "從", "ἀλλά": "但是", "ἔρχομαι": "來、去",
    "ποιέω": "做", "τίς": "誰？甚麼？", "ἄνθρωπος": "人", "τις": "某人、某物", "Χριστός": "基督", "ὡς": "如同",
    "εἰ": "如果", "οὖν": "所以", "ὁράω": "看見", "μετά": "與、在……之後", "κατά": "按著、對著", "ἀκούω": "聽",
    "πολύς": "多", "δίδωμι": "給", "πατήρ": "父", "ἡμέρα": "日子", "πνεῦμα": "靈、風、氣", "υἱός": "兒子",
    "ἤ": "或者", "ἀδελφός": "弟兄", "εἷς": "一", "ἑαυτοῦ": "他自己", "περί": "關於", "ἐάν": "若",
    "λόγος": "話、道", "λαλέω": "講說", "οἶδα": "知道", "οὐρανός": "天", "μαθητής": "門徒", "λαμβάνω": "接受、拿",
    "γῆ": "地", "ἐκεῖνος": "那個", "πίστις": "信、信實", "πιστεύω": "信", "μέγας": "大", "ἅγιος": "聖",
    "ἀποκρίνομαι": "回答", "οὐδείς": "沒有一個", "ὄνομα": "名", "γινώσκω": "認識、知道", "ὑπό": "被、在……之下",
    "ἀνήρ": "男人、丈夫", "ἐξέρχομαι": "出去", "τέ": "又、並且", "γυνή": "女人、妻子", "δύναμαι": "能夠",
    "θέλω": "願意、想要", "οὕτω(ς)": "這樣", "ἰδού": "看哪", "Ἰουδαῖος": "猶太人", "παρά": "在……旁邊、從……而來",
    "εἰσέρχομαι": "進去", "νόμος": "律法", "γράφω": "寫", "κόσμος": "世界", "καθώς": "正如", "μέν": "（對比小品詞）一方面",
    "εὑρίσκω": "找到", "χείρ": "手", "ἄγγελος": "天使、使者", "ὄχλος": "群眾", "ἁμαρτία": "罪", "ἄν": "（假設小品詞，不譯）",
    "ἔργον": "工作、行為", "δόξα": "榮耀", "πόλις": "城", "βασιλεία": "國度", "ἔθνος": "民族、外邦", "τότε": "那時",
    "Παῦλος": "保羅",
    # John 1:1-5 extras
    "ἀρχή": "起初、開端", "ζωή": "生命", "φῶς": "光", "σκοτία": "黑暗", "φαίνω": "照、顯出",
    "καταλαμβάνω": "抓住、勝過；領會", "οὐδέ": "也不、連……也沒有", "χωρίς": "沒有、離開",
}


def parse_desc(pos, parse):
    p = parse
    if pos == "V-":
        bits = []
        if p[1] != "-": bits.append(TENSE[p[1]])
        if p[2] != "-": bits.append(VOICE[p[2]])
        if p[3] != "-": bits.append(MOOD[p[3]])
        if p[0] != "-": bits.append(f"第{p[0]}人")
        if p[4] != "-": bits.append(CASE[p[4]])
        if p[5] != "-": bits.append(NUM[p[5]])
        if p[6] != "-": bits.append(GEN[p[6]])
        return POS[pos] + "：" + "·".join(bits)
    bits = []
    if p[4] != "-": bits.append(CASE[p[4]])
    if p[5] != "-": bits.append(NUM[p[5]])
    if p[6] != "-": bits.append(GEN[p[6]])
    return POS.get(pos, pos) + ("：" + "·".join(bits) if bits else "")


def load():
    toks = []
    for f in sorted(glob.glob(os.path.join(CORPUS, "*.txt"))):
        for line in open(f, encoding="utf-8"):
            p = line.split()
            if len(p) == 7:
                toks.append(p)
    return toks


def main():
    toks = load()
    counts = collections.Counter(t[6] for t in toks)
    pos = {t[6]: t[1] for t in toks}
    total = len(toks)
    top = counts.most_common(100)

    def cover(k):
        return round(sum(n for _, n in counts.most_common(k)) / total * 100, 1)

    stats = {
        "tokens": total, "lemmas": len(counts), "hapax": sum(1 for n in counts.values() if n == 1),
        "cover10": cover(10), "cover25": cover(25), "cover50": cover(50), "cover100": cover(100),
        "cover200": cover(200), "cover300": cover(300), "cover500": cover(500), "cover1000": cover(1000),
        "n_ge50": sum(1 for n in counts.values() if n >= 50),
        "cover_ge50": round(sum(n for n in counts.values() if n >= 50) / total * 100, 1),
    }
    for w in ["θεός", "λόγος", "ἀγάπη", "ἀγαπάω", "φιλέω", "πιστεύω", "χάρις", "ἁμαρτία", "ζωή", "φῶς",
              "ἀλήθεια", "κύριος", "πνεῦμα", "Χριστός", "σώζω", "δικαιοσύνη", "ἐκκλησία", "εὐαγγέλιον", "δύναμις"]:
        stats["n_" + w] = counts[w]
    os.makedirs(os.path.join(OUT, "generated"), exist_ok=True)
    json.dump(stats, open(os.path.join(OUT, "generated/stats.json"), "w"), ensure_ascii=False, indent=1)

    # --- top-100 appendix
    missing = [w for w, _ in top if w not in GLOSS]
    if missing:
        sys.exit(f"missing gloss: {missing}")
    rows = ["---", "title: 附錄：最常見的一百個希臘字", "subtitle: Top 100 Greek Words", "author: PubHub 三書精讀系統",
            "date: 2026年11月", "publisher: 三書精讀出版系統", "---", "",
            "# 附錄：最常見的一百個希臘字 (The Hundred Commonest Words) {.unnumbered}", "",
            f"> 次數由 SBLGNT 希臘文新約（MorphGNT 標注本）逐詞目（lemma）實際計數：全新約 {total:,} 個詞、{len(counts):,} 個詞目。"
            f"「累計」欄是這些字合起來佔全新約的百分比。中文意思只列最常見的一種，不是詞典定義。", "",
            "| # | 原文 | 詞類 | 次數 | 累計 | 常見意思 |", "|----|-------------|--------------------|---------|---------|----------------------|"]
    cum = 0
    for i, (w, n) in enumerate(top, 1):
        cum += n
        rows.append(f"| {i} | {w} | {POS.get(pos[w], pos[w])} | {n:,} | {cum / total * 100:.1f}% | {GLOSS[w]} |")
    rows.append("")
    open(os.path.join(OUT, "96-appendix-4-top-words.md"), "w", encoding="utf-8").write("\n".join(rows))

    # --- John 1:1-5 parse
    ref_ok = {f"0401{v:02d}" for v in range(1, 6)}
    lines = []
    for f in [os.path.join(CORPUS, "64-Jn.txt")]:
        for line in open(f, encoding="utf-8"):
            p = line.split()
            if len(p) == 7 and p[0] in ref_ok:
                lines.append(p)
    miss = sorted({p[6] for p in lines if p[6] not in GLOSS})
    if miss:
        sys.exit(f"missing gloss (John): {miss}")
    out = ["| 節 | 原文 | 詞目 | 形態 | 意思 |", "|----|-------------|-----------------|------------------------------------|----------------|"]
    for p in lines:
        v = int(p[0][4:6])
        word = p[3].strip(",.;·")
        out.append(f"| {v} | {word} | {p[6]} | {parse_desc(p[1], p[2])} | {GLOSS[p[6]]} |")
    open(os.path.join(OUT, "generated/john1-1-5-parse.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("ok", stats["tokens"], stats["lemmas"], len(lines), "tokens in Jn 1:1-5")


if __name__ == "__main__":
    main()
