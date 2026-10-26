#!/bin/bash
# One-shot checks for books/bible/ecclesiastes (run from anywhere).
# usage: books/bible/ecclesiastes/sources/check.sh [--fast]    (--fast skips the FHL-fetching ones)
B="$(cd "$(dirname "$0")/.." && pwd)"; R="$(cd "$B/../../.." && pwd)"; C="$B/sources/commentary"
echo "== 1 markup lint";           python3 "$R/scripts/lint-chapter-markup.py" "$B" | tail -2
echo "== 2 scripture text lint";   python3 "$R/scripts/lint-scripture-text.py" "$B" 2>&1 | tail -2
echo "== 3 commentary quotes verbatim (all corpora)"
cat "$C"/corpus-henry.txt "$C"/corpus-bridges.txt "$C"/corpus-morgan.txt "$C"/corpus-gregory.txt "$C"/corpus-gty.txt "$C"/corpus-talmud.txt > "$C"/corpus-all.txt
python3 "$R/scripts/verify-citations.py" "$B" --source "$C/corpus-all.txt" --heading "" 2>&1 | grep -v "^  OK" | grep -v "^$" | grep -v "^[0-9][0-9a-z-]*\.md$" | tail -6
[ "$1" = "--fast" ] && exit 0
echo "== 4 prose citations (quote followed by ref)"; python3 "$R/scripts/verify-prose-citations.py" "$B" --self 傳 2>&1 | tail -6
echo "== 5 cross-ref quotes (ref anywhere on the line)"; python3 "$B/sources/verify_xref_quotes.py" "$B" 2>&1 | tail -12
echo "== 6 spine";                python3 "$R/scripts/check-book-spine.py" "$B" 2>&1 | tail -12
