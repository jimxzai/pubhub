#!/usr/bin/env bash
set -euo pipefail
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
if test -f "$script_dir/../book.yaml"; then
  book_dir=$(CDPATH= cd -- "$script_dir/.." && pwd)
else
  book_dir=$(CDPATH= cd -- "$script_dir/../books/bible/1cor" && pwd)
fi
make -C "$book_dir" all
python3 "$book_dir/scripts/publish_consolidated.py"
