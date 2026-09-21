#!/usr/bin/env python3
"""Build a single semantic source into validated, consistently named artifacts."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parents[2]
NAME = 'cor2-consolidated'

def run(args, **kwargs):
    return subprocess.run([str(x) for x in args], check=True, text=True, **kwargs)

def source_hashes():
    paths = list(ROOT.glob('*.md')) + list((ROOT/'appendices').glob('*.md'))
    paths += [ROOT/'publication.yaml',ROOT/'volumes.json',ROOT/'templates/book.css',
              ROOT/'scripts/normalize.lua',ROOT/'scripts/pdf-style.lua',
              REPO/'templates/pdf/cor2.latex']
    return {str(p.relative_to(REPO)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}

def strip_frontmatter(text):
    if text.startswith('---\n'):
        match = re.match(r'\A---\n.*?\n---\n', text, re.S)
        if not match:
            raise ValueError('Unclosed YAML frontmatter')
        return text[match.end():]
    return text

def lessons(root=ROOT):
    found = []
    for n in range(1, 25):
        matches = list(root.glob(f'{n:02d}-*.md'))
        if len(matches) != 1:
            raise ValueError(f'Lesson {n:02d}: expected exactly one file, got {len(matches)}')
        text = matches[0].read_text()
        header = re.match(r'\A---\n(.*?)\n---\n', text, re.S)
        if not header or not re.search(rf'^lesson:\s*0?{n}\s*$', header[1], re.M):
            raise ValueError(f'Wrong lesson metadata: {matches[0]}')
        body = strip_frontmatter(text)
        if len(re.findall(r'^# ', body, re.M)) != 1:
            raise ValueError(f'Expected one lesson title: {matches[0]}')
        found.append((n, matches[0], body))
    return found

def scripture_index(items):
    spec = importlib.util.spec_from_file_location('index_library', REPO/'scripts/gen-john-scripture-index.py')
    lib = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(lib)
    # The John generator omits its own book; add it explicitly for this volume.
    aliases = {**lib.ALIAS, '約': '約翰福音', '約翰福音': '約翰福音'}
    names = '|'.join(re.escape(x) for x in sorted(aliases, key=len, reverse=True))
    pattern = re.compile(rf'(?<![A-Za-z0-9])({names})\s*(\d+)(?::(\d+(?:[-–]\d+)?))?')
    refs = {}
    for n, _, body in items:
        # Exclude URLs, dates and raw code; index explicit book names only.
        body = re.sub(r'https?://[^\s)；，。]+', '', body)
        body = re.sub(r'```.*?```', '', body, flags=re.S)
        for m in pattern.finditer(body):
            alias, ch, vs = m.groups()
            if len(alias) == 1 and m.start() and '\u4e00' <= body[m.start()-1] <= '\u9fff':
                continue
            book = aliases[alias]
            if not 1 <= int(ch) <= lib.MAXCHAP.get(book, 21):
                continue
            refs.setdefault((book, int(ch)), {}).setdefault(n, set()).add(vs or '全章')
    lines = ['# Appendix A: Scripture Index 經文索引 {#appendix-a}', '',
        '本索引依24課正文中明寫卷名的經文自動生成，按卷、章與課次排列。課次可點選返回正文。未寫卷名、跨章延伸及省略寫法不自動推定，故非窮盡式索引。', '',
        '下表「經文出處」屬所列經卷；「出現課次」屬本書24課，並非聖經章號。', '',
        '| 經文出處 | 節號（依正文） | 出現課次 |', '|---|---|---|']
    order = {**lib.ORDER, '約翰福音': lib.ORDER['路加福音'] + .5}
    for (book, ch), by_lesson in sorted(refs.items(), key=lambda r: (order[r[0][0]], r[0][1])):
        verses = sorted(set().union(*by_lesson.values()), key=lambda v: (v == '全章', int(re.match(r'\d+', v)[0]) if v != '全章' else 0, v))
        links = '、 '.join(f'[{n:02d}](#lesson-{n:02d})' for n in sorted(by_lesson))
        lines.append(f'| {book} {ch}章 | {"、 ".join(verses)} | {links} |')
    if not refs:
        raise ValueError('Empty scripture index')
    return '\n'.join(lines)+'\n'

def assemble():
    items = lessons()
    volumes = json.loads((ROOT/'volumes.json').read_text())
    if len(volumes) != 7:
        raise ValueError('Expected seven volume dividers')
    parts = ['---\n'+(ROOT/'publication.yaml').read_text()+'\n---\n']
    def add_file(name):
        body = strip_frontmatter((ROOT/name).read_text())
        parts.append(body+'\n\n\\newpage\n')
    def divider(i):
        v = volumes[i]
        parts.append(f'# {v["title"]}\n\n> {v["description"]}\n\n\\newpage\n')
    add_file('000-preface.md')
    parts.append('# 版本與閱讀說明 {#edition}\n\nCONSOLIDATED 2026 EDITION\n\n'
                 '哥林多後書研讀：十字架事奉\n\n版權與來源核查中；完成審核前不得公開或商業發行。\n\n'
                 '本書按五卷、24課編排。目錄列出卷、課與附錄；電子書籤保留小節。附錄經文索引的課次連結可直接返回相關課文。\n\n\\newpage\n')
    divider(0)
    for name in ('00-overview.md','00a-cor2-position.md','00b-weakness-spine.md'):
        add_file(name)
    body = strip_frontmatter((ROOT/'elder-wong-systematic-study.md').read_text())
    parts.append('# 全書領受總綱——查經領受 (Systematic Reception)\n\n'+re.sub(r'^#', '##', body, flags=re.M)+'\n\n\\newpage\n')
    starts = {1:1, 5:2, 10:3, 15:4, 19:5}
    for n, _, body in items:
        if n in starts:
            divider(starts[n])
        body = re.sub(r'^# (.+)$', lambda m: f'# 第{n:02d}課 · {m[1]} {{#lesson-{n:02d}}}', body, count=1, flags=re.M)
        parts.append(body+'\n\n\\newpage\n')
    divider(6)
    add_file('99-grace-sufficient.md')
    add_file('999-afterword.md')
    parts += ['\\backmatter\n', scripture_index(items)]
    for letter in 'BCDE':
        body = (ROOT/'appendices'/f'{letter}.md').read_text()
        body = re.sub(r'^# (.+)$', rf'# \1 {{#appendix-{letter.lower()}}}', body, count=1, flags=re.M)
        if letter == 'C':
            body += '\n\n## 逐課注疏來源定位\n\n此表由各課「歷代注疏」段落的實際網址生成，供回查原出處；不代表來源已核實或取得授權。\n\n| 課次 | 正文所列來源 |\n|---|---|\n'
            for n, _, lesson in items:
                section=re.search(r'^## 歷代注疏.*?(?=^## |\Z)',lesson,re.M|re.S)
                urls=sorted(set(re.findall(r'https?://[^\s<>）)\]]+',section[0] if section else '')))
                links=', '.join(f'[{urlsplit(url).netloc} {i+1}]({url.rstrip("。，；")})' for i,url in enumerate(urls))
                body += f'| [{n:02d}](#lesson-{n:02d}) | {links or "未列網址，待人工核對版本與頁碼"} |\n'
        parts.append(body)
    return '\n\n'.join(parts)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--check-source', action='store_true')
    args = parser.parse_args()
    fingerprints = source_hashes()
    source = assemble()  # All missing/duplicate sources fail before touching outputs.
    if args.check_source:
        print('PASS: 24 unique lessons; all front matter, seven dividers and full shared appendices available.')
        return
    if not shutil.which('epubcheck'):
        raise RuntimeError('EPUBCheck is required. Install with brew install epubcheck.')
    out = REPO/'output'
    out.mkdir(exist_ok=True)
    lock = out/'.cor2-build.lock'
    lock.mkdir()  # Refuse concurrent builds; never delete another process’s lock.
    try:
        with tempfile.TemporaryDirectory(prefix='.cor2-stage-', dir=out) as folder:
            stage = Path(folder)
            md = stage/f'{NAME}.md'
            md.write_text(source)
            ast = stage/f'{NAME}.json'
            run(['pandoc',md,'-f','markdown','-t','json','--lua-filter',ROOT/'scripts/normalize.lua','-o',ast])
            pdf = stage/f'{NAME}.pdf'
            log = stage/f'{NAME}-build.log'
            print('Building PDF from shared source…', flush=True)
            try:
                with log.open('w') as stream:
                    run(['pandoc',ast,'-f','json','--standalone','--verbose','--pdf-engine=lualatex',
                         '--lua-filter',ROOT/'scripts/pdf-style.lua',
                         '--template',REPO/'templates/pdf/cor2.latex','--toc','--toc-depth=1',
                         '--top-level-division=chapter','-o',pdf], stdout=stream, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError:
                print(log.read_text()[-6000:], file=sys.stderr)
                raise
            logtext = log.read_text()
            defects = re.findall(r'^.*(?:Missing character|Overfull \\[hv]box|^! |Error producing PDF).*$', logtext, re.M)
            if defects or 'This is LuaHBTeX' not in logtext or 'Output written on' not in logtext:
                raise RuntimeError('PDF build failed quality checks:\n'+'\n'.join(defects[:12]))
            epub = stage/f'{NAME}.epub'
            print('Building EPUB from the identical shared source…', flush=True)
            run(['pandoc',ast,'-f','json','--standalone','--toc','--toc-depth=2','-t','epub3',
                 '--css',ROOT/'templates/book.css','-o',epub])
            checklog=stage/f'{NAME}-epubcheck.log'
            try:
                with checklog.open('w') as stream:
                    run(['epubcheck', epub], stdout=stream, stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError:
                print(checklog.read_text(), file=sys.stderr)
                raise
            try:
                run(['python3',ROOT/'scripts/verify_publication.py',stage])
            except subprocess.CalledProcessError:
                diagnostic = Path(tempfile.mkdtemp(prefix='cor2-failed-qa-'))
                shutil.copytree(stage, diagnostic, dirs_exist_ok=True)
                print(f'Failed QA artifacts retained for diagnosis: {diagnostic}', file=sys.stderr)
                raise
            if source_hashes() != fingerprints:
                raise RuntimeError('Sources changed during build; no artifacts promoted. Rebuild the final sources.')
            reportfile=stage/f'{NAME}-qa.json'
            report=json.loads(reportfile.read_text())
            report['inputs']=fingerprints
            reportfile.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
            # All validations precede promotion; os.replace is atomic per file.
            for item in sorted(stage.iterdir(), key=lambda p: (p.name.endswith('-qa.json'),p.name)):
                if item.is_file():
                    os.replace(item, out/item.name)
            print('PASS: validated consolidated PDF/EPUB promoted.', flush=True)
    finally:
        lock.rmdir()

if __name__ == '__main__':
    main()
