#!/usr/bin/env python3
"""Generate the build template and passage inventory from current sources."""
import argparse
import contextlib
import importlib.util
import io
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]


def generate(output):
    manifest = json.loads((ROOT / 'publication-manifest.json').read_text())
    spec = importlib.util.spec_from_file_location('john_index', REPO / 'scripts/gen-john-scripture-index.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert [name for name, _ in module.SOURCES] == manifest['required_source_files'], 'index/build source order differs'
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        module.main()
    template = (REPO / 'templates/pdf/gospel-of-john.latex').read_text()
    start = template.index('\\section*{舊約 Old Testament}', template.index('%% APPENDIX A:'))
    end = template.index('\\noindent 以下一表為編者所選', start)
    template = template[:start] + buffer.getvalue() + '\n\\pagebreak\n\n' + template[end:]
    rows = []
    for name in manifest['required_source_files']:
        text = (ROOT / name).read_text()
        scripture = re.search(r'^## 經文[^\n]*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
        if not scripture:
            continue
        verses = {'CUV 1919': [], 'NASB 1995': []}
        language = None
        for line in scripture[1].splitlines():
            if re.match(r'^#{3,4} 中文', line):
                language = 'CUV 1919'
            elif re.match(r'^#{3,4} English', line):
                language = 'NASB 1995'
            elif line.startswith('#'):
                language = None
            elif language:
                verses[language].extend(re.findall(r'\^(\d+(?::\d+)?)\^', line))
        rows.append({'source': name, 'verse_markers': verses,
                     'matching_markers': verses['CUV 1919'] == verses['NASB 1995'],
                     'text_verified': False})
    output.mkdir(parents=True, exist_ok=True)
    (output / 'gospel-of-john-generated.latex').write_text(template)
    (output / 'gospel-of-john-passage-inventory.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
    report = ['# Scripture passage inventory', '', 'CUV 1919 + NASB 1995. Numbers below are printed verse markers within each study unit. They do not certify complete verse text or quotation accuracy.', '', '| Study unit | CUV markers | NASB markers | Same markers |', '|---|---|---|---|']
    for row in rows:
        marks = row['verse_markers']
        report.append('| ' + row['source'] + ' | ' + ', '.join(marks['CUV 1919']) + ' | ' + ', '.join(marks['NASB 1995']) + ' | ' + ('Yes' if row['matching_markers'] else 'No') + ' |')
    (output / 'gospel-of-john-passage-inventory.md').write_text('\n'.join(report) + '\n')
    print(f'Generated current Scripture index and passage inventory for {len(rows)} study units')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    generate(parser.parse_args().output)
