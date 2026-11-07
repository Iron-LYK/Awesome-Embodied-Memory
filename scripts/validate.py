#!/usr/bin/env python3
"""Validate catalogue structure, provenance, bilingual completeness, and counting invariants."""
import json,re,collections,datetime
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(n):return json.loads((R/'data'/n).read_text(encoding='utf-8'))
def require(condition,message):
 if not condition:raise ValueError(message)
papers=read('papers.json');impl=read('implementations.json');tax=read('taxonomy.json');meta=read('provenance.json');rows=papers+impl
ids=[p['id'] for p in rows];require(len(ids)==len(set(ids)),'Duplicate record IDs')
cats={c['id']:c for c in tax['categories']};groups={g['id'] for g in tax['groups']};tags={t['id'] for t in tax['mechanism_tags']}
for p in rows:
 pid=p['id'];require(p['title'] and p['url'].startswith('https://'),pid+': title/source')
 for field in ['summary_en','summary_zh','analysis_en','analysis_zh']:require(bool(p.get(field)),pid+': missing '+field)
 require(not re.search('[\u4e00-\u9fff]',p['summary_en']+p['analysis_en']),pid+': Chinese in English annotation')
 require(p['primary_domain'] in groups,pid+': domain');require(p['primary_category'] in cats,pid+': category')
 c=cats[p['primary_category']];require(c['parent_id']==p['primary_domain'] and c['method_family']==p['method_family'],pid+': hierarchy mismatch')
 require(set(p['category_ids'])<=cats.keys() and p['primary_category'] in p['category_ids'],pid+': category list')
 require(set(p['mechanism_tags'])<=tags,pid+': mechanism tags')
 require(set(p.get('related_ids',[]))<=set(ids),pid+': related IDs')
 require(p.get('source_links') and all(s['url'].startswith('https://') for s in p['source_links']),pid+': source links')
 require('@' in p['bibtex'] and '{'+p['bibkey']+',' in p['bibtex'],pid+': BibTeX')
 if p['kind']=='paper':
  for lang in ['en','zh']:
   short=p.get('tldr_'+lang,'')
   require(bool(short) and '\n' not in short and '|' not in short,pid+': compact table summary '+lang)
   require(len(short.split())<=30 if lang=='en' else len(short)<=75,pid+': TL;DR too long '+lang)
  require(not re.search('[\u4e00-\u9fff]',p['tldr_en']),pid+': Chinese in English TL;DR')
  for field in ['code_url','project_url']:
   if p.get(field):
    require(p[field].startswith(('https://','http://')),pid+': resource URL scheme')
    require(any(e.get('field')==field and e.get('url')==p[field] and e.get('source') for e in p.get('link_evidence',[])),pid+': missing resource provenance '+field)
  if p.get('code_url'):
   require(p.get('code_availability',{}).get('status')=='implementation-visible',pid+': unverified implementation badge')
  if p.get('publication_label'):require(p.get('publication_evidence',{}).get('source'),pid+': venue source')
  require(p['citation_status']=='verified' and 'TODO ref' not in p['bibtex'],pid+': unresolved research citation')
  require(p['authors'] and p.get('review_depth'),pid+': authors/review depth')
  require(p['role'] in ['primary','context','survey'],pid+': role')
  require(bool(re.fullmatch('[a-f0-9]{64}',p.get('source_sha256',''))),pid+': source hash')
  if p.get('date'):
   
   if re.fullmatch(r'\d{4}',p['date']):require(p['source_type']=='report',pid+': year-only non-report')
   else:datetime.date.fromisoformat(p['date'])
   require(p['date']<=meta['updated'],pid+': future date')
  else:require(p['source_type']=='report',pid+': undated non-report')
  if p.get('inclusion_batch')=='2026-11-02 embodied expansion':
   for key in ['memory_relevance_en','memory_relevance_zh','evidence_locator','source_sha256_basis','discovery_sources','versioned_url','source_version']:require(bool(p.get(key)),pid+': missing '+key)
 else:
  for f in ['enabled_status','lifetime','reset','handoff']:
   require(bool(p.get(f)) and bool(p.get(f+'_en')),pid+': bilingual '+f)
  require(set(p.get('axes_en',{}))=={a['id'] for a in tax['six_axes']},pid+': English axes')
  if p['citation_status']=='pending':require(p['display_citation'].endswith(': TODO ref') and 'TODO ref' in p['bibtex'],pid+': pending marker')
  require(all(re.fullmatch('[a-f0-9]{40}',s['commit']) for s in p['source_links'] if s.get('commit')),pid+': commit')
 require('/Users/' not in json.dumps(p) and 'primary_source_file' not in p,pid+': private path/cache')
 if p.get('timeline_date'):
  datetime.date.fromisoformat(p['timeline_date'])
  require(p['timeline_date']<=meta['updated'],pid+': future timeline date')
  require(p.get('timeline_date_basis') in ['benchmark-pr','report-repository-commit'],pid+': timeline date basis')
  e=p.get('timeline_date_evidence',{})
  require(e.get('url','').startswith('https://') and re.fullmatch('[a-f0-9]{64}',e.get('source_sha256','')),pid+': timeline date evidence')
  require(p.get('timeline_date_note_en') and p.get('timeline_date_note_zh'),pid+': bilingual timeline date scope')
keys=[p['bibkey'] for p in papers];require(len(set(keys))==len(keys),'Duplicate research citation keys')
def norm(s):return re.sub(r'[^\w]+','',s.casefold())
nt=collections.defaultdict(list)
for p in papers:nt[norm(p['title'])].append(p['id'])
require(not any(len(v)>1 for v in nt.values()),'Duplicate normalized titles: '+str({k:v for k,v in nt.items() if len(v)>1}))
dois=[p['doi'].casefold().strip() for p in papers if p.get('doi')];require(len(dois)==len(set(dois)),'Duplicate DOI')
for n in read('research_notes.json'):
 require(all(n.get(k) for k in ['title_en','title_zh','body_en','body_zh']),'Research-note translation');require(set(n['ids'])<=set(ids),'Research-note links')
for p in read('reading_paths.json'):
 require(all(s['id'] in ids for s in p['steps']),'Reading-path reference')
require(meta['research_works']==len(papers),'Stale provenance count');require(meta['implementation_records']==len(impl),'Stale implementation count')
report={'status':'PASS','research_works':len(papers),'implementation_records':len(impl),'pending_references':sum(x['citation_status']=='pending' for x in impl),'primary_domains':dict(collections.Counter(p['primary_domain'] for p in papers)),'roles':dict(collections.Counter(p['role'] for p in papers)),'method_families':len(cats),'checks':['IDs/titles/DOIs deduplicated','bilingual annotations','hierarchy and mechanism tags','primary-source links/hashes','date and review-depth presence','BibTeX/placeholders','private-path exclusion','reading-path links'],'scope':'Structural/content-contract checks, not independent full-paper replication.'}
(R/'docs/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,ensure_ascii=False))
