#!/usr/bin/env python3
"""Audit the internal rights/source package without inferring legal clearance."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSE_MARKER = re.compile(r"\^(\d+)(?:-(\d+))?\^")


def marked_verse_occurrences(text: str) -> int:
    section = re.search(
        r"^### English[^\n]*\n(.*?)(?=^\*\*經文核對\*\*)", text, re.M | re.S
    )
    if not section:
        return 0
    total = 0
    for start, end in VERSE_MARKER.findall(section.group(1)):
        total += int(end or start) - int(start) + 1
    return total


def main() -> int:
    required = ("000-copyright.md", "BIBLIOGRAPHY.md", "RIGHTS-REGISTER.md")
    missing = [name for name in required if not (ROOT / name).exists()]
    if missing:
        print("ERROR: missing rights/source files: " + ", ".join(missing))
        return 1

    chapters = []
    for number in range(1, 29):
        matches = sorted(ROOT.glob(f"{number:02d}-*.md"))
        if len(matches) != 1:
            print(f"ERROR: expected one chapter file for {number:02d}, found {matches}")
            return 1
        chapters.extend(matches)
    hymn_sections = 0
    verse_occurrences = 0
    for path in chapters:
        text = path.read_text(encoding="utf-8")
        if re.search(r"^## 配詩", text, re.M):
            hymn_sections += 1
        verse_occurrences += marked_verse_occurrences(text)

    register = (ROOT / "RIGHTS-REGISTER.md").read_text(encoding="utf-8")
    references = (
        "lockman.org/permission-to-quote",
        "hkbs.org.hk/8",
        "bstwn.org/chinese-bible",
    )
    missing_references = [url for url in references if url not in register]
    if missing_references:
        print("ERROR: missing official rights references: " + ", ".join(missing_references))
        return 1

    print(f"PASS: rights/source package present for {len(chapters)} chapters.")
    print(f"NASB_MARKED_VERSE_OCCURRENCES: {verse_occurrences}")
    print(f"CHAPTERS_WITH_OPENING_HYMN_SECTION: {hymn_sections}/{len(chapters)}")
    print("LEGAL_STATUS: external edition, permission, and contributor review still required.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
