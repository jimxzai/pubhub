# 1 Kings chapter-writing spec (units 01-24)

Exemplar: `../03-solomon-asks-for-wisdom.md` (copy its skeleton, voice, and section order exactly).

Files (fixed names; build script depends on them):
01-adonijah-and-solomon 02-davids-charge 03-solomon-asks-for-wisdom 04-wise-kings-kingdom 05-hiram-and-the-levy
06-building-the-temple 07-palace-and-furnishings 08-glory-fills-the-house 09-dedication-prayer 10-second-appearance
11-queen-of-sheba 12-solomons-heart-turns 13-shechem-and-the-yoke 14-golden-calves 15-man-of-god-and-old-prophet
16-ahijah-and-shishak 17-abijam-asa-and-baasha 18-omri-ahab-and-jezebel 19-elijah-and-the-widow 20-mount-carmel
21-horeb-still-small-voice 22-ben-hadad-and-the-prophets 23-naboths-vineyard 24-micaiah-and-ahabs-death
Unit -> 1 Kings passage: 01 1:1-53, 02 2:1-46, 03 3, 04 4, 05 5, 06 6, 07 7, 08 8:1-21, 09 8:22-66, 10 9, 11 10, 12 11,
13 12:1-24, 14 12:25-33, 15 13, 16 14, 17 15, 18 16, 19 17, 20 18, 21 19, 22 20, 23 21, 24 22.

Tools (all in this dir): scr.py (cached CUV/NASB), mkscr.py (emits the whole `## 經文` section), verify_blocks.py,
heb.py (Hebrew, ENGLISH verse numbering; `--strong H####`), bib.py (any other book's CUV), txt/henry.txt (Henry full),
QUOTE-BANK.md (patristic/Calvin/Farrar/Meyer/Morgan), HYMN-BANK.md + hymns/ (hymn per unit).

Rules
1. 11 sections in order: 基督焦點(鑰詞 + **全書座標**) / 配詩 / 經文 / 背景 / 原文研讀 / 領受要點 / 歷代注疏 / 詩篇與聖詩 /
   老弟兄查經 / 生命應用 / 與其他經文的關聯 + closing italic line. YAML front matter = the same 7 lines as unit 03.
   H1 = `# 中文題 (English Title)`; line 2 = `列王紀上 N:x-y` (the real passage); then the 經文核對 link `ai-eden.com/bible/1-kings/N`.
2. Scripture block ONLY via mkscr.py, same verses in CUV and NASB; verify with verify_blocks.py (must be 0 bad).
   Every Scripture verse quoted elsewhere (other books, or 王上 verses outside the block) must be copied from bib.py/scr.py. No memory quotes.
3. Word study: >=4 rows, Hebrew copied from heb.py, Strong's number checked with `heb.py --strong`. Any count ("N times") must be computed from sources/heb/*.json.
4. 歷代注疏: quotes ONLY from QUOTE-BANK.md (unit entries; neighbouring units allowed if on-topic) or verbatim from txt/henry.txt. Format as in unit 03
   (English `> "..."`, blank `>`, 中譯 line, then `> 出處：...`). Verify with
   `python3 scripts/verify-citations.py books/bible/kings --source sources/txt/henry.txt --source sources/fathers/<file> ...`
   (file names are in each QUOTE-BANK entry). 教父時期: use a bank entry if one exists, else the one-sentence honest "未能找到" note used in unit 03.
   改革宗時期: Henry (1-3 quotes) plus Calvin/Meyer/Farrar entries if relevant. 摩根 subsection only if the bank has a Morgan quote for the unit (else omit it).
   No 麥克阿瑟 subsection (no verifiable sermons on 1 Kings; disclosed in preface). Chinese translations of the English quotes are yours; no invented quotes, no invented attributions.
   Never put quotation marks around anything attributed to 黃長老/老弟兄 (method-based only).
5. Hymn: the unit's hymn from HYMN-BANK.md, 4 lines in 配詩 and another stanza in 詩篇與聖詩 (second stanza must be verbatim from the cached file in sources/hymns/); write your own Chinese translation. Pre-1929 public-domain only.
6. Spine: **全書座標** line must locate the chapter on the book's spine (see ../00b-lamp-spine.md: four speeches to Solomon, the lamp 11:36/15:4, "raq", the word that never falls, Egypt thread, the heart) and name Christ where the text itself allows (no invented typology; use the NT's own links).
   Tie to the volume's 啟示的次序 step (see the plan in the conversation / build script comments).
7. 領受要點 3-4, each specific to this chapter. 提問式對話 (exegetical, about the text) must differ from 默想問題 (personal, forward-looking). AI時代 paragraph concrete, not cliché. 今天的祭壇 three bullets. 老弟兄查經 ends with **你看見耶穌了嗎**.
8. Hold open genuine tensions; never invent historical facts, dates, numbers, or names. When unsure, omit.
9. Style: Traditional Chinese, 裏/甚麼 per house policy (the helper scripts already convert 裡->裏), "·" interpunct, full-width punctuation between CJK, no emojis, no AI filler. Target 18-26KB per chapter.
10. Checks before reporting: verify_blocks.py; verify-citations.py; `python3 scripts/lint-chapter-markup.py books/bible/kings`; `python3 scripts/check-prose-scripture-quotes.py books/bible/kings`. Report numbers + any flags.
Do NOT: edit files other than your assigned chapters, run builds, git add/commit, fetch from ai-eden.com or studylight.org (fhl bib.py is fine, lightly).
