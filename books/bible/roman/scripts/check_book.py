#!/usr/bin/env python3
"""Deterministic structural checks for the Romans Deep Study source package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "book.json"

EXPECTED_IDENTITY = {
    "title": "羅馬書研讀 — Romans Deep Study — 2026 整編版",
    "subtitle": "Romans Deep Study",
    "author": "PubHub 三書精讀系統",
    "publisher": "三書精讀出版系統",
    "date": "2026-09-20",
}


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    if not MANIFEST.exists():
        print("ERROR: missing book.json")
        return 1

    manifest = json.loads(MANIFEST.read_bytes().decode("utf-8"))
    order = manifest.get("source_order", [])
    required = manifest.get("required_chapter_sections", [])

    for key, expected in EXPECTED_IDENTITY.items():
        if manifest.get(key) != expected:
            fail(f"book.json {key} must be {expected!r}", errors)

    required_metadata = {
        "identifier",
        "edition",
        "copyright",
        "release_status",
    }
    missing_metadata = sorted(key for key in required_metadata if not manifest.get(key))
    if missing_metadata:
        fail(f"book.json missing release metadata: {', '.join(missing_metadata)}", errors)
    from release_gate import validate_release
    errors.extend(validate_release(manifest, ROOT))
    if "998-colophon.md" not in order:
        fail("manifest is missing the edition and copyright colophon", errors)
    for control_file in ("PASSAGE-MAP.md", "ROMANS-EDITORIAL-REVIEW.md", "RIGHTS.md", "EDITORIAL-AUDIT.md", "RELEASE-CHECKLIST.md", "RIGHTS-AND-CITATION-LEDGER.md", "COVER-AUDIT.md", "publication-manifest.json"):
        if not (ROOT / control_file).exists():
            fail(f"missing release-control document: {control_file}", errors)

    if len(order) != len(set(order)):
        fail("book.json contains duplicate source files", errors)

    for name in order:
        path = ROOT / name
        if not path.exists():
            fail(f"manifest source does not exist: {name}", errors)
            continue
        text = path.read_bytes().decode("utf-8")
        if not text.startswith("---\n"):
            fail(f"missing YAML front matter: {name}", errors)
        front = text.split("\n---\n", 1)[0]
        for key, expected in EXPECTED_IDENTITY.items():
            if not re.search(rf"^{re.escape(key)}:\s*{re.escape(expected)}$", front, re.M):
                fail(f"{name}: front matter {key} is not the assigned edition identity", errors)
        if re.search(r"\\(?:begin|end|textcolor|textbf|textit|vspace|large)", text):
            fail(f"raw LaTeX remains in manuscript source: {name}", errors)
        if re.search(r"\^\d+\^", text):
            fail(f"non-portable verse-number syntax remains: {name}", errors)
        if re.search(r"\b(?:TODO|FIXME|TBD|PLACEHOLDER)\b", text, re.I):
            fail(f"unfinished marker remains: {name}", errors)

    chapter_names = [name for name in order if re.match(r"^(?:0[1-9]|1[0-6])-", name)]
    if len(chapter_names) != 16:
        fail(f"expected 16 numbered chapter sources, found {len(chapter_names)}", errors)

    for name in chapter_names:
        text = (ROOT / name).read_bytes().decode("utf-8")
        headings = re.findall(r"^## (.+)$", text, flags=re.M)
        observed = [heading.split(" (", 1)[0].strip() for heading in headings]
        if observed[:len(required)] != required:
            fail(f"{name}: required study sections must occur in the manifest order", errors)
        for section in required:
            if not any(section in heading for heading in headings):
                fail(f"{name}: missing required section {section}", errors)
        if not re.search(r"^### 中文 — 和合本", text, re.M):
            fail(f"{name}: missing Chinese Scripture heading", errors)
        if not re.search(r"^### English — NASB 1995$", text, re.M):
            fail(f"{name}: missing NASB Scripture heading", errors)

    registry = ROOT / "sources" / "registry.json"
    if not registry.exists():
        fail("missing sources/registry.json", errors)
    else:
        try:
            registry_data = json.loads(registry.read_bytes().decode("utf-8"))
            if not registry_data.get("sources"):
                fail("source registry has no source records", errors)
        except json.JSONDecodeError as exc:
            fail(f"invalid sources/registry.json: {exc}", errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        print(f"{len(errors)} structural check(s) failed")
        return 1

    print(f"OK: {len(order)} sources checked; {len(chapter_names)} numbered chapters validated")
    print("OK: semantic verse markup, manuscript headings, source registry, and release markers are clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
