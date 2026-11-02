#!/bin/bash
# 舊約希伯來文彙編 — A Hebrew Companion to the Old Testament Series
# = preface + how-to-use + overview + book-by-book + lemma index + sources + afterword
# Data comes from mine-hebrew-wordstudies.py (the OT books' 原文研讀 tables) and OSHB, via gen-hebrew-compendium.py.
# Template: templates/pdf/hebrew-compendium.latex (derived from biblehebrew.latex). Pipeline: scripts/lib/hebrew-build.sh
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/hebrew-build.sh"
hebrew_build hebrew-compendium Biblehebrew-compendium hebrew-compendium combine-hebrew-compendium.py gen-hebrew-compendium.py || exit 1
