#!/usr/bin/env python3
"""Generate the paradigm and example tables for 04b-basic-grammar.md from MorphGNT SBLGNT.

Every form printed is the most frequent attested form for that cell in the corpus (not typed from
memory); an empty cell prints '—'. Every example phrase is asserted to occur in its verse.
Writes books/bible/Biblegreek/generated/gram-*.md
"""
import collections, glob, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(ROOT, "docs/sources/biblegreek/morphgnt")
OUT = os.path.join(ROOT, "books/bible/Biblegreek/generated")
SIGLA = re.compile("[⸀-⸍]")
CASES = [("N", "主格"), ("G", "屬格"), ("D", "與格"), ("A", "賓格"), ("V", "呼格")]
PERSONS = [("1", "第一人稱"), ("2", "第二人稱"), ("3", "第三人稱")]


def load():
    toks, verse = [], collections.defaultdict(list)
    for f in sorted(glob.glob(os.path.join(CORPUS, "*.txt"))):
        book = os.path.basename(f)[:-4]
        for line in open(f, encoding="utf-8"):
            p = line.split()
            if len(p) == 7:
                toks.append(p)
                verse[(book, int(p[0][2:4]), int(p[0][4:6]))].append(p)
    return toks, verse


def table(rows, header):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("------" for _ in header) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(out) + "\n"


