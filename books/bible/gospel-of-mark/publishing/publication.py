#!/usr/bin/env python3
"""Staged Mark-only build. No final output is touched before validation."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from datetime import datetime, timezone
from pypdf import PdfReader
from epub import build as build_epub

BOOK = Path(__file__).resolve().parents[1]
ROOT = BOOK.parents[2]
STEM = 'gospel-of-mark-consolidated'

def check_log(path):
    text = path.read_text(errors='replace')
    failures = re.findall(r'(?m)^\s*!.*|Missing character:.*|Overfull \\[hv]box.*|.*Undefined control sequence.*|.*undefined references.*', text)
    if failures: raise ValueError('TeX preflight failed: ' + '\n'.join(failures[:20]))
    if 'Output written on' not in text: raise ValueError('Missing successful XeTeX log')

def index_template(template, pdf):
    reader = PdfReader(pdf)
    text = subprocess.run(['pdftotext', '-layout', str(pdf), '-'], capture_output=True, text=True, check=True).stdout.split('\f')
    pages = []
    for label, page in zip(reader.page_labels, text):
        if '附錄十二：字母索引' in page and label.isdigit(): break
        lines = page.splitlines()
        # Running headers and standalone page numbers are not index hits.
        body = re.sub(r'\s+', '', '\n'.join(lines[2:-2]))
        if label.isdigit(): pages.append((label, body))
    aliases = {'雅各與約翰': ['雅各', '約翰'], '猶大': ['猶大'], '彌賽亞秘密': ['彌賽亞秘密', '彌賽亞隱秘'],
               '三次預言受難': ['三次預言', '三次受難預言'], '幔子裂開': ['幔子', '裂開']}
    start = template.index('Bartimaeus 巴底買 &')
    end = template.index('\\bottomrule', start)
    rows = []
    for line in template[start:end].splitlines():
        entry = line.split(' & ')[0]
        term = re.search(r'[\u3400-\u9fff][\u3400-\u9fff／與]*', entry)[0]
        terms = aliases.get(term, [term])
        match = any if term in ('彌賽亞秘密', '三次預言受難') else all
        hits = [label for label, body in pages if match(t in body for t in terms)]
        if not hits: raise ValueError('Index has no matches: ' + entry)
        # Compact consecutive pages; all references are generated, not hand copied.
        ranges = []
        numbers = [int(h) for h in hits]
        a = b = numbers[0]
        for number in numbers[1:] + [None]:
            if number is not None and number == b + 1: b = number; continue
            ranges.append(str(a) if a == b else f'{a}–{b}')
            a = b = number
        rows.append(entry + ' & ' + ', '.join(ranges) + r' \\')
    return template[:start] + '\n'.join(rows) + '\n' + template[end:]

def main(output):
    output.mkdir(parents=True, exist_ok=True)
    with (BOOK / 'publishing/.build.lock').open('w') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        # Validate YAML boundary before the historical seven-line assembler.
        sources = list(BOOK.glob('*.md'))
        manuscript = [p for p in sources if re.match(r'^\d', p.name)]
        if len(manuscript) != 29: raise ValueError('Expected 29 source files')
        for path in manuscript:
            print('Checking source:', path.name, flush=True)
            lines = subprocess.run(['sed', '-n', '1,7p', str(path)], capture_output=True, text=True, check=True).stdout.splitlines()
            if lines[0] != '---' or lines[6] != '---': raise ValueError('Unexpected front matter: ' + str(path))
        with tempfile.TemporaryDirectory(prefix='.mark-build-', dir=output) as directory:
            stage = Path(directory)
            template = stage / 'gospel-of-mark.latex'
            shutil.copy2(ROOT / 'templates/pdf/gospel-of-mark.latex', template)
            env = dict(os.environ, MARK_STAGE_DIR=str(stage), MARK_TEMPLATE=str(template))
            pdf = stage / (STEM + '.pdf')
            for iteration in range(3):
                print(f'PDF build pass {iteration + 1}', flush=True)
                result = subprocess.run(['bash', str(BOOK / 'publishing/assemble.sh')], env=env)
                if result.returncode:
                    log = stage / (STEM + '-build.log')
                    if log.exists():
                        failed = Path(tempfile.mkdtemp(prefix='mark-failed-build-'))
                        shutil.copy2(log, failed / log.name)
                        print(log.read_text(errors='replace')[-6000:], flush=True)
                        print('Failure log:', failed, flush=True)
                    raise RuntimeError(f'PDF build failed: {result.returncode}')
                check_log(stage / (STEM + '-build.log'))
                before = template.read_text()
                after = index_template(before, pdf)
                if after == before: break
                template.write_text(after)
            else: raise ValueError('Index pagination did not stabilize')
            reader = PdfReader(pdf)
            if reader.trailer['/Root'].get('/Lang') != 'zh-TW': raise ValueError('Missing PDF language')
            if not reader.outline: raise ValueError('Missing bookmarks')
            subprocess.run(['pdftoppm', '-f', '1', '-l', '1', '-singlefile', '-scale-to', '1600',
                            '-png', str(pdf), str(stage / 'cover')], check=True)
            report = build_epub(stage / (STEM + '.md'), template, stage / (STEM + '-accessible.epub'), stage / 'cover.png')
            jar = Path(os.environ.get('EPUBCHECK_JAR', '/tmp/mark-epubcheck-tools/epubcheck-5.3.0/epubcheck.jar'))
            if not jar.is_file():
                raise RuntimeError('EPUBCheck is required before promotion. Set EPUBCHECK_JAR to the official epubcheck.jar.')
            java = '/opt/homebrew/opt/openjdk/bin/java'
            if not Path(java).exists(): java = 'java'
            epubcheck_report = stage / (STEM + '-epubcheck.json')
            subprocess.run([java, '-jar', str(jar), str(stage / (STEM + '-accessible.epub')),
                            '--json', str(epubcheck_report)], check=True)
            messages = json.loads(epubcheck_report.read_text()).get('messages', [])
            if any(m.get('severity') in ('WARNING', 'ERROR', 'FATAL') for m in messages):
                raise ValueError('EPUBCheck warnings/errors block promotion')
            report['epubcheck'] = 'PASS: zero errors/warnings'
            report.update({'date_utc': datetime.now(timezone.utc).isoformat(), 'pdf_pages': len(reader.pages),
                           'pdf_language': 'zh-TW', 'pdf_preflight': 'PASS', 'index': 'generated and stable',
                           'rights': 'HOLD', 'independent_scripture_proofreading': 'HOLD',
                           'pdf_tagging': 'NOT TAGGED', 'visual_review': 'PENDING'})
            def count_outline(items):
                return sum(count_outline(item) if isinstance(item, list) else 1 for item in items)
            report['pdf_bookmarks_recursive'] = count_outline(reader.outline)
            finals = [stage / (STEM + suffix) for suffix in ('.pdf', '.md', '-build.log', '-accessible.epub')]
            report['sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in finals}
            qa = stage / (STEM + '-qa.json')
            qa.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
            finals.extend([qa, epubcheck_report])
            # Recoverable backup outside distributable output directory.
            backup = Path(tempfile.mkdtemp(prefix='mark-previous-'))
            replaced = []
            try:
                for path in finals:
                    target = output / path.name
                    if target.exists(): shutil.copy2(target, backup / path.name)
                    os.replace(path, target); replaced.append(target)
                stale_ace = output / (STEM + '-ace.json')
                if stale_ace.exists(): shutil.move(stale_ace, backup / stale_ace.name)
            except BaseException:
                for target in replaced:
                    old = backup / target.name
                    if old.exists(): shutil.copy2(old, target)
                    else: target.unlink()
                raise
            print('Verified outputs:', output, '\nPrevious outputs preserved:', backup)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'output')
    main(parser.parse_args().output_dir)
