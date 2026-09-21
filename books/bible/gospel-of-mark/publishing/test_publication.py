import tempfile
from pathlib import Path
import unittest
from collections import Counter
from unittest.mock import patch
from epub import convert, build
from publication import check_log, index_template

class PublicationTests(unittest.TestCase):
    def test_nested_red_letter_and_verse(self):
        counts = Counter()
        result = convert(r'\jesus{Words \textbf{nested} \textsuperscript{15}}', counts)
        self.assertEqual(result, '<span class="jesus">Words <strong>nested</strong> <sup>15</sup></span>')
        self.assertEqual(counts['jesus'], 1)

    def test_unknown_and_unbalanced_fail(self):
        for text in (r'\unknown{do not lose}', r'\jesus{unfinished'):
            with self.assertRaises(ValueError): convert(text)

    def test_fatal_and_missing_glyph_logs_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'log'
            for error in ('  ! Undefined control sequence.', 'Missing character: x', 'Overfull \\hbox (2pt)', 'LaTeX Warning: There were undefined references.'):
                path.write_text('Output written on test.pdf\n' + error)
                with self.assertRaises(ValueError): check_log(path)
            path.write_text('Output written on test.pdf\n')
            check_log(path)

    def test_failed_epub_keeps_previous_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            md, template, output = [root / p for p in ('input.md', 'template.tex', 'book.epub')]
            md.write_text(r'\unknown{lost text}')
            template.write_text('unused')
            output.write_bytes(b'LAST VERIFIED EDITION')
            with self.assertRaises(ValueError): build(md, template, output)
            self.assertEqual(output.read_bytes(), b'LAST VERIFIED EDITION')

    def test_index_is_generated_from_page_labels_not_old_numbers(self):
        template = 'Bartimaeus 巴底買 & 999 \\\\\n\\bottomrule'
        pages = 'header\n\n巴底買\n\nfooter\fheader\n\n巴底買\n\nfooter\fheader\n\nother\n\nfooter\f'
        with patch('publication.PdfReader') as reader, patch('publication.subprocess.run') as run:
            reader.return_value.page_labels = ['1', '2', '3']
            run.return_value.stdout = pages
            result = index_template(template, Path('unused.pdf'))
            self.assertIn('1–2', result)
            self.assertNotIn('999', result)

    def test_missing_index_term_blocks_build(self):
        with patch('publication.PdfReader') as reader, patch('publication.subprocess.run') as run:
            reader.return_value.page_labels = ['1']
            run.return_value.stdout = 'header\n\nother\n\nfooter\f'
            with self.assertRaises(ValueError):
                index_template('Bartimaeus 巴底買 & 999 \\\\\n\\bottomrule', Path('unused.pdf'))

if __name__ == '__main__': unittest.main()
