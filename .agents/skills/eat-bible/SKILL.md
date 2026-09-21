---
name: eat-bible
description: Build, edit, improve, proofread, visually verify, and score PubHub bilingual Bible-study books and consolidated PDFs. Use for Scripture and commentary verification, chapter structure and spiritual spine, publisher-quality covers, PDF defects, and scoped edition cleanup in this repository.
---

# Eat Bible — PubHub publishing

Adapted from this repository's Claude `eat-bible` skill, incorporating the
Matthew publication work through 2026-09-21. This is a repository-local Codex
edition, not a standalone general PDF tool. Keep the original Claude skill,
shared driver, and baseline intact; do not create a second baseline history.

Repository paths below are relative to `pubhub/`; `references/` and `scripts/`
links are relative to this skill. Locate the repository by walking upward for
`.claude/skills/eat-bible/driver.sh` and `templates/pdf`, not by assuming cwd.

## Establish identity and scope first

Read the actual builder, its ordered inputs, template, output assignments,
and the latest relevant score. Do not source or execute a builder to discover
paths. Record the canonical manuscript, output filename, title/edition,
translation pair, and requested scope before editing. Preserve these choices.

For Matthew, the assigned artifact is
`output/gospel-of-matthew-consolidated.pdf`; the builder is
`scripts/build-gospel-of-matthew-consolidated.sh`, which reads
`books/bible/matthew/book/`, **not** the similarly named legacy
`books/bible/gospel-of-matthew/`. Its current template is
`templates/pdf/gospel-of-matthew.latex`; the declared translations are CUV
1919 / NASB 1995. Recheck these assignments rather than assuming this historical
mapping can never change. General RCUV/ESV project defaults do not authorize
changing this explicitly assigned edition.

- **Evaluate / score / plan:** inspect read-only; do not rebuild, rewrite
  notices, record baselines, or delete versions. Save a score report only when
  the user requests an update or a report artifact.
- **Fix / improve:** implement the requested changes and verify their effects.
  A cover request does not authorize rewriting Scripture or restructuring the book.
- **Cleanup:** read [publishing.md](references/publishing.md); resolve exact
  redundant targets and preserve canonical outputs, build inputs, and evidence.

## Choose the relevant workflow

In newly authored prose, headings, reviews, and cover copy, refer to the teacher
as **老弟兄 / Elder Brother**. Describe our own work as **領受、亮光**, Scripture
insights, or reflections, not as our theology. Preserve “神學 / theology” only
when faithfully presenting another person's own terminology, quotation, or
original title, with clear attribution. Keep bibliographic identities and paths
intact; never apply a blind global replacement. For guided study, the optional
`ask-elder-wong` skill supplies the corresponding voice and source safeguards.

- Manuscript, quotations, translation, or spiritual spine:
  read [editorial.md](references/editorial.md).
- PDF build, fonts, tables, cover design, visual verification, or cleanup:
  read [publishing.md](references/publishing.md).
- Publisher evaluation, updated score, improvement priorities, or release claim:
  read [scoring.md](references/scoring.md).

Use the smallest relevant checks. A broad publication upgrade needs editorial
review as well as build and visual checks; a narrow cover change needs a
reference comparison and an interior-regression check. Do not turn either into
the other. If required evidence is unavailable, identify the unverified area
instead of inventing a pass or silently expanding the task.

## Shared tools and evidence

Run repository tools from the root with the canonical directory and actual
template slug. Inspect CLI help/implementation if an argument or side effect
is unclear. These commands are examples, not a mandatory all-books sequence:

```text
python3 scripts/check-book-spine.py CANONICAL_DIR
bash scripts/lint-templates.sh TEMPLATE_SLUG
python3 scripts/lint-chapter-markup.py CANONICAL_DIR
python3 scripts/lint-scripture-text.py CANONICAL_DIR
python3 scripts/check-citation-ledger.py CANONICAL_DIR
python3 scripts/normalize-commentary-notice.py CANONICAL_DIR --dry-run
python3 scripts/verify-citations.py CANONICAL_DIR --source VERIFIED_WORK.txt
python3 scripts/verify-sermon-quotes.py CANONICAL_DIR
```

The sermon verifier fetches sources and writes caches; it is not a purely
read-only local lint. Without `--dry-run`, the notice normalizer edits files.
The shared `.claude/skills/eat-bible/driver.sh BUILD_SLUG` rebuilds the assigned
PDF and log. Its `--record-baseline` updates the shared baseline: use only
after an intended, inspected result, never to hide a regression. The driver's
PASS means its checks passed, not that the book has no defects.

For additional read-only PDF checks (requires PyMuPDF in the chosen Python):

```text
python3 .agents/skills/eat-bible/scripts/audit_pdf.py PDF --log BUILD_LOG
python3 .agents/skills/eat-bible/scripts/audit_pdf.py PDF --expected-chapters 28 --chapter-pattern '(?:\d+\s+)?第[一二三四五六七八九十]+章'
python3 .agents/skills/eat-bible/scripts/audit_pdf.py PDF --compare-interior BEFORE.pdf
```

The helper scans all pages, renders at low resolution to exercise the decoder,
checks text bounds and local destinations, and emits JSON with an artifact
hash. The interior comparison excludes only the first and last pages and
checks text, not typography. Automated success still requires viewing rendered
pages. See `python3 .../audit_pdf.py --help` for limits/options.

## Finish with an honest handoff

State what changed, canonical output link, checks actually run, unresolved
issues, and any cleanup/recovery location. Separate observed facts from prior
claims and current recommendations. Do not silently commit, publish, migrate
engines, change translations, or update shared baselines. If a check regresses,
inspect and undo only this task's changes; preserve other work.
