# Consolidated PDF source audit

**Source:** `/Users/jimxiao/Documents/GitHub/pubhub/output/gospel-of-matthew-consolidated.pdf`

## Source profile

- Title: *馬太福音研讀 — 天國之王 — Gospel of Matthew Deep Study — 2026 整編版*
- Author: PubHub 三書精讀系統
- Edition date shown in the PDF: 2026年8月
- Original PDF creation date: 2026-09-02; rebuilt 2026-09-20
- Length: 436 pages after corrections (original supplied PDF: 437)
- Page size: 504 × 720 pt
- Production: LaTeX / xdvipdfmx

## Assigned release identity

All manuscript files in this directory are now standardized to this single release identity:

**馬太福音研讀 — 天國之王 — Gospel of Matthew Deep Study — 2026 整編版**

Older working labels such as `0.2.0`, the 2025 date, and the shorter title `馬太福音研讀` are retired from the release metadata. They must not be reintroduced in chapter front matter, contents, exports, or cover copy.

## Editorial value

The PDF is a richer consolidated edition than the chapter Markdown currently in this directory. It includes a designed cover, maps, five-discourse structure, copyright page, expanded orientation material, chapter-level deep explorations, source notes, applications, and a 28-day devotional sequence.

The PDF should therefore be treated as the current editorial reference for structure, chapter naming, and expanded commentary. It must not be treated as automatic permission to reproduce every quotation in the Markdown package.

## Canonical build inputs — corrected source mapping

The assigned PDF is built by `../../../scripts/build-gospel-of-matthew-consolidated.sh` from `../matthew/book/`, using `../../../templates/pdf/gospel-of-matthew.latex`. The 29 Markdown files in this directory are a separate legacy manuscript and are **not inputs to that build**. Their render checks do not validate the assigned PDF.

The active source includes preface, overview, canonical-context introduction, kingdom-order and Emmanuel essays, systematic study, 28 chapters, Revelation epilogue, references, indexes, glossary, additional appendices, and afterword. These existing sections must be preserved when rebuilding.

## Translation policy and verification scope

The PDF copyright page identifies Chinese Scripture as the 1919 Chinese Union Version and identifies NASB quotations with Lockman Foundation permission. The Markdown package currently labels its Scripture as RCUV and ESV. These are different rights and translation configurations.

The assigned edition retains **CUV 1919 and NASB 1995**, as stated in the canonical builder. CUV 1919 is not the Revised Chinese Union Version (RCUV). The earlier request to choose a new translation policy was based on the legacy manuscript, not the assigned edition.

Verify quotation accuracy and retain permissions evidence for this existing policy. A printed permission notice is not, by itself, evidence that all intended distribution is covered.

Do not merge the legacy RCUV/ESV manuscript into the active CUV/NASB source. The legacy release scripts apply only to files in this directory.

## Visual inspection

### Rebuilt proof — 2026-09-20

- Built from the actual 40-file source assembly, preserving all 28 chapters and existing appendices.
- Corrected chapter 1's excerpt disclosure, unsupported ethnic attribution to Tamar, overstatement about genealogy as a legal document, and distinction between textual evidence and theological inference.
- Replaced the unsupported “three days from the tomb to the Great Commission” statement in the volume divider.
- Fixed an introduction table that printed above the page boundary; inspected the corrected page and the revised chapter pages.
- Automated checks on all 436 pages: 28 chapter bookmarks, no text beyond page edges, no invalid internal link destinations, zero missing-glyph and overfull-box warnings. Blank pages 4 and 6 remain as existing front-matter versos.
- Preserved the assigned title, edition, and output filename. A recovery copy of the prior PDF is at `/private/tmp/matthew-before-update/gospel-of-matthew-consolidated.pdf`.
- This pass is not a completed independent theological review or a verification of every quotation in all 28 chapters. The PDF remains untagged; accessibility remediation is still outstanding.

Run the repeatable PDF check with:

```sh
python3 scripts/check-pdf.py ../../../output/gospel-of-matthew-consolidated.pdf --log ../../../output/gospel-of-matthew-consolidated-build.log
```

### Initial sample inspection

Representative rendered pages were inspected: the cover, front matter, a chapter study page, and the map/structure pages. The visual system is strong: generous margins, consistent purple/gold hierarchy, bilingual display, and clear chapter transitions. The blank verso after the opening visual pages should be confirmed as intentional in the final print proof.
