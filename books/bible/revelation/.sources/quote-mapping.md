# Revelation — Morgan + MacArthur quote mapping (2026-09-19)

Local sources (already fetched, verbatim, cached — do NOT re-fetch from the network):
- Morgan: `books/bible/revelation/.sources/morgan-exposition-revelation.txt` — plain text,
  22 chapters, each starting with a line `=== Revelation N ===`. This is G. Campbell Morgan's
  *Morgan's Exposition on the Whole Bible* (1959, public domain), from
  https://www.studylight.org/commentaries/eng/gcm/revelation-N.html — cite it as:
  `— G. Campbell Morgan, *Morgan's Exposition on the Whole Bible*, 論啟示錄N章, https://www.studylight.org/commentaries/eng/gcm/revelation-N.html`
- MacArthur sermons: `books/bible/revelation/.sources/gty-cache/gty-66-N.txt` — plain-text
  transcripts already extracted from https://www.gty.org/sermons/66-N/<slug>. Cite as:
  `— John MacArthur, "<Sermon Title>" (gty.org, sermon 66-N), https://www.gty.org/sermons/66-N/<slug>`
  (the word "sermon" before the code is required so the verifier script can find it).
- Index of all 87 sermons with exact passage + title: `books/bible/revelation/.sources/gty-sermon-index.txt`
  (format: `code | slug | title | passage | transcript-char-length`).

Rule: every quote must be copy-pasted verbatim (character-for-character, English) from these
local files — never paraphrased, never reconstructed from memory. Pick short, self-contained
excerpts (1–3 sentences). After writing, grep the exact English string against the source file
to confirm it matches before moving on.

Morgan is thin (~1,500 chars/chapter, no verse-by-verse detail) — one paragraph per file is
normal; do not stretch it into more than it says. Where a Bible chapter splits across two file
we've split the Morgan chapter's own paragraphs, since they follow topic order.

