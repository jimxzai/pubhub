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
        self.assertEqual(self.numbering,133)
        self.assertEqual(len(self.doc),348)
        for n,start in enumerate(CHAPTER_PAGES,1):
            self.assertIn(fold(f'Romans {n}'),fold(self.doc[start-1].get_text()))
    def test_corrections_and_guides(self):
        for n in (244,259):
            self.assertNotIn('沒有直接提耶穌',self.doc[n-1].get_text())
            self.assertIn('13:14',self.doc[n-1].get_text())
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
