#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
if [ "$#" -gt 1 ] || [ "${1:-pdf}" != pdf ]; then
  echo "Only the assigned consolidated PDF is supported." >&2
  exit 2
fi
exec bash "$ROOT_DIR/../../../scripts/build-gospel-of-luke-consolidated.sh"
