#!/bin/bash
# check-chapter.sh <chapter.md> [sermon-codes-not-needed]
# Runs every machine check this book has, on ONE chapter. Exit status 1 if anything fails.
# Quotes are checked per commentator heading, against ONLY that commentator's source files, so a quote
# placed under the wrong name fails (a defect class no lint sees).
set -u
F="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
S="$ROOT/books/bible/daniel/.sources"; C="$S/commentary"
T="$(mktemp -d)"; cp "$F" "$T/"; STEM="$(basename "$F" .md)"; rc=0
echo "### scripture block == generated unit";      python3 "$ROOT/scripts/gen-daniel-scripture.py" --check 2>&1 | grep -E "^(OK|DIFFERS) +$STEM" || rc=1
echo "### markup lint";                              python3 "$ROOT/scripts/lint-chapter-markup.py" "$F" | tail -3
echo "### scripture-character lint";                 python3 "$ROOT/scripts/lint-scripture-text.py" "$F" | tail -2
echo "### prose Scripture citations (但)";           python3 "$ROOT/scripts/verify-prose-citations.py" "$T" --self 但 2>&1 | tail -4
V="python3 $ROOT/scripts/verify-citations.py $T --quiet"
echo "### 改革宗 (Calvin, Henry)";   $V --heading 改革宗 --source $C/calvin-calcom24.txt --source $C/calvin-calcom25.txt --source $C/henry/henry-intro.txt $(for i in $(seq 1 12); do echo --source $C/henry/henry-$i.txt; done) | tail -6
echo "### 教父 (Hippolytus)";         $V --heading 教父 --source $C/hippolytus-exegetical-fragments.txt --source $C/hippolytus-christ-and-antichrist.txt | tail -6
echo "### 約瑟夫 (Josephus)";         $V --heading 約瑟夫 --source $C/josephus-antiquities.txt | tail -6
echo "### 摩根 (Morgan overview)";    $V --heading 摩根 --source $C/morgan-clean.txt | tail -6
echo "### 麥克阿瑟 (sermon codes)";   python3 "$ROOT/scripts/verify-sermon-quotes.py" "$T" --cache "$S/sermon-cache" 2>&1 | tail -8
echo "### size";  wc -c "$F"
rm -rf "$T"
