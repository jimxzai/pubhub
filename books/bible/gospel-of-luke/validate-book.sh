#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
python3 "$ROOT_DIR/production-check.py" "${LUKE_RELEASE_MODE:-proof}"
test -s "$ROOT_DIR/../../../scripts/build-gospel-of-luke-consolidated.sh"
test -s "$ROOT_DIR/../../../templates/pdf/gospel-of-luke.latex"
test ! -e "$ROOT_DIR/build/luke-study.pdf"
test ! -e "$ROOT_DIR/build/luke-study.html"
echo "Validation passed: canonical builder, complete sources and valid rights ledger."
