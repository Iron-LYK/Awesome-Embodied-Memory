#!/usr/bin/env python3
"""Build the English README and bilingual offline catalogue from data/*.json (stdlib only)."""
from pathlib import Path
import json,collections,shutil,re,html,hashlib
ROOT=Path(__file__).resolve().parents[1]
def read(name):return json.loads((ROOT/'data'/name).read_text(encoding='utf-8'))
def write(path,s):
 p=ROOT/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
def clean(s):return s.replace('\\pi','π').replace('\\mu','μ').replace('\\tau','τ').replace('$','').replace('\\','').replace('{','').replace('}','').replace('|','\\|')
def lang(x,key,l):return x.get(key+'_'+l,x.get(key,''))
DOMAIN_ICONS={'world-models':'🌌','vla':'🦾','agentic-robotics':'🤖','foundations':'🧩'}
METHOD_ICONS={'observed-history':'🎞️','compression-recurrence':'🧠','retrieval-spatial':'🧭','persistent-state':'🌍','predictive-control':'🔮','learning-runtime':'⚙️','evaluation':'🧪','episodic-retrieval':'🗂️','task-progress':'🪜','action-touch':'✋','semantic-spatial':'🗺️','task-state-planning':'📋','procedural-harness':'🛠️','reflection-adaptation':'🔄','architectures':'🏗️','agent-memory':'💭','surveys':'📚'}
def cell(s):return clean(str(s)).replace('\n',' ').replace('<','&lt;').replace('>','&gt;')
def resource_badges(p):
 from urllib.parse import urlparse, quote
 links=[('paper',p['url'])] if p['kind']=='paper' else [('code',p['url'])]
 if p.get('code_url') and p['code_url']!=p['url']:links.append(('code',p['code_url']))
 if p.get('project_url'):links.append(('web',p['project_url']))
 badges=[]
 for k,u in links:
  parsed=urlparse(u);parts=parsed.path.strip('/').split('/')
  # Benchmark forks, PRs and pinned source snippets are evidence links, not project stars.
  repo=(parsed.hostname=='github.com' and len(parts)>=2 and parts[1].lower()!='xpolicylab'
        and (len(parts)==2 or len(parts)>=4 and parts[2]=='tree'))
  if k=='code' and repo:
   name='/'.join(parts[:2]);badge='https://img.shields.io/github/stars/'+quote(name,safe='/')+'.svg?style=social&label=Star'
   badges.append(f'[![GitHub stars]({badge})]({u})')
  else:badges.append(f'[![{k.title()}](assets/link-{k}.svg)]({u})')
 return ' '.join(badges)
def publication(p,l='en'):
 label=p.get('publication_label') or ('Report' if p['source_type']=='report' else 'arXiv')
 date=p.get('date') or ('Repo '+p['timeline_date'] if p.get('timeline_date') else 'n.d.')
 return cell(label)+'<br>'+date
