import unittest
import unicodedata
import fitz
from cover_design import covers


class CoverTests(unittest.TestCase):
    def test_identity_geometry_and_no_obsolete_text(self):
        with fitz.open() as doc:
            for _ in range(2):
                page = doc.new_page(width=504, height=720)
                page.insert_text((80,80), 'OBSOLETE COVER')
            covers(doc)
            for page in doc:
                text = page.get_text()
                self.assertIn('因信得生', text)
                self.assertIn('羅馬書研讀', text)
                self.assertNotIn('OBSOLETE', text)
                self.assertNotIn('\ufffd', text)
                for x0,y0,x1,y1,*_ in page.get_text('blocks'):
                    self.assertGreaterEqual(x0, 29)
                    self.assertLessEqual(x1, 475)
                    self.assertGreaterEqual(y0, 29)
                    self.assertLessEqual(y1, 691)
            self.assertIn('Justified to Live by Faith', unicodedata.normalize('NFKC', doc[0].get_text()))
            self.assertIn('非羅馬書原始課堂逐字稿', doc[1].get_text())

    def test_only_cover_pages_are_changed(self):
        with fitz.open() as doc:
            for _ in range(3):
                doc.new_page(width=504, height=720)
            doc[1].insert_text((70,70), 'INTERIOR PRESERVED')
            before = doc[1].get_pixmap().samples
            covers(doc)
            self.assertEqual(before, doc[1].get_pixmap().samples)
