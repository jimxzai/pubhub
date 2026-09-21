"""Validate review/release states without treating structural checks as approval."""
import json
import re
from pathlib import Path

GATES = ("rights", "theology", "copyedit", "quotations", "source_reconciliation", "production", "accessibility")

def valid_isbn(value):
    code = re.sub(r"[- ]", "", str(value))
    if len(code) == 13 and code.isdigit() and code.startswith(("978", "979")):
        return sum(int(c) * (1 if i % 2 == 0 else 3) for i, c in enumerate(code)) % 10 == 0
    if re.fullmatch(r"\d{9}[\dX]", code):
        return sum((10-i) * (10 if c == "X" else int(c)) for i, c in enumerate(code)) % 11 == 0
    return False

def validate_release(manifest, root):
    errors = []
    isbn = manifest.get("isbn")
    if isbn and not valid_isbn(isbn):
        errors.append("ISBN has an invalid format or checksum")
    state = manifest.get("release_state", "review")
    if state not in ("review", "approved"):
        errors.append("release_state must be review or approved")
    if state == "review" and "HOLD" not in manifest.get("release_status", ""):
        errors.append("Review editions require a HOLD status")
    if state == "approved":
        if "HOLD" in manifest.get("release_status", ""):
            errors.append("Approved state conflicts with HOLD status")
        records = json.loads((root / "sources/release-approvals.json").read_text())
        for gate in GATES:
            item = records.get(gate, {})
            evidence = item.get("evidence", "")
            if item.get("status") != "approved" or not item.get("reviewer") or not item.get("date") or not evidence:
                errors.append(f"Release blocked: {gate} needs dated reviewer approval and evidence")
            elif not (root / evidence).is_file():
                errors.append(f"Release blocked: {gate} evidence file missing")
    return errors

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "book.json").read_text())
    errors = validate_release(manifest, root)
    if manifest.get("release_state", "review") != "approved":
        errors.append("Release blocked: review edition has not received final approval")
    print("\n".join(errors) if errors else "Release approval records: OK")
    raise SystemExit(bool(errors))
