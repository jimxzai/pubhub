# Consolidated edition production review — 2026-09-21

Canonical artifact: `../../../output/gospel-of-luke-consolidated.pdf`.

## Current scorecard

- Overall professional edition score: **9.6/10**.
- Cover and back cover: **9.7/10** — Gospel-of-John-level series lockup, refined vector emblem, thematic strapline, bilingual/Greek layering and explicit edition/source metadata.
- Interior layout and navigation: **9.6/10** — consistent 7 × 10 inch pages, chapter structure, map, dividers and reading hierarchy.
- Technical PDF quality: **9.5/10** — 299 pages; zero missing-glyph, overfull-box and underfull-box warnings in the canonical build.
- Publication readiness: **8.7/10** — held below release grade until Scripture edition comparison, quotation permissions and final editorial sign-off are documented.

The canonical Luke output set is clean: one assigned PDF plus its matching build log and combined Markdown source; no alternate Luke PDF or HTML version remains in `output/`.

## Implemented

- One build entry point, rejecting alternate PDF/HTML names.
- Required sources, unique chapter files, metadata boundaries and chapter structure checked before building.
- Ledger schema, required assets, status values and approval-evidence files checked; unresolved and malformed records block release.
- PDF staged before promotion; missing glyphs, overfull boxes and compilation failure prevent replacement.
- Reference 8:9 corrected to 8:25 on the Galilee divider.
- Narrative part boundaries aligned; overview explains whole-chapter placement across narrative boundaries.
- Cover diagrams enlarged and separated; bilingual contents reserve a page-number column.
- Front and back covers upgraded to the Genesis series standard with a deep-blue/gold visual system, vector emblem, stronger title hierarchy and concise bilingual back-cover copy.
- Cover system refined against Gospel of John: explicit series/book lockup, thematic strapline, halo/ray emblem finish, Greek/English/Chinese concept line, and CUV/NASB edition metadata.
- Natural bottom-page spacing enabled to remove underfull-box warnings without changing page size or chapter order.
- Proof/distribution wording reconciled; back-cover description acknowledges quotations and summaries.

## Checks performed

- Four production regression tests passed, including invalid/empty/missing rights records and missing chapters.
- MacArthur: 63 quoted passages matched their attributed cached sermon transcripts; no missing or unresolved matches. Normalized text matching is not an audio, translation or permissions audit.
- Morgan: 85 matches plus one OCR-tolerant match against `/tmp/morgan_luke.txt`; no drift or missing matches. This verifies wording against that local source, not territorial rights or printed page references.
- CUV comparison against `/tmp/cuv_luke.json` examined 610 verse units across 25 candidate files and reported differences. These include edition spellings, verse boundaries, notes and excerpts. The result is not a clean pass and must not be represented as one.
- Chapter inventory is reproducible using `citation-inventory.py`. NASB marker/range counts exclude unmarked passages and template/front/back-matter repetitions; they are not a complete permission tally.

## Outstanding work requiring evidence or editorial decision

1. Select the exact authoritative CUV edition, then adjudicate comparison differences verse by verse (including 2:14, 8:25, 9:16, 16:13, 22:19 and 24:30). Do not blanket-replace variant characters.
2. Finish the whole-work NASB count, including partial and repeated quotations outside the main English Scripture sections, and verify wording against the licensed edition.
3. Attach permission or other documented rights basis for every commentary quotation and hymn version/translation. An English source match is not permission, and paraphrasing does not automatically resolve all rights issues.
4. Verify patristic/Reformation summaries, Greek glosses, bibliographic page locators and historical claims against primary sources; obtain theological/copyeditor sign-off.
5. Proof every page at final size, confirm the printer's paper/binding/bleed/colour requirements and approve a physical sample. Digital accessibility tagging remains incomplete.

No new ISBN or permission has been obtained. The edition remains an editorial proof. Technical checks do not establish publication clearance; the 8.7/10 publication-readiness score remains conditional on the outstanding evidence above.
