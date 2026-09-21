#!/bin/bash
set -euo pipefail

# Historical filename retained; accessibility certification is a separate gate.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Rebuild the pair so EPUB print-page references cannot drift from the PDF.
exec python3 "$SCRIPT_DIR/publishing/publication.py" "$@"
