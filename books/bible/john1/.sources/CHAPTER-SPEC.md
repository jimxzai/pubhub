# 約翰一書（books/bible/john1）逐章撰寫規格

You are writing ONE chapter of the 1 John study book. Repo root: /Users/jimxiao/Documents/GitHub/pubhub
Book dir: books/bible/john1   Sources: books/bible/john1/.sources/

## Read first (mandatory)
1. books/bible/john1/01-word-of-life.md — THE EXEMPLAR. Match its structure, section order, YAML (7 lines, date 2026年10月), headings, table widths, Greek markup `{\greekfont ...}`{=latex}, quote format, tone, length (~17-22K bytes).
2. .claude/skills/eat-bible/references/chapter-template.md — the 11-section house template.
3. .claude/skills/ask-elder-wong/SKILL.md and references/voice.md, seven-keys.md — for the 老弟兄查經 section.

## Book spine (put the 座標 line in 基督焦點 exactly in this form)
全書六步，每一步都是神先動、人後應（鑰節 4:19「我們愛，因為神先愛我們」）：
- 第一步 神先顯現（1:1-4，ch01）→ 人：相交
- 第二步 神先是光（1:5-2:11，ch02）→ 人：認罪、行在光中
- 第三步 神先把道與恩膏放在人裏面（2:12-29，ch03）→ 人：住在主裏面、不愛世界
- 第四步 神先賜兒女的名分（3:1-24，ch04）→ 人：潔淨自己、行義、捨己相愛
- 第五步 神先愛我們（4:1-21，ch05）→ 人：試驗諸靈、彼此相愛
- 第六步 神先為祂兒子作見證（5:1-21，ch06）→ 人：信、知道有永生、遠避偶像
Coordinate line format: `> **全書座標**：啟示的次序·第N步——**...**。...` (2-3 sentences locating this chapter on the spine, linking to previous/next step).

## Scripture (non-negotiable)
- Chinese = CUV from .sources/cuv-1john-house.txt (already in house style: 裏, no 抬頭 space). Copy the verses of your range VERBATIM into `## 經文` with ^n^ markers (use ^2:1^ style when the range crosses a chapter, as in `^2:1^`). Paragraph breaks ok (`>` blank line `>`).
- English = NASB 1995 from .sources/nasb1995-1john.txt, verbatim incl. *italics*.
- Every OTHER Bible verse you quote in Chinese with 「」 must be verified verbatim against CUV via:
  curl -s "https://bible.fhl.net/json/qb.php?chineses=<URL-encoded 書卷簡稱 e.g. 約, 詩, 創, 出, 太, 啟, 約壹 is 約一>&chap=N&sec=N&version=unv&gb=0"
  then convert 裡→裏 and drop the full-width space before 神. Verify the chapter:verse address too. If you can't verify, paraphrase without 「」. Do NOT use ai-eden.com (rate-limited).
- Partial quotes must be exact substrings. Never "improve" CUV wording.

## Commentary (non-negotiable — the #1 failure mode of this repo is fabricated quotes)
Sections in 歷代注疏: `### 教父時期` (Augustine), `### 改革宗時期` (Calvin), `### 摩根 (G. Campbell Morgan)`, `### 麥克阿瑟 (John MacArthur)`. Names in Chinese prose: 奧古斯丁, 加爾文, 摩根, 麥克阿瑟, 愛任紐, 衛斯科 (Westcott) — use exactly these.
- Every `> "..."` quote must be a VERBATIM substring of a local source:
  - Augustine: .sources/augustine-homilies-1john.txt (NPNF¹ 7; homilies 1-10 cover 1 John 1:1–5:3; cite "Homily N.§"). Ch06 5:4-21 has no Augustine homily — say so honestly or use only what exists.
  - Calvin: .sources/calvin-1john.txt (cite "on 1 John X:Y").
  - Morgan: .sources/morgan-letters-of-john.txt — ONE essay (pp. 175-190 of Living Messages, 1912), not verse-by-verse. Cite page from the running headers. Use only if a passage genuinely bears on your range; otherwise write 摩根 section as an honest short note or reuse a different aspect. Never force it. Avoid re-using the two Morgan quotes ch01 already used.
  - MacArthur: .sources/gty/62-N.txt transcripts; index in .sources/gty-1john-index.tsv (code → passage). Attribution line MUST be: `> — John MacArthur, "Title" (sermon 62-N)` (title from line 1 of the txt).
  - Westcott (.sources/westcott-epistles-st-john-1892.txt) may be used in 原文研讀/背景 as unquoted summary or a quote under a `### 近代釋經` heading placed after 麥克阿瑟 (optional).
- Format each quote: one Chinese lead-in sentence (unquoted summary), then `> "English verbatim"` then `> — Author, *Work*, locator`. Inner double quotes inside a quote → use ‘ ’.
- 3 quotes per commentator is the target (Augustine 2-3, Calvin 2-3, Morgan 0-2, MacArthur 3).
- Unquoted summaries must be faithful to the source's actual position.

## Verify before you finish (run all; paste the summary lines in your report)
cd /Users/jimxiao/Documents/GitHub/pubhub
S=books/bible/john1/.sources
python3 scripts/verify-sermon-quotes.py books/bible/john1 --heading 麥克阿瑟 --cache $S/sermon-cache --only <your file stem>   (if --only fails, run without it and read your file's lines)
for h in 教父 改革宗 摩根 近代; do python3 scripts/verify-citations.py books/bible/john1 --source $S/augustine-homilies-1john.txt --source $S/calvin-1john.txt --source $S/morgan-letters-of-john.txt --source $S/westcott-epistles-st-john-1892.txt --heading $h; done
python3 scripts/lint-chapter-markup.py books/bible/john1/<yourfile>
python3 scripts/lint-scripture-text.py books/bible/john1/<yourfile>
Also diff your ## 經文 Chinese against cuv-1john-house.txt with a small python check (strip markers).
All quotes must be OK or OK-OCR; zero DRIFT/MISS. grep -c '^## ' must be 11.

## Content rules
- Traditional Chinese, house style: 裏 (not 裡), 甚麼 (not 什麼), 和合本 names. Full-width punctuation between CJK.
- 老弟兄 (never 黃長老) in the book. Do not put 「」 quotes in 老弟兄's mouth unless verbatim from .claude/skills/ask-elder-wong/references/voice.md whitelist.
- No emoji. No AI filler (「值得注意的是」「不是可有可無的」). Every 領受要點 must be specific to this passage.
- Hymn: use ONLY the assigned public-domain hymn; quote one stanza verbatim (you must be sure of the wording; if unsure of a line, pick a stanza you are sure of) + your own Chinese rendering + `*Author, year*`.
- End 老弟兄查經 with `**你看見耶穌了嗎**？` paragraph (required by spine checker).
- Do not touch any file except your own chapter. Other sessions are working in sibling dirs (john2, john3, jude…) — never edit them.
- Count claims ("出現N次") only if you actually counted in .sources/sblgnt-1john.txt or cuv text.

## Report back
File path, byte size, verse range, list of quotes with OK status, every scripture reference you verified, and any FLAG (doubts, things you couldn't verify, tensions you kept open).
