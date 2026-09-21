#!/bin/zsh
set -euo pipefail

root=${0:A:h:h}
cd "$root"

failed=0
while IFS=$'\t' read -r source target; do
  [[ -z "$target" ]] && continue
  if [[ ! -f "$target" ]]; then
    print -u2 "FAIL: $source links to missing local file $target"
    failed=1
  fi
done < <(perl -ne 'while(/\]\(([^)#?]+\.md)(?:#[^)]+)?\)/g){ print "$ARGV\t$1\n"; }' *.md)

if (( failed )); then
  exit 1
fi

print "PASS: all local Markdown links resolve."
