# Rights and permissions matrix

**Release:** 馬太福音研讀 — 天國之王 — Gospel of Matthew Deep Study — 2026 整編版  
**Current gate:** BLOCKED — translation policy and permissions are not yet finalized.

**Scope:** legacy files in this directory only. The assigned PDF uses the separate active manuscript in `../matthew/book/`, with CUV 1919/NASB 1995. This legacy gate does not determine that PDF's release status or require a new translation choice.

This matrix prevents the manuscript from silently mixing the source PDF's rights notices with the Markdown package's translation labels. Every row must be completed before commercial or public release.

## Policy decision

| Decision | Current status | Required evidence | Owner |
|---|---|---|---|
| Scripture translation policy | **PENDING** | Written decision selecting CUV 1919 + NASB, RCUV + ESV, or reference-only Scripture | Release editor |
| Territory and format | **PENDING** | Territory, print/e-book/web formats, print run, and distribution channels | Publisher |
| Final copyright notices | **PENDING** | Approved wording from every rights holder | Publisher/legal reviewer |

## Source clearance

| ID | Material | Manuscript use | Status | Required action |
|---|---|---|---|---|
| P1 | Consolidated PDF, 2026 edition | Structure, chapter naming, editorial reference | INTERNAL SOURCE | Keep as provenance; do not treat it as quotation permission |
| B1 | Chinese Scripture translation | Chinese Scripture blocks | PENDING | Confirm exact edition, rights holder, limits, notice, and territory |
| B2 | English Scripture translation | English Scripture blocks | PENDING | Confirm ESV permission or replace with the selected licensed translation |
| C1–C4 | Published commentary sources | Commentary, quotations, paraphrases | PENDING | Record exact edition/page and clear direct or close quotations |
| C5 | Local teaching material | Study synthesis | PENDING | Identify contributors and obtain written release |
| H1 | Hymns and translations | Devotional sections | PENDING | Clear original, translation, arrangement, and excerpt rights separately |
| O1 | Original manuscript contribution | Commentary and editorial work | PENDING | Record author, editor, translator, reviewers, and copyright owner |

## Chapter-level clearance rule

The chapter status in `PASSAGE_COVERAGE.md` is the source of truth for whether a passage is complete or selected. A chapter may move to **CLEARED** only when:

1. the translation policy is selected;
2. every reproduced verse has been checked against the licensed source;
3. every selected excerpt is labeled as selected;
4. all commentary quotations and close paraphrases have source IDs and page references; and
5. the approved copyright notice is present in the final export.

Until then, all numbered chapters remain `status: editorial-draft` and `scripture_policy: pending-clearance`.
