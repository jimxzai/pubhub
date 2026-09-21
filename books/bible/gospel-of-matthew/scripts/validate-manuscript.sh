#!/usr/bin/env bash
set -u

root_dir="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root_dir" || exit 1

status=0

for required_file in COPYRIGHT.md SOURCES.md SOURCE_PDF_AUDIT.md PASSAGE_COVERAGE.md EDITORIAL_QA.md RIGHTS_MATRIX.md BIBLIOGRAPHY.md RELEASE_CHECKLIST.md CHANGELOG.md; do
  if [[ ! -f "$required_file" ]]; then
    printf 'ERROR: missing release-control file: %s\n' "$required_file"
    status=1
  fi
done

files=()
for file in [0-9][0-9]-*.md; do
  [[ -f "$file" ]] || continue
  files[${#files[@]}]="$file"
done

if [[ "${#files[@]}" -ne 29 ]]; then
  printf 'ERROR: expected 29 numbered manuscript files; found %s\n' "${#files[@]}"
  status=1
fi

for file in "${files[@]}"; do
  for field in title subtitle author date publisher edition updated language rights source status scripture_policy; do
    if ! rg -q "^${field}:" "$file"; then
      printf 'ERROR: %s is missing front-matter field: %s\n' "$file" "$field"
      status=1
    fi
  done

  for identity in \
    '^title: 馬太福音研讀 — 天國之王$' \
    '^subtitle: Gospel of Matthew Deep Study$' \
    '^date: 2026年8月$' \
    '^edition: 2026 整編版$' \
    '^status: (editorial-draft|reviewed|release-ready)$' \
    '^scripture_policy: (pending-clearance|cuv1919-nasb1995|reference-only)$'; do
    if ! rg -q "$identity" "$file"; then
      printf 'ERROR: %s is not aligned to the assigned 2026 consolidated edition: %s\n' "$file" "$identity"
      status=1
    fi
  done

  if ! rg -q '^# ' "$file"; then
    printf 'ERROR: %s is missing a level-one title\n' "$file"
    status=1
  fi

  if rg -n '\\jesus|\.\.\. \[|\^[0-9]+(?:-[0-9]+)?\^' "$file"; then
    printf 'ERROR: %s contains unresolved rendering or placeholder syntax\n' "$file"
    status=1
  fi
done

selected_files="04-temptation.md 05-beatitudes.md 08-miracles.md 09-calling-matthew.md 11-johns-question.md 12-sabbath-lord.md 14-feeding-walking.md 15-true-purity.md 16-peters-confession.md 17-transfiguration.md 21-triumphal-entry.md 23-woes-pharisees.md 25-parables-judgment.md 26-last-supper-gethsemane.md 27-crucifixion.md 28-resurrection-commission.md"
for file in $selected_files; do
  if ! rg -q '編輯狀態：節選經文' "$file"; then
    printf 'ERROR: %s must identify its Scripture as selected excerpts\n' "$file"
    status=1
  fi
done

if [[ "$status" -eq 0 ]]; then
  printf 'PASS: %s manuscript files passed structural checks\n' "${#files[@]}"
else
  printf 'FAIL: manuscript validation found unresolved issues\n'
fi

exit "$status"
