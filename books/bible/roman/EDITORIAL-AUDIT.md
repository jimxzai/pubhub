# Romans Deep Study — publisher audit

Date: 2026-09-21. Assigned identity and filename are unchanged.

## Controls learned from Gospel of John

- The 348-page, 7 × 10-inch original PDF remains the physical-layout authority; the shorter manuscript build remains a reference only.
- Source identity, chapter-section order, translation policy, and duplicate/missing-source checks are now explicit in `book.json`, `publication-manifest.json`, and `scripts/check_book.py`.
- Scripture text, prose references, historical quotations, rights, theological review, accessibility, and printer proof are separate gates. A technical pass does not close a human gate.
- The cover is treated as a tested product surface: title, subtitle, edition, versions, date, hierarchy, trim, and rendered overflow are checked in `COVER-AUDIT.md`.
- Regression tests intentionally include false-pass cases for source drift, section-order drift, invalid release evidence, ISBN checksum, and quotation-source hash drift.

## Current evidence

- 348 pages; 504 × 720 pt trim; original baseline comparison retained.
- Prior merge audit: 196 pages wholly unchanged; 144 further pages compared outside approved rectangles; eight earlier corrected/cover pages retain their prior treatment.
- Current inventory checked 2026-09-21: 256 bookmarks and 366 total link annotations. Earlier 254-bookmark / 382-link figures are historical.
- Checked 2026-09-21: 13 regression tests pass; `scripts/check_book.py` validates 26 ordered sources and 16 chapters. These checks do not establish quotation clearance.
- The cover rebuild is based on the Romans navy/gold series treatment, with metadata corrected to `Edition 1.1 · CUV · NASB 1995 · 2026-09-20`.

## Open gates

See [publisher status](PUBLISHER-FIX-REPORT.md) for separate recorded scores and evidence limits, including 51 unresolved Chinese Scripture differences and 46 unresolved quoted passages.

Rights, quotation-level source retention, independent theological and bilingual review, accessible PDF reading order/tagging, and printer-specific proof remain open. The release state therefore remains `review`/`HOLD`.
