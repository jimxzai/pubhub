"""Inventory explicitly quoted block paragraphs and verify archived source matches.

Coverage is deliberately limited to English block quotations beginning with a
quote mark. Inline quotes, translations and other languages need human review.
Whitespace alone is normalized; punctuation and case differences fail.
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def inventory(root=ROOT):
    manifest = json.loads((root / 'book.json').read_text())
    results = []
    for name in manifest['source_order']:
        text = (root / name).read_text()
        for match in re.finditer(r'^> ["“]([A-Za-z][^\n]+)', text, re.M):
            quote = match.group(1).rstrip().rstrip('"”')
            key = hashlib.sha256((name + '\n' + quote).encode()).hexdigest()[:20]
            results.append({'id': key, 'file': name, 'line': text[:match.start()].count('\n')+1, 'quote': quote})
    return results

def normalize(text):
    return ' '.join(text.split())

def verify(item, record, root=ROOT):
    if not record:
        return 'pending-source-record'
    required = ('author', 'work', 'edition', 'location', 'archive', 'sha256', 'reviewer', 'date')
    if any(not record.get(field) for field in required):
        return 'incomplete-source-record'
    path = (root / record['archive']).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        return 'missing-source-archive'
    data = path.read_bytes()
    if hashlib.sha256(data).hexdigest() != record['sha256']:
        return 'source-hash-mismatch'
    if normalize(item['quote']) not in normalize(data.decode('utf-8')):
        return 'quotation-mismatch'
    return 'text-match'

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--strict', action='store_true')
    args = parser.parse_args()
    records = json.loads((ROOT / 'sources/quotation-evidence.json').read_text())
    items = inventory()
    for item in items:
        item['status'] = verify(item, records.get(item['id']))
    directory = ROOT / 'build'
    directory.mkdir(exist_ok=True)
    (directory / 'quotation-audit.json').write_text(json.dumps(items, ensure_ascii=False, indent=2)+'\n')
    pending = sum(i['status'] != 'text-match' for i in items)
    print(f'Quotation candidates: {len(items)}; archived text matches: {len(items)-pending}; unresolved: {pending}')
    print('Scope: explicit English block quotes only; text match does not certify translation, context or permission.')
    return int(args.strict and (not items or pending > 0))

if __name__ == '__main__':
    raise SystemExit(main())
