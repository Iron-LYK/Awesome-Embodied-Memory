#!/usr/bin/env python3
"""Build a four-quadrant, data-driven English README map with original vector artwork."""
from pathlib import Path
from html import escape
from collections import Counter
import json,xml.etree.ElementTree as ET
from robot_art import robot_svg
ROOT=Path(__file__).resolve().parents[1]
FONT="-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,sans-serif"
INK='#21363e';MUTED='#60747a'
COLORS={'world-models':('#366a8a','#edf4f8','#bdd3df'),'vla':('#317867','#eef6f1','#bfdacf'),'agentic-robotics':('#976c35','#faf4e9','#e4d2b4'),'foundations':('#746687','#f5f1f8','#d7cee2')}

def text(x,y,s,size=22,color=INK,weight=400,anchor='start',extra=''):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}" {extra}>{escape(str(s))}</text>'
def icon(name,x,y,color,size=42):
 paths={
 'world-models':'<circle cx="20" cy="20" r="16"/><ellipse cx="20" cy="20" rx="7" ry="16"/><path d="M4 20h32M7 11h26M7 29h26"/>',
 'vla':'<path d="M4 36h32M9 35v-9l10-9-7-9M20 17l10-9M27 4l9 2-1 9"/><circle cx="12" cy="8" r="4"/><circle cx="20" cy="17" r="4"/><circle cx="9" cy="27" r="3"/>',
 'agentic-robotics':'<rect x="6" y="11" width="28" height="24" rx="8"/><path d="M20 11V5M2 19h4M34 19h4M14 28q6 4 12 0"/><circle cx="20" cy="3" r="2"/><path d="M13 20v2M27 20v2"/>',
 'foundations':'<path d="M3 10l17-7 17 7-17 7zM3 20l17 7 17-7M3 30l17 7 17-7"/>'}
 return f'<g transform="translate({x} {y}) scale({size/40})" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{paths[name]}</g>'
def method_icon(index,x,y,color):
 paths=['<path d="M1 5h15v11H1zM5 2h14v10M5 9h7M5 12h4"/>','<path d="M1 3h4v14H1zM8 6h4v8H8zM15 8h4v4h-4z"/>','<circle cx="8" cy="8" r="6"/><path d="m12 12 6 6M5 8h6M8 5v6"/>','<path d="M2 4h16v13H2zM5 1v6M15 1v6M5 10h10M5 13h6"/>','<path d="M1 10h5l3-7 3 14 3-7h4"/>','<path d="M3 3h5v5H3zM12 3h5v5h-5zM3 12h5v5H3zM12 12h5v5h-5z"/>','<path d="M4 1h12M7 1v7L2 17h16l-5-9V1M5 12h10"/>']
 return f'<g transform="translate({x} {y})" fill="none" stroke="{color}" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">{paths[index%len(paths)]}</g>'
