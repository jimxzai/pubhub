#!/usr/bin/env bash
# Build an editorial proof. --publish requires documented approvals.
set -Eeuo pipefail
BOOK_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$BOOK_ROOT/../../.." && pwd)"
if [[ $# -gt 1 || ( $# -eq 1 && "$1" != "--publish" ) ]]; then
  echo 'Usage: bash build_release.sh [--publish]' >&2
  exit 2
fi
python3 "$BOOK_ROOT/validate_publication.py"
if [[ "${1:-}" == "--publish" ]]; then
  python3 "$BOOK_ROOT/check_signoffs.py"
fi
BOOK_PUB_SKIP_VALIDATOR=1 bash "$REPO_ROOT/scripts/build-gospel-consolidated.sh"
python3 "$BOOK_ROOT/verify_pdf.py" \
  "$REPO_ROOT/output/gospel-of-john-consolidated.pdf" \
  "$REPO_ROOT/output/gospel-of-john-consolidated-build.log"
echo 'Editorial proof built and verified.'
