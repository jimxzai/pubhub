# 馬可福音研讀 — Publication Release Register

## Assigned edition

- **Title:** 馬可福音研讀
- **English subtitle:** Gospel of Mark Deep Study — 2026 整編版
- **Author:** PubHub 三書精讀系統
- **Publisher:** 三書精讀出版系統
- **Scripture editions:** 和合本 1919 (CUV) and NASB 1995
- **Canonical output stem:** `gospel-of-mark-consolidated`

The PDF and EPUB are two formats of the same assigned edition. The historical EPUB filename contains `accessible`; that filename is not a certification. Older combined or alternate-version artifacts are superseded and must not be published. No distribution is authorized by this register while release holds remain open.

## Release gates

| Gate | Status | Required evidence |
|---|---|---|
| Assigned title/version consistency | PASS | Source, combined Markdown, PDF metadata, and output stem agree |
| Build integrity | PASS | Staged build, strict failure checks, stable generated index, backup and rollback; six regression tests pass |
| Visual/PDF preflight | PASS, SAMPLED | 385 pages; embedded Unicode fonts; no logged fatal/glyph/overflow/reference errors; representative rendered pages checked, not a complete proofread |
| Navigation | PASS, AUTOMATED | EPUB internal targets checked; 321 PDF bookmarks counted recursively |
| Language metadata | PASS | Template sets `zh-TW`; rebuilt PDF checked; predominantly English EPUB paragraphs marked `en` |
| Rights, including non-sale distribution | HOLD | Document applicable rights/permission for NASB, MacArthur, Morgan, hymns, and other third-party material |
| EPUB text preservation | PASS | 7,412 text blocks checked; 432 red-letter spans; 1,403 superscripts; copyright text and all twelve appendices included |
| EPUB automated validation | PASS | EPUBCheck 5.3.0: zero errors/warnings; DAISY Ace 1.4.6: zero automated findings on the final EPUB |
| EPUB manual accessibility | HOLD | Mixed-language phrases, table navigation and assistive-technology/manual review still require evidence; automated passes are not certification |
| Independent Scripture/source proofreading | HOLD | Retain verse-by-verse source comparison and independent sign-off; conversion parity alone is insufficient |
| Structural PDF tagging | HOLD | Current PDF is untagged; no PDF/UA compliance claimed |
| ISBN/catalog metadata | HOLD | Complete only for a public retail edition |

## Rights register

| Material | Edition/source | Action before public release | Status |
|---|---|---|---|
| Chinese Scripture | 和合本 1919 | Retain public-domain/source statement | Documented in manuscript; verify jurisdiction |
| English Scripture | NASB 1995 | Confirm permission covers the full Gospel of Mark and intended distribution | OPEN |
| John MacArthur | Grace to You / related works | Retain quotation log and obtain permission or confirm applicable basis | OPEN |
| G. Campbell Morgan | *The Gospel According to Mark* (1927) | Retain source/page evidence and confirm quotation status | OPEN |
| Chrysostom/Calvin/other commentators | Listed source works | Verify public-domain status and translation used | OPEN |
| Hymns and lyrics | Per-chapter hymn material | Verify public-domain status or license each text | OPEN |

No rights status is considered cleared merely because a copyright notice appears in the PDF.

## Accessibility path

The print PDF is the canonical visual edition. For digital accessibility, create a separate reflowable EPUB3/HTML edition from the structured Markdown source with:

- `lang="zh-TW"`;
- semantic headings;
- real table headers;
- descriptive link text;
- alt text for diagrams/ornamentation;
- keyboard-readable navigation;
- no raw LaTeX-only content.

Do not enable PDF tagging in the current XeLaTeX template without an engine migration and a full visual regression pass.

## Fixes and verification workflow

Run `bash build-publication.sh` from this book directory. The build works in a hidden staging directory, validates all 29 sources, compiles until the generated index stabilizes, checks PDF language and bookmarks, builds the EPUB with all twelve appendices, and promotes only after technical checks pass. Previous outputs are backed up outside the distributable output directory. Machine evidence is recorded in `output/gospel-of-mark-consolidated-qa.json`.

Run regression tests with `python3 -m unittest discover -s publishing -v`. EPUB conversion rejects unknown TeX macros instead of silently discarding their contents. Index entries now represent automatic text occurrences, not a professionally selected analytical index; the printed explanation explicitly states this distinction.

The PDF skill requires visual verification of rebuilt pages; a successful compilation is not a substitute. A complete independent proofread and screen-reader review remain human review gates.

## Cover upgrade

Both covers were compared visually with `genesis-consolidated.pdf`. Mark now uses a coordinated full-bleed burgundy gradient, cream typography, fine gold borders and a vector ox emblem. The assigned title is the dominant front-cover heading; the assigned 2026 edition line is retained. The back cover has a bilingual synopsis and a three-part reader-benefit panel. The EPUB uses the same front-cover artwork. Artwork remains vector in the PDF. These are trim-size book pages, not a printer-specific spine/bleed wraparound file.

## Release decision

**Current decision:** editorial working files only; distribution approval is not established, including internal/non-sale circulation. The previous approval statement is withdrawn. No permission request has been sent and no license has been purchased.

**Updated publisher-scale assessment:** 9.6/10, provisional editorial-quality assessment. **Cover design: 9.7/10.** The score reflects the John-informed series hierarchy now applied to Mark: thematic title first, consistent bilingual metadata, explicit CUV/NASB edition line, restrained vector emblem, coordinated back cover and clean publisher footer. Technical production is strong: 385 pages, embedded fonts, 321 recursive bookmarks, stable generated indexes, preserved EPUB content, EPUBCheck zero errors/warnings and DAISY Ace zero automated findings on the final rebuild. Remaining release gates are separate: rights evidence, independent Scripture/quotation proofreading, manual accessibility review, untagged PDF structure and printer-specific production requirements. These scores are not release approval or compliance certification.

For the remaining actions and evidence owners, see `publishing/RELEASE_HANDOFF.md`.
