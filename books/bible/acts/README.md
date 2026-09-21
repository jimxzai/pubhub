# 使徒行傳研讀 — Acts of the Apostles Deep Study — 2026 整編版

This directory is the source package for a Traditional Chinese bilingual Acts study guide.

## Editorial position

The assigned edition is **使徒行傳研讀 — Acts of the Apostles Deep Study — 2026 整編版**, by **PubHub 三書精讀系統**. The intended audience is church small groups, Bible-study leaders, and mature readers who want a devotional study with historical and Greek-language notes. The manuscript remains an internal rights-review edition until the register is closed.

## Build and QA

Requirements:

- Pandoc 3+
- XeLaTeX with `xeCJK`
- A Traditional Chinese CJK font; the default build uses `STSong`. The default main font is `Arial Unicode MS` so polytonic Greek terms render. Override fonts with `make CJK_FONT="Songti TC" MAIN_FONT="..."` when needed.

Run the structural audit:

```sh
make check
```

Run the release gate:

```sh
make release-check
```

Audit the internal source and rights package:

```sh
make rights-audit
```

This audit verifies that the package is documented; it does not grant permission or replace legal review.

Build a PDF draft:

```sh
make pdf
```

The canonical PDF is written to `../../output/acts-consolidated.pdf` by the repository-level
Acts builder. The local `make pdf` target delegates to that same builder; no alternate Acts
edition is produced from this folder.

## Publication gates

Before public release, the following must be closed:

1. Chinese and English Scripture selections must use identical verse ranges, or the sections must be explicitly labeled as non-parallel reference excerpts. The current package passes this structural gate.
2. The bilingual policy is documented in [PASSAGE-MAP.md](PASSAGE-MAP.md); changes to verse selection must update both chapter headings and the map.
3. Permissions must be documented for NASB, CUV, hymn lyrics/translations, and all modern commentary quotations.
4. Historical, chronological, Greek, and quantitative claims require source-level verification.
5. A complete bibliography, permissions log, copyright page, edition statement, and contributor credits must be added.
6. PDF, EPUB, and accessible HTML outputs must pass visual and structural QA. The canonical PDF is the controlled release artifact; alternate local PDFs are not release candidates.

## Source order

The numeric filename prefix is the canonical reading order. `elder-wong-systematic-study.md` is a supplementary structural study and should be treated as an appendix or leader resource, not as an unmarked chapter.
