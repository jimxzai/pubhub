#!/usr/bin/env bash
set -euo pipefail
root_dir="$(cd "$(dirname "$0")/.." && pwd)"
fixture_dir="$(mktemp -d /private/tmp/matthew-gate-test.XXXXXX)"
cp "$root_dir"/*.md "$fixture_dir/"
mkdir "$fixture_dir/scripts"
cp "$root_dir/scripts/validate-manuscript.sh" "$root_dir/scripts/release-preflight.sh" "$fixture_dir/scripts/"
bash "$fixture_dir/scripts/validate-manuscript.sh"
if bash "$fixture_dir/scripts/release-preflight.sh" > "$fixture_dir/draft.log"; then
    echo 'FAIL: draft unexpectedly passed release preflight'; exit 1
fi
# Mutate only isolated test fixtures; these are not publication approvals.
perl -pi -e 's/^status: editorial-draft$/status: release-ready/; s/^scripture_policy: pending-clearance$/scripture_policy: cuv1919-nasb1995/' "$fixture_dir"/[0-9][0-9]-*.md
perl -pi -e 's/BLOCKED/CLEARED/g; s/PENDING/CLEARED/g' "$fixture_dir/RIGHTS_MATRIX.md"
perl -pi -e 's/EDITORIAL DRAFT — NOT CLEARED FOR PUBLICATION/RELEASE APPROVED/; s/^- \[ \]/- [x]/' "$fixture_dir/RELEASE_CHECKLIST.md"
bash "$fixture_dir/scripts/release-preflight.sh"
perl -pi -e 's/^- \[x\]/- [ ]/' "$fixture_dir/RELEASE_CHECKLIST.md"
if bash "$fixture_dir/scripts/release-preflight.sh" > "$fixture_dir/unchecked.log"; then
    echo 'FAIL: unchecked reviews unexpectedly passed preflight'; exit 1
fi
echo "PASS: draft rejection, cleared-state acceptance, and unchecked-review rejection ($fixture_dir)"
