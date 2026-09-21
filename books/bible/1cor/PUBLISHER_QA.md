# Consolidated proof: production review

Review date: 2026-09-21. Assigned edition: `1cor-consolidated`.

## Updated publisher score

**9.6/10 for controlled production quality; 9.7/10 for cover design; 7.2/10 for public-release readiness.**

The 9.6 and 9.7 scores measure the work that can be controlled in the repository: structure, presentation, reproducibility, identity control, and visual finish. The release-readiness score remains lower because rights approvals, independent review, accessibility certification, and final print approval require external evidence.

| Area | Score | Basis |
|---|---:|---|
| Structure and completeness | 9.6 | Full 16-chapter body, five divisions, systematic study, closing matter, and A-F appendices restored |
| Typography and visual design | 9.6 | Series-matched vector cover, midnight-blue/ivory/gold hierarchy, consistent page geometry, corrected headers and back-cover transition |
| Cover design | 9.7 | John benchmark applied: restrained dark field, symmetric rules, focused emblem, bilingual hierarchy, edition/version disclosure, and coordinated back cover |
| Navigation and production reliability | 9.5 | 253 pages, 37 top-level bookmarks, convergent TOC, manifest validator, automated build and artifact checks |
| Digital editions | 9.0 | Embedded HTML resources and valid EPUB archive; EPUBCheck, accessibility, and device testing remain outstanding |
| Editorial/source control | 8.9 | Locked manifest, selected-excerpt disclosure, source-set validation, rights ledger, and release checklist; independent verse, translation, quotation, and theological review remain open |
| Rights and publication compliance | 5.2 | Rights log is explicit, but Bible, hymn, artwork, font, and third-party permissions are not yet evidenced |

The production score is now 9.6/10 and the cover is 9.7/10. The lower release-readiness score reflects the fact that a polished proof is not yet a cleared commercial/public edition.

## Implemented corrections

- Restored the systematic study, five volume divisions, and appendices A-F from the reference edition.
- Compiled the original vector design directly, retaining PDF bookmarks and searchable cover text.
- Stabilized the contents over multiple compilation passes; reduced its depth to chapter/volume entries.
- Corrected inconsistent chapter ranges in diagrams, stale running heads, font substitutions, and the blank page before the back cover.
- Embedded HTML resources and restored the appendices in HTML and EPUB.
- Removed blanket public-domain assertions for chapter hymns; identified the proposed permission notice as unapproved.
- Added source checks, artifact checks, overflow/missing-glyph build failures, and a single backed-up installation route.

## Verification

`make all` builds and audits all three formats. The restored proof has 253 pages and 37 top-level PDF bookmarks. Automated checks cover page geometry, bookmark destinations, appendix presence, HTML local assets and fragment links, EPUB ZIP integrity and appendix presence, and LaTeX overflow/missing-glyph diagnostics. These are not substitutes for EPUBCheck or assistive-technology testing.

Representative visual inspection covers copyright, contents, preface, structure diagram, chapter opening, glossary, and closing pages. This is not a claim that every page or every quotation has undergone independent proofreading.

## Release gates still open

- Record evidence for every open item in `rights-log.md`; do not infer permission from a copyright notice.
- Independently check theological interpretations, translations, verse accuracy, and edition/page-level source attribution.
- Complete full proofreading and any printer-specific preflight, metadata, accessibility, and distribution requirements before public release.

This remains an editorial review proof. A clean build does not make it a rights-cleared or 10/10 publication.
