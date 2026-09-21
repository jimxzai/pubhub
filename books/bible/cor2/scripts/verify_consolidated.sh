#!/bin/zsh
set -euo pipefail
root=${0:A:h:h}
exec python3 "$root/scripts/verify_publication.py" "${1:-$root/../../../output}"
