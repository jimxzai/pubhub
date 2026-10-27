import unittest
from pathlib import Path
import fitz
from editorial_upgrade import upgrade, unchanged_outside, CHAPTER_PAGES
from merge_baseline_pdf import replace, put
from audit_actual_pdf import fold, reference

class EditorialTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        baseline=Path(__file__).resolve().parents[1]/'sources/archive/romans-original-baseline.pdf'
        cls.original=fitz.open(baseline)
        cls.doc=fitz.open(baseline)
        cls.regions,cls.numbering=upgrade(cls.doc,replace,put)
    @classmethod
    def tearDownClass(cls):
        cls.original.close();cls.doc.close()
    def test_numbering_and_identity(self):
        # 2026-09-24: capped at chapters 1-11 (91, was 133 across 1-16) --
        # chapters 12-16 are now sourced from a fresh from-source render
        # (merge_baseline_pdf.py's splice) whose own build already prints
        # correct "Romans N" running heads, so this mislabel never occurs
        # there; see editorial_upgrade.py's numbering-repair loop.
        self.assertEqual(self.numbering,91)
        self.assertEqual(len(self.doc),348)
        for n,start in enumerate(CHAPTER_PAGES[:11],1):
            self.assertIn(fold(f'Romans {n}'),fold(self.doc[start-1].get_text()))
    def test_corrections_and_guides(self):
        # Pages 244/259's "13:14" correction moved out of editorial_upgrade.py
        # on 2026-09-24: those pages are now sourced from
        # 13-submission-to-authority.md, which already carries the corrected
        # wording (verified present before the PDF-patch code was removed).
        self.assertIn('不能只憑冠詞',self.doc[151].get_text())
        self.assertIn('讀經、辨別、回應',self.doc[5].get_text())
    def test_outside_all_edit_regions_preserved(self):
        for n,rects in self.regions.items():
            self.assertTrue(unchanged_outside(self.original[n-1],self.doc[n-1],rects),n)
    def test_mask_detects_unapproved_change(self):
        with fitz.open() as d:
            a=d.new_page(width=100,height=100)
            d.new_page(width=100,height=100)
            d[1].insert_text((20,70),'UNEXPECTED',fontsize=8)
            self.assertFalse(unchanged_outside(d[0],d[1],[fitz.Rect(0,0,10,10)]))
    def test_reference_identity_and_counts(self):
        for lang in ('zh','en'):
            self.assertEqual(sum(len(reference(ch,lang)) for ch in range(1,17)),433)
        self.assertEqual(fold('ﬁrst 裏'),fold('first 裡'))
        self.assertNotEqual(fold('word'),fold('words'))
