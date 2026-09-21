#!/usr/bin/env python3
"""Offline citation-structure check.

This deliberately does not claim to prove that quotations match a source. That
requires an editorial comparison against the recorded edition and archive.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    manifest = json.loads((ROOT / "book.json").read_bytes().decode("utf-8"))
    registry = json.loads((ROOT / "sources" / "registry.json").read_bytes().decode("utf-8"))
    errors: list[str] = []
    if not registry.get("sources"):
        errors.append("source registry is empty")
    for source in registry.get("sources", []):
        if not source.get("id") or not source.get("label") or not source.get("urls"):
            errors.append("every source record requires id, label, and urls")
        for url in source.get("urls", []):
            if not re.match(r"^https?://", url):
                errors.append(f"invalid source URL: {url}")

    chapter_count = 0
    for name in manifest["source_order"]:
        if not re.match(r"^(?:0[1-9]|1[0-6])-", name):
            continue
        chapter_count += 1
        text = (ROOT / name).read_bytes().decode("utf-8")
        if "經文核對" not in text:
            errors.append(f"{name}: missing Scripture verification note")
        if not re.search(r"出處|來源|核對|三方資源", text):
            errors.append(f"{name}: missing a source/provenance marker")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"OK: {chapter_count} chapters have citation/provenance markers")
    print("NOTE: quotation-level verification and permissions remain editorial release gates")
    return 0


if __name__ == "__main__":
    sys.exit(main())
