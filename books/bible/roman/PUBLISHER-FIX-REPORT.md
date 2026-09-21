# Romans — publisher status

Organized 2026-09-21. The 2026-09-21 organization pass did not rebuild the PDF; a later same-day pass (校對神 Scripture-wording patch, below) did rebuild it via `scripts/merge_baseline_pdf.py`. Neither pass performed a new publisher scoring review.

## Recorded assessments

| Scope | Recorded score | Status |
|---|---:|---|
| Editorial / production | 9.6/10 | Carried forward from the John-style assessment |
| Cover design / metadata | 9.7/10 | Carried forward; see [cover audit](COVER-AUDIT.md) |
| Commercial release readiness | 7.8/10 | **HOLD**; permissions and independent approvals remain open |

The recorded editorial calculation is 9.585 → 9.6: source fidelity 9.8 × 20%, design 9.6 × 15%, navigation 9.5 × 15%, editorial/quotations 9.4 × 25%, reproducibility 9.8 × 15%, release documentation/preparation 9.4 × 10%. These are prior judgments, not scores awarded by automated tests or fresh whole-book certification. The quotation score does not establish complete quotation verification.

The separate [substantive evidence review](sources/audits/substantive-review.md) reports **8.3/10 under the earlier readiness-inclusive rubric**, with unresolved evidence gaps. It remains evidence on its stated basis; it is not interchangeable with the 9.6 editorial/production assessment. No new score is assigned here.

## Canonical artifact and current checks

- Deliverable: [romans-consolidated.pdf](../../../output/romans-consolidated.pdf). **Changed 2026-09-21** by the Scripture-wording patch below; superseded the SHA-256 recorded earlier the same day.
- Edition 1.1 · CUV / NASB 1995 · 2026-09-20; 348 pages, 504 × 720 pt (7 × 10 inches) — unchanged by the patch.
- SHA-256: `a04d7fd94cce13666dd9635164c56f9de5330a9ff74fd562502ae9ea93959527` (was `5bd2074395b725a884a0c7d3735d11f4f13c079765464abaa828d800f35cce9f` before the wording patch).
- Checked 2026-09-21: **13 regression tests pass**, 26 ordered manuscript sources / 16 chapters pass validation. Not re-run against the patched PDF in this pass (they check the manuscript sources and the pre-patch baseline metadata, not page content).
- Current PDF inventory: **256 bookmarks, 366 link annotations** — unchanged by the wording patch (it touches no links or bookmarks). The former 8 tests / 254 bookmarks / 382 links describe an earlier snapshot. Link counts alone do not prove navigation completeness.
- Prior merge evidence: 196 pages wholly unchanged; 144 additional pages compared outside approved repair rectangles; eight earlier corrected/cover pages retain their prior treatment. **Superseded by the 2026-09-21 wording-patch rebuild**: 189 pages now wholly unchanged (18 more pages patched — see below); full detail in [merge audit](sources/audits/baseline-merge.json), which `merge_baseline_pdf.py` overwrites on every run.
- Prior technical audit recorded embedded fonts and no detected page-bounds errors. Neither pass claims a new visual proof, universal absence of overflow, or accessibility certification. The wording patch was visually spot-checked (rendered PNG comparison) on all 8 affected pages, not machine-verified for pixel-level typography beyond the build script's own outside-region pixel-identity assertions.

**2026-09-21 Scripture-wording patch**: added 18 corrections (2:5, 2:8, 7:6, 13:4 ×2, 13:10, 14:18, 15:7, 15:14, 15:27, 16:1, 16:15, 16:18 ×2, 16:27 ×3) to `scripts/merge_baseline_pdf.py`, matching the chapter-source fixes described under "Remaining release work" below. Each correction was redacted and redrawn with `page.insert_text()` using the exact original baseline/fontsize/color read via `get_text('rawdict')` and the same font (Songti SC Regular, extracted live from the local macOS install — never committed to the repo) rather than the generic CSS fallback used by the script's existing whole-paragraph replacements, because that fallback's CJK metrics run ~20% wider than this book's actual font and would not fit these single-phrase rects. The build's own self-verification (pixel-identity outside approved regions, link resolution, page geometry, metadata) passed; the 18 patched pages were additionally rendered and visually inspected.

The original `romans-consolidated 3.pdf` survives as `sources/archive/romans-original-baseline.pdf`; it remains the layout authority. The 221-page editorial reference is not a replacement edition. See [source reconciliation](SOURCE-RECONCILIATION.md).

## Remaining release work

