#!/usr/bin/env python3
"""Read-only checks for the assigned Matthew PDF; requires PyMuPDF."""
import argparse
import json
import re
from pathlib import Path

import fitz

parser = argparse.ArgumentParser()
parser.add_argument("pdf", type=Path)
parser.add_argument("--log", type=Path)
args = parser.parse_args()
errors = []
with fitz.open(args.pdf) as doc:
    bookmarks = doc.get_toc()
    chapter_titles = [row[1] for row in bookmarks if re.match(r"(?:\d+\s+)?第[一二三四五六七八九十]+章", row[1])]
    if len(chapter_titles) != 28 or len(set(chapter_titles)) != 28:
        errors.append(f"Expected 28 distinct chapter bookmarks; found {len(chapter_titles)}")
    blank_pages = []
    for number, page in enumerate(doc, 1):
        if not page.get_text().strip():
            blank_pages.append(number)
        for x0, y0, x1, y1, word, *_ in page.get_text("words"):
            if x0 < -1 or y0 < -1 or x1 > page.rect.width + 1 or y1 > page.rect.height + 1:
                errors.append(f"Page {number}: text outside page: {word}")
        for link in page.get_links():
            if link.get("kind") == fitz.LINK_GOTO and not 0 <= link.get("page", -1) < len(doc):
                errors.append(f"Page {number}: invalid internal link")
    if args.log:
        log = args.log.read_text()
        if "Output written on" not in log:
            errors.append("Build log has no completed TeX output")
        for pattern in (r"Missing character", r"Overfull \\hbox", r"^! ", r"Error producing PDF"):
            if re.search(pattern, log, re.MULTILINE):
                errors.append(f"Build log defect: {pattern}")
    print(json.dumps({"pdf": str(args.pdf), "pages": len(doc),
                      "chapter_bookmarks": len(chapter_titles),
                      "blank_pages_for_visual_review": blank_pages,
                      "errors": errors}, ensure_ascii=False, indent=2))
raise SystemExit(bool(errors))
