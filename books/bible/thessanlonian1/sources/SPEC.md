# 帖撒羅尼迦前書研讀 — chapter-writing spec (for every chapter agent)

Repo root: `/Users/jimxiao/dev/pubhub`. Book dir: `books/bible/thessanlonian1/`.
Exemplar chapter (written by hand, follow it exactly in form): `books/bible/thessanlonian1/01-chosen-and-called.md`.
Read it in full before writing anything. Model book for tone and density: `books/bible/james/01-trials-and-temptation.md`.

**Do NOT grep/read across `books/` broadly** — the filesystem there is very slow (cloud-synced). Read only the
files named in this spec.

## The three lines that may never be crossed

1. **No fabricated Scripture.** Every Scripture quotation (CUV or NASB, block or inline in prose, any book of the
   Bible) must be copied from a fetched source, not from memory. For 1 Thessalonians the sources are local:
   - CUV: `sources/cuv-verified.json` (original 和合本: ai-eden.com == cnbible 繁體中文和合本, all 89 verses; fhl `unv` was found to mix in CUVMP readings and is NOT used for this letter's text). House conversions, apply exactly these and nothing else:
     `裡`→`裏`; `　神`(full-width space + 神)→`神`; `─`→`——` is NOT done, instead `神─我們的父` → `神——我們的父`
     (i.e. U+2500 → two em-dashes `——`); drop the CUV marginal note in 3:2 `（作神執事的：有古卷是與神同工的）`
     from the Scripture block but mention it in 原文研讀 if relevant.
   - NASB 1995: `sources/nasb1995.json` (biblehub `/nasb/` = 1995; supplied words already `*italic*`).
   - Other books (cross references, Psalms): fetch CUV from
     `curl -s "https://bible.fhl.net/json/qb.php?chineses=<URL-encoded 書卷簡稱>&chap=<n>&sec=<v>&version=unv&gb=0"`
     (e.g. 詩=%E8%A9%A9, 羅=%E7%BE%85, 徒=%E5%BE%92, 林前=%E6%9E%97%E5%89%8D, 約=%E7%B4%84, 賽=%E8%B3%BD,
     但=%E4%BD%86, 太=%E5%A4%AA, 啟=%E5%95%9F, 帖後=%E5%B8%96%E5%BE%8C, 腓=%E8%85%93, 創=%E5%89%B5, 出=%E5%87%BA).
     Apply the same 裡→裏 / 　神→神 conversions. Easiest: `cd books/bible/thessanlonian1/sources && python3 fhl.py 羅:8:24 詩:33:6-9`
     (prints converted CUV; book abbreviations as in 和合本). `python3 cuvconv.py <ch> <from> <to>` prints this
     epistle's CUV and NASB blocks ready to paste. If you cannot fetch a verse, paraphrase without quotation marks.
   - A prose quotation in 「」 followed by a reference like （羅8:24） must be the exact CUV wording of that
     verse (a contiguous substring). If you shorten, use …… and keep each piece verbatim. A machine checker
     (`scripts/verify-prose-citations.py`) will test this.
2. **No fabricated commentary.** Every sentence inside `> "..."` attributed to a commentator must be a verbatim
   contiguous substring of the local source file (case/punctuation/curly-quote differences are tolerated by the
   checker, words are not). Copy-paste from the file; never retype from memory. Do not quote the transcript's
   own reading of the Bible text as if it were MacArthur's comment — quote his comment.
   - Chrysostom: `sources/chrysostom-1thess.txt` (NPNF1 vol. 13, New Advent). Homily numbers: 230401 = Homily 1 …
     230411 = Homily 11. Cite as `— John Chrysostom, *Homilies on First Thessalonians*, Homily N (NPNF¹ 13)`.
   - Calvin: `sources/calvin-1thess.txt` (CCEL calcom42, John Pringle tr.). Cite as
     `— John Calvin, *Commentary on 1 Thessalonians*, on 1 Thessalonians X:Y`.
   - Morgan: `sources/morgan-exposition-1thess.txt` (*An Exposition of the Whole Bible*, 1959, studylight gcm) — one
     short paragraph per chapter; cite `— G. Campbell Morgan, *An Exposition of the Whole Bible* (1959), on 1 Thessalonians N`.
     And `sources/morgan-living-messages-1thess.txt` ("The Message of I. Thessalonians" in *Living Messages of the
     Books of the Bible: Matthew to Revelation*, New York: Revell, 1912; OCR — page numbers appear as running heads like
     `14 MESSAGE OF I. THESSALONIANS`); cite `— G. Campbell Morgan, *The Message of I. Thessalonians*, in
     *Living Messages of the Books of the Bible: Matthew to Revelation* (Revell, 1912), p. N`. Fix only obvious OCR hyphen breaks; if an
     OCR word is garbled, do not quote that sentence.
   - MacArthur: `sources/gty-txt/52-N.txt` (first line = title); passage list in `sources/gty-meta.json`.
     Cite EXACTLY in this form (the checker resolves the code from it):
     `— John MacArthur, "Title" (sermon 52-N)`.
   - Each commentator's quotes go under ONE `###` heading per chapter (the checkers only read the first heading
     with that name). Heading names, exactly:
     `### 教父時期 (屈梭多模 John Chrysostom)` / `### 加爾文·改革宗時期 (John Calvin)` /
     `### 摩根 (G. Campbell Morgan)` / `### 麥克阿瑟 (John MacArthur)`.
     Chinese names fixed: 屈梭多模、加爾文、摩根、麥克阿瑟、司提反、西拉、提摩太、耶孫. Never other transliterations.
   - Inside a `> "..."` quote never leave a straight double quote: turn the source's inner "x" into ‘x’
     (the checker stops at the first inner `"` and would silently verify only a fragment).
   - Each quote: a one-line Chinese lead-in that says what he argues (your summary, no quotation marks), then
     the English `> "..."` verbatim, then `> — ...` source line. Target per chapter: Chrysostom 1-2, Calvin 1-2,
     Morgan 1 (from either work; if the exposition paragraph has nothing for your passage, use Living Messages),
     MacArthur 2-3. Quality over count; never pad.