def build_readme(papers,impl,tax,meta,project,paths,l='en'):
 out=[];put=out.append;web=project.get('website_url') or 'website/index.html'
 put('# Awesome-Embodied-Memory\n\n**Remember the world. Carry the past. Act on experience.**\n')
 put(f'🌐 [Website]({web})\n')
 put('An open map of memory in **World Models & WAM, VLA, and Agentic Robotics**. Find the system first, then the mechanism that carries its history into prediction or action.\n')
 put(f'For more detail, search and explore our [interactive website]({web}), which we will continue to update.\n')
 put('<a id="memory-map"></a>\n\n## 🧭 The embodied memory map\n')
 put(f'[![Four perspectives on embodied memory: WAM, VLA, Agentic Robotics and Supporting Foundations](assets/memory-map.svg)]({web})\n')
 put('| Domain | The memory question | Method families | Papers & reports |\n|:---|:---|:---|---:|')
 questions={'world-models':'What persists as the world changes?','vla':'Which history should guide the next action?','agentic-robotics':'How does experience guide a robot over time?','foundations':'Which mechanisms transfer across systems?'}
 for g in tax['groups']:
  cats=[c for c in tax['categories'] if c['parent_id']==g['id']]
  links=' · '.join(f'[{c["label_en"]}](#{c["id"]})' for c in cats)
  put(f'| {DOMAIN_ICONS[g["id"]]} **[{g["label_en"]}](#{g["id"]})** | {questions[g["id"]]} | {links} | **{sum(p["primary_domain"]==g["id"] for p in papers)}** |')
 put('\n**How to read the map:** WAM/VLA describe model interfaces; Agentic Robotics covers the system around them—VLM planning, execution, skills and harnesses. Each work has one primary home. Supporting and contextual work is labeled; long trajectories or action chunks alone do not establish memory.\n')
 put('### 📑 Contents\n')
 for g in tax['groups']:
  put(f'- {DOMAIN_ICONS[g["id"]]} **[{g["label_en"]}](#{g["id"]})**')
  for c in tax['categories']:
   if c['parent_id']==g['id']:put(f'  - [{c["label_en"]}](#{c["id"]})')
 put('- 🔭 **[Pre-publication Methods](#pre-publication-methods)**')
 for g in tax['groups']:
  if any(p['primary_domain']==g['id'] and p['citation_status']=='pending' for p in impl):put(f'  - [{g["label_en"]}](#prepublication-{g["id"]})')
 put('')
 for g in tax['groups']:
  put(f'<a id="{g["id"]}"></a>\n\n## {DOMAIN_ICONS[g["id"]]} {g["label_en"]}\n')
  if g['id']=='vla':put('Vision-language-action models and relevant visuomotor precursors, grouped by how historical evidence reaches the action policy.\n')
  for cat in [c for c in tax['categories'] if c['parent_id']==g['id']]:
   rows=sorted((p for p in papers if p['primary_category']==cat['id']),key=lambda p:(p.get('date') or '',p['title']),reverse=True)
   put(f'<a id="{cat["id"]}"></a>\n\n### {METHOD_ICONS.get(cat["method_family"],"✦")} {cat["label_en"]} · {len(rows)}\n\n{cat["description_en"]}\n')
   put('| Paper | Link | Pub. & Date | TL;DR |\n|:---|:---:|:---:|:---|')
   for p in rows:
    mark={'context':' ◇','survey':' 📚'}.get(p['role'],'')
    put(f'| [{cell(p["title"])}]({p["url"]}){mark} | {resource_badges(p)} | {publication(p)} | {cell(p.get("tldr_en") or p["summary_en"])} |')
   put('')
  put('[↑ Back to the map](#memory-map)\n')
 put('<a id="pre-publication-methods"></a>\n\n## 🔭 Pre-publication Methods\n')
 put('The following methods were surveyed from benchmark submissions, including [RoboDojo](https://robodojo-benchmark.com/), before a matching standalone paper or technical report was verified.\n')
 pending=[p for p in impl if p['citation_status']=='pending']
 for g in tax['groups']:
  rows=[p for p in pending if p['primary_domain']==g['id']]
  if not rows:continue
  put(f'<a id="prepublication-{g["id"]}"></a>\n\n### {DOMAIN_ICONS[g["id"]]} {g["label_en"]}\n')
  put('| Method | Link | TL;DR |\n|:---|:---:|:---|')
  for p in rows:put(f'| [{cell(p["title"])}]({p["url"]}) | {resource_badges(p)} | {cell(p.get("tldr_en") or p["summary_en"])} |')
  put('')
 put('---\n')
 put(f'**Sources & licenses:** {len(papers)} papers and reports; review depth is shown per record on the website. [Evidence policy](docs/methodology.md) · [Acknowledgements](docs/acknowledgements.md) · Content [CC BY 4.0](LICENSE-CONTENT) / code [MIT](LICENSE-CODE). AI-assisted curation; no model experiments rerun.')
 return '\n'.join(out)+'\n'
def public_catalogue(papers,impl):
 # Keep every source audit in canonical JSON; fold paper-backed deployments into their paper's details.
 import copy
 records=copy.deepcopy(papers);by={p['id']:p for p in records};aliases={}
 for entry in impl:
  target=next((pid for pid in entry.get('related_ids',[]) if pid in by),None)
  if entry['citation_status']=='verified' and target:
   by[target].setdefault('implementation_notes',[]).append(copy.deepcopy(entry));aliases[entry['id']]=target
  else:records.append(copy.deepcopy(entry))
 return records,aliases