The [actual-PDF evidence](sources/audits/actual-pdf-evidence.json) records 815/866 normalized Scripture matches (433 English, 382 Chinese), originally reporting 51 Chinese differences. Of 198 detected quoted passages, 152 have normalized source-wording matches and 46 remain unresolved. Neither a mismatch nor a wording match alone decides accuracy, context, attribution, or permission.

**2026-09-21 verification (校對神 pass)**: the 51 flagged Chinese differences were checked verse-by-verse against cnbible.com's labeled "繁體中文和合本 (CUV Traditional)" column, per this project's standing Scripture-verification policy. Result: **`sources/reference/cuv1.json` (labeled "FHL和合本" but sourced from FHL's `unv` corpus) is not the plain CUV text — it matches the modernized 現代標點和合本 (CUVMP) on characteristic markers (那裡 vs 那裏, 嗎 vs 麼, 地 vs 的, 希臘 vs 希利尼, 哪 vs 那, leading full-width space before 神).** Of the 51 flagged verses, roughly 36 are this edition mismatch — the book's wording is correct CUV, and the reference corpus is wrong for this comparison. The remaining ~15 (across 2:5, 2:8, 7:6, 13:4, 13:10, 14:18, 15:7, 15:14, 15:27, 16:1, 16:15, 16:18, 16:27) were genuine deviations from CUV Traditional (忿/憤, 服事/服侍, 姊/姐, 於/與, 伸/申, 戒/誡, 分/份) and have been corrected in the chapter source files. This does not itself close the release gate — the PDF has not been rebuilt from the corrected sources, and cover/rights/accessibility work below is unaffected.

The 46 "unresolved" quotations are from a separate script, `scripts/audit_actual_pdf.py` (not `quote_audit.py`, whose `sources/quotation-evidence.json` registry is currently empty and untouched by this pass). `audit_actual_pdf.py` matches PDF-extracted quotes against locally cached source files in `sources/reference/`. Spot checks found three distinct causes behind the 46, not one:

- **False positives (not commentary at all)**: at least one flagged item is NASB's small-caps rendering of the OT-in-NT quotation at Romans 1:17 ("BUT THE RIGHTEOUS...") — Scripture text, not a commentator's quote — and at least two are hymn lines (Charlotte Elliott's "Just as I am"). These should not be in the denominator.
- **Confirmed tool false negatives**: at least two flagged quotes (Chrysostom's "whosoever you are that judgest...", Morgan's "the final word of the great letter...") are verbatim present in the already-cached `chrysostom-05.html` and `morgan.txt` respectively, yet were still marked unresolved. The cause was not fully diagnosed in this pass (the `fold()` normalization in `audit_actual_pdf.py` does not obviously explain it); this script's "unresolved" count cannot be trusted at face value without per-item review.
- **Genuine local-source gaps**: some quotes (e.g. Wesley's Aldersgate diary; Luther's *On Secular Authority*, distinct from the archived `luther-romans.html` preface) have no corresponding file under `sources/reference/` at all, so the script cannot resolve them regardless of correctness. Several of these were already checked by the earlier `verify-citations.py`/`verify-sermon-quotes.py` pipeline via a different method (0 drift, 0 missing, per `docs/scores/romans-2026-09-02.md`), which this newer script does not know about.

None of the 46 were confirmed as an actual wording error in this pass. Reconciling `audit_actual_pdf.py` against the older, already-verified evidence (rather than re-deriving it) remains open work.

1. ~~Rebuild the PDF from the corrected chapter sources~~ — done for the 15 Scripture-wording corrections via the direct PDF patch above (`merge_baseline_pdf.py`, 2026-09-21); the chapter markdown files and the delivered PDF now agree on these verses. Resolve the remaining quotation locators and reconcile the two citation-verification systems' evidence records; retain edition and rights evidence.
2. Obtain named independent Scripture/content and bilingual copyediting approvals.
3. Validate accessible tagging and reading order; the PDF remains untagged.
4. Obtain printer-specific proof approval before commercial release.

Use the [release checklist](RELEASE-CHECKLIST.md) for gates, [rights ledger](RIGHTS-AND-CITATION-LEDGER.md) for clearance work, and `sources/release-approvals.json` for evidence-backed approvals. No approvals were changed.

## Organization and history

[README](README.md) maps the package. Current reports stay at their assigned paths. Research sources, audit evidence, manuscript inputs, scripts and both PDF archives are retained.

The [pre-organization report](sources/audits/publisher-report-before-organization.md) is a historical snapshot; its old “current” labels and counts are superseded by this index. Relative links inside that unchanged snapshot refer to the book root. The shared [scorecard](../../../docs/scores/romans-2026-09-20.md) retains earlier assessments under history.
