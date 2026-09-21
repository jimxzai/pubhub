# Release checklist

**Assigned release:** 馬太福音研讀 — 天國之王 — Gospel of Matthew Deep Study — 2026 整編版

## Current status

**EDITORIAL DRAFT — NOT CLEARED FOR PUBLICATION**

## Required sign-offs

- [ ] Translation policy selected and recorded in `RIGHTS_MATRIX.md`.
- [ ] Scripture passages checked against the licensed edition.
- [ ] Selected excerpts and complete passages labeled accurately.
- [ ] Secondary-source quotations and paraphrases cited in `BIBLIOGRAPHY.md`.
- [ ] Hymns, maps, illustrations, and local teaching material cleared.
- [ ] Copyright page contains approved notices.
- [ ] Chinese copy edit completed.
- [ ] Biblical and theological review completed.
- [ ] Final PDF, EPUB, and web exports rendered and proofread.
- [ ] Accessibility review completed: reading order, headings, links, contrast, and alt text.
- [ ] Final checksum and source archive recorded.

## Automated gates

```sh
bash scripts/validate-manuscript.sh
bash scripts/release-preflight.sh
```

The structural validator should pass during editing. The release preflight must pass only after all external rights and review gates are cleared.

