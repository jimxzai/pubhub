"""Print an editorial inventory; counts are not permission or textual verification."""
import re
from pathlib import Path

root = Path(__file__).resolve().parent
print('file\tNASB marked verse occurrences\tNASB verse markers\tMorgan English quote blocks\tMacArthur English quote blocks\thymn titles requiring version review')
total = 0
expanded_total = 0
for n in range(1,25):
    path, = root.glob(f'{n:02d}-*.md')
    text = path.read_text()
    def section(heading):
        stop = r'\n#{1,3} ' if heading.startswith('### ') else r'\n#{1,2} '
        match = re.search(heading + r'\n(.*?)(?=' + stop + r'|\Z)', text, re.S)
        return match.group(1) if match else ''
    nasb = section(r'### English[^\n]*NASB[^\n]*')
    markers = re.findall(r'\^([0-9,:-]+)\^', nasb)
    total += len(markers)
    for marker in markers:
        for part in marker.split(','):
            nums = part.split('-')
            expanded_total += int(nums[-1]) - int(nums[0]) + 1
    morgan = section(r'### 摩根[^\n]*')
    mac = section(r'### 麥克阿瑟[^\n]*')
    hymns = section(r'## 詩篇與聖詩[^\n]*')
    titles = re.findall(r'^### ([A-Za-z][^\n]*)', hymns, re.M)
    print('\t'.join([path.name, str(len(markers)), ','.join(markers),
        str(len(re.findall(r'^> "', morgan, re.M))),
        str(len(re.findall(r'^> "', mac, re.M))), '; '.join(titles)]))
print(f'# NASB main-section marked occurrences: {total}. Excludes unmarked quotes, front/back matter and template repeats; not a release total.')
print(f'# NASB main-section verse occurrences after expanding ranges: {expanded_total}; partial verses count once. Same exclusions apply.')
