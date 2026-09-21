# Changelog

## 2026 整編版 — 2026-09-20

- 2026-09-21 使用共享 `.claude/skills/eat-bible` 重新執行 canonical source audit：spine、template、markup、scripture candidate、citation ledger 與 PDF checks 均完成；保留 12 個需要人工回查的 CUV「做／作」候選字。

- Redesigned the canonical template's front and back covers against the Genesis consolidated edition: royal-purple gradient, gold framing, vector crown, stronger bilingual title hierarchy, and concise back-cover copy.
- Kept the assigned edition identity and moved the cover's emphasis to the title; the existing interior map remains in place.

- Corrected the source mapping: the assigned PDF is generated from `books/bible/matthew/book`, not this legacy directory.
- Preserved the active edition's CUV 1919/NASB 1995 policy; corrected the erroneous term “RCUV 1919” in the audit.
- Fixed the legacy validator/preflight contradiction and added isolated draft/release transition checks.
- Applied chapter 1 corrections to the active manuscript: excerpt disclosure, interpretive qualifications, Tamar's identity, and separation of theological inference from textual claims.
- Hardened the active builder against missing inputs and variable-length YAML, and corrected its unsupported Great Commission chronology.

- Standardized all 29 manuscript files to the assigned title and edition identity.
- Aligned chapter headings with the consolidated PDF.
- Replaced unresolved rendering macros and nonstandard verse-marker syntax.
- Marked selected Scripture passages explicitly.
- Added source, passage-coverage, rights, bibliography, and release-control documentation.
- Added structural validation and a release preflight gate.
- Kept the edition in editorial-draft status pending translation permissions and final review.
