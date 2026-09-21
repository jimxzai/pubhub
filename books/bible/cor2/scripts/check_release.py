#!/usr/bin/env python3
"""Fail closed on missing records, unsupported status or missing review evidence."""
import datetime
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent.parent
RIGHTS={*(f'source-{i}' for i in range(1,9)), *(f'hymn-{i:02d}' for i in range(1,25))}
REVIEWS={'chinese-scripture','english-scripture','greek','theology','copyedit','appendices','visual-proof','accessibility','rights-review'}

def check_records(data, root, pdf_hash, epub_hash):
    errors=[]
    if data.get('edition') != 'CONSOLIDATED 2026 EDITION': errors.append('Wrong edition')
    for kind, required in [('rights',RIGHTS),('reviews',REVIEWS)]:
        records=data.get(kind)
        if not isinstance(records,list):
            errors.append(f'{kind}: missing record list'); continue
        ids=[r.get('id') for r in records if isinstance(r,dict)]
        if len(ids)!=len(records) or len(ids)!=len(set(ids)) or set(ids)!=required:
            errors.append(f'{kind}: exact required inventory missing, duplicated or changed')
        for r in records:
            if not isinstance(r,dict): continue
            label=r.get('id','unknown')
            allowed={'CLEARED','PUBLIC-DOMAIN','REMOVED'} if kind=='rights' else {'APPROVED'}
            if r.get('status') not in allowed: errors.append(f'{label}: unresolved/unknown status')
            if not isinstance(r.get('reviewer'),str) or len(r['reviewer'].strip())<2:
                errors.append(f'{label}: reviewer missing')
            try:
                date=datetime.date.fromisoformat(r.get('date',''))
                if date>datetime.date.today(): raise ValueError()
            except (ValueError,TypeError): errors.append(f'{label}: invalid review date')
            try:
                path=(root/r['evidence']).resolve()
                if not r['evidence'] or not path.is_relative_to(root.resolve()) or not path.is_file() or path.stat().st_size==0:
                    raise ValueError()
                if hashlib.sha256(path.read_bytes()).hexdigest()!=r.get('evidence_sha256'): raise ValueError()
            except (ValueError,KeyError,TypeError,OSError): errors.append(f'{label}: absent/changed evidence')
            if kind=='reviews' and (r.get('pdf_sha256')!=pdf_hash or r.get('epub_sha256')!=epub_hash):
                errors.append(f'{label}: review does not match current PDF/EPUB')
    return errors

def main():
    try:
        data=json.loads((ROOT/'release-approvals.json').read_text())
        out=ROOT.parents[2]/'output'
        hashes=[hashlib.sha256((out/f'cor2-consolidated.{ext}').read_bytes()).hexdigest() for ext in ['pdf','epub']]
        errors=check_records(data,ROOT,*hashes)
        report=json.loads((out/'cor2-consolidated-qa.json').read_text())
        if not report.get('tagged'): errors.append('PDF tagging/accessibility remains open')
        for ext, digest in zip(['pdf','epub'],hashes):
            if report.get('artifacts',{}).get(f'cor2-consolidated.{ext}') != digest:
                errors.append(f'{ext}: QA report does not match artifact')
        if report.get('epubcheck')!='passed': errors.append('EPUBCheck approval absent')
    except (ValueError,OSError,KeyError) as exc:
        errors=[f'Missing/invalid release evidence: {exc}']
    if errors:
        print('BLOCKED: formal release has unresolved requirements.\n'+'\n'.join(errors[:16]))
        print(f'{len(errors)} unresolved checks. No approval inferred from checkboxes.')
        sys.exit(1)
    print('PASS: complete rights inventory, dated evidence, reviews and current artifact hashes.')

if __name__=='__main__': main()
