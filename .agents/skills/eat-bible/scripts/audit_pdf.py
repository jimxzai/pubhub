#!/usr/bin/env python3
"""Read-only PDF production checks; requires PyMuPDF (import fitz).

Exit 0: enabled automated checks passed; 1: defects; 2: input/dependency error.
Does not certify visual quality, editorial accuracy, permissions, or PDF/UA.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys

try:
    import fitz
except ImportError:
    raise SystemExit("PyMuPDF is required; use an environment with import fitz available.")


def fingerprint(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def check_log(path):
    log = path.read_text(encoding="utf-8", errors="replace")
    errors = []
    if not re.search(r"This is (?:XeTeX|LuaHBTeX|LuaTeX|pdfTeX)", log):
        errors.append("Build log lacks a TeX engine banner; warning counts are unverified")
    if "Output written on" not in log:
        errors.append("Build log lacks completed TeX output")
    for label, pattern in (
        ("missing glyphs", r"Missing character:"),
        ("overfull boxes", r"Overfull \\[hv]box"),
        ("TeX errors", r"^!|Error producing PDF|Emergency stop|Fatal error occurred"),
    ):
        count = len(re.findall(pattern, log, re.MULTILINE))
        if count:
            errors.append(f"Build log: {label}: {count} occurrences (may span repeated passes)")
    return errors


def inspect_pdf(path, *, expected_chapters=None, chapter_pattern=None,
                log=None, compare_interior=None, tolerance=1.0):
    errors = []
    report = {"pdf": str(path.resolve()), "sha256": fingerprint(path),
              "errors": errors, "limitations": [
                  "Bounds checks do not detect every overlap, clipped glyph, or column overflow.",
                  "Low-resolution decoder renders do not replace visual page review.",
                  "A text comparison cannot prove unchanged interior typography.",
                  "Build log identity/freshness requires checking the actual build context.",
              ]}
    fitz.TOOLS.mupdf_warnings(reset=True)
    with fitz.open(path) as doc:
        if doc.needs_pass:
            raise ValueError("Encrypted PDF requires a password; not audited")
        if not doc.is_pdf or not len(doc):
            raise ValueError("Expected a nonempty PDF")
        report.update(pages=len(doc), metadata=doc.metadata,
                      text_empty_pages_for_review=[], chapter_bookmarks=None)
        chapters = []
        for _, title, page in doc.get_toc():
            if page != -1 and not 1 <= page <= len(doc):
                errors.append(f"Invalid bookmark destination: {title!r} -> {page}")
            if chapter_pattern and re.match(chapter_pattern, title):
                chapters.append((title, page))
        if chapter_pattern:
            report["chapter_bookmarks"] = len(chapters)
        if expected_chapters is not None:
            if (len(chapters) != expected_chapters or
                    len({title for title, _ in chapters}) != expected_chapters):
                errors.append(f"Expected {expected_chapters} distinct chapter bookmarks; found {len(chapters)}")
            if any(page < 1 for _, page in chapters):
                errors.append("A chapter bookmark has no usable page destination")
        texts = []
        for number, page in enumerate(doc, 1):
            # Text coordinates are unrotated; page.rect itself follows rotation.
            bounds = page.rect * page.derotation_matrix
            words = page.get_text("words", clip=fitz.INFINITE_RECT())
            text = page.get_text("text", clip=fitz.INFINITE_RECT())
            texts.append(text)
            if not text.strip():
                report["text_empty_pages_for_review"].append(number)
            outside = [word[4] for word in words if
                       word[0] < bounds.x0 - tolerance or word[1] < bounds.y0 - tolerance or
                       word[2] > bounds.x1 + tolerance or word[3] > bounds.y1 + tolerance]
            if outside:
                errors.append(f"Page {number}: {len(outside)} text boxes outside page; examples: {outside[:5]}")
            for link in page.get_links():
                if link.get("kind") == fitz.LINK_GOTO and not 0 <= link.get("page", -1) < len(doc):
                    errors.append(f"Page {number}: invalid internal link destination")
            try:
                page.get_pixmap(matrix=fitz.Matrix(0.5, 0.5), alpha=False)
            except Exception as exc:
                errors.append(f"Page {number}: decoder render failed: {exc}")
            warnings = fitz.TOOLS.mupdf_warnings(reset=True)
            if warnings.strip():
                errors.append(f"Page {number}: PDF decoder diagnostics: {warnings.strip()}")
        if compare_interior:
            with fitz.open(compare_interior) as before:
                comparison = {"before": str(compare_interior.resolve()),
                              "sha256": fingerprint(compare_interior),
                              "changed_pages": [], "mode": "text only, excludes first and last page"}
                report["interior_comparison"] = comparison
                if before.needs_pass or not before.is_pdf:
                    raise ValueError("Interior comparison requires an unlocked PDF")
                if len(before) != len(doc):
                    errors.append(f"Cover-only comparison page count changed: {len(before)} -> {len(doc)}")
                elif len(doc) < 3:
                    errors.append("Cover-only comparison has no interior pages to verify")
                else:
                    comparison["changed_pages"] = [i + 1 for i in range(1, len(doc) - 1)
                        if before[i].get_text("text", clip=fitz.INFINITE_RECT()) != texts[i]]
                    if comparison["changed_pages"]:
                        errors.append(f"Interior text changed on pages: {comparison['changed_pages']}")
            warnings = fitz.TOOLS.mupdf_warnings(reset=True)
            if warnings.strip():
                errors.append(f"Comparison PDF decoder diagnostics: {warnings.strip()}")
    if log:
        report["build_log"] = {"path": str(log.resolve()), "sha256": fingerprint(log)}
        errors.extend(check_log(log))
    report["automated_checks_passed"] = not errors
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--log", type=Path, help="Verbose log from this build (identity verified manually)")
    parser.add_argument("--expected-chapters", type=int, help="Requires --chapter-pattern")
    parser.add_argument("--chapter-pattern", help="Regex matched at start of chapter bookmark titles")
    parser.add_argument("--compare-interior", type=Path, help="Prior PDF; excludes first/last page, text only")
    parser.add_argument("--tolerance", type=float, default=1.0, help="Bounds tolerance in points (default 1)")
    args = parser.parse_args()
    if args.expected_chapters is not None and (args.expected_chapters < 1 or not args.chapter_pattern):
        parser.error("--expected-chapters must be positive and requires --chapter-pattern")
    if not math.isfinite(args.tolerance) or args.tolerance < 0:
        parser.error("--tolerance must be finite and nonnegative")
    try:
        if args.chapter_pattern:
            re.compile(args.chapter_pattern)
        report = inspect_pdf(args.pdf, expected_chapters=args.expected_chapters,
                             chapter_pattern=args.chapter_pattern, log=args.log,
                             compare_interior=args.compare_interior, tolerance=args.tolerance)
    except (OSError, ValueError, RuntimeError, re.error) as exc:
        print(json.dumps({"pdf": str(args.pdf), "input_error": str(exc)}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return int(not report["automated_checks_passed"])


if __name__ == "__main__":
    sys.exit(main())
