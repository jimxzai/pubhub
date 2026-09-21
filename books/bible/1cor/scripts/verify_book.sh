#!/usr/bin/env bash
set -euo pipefail

root_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$root_dir"

inputs=(
  elder-wong-systematic-study.md
  000-preface.md 000-copyright.md 00-overview.md 00a-1cor-position.md 00b-cross-spine.md
  ch01.md ch02.md ch03.md ch04.md ch05.md ch06.md ch07.md ch08.md
  ch09.md ch10.md ch11.md ch12.md ch13.md ch14.md ch15.md ch16.md
  99-until-he-comes.md 99-appendix-references.md 999-afterword.md
)

for file in "${inputs[@]}"; do
  test -f "$file" || { echo "ERROR: missing controlled input: $file" >&2; exit 1; }
  test "$(head -n 1 "$file")" = "---" || { echo "ERROR: missing YAML front matter: $file" >&2; exit 1; }
done

test -f assets/1cor-consolidated-cover.png || { echo "ERROR: missing canonical cover asset" >&2; exit 1; }
for file in templates/1cor.latex templates/book.css assets/images/dove.png assets/images/gloriousFreedom.jpg; do
  test -f "$file" || { echo "ERROR: missing build asset: $file" >&2; exit 1; }
done

for n in $(seq 1 16); do
  file=$(printf 'ch%02d.md' "$n")
  grep -q "^chapter: $n$" "$file" || { echo "ERROR: chapter metadata mismatch: $file" >&2; exit 1; }
  grep -q '^\\newpage$' "$file" || { echo "ERROR: chapter lacks a controlled PDF page break: $file" >&2; exit 1; }
done

if grep -RniE '\\(textcolor|textbf|begin|end|vspace|jesus)' "${inputs[@]}"; then
  echo "ERROR: raw TeX command remains in controlled reader files" >&2
  exit 1
fi

if grep -RniE 'TODO|FIXME|TBD|待補|placeholder' "${inputs[@]}"; then
  echo "ERROR: unresolved editorial marker remains" >&2
  exit 1
fi

if grep -Rni '^### English — NASB$' ch*.md; then
  echo "ERROR: NASB excerpts must be labeled as selected readings" >&2
  exit 1
fi

for file in "${inputs[@]}"; do
  fences=$(grep -c '^```' "$file" || true)
  test $((fences % 2)) -eq 0 || { echo "ERROR: unbalanced Markdown fence: $file" >&2; exit 1; }
done

echo "OK: ${#inputs[@]} controlled files passed structural checks."
