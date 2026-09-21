# Editorial integrity and spiritual spine

Adapted from the Claude skill's chapter-template, scripture-sources, and
spine-and-score references. Preserve the author's voice and established book
structure; these house conventions are not permission to rewrite a narrow task.

## Source and translation controls

- Verify Scripture against a retrievable source in the declared edition, not
  memory. For a discrepancy or consequential change, cross-check an independent
  source and record passage, edition, URL/local source, and result.
- A URL parameter or translation label alone does not prove edition identity.
  CUV 1919 and RCUV 2010 differ; NASB 1995 and NASB 2020 differ. Inspect actual
  source metadata and wording. Do not relabel text or convert 神/上帝 or 做/作
  globally to make it look consistent. Variant-character lints are review leads.
- The project's preferred entry point is ai-eden.com, historically using
  `/bible/BOOK/CHAPTER?t=CUV,NASB&cols=2`. Confirm current availability and
  edition. If empty or rate-limited, retry sparingly, respect retry headers,
  and use an identified reliable fallback. Record the source actually used.
  FHL, BibleGateway, and BibleHub are candidate comparison sources, not
  automatically authoritative for every requested edition.
- Compare supplied manuscript text and report differences; do not repeatedly
  split copyrighted chapters into requests to evade reproduction restrictions.
  Respect source access and quotation limits. Never invent “used by permission”
  or treat a copyright notice as evidence of permission. Check current primary
  publisher terms if rights/public release is in scope.
- Preserve selected excerpts when deliberate: label them as excerpts and state
  their verse ranges. Do not silently expand them into full chapters. Distinguish
  an intentional bilingual selection from a missing-language defect.
- Preserve verse markers, NASB supplied-word italics and other edition details.
  `^n^` and `\jesus{...}` can be valid pipeline syntax. Inspect the builder
  before replacing them. Markdown emphasis inside raw `\jesus{...}` prints
  literally; use supported LaTeX emphasis inside that macro.

## Commentary and Scripture-grounded content review

Quotation marks mean verified wording from the identified work/sermon.
Distinguish original quotation, editor's translation, and unquoted summary;
retain author, work, locator/sermon code, and source. A matching citation ledger
proves bookkeeping consistency, not that quotation words match the source.
Source matching that ignores punctuation does not verify every punctuation mark.

Do not invent historical details, quotations, or certainty in debated exegesis.
Distinguish what the passage says from our interpretive inferences, tradition, and
editorial illustration. In Matthew, avoid asserting Tamar's ethnicity without
evidence, turning genealogy into a literal legal document, or claiming the text
specifies a biological mechanism for the virgin birth. These are examples of
reasoning boundaries, not wording to insert into every chapter.

Ledger parsing can fail when multiple commentators share one H2: inspect the
checker and ledger before changing content to appease it. Existing tooling
expects commentator names such as 摩根 / 麥克阿瑟 in separate H2 headings and
individual `第N章` tokens for verbatim chapter lists. Normalize notices in
dry-run first; a skipped notice is not a verified notice.

## Structure and deduplication

For books using the established eleven-section layout, preserve the progression:
基督焦點 → 配詩 → 經文 → 背景 → 原文研讀 → 領受要點 → 歷代注疏 →
詩篇與聖詩 → 老弟兄查經 → 生命應用 → 與其他經文的關聯.
Do not force unrelated books into this structure without a restructuring brief.

Deduplicate the same thought, not distinct evidence. Keep unique hymns, source
credits, useful cross-references, and meaningful recurring orientation. Compare
Scripture, quotations, hymn content, and references before/after a restructure;
word-count reduction is a diagnostic, not a target proving quality.

Keep the book's established study-unit numbering in H1. Put actual biblical
passage ranges below it and in the coordinate/index when those ranges differ.
Strip YAML by opening/closing delimiters when fixing builders, never by assuming
seven lines. Preserve front matter fields and the actual ordered input list.

## Spiritual spine — inspect, don't just count

The whole book should explain its progression, carry it through part dividers,
locate each study with a coordinate, and close each chapter with a substantive
return to Christ. Check that these say something specific, not merely that the
headings exist. Don't insert a generic Christ paragraph just to pass a checker.

`check-book-spine.py` can miss divider checks when the source directory name
doesn't match the builder slug (Matthew's nested `matthew/book` is one example).
Treat `n/a`, skipped, or missing checks as unverified. Read the builder's divider
inputs and rendered divider pages manually instead of counting these as passes.
