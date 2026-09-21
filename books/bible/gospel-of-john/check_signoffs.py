#!/usr/bin/env python3
"""Require documentary evidence for every publication gate."""
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent

def main():
    manifest = json.loads((ROOT / 'publication-manifest.json').read_text())
    records = json.loads((ROOT / 'editorial-signoffs.json').read_text())
    errors = []
    for gate in manifest['release_gates']:
        record = records.get(gate, {})
        evidence = record.get('evidence', '')
        if not (record.get('status') == 'approved' and record.get('reviewer') and record.get('date')
                and evidence and (ROOT / evidence).is_file()):
            errors.append(gate)
    if errors:
        print('Publication blocked; missing documented approvals:\n' + '\n'.join(errors))
        return 1
    print('Documented approvals present; retained evidence requires editorial review.')
    return 0

if __name__ == '__main__':
    sys.exit(main())
