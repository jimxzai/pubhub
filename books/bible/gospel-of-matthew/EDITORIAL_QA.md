# Editorial QA standard

**Assigned release:** 馬太福音研讀 — 天國之王 — Gospel of Matthew Deep Study — 2026 整編版

This file is the release checklist for the Matthew study set. It is intentionally separate from the reader-facing chapters so editors can use it during every revision.

## Chapter template

Each numbered chapter should contain, in this order:

1. Front matter with the assigned title, subtitle, author, date, publisher, edition, updated date, language, rights reference, source record, draft status, and Scripture policy.
2. A clear chapter title and passage range.
3. Scripture, explicitly labeled as **complete text** or **selected excerpts**.
4. Context and literary structure.
5. Observation and interpretation, clearly distinguished.
6. Word study only where the Greek/Hebrew claim is sourced and checked.
7. Theological synthesis and cross-references.
8. Application, reflection, and prayer.
9. Sources with edition/page or stable URL.

## Automated checks

Run:

```sh
bash scripts/validate-manuscript.sh
bash scripts/release-preflight.sh
```

The structural command must pass with zero unresolved macros, placeholders, missing front-matter fields, or missing chapter files. The release preflight is expected to remain blocked until `RIGHTS_MATRIX.md` and `RELEASE_CHECKLIST.md` are fully cleared.

## Human checks before release

- Compare every quoted verse against the licensed RCUV or ESV source.
- Confirm every stated passage range matches the verses actually reproduced.
- Reconcile the chapter against `PASSAGE_COVERAGE.md` before changing any excerpt to “complete.”
- Reconcile the Markdown package against `SOURCE_PDF_AUDIT.md` before importing structure, quotations, or rights notices from the consolidated PDF.
- Mark excerpts clearly; never imply that a partial quotation is complete.
- Verify all direct quotations and close paraphrases with edition and page references.
- Assign every external source a register ID in `SOURCES.md`; “integrated resources” alone is not an acceptable citation.
- Clear Scripture, commentary, hymn, and translation rights in `COPYRIGHT.md`.
- Complete `RIGHTS_MATRIX.md` and `BIBLIOGRAPHY.md`; do not treat a passing structural check as legal clearance.
- Check Traditional Chinese terminology, punctuation, names, and theological vocabulary.
- Review contested interpretations as interpretations, not settled facts.
- Render and proofread PDF, EPUB, and web output on desktop and mobile.
- Check heading hierarchy, links, reading order, contrast, and alt text.

## Release gate

Publication is **blocked** until the rights register is complete, all 29 chapters pass structural validation, the theological review is signed off, and a final proofreader approves the rendered files.
