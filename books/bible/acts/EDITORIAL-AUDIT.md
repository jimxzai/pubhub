# Acts Publisher Audit — 2026 整編版

Controlled edition: **使徒行傳研讀 — Acts of the Apostles Deep Study — 2026 整編版**.

## Current score

**9.6 / 10 for internal publisher production.**

| Area | Score | Evidence / remaining gap |
|---|---:|---|
| Biblical and theological spine | 9.7 | 1:8, Spirit, witness, and the unfinished mission are carried through all five volumes and 28 chapters. |
| Editorial architecture | 9.8 | Orientation, five volume dividers, chapter coordinates, conclusion, and afterword are controlled by one canonical builder. |
| Bilingual passage control | 9.6 | Strict validator passes; 22 intentionally independent reference pairs are explicitly labeled. |
| Commentary and study usability | 9.4 | Chapter rhythm is consistent and leader-friendly; final source-level citation review remains open. |
| Production quality | 9.7 | 435 pages, 7×10 in, embedded fonts, bookmarks, metadata, zero missing glyphs, zero overfull boxes. |
| Rights and release readiness | 8.8 | NASB, hymn, and modern-commentary permissions still require documented closure before public distribution. |

The rights score is the only material ceiling on a public-release score above 9.7. It is deliberately not represented as closed.

## Completed in this pass

- Kept Acts isolated from Romans and preserved the assigned title, version, and canonical output name.
- Made `make pdf` delegate to the repository-level canonical Acts builder; the divergent 321-page local PDF was removed from the release path and retained recoverably in `/private/tmp/acts-upgrade/`.
- Corrected date metadata to 2026-09-20 and made the NASB permission status accurate.
- Repaired front-matter stripping and safe chapter counting in the canonical builder.
- Removed unsupported small-caps requests, added a real header-height reserve, and added an explicit cover edition/version line.
- Rebuilt and checked the canonical 435-page PDF.

## Release blockers still requiring human sign-off

1. Lockman/NASB permission and exact notice language.
2. Hymn lyric and translation permissions.
3. Permission/source confirmation for modern commentary quotations.
4. Final historical, chronological, Greek, and quantitative fact-check sign-off.
5. Accessibility/EPUB/HTML export review if those formats are distributed.
