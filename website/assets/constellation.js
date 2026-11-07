/* Original interactive taxonomy artwork. Connections encode categories, not citation or performance relations. */
(() => {
'use strict';
const $=id=>document.getElementById(id),data=window.MEMORY_CATALOGUE;
if(!data||!$('constellation'))return;
const papers=data.records,tax=data.taxonomy;
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const layouts={
 'world-models':{color:'#a7d8ef',at:[155,135],children:[[100,70],[178,48],[242,85],[70,160],[213,196],[97,245],[246,241]],name:['World Models & WAM','世界模型与 WAM']},
 'vla':{color:'#b5d8c8',at:[620,148],children:[[570,72],[650,42],[730,90],[742,180],[695,260],[592,253],[552,177]],name:['VLA','VLA']},
 'agentic-robotics':{color:'#ead3a8',at:[620,451],children:[[700,360],[746,440],[699,541],[598,563],[528,520],[530,409]],name:['Agentic Robotics','智能体机器人']},
 'foundations':{color:'#cbd2d7',at:[205,466],children:[[118,375],[94,490],[232,560],[299,505]],name:['Foundations','支撑性基础']}
};
let language='en',domain='',category='',hover='';
const tr=(k,v={})=>Object.entries(v).reduce((s,[key,val])=>s.replaceAll('{'+key+'}',val),window.MEMORY_I18N[language][k]||k);
const label=o=>o['label_'+language];
const count=(d,c='')=>papers.filter(r=>(!d||r.primary_domain===d)&&(!c||r.primary_category===c)).length;
const nodes=[],edges=[];
for(const g of tax.groups){const layout=layouts[g.id],[x,y]=layout.at;nodes.push({id:g.id,domain:g.id,x,y,root:true});
 edges.push(`<path class="neural-link main-link" data-edge-domain="${g.id}" style="--node-color:${layout.color}" d="M${x} ${y}C${(x+400)/2} ${y},${(x+400)/2} 273,400 273"/>`);
 const cats=tax.categories.filter(c=>c.parent_id===g.id);
 cats.forEach((c,i)=>{const [u,v]=layout.children[i];nodes.push({id:c.id,domain:g.id,x:u,y:v,root:false});edges.push(`<path class="neural-link" data-edge-domain="${g.id}" data-edge-category="${c.id}" style="--node-color:${layout.color}" d="M${x} ${y}Q${(x+u)/2+15} ${(y+v)/2-10} ${u} ${v}"/>`);
  if(i){const [a,b]=layout.children[i-1];edges.push(`<path class="neural-link mesh-link" data-edge-domain="${g.id}" style="--node-color:${layout.color}" d="M${a} ${b}L${u} ${v}"/>`);}
 });
}
$('neuralLinks').innerHTML=edges.join('');
$('starNodes').innerHTML=nodes.map(n=>`<button class="star-node ${n.root?'domain-star':''}" data-star="${n.id}" data-star-domain="${n.domain}" style="left:${n.x/8}%;top:${n.y/6.5}%;--node-color:${layouts[n.domain].color}" aria-pressed="false">${n.root?'<span class="node-label"></span>':''}</button>`).join('');
function highlight(temp=''){
 const selected=category||domain,focus=temp||selected,group=layouts[focus]?focus:tax.categories.find(c=>c.id===focus)?.parent_id;
 document.querySelectorAll('[data-star]').forEach(b=>{const active=b.dataset.star===focus;b.classList.toggle('active',active);b.classList.toggle('dimmed',!!group&&b.dataset.starDomain!==group);b.setAttribute('aria-pressed',String(b.dataset.star===selected));});
 document.querySelectorAll('[data-edge-domain]').forEach(e=>{e.classList.toggle('lit',!!focus&&(e.dataset.edgeCategory===focus||!e.dataset.edgeCategory&&e.dataset.edgeDomain===group));e.classList.toggle('dimmed',!!group&&e.dataset.edgeDomain!==group);});
}
function selection(){const c=tax.categories.find(c=>c.id===category),g=tax.groups.find(g=>g.id===(domain||c?.parent_id));
 const n=count(g?.id||'',c?.id||'');
 $('mapSelection').innerHTML=`<p class="selection-eyebrow">${esc(tr(c?'mapSelectedMethod':g?'mapSelected':'mapMethods'))}</p><h2>${esc(c?label(c):g?label(g):tr('mapAllTitle'))}</h2><p>${esc(c?c['description_'+language]:g?g['tagline_'+language]:tr('mapAllBody'))}</p>${g&&!c?`<div class="method-chips">${tax.categories.filter(c=>c.parent_id===g.id).map(c=>`<button data-map-category="${c.id}">${esc(label(c))} <span>${count(g.id,c.id)}</span></button>`).join('')}</div>`:''}<a href="#library" class="selection-link">${esc(tr('viewWorks',{n}))}</a>`;
}
function update(next){language=next.language;domain=next.domain||'';category=next.category||'';
 for(const n of nodes){const button=document.querySelector(`[data-star="${n.id}"]`),obj=n.root?tax.groups.find(g=>g.id===n.id):tax.categories.find(c=>c.id===n.id),nCount=count(n.domain,n.root?'':n.id);button.setAttribute('aria-label',label(obj)+' · '+nCount+' '+tr('works'));if(n.root)button.querySelector('.node-label').innerHTML=esc(layouts[n.domain].name[language==='zh'?1:0])+`<small>${nCount} ${esc(tr('works'))}</small>`;}
 highlight();selection();setMotionLabel();hero.classList.toggle('has-selection',!!(domain||category));
}
function choose(id){const n=nodes.find(n=>n.id===id);document.dispatchEvent(new CustomEvent('memory-map-select',{detail:{domain:n?.root?n.id:'',category:n&&!n.root?n.id:''}}));$('starTooltip').hidden=true;}
function tooltip(button){const n=nodes.find(n=>n.id===button.dataset.star),obj=n.root?tax.groups.find(g=>g.id===n.id):tax.categories.find(c=>c.id===n.id);hover=n.id;highlight(hover);const tip=$('starTooltip');tip.textContent=label(obj)+' · '+count(n.domain,n.root?'':n.id);tip.style.left=Math.max(21,Math.min(79,n.x/8))+'%';tip.style.top=n.y/6.5+'%';tip.hidden=false;}
$('starNodes').addEventListener('click',e=>{const b=e.target.closest('[data-star]');if(b)choose(b.dataset.star);});
$('starNodes').addEventListener('pointerover',e=>{const b=e.target.closest('[data-star]');if(b)tooltip(b);});
$('starNodes').addEventListener('focusin',e=>{const b=e.target.closest('[data-star]');if(b)tooltip(b);});
function leave(){hover='';highlight();$('starTooltip').hidden=true;}
$('starNodes').addEventListener('pointerout',e=>{if(!e.relatedTarget?.closest?.('[data-star]'))leave();});
$('starNodes').addEventListener('focusout',leave);
$('starNodes').addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight','ArrowUp','ArrowDown','Home','End'].includes(e.key))return;const buttons=[...$('starNodes').querySelectorAll('button')],i=buttons.indexOf(e.target);if(i<0)return;e.preventDefault();const n=e.key==='Home'?0:e.key==='End'?buttons.length-1:(i+(['ArrowLeft','ArrowUp'].includes(e.key)?-1:1)+buttons.length)%buttons.length;buttons[n].focus();});
$('mapSelection').addEventListener('click',e=>{const b=e.target.closest('[data-map-category]');if(b)choose(b.dataset.mapCategory);});
$('allStars').onclick=()=>choose('');

// Scroll-linked perspective, rendered locally and paused when outside the viewport.
const canvas=$('starfield'),ctx=canvas.getContext('2d'),hero=document.querySelector('.hero'),stage=document.querySelector('.hero-stage');
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
let paused=reduced.matches,width=0,height=0,dpr=1,stars=[],tick=0,last=0,raf=0,visible=true,scrollProgress=0,travel=0;
let pointer={x:.5,y:.5},offset={x:0,y:0},ripples=[];
const clamp=(v,a=0,b=1)=>Math.max(a,Math.min(b,v));
function random(seed){let x=seed;return()=>{x=(x*1664525+1013904223)>>>0;return x/4294967296;};}
function readScroll(){const box=hero.getBoundingClientRect(),mobile=innerWidth<=640;scrollProgress=clamp(-box.top/(mobile?Math.max(1,box.height*.7):Math.max(1,box.height-stage.offsetHeight)));if(paused||!visible){journey();draw();}else run();}
function journey(){const p=paused?travel:scrollProgress;travel+=paused?0:(p-travel)*.12;if(Math.abs(p-travel)<.0001)travel=p;const copy=1-clamp((travel-.08)/.32),panel=clamp((travel-.38)/.3),seconds=tick*.001;hero.style.setProperty('--travel',travel.toFixed(4));hero.style.setProperty('--copy-alpha',copy.toFixed(4));hero.style.setProperty('--panel-alpha',panel.toFixed(4));hero.style.setProperty('--map-scale',(1+travel*.12).toFixed(4));hero.style.setProperty('--map-x',(-travel*24+Math.sin(seconds*.08)*2.5).toFixed(2)+'px');hero.style.setProperty('--map-y',(-travel*12+Math.sin(seconds*.06)*2).toFixed(2)+'px');hero.style.setProperty('--ambient-x',(Math.sin(seconds*.024)*9).toFixed(3)+'px');hero.style.setProperty('--ambient-y',(Math.sin(seconds*.018)*6).toFixed(3)+'px');hero.style.setProperty('--ambient-scale',(1+(1-Math.cos(seconds*.02))*.008).toFixed(6));for(let i=0;i<4;i++)hero.style.setProperty('--brain-signal-'+i,(.18+.82*Math.pow((1+Math.sin(seconds*1.35-i*1.5))*.5,4)).toFixed(3));hero.classList.toggle('map-visible',panel>.02);hero.classList.toggle('copy-hidden',copy<.05);}
function resize(){const rect=stage.getBoundingClientRect();width=rect.width;height=rect.height;dpr=Math.min(devicePixelRatio||1,1.8);canvas.width=Math.round(width*dpr);canvas.height=Math.round(height*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);const rnd=random(45813);stars=Array.from({length:Math.round(Math.min(620,width*.48))},()=>({x:rnd(),y:rnd(),r:.3+rnd()*1.05,a:.15+rnd()*.65,p:rnd()*6.28,z:.15+rnd()*.85,vx:.45+rnd()*.8,vy:-.15-rnd()*.35}));readScroll();draw();}
function draw(){ctx.clearRect(0,0,width,height);const time=tick*.00024,seconds=tick*.001;offset.x+=(paused?0:(pointer.x-.5)*14-offset.x)*.055;offset.y+=(paused?0:(pointer.y-.5)*9-offset.y)*.055;const nearby=[];
  // Depth-dependent drift continues at rest; wrap only outside the visible canvas.
  for(const s of stars){const zoom=1+travel*(.22+s.z*.5),depth=.5+s.z,baseX=((s.x*width+seconds*s.vx*depth+24)%(width+48))-24,baseY=(((s.y*height+seconds*s.vy*depth+24)%(height+48))+(height+48))%(height+48)-24,x=width*.65+(baseX-width*.65)*zoom+offset.x*s.z,y=height*.48+(baseY-height*.48)*zoom+offset.y*s.z;const dist=Math.hypot(x-pointer.x*width,y-pointer.y*height),alpha=s.a*(.78+.22*Math.sin(time+s.p));ctx.fillStyle=`rgba(226,237,244,${Math.min(.95,alpha+(dist<100?(1-dist/100)*.4:0))})`;ctx.beginPath();ctx.arc(x,y,s.r*(1+travel*s.z*.6),0,Math.PI*2);ctx.fill();if(dist<95)nearby.push([x,y]);if(s.r>1.22){ctx.strokeStyle=`rgba(213,231,244,${alpha*.28})`;ctx.lineWidth=.65;ctx.beginPath();ctx.moveTo(x-4,y);ctx.lineTo(x+4,y);ctx.moveTo(x,y-4);ctx.lineTo(x,y+4);ctx.stroke();}}
  for(let i=0;i<nearby.length;i++)for(let j=i+1;j<nearby.length;j++){const [x,y]=nearby[i],[u,v]=nearby[j],distance=Math.hypot(x-u,y-v);if(distance<72){ctx.strokeStyle=`rgba(205,227,238,${.18*(1-distance/72)})`;ctx.lineWidth=.65;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(u,v);ctx.stroke();}}
  ripples=ripples.filter(r=>tick-r.t<1600);for(const r of ripples){const f=(tick-r.t)/1600;ctx.strokeStyle=`rgba(230,242,248,${(1-f)*.4})`;ctx.lineWidth=.65;ctx.beginPath();ctx.arc(r.x,r.y,8+f*135,0,Math.PI*2);ctx.stroke();}
}
function frame(now){raf=0;if(paused||!visible||document.hidden)return;if(now-last>30){tick+=Math.min(50,now-last||32);last=now;journey();draw();}raf=requestAnimationFrame(frame);}
function run(){if(!raf&&!paused&&visible&&!document.hidden){last=performance.now();raf=requestAnimationFrame(frame);}}
function setMotionLabel(){const b=$('motionToggle');b.setAttribute('aria-pressed',String(paused));b.setAttribute('aria-label',tr(paused?'resumeMotion':'pauseMotion'));b.innerHTML=`<span aria-hidden="true">${paused?'▷':'Ⅱ'}</span>`;hero.classList.toggle('motion-paused',paused);}
function changeMotion(value){paused=value;setMotionLabel();if(paused){cancelAnimationFrame(raf);raf=0;journey();draw();}else run();}
$('motionToggle').onclick=()=>changeMotion(!paused);
reduced.addEventListener('change',e=>{if(e.matches)travel=0;changeMotion(e.matches);readScroll();});
stage.addEventListener('pointermove',e=>{const r=stage.getBoundingClientRect();pointer={x:clamp((e.clientX-r.left)/width),y:clamp((e.clientY-r.top)/height)};},{passive:true});
stage.addEventListener('pointerleave',()=>{pointer={x:.5,y:.5};},{passive:true});
stage.addEventListener('pointerdown',e=>{if(e.target.closest('a,button')||paused)return;const r=stage.getBoundingClientRect();ripples.push({x:e.clientX-r.left,y:e.clientY-r.top,t:tick});if(ripples.length>4)ripples.shift();});
window.addEventListener('scroll',readScroll,{passive:true});
new ResizeObserver(resize).observe(stage);
new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;if(visible){readScroll();run();}else{cancelAnimationFrame(raf);raf=0;}},{threshold:0}).observe(stage);
document.addEventListener('visibilitychange',()=>{if(document.hidden){cancelAnimationFrame(raf);raf=0;}else run();});
window.MemoryConstellation={update};resize();run();
})();
