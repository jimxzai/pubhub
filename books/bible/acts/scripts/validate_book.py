#!/usr/bin/env python3
"""Validate the Acts manuscript package before production."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = [ROOT / f"{n:02d}-" for n in range(1, 29)]


def chapter_files() -> list[Path]:
    files: list[Path] = []
    for prefix in CHAPTERS:
        matches = sorted(ROOT.glob(prefix.name + "*.md"))
        if len(matches) != 1:
            raise RuntimeError(f"expected one file for {prefix.name}, found {matches}")
        files.extend(matches)
    return files


def has_front_matter(text: str) -> bool:
    return text.startswith("---\n") and "\n---\n" in text[4:]


def verse_set(section: str) -> set[int]:
    verses: set[int] = set()
    for start, end in re.findall(r"\^(\d+)(?:-(\d+))?\^", section):
        first = int(start)
        last = int(end or start)
        verses.update(range(first, last + 1))
    return verses


def scripture_sections(text: str) -> tuple[str, str, str, str]:
    chinese = re.search(r"^(### 中文[^\n]*)\n(.*?)(?=^### English|^\*\*經文核對\*\*)", text, re.M | re.S)
    english = re.search(r"^(### English[^\n]*)\n(.*?)(?=^\*\*經文核對\*\*)", text, re.M | re.S)
    return (
        chinese.group(1) if chinese else "",
        chinese.group(2) if chinese else "",
        english.group(1) if english else "",
        english.group(2) if english else "",
    )


def main() -> int:
    strict = "--strict" in sys.argv[1:]
    errors: list[str] = []
    warnings: list[str] = []
    resolved_independent_pairs = 0

    required_sections = (
        "基督焦點",
        "配詩",
        "經文",
        "背景",
        "原文研讀",
        "領受要點",
        "歷代注疏",
        "詩篇與聖詩",
        "老弟兄查經",
        "生命應用",
        "與其他經文的關聯",
    )

    book_files = sorted(
        path
        for path in ROOT.glob("*.md")
        if path.name
        not in {
            "README.md",
            "RIGHTS-REGISTER.md",
            "PASSAGE-MAP.md",
            "BIBLIOGRAPHY.md",
            "EDITORIAL-AUDIT.md",
            "RELEASE-CHECKLIST.md",
        }
    )
    all_files = book_files
    for path in all_files:
        text = path.read_text(encoding="utf-8")
        if path.name != "elder-wong-systematic-study.md" and not has_front_matter(text):
            errors.append(f"missing front matter: {path.name}")
        if "\\jesus{" in text and "\\newcommand{\\jesus}" not in (ROOT / "build/header.tex").read_text():
            errors.append(f"undefined production macro reference: {path.name}")

    for path in chapter_files():
        text = path.read_text(encoding="utf-8")
        for section in required_sections:
            if not re.search(rf"^## {re.escape(section)}", text, re.M):
                errors.append(f"{path.name}: missing section {section}")

        chinese_heading, chinese, english_heading, english = scripture_sections(text)
        if not chinese or not english:
            errors.append(f"{path.name}: missing Chinese or English Scripture section")
            continue
        cuv = verse_set(chinese)
        nasb = verse_set(english)
        if cuv != nasb:
            independently_labeled = (
                "獨立參考" in chinese_heading
                and "Independent Reference" in english_heading
            )
            if independently_labeled:
                resolved_independent_pairs += 1
                continue
            warnings.append(
                f"{path.name}: Scripture ranges differ; CUV-only={sorted(cuv - nasb)}, "
                f"NASB-only={sorted(nasb - cuv)}"
            )

    if warnings:
        print("WARNINGS:")
        print("\n".join(f"- {warning}" for warning in warnings))
        print("\nThese are publication blockers until the bilingual passage policy is resolved.")

        if strict:
            errors.extend(warnings)

    if errors:
        print("ERRORS:")
        print("\n".join(f"- {error}" for error in errors))
        return 1

    print(f"PASS: validated {len(all_files)} Markdown files and {len(chapter_files())} chapter files.")
    if resolved_independent_pairs:
        print(
            f"PASSAGE_POLICY: {resolved_independent_pairs} chapter pairs are explicitly labeled "
            "independent reference excerpts."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
