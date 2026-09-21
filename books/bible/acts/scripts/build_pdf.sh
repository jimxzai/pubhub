#!/bin/bash
set -euo pipefail

# One canonical Acts production path. This wrapper intentionally delegates to
# the repository builder so `make pdf` cannot create a second, divergent book.
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PUBHUB_ROOT="$(cd "$ROOT_DIR/../../.." && pwd)"
exec bash "$PUBHUB_ROOT/scripts/build-acts-consolidated.sh" "$@"