def build_pending_references(impl,updated,l):
 zh=l=='zh';pending=[p for p in impl if p['citation_status']=='pending']
 if zh:
  out=['# 待补引用\n',f'更新于 {updated}。**{len(pending)} 项实现变体**尚未核实匹配的独立论文或技术报告。这不表示任何地方都不存在论文，也不保证之后发表。核实之前保留 **`方法名: TODO ref`**。\n','网站将这些条目统一标记为“待正式发表的方法”。这描述论文匹配状态，不否认代码可能由作者官方发布。已有论文的部署核查附在对应论文详情中，保留原始证据与版本。\n','| 占位引用 | 固定来源 | 相关研究 |\n|---|---|---|']
 else:
  out=['# Pending references\n',f'Updated {updated}. **{len(pending)} implementation variants** have no matching standalone paper or technical report verified in this audit. This is not a claim that no paper exists anywhere, nor a prediction that one will be published. Keep **`Method name: TODO ref`** until replacement.\n','The website labels these entries **Pre-publication methods**. This describes publication matching, not whether the code release is official. Paper-backed deployment audits appear within the corresponding paper details, retaining their original evidence and versions.\n','| Placeholder | Fixed source | Related research |\n|---|---|---|']
 for p in pending:
  related=', '.join(p.get('related_ids',[])) or ('尚未核实' if zh else 'None verified for this variant')
  out.append(f'| {cell(p["display_citation"])} | [{"核查代码" if zh else "audited code"}]({p["source_links"][0]["url"]}) | {related} |')
 if zh:out.append('\n## 替换占位引用\n\n1. 核实标题、作者、主要网址／标识符、版本日期，以及论文是否涵盖这个实现变体。\n2. 新增或关联去重论文记录，保留实现 ID、固定提交、来源哈希及引用映射。\n3. 仅在匹配来源核实后设 `citation_status: verified`，更新 `display_citation` 和 `bibtex`；配置特有结论仍以代码证据为准。\n4. 重新构建目录；构建器将已匹配的部署核查移入论文详情，旧条目链接及收藏继续映射。\n\n这些占位项不是有效的论文引用。若在投稿稿件中使用，需核实替换、改为合规软件引用或移除；目录更新不会自动改动配套稿件。')
 else:out.append('\n## Replace a placeholder\n\n1. Verify title, authors, primary URL/identifier, version date, and whether the paper covers this variant.\n2. Add or link the distinct research-work record. Preserve the implementation ID, pinned commit, source hash and citation mapping.\n3. Set `citation_status: verified` only after verifying the matching source; update `display_citation` and `bibtex`. Implementation-specific claims remain grounded in code.\n4. Rebuild the catalogue. The build attaches the verified deployment audit to its paper; old record links and saved items resolve to that paper.\n\nThese placeholders are not valid paper citations. A submission must resolve them, use valid software citations, or omit them. Catalogue updates do not automatically modify the companion manuscript.')
 return '\n'.join(out)+'\n'