def build_assets(papers,impl,tax,meta):
 pending=[r for r in impl if r['citation_status']=='pending'];counts=Counter(r['primary_domain'] for r in papers);waiting=Counter(r['primary_domain'] for r in pending)
 out=['<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="1160" viewBox="0 0 1400 1160" role="img" aria-labelledby="map-title map-desc">','<title id="map-title">The embodied memory map</title>','<desc id="map-desc">Four quadrants: World Models and WAM, VLA, Agentic Robotics, and Supporting Foundations. Counts separate papers and reports from pre-publication methods. Connections show classification, not model architecture.</desc>',f'<g font-family="{FONT}">','<rect width="1400" height="1160" rx="28" fill="#fcfbf7"/>',text(50,49,'AWESOME / EMBODIED MEMORY',16,MUTED,600,extra='letter-spacing="2"'),text(50,106,'The embodied memory map',43,INK,650),text(1350,101,'FOUR PERSPECTIVES · ONE FIELD',15,MUTED,500,'end',extra='letter-spacing="1.6"')]
 positions={'world-models':(40,155),'vla':(760,155),'agentic-robotics':(40,665),'foundations':(760,665)}
 for g in tax['groups']:
  domain=g['id'];x,y=positions[domain];color,tint,edge=COLORS[domain];cats=[c for c in tax['categories'] if c['parent_id']==domain];header_offset=40 if domain=='foundations' else 0
  assert len(cats)<=7,'More than seven families requires a map-layout update'
  out += [f'<g data-domain="{domain}">',f'<rect x="{x}" y="{y+5}" width="600" height="395" rx="23" fill="#293e42" opacity=".035"/>',f'<rect x="{x}" y="{y}" width="600" height="395" rx="23" fill="#ffffff" stroke="{edge}" stroke-width="1.5"/>',f'<path d="M{x+23} {y}H{x+577}Q{x+600} {y} {x+600} {y+23}V{y+132}H{x}V{y+23}Q{x} {y} {x+23} {y}Z" fill="{tint}"/>',icon(domain,x+28+header_offset,y+23,color,38),text(x+82+header_offset,y+51,g['label_en'],27,color,650),text(x+565,y+88,str(len(cats)).zfill(2),25,color,600,'end'),text(x+565,y+111,'FAMILIES',12,color,500,'end',extra='letter-spacing="1.2"'),text(x+30,y+108,counts[domain],42,color,650),text(x+132,y+106,'papers & reports',17,MUTED)]
  if waiting[domain]:out += [text(x+310,y+108,'+'+str(waiting[domain]),27,color,600),text(x+365,y+106,'pre-publication',16,MUTED)]
  else:out += [text(x+310,y+108,'Cross-domain',17,MUTED,500)]
  for n,c in enumerate(cats):
   row=y+169+n*31
   out += [f'<g data-category="{c["id"]}">',method_icon(n,x+31,row-15,color),text(x+63,row,c['label_en'],21.5,INK),'</g>']
  if domain=='agentic-robotics':out += [text(x+63,y+366,'VLM planning · policy execution · harness',16,MUTED)]
  if domain=='foundations':out += [text(x+63,y+315,'Shared mechanisms, concepts and evaluation',17,MUTED),text(x+63,y+343,'that connect worlds, policies and agents.',17,MUTED)]
  out.append('</g>')
 # The hub sits in the four inner corners, without covering the category labels.
 for d,(x,y) in {'world-models':(618,525),'vla':(782,525),'agentic-robotics':(618,690),'foundations':(782,690)}.items():
  color=COLORS[d][0];out += [f'<path d="M{x} {y}Q700 {y} 700 606" fill="none" stroke="{color}" stroke-width="1.5" opacity=".7"/>',f'<circle cx="{x}" cy="{y}" r="5" fill="{color}"/>']
 out += ['<circle cx="700" cy="606" r="132" fill="#fcfbf7"/>','<circle cx="700" cy="606" r="121" fill="#142b38"/>','<circle cx="700" cy="606" r="114" fill="none" stroke="#7598a5" stroke-width=".8"/>','<circle cx="700" cy="606" r="128" fill="none" stroke="#c7d5d7" stroke-width="1" stroke-dasharray="2 9"/>','<g transform="translate(650 510)">'+robot_svg('map-robot',width=100,height=100)+'</g>',text(700,633,'EMBODIED',23,'#f4fbf9',600,'middle',extra='letter-spacing="2"'),text(700,662,'MEMORY MAP',20,'#b8d9dd',500,'middle',extra='letter-spacing="1.2"')]
 out += ['<path d="M50 1090h1300" stroke="#d8e0de"/>',text(50,1124,f'{len(papers)} papers & reports   +   {len(pending)} pre-publication methods   ·   {len(tax["categories"])} method families',19,INK,500),text(1350,1124,'UPDATED '+meta['updated'],16,MUTED,500,'end'),'</g></svg>']
 result='\n'.join(out)+'\n';tree=ET.fromstring(result)
 assert {x.attrib['data-category'] for x in tree.iter() if 'data-category' in x.attrib}=={c['id'] for c in tax['categories']}
 (ROOT/'assets/memory-map.svg').write_text(result,encoding='utf-8')
 (ROOT/'assets/memory-robot.svg').write_text(robot_svg(),encoding='utf-8')
 return result

def main():
 args=[json.loads((ROOT/'data'/f'{name}.json').read_text()) for name in ['papers','implementations','taxonomy','provenance']];build_assets(*args);print('Built the four-quadrant taxonomy map with canonical counts.')
if __name__=='__main__':main()
