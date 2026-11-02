#!/bin/bash
# 讀懂聖經的希伯來文 — Reading the Hebrew Old Testament: a first guide for new Bible students
# = preface + order-of-revelation chapter + 13 chapters + appendices (series words, top-100 words, parsing glossary,
#   songs, sources) + afterword. Data (counts, parse table, grammar tables, song cards) is generated from OSHB by
#   gen-biblehebrew-data.py; series vocabulary comes from mine-hebrew-wordstudies.py.
# Template: templates/pdf/biblehebrew.latex (derived from revelation.latex). Pipeline: scripts/lib/hebrew-build.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/hebrew-build.sh"
hebrew_build biblehebrew Biblehebrew biblehebrew combine-biblehebrew.py gen-biblehebrew-data.py || exit 1
