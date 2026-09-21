# Gospel of John Deep Study — Release Checklist

Assigned identity: **Gospel of John Deep Study, Edition 4.0**  
Assigned Scripture versions: **CUV 1919 + NASB 1995**

This checklist separates work that can be verified in the repository from work
that requires a rights holder, contributor, or independent editor.

## Completed repository gates

- [x] All declared source files exist.
- [x] All 29 sources with YAML metadata are checked for the exact assigned title and subtitle; the systematic study has no YAML metadata.
- [x] Maintained examples use CUV 1919 and NASB 1995.
- [x] PDF states that Scripture passages are selected excerpts.
- [x] Final PDF build has zero missing-glyph and overfull-box warnings.
- [x] Rebuilt proof passes the current technical checks (2026-09-21: 327 pages, 372 links, final TeX pass clean). Build log: `../../../output/gospel-of-john-consolidated-build.log`.

## Required human sign-offs

- [ ] Confirm CUV 1919 source edition and punctuation policy.
- [ ] Confirm NASB 1995 quotation permission and required notice with Lockman.
- [ ] Clear or replace MacArthur/Grace to You material.
- [ ] Obtain consent for CCIC unpublished teaching notes.
- [ ] Confirm hymn and translation rights.
- [ ] Independently verify every quotation and bibliography entry.
- [ ] Complete theological/editorial review.
- [ ] Approve print, EPUB, and accessible-PDF proofs.

## Product decision

The current release is a **study guide with selected Scripture excerpts**, not
a complete bilingual Gospel text. A complete bilingual edition requires a
separate verse-pairing pass and a new rights review.

## Commands and evidence

`bash build_release.sh` creates and verifies an editorial proof.
`bash build_release.sh --publish` additionally requires every manifest gate to
have an approved record in `editorial-signoffs.json`, including `status`,
`reviewer`, `date`, and a local `evidence` file path. Technical success does not
approve the book for publication. No approvals have been invented.

Each build regenerates the Scripture index and writes JSON and Markdown passage
inventories into the repository output directory. The inventories count printed
verse markers; they do not certify textual accuracy or complete verses.
