# Shared brief for writing Ephesians chapters (books/bible/ephisian/)

You are writing chapters for a from-scratch build of 以弗所書研讀 (Ephesians
Deep Study), part of the pubhub "三書精讀出版系統" project. This follows the
same John-standard 11-section chapter template already used across this
repo's Job, Leviticus, Joshua, Ruth, Judges, Romans, Acts etc. builds.

## Read the exemplar FIRST, before writing anything

Read `/Users/jimxiao/Documents/GitHub/pubhub/books/bible/ephisian/01-chosen-in-christ.md`
in full. This is chapter 1, already written and approved. **Match its exact
structure, section order, heading wording, tone, and register.** Do not add
sections it doesn't have; do not omit sections it has. The 11 sections, in
this exact order, are:

1. `# 章題 (English)` + reference line + `**經文核對**：` link line
2. `## 基督焦點 (Christ at the Center)` — a blockquote box with 本章鑰詞 and
   全書座標 (locate this chapter on the book's spine — see below), then one
   paragraph connecting the passage to Christ.
3. `## 配詩 (Opening Hymn)` — ONE public-domain hymn stanza (pre-1930,
   genuinely real — do not invent a hymn or misattribute one), English +
   Chinese translation.
4. `## 經文 (Scripture)` — `### 中文 — 和合本 (CUV)` then `### English — NASB`,
   using `^n^` verse-number markers, text copied VERBATIM from the cached
   source files (see below) — never retyped from memory.
5. `## 背景 (Context)` — 2 subsections of historical/literary background.
6. `## 原文研讀 (Word Study)` — a table of Greek terms (word | 音譯 | 意義 |
   經文 | 註解), 4-8 rows, plus a short prose note on a structural feature.
7. `## 領受要點 (Truths Received)` — 3 numbered points.
8. `## 歷代注疏 (Historical Commentary)` — the `體例說明` box (copy verbatim
   from the exemplar), then `### 教父時期` (Chrysostom, prose summary +
   1-2 verbatim quotes), `### 摩根 (G. Campbell Morgan)` (1 verbatim quote),
   `### 麥克阿瑟 (John MacArthur)` (1-2 verbatim quotes). See sourcing rules
   below — every quoted line MUST be verbatim from a real fetched source.
9. `## 詩篇與聖詩 (Psalm & Hymn)` — one related Psalm passage + 1-2 sentences
   connecting it.
10. `## 老弟兄查經 (Reading with the Elder Brother)` — **exactly** the format
    in the exemplar: 先問/再問/追問/落到自己/你看見耶穌了嗎, each a bolded
    lead-in followed by 1-2 sentences. This book has NO first-hand Elder Wong
    (老弟兄) teaching notes on Ephesians — do not invent or quote him. This
    section is a methodological application of his style, not a transcript.
11. `## 生命應用 (Application)` — `### 默想問題` (3 numbered) + `### 禱告回應`
    (one prayer in second person, ending 奉主耶穌基督的名禱告，阿們。)
12. `## 與其他經文的關聯` — a table: 主題 | 本章經文 | 相關經文 (5 rows)

Every chapter file needs the same 7-line YAML front matter as the exemplar
(copy it verbatim):
```
---
title: 以弗所書研讀
subtitle: Ephesians Deep Study
author: PubHub 三書精讀系統
date: 2026年9月
publisher: 三書精讀出版系統
---
```

## The book's spine — so your 全書座標 line is correct

Read these three files for full context before writing your 全書座標 lines
and your chapter's closing paragraphs:
- `/Users/jimxiao/Documents/GitHub/pubhub/books/bible/ephisian/00b-sit-walk-stand.md`
- `/Users/jimxiao/Documents/GitHub/pubhub/books/bible/ephisian/00c-revelation-order.md`
- `/Users/jimxiao/Documents/GitHub/pubhub/books/bible/ephisian/elder-wong-systematic-study.md`

Short version: the book has 3 volumes — 卷一 你的地位·坐 (弗1-3, chapters
01-06 by file number), 卷二 你的行為·行 (弗4-5, chapters 07-10), 卷三 你的
站立·站 (弗6, chapter 11). The revelation-order spine traces "in the heavenly
places" (ἐν τοῖς ἐπουρανίοις) through 1:3 → 1:20 → 2:6 → 3:10 → 6:12. Your
全書座標 line should say which step of that (or which volume) your chapter
belongs to, in your own words — don't just copy the phrasing above.

## Scripture sourcing — use the CACHED files, do not re-fetch or paraphrase

CUV (和合本) and NASB 1995 text for all 6 chapters of Ephesians is already
fetched and verified, one verse per line, in:
- `/Users/jimxiao/Documents/GitHub/pubhub/books/bible/ephisian/.sources/cuv_clean/ephN.txt`
- `/Users/jimxiao/Documents/GitHub/pubhub/books/bible/ephisian/.sources/nasb_clean/ephN.txt`

(N = chapter number 1-6). Each line is `verseRef text`. Copy the text for your
assigned verse range VERBATIM — do not retype from memory, do not paraphrase.
Convert to `^n^text` inline format exactly as the exemplar chapter does
(join verses into 1-2 blockquote paragraphs of reasonable length, verse
number as `^n^` immediately before that verse's first word, no space).
NASB supplied words already carry `*word*` markers in the cached file — keep
them as markdown `*italic*`.

The `經文核對` link line format: `**經文核對**：[ai-eden.com/bible/ephesians/N](https://www.ai-eden.com/bible/ephesians/N?t=CUV,NASB&cols=2)（CUV 另以 bible.fhl.net 和合本覆核逐節）`
(N = the chapter number your passage is in; if your passage spans two
chapters, cite both, e.g. `.../ephesians/5` and `.../ephesians/6`).

## Commentary sourcing — every quote must be real and verbatim, or don't quote

**This is the most important rule in this brief.** A quoted line attributed to
a named commentator must be copied verbatim from a real source you actually
fetched this session. If you cannot find a clean quotable sentence on your
specific verses, either (a) write an unquoted prose summary of that
commentator's position instead (no quotation marks), or (b) skip that
commentator for this chapter rather than inventing or loosely paraphrasing a
quote and dressing it in quotation marks. Never present a paraphrase as a
verbatim quote.

### Chrysostom (教父時期)

Fetch your assigned Homily page(s) with curl (not WebFetch — WebFetch
summarizes and can silently reword), e.g.:
```
curl -sL -A "Mozilla/5.0" "https://ccel.org/ccel/schaff/npnf113/npnf113.iii.iv.<homily-letter>.html" -o /tmp/homily.html
```
Then extract the body text (strip HTML tags, drop leading UI chrome before the
literal string "Homily"), and search it for material discussing your assigned
verses. Quote 1-2 sentences verbatim (English), then give a faithful Chinese
translation, in the exact two-line block format the exemplar uses (English in
quotes, Chinese translation below it, then an `— John Chrysostom, ...` or
`出處：` attribution line naming Homily number, verse range, and
`*Nicene and Post-Nicene Fathers*, First Series, vol. 13`).

If a homily's text is long, and you need only the part touching your assigned
verses, search for keywords from those verses (e.g. an English word from the
NASB text) to locate the relevant paragraph rather than reading the whole
thing.

### G. Campbell Morgan (摩根)

One cached synthesis sermon covers the whole book (not verse-by-verse):
`/Users/jimxiao/Documents/GitHub/pubhub/books/bible/ephisian/.sources/morgan-message-of-ephesians.txt`
(from *The Message of Ephesians*, in *Living Messages of the Books of the
Bible*). Read it and search for a passage that genuinely speaks to your
chapter's theme (it discusses eternal/temporal, construction, confession,
conflict, unity, sanctification — matching different parts of the letter).
Quote 1-2 sentences verbatim if you find a good match. If nothing in this
synthesis text genuinely fits your specific verses, it is fine to have NO
Morgan quote in your chapter (or use an unquoted one-sentence summary of his
book's stated theme as it relates to your section) — do not force a quote
that isn't really about your passage.

### John MacArthur (麥克阿瑟)

Fetch your assigned sermon code(s) from gty.org:
```
curl -sL -A "Mozilla/5.0" "https://www.gty.org/sermons/<CODE>" -o /tmp/sermon.html
```
Extract the transcript: find the `expand--content` div, strip HTML tags. The
sermon title is in `<title>...</title>`. Search the transcript for a
quotable sentence discussing your assigned verses (MacArthur reads a verse
range aloud early in each sermon, then expounds it — the discussion after
that point is usually the richest). Quote 1-2 sentences verbatim, translate
faithfully, cite as:
`出處：John MacArthur, 講道 "<English title>"（sermon <CODE>），恩典社區教會，
1978或1979年<月>，逐字講章見 gty.org`
(check the actual date near the top of the transcript if mentioned, else omit
the month).

## Greek word study — use real, verifiable Greek terms

For each Word Study table row, use genuine Greek words that actually occur in
your passage's Greek text (this is well-established NT Greek vocabulary — if
you are not certain a word is correct for a specific verse, pick a different,
safer term you are confident about rather than guessing). Standard
Strong's-number format like the exemplar. Do not invent a Greek word or a
Strong's number.

## Do not touch other files

Only create/edit the specific chapter file(s) you are assigned. Do not modify
`01-chosen-in-christ.md`, the front-matter files, or any other chapter.

## When done

Report back: which file(s) you created, word count of each, which
commentators you were able to quote verbatim vs. summarize unquoted, and any
verse range where the cached CUV/NASB text looked incomplete or wrong (do not
silently fix it — flag it).