def main():
    toks, verse = load()
    os.makedirs(OUT, exist_ok=True)

    def best(pred):
        c = collections.Counter(t[5] for t in toks if pred(t))
        return c.most_common(1)[0][0] if c else "—"

    # --- article
    cols = [("S", "M", "陽單"), ("S", "F", "陰單"), ("S", "N", "中單"), ("P", "M", "陽複"), ("P", "F", "陰複"), ("P", "N", "中複")]
    rows = []
    for c, zh in CASES[:4]:  # the article has no vocative
        row = [zh]
        for n, g, _ in cols:
            row.append(best(lambda t: t[6] == "ὁ" and t[1] == "RA" and t[2][4] == c and t[2][5] == n and t[2][6] == g))
        rows.append(row)
    open(os.path.join(OUT, "gram-article.md"), "w", encoding="utf-8").write(table(rows, ["格"] + [z for _, _, z in cols]))

    # --- nouns
    def noun(lemma):
        rows = []
        for c, zh in CASES:
            rows.append([zh, best(lambda t: t[6] == lemma and t[1] == "N-" and t[2][4] == c and t[2][5] == "S"),
                         best(lambda t: t[6] == lemma and t[1] == "N-" and t[2][4] == c and t[2][5] == "P")])
        return rows
    parts = []
    for lemma, label in (("λόγος", "第二變格（陽性）：`λόγος` 話、道"), ("ἡμέρα", "第一變格（陰性）：`ἡμέρα` 日子"),
                         ("χάρις", "第三變格（陰性）：`χάρις` 恩典")):
        parts += [f"**{label}**", "", table(noun(lemma), ["格", "單數", "複數"])]
    open(os.path.join(OUT, "gram-nouns.md"), "w", encoding="utf-8").write("\n".join(parts))

    # --- verbs
    def verb(lemma, tense, mood="I", voice=None):
        rows = []
        for p, pz in PERSONS:
            rows.append([pz] + [best(lambda t: t[6] == lemma and t[1] == "V-" and t[2][0] == p and t[2][1] == tense and
                                     t[2][3] == mood and t[2][5] == n and (voice is None or t[2][2] == voice))
                                for n in ("S", "P")])
        return rows
    parts = []
    for lemma, tense, voice, label in (("εἰμί", "P", None, "`εἰμί`（是）現在式"), ("εἰμί", "I", None, "`εἰμί`（是）未完成式"),
                                       ("λέγω", "P", "A", "`λέγω`（說）現在式主動"), ("πιστεύω", "P", "A", "`πιστεύω`（信）現在式主動"),
                                       ("πιστεύω", "A", "A", "`πιστεύω`（信）簡單過去式主動")):
        parts += [f"**{label}，直述語氣**", "", table(verb(lemma, tense, "I", voice), ["人稱", "單數", "複數"])]
    open(os.path.join(OUT, "gram-verbs.md"), "w", encoding="utf-8").write("\n".join(parts))

    # --- examples (each asserted)
    EX = [
        ("主格：主詞", "64-Jn", 1, 1, "ὁ λόγος ἦν πρὸς τὸν θεόν", "道與神同在（`λόγος` 是主詞）"),
        ("屬格：「……的」", "64-Jn", 1, 12, "τέκνα θεοῦ", "神的兒女（`θεοῦ`）"),
        ("與格：在……", "64-Jn", 1, 2, "ἐν ἀρχῇ", "在起初（`ἀρχῇ`）"),
        ("賓格：受詞，或介系詞後的名詞", "64-Jn", 1, 1, "πρὸς τὸν θεόν", "與神同在（`πρός` 接賓格）"),
        ("呼格：呼喚", "61-Mt", 15, 22, "κύριε", "主啊"),
        ("`ἐκ` 接屬格", "64-Jn", 1, 13, "ἐκ θεοῦ", "從神而生"),
        ("`διά` 接屬格", "64-Jn", 1, 3, "δι’ αὐτοῦ", "藉著他"),
        ("`εἰς` 接賓格", "64-Jn", 3, 17, "εἰς τὸν κόσμον", "進入世界"),
        ("分詞：像形容詞", "64-Jn", 3, 16, "ὁ πιστεύων", "那相信的人（「正在信的」）"),
        ("不定詞：動詞的名詞形式", "64-Jn", 1, 12, "γενέσθαι", "成為（子女）"),
        ("`οὐ` 否定直述句", "64-Jn", 1, 5, "οὐ κατέλαβεν", "沒有勝過／領會"),
        ("`μή` 否定虛擬句", "64-Jn", 3, 16, "μὴ ἀπόληται", "使他不致滅亡"),
        ("`ἵνα` 引出目的", "64-Jn", 3, 16, "ἵνα πᾶς", "為要使凡……"),
        ("`γάρ` 說明理由", "64-Jn", 3, 16, "γὰρ ἠγάπησεν", "因為（神）愛了"),
    ]
    rows = []
    for label, book, ch, v, phrase, zh in EX:
        text = SIGLA.sub("", " ".join(t[3] for t in verse[(book, ch, v)]))
        if phrase not in text:
            sys.exit(f"example not in verse: {book} {ch}:{v} {phrase!r}\n  verse: {text}")
        ref = {"64-Jn": "約", "61-Mt": "太"}[book]
        rows.append([label, f"{ref} {ch}:{v}", phrase, zh])
    open(os.path.join(OUT, "gram-examples.md"), "w", encoding="utf-8").write(table(rows, ["語法點", "經節", "希臘文", "意思"]))

    # --- small words
    cnt = collections.Counter(t[6] for t in toks)
    small = [("καί", "和、並且"), ("δέ", "但、而"), ("γάρ", "因為（說明理由）"), ("ὅτι", "因為／……這件事"), ("ἵνα", "為要"),
             ("ἀλλά", "但是（強烈對比）"), ("οὖν", "所以"), ("εἰ", "如果"), ("οὐ", "不（否定事實）"), ("μή", "不（否定意願、命令、可能）")]
    open(os.path.join(OUT, "gram-small.md"), "w", encoding="utf-8").write(
        table([[w, f"{cnt[w]:,}", zh] for w, zh in small], ["詞", "新約次數", "意思"]))
    print("ok", {k: len(open(os.path.join(OUT, f"gram-{k}.md")).read().splitlines()) for k in ("article", "nouns", "verbs", "examples", "small")})


if __name__ == "__main__":
    main()
