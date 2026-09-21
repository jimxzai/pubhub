"""Source and rights checks for the assigned consolidated edition."""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIELDS = ['asset', 'locations', 'status', 'action before release', 'owner']
ASSETS = {'NASB 1995 Scripture excerpts', 'Chinese Union Version 1919',
    'John MacArthur / Grace to You verbatim quotations',
    'G. Campbell Morgan, The Gospel According to Luke (1931)',
    'Patristic and Reformation summaries', 'Hymn lyrics and translations',
    'CCIC / “老弟兄” material', 'External Bible-reference links'}

def body(path):
    lines = Path(path).read_text(encoding='utf-8').splitlines(keepends=True)
    if not lines or lines[0].strip() != '---':
        raise ValueError(f'{path}: missing opening YAML delimiter')
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == '---'), None)
    if end is None:
        raise ValueError(f'{path}: unclosed YAML metadata')
    result = ''.join(lines[end + 1:])
    if len(re.findall(r'^# ', result, re.M)) != 1:
        raise ValueError(f'{path}: expected exactly one chapter title')
    return result

def rights(path, release=False):
    with Path(path).open(encoding='utf-8', newline='') as f:
        reader = csv.DictReader(f, delimiter='\t')
        if reader.fieldnames not in (FIELDS, FIELDS + ['evidence']):
            raise ValueError('Invalid rights ledger columns')
        rows = list(reader)
    if len(rows) != len(ASSETS) or {r['asset'] for r in rows} != ASSETS:
        raise ValueError('Missing, duplicate or unexpected rights ledger assets')
    for row in rows:
        if None in row or any(not row.get(k, '').strip() for k in FIELDS):
            raise ValueError('Incomplete rights ledger row')
        if row['status'] not in {'HOLD', 'REVIEW', 'CLEARED'}:
            raise ValueError(f"Invalid rights status: {row['status']}")
        if row['status'] == 'CLEARED':
            evidence = (Path(path).parent / row.get('evidence', '')).resolve()
            if not evidence.is_file() or evidence.stat().st_size == 0:
                raise ValueError(f"Missing approval evidence: {row['asset']}")
        elif release:
            raise ValueError(f"Release blocked: {row['asset']} is {row['status']}")

def sources(root=ROOT):
    files = [root / n for n in ['000-preface.md', '00-overview.md',
        '00a-son-of-man-position.md', '00b-systematic-reception.md',
        '00c-set-face-spine.md', '99-toward-the-nations.md',
        '99-appendix-references.md', '999-afterword.md']]
    for n in range(1, 25):
        matches = list(root.glob(f'{n:02d}-*.md'))
        if len(matches) != 1:
            raise ValueError(f'Chapter {n}: expected one source; found {len(matches)}')
        chapter = body(matches[0])
        if len(re.findall(r'^## ', chapter, re.M)) != 11:
            raise ValueError(f'Chapter {n}: expected 11 sections')
        files += matches
    for path in files:
        body(path)
    return files

if __name__ == '__main__':
    try:
        if len(sys.argv) > 1 and sys.argv[1] == 'body':
            print(body(sys.argv[2]), end='')
        else:
            mode = sys.argv[1] if len(sys.argv) > 1 else 'proof'
            if mode not in {'proof', 'release'}:
                raise ValueError('Mode must be proof or release')
            sources()
            rights(ROOT / 'rights-ledger.tsv', mode == 'release')
            print(f'Source and rights checks passed ({mode}).')
    except (ValueError, OSError, KeyError, csv.Error) as exc:
        sys.exit(str(exc))
