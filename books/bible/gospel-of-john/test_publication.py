"""Regression checks for false passes in the publisher validator."""
import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
import validate_publication as validator

class PublicationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(validator.MANIFEST.read_text())
        cls.sources = {name: (validator.ROOT / name).read_text() for name in cls.manifest['required_source_files'] + ['README.md', 'RED-LETTER-GUIDE.md']}

    def run_case(self, edit=None):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = copy.deepcopy(self.manifest)
            sources = self.sources.copy()
            if edit:
                edit(manifest, sources)
            for name, text in sources.items():
                (root / name).write_text(text)
            (root / 'publication-manifest.json').write_text(json.dumps(manifest))
            old_root, old_manifest = validator.ROOT, validator.MANIFEST
            try:
                validator.ROOT, validator.MANIFEST = root, root / 'publication-manifest.json'
                with contextlib.redirect_stdout(io.StringIO()):
                    return validator.main()
            finally:
                validator.ROOT, validator.MANIFEST = old_root, old_manifest

    def test_valid_sources(self):
        self.assertEqual(self.run_case(), 0)

    def test_translation_drift(self):
        self.assertEqual(self.run_case(lambda m, s: m['translation_policy'].update(english='NASB 2020')), 1)

    def test_nonstudy_title_suffix(self):
        def edit(m, s):
            s['000-preface.md'] = s['000-preface.md'].replace('subtitle: Gospel of John Deep Study', 'subtitle: Gospel of John Deep Study Other')
        self.assertEqual(self.run_case(edit), 1)

    def test_missing_source(self):
        self.assertEqual(self.run_case(lambda m, s: s.pop('02-cana-wedding.md')), 1)

    def test_duplicate_source(self):
        self.assertEqual(self.run_case(lambda m, s: m['required_source_files'].append('000-preface.md')), 1)

    def test_section_order(self):
        def edit(m, s):
            s['02-cana-wedding.md'] = s['02-cana-wedding.md'].replace('## 背景 (Context)', '## 生命應用 (Application)', 1)
        self.assertEqual(self.run_case(edit), 1)

if __name__ == '__main__':
    unittest.main()
