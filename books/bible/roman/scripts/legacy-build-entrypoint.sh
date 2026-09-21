#!/bin/bash
# Compatibility entry point, installed at pubhub/scripts/build-romans-consolidated.sh.
set -euo pipefail
ROMANS_PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
exec make -C "$ROMANS_PROJECT_ROOT/books/bible/roman" pdf
