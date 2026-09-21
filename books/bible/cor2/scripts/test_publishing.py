import copy
import datetime
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from build_consolidated import ROOT, lessons, strip_frontmatter, scripture_index, assemble
from check_release import RIGHTS, REVIEWS, check_records

class SourceTests(unittest.TestCase):
    def test_all_lessons_exactly_once(self):
        text=assemble()
        for n in range(1,25): self.assertEqual(text.count(f'{{#lesson-{n:02d}}}'),1)
        for c in 'abcde': self.assertEqual(text.count(f'{{#appendix-{c}}}'),1)

    def test_missing_and_duplicate_lesson_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with self.assertRaises(ValueError): lessons(root)
            for n, file, _ in lessons(): (root/file.name).write_text(file.read_text())
            self.assertEqual(len(lessons(root)),24)
            (root/'01-duplicate.md').write_text((root/'01-comfort.md').read_text())
            with self.assertRaises(ValueError): lessons(root)

    def test_mismatched_lesson_metadata_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            (root/'01-test.md').write_text('---\nlesson: 02\n---\n# Wrong\n')
            with self.assertRaises(ValueError): lessons(root)

    def test_unclosed_header_fails(self):
        with self.assertRaises(ValueError): strip_frontmatter('---\ntitle: broken\n')
        self.assertEqual(strip_frontmatter('---\ntitle: x\n---\nBODY'),'BODY')

    def test_index_distinguishes_books_and_ignores_urls(self):
        result=scripture_index([(7,Path('07.md'),'創世記1:3；林後4:6；https://x.test/創99:1；約翰福音1:14')])
        self.assertIn('創世記 1章',result); self.assertIn('哥林多後書 4章',result)
        self.assertIn('約翰福音 1章',result); self.assertNotIn('99章',result)
        self.assertIn('[07](#lesson-07)',result)

class ReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.root=Path(self.temp.name)
        (self.root/'evidence.txt').write_text('Test fixture: not an actual editorial approval.')
        evidence_hash=hashlib.sha256((self.root/'evidence.txt').read_bytes()).hexdigest()
        fields=dict(reviewer='Test Reviewer',date=datetime.date.today().isoformat(),evidence='evidence.txt',evidence_sha256=evidence_hash)
        self.data={'edition':'CONSOLIDATED 2026 EDITION',
            'rights':[dict(id=i,status='CLEARED',**fields) for i in RIGHTS],
            'reviews':[dict(id=i,status='APPROVED',pdf_sha256='pdf',epub_sha256='epub',**fields) for i in REVIEWS]}
    def tearDown(self): self.temp.cleanup()
    def check(self,data): return check_records(data,self.root,'pdf','epub')
    def test_complete_evidence_fixture(self): self.assertEqual(self.check(self.data),[])
    def test_empty_inventory_rejected(self):
        self.data['rights']=[]; self.assertTrue(self.check(self.data))
    def test_deleted_or_duplicate_row_rejected(self):
        self.data['rights'][0]=self.data['rights'][1]; self.assertTrue(self.check(self.data))
    def test_pending_unknown_and_lowercase_status_rejected(self):
        for status in ['PENDING','cleared','APPROVED','']:
            self.data['rights'][0]['status']=status; self.assertTrue(self.check(self.data))
    def test_missing_evidence_rejected(self):
        (self.root/'evidence.txt').unlink(); self.assertTrue(self.check(self.data))
    def test_changed_evidence_rejected(self):
        (self.root/'evidence.txt').write_text('changed'); self.assertTrue(self.check(self.data))
    def test_stale_artifact_review_rejected(self):
        self.data['reviews'][0]['pdf_sha256']='old'; self.assertTrue(self.check(self.data))
    def test_incomplete_reviewer_and_future_date_rejected(self):
        self.data['reviews'][0]['reviewer']=''; self.data['reviews'][0]['date']='2999-01-01'
        self.assertTrue(self.check(self.data))

if __name__=='__main__': unittest.main()
