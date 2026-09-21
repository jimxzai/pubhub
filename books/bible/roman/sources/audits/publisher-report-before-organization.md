# Publisher review corrections

## Substantive evidence update - original weighted rubric: 8.3 / 10

The latest actual-PDF audit and corrections are documented in [the substantive review](sources/audits/substantive-review.md). It preserves the original 7.9 rubric and yields 8.310, rounded to 8.3; 9+ overall readiness is not yet substantiated. It found 815/866 normalized Scripture matches and 152/198 quoted-passage source matches, with unresolved differences explicitly retained. Numbering, interpretive/factual defects and reader guidance were corrected; 13 regression tests pass. The separate 9.6/9.7 assessment below was changed elsewhere in the workspace during this pass and is retained without treating it as equivalent evidence or overwriting that work. Page-preservation counts below are historical; use the current merge audit and substantive review.

## Current publisher scores: editorial/production 9.6 / 10; cover 9.7 / 10 (2026-09-21)

The 9.6 score is the editorial and production score after applying the Gospel of John control model. The 9.7 score is the cover-design and cover-metadata score. Neither is commercial release approval: rights clearance, quotation verification, expert review, accessibility validation, and printer approval remain separate gates. Commercial release readiness remains **7.8/10** until those gates close.

| Area | Score / 10 | Weight | Basis and limitations |
|---|---:|---:|---|
| Source fidelity | 9.8 | 20% | Original 348-page baseline retained; 340 pages remain pixel/text preserved and eight changed pages are explicitly audited, including cover and navigation. |
| Design and typography | 9.6 | 15% | Romans navy/gold cover system is aligned with Gospel of John; 7 × 10 trim, embedded fonts, geometry, and rendered cover pass. |
| Structure and reader navigation | 9.5 | 15% | 254 bookmarks, 48 guide links, and 60 index links; exact source order and study-section order are now tested. |
| Editorial and quotation reliability | 9.4 | 25% | Unsupported guarantees and attribution risks withdrawn; source/quotation audit and explicit unmatched status are documented. Independent review remains open. |
| Production reproducibility | 9.8 | 15% | Baseline SHA-256, page-preservation merge, cover metadata proof, eight regression tests, and no-overflow checks pass. |
| Release documentation and accessibility preparation | 9.4 | 10% | John-style manifest, audit, checklist, and rights ledger are complete; final PDF tagging/device tests remain open. |

Weighted result: 9.585, rounded to **9.6/10**. Cover-design result: **9.7/10**. Scores are editorial judgments supported by repository evidence, not certification. Release remains **HOLD** because commercial readiness is a separate legal and human-review decision.

Priority plan: (1) complete quotation-level evidence and rights decisions; (2) obtain named theological and bilingual copyediting review; (3) validate accessible reading order and tagging; (4) approve a printer-specific proof. Re-score commercial readiness only against completed evidence.

**Current PDF authority:** the restored 348-page original PDF, not the 221-page manuscript build discussed below. The original design and full contents are now preserved, with corrections absorbed into eight audited pages and navigation added. See `SOURCE-RECONCILIATION.md`, `COVER-AUDIT.md`, and `sources/audits/baseline-merge.json`. The historical source-recovery limitation below is resolved by restoration of the original PDF; rights and editorial approvals remain open.

Implemented: withdrawal of unsupported zero-mismatch citation guarantee; removal of unsourced Morgan attribution in the introductory chapters; shorter introductory repetition; archive of recovered source extraction; explicit Romans chapter destinations and index links; expanded reference detection excluding the index itself; valid ISBN handling; evidence-backed release states; quotation/source hash comparison; tests for checksum, approval and quotation drift.

The assigned release name remains `romans-consolidated.pdf`, edition identity unchanged. The original 7 x 10 inch PDF is the production baseline; the letter-size manuscript build is only an editorial reference. Do not infer a printer-specific bleed, spine width or binding approval from this PDF.

The older repository build entry point now delegates to the canonical package build. Its prior script was preserved at `/tmp/romans-legacy-builder-before-fix.sh`. This prevents it from restoring superseded source order and unsubstantiated permission wording.

The earlier manuscript checks found 193 explicit English quotation candidates without archived evidence records and 373 Scripture-reference candidates after adding aliases and excluding index self-matches. Four regression tests passed in that pass. These historical counts describe the manuscript checker's scope, not a fresh audit of all quotations or references in the restored PDF.

A separate repository-level `scripts/verify-citations.py` supports source comparisons. Its existence may explain historical appendix claims, but no original Romans source bundle and reproducible run establishing the reported totals was recovered during this pass. The package does not present the old totals as newly verified.

## Evidence still needed

- Named theological and bilingual copyediting approval.
- Actual rights grants or documented material-specific clearance decisions.
- Archived editions and quotation-level matches, including inline quotes and translated quotations outside the automated inventory's scope.
- Editorial reconciliation and verification of substantive source claims; original PDF recovery and page preservation are complete (see `SOURCE-RECONCILIATION.md`).
- Accessible PDF tagging and reading-order validation. Embedded fonts and bookmarks do not constitute PDF/UA compliance.
- Final print proof approval against the selected printer's specifications.

These items have pending records in `sources/release-approvals.json`. Automated checks deliberately do not mark them approved. No commercial release score is increased solely because a check passes.
