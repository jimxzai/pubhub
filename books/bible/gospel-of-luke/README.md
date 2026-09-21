# 路加福音研讀：指定整編版源稿

This repository contains the editorial source for the assigned consolidated edition. The only canonical deliverable is `output/gospel-of-luke-consolidated.pdf`. It is **not ready for public distribution** until every item marked `HOLD` or `REVIEW` in `rights-ledger.tsv` has been cleared.

## Build

```sh
./validate-book.sh
bash ../../../scripts/build-gospel-of-luke-consolidated.sh
```

The consolidated builder and template under `../../../scripts/` and `../../../templates/` are authoritative. Do not create or distribute alternate `luke-study` PDF or HTML outputs.

## Editorial policy

- Scripture, quotation, paraphrase, historical summary, and original application must remain distinguishable.
- Modern copyrighted material must be paraphrased or licensed before print, ebook, audio, or web release.
- Every source claim must be traceable through `99-appendix-references.md` and the rights ledger.
- The study edition and a shorter reader edition should be treated as separate products.

## Release gate

The current build is an internal proofing build. A passing technical validation does not mean that rights, theology, or copyediting are complete.

For a release check, use `LUKE_RELEASE_MODE=release` with the consolidated builder. It must stop while any `HOLD` or `REVIEW` item remains.

`./build.sh` delegates to that same builder; alternate formats are rejected. Source checks no longer assume seven metadata lines. Builds use a temporary staging directory and replace the canonical PDF only after successful typography checks.

Run `python3 test-production.py` for missing-source and invalid-rights regression checks. A `CLEARED` ledger row requires an additional `evidence` column naming a nonempty approval file relative to the ledger. Evidence contents must still be reviewed by the publisher.

Run `python3 citation-inventory.py` to reproduce the chapter inventory. Read `PRODUCTION_REVIEW.md` for the latest verified results and remaining editorial decisions.
