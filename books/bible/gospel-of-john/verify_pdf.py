#!/usr/bin/env python3
"""Check the actual proof PDF, navigation, and final TeX pass."""
import re
import subprocess
import sys
from pathlib import Path
from pypdf import PdfReader

def verify(pdf, log):
    text = ' '.join(subprocess.check_output(['pdftotext', str(pdf), '-'], text=True).split())
    for expected in ('selected CUV 1919 and NASB 1995', 'Gospel of John Deep Study', 'Edition 4.0'):
        if expected not in text:
            raise ValueError(f'PDF missing required text: {expected}')
    if 'The Way of Life' in text or re.search(r'\b(?:RCUV|ESV)\b', text):
        raise ValueError('PDF contains stale title or translation')
    reader = PdfReader(pdf)
    if not reader.outline:
        raise ValueError('PDF has no bookmarks')
    links = sum(a.get_object().get('/Subtype') == '/Link' for p in reader.pages for a in p.get('/Annots', []))
    if not links:
        raise ValueError('PDF has no links')
    runs = re.split(r'^\[INFO\] \[makePDF\] LaTeX run number \d+.*$', Path(log).read_text(), flags=re.M)
    if len(runs) < 2 or not re.search(r'Output written on.*?\(\d+ pages?\)', runs[-1], re.S):
        raise ValueError('No completed final TeX pass')
    warnings = re.findall(r'^.*(?:Missing character|Overfull|Underfull|LaTeX (?:Font )?Warning|Package \S+ Warning|Rerun needed|Some font shapes).*$', runs[-1], re.M)
    if warnings:
        raise ValueError('\n'.join(warnings))
    print(f'Proof checks passed: {len(reader.pages)} pages, bookmarks present, {links} links, final TeX pass clean')

if __name__ == '__main__':
    try:
        verify(Path(sys.argv[1]), Path(sys.argv[2]))
    except (ValueError, OSError) as exc:
        sys.exit(str(exc))