| # | File | Scripture | Morgan source | MacArthur sermon code(s) |
|---|------|-----------|---------------|---------------------------|
| 1 | 01a-prologue.md | 1:1-8 | ch1 paragraphs 1–2 (theme; greeting) | 66-1, 66-2, 66-3 |
| 2 | 01b-vision-of-christ.md | 1:9-20 | ch1 paragraphs 3–4 (vision; effect on John) | 66-4, 66-5 |
| 3 | 02a-ephesus.md | 2:1-7 | ch2 paragraph on Ephesus | 66-6 |
| 4 | 02b-smyrna.md | 2:8-11 | ch2 paragraph on Smyrna | 66-7 |
| 5 | 02c-pergamum.md | 2:12-17 | ch2 paragraph on Pergamum | 66-8 |
| 6 | 02d-thyatira.md | 2:18-29 | ch2 paragraph on Thyatira | 66-9, 66-10 |
| 7 | 03a-sardis.md | 3:1-6 | ch3 paragraph on Sardis | 66-11 |
| 8 | 03b-philadelphia.md | 3:7-13 | ch3 paragraph on Philadelphia | 66-12, 66-13 |
| 9 | 03c-laodicea.md | 3:14-22 | ch3 paragraph on Laodicea (+ closing "I know/I will" paragraph if useful) | 66-14, 66-15 |
| 10 | 04-throne-room.md | 4:1-11 | ch4, whole (short) | 66-16, 66-17, 66-18, 66-19 |
| 11 | 05-lamb-and-scroll.md | 5:1-14 | ch5, whole | 66-20, 66-21, 66-22 |
| 12 | 06a-six-seals.md | 6:1-17 | ch6, whole | 66-23, 66-24, 66-25, 66-26, 66-27 |
| 13 | 06b-144000-sealed.md | 7:1-17 | ch7, whole | 66-28, 66-29, 66-30 |
| 14 | 06c-seventh-seal.md | 8:1-5 | ch8 paragraph 1 (seventh seal, silence) | 66-31 |
| 15 | 07a-four-trumpets.md | 8:6-13 | ch8 paragraph 2 (four trumpets, eagle) | 66-32 |
| 16 | 07b-fifth-sixth-trumpet.md | 9:1-21 | ch9, whole | 66-33, 66-34 |
| 17 | 07c-little-scroll.md | 10:1-11 | ch10, whole | 66-35 |
| 18 | 07d-two-witnesses.md | 11:1-14 | ch11 paragraphs 1–2 (temple measured; two witnesses) | 66-36, 66-37, 66-38 |
| 19 | 07e-seventh-trumpet.md | 11:15-19 | ch11 paragraph 3 (seventh angel/trumpet) | 66-39, 66-40 |
| 20 | 08a-woman-and-dragon.md | 12:1-17 | ch12, whole | 66-41, 66-42, 66-43 |
| 21 | 08b-beast-from-sea.md | 13:1-10 | ch13 paragraph 1 (first beast) | 66-44, 66-45, 66-46 |
| 22 | 08c-beast-from-earth.md | 13:11-18 | ch13 paragraph 2 (second beast) | 66-47, 66-48 |
| 23 | 08d-lamb-on-zion.md | 14:1-13 | ch14 paragraphs 1–3 (144k with Lamb; three angels; blessed are the dead) | 66-49, 66-50, 66-51, 66-52 |
| 24 | 08e-harvest-and-winepress.md | 14:14-20 | ch14 paragraph 4 (harvest and vintage) | 66-53 |
| 25 | 09a-bowls-prepared.md | 15:1-8 | ch15, whole | 66-54, 66-55 |
| 26 | 09b-seven-bowls.md | 16:1-21 | ch16, whole | 66-56, 66-57, 66-58 |
| 27 | 10a-babylon-the-harlot.md | 17:1-18 | ch17, whole | 66-59, 66-60, 66-61, 66-62 |
| 28 | 10b-babylon-fallen.md | 18:1-24 | ch18, whole | 66-63, 66-64, 66-65 |
| 29 | 11a-marriage-of-lamb.md | 19:1-10 | ch19 paragraphs 1–2 (three praises; blessing on the invited) | 66-66, 66-67, 66-68 |
| 30 | 11b-rider-on-white-horse.md | 19:11-21 | ch19 paragraphs 3–4 (manifestation of Christ; the battle) | 66-69, 66-70, 66-71, 66-72 |
| 31 | 12a-millennium.md | 20:1-6 | ch20 paragraphs 1–2 (Satan bound; the thousand years) | 66-73, 66-74 |
| 32 | 12b-great-white-throne.md | 20:7-15 | ch20 paragraphs 3–5 (Satan loosed; the great assize; lake of fire) | 66-75, 66-76, 66-77, 66-78, 66-79 |
| 33 | 13a-new-heaven-new-earth.md | 21:1-8 | ch21 paragraphs 1–2 (holy city; "Behold, I make all things new") | 66-80, 66-81, 66-82 |
| 34 | 13b-new-jerusalem.md | 21:9-22:5 | ch21 paragraph 3 (the Bride/city described) + ch22 paragraph 1 (river/tree of life) | 66-83, 66-84 |
| 35 | 14-epilogue.md | 22:6-21 | ch22 paragraphs 2–6 (ratification; testimony; final invitation) | 66-85, 66-86, 66-87 |

## Format to add (inside the existing `## 歷代注疏 (Historical Commentary)` section)

Keep all existing prose/summary content in the file as-is. ADD a new verbatim quote block
under the existing `### 摩根 (G. Campbell Morgan)`-style heading if one exists, or add a new
`### 摩根 (G. Campbell Morgan)` subsection right before `### 當代釋經` if it doesn't. Same for
MacArthur: add a real verbatim quote to the existing MacArthur subsection (keep the existing
paraphrase paragraph — add the quote block after it, do not delete honest "大意整理" text
that isn't being replaced by a verbatim quote).

Morgan block shape (see books/bible/genesis/01-creation.md lines ~178-192 for the house style):

    ### 摩根 (G. Campbell Morgan)

    <one Chinese sentence introducing what Morgan says, in your own words>：

    > "<verbatim English sentence(s), copy-pasted exactly>"
    >
    > 中譯：<your translation>
    > — G. Campbell Morgan, *Morgan's Exposition on the Whole Bible*, 論啟示錄N章, https://www.studylight.org/commentaries/eng/gcm/revelation-N.html

MacArthur block shape (see books/bible/roman/12-living-sacrifice.md lines ~220-230 for the
house style with a sermon code):

    > "<verbatim English sentence(s) from the transcript>"
    >
    > 中譯：<your translation>（66-N）
    > — John MacArthur, "<Sermon Title>" (gty.org, sermon 66-N), https://www.gty.org/sermons/66-N/<slug>

If a chapter cites two sermon codes for one quote (e.g. an idea spanning both halves of a
two-part sermon), separate the two English fragments with "..." and make sure EACH fragment
independently appears verbatim in its own transcript — do not blend words from the two.
