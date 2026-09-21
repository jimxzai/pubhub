#!/bin/zsh
set -euo pipefail

root=${0:A:h:h}
cd "$root"

lesson_files=( 0[1-9]-*.md 1[0-9]-*.md 2[0-4]-*.md )
if (( ${#lesson_files} != 24 )); then
  print -u2 "FAIL: expected 24 lesson files, found ${#lesson_files}"
  exit 1
fi

required=(README.md publication.yaml volumes.json Makefile RELEASE-CHECKLIST.md RIGHTS-LEDGER.md EDITORIAL-SIGNOFF.md release-approvals.json appendices/B.md appendices/C.md appendices/D.md appendices/E.md 000-preface.md 000-copyright.md 00-overview.md 99-grace-sufficient.md 999-afterword.md)
for file in $required; do
  [[ -f "$file" ]] || { print -u2 "FAIL: missing $file"; exit 1; }
done

for executable in scripts/verify_consolidated.sh scripts/release_gate.sh ../../../scripts/build-cor2-consolidated.sh; do
  [[ -x "$executable" ]] || { print -u2 "FAIL: missing executable $executable"; exit 1; }
done

for file in $lesson_files; do
  [[ "$(sed -n '1p' "$file")" == "---" ]] || { print -u2 "FAIL: $file has no YAML frontmatter"; exit 1; }
  for key in book_id lesson part title subtitle passage session_date status; do
    rg -q "^${key}:" "$file" || { print -u2 "FAIL: $file missing ${key}"; exit 1; }
  done
done

if rg -n -i 'TODO|FIXME|placeholder|TBD' $lesson_files README.md publication.yaml; then
  print -u2 "FAIL: unresolved editorial marker found"
  exit 1
fi

color_uses=$(rg -o '\\textcolor\{ScriptureGold\}' *.md | wc -l | tr -d ' ')
python3 scripts/build_consolidated.py --check-source

for file in $lesson_files; do
  [[ -n "$(rg -n '^\*\*經文核對\*\*' "$file")" ]] || { print -u2 "FAIL: $file has no scripture verification link"; exit 1; }
done

print "PASS: ${#lesson_files} lesson files, ${color_uses} callouts, source metadata validated. Formal release requires make release-check."
