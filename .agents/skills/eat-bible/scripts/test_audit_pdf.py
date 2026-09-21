#!/usr/bin/env python3
"""Synthetic regression tests; no book files are modified."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import fitz

from audit_pdf import check_log, inspect_pdf


class AuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def pdf(self, name="book.pdf", interior="Body", front="Front", outside=False,
            broken_resource=False, rotation=0, page_count=3):
        target = self.root / name
        with fitz.open() as doc:
            for text in [front, interior, "Back"][:page_count]:
                page = doc.new_page(width=300, height=400)
                page.insert_text((25, 50), text)
                if outside:
                    page.insert_text((-10, 90), "Outside page")
                page.set_rotation(rotation)
            if broken_resource:
                page = doc[0]
                xref = page.get_contents()[0]
                doc.update_stream(xref, doc.xref_stream(xref) + b"\n/NotDefined gs\n")
            if page_count >= 2:
                doc.set_toc([[1, "Chapter 1", 2]])
            doc.save(target)
        return target

    def test_clean(self):
        result = inspect_pdf(self.pdf(), expected_chapters=1, chapter_pattern=r"Chapter \d+")
        self.assertTrue(result["automated_checks_passed"], result)
        self.assertEqual(len(result["sha256"]), 64)

    def test_outside_content(self):
        result = inspect_pdf(self.pdf(outside=True))
        self.assertTrue(any("outside page" in item for item in result["errors"]))

    def test_missing_chapters(self):
        result = inspect_pdf(self.pdf(), expected_chapters=2, chapter_pattern=r"Chapter \d+")
        self.assertFalse(result["automated_checks_passed"])

    def test_bad_decoder_resource(self):
        result = inspect_pdf(self.pdf(broken_resource=True))
        self.assertTrue(any("decoder" in item for item in result["errors"]), result)

    def test_rotated_page(self):
        result = inspect_pdf(self.pdf(rotation=90))
        self.assertTrue(result["automated_checks_passed"], result)

    def test_cover_only(self):
        before = self.pdf("before.pdf")
        after = self.pdf("after.pdf", front="New cover")
        result = inspect_pdf(after, compare_interior=before)
        self.assertTrue(result["automated_checks_passed"], result)

    def test_changed_interior(self):
        before = self.pdf("before.pdf")
        after = self.pdf("after.pdf", interior="Changed body")
        result = inspect_pdf(after, compare_interior=before)
        self.assertEqual(result["interior_comparison"]["changed_pages"], [2])
        self.assertFalse(result["automated_checks_passed"])

    def test_changed_page_count(self):
        result = inspect_pdf(self.pdf(), compare_interior=self.pdf("short.pdf", page_count=2))
        self.assertTrue(any("page count" in item for item in result["errors"]))

    def test_no_interior(self):
        target = self.pdf(page_count=2)
        self.assertFalse(inspect_pdf(target, compare_interior=target)["automated_checks_passed"])

    def test_logs(self):
        target = self.root / "build.log"
        target.write_text("All checks passed\n", encoding="utf-8")
        self.assertEqual(len(check_log(target)), 2)
        target.write_text("This is XeTeX\nOutput written on book.pdf\n", encoding="utf-8")
        self.assertEqual(check_log(target), [])
        with target.open("a", encoding="utf-8") as stream:
            stream.write("Missing character: x\nOverfull \\vbox\n! Undefined control sequence\n")
        self.assertEqual(len(check_log(target)), 3)

    def test_cli_requires_bookmark_pattern(self):
        result = subprocess.run([sys.executable, str(Path(__file__).with_name("audit_pdf.py")),
                                 str(self.pdf()), "--expected-chapters", "1"], capture_output=True)
        self.assertEqual(result.returncode, 2)

    def test_cli_nonexistent_input(self):
        result = subprocess.run([sys.executable, str(Path(__file__).with_name("audit_pdf.py")),
                                 str(self.root / "missing.pdf")], capture_output=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"input_error", result.stdout)


if __name__ == "__main__":
    unittest.main()
