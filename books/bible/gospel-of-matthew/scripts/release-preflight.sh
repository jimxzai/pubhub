#!/usr/bin/env bash
set -u

root_dir="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root_dir" || exit 1

status=0

if ! bash scripts/validate-manuscript.sh; then
  status=1
fi

if rg -q 'BLOCKED|PENDING' RIGHTS_MATRIX.md; then
  printf 'BLOCKED: rights matrix still contains unresolved permissions or policy decisions\n'
  status=1
fi

if ! rg -q '^\*\*RELEASE APPROVED\*\*$' RELEASE_CHECKLIST.md || rg -q '^- \[ \]' RELEASE_CHECKLIST.md; then
  printf 'BLOCKED: release checklist is not signed off\n'
  status=1
fi

for file in [0-9][0-9]-*.md; do
  if ! rg -q '^status: release-ready$' "$file" || ! rg -q '^scripture_policy: (cuv1919-nasb1995|reference-only)$' "$file"; then
    printf 'BLOCKED: %s needs release-ready status and a resolved Scripture policy\n' "$file"
    status=1
  fi
done

if rg -n '0\.2\.0|2025年12月|title: 馬太福音研讀$' [0-9][0-9]-*.md; then
  printf 'BLOCKED: retired edition identity found in manuscript metadata\n'
  status=1
fi

if [[ "$status" -eq 0 ]]; then
  printf 'PASS: release preflight cleared\n'
else
  printf 'FAIL: release preflight is blocked; resolve the listed external gates\n'
fi

exit "$status"
