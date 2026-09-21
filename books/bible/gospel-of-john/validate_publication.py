#!/usr/bin/env python3
"""Validate the Gospel of John publication source tree.

This is intentionally a release gate, not a prose-quality grader. It checks
that the declared source set exists, that study units contain the house
sections, and that the current documentation does not silently describe the
selected-excerpt edition as a complete bilingual Gospel text.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "publication-manifest.json"
STUDY_FILES = {
    "01-prologue.md",
    "01b-first-disciples.md",
    "02-cana-wedding.md",
    "03-nicodemus.md",
    "04-samaritan-woman.md",
    "04b-nobleman-son.md",
    "05-bethesda.md",
    "06-bread-of-life.md",
    "07-feast-tabernacles.md",
    "08-light-of-world.md",
    "09-blind-man.md",
    "10-good-shepherd.md",
    "11-lazarus.md",
    "12-triumphal-entry.md",
    "13-washing-feet.md",
    "14-way-truth-life.md",
    "15-true-vine.md",
    "16-holy-spirit.md",
    "17-high-priestly-prayer.md",
    "18-arrest-trial.md",
    "19-crucifixion.md",
    "20-resurrection.md",
    "21-epilogue.md",
}


def main() -> int:
    errors: list[str] = []
    reviews: list[str] = []

    try:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR manifest: {exc}")
        return 1

    if manifest.get("content_model") != "study-guide-with-selected-scripture-excerpts":
        errors.append("manifest content_model must declare selected Scripture excerpts")
    if manifest.get("translation_policy", {}).get("parallel_text") is not False:
        errors.append("manifest must explicitly set parallel_text=false until parity is complete")

    product_name = manifest.get("product")
    edition = manifest.get("edition")
    if product_name != "Gospel of John Deep Study":
        errors.append("manifest product must remain Gospel of John Deep Study")
    if edition != "4.0":
        errors.append("manifest edition must remain 4.0")
    for language, expected in (("chinese", "CUV 1919"), ("english", "NASB 1995")):
        if manifest.get("translation_policy", {}).get(language) != expected:
            errors.append(f"manifest {language} translation must be {expected}")

    required = manifest.get("required_source_files", [])
    missing = [name for name in required if not (ROOT / name).is_file()]
    errors.extend(f"missing required source: {name}" for name in missing)
    if len(required) != len(set(required)):
        errors.append("manifest contains duplicate sources")
    errors.extend(f"study unit absent from manifest: {name}" for name in STUDY_FILES - set(required))
    texts = {name: (ROOT / name).read_text(encoding="utf-8") for name in required if name not in missing}
    for name, text in texts.items():
        # The systematic study deliberately has no YAML front matter.
        if name == "elder-wong-systematic-study.md":
            continue
        front = re.match(r"\A---\n(.*?)\n---(?:\n|$)", text, re.S)
        if not front:
            errors.append(f"{name}: missing or malformed metadata")
            continue
        for key, value in (("title", "約翰福音研讀"), ("subtitle", "Gospel of John Deep Study")):
            if not re.search(rf"^{key}:\s*{re.escape(value)}\s*$", front[1], re.M):
                errors.append(f"{name}: incorrect {key}")
    for name in ("README.md", "RED-LETTER-GUIDE.md"):
        texts[name] = (ROOT / name).read_text(encoding="utf-8")
    for name, text in texts.items():
        if re.search(r"\b(?:RCUV|ESV)\b|和合本修訂版", text):
            errors.append(f"{name}: obsolete translation reference")

    sections = manifest.get("required_study_sections", [])
    for name in sorted(STUDY_FILES):
        path = ROOT / name
        if not path.is_file():
            continue
        text = texts[name] if name in texts else path.read_text(encoding="utf-8")
        frontmatter = text.split("---", 2)[1] if text.startswith("---") else ""
        if "title: 約翰福音研讀" not in frontmatter:
            errors.append(f"{name}: title drift; expected 約翰福音研讀")
        if "subtitle: Gospel of John Deep Study" not in frontmatter:
            errors.append(f"{name}: subtitle drift; expected Gospel of John Deep Study")
        for section in sections:
            if not re.search(rf"^##\s+{re.escape(section)}(?:\s|$)", text, re.M):
                errors.append(f"{name}: missing required section {section}")
        observed = [heading.split(' (', 1)[0].strip() for heading in re.findall(r'^##\s+(.+)$', text, re.M)]
        if observed != sections:
            errors.append(f"{name}: study sections must occur once in the required order")
        if "經文核對" not in text:
            errors.append(f"{name}: missing Scripture verification link")
        if "中文 — 和合本" not in text:
            errors.append(f"{name}: missing CUV Scripture heading")
        if "English — NASB" not in text:
            errors.append(f"{name}: missing NASB Scripture heading")

        def verse_markers(heading: str) -> list[str]:
            starts = list(re.finditer(rf"^#{{3,4}}\s+{heading}[^\n]*$", text, re.M))
            values: list[str] = []
            for index, start in enumerate(starts):
                end = starts[index + 1].start() if index + 1 < len(starts) else len(text)
                next_heading = re.search(r"^#{1,4}\s+", text[start.end():end], re.M)
                if next_heading:
                    end = start.end() + next_heading.start()
                values.extend(re.findall(r"\^(\d+)\^", text[start.end():end]))
            return values

        cn_verses = verse_markers("中文")
        en_verses = verse_markers("English")
        if cn_verses and en_verses:
            if cn_verses != en_verses:
                reviews.append(
                    f"{name}: selected excerpt markers differ CUV={len(cn_verses)} NASB={len(en_verses)}"
                )

    # Documentation drift that would mislabel the current edition.
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    if "selected Scripture excerpts" not in readme and "經文選摘" not in readme:
        errors.append("README must disclose that Scripture is selected excerpts")
    overview = (ROOT / "00-overview.md").read_text(encoding="utf-8")
    if "CUV 1919" not in overview or "NASB 1995" not in overview or "選摘" not in overview:
        errors.append("overview must state the assigned CUV 1919/NASB 1995 selected-excerpt model")
    for stale in ("RCUV", "ESV", "Revised Version", "complete-book.md"):
        if stale in readme:
            errors.append(f"README contains stale edition reference: {stale}")

    for line in errors:
        print(f"ERROR {line}")
    for line in reviews:
        print(f"REVIEW {line}")
    print(
        f"validated {len(required)} declared files; errors={len(errors)}; "
        f"reviews={len(reviews)}"
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
