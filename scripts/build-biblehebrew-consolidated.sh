#!/bin/bash
# 讀懂聖經的希伯來文 — Reading the Hebrew Old Testament, one volume in two parts (like the Greek volume):
#   卷一 a first guide for new Bible students = preface + order-of-revelation chapter + 13 chapters
#   卷二 the Hebrew of each OT book = divider + overview + one chapter per book + index of Hebrew words
#   then appendices (series words, top-100 words, parsing glossary, songs, sources) and the afterword.
# Part 1's data comes from OSHB via gen-biblehebrew-data.py; Part 2's from the OT books' 原文研讀 tables via
# mine-hebrew-wordstudies.py + gen-hebrew-compendium.py; Template: templates/pdf/biblehebrew.latex
# (derived from revelation.latex). Pipeline: scripts/lib/hebrew-build.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/hebrew-build.sh"
hebrew_build || exit 1
