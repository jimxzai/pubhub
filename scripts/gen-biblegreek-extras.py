#!/usr/bin/env python3
"""Generate two appendices of books/bible/Biblegreek from the MorphGNT corpus:
  96-appendix-1-reading-map.md   one starter verse per NT book + words to stop on (phase 5)
  96-appendix-2-practice.md      practice questions whose answers are computed (phase 4)
Any chosen word that is not in its verse, or any verse that is missing, aborts the build.
"""
import collections, glob, importlib.util, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(ROOT, "docs/sources/biblegreek/morphgnt")
OUT = os.path.join(ROOT, "books/bible/Biblegreek")
spec = importlib.util.spec_from_file_location("gd", os.path.join(ROOT, "scripts/gen-biblegreek-data.py"))
gd = importlib.util.module_from_spec(spec); spec.loader.exec_module(gd)
ctx_spec = importlib.util.spec_from_file_location("gc", os.path.join(ROOT, "scripts/gen-biblegreek-context.py"))
gc = importlib.util.module_from_spec(ctx_spec); ctx_spec.loader.exec_module(gc)

SIGLA = re.compile("[⸀-⸍]")
# book file stem -> (zh name, chapter, verse, [lemmas to stop on])
MAP = [
    ("61-Mt", 28, 19, ["μαθητεύω", "ἔθνος", "βαπτίζω", "ὄνομα"]),
    ("62-Mk", 1, 1, ["ἀρχή", "εὐαγγέλιον", "Χριστός"]),
    ("63-Lk", 19, 10, ["ζητέω", "σῴζω", "ἀπόλλυμι", "υἱός"]),
    ("64-Jn", 1, 14, ["λόγος", "σάρξ", "σκηνόω", "δόξα", "χάρις", "ἀλήθεια"]),
    ("65-Ac", 1, 8, ["δύναμις", "μάρτυς", "πνεῦμα", "γῆ"]),
    ("66-Ro", 1, 16, ["εὐαγγέλιον", "δύναμις", "σωτηρία", "πιστεύω"]),
    ("67-1Co", 13, 13, ["πίστις", "ἐλπίς", "ἀγάπη"]),
    ("68-2Co", 5, 17, ["καινός", "κτίσις", "ἀρχαῖος"]),
    ("69-Ga", 2, 20, ["ζάω", "πίστις", "ἀγαπάω", "παραδίδωμι"]),
    ("70-Eph", 2, 8, ["χάρις", "σῴζω", "πίστις", "δῶρον"]),
    ("71-Php", 4, 4, ["χαίρω", "κύριος"]),
    ("72-Col", 1, 15, ["εἰκών", "ἀόρατος", "πρωτότοκος", "κτίσις"]),
    ("73-1Th", 5, 16, ["χαίρω", "πάντοτε"]),
    ("74-2Th", 3, 3, ["πιστός", "κύριος", "στηρίζω"]),
    ("75-1Ti", 2, 5, ["θεός", "μεσίτης", "ἄνθρωπος"]),
    ("76-2Ti", 3, 16, ["γραφή", "θεόπνευστος", "ὠφέλιμος", "διδασκαλία"]),
    ("77-Tit", 2, 11, ["χάρις", "σωτήριος", "ἐπιφαίνω"]),
    ("78-Phm", 1, 16, ["δοῦλος", "ἀδελφός", "ἀγαπητός"]),
    ("79-Heb", 11, 1, ["πίστις", "ἐλπίζω", "ὑπόστασις", "ἔλεγχος"]),
    ("80-Jas", 2, 17, ["πίστις", "ἔργον", "νεκρός"]),
    ("81-1Pe", 1, 3, ["ἀναγεννάω", "ἐλπίς", "ἀνάστασις", "ἔλεος"]),
    ("82-2Pe", 3, 18, ["αὐξάνω", "χάρις", "γνῶσις"]),
    ("83-1Jn", 4, 8, ["ἀγαπάω", "ἀγάπη", "γινώσκω"]),
    ("84-2Jn", 1, 6, ["ἀγάπη", "ἐντολή", "περιπατέω"]),
    ("85-3Jn", 1, 4, ["χαρά", "τέκνον", "ἀλήθεια", "περιπατέω"]),
    ("86-Jud", 1, 3, ["πίστις", "ἅγιος", "παραδίδωμι"]),
    ("87-Re", 1, 8, ["Ἄλφα", "παντοκράτωρ", "ἔρχομαι"]),
]


