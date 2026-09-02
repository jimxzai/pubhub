# eat-bible — Chapter template (publisher-optimized, 2026-08-31)

Loaded on demand from `SKILL.md`. Read this when **restructuring or
editing a book's chapter markdown** for print — not when building the PDF.

## The problem this template solves

The original 16-section chapter (John/Mark/Luke 2026-08) said the same
things three or four times: the one-line key appeared in 基督焦點, 老弟兄查經法,
and 老弟兄精義; the cross-Scripture chain in 整本聖經的連結, 全經連線, 貫通全經
and the 關聯 table; the discussion questions in 老弟兄這樣帶你讀, 提問式對話 and
默想問題; and hymns in three sections, two of them literally titled 配詩.
Readers experience that as padding. A publisher's rule: **one fact, one place.**

Applying the template below to Luke (2026-08-31) cut every chapter to
84–91 % of its length with no idea lost, and the PDF from 319 to 285 pages.

## The 11 sections, in order

```
# 章題 (English)
路加福音 N:x-y                              ← reference line
**經文核對**：[ai-eden.com/...](...?t=CUV,NASB&cols=2)

## 基督焦點 (Christ at the Center)        鑰詞 / 人子座標 box + one hook paragraph
## 配詩 (Opening Hymn)                     ONE hymn stanza + 中譯 + author/year
## 經文 (Scripture)                        ### 中文 — 和合本 (CUV)  /  ### English — NASB
## 背景 (Context)                          2–3 ### subsections
## 原文研讀 (Word Study)                   table(s); punctuation full-width
## 領受要點 (Truths Received)              3–4 numbered points
## 歷代注疏 (Historical Commentary)        > 體例說明 box
                                            ### 教父時期 / ### 改革宗時期
                                            ### 摩根 (G. Campbell Morgan)      ← 出處 line kept
                                            ### 麥克阿瑟 (John MacArthur)      ← verbatim quotes + sermon code
## 詩篇與聖詩 (Psalm & Hymn)               ### 詩篇 x:y … / ### <Hymn title> … (+ any chapter-unique hymn)
## 老弟兄查經 (Reading with the Elder Brother)
                                            **精義一句話** (once)
                                            ### 全經連線  (2–4 named 線)
                                            ### 提問式對話 (先問 / 再問 / 追問 / 落到自己)
                                            ### 活在今天 · AI時代
                                            ### 今天的祭壇 (早晨 / 晚上 / 一個行動)
                                            **你看見耶穌了嗎** (one paragraph, last)
## 生命應用 (Application)                  ### 默想問題 (≤3, angles not already asked) / ### 禱告回應
## 與其他經文的關聯                        reference table
*本章研讀整合三方資源：…*
```

Sections **removed entirely** from the old template (their content lives
above): the second `配詩 (Hymns & Psalms)`, `三大資源深度整合`, `老弟兄精義`,
`詩篇回應` + `聖詩默想` (merged), `老弟兄查經 · 深讀` (renamed).

## What never changes during an edit

1. The 7-line YAML front matter — build scripts strip it with `tail -n +8`.
2. Everything under `## 經文`: verse markers `^n^`, `\jesus{}` spans, bold.
3. Hymn lyrics, translations, author/year lines.
4. Quoted commentary (`> "…"`), every `> —` / `> 出處` line, sermon codes.
5. Word-study table content (only `,` → `，` between CJK is allowed).
6. The 體例說明 box — **except** a section name it cites, which must follow
   the rename (Luke shipped five dangling 「見『三大資源深度整合』一節」 boxes
   until `scripts/lint-chapter-markup.py` `dangling-section-ref` caught them).
7. 老弟兄 naming, Scripture references, Greek. Add nothing not in the source.

## Editing rules

- **Deduplicate, don't summarize.** When two sections say the same thing,
  keep the better wording once; fold any genuinely new reference into the
  surviving section (e.g. a new OT link goes into the matching 全經連線 線).
- **A second-配詩 hymn is only a duplicate if the same hymn already appears.**
  Eleven Luke chapters carried a chapter-unique hymn there; relocate it into
  詩篇與聖詩 rather than deleting lyrics.
- Delete a 領受要點 only when it restates the 人子座標 box (same verses, same
  Greek, same sentence). Renumber.
- Cut editorial throat-clearing (「不是可有可無的」「值得逐字留意」「這不是文學上的
  呼應，是…」). Keep the vivid, concrete lines — they are the book's voice.
- Bold: at most one conclusion sentence per subsection; leave table/box bold.
- **Inside `\jesus{…}` markdown emphasis does not render** (raw LaTeX inline):
  write `\textbf{}` / `\textit{}` there. Outside it, `**…**` / `*…*` are fine.

## Verifying a restructure (what the Luke pass checked, per chapter)

```
head -7 new == head -7 HEAD                         YAML intact
grep -c '^## ' == 11, in the order above            structure
sed -n '/^## 經文/,/^## 背景/p' new == same from HEAD  scripture untouched (or only ESV→NASB block changed)
grep -c '^> "' new == HEAD                          every verbatim quote survives
every *Author, YEAR* hymn credit in HEAD is in new   no lyrics lost
0.65 ≤ len(new)/len(HEAD) ≤ 0.92                    below 0.65 means real content went
python3 scripts/lint-chapter-markup.py <dir>        raw-macro emphasis, duplicate H2, dangling refs
```

Then build with the driver and *read* two rendered pages — the Luke pass
found the `\jesus{**…**}` asterisks only by looking at a page.

## Fan-out that worked

One exemplar chapter edited by hand + a written spec (this file's rules) +
one agent per two chapters, each told to diff against the exemplar and run
the checks above, then a single verifier over the whole book. Reports came
back with "flags" — read them: they surfaced the unique hymns, the dangling
boxes, and several wrong verse references worth an author's eye.
