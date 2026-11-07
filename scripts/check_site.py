#!/usr/bin/env python3
"""Offline checks for generated assets, bilingual UI, links and source/package safety."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
import json,re,sys,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];site=R/'website'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=[];self.keys=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  for k in ['href','src']:
   if k in a:self.links.append(a[k])
  self.keys += [v for k,v in attrs if k.startswith('data-i18n')]
p=Page();p.feed((site/'index.html').read_text())
assert len(p.ids)==len(set(p.ids)),'Duplicate HTML IDs'
for link in p.links:
 u=urlparse(link)
 if u.scheme or not u.path:continue
 assert (site/unquote(u.path)).is_file(),f'Missing HTML target: {link}'
raw=(site/'assets/i18n.js').read_text();strings=json.loads(raw[raw.index('{'):raw.rindex('}')+1])
assert set(strings['en'])==set(strings['zh']),'Translation keys differ'
assert set(p.keys)<=set(strings['en']),'HTML has missing translation keys'
js=(site/'assets/app.js').read_text()+(site/'assets/constellation.js').read_text()
assert not re.search(r'\bfetch\(|XMLHttpRequest|https://[^\s]+cdn',js),'Unexpected external runtime dependency'
for key in re.findall(r"\bt\('([A-Za-z]+)'",js):assert key in strings['en'],f'Missing UI key: {key}'
for key in re.findall(r"\btr\('([A-Za-z]+)'",js):assert key in strings['en'],f'Missing map UI key: {key}'
catalogue=json.loads((site/'assets/catalogue.json').read_text());records=catalogue['records'];aliases=catalogue['record_aliases']
canonical=[r for n in ['papers.json','implementations.json'] for r in json.loads((R/'data'/n).read_text())]
visible_ids={r['id'] for r in records};all_ids={r['id'] for r in canonical}
assert len(visible_ids)==len(records),'Duplicate public records'
assert visible_ids.isdisjoint(aliases) and visible_ids|set(aliases)==all_ids,'Missing source record after consolidation'
assert all(target in visible_ids for target in aliases.values()),'Broken deployment alias'
assert {n['id'] for r in records for n in r.get('implementation_notes',[])}==set(aliases),'Lost deployment evidence'
assert all(r['citation_status']=='pending' for r in records if r['kind']=='implementation'),'Paper-backed deployment was not consolidated'
public=[R/'README.md',*site.rglob('*.html'),*site.rglob('*.js'),*site.rglob('*.json'),*site.rglob('*.md')]
for path in public:assert '/Users/' not in path.read_text(),f'Local path leak: {path.name}'
for path in [R/'README.md',*site.glob('resources/*.md'),*R.glob('docs/*.md')]:
 for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
  u=urlparse(target.strip('<>'))
  if u.scheme or not u.path:continue
  assert (path.parent/unquote(u.path)).exists(),f'Broken document link: {path.relative_to(R)} -> {target}'
for svg in [*(R/'assets').glob('*.svg'),*(site/'assets').glob('*.svg')]:ET.parse(svg)
for license in ['LICENSE','LICENSE-CODE','LICENSE-CONTENT','NOTICE.md']:assert (R/license).is_file(),license
for lang in ['']:
 readme=(R/('README'+lang+'.md')).read_text()
 assert readme.count('| Pub. & Date | TL;DR |')==24,'Expected one table per method family'
 assert all(f'<a id="{c["id"]}"></a>' in readme for c in json.loads((R/'data/taxonomy.json').read_text())['categories']),'Missing category anchor'
 assert not any(s in readme for s in ['Start here: three reading paths','A research desk in your browser','The paper index','Contributing and maintaining','README.zh-CN','assets/banner','assets/stats','Implementation watch','Reference status','🔗 **Links:**']),'Removed section was restored'
 assert '](assets/memory-map.svg)' in readme,'Missing requested four-quadrant map'
 assert '[interactive website](' in readme and '## 🔭 Pre-publication Methods' in readme,'Missing requested entry points'
 assert not re.search(r'img\.shields\.io/github/stars/[^\s)]+/XPolicyLab',readme,re.I),'Benchmark fork stars must not represent a method'
 assert len(re.findall(r'^\| \[[^\]]+\]\(https://',readme,re.M))==len(records),'Each public method must appear once in README'
assert not (R/'README.zh-CN.md').exists() and not (site/'resources/README.zh-CN.md').exists(),'Retired translated README restored'
assert 'tab-implementations' not in p.ids and 'implementationTotal' not in p.ids,'Retired UI survived'
print(f'PASS: {len(p.ids)} HTML IDs, {len(strings["en"])} bilingual UI keys, {len(records)} catalogue entries; local links, generated data and public-path checks.')
