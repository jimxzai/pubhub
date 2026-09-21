#!/usr/bin/env python3
"""Attach a human/agent's explicit rendered-page review and external Ace result.

This command does not perform visual review. The supplied PDF hash and physical
page numbers identify the rendering that the reviewer actually inspected.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
from datetime import datetime, timezone

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--qa', type=Path, required=True)
    parser.add_argument('--ace-report', type=Path, required=True)
    parser.add_argument('--reviewed-pdf-sha256', required=True)
    parser.add_argument('--pages', required=True)
    args = parser.parse_args()
    qa = json.loads(args.qa.read_text())
    folder = args.qa.parent
    for name, expected in qa['sha256'].items():
        if hashlib.sha256((folder / name).read_bytes()).hexdigest() != expected:
            raise ValueError('Artifact changed since build: ' + name)
    pdf_hash = qa['sha256']['gospel-of-mark-consolidated.pdf']
    if pdf_hash != args.reviewed_pdf_sha256:
        raise ValueError('The reviewed PDF is not this build')
    ace = json.loads(args.ace_report.read_text())
    if ace.get('earl:result', {}).get('earl:outcome') != 'pass':
        raise ValueError('Ace did not report a pass; retain the findings, do not clear the gate')
    pages = [int(p) for p in args.pages.split(',')]
    if not pages or any(p < 1 or p > qa['pdf_pages'] for p in pages):
        raise ValueError('Invalid physical page list')
    report_name = 'gospel-of-mark-consolidated-ace.json'
    shutil.copy2(args.ace_report, folder / report_name)
    qa['ace'] = {'status': 'PASS: zero automated findings', 'report': report_name,
                 'epub_sha256': qa['sha256']['gospel-of-mark-consolidated-accessible.epub']}
    qa['visual_review'] = {'status': 'PASS, representative pages only', 'physical_pages': pages,
                           'pdf_sha256': pdf_hash, 'date_utc': datetime.now(timezone.utc).isoformat()}
    stage = args.qa.with_suffix('.review.tmp')
    stage.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + '\n')
    stage.replace(args.qa)
    print('Review evidence recorded; rights, independent proofreading and manual accessibility holds remain.')

if __name__ == '__main__': main()