def load():
    tok = collections.defaultdict(list)   # (book,ch,v) -> list of token lists
    counts = collections.Counter()
    for f in sorted(glob.glob(os.path.join(CORPUS, "*.txt"))):
        book = os.path.basename(f)[:-4]
        for line in open(f, encoding="utf-8"):
            p = line.split()
            if len(p) == 7:
                tok[(book, int(p[0][2:4]), int(p[0][4:6]))].append(p)
                counts[p[6]] += 1
    return tok, counts


def vtext(tok, b, c, v):
    t = tok.get((b, c, v))
    if not t:
        sys.exit(f"missing verse {b} {c}:{v}")
    return SIGLA.sub("", " ".join(x[3] for x in t))


def main():
    tok, counts = load()
    head = lambda t, s: ["---", f"title: 附錄", f"subtitle: {s}", "author: PubHub 三書精讀系統", "date: 2026年11月",
                         "publisher: 三書精讀出版系統", "---", ""]
    # ---------- reading map
    m = head("", "新約各卷讀經地圖") + [
        "# 附錄：新約二十七卷讀經地圖 (A Reading Map of the New Testament) {.unnumbered}", "",
        "> 每卷選一節值得停下來讀的經文，列出希臘文與幾個值得停一下的字。希臘文與次數由 SBLGNT 語料取得；"
        "「為甚麼選這節」只是編者的挑選，不是唯一的答案。這些字不需要背，只要在讀這一節時認一認它們的樣子。", "",
        "| 卷 | 節 | 希臘文 | 停一下的字（詞目與新約次數） |", "|--------|------|--------------------------|------------------------------|"]
    for b, c, v, lemmas in MAP:
        t = tok.get((b, c, v))
        if not t:
            sys.exit(f"missing {b} {c}:{v}")
        have = {x[6] for x in t}
        bad = [l for l in lemmas if l not in have]
        if bad:
            sys.exit(f"{b} {c}:{v}: lemma(s) not in verse: {bad}")
        words = "、 ".join(f"{l} ({counts[l]:,})" for l in lemmas)
        m.append(f"| {gc.ZH[b]} | {c}:{v} | {vtext(tok, b, c, v)} | {words} |")
    open(os.path.join(OUT, "96-appendix-1-reading-map.md"), "w", encoding="utf-8").write("\n".join(m) + "\n")

    # ---------- practice
    J = lambda c, v: tok[("64-Jn", c, v)]
    j15 = [x for v in range(1, 6) for x in J(1, v)]
    q = head("", "練習題與答案") + ["# 附錄：練習題與答案 (Practice and Answers) {.unnumbered}", "",
        "> 答案裏的次數、詞形與形態由 SBLGNT 語料與形態標注計算；第 1 題的轉寫與各題的說明文字是人工寫的。做之前請先自己試試。", ""]
    n = 0

    def add(title, ask, ans):
        nonlocal n
        n += 1
        q.extend([f"## 第 {n} 題　{title}", "", ask, "", f"**答案：** {ans}", ""])

    add("認字母（第三章）", "把下列約 1:1-5 裏的字用拉丁字母拼出來：`ἀρχή`、`λόγος`、`ζωή`、`φῶς`、`σκοτία`。",
        "arche、logos、zoe、phos、skotia（按通行的簡化轉寫；氣號與重音忽略）。")
    assert all(any(x[6] == w for x in j15) for w in ["ἀρχή", "λόγος", "ζωή", "φῶς", "σκοτία"])
    t1 = J(1, 1)
    th = [(x[3].strip(",.;"), x[2]) for x in t1 if x[6] == "θεός"]
    add("認格（第四章）", "約 1:1 裏 `θεός` 出現兩次，各是甚麼格？為甚麼詞尾不同？",
        "；".join(f"`{w}` 是{gd.CASE[p[4]]}" for w, p in th) + "。賓格是因為介系詞 `πρός` 接賓格（「與神同在」）；主格是「道就是神」裏的述語名詞（這句的主詞是 `ὁ λόγος`）。詞尾不同，是因為它在句中的角色不同。")
    hn = [(i, x) for i, x in enumerate(j15) if x[6] == "εἰμί"]
    per = collections.Counter(int(x[0][4:6]) for _, x in hn)
    add("數動詞（第四章）", "約 1:1-5 裏詞目 `εἰμί`（是／有）出現幾次？各在哪一節？",
        f"共 {len(hn)} 次：" + "、".join(f"第 {v} 節 {c} 次" for v, c in sorted(per.items())) + "。")
    fin = [x for x in j15 if x[1] == "V-" and x[2][3] in "I"]
    rows = []
    seen = set()
    for x in fin:
        k = (x[3].strip(",.;"), x[2])
        if k in seen:
            continue
        seen.add(k); rows.append(f"`{k[0]}`（{x[6]}）：{gd.TENSE[x[2][1]]}")
    add("認時態（第六章）", "列出約 1:1-5 裏所有直述語氣動詞（不重複），並說出各自的時態。", "；".join(rows) + "。")
    lemmas_top10 = [w for w, _ in counts.most_common(10)]
    in11 = [w for w in lemmas_top10 if any(x[6] == w for x in t1)]
    add("認常用字（第八章）", "新約最常見的十個詞目，哪些出現在約 1:1？",
        f"十個詞目是：{'、'.join(lemmas_top10)}。出現在約 1:1 的有：{'、'.join(in11)}。")
    jn = [x for v in range(7, 22) for x in tok[("83-1Jn", 4, v)]]
    ga = collections.Counter(x[6] for x in jn if x[6] in ("ἀγαπάω", "ἀγάπη", "ἀγαπητός"))
    add("數關鍵字（第五章）", "約壹 4:7-21 裏，`ἀγαπάω`、`ἀγάπη`、`ἀγαπητός` 各出現幾次？",
        "、".join(f"`{w}` {ga[w]} 次" for w in ("ἀγαπάω", "ἀγάπη", "ἀγαπητός")) + "。")
    rows = []
    for v in (15, 16, 17):
        for x in J(21, v):
            if x[6] in ("ἀγαπάω", "φιλέω"):
                rows.append(f"21:{v} `{x[3].strip(',.;·;')}`（{x[6]}，第{x[2][0]}人）")
    add("比較兩個「愛」（第五章）", "列出約 21:15-17 裏所有 `ἀγαπάω` 與 `φιλέω` 的形式，並注明人稱。",
        "；".join(rows) + "。注意：第 17 節耶穌第三次問時改用 `φιλέω`（該節 `Φιλεῖς` 出現兩次，是因為敘述者重述了耶穌的問話）。這個變化值得觀察，但本書第五章已經說明：不能單靠兩個動詞的對照表就推出兩種層次的愛。")
    mt = [x for x in tok[("61-Mt", 15, 22)] if x[6] == "ἐλεάω"][0]
    add("認語氣（第六章）", "太 15:22 的 `Ἐλέησόν`，是甚麼語氣、人稱與數？",
        f"{gd.MOOD[mt[2][3]]}語氣、{gd.TENSE[mt[2][1]]}時態、第 {mt[2][0]} 人、{gd.NUM[mt[2][5]]}數——就是一句命令式的呼求「求你憐憫我」。命令語氣裏的簡單過去式不是指過去，只是把這個呼求看成一個整體（見第六章）。")
    open(os.path.join(OUT, "96-appendix-2-practice.md"), "w", encoding="utf-8").write("\n".join(q) + "\n")
    print("map rows", len(MAP), "questions", n)


if __name__ == "__main__":
    main()