3. **No fabricated 老弟兄 words.** Do not put anything in 「」 attributed to 老弟兄 / 黃長老 unless it is one of these
   whitelisted sayings (from `.claude/skills/ask-elder-wong/references/voice.md`):
   「你研讀聖經，卻沒有看見耶穌——那本書等於白讀了。」「字句叫人死，精義叫人活。」
   「哪裡有信，哪裡就有聖靈的工作；哪裡有不信，哪裡就有撒旦的工作。」
   「我們照著神的意思去做，神就負責；照著我的意思去做，我要負責。」
   「不是我們去建立教會，是你手上有沒有釘痕的手。」「躺在青草地上，是羊在反芻——你的讀經是反芻嗎？」
   Otherwise speak in his voice (提問式, 不急著給答案) without quotation marks. The original 查經班 notes contain no
   study of 1 Thessalonians; the 老弟兄查經 section is the method applied, never presented as a transcript.
   Always call him 老弟兄 in the book, never 黃長老.

## Chapter file shape (11 sections, this order, nothing else at `## ` level)

```
---                                   ← 7-line YAML, copy from the exemplar verbatim
...
---

# 中文章題 (English Title)

帖撒羅尼迦前書 X:Y-Z

**經文核對**：[ai-eden.com/bible/1-thessalonians/X](https://www.ai-eden.com/bible/1-thessalonians/X?t=CUV,NASB&cols=2)

## 基督焦點 (Christ at the Center)      box: 本章鑰詞 + **全書座標** (+ **神的次序**) ; then one hook paragraph
## 配詩 (Opening Hymn)                  ONE public-domain hymn, 2 stanzas EN verbatim + 編者中譯; author, year
## 經文 (Scripture)                     版本說明 line; ### 中文 — 和合本 (CUV); ### English — NASB 1995
## 背景 (Context)                       2-3 ### subsections
## 原文研讀 (Word Study)                table; Greek as `{\greekfont ...}`{=latex}; full-width CJK punctuation
## 領受要點 (Truths Received)           3-4 numbered points, each specific to THIS passage
## 歷代注疏 (Historical Commentary)     體例說明 box (copy exemplar) + the four ### commentator headings
## 詩篇與聖詩 (Psalm & Hymn)            ### 詩篇 x:y (CUV verbatim) + ### hymn (one line tying back)
## 老弟兄查經 (Reading with the Elder Brother)
     **精義一句話**：…  / ### 全經連線 (2-4 bullets) / ### 提問式對話 (先問/再問/追問/落到自己)
     / ### 活在今天·AI時代 / ### 今天的祭壇 (早晨/晚上/一個行動) / **你看見耶穌了嗎**？ one paragraph, last
## 生命應用 (Application)               ### 默想問題 (≤3, new angles) / ### 禱告回應
## 與其他經文的關聯                     table 經文 | 關聯主題 (6-9 rows)
---
*本章研讀整合三方資源：…*
```

