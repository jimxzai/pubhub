#!/usr/bin/env python3
"""Manifest and edition-drift checks for the assigned 1cor-consolidated proof."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def front(text):
    match = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
    return match.group(1) if match else ""

def main():
    manifest = json.loads((ROOT / "publication-manifest.json").read_text())
    errors = []
    if manifest.get("identifier") != "1cor-consolidated":
        errors.append("assigned identifier drift")
    if manifest.get("content_model") != "study-guide-with-selected-scripture-excerpts":
        errors.append("content model must disclose selected excerpts")
    policy = manifest.get("translation_policy", {})
    if (policy.get("chinese"), policy.get("english"), policy.get("parallel_text")) != ("CUV 1919", "NASB 1995", False):
        errors.append("translation policy drift")
    required = manifest.get("required_source_files", [])
    if len(required) != len(set(required)):
        errors.append("duplicate required source")
    for name in required:
        path = ROOT / name
        if not path.is_file():
            errors.append(f"missing source: {name}")
            continue
        text = path.read_text()
        if name != "elder-wong-systematic-study.md" and not front(text):
            errors.append(f"missing metadata: {name}")
    for n in range(1, 17):
        text = (ROOT / f"ch{n:02d}.md").read_text()
        if not re.search(rf"^chapter: {n}$", front(text), re.M):
            errors.append(f"chapter metadata drift: ch{n:02d}.md")
    overview = (ROOT / "00-overview.md").read_text()
    if not all(term in overview for term in ("CUV 1919", "NASB 1995", "經文選摘")):
        errors.append("overview lacks selected-excerpt/version disclosure")
    for path in [ROOT / "README.md", ROOT / "rights-log.md", ROOT / "PUBLISHER_QA.md"]:
        text = path.read_text()
        if "1cor-consolidated" not in text:
            errors.append(f"assigned identity missing: {path.name}")
    stale = re.compile(r"\b(?:RCUV|ESV|NIV|NASB 2020|1cor-combined)\b")
    for path in [ROOT / "README.md", ROOT / "book.yaml", ROOT / "00-overview.md"]:
        if stale.search(path.read_text()):
            errors.append(f"edition drift: {path.name}")
    for error in errors:
        print("ERROR", error)
    print(f"validated {len(required)} sources; errors={len(errors)}")
    return 1 if errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
