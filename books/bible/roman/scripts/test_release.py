import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from release_gate import valid_isbn, validate_release
from quote_audit import verify

class ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).resolve().parents[1]
        cls.manifest = json.loads((cls.root / 'book.json').read_text())

    def test_isbn_checksums(self):
        self.assertTrue(valid_isbn('978-0-306-40615-7'))
        self.assertTrue(valid_isbn('0-8044-2957-X'))
        self.assertFalse(valid_isbn('978-0-306-40615-8'))
        self.assertFalse(valid_isbn('123'))

    def test_review_accepts_assigned_isbn(self):
        self.assertEqual(validate_release({'isbn':'9780306406157', 'release_state':'review', 'release_status':'HOLD'}, Path('.')), [])

    def test_approval_requires_evidence(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root/'sources').mkdir()
            (root/'sources/release-approvals.json').write_text('{}')
            errors = validate_release({'release_state':'approved', 'release_status':'Approved'}, root)
            self.assertEqual(len(errors), 7)

    def test_quote_evidence_and_drift(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root/'source.txt'
            path.write_text('An exact quotation with context.')
            record = dict.fromkeys(('author','work','edition','location','reviewer','date'), 'fixture')
            record.update(archive='source.txt', sha256=hashlib.sha256(path.read_bytes()).hexdigest())
            self.assertEqual(verify({'quote':'An exact quotation'}, record, root), 'text-match')
            self.assertEqual(verify({'quote':'An altered quotation'}, record, root), 'quotation-mismatch')
            path.write_text('Changed source')
            self.assertEqual(verify({'quote':'An exact quotation'}, record, root), 'source-hash-mismatch')

    def test_source_order_and_required_sections(self):
        manifest = self.manifest
        self.assertEqual(len(manifest['source_order']), len(set(manifest['source_order'])))
        for name in ('01-gospel-and-condemnation.md', '16-greetings-conclusion.md'):
            text = (self.root / name).read_text()
            headings = [line[3:].split(' (', 1)[0].strip() for line in text.splitlines() if line.startswith('## ')]
            self.assertEqual(headings[:len(manifest['required_chapter_sections'])], manifest['required_chapter_sections'])

    def test_cover_audit_is_explicit(self):
        manifest = self.manifest
        self.assertEqual(manifest['cover']['visual_score_target'], 9.7)
        self.assertIn('Edition 1.1', (self.root / 'COVER-AUDIT.md').read_text())

if __name__ == '__main__':
    unittest.main()