Scripture block: `> ^1^text^2^text…` one blockquote, paragraphs separated by `>` blank lines at natural breaks;
verse markers `^n^` only (no chapter prefix). No italics in CUV. NASB keeps `*supplied*` italics and ALL CAPS.
Hymn lyrics: only the public-domain hymn assigned below. Its text is already fetched (hymnary.org is blocked) at
`sources/hymns/<key>.txt` (Wikisource; first line names the printed hymnal). Keys: veni-creator/fugitive (ch1, use
fugitive.txt = J. C. Hutchieson, *Fugitive Poetry 1600–1878*), jesus-shall-reign, take-my-life, break-thou,
blest-be-the-tie, spirit-of-god, o-master, it-is-well, soldiers-of-christ, rejoice-lord-is-king (Wesley 1746 original
text, *Hymns for our Lord's Resurrection*), love-divine. The Army and Navy Hymnal pages interleave lines from the
sheet music and contain hyphenated syllables (`Spir-it`) and typos (`suecessive`, `Christan`, `mutal`): rejoin
syllables, fix only an obvious typo, and reconstruct stanza order carefully (in Jesus Shall Reign the stanzas are
scrambled — use stanzas whose line order is unambiguous). Quote 2 stanzas. Chinese lines are the editor's own
translation: credit line `*作者, 年份；中譯為編者試譯*`. Never use a copyrighted hymn.

Table separator rows must be long (at least as wide as the exemplar's) — short `|---|` rows make
non-breaking columns in this pipeline. Inside any `\jesus{}` (not used in this epistle) no markdown. Never write a
line `---` directly under a paragraph without a blank line before it (Setext heading trap).
Use 裏 not 裡, 甚麼 not 什麼, 祂 is NOT used for God in this repo's chapters — use 他 as CUV does (match exemplar).
Full-width punctuation in Chinese. Length target: 8,000-11,000 characters per chapter file as measured by `wc -m` (the exemplar is ~9,100; James chapters are similar).
**Write each chapter in 3-4 tool calls** (Write the first sections, then append the rest with further edits) —
one giant Write of a whole chapter has stalled agents in this session.

## The book's spine (every chapter must locate itself on it)

全書骨幹 = **神的動詞**。帖撒羅尼迦前書是保羅現存最早的書信之一，寫給一間建立不過幾個月、在患難中的教會。
它的骨幹不是人做了甚麼，是神做了甚麼——而且按著次序：

| 步 | 經文 | 神的作為 | 人的回應 (信·愛·望) |
|---|---|---|---|
| 第一步 | 1:4-5；1:9-10 | 神**揀選**；福音帶著權能、聖靈臨到 | 信心的工夫：離棄偶像，歸向神 |
| 第二步 | 2:12-13；3:3,13 | 神**召**人進他國；神的道**運行**；神**堅固**人心 | 愛心的勞苦：在患難中站立得穩 |
| 第三步 | 4:3,7-8 | 神的**旨意**是成聖；神**召**人成聖、**賜聖靈** | 聖潔與相愛，「更加勉勵」 |
| 第四步 | 4:14；5:9-10 | 神必將睡了的人與耶穌一同**帶來**；神**預定**我們得救 | 盼望的忍耐：彼此勸慰，警醒謹守 |
| 第五步 | 5:23-24 | 賜平安的神**親自**使你們全然成聖；那**召**你們的必**成就** | 常常喜樂、不住禱告、凡事謝恩 |

Three textual facts the book leans on (all verified against the CUV/Greek — do not alter them):
- 「召」(καλέω) three times: 2:12 召你們進他國、得他榮耀；4:7 神召我們……成為聖潔；5:24 那召你們的本是信實的。
- Every chapter of the letter ends looking at the coming of Christ: 1:10；2:19；3:13；4:13-18；5:23. παρουσία occurs
  4 times (2:19；3:13；4:15；5:23).
- 信、愛、望 triad: 1:3 (all three) → 3:6 Timothy's report brings 「信心和愛心」 only → 3:10 「補滿你們信心的不足」 →
  4:13 「像那些沒有指望的人」 → 5:8 信和愛當護心鏡、得救的盼望當頭盔. (The observation that hope is missing from
  3:6 and is what 4:13-5:11 supplies is the editor's reading of the text; state it as reading, not as a quotation.)

Each chapter's 基督焦點 box must contain a `**全書座標**：` line saying which step (第N步) it is and how it moves the
line on. The last paragraph `**你看見耶穌了嗎**？…` must return to Christ concretely from this passage.

## Chapter assignments

| file | passage | title | volume / step | MacArthur sermons | hymn |
|---|---|---|---|---|---|
| 01-chosen-and-called.md | 1:1-5 | 蒙揀選的記號 (Marks of the Chosen) | 卷一·第一步 | 52-1, 52-2, 52-3 | Come, Holy Ghost, Our Souls Inspire (John Cosin tr., 1627) |
| 02-turned-to-god.md | 1:6-10 | 離棄偶像，等候他兒子 (Turned to God, Waiting for His Son) | 卷一·第一步 | 52-3 | Jesus Shall Reign Where'er the Sun (Isaac Watts, 1719) |
| 03-mother-and-father.md | 2:1-12 | 如母乳養，如父勸勉 (As a Mother, As a Father) | 卷一·第一步→第二步 | 52-4, 52-5, 52-6 | Take My Life, and Let It Be (Frances R. Havergal, 1874) |
| 04-word-at-work.md | 2:13-20 | 運行在心中的道 (The Word at Work) | 卷二·第二步 | 52-7, 52-8, 52-9 | Break Thou the Bread of Life (Mary A. Lathbury, 1877) |
| 05-standing-firm.md | 3:1-13 | 靠主站立得穩 (Standing Firm in the Lord) | 卷二·第二步 | 52-10, 52-11, 52-12 | Blest Be the Tie That Binds (John Fawcett, 1782) |
| 06-gods-will-holiness.md | 4:1-8 | 神的旨意：成為聖潔 (The Will of God: Your Sanctification) | 卷三·第三步 | 52-13, 52-14, 52-15 | Spirit of God, Descend upon My Heart (George Croly, 1854) |
| 07-love-and-quiet-work.md | 4:9-12 | 彼此相愛，安靜做工 (Love and Quiet Work) | 卷三·第三步 | 52-16 | O Master, Let Me Walk with Thee (Washington Gladden, 1879) |
| 08-asleep-and-coming.md | 4:13-18 | 睡了的人與主降臨 (Those Who Sleep and the Lord Who Comes) | 卷四·第四步 | 52-17, 52-18 | It Is Well with My Soul (Horatio G. Spafford, 1873) |
| 09-children-of-light.md | 5:1-11 | 光明之子 (Sons of Light) | 卷四·第四步 | 52-19 … 52-23 | Soldiers of Christ, Arise (Charles Wesley, 1749) |
| 10-life-together.md | 5:12-22 | 教會的日常 (The Church's Daily Life) | 卷五·第五步 | 52-24 … 52-34 | Rejoice, the Lord Is King (Charles Wesley, 1744) |
| 11-faithful-is-he.md | 5:23-28 | 那召你們的必成就 (Faithful Is He Who Calls) | 卷五·第五步 | 52-35, 52-36 | Love Divine, All Loves Excelling (Charles Wesley, 1747) |

The sister volume (books/bible/thessanlonian2, being written now by another session) uses: The Church's One Foundation, Guide Me O Thou Great Jehovah, How Firm a Foundation, Lo! He Comes, A Mighty Fortress, Stand Up Stand Up for Jesus, Work for the Night Is Coming — never use those. Do not reuse another chapter's hymn or the same psalm as an adjacent chapter. Psalms already used: ch01 詩33:6,9.

## Checks to run on your own files before reporting (from repo root)

```
python3 scripts/lint-chapter-markup.py books/bible/thessanlonian1/<file>
python3 scripts/lint-scripture-text.py books/bible/thessanlonian1/<file>
python3 scripts/verify-sermon-quotes.py books/bible/thessanlonian1 --heading 麥克阿瑟 --cache books/bible/thessanlonian1/sources/gty-cache
python3 scripts/verify-citations.py books/bible/thessanlonian1 --source books/bible/thessanlonian1/sources/calvin-1thess.txt --heading 加爾文
python3 scripts/verify-citations.py books/bible/thessanlonian1 --source books/bible/thessanlonian1/sources/chrysostom-1thess.txt --heading 屈梭多模
python3 scripts/verify-citations.py books/bible/thessanlonian1 --source books/bible/thessanlonian1/sources/morgan-exposition-1thess.txt --source books/bible/thessanlonian1/sources/morgan-living-messages-1thess.txt --heading 摩根
grep -c '^## ' <file>   # must be 11
```
(Check each script's `--help` first; flags may differ slightly. Other agents are writing other chapters at the same
time — only judge findings in YOUR files; never edit files you were not assigned.)
Also self-check every CUV verse in your 經文 block against the JSON with a short python diff (after the house
conversions) — it must be identical.

Report back: files written, character counts, the check results, and any FLAGS (things you could not verify,
judgment calls, possible errors you noticed in the spec).
