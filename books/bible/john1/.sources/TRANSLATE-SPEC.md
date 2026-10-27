# 約翰一書 注疏引文逐句中譯規格

Repo: /Users/jimxiao/dev/pubhub   Book: books/bible/john1

Every `> "English…"` commentary quote in the 歷代注疏 section (66 in the book) gets a full Chinese translation.

## Format (exact)
Leave the quote line and its `> — ` attribution line BYTE-IDENTICAL. Directly after the attribution line, inside the same blockquote, add a blank `>` line and one translation line:

```
> "Who is he that with hands does handle the Word, except because The Word was made flesh, and dwelt in us?"
> — Augustine, *Ten Homilies on the First Epistle of John*, Homily 1.1 (NPNF¹ 7)
>
> 中譯：若不是因為「道成了肉身，住在我們中間」，誰能用手摸道呢？
```

- Prefix is exactly `中譯：` (full-width colon). Do NOT start the line with 「 (a checker treats `> 「` as a Chinese-only citation).
- One translation line per quote, no line breaks inside it.

## Translation rules
1. Faithful and complete: translate every clause; add nothing, explain nothing, drop nothing. No smoothing that changes the author's claim. Keep the author's register (Augustine's rhetoric, Calvin's argument, MacArthur's spoken style) but in natural written Traditional Chinese.
2. When the English quotes or closely renders Scripture, use the CUV (和合本) wording inside 「」 for that phrase, with house style 裏 (verify against books/bible/john1/.sources/cuv-1john-house.txt for 1 John; for other books use bible.fhl.net JSON `https://bible.fhl.net/json/qb.php?chineses=<書>&chap=N&sec=N&version=unv&gb=0` with curl --max-time 30, convert 裡→裏, drop space before 神). If unsure of the CUV wording, translate without 「」.
3. House terms: propitiation 挽回祭; advocate 中保; fellowship 相交; anointing 恩膏; abide 住（在）/常存; the world 世界; antichrist 敵基督; regeneration 重生; assurance 確據; eternal life 永生; the Word 道; Gnostics 諾斯底派; perseverance (of the saints) 恆忍; sermon names stay English. Names: 奧古斯丁、加爾文、摩根、麥克阿瑟、衛斯科、該隱、克林妥.
4. 甚麼 not 什麼; 裏 not 裡; full-width punctuation; Western quotes inside a quote → 『』 nested inside 「」 only where needed.
5. If the English is an OCR quote with a hyphenation artifact ("be-comes"), translate the intended word.
6. If a quote is a fragment starting mid-sentence, translate it as a fragment (start with ……if the English starts mid-sentence lowercase).

## Never touch
Anything outside the 歷代注疏 section; the quote and attribution lines themselves; the 體例說明 box (the coordinator regenerates it).

## Check before finishing
- For each of your chapters: number of `^> "` lines == number of `^> 中譯：` lines; and each 中譯 line comes after its own attribution line.
- `python3 scripts/lint-chapter-markup.py books/bible/john1/<file>` clean.
- Quote lines unchanged: compare sorted `^> (?:"|— )` lines before/after (keep a copy of the file before you start, in /private/tmp/claude-501/-Users-jimxiao-Documents-GitHub-pubhub-books-bible-john1/23dc1de0-f3c9-4514-a375-536c61104b67/scratchpad/).

Work file by file and SAVE after each few quotes (this machine stalls); shell commands can hang — prefer Read/Edit tools and never retry a hung command.

## Report
Per chapter: count of quotes translated; every CUV phrase you inserted with its reference; any quote where the English was ambiguous and how you resolved it.
