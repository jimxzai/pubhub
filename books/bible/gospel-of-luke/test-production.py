"""Regression checks for silent data loss and invalid release approvals."""
import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('production', Path(__file__).with_name('production-check.py'))
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)

class ProductionTests(unittest.TestCase):
    def test_variable_metadata_and_missing_delimiter(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / 'chapter.md'
            f.write_text('---\ntitle: test\n---\n# Chapter\nBody\n')
            self.assertEqual(p.body(f), '# Chapter\nBody\n')
            f.write_text('---\ntitle: test\n# Chapter\n')
            with self.assertRaises(ValueError): p.body(f)

    def test_missing_chapter(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError): p.sources(Path(d))

    def test_rights_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            f = Path(d) / 'ledger.tsv'
            for status in ['REVEIW', 'CLEARED', 'HOLD', 'REVIEW']:
                with f.open('w') as out:
                    writer = csv.writer(out, delimiter='\t')
                    writer.writerow(p.FIELDS)
                    for asset in p.ASSETS:
                        writer.writerow([asset, 'chapter', status, 'verify', 'publisher'])
                with self.assertRaises(ValueError): p.rights(f, True)
            f.write_text('\t'.join(p.FIELDS) + '\n')
            with self.assertRaises(ValueError): p.rights(f)
            f.unlink()
            with self.assertRaises(OSError): p.rights(f)

    def test_real_sources_and_proof_rights(self):
        self.assertEqual(len(p.sources()), 32)
        p.rights(p.ROOT / 'rights-ledger.tsv')

if __name__ == '__main__': unittest.main()