def main():
 papers,impl,tax,notes,meta,project,paths=[read(n+'.json') for n in ['papers','implementations','taxonomy','research_notes','provenance','project','reading_paths']]
 from build_taxonomy_art import build_assets
 build_assets(papers,impl,tax,meta)
 meta.update(research_works=len(papers),implementation_records=len(impl),pending_references=sum(r['citation_status']=='pending' for r in impl))
 public_records,aliases=public_catalogue(papers,impl)
 data={'updated':meta['updated'],'project':project,'taxonomy':tax,'records':public_records,'record_aliases':aliases,'notes':notes,'reading_paths':paths,'provenance':meta}
 payload=json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
 write('website/assets/catalogue.js','/* Generated by scripts/build.py. Edit data/*.json. */\nwindow.MEMORY_CATALOGUE='+payload+';\n');write('website/assets/catalogue.json',json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 write('references.bib','% Research works only. Pinned/observed versions; venues not silently inferred.\n\n'+'\n\n'.join(p['bibtex'] for p in papers)+'\n')
 write('implementation-references.bib','% Unresolved publication placeholders; NOT research-paper citations.\n\n'+'\n\n'.join(p['bibtex'] for p in impl if p['citation_status']=='pending')+'\n')
 write('README.md',build_readme(papers,impl,tax,meta,project,paths))
 for l in ['en','zh']:write('docs/pending-references'+('.zh-CN' if l=='zh' else '')+'.md',build_pending_references(impl,meta['updated'],l))
 for l in ['en','zh']:
  zh=l=='zh';s='# '+('领域与方法分类' if zh else 'Domain and method taxonomy')+'\n\n'+('主要归属用于不重复计数；机制标签用于跨领域检索。领域不是互斥的能力声明。旧综述章节映射保留在每条记录的 legacy 字段中。\n\n' if zh else 'The primary home supplies non-duplicated counts; mechanism tags support cross-domain discovery. Domains are not mutually exclusive capability claims. Original manuscript mappings remain in each record’s legacy fields.\n\n')
  for g in tax['groups']:
   s+='## '+lang(g,'label',l)+'\n\n'+lang(g,'description',l)+'\n\n'
   for c in tax['categories']:
    if c['parent_id']==g['id']:s+=f'- **{lang(c,"label",l)}** (`{c["id"]}`): {lang(c,"description",l)}\n'
   s+='\n'
  s+='## '+('六个证据轴' if zh else 'Six evidence axes')+'\n\n'
  for a in tax['six_axes']:s+='- **'+lang(a,'label',l)+'**: '+lang(a,'description',l)+'\n'
  write('docs/taxonomy'+('.zh-CN' if zh else '')+'.md',s)
 # The site folder is independently deployable. Rewrite resource links without inventing a hosting URL.
 resource=ROOT/'website/resources';resource.mkdir(parents=True,exist_ok=True)
 for f in ['README.md','CONTRIBUTING.md','CONTRIBUTING.zh-CN.md','references.bib','implementation-references.bib','LICENSE-CONTENT','LICENSE-CODE','NOTICE.md']:
  if (ROOT/f).exists():shutil.copy2(ROOT/f,resource/f)
 for f in (ROOT/'docs').glob('*.md'):
  if f.name not in ['README.md','README.zh-CN.md']:(resource/f.name).write_text(f.read_text().replace('(../data/','(../assets/').replace('(../NOTICE.md)','(NOTICE.md)'),encoding='utf-8')
 for pattern in ['*.png','*.gif','*.jpg']:
  for figure in (ROOT/'docs').glob(pattern):shutil.copy2(figure,resource/figure.name)
 for f in ['README.md']:
  p=resource/f;p.write_text(p.read_text().replace('(website/index.html','(../index.html').replace('(assets/','(../assets/').replace('(docs/','('),encoding='utf-8')
 for name in ['discovery_log.json','coverage.json','resource_audit.json','date_audit.json']:
  if (ROOT/'data'/name).exists():shutil.copy2(ROOT/'data'/name,ROOT/'website/assets'/name)
 for f in (ROOT/'assets').glob('*.svg'):shutil.copy2(f,ROOT/'website/assets'/f.name)
 shutil.copy2(ROOT/'assets/neural-brain-network.png',ROOT/'website/assets/neural-brain-network.png')
 index=(ROOT/'website/index.html').read_text()
 index=re.sub(r'(<strong id="paperTotal">)\d+(</strong>)',lambda m:m[1]+str(len(public_records))+m[2],index)
 index=re.sub(r'(<b id="researchTotal">).*?(</b>)',lambda m:m[1]+str(len(public_records))+m[2],index)
 for asset in ['style.css','app.js','i18n.js','catalogue.js','constellation.js','neural-brain-network.png']:
  digest=hashlib.sha256((ROOT/'website/assets'/asset).read_bytes()).hexdigest()[:12]
  index=re.sub(r'assets/'+re.escape(asset)+r'(?:\?v=[a-zA-Z0-9.\-]+)?', 'assets/'+asset+'?v='+digest,index)
 write('website/index.html',index)
 print(json.dumps({'research':len(papers),'implementations':len(impl),'method_families':len(tax['categories']),'domains':dict(collections.Counter(p['primary_domain'] for p in papers))},ensure_ascii=False))
if __name__=='__main__':main()
