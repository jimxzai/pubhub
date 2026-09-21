# Romans substantive review - 2026-09-21

## Comparable overall assessment: 8.3 / 10, provisional

This continues the six weighted dimensions behind the user's 7.9 score. It does not substitute a different rubric to claim 9+. A concurrent workspace scorecard reports 9.6 for a differently defined editorial/production scope; that claim is retained as separate work, not adopted as verification by this audit.

| Existing dimension | Before | Now | Weight | Evidence and remaining defect |
|---|---:|---:|---:|---|
| Source fidelity | 9.5 | 9.5 | 20% | Original 348-page order, size and pagination retained; baseline hash fixed. |
| Design and typography | 9.2 | 9.2 | 15% | Existing covers retained; representative proof reviewed. New correction text still differs typographically from the original interior. |
| Structure and reader navigation | 8.5 | 9.3 | 15% | 133 printed labels/headers and 16 contents entries corrected; two reader guides, 256 bookmarks. |
| Editorial and quotation reliability | 6.5 | 7.3 | 25% | Factual/interpretive defects corrected; actual-PDF source comparisons added. 51 CUV differences and 46 quoted-passage candidates remain unresolved. |
| Production reproducibility | 9.0 | 9.4 | 15% | 13 tests, all-page geometry/decoder/link checks, embedded fonts, region-preservation checks; no printer proof yet. |
| Rights and accessibility readiness | 4.0 | 4.0 | 10% | No new permission or expert sign-offs. Language metadata added, but PDF remains untagged. |

Calculation: 9.5×.20 + 9.2×.15 + 9.3×.15 + 7.3×.25 + 9.4×.15 + 4.0×.10 = **8.310**, displayed **8.3**. Scores are editorial judgment, not certification. Cover was not rescored in this substantive pass. Release remains HOLD.

## Artifact and authority

- Canonical PDF: `/Users/jimxiao/Documents/GitHub/pubhub/output/romans-consolidated.pdf`.
- SHA-256: `5bd2074395b725a884a0c7d3735d11f4f13c079765464abaa828d800f35cce9f`.
- 348 pages, 504 × 720 points. Assigned titles and edition 1.1 retained.
- Authority: `sources/archive/romans-original-baseline.pdf`, not the shorter manuscript PDF. Original hash: `abed9a6294db5db9a9da7fc96a5e482d36013103ce74783048434339a515524b`.
- Builder: `scripts/build_book.py` → `scripts/merge_baseline_pdf.py`; measured repairs in `scripts/editorial_upgrade.py`, vector covers in `scripts/cover_design.py`. Markdown order remains in `book.json`; optional manuscript outputs are not substitutes for the original PDF.
- Pre-change proof retained at `/tmp/romans-before-substantive.pdf`; permanent original/reference archives remain untouched.

## Implemented corrections

