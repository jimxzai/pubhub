# Acts Release Checklist

## Controlled identity

- [x] Title: 使徒行傳研讀 — Acts of the Apostles Deep Study — 2026 整編版
- [x] Canonical artifact: `../../output/acts-consolidated.pdf`
- [x] Canonical builder: `../../scripts/build-acts-consolidated.sh`
- [x] No alternate `dist/acts-study.pdf` remains in this package.

## Editorial and structural QA

- [x] `make check`
- [x] `make release-check`
- [x] `make rights-audit` (documentation audit; not permission approval)
- [x] 28 chapter files and 28 chapter coordinates
- [x] Five volume dividers and 28 Christ-focused endings
- [x] CUV/NASB passage policy documented in `PASSAGE-MAP.md`
- [x] Bibliography and rights register present

## PDF QA

- [x] 435 pages, 7×10 in trim
- [x] Bookmarks and metadata present
- [x] Fonts embedded and Unicode-capable
- [x] Zero missing-glyph warnings
- [x] Zero overfull-box warnings
- [x] Cover, contents, volume divider, interior, and back matter visually checked

## Human release approvals

- [ ] NASB/Lockman permission and notice approved
- [ ] Hymn permissions approved
- [ ] Commentary quotation permissions approved
- [ ] Final scholarly fact-check signed off
- [ ] Accessibility and alternate-format QA signed off