1. Replaced misleading internal Chapter 8–27 labels on the sixteen biblical studies with Romans 1–16: 133 chapter-opening/running-head labels. Corrected sixteen contents prefixes to R1–R16 and explained the notation. Existing contents links and printed page numbers preserved.
2. Physical pages 244 and 259: removed the false claim that Romans 13 never names Jesus; both now explicitly acknowledge 13:14.
3. Physical page 152: corrected the claim that presence/absence of the Greek article distinguishes senses of nomos. Romans 7:21 has an article before nomon; context remains essential. The Greek wording is visible in the [Nestle 1904 and Westcott–Hort texts](https://biblehub.com/text/romans/7-21.htm).
4. Physical page 154: removed an unsupported contemporary-majority claim and stopped presenting one interpretation of 7:25 as the common conclusion of competing readings.
5. Physical page 331: exposed the arithmetic mismatch in the historical Morgan ledger: 19+14+3=36, not 46; its ten-item subset cannot be counted twice.
6. Filled existing blank pages 6 and 8 with reading/interpretation guidance, source-type distinctions, edition caveats and an error-reporting protocol. No new pages inserted.
7. Mirrored the substantive corrections into chapters 7 and 13 and the reference-appendix manuscript. Added document language and modification metadata; no PDF/UA claim.

## Actual PDF evidence, not manuscript proxy

`make pdf-audit` produces `actual-pdf-evidence.json` and `reference-catalog.json` in this directory. The audit extracts the canonical PDF and retains source hashes and unresolved cases.

- Scripture: 433 Chinese + 433 English verse entries checked. **815/866 normalized matches**: **433/433 NASB**, **382/433 CUV**. All 51 differences are in CUV. These include older spellings, translator parentheses and wording differences; they are not all established errors. No silent conversion to a different Chinese edition was made.
- Comparison texts: recovered FHL `unv` Traditional Chinese chapter data and Bible Hub pages explicitly labeled NASB 1995. A live [NASB 1995 Romans 7 page](https://biblehub.com/nasb/romans/7.htm) was also inspected. Original retrieval dates for recovered files are unknown; recovery is not a fresh retrieval claim.
- Quoted-passage inventory: **198 candidates**, **152 normalized source-wording matches**, **46 unresolved**. This broad double-quoted, Latin-alphabet inventory can include quoted Scripture in prose, hymn fragments and German; it is not identical to the previous 193-item Markdown inventory. Scripture blocks are excluded from this quotation count.
- Normalization ignores case, punctuation, whitespace, compatibility ligatures and two specified Chinese character variants. It does not certify punctuation, omissions, attribution, context, Chinese translation or permission. Source candidates are leads for attribution review, not automatic approvals.
- Fresh research: eight additional primary-text editions retrieved on 2026-09-21, including [Augustine's Spirit and Letter](https://www.newadvent.org/fathers/1502.htm), [Against Two Letters I](https://www.newadvent.org/fathers/15091.htm), [Calvin's Institutes, Beveridge translation](https://www.ccel.org/c/calvin/institutes/cache/institutes.html3), and [Luther's Romans preface, Thornton translation](https://www.ccel.org/l/luther/romans/pref_romans.html). Exact files/URLs/hashes are in the catalog; retrieval does not grant redistribution rights.

## Ten-dimension editorial coverage (diagnostic, not a new scored mean)

| House dimension | Status and coverage | Main remaining gap |
|---|---|---|
| Scripture accuracy | Checked now: 866 verse entries by normalized comparison | Resolve 51 CUV differences against the assigned print edition; punctuation/italics proof |
| Format consistency | Checked now: 16 study labels/contents entries, all affected headers; manuscript structure check | Full-book bilingual style review |
| Layout and production | Checked now: all-page decoder/bounds/links; representative Poppler renders | Print-size proof and typographic harmonization |
| Logical structure | Checked now: chapter 7 discussion, chapter 13 contradiction, reading guide | Independent whole-book argument review |
| Chapter-specific insights | Sample reviewed: 1, 4, 7, 9, 13, 16; not all chapters freshly assessed | Full substantive review rather than heading counts |
| Commentary verifiability | Checked now: 198 candidate comparisons | 46 unresolved; locators/context/translation still need review |
| Bilingual completeness | Checked now: 433 verse entries in each language | Detailed edition variants, notes and punctuation |
| Citation format | Checked now: method guide and ledger arithmetic | Reconcile all historical 'verified' claims with per-quote evidence |
| Usability | Checked now: 16 chapter destinations, numbering, added guides | Reader testing and assistive-technology review |
| Spiritual spine | Sample read: chapter openings 1, 4, 9, 13, 16 and new whole-book route | Not all sixteen returns to Christ freshly reviewed |

## Verification and acceptance

- Thirteen regression tests passed, including region-masking negative test, real-page editorial corrections, 16 labels, verse-source counts, cover identity, quotation drift and release guards.
- `scripts/check_book.py`: 26 declared sources and 16 numbered chapters pass.
- Skill `audit_pdf.py`: 348 pages; zero reported bounds/decoder/local-link errors; 16 distinct chapter bookmarks. Blank pages 2/4 retained as original versos.
- Fonts embedded; language `zh-Hant`. Tagging and accessible reading order remain unverified.
- Preservation: 196 pages entirely unchanged from original; 144 additional pages checked pixel-for-pixel outside approved rectangles at 0.75 scale; eight earlier correction/cover pages retain the previous treatment. All original local-link destinations and page labels retained.
- Current pre-publication canonical file was separately compared against the proof: no appearance differences outside this pass's approved regions, preserving concurrent cover metadata work.
- Poppler pages viewed: 1, 6, 8, 12, 52, 100, 152, 154, 181, 244, 259, 294, 331, 348. No observed clipping/overlap in the revised regions. This is a representative review, not a full visual proof of every line.

## Work required for a defensible 9+

1. Resolve the 51 CUV differences against an identified copy of the assigned edition; approve each retained variant/correction, then rerun the comparison.
2. Finish the 46 quotation-source leads, review matched quotations' actual locators/context and Chinese translations, and replace or accurately label unsupported claims.
3. Obtain independent theological and bilingual copyediting sign-offs covering the complete book.
4. Record material-specific rights decisions; complete tagged-PDF reading-order/device testing and the printer proof.

Acceptance is evidence closure, not a changed score label. This pass improves the book but does **not** establish 9+ overall readiness.
