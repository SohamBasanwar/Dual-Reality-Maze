import fs from 'node:fs/promises';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const nodes=new Map(),node=()=>({hidden:true,children:[],style:{setProperty(){},removeProperty(){}},classList:{add(){},remove(){},toggle(){}},setAttribute(){},addEventListener(){},append(){},prepend(){},replaceChildren(){},focus(){},getContext(){return {clearRect(){},drawImage(){},createImageData(w,h){return {data:new Uint8ClampedArray(w*h*4)}}}}});
const document={hidden:false,getElementById(id){if(!nodes.has(id))nodes.set(id,node());return nodes.get(id)},createElement:node,querySelector:node,addEventListener(){}};
const context={document,window:{addEventListener(){}},Image:class{},matchMedia:()=>({matches:false}),performance:{now:()=>context.now},now:100000,setTimeout:()=>0,clearTimeout(){},requestAnimationFrame(){},console};vm.createContext(context);
let script=(await fs.readFile(new URL('engine-rendered.mjs',import.meta.url),'utf8')).replaceAll('export ','')+'\nconst ASSETS={};';
for(const f of ['game-rendered.js','render-scene.js','architect-spirit.js','story/story.js','story/quests.js','story/title.js','story/voice.js','chapters/laboratory-level.js','chapters/campaign.js','chapters/laboratory-render.js','chapters/laboratory-intro.js','chapters/forest-level.js','chapters/forest.js','chapters/forest-render.js'])script+='\n'+await fs.readFile(new URL(f,import.meta.url),'utf8');
vm.runInContext(script,context);const run=s=>vm.runInContext(s,context);


run("loaded=true;story.ready=true;story.voice=false;state.mode='playing';forest.active=false;campaign.active=false;resetReveal(state)");
function checkPlan(kind){const data=run('revealPlan(revealContext())');assert(data,kind+' has route');for(let i=1;i<data.path.length;i++)assert.equal(Math.abs(data.path[i].x-data.path[i-1].x)+Math.abs(data.path[i].y-data.path[i-1].y),1);return data;}
function useLimit(owner){
 run('resetReveal('+owner+')');for(let i=1;i<=3;i++){context.now+=12000;assert.equal(run('reveal()'),true);assert.equal(run(owner+'.revealUsed'),i);assert.equal(run(owner+'.revealUntil'),context.now+3000);assert.equal(run(owner+'.revealReady'),context.now+12000);assert(run('activeReveal()'));const snap=run(owner+'.revealUntil');assert.equal(run('reveal()'),false);assert.equal(run(owner+'.revealUntil'),snap);assert.equal(run(owner+'.revealUsed'),i);context.now+=3000;assert.equal(run('activeReveal()'),null);if(i<3){assert.equal(run('reveal()'),false);assert.equal(run(owner+'.revealUsed'),i);}}
 context.now+=12000;assert.equal(run('reveal()'),false);assert.equal(run(owner+'.revealUsed'),3);
}
// Shortest floor route, rather than Euclidean proximity; sealed lock is excluded.
const first=checkPlan('Chapter I');assert(first.target.name.endsWith('rune'));assert(!first.path.some(p=>p.x===29&&p.y===15));assert(first.closed.length>0);
for(const p of first.path)assert(run('cells['+p.y+']['+p.x+']===1'));
run('resetReveal(state);reveal();state.runes=RUNES.map(r=>r.name+" rune"===state.guidance.target.name)');assert.notEqual(run('activeReveal().plan.target.name'),first.target.name,'Collected rune is no longer highlighted');
run('state.runes=[true,true,true]');assert.equal(checkPlan('Chapter I key').target.name,'Golden key');run('state.key=true');assert.equal(checkPlan('Chapter I exit').target.name,'Wormhole');useLimit('state');run('restart()');assert.equal(run('state.revealUsed'),0);
// Lab targets all remaining ingredients in path-distance order, then dragon.
run("campaign.active=true;state.mode='chapter2';labReset()");assert.equal(checkPlan('Chapter II').target.name,'Moonblossom');
run('resetReveal(campaign);reveal();campaign.ingredients[1]=true');assert.notEqual(run('activeReveal().plan.target.name'),'Moonblossom');
run('campaign.ingredients=[true,true,true]');assert.equal(checkPlan('Chapter II dragon').target.name,'Dragon’s roost');
for(const p of checkPlan('Chapter II floor').path)assert(run('laboratory.grid['+p.y+']['+p.x+']===1'));
useLimit('campaign');run('labReset()');assert.equal(run('campaign.revealUsed'),0);run("campaign.mode='paused'");assert.equal(run('reveal()'),false);assert.equal(run('campaign.revealUsed'),0);
// Forest permits R only in the offering. Fruit trees themselves are not floor.
run("campaign.active=false;forest.active=true;forest.ready=true;forestClearRound();forestBeginOffering()");assert.equal(checkPlan('Orchard').target.name,'Golden Moonpear');
for(let i=0;i<3;i++){run('forest.pears=[true,true,true];forest.pears['+i+']=false');const p=checkPlan('Tree '+i);const goal=p.path.at(-1);assert.equal(Math.abs(goal.x-p.target.x)+Math.abs(goal.y-p.target.y),1);assert(run('forestGrid()['+goal.y+']['+goal.x+']===1'));}
run('forest.pears=[true,true,true]');assert.equal(checkPlan('Orchard exit').target.name,'Orchard return');
useLimit('forest');run('forestFinishContact()');assert.equal(run('forest.revealUsed'),3,'Contact does not replenish hints');assert.equal(run('reveal()'),false);
run('forestClearRound();forestBeginOffering();forest.invulnerable=0;forest.player={...forestPlantPoint(forestPlants[0])};forest.visual={...forest.player};reveal();forestPlantCollision()');assert.equal(run('forest.revealUsed'),1);assert.equal(run('activeReveal()'),null);run('forestFinishContact()');assert.equal(run('forest.revealUsed'),1);
run('forestBeginHunt()');const budget=run('forest.revealUsed');assert.equal(run('reveal()'),false);assert.equal(run('activeReveal()'),null);assert.equal(run('forest.revealUsed'),budget);assert.equal(nodes.get('forestReveal').hidden,true);
run('forestClearRound();forestBeginOffering();voiceEngine.settingsOpen=true');assert.equal(run('reveal()'),false);assert.equal(run('forest.revealUsed'),0);run('voiceEngine.settingsOpen=false');
// Input routes use the chapter-specific budget. Holding R cannot spend repeats.
const event={key:'r',target:{tagName:'CANVAS'},preventDefault(){},stopImmediatePropagation(){},repeat:false};context.event=event;run('forestKey(event)');assert.equal(run('forest.revealUsed'),1);event.repeat=true;run('forestKey(event)');assert.equal(run('forest.revealUsed'),1);event.repeat=false;
run("forest.active=false;campaign.active=true;labReset();campaignKey(event)");assert.equal(run('campaign.revealUsed'),1);
// A disconnected or impossible objective never consumes a charge.
assert.equal(run('nearestRevealRoute([[1,0,1]],{x:0,y:0},[{x:2,y:0}])'),null);
console.log('PASS: nearest floor routes; remaining targets/key/exit/dragon; blocked passage markers; tree-adjacent picking goals; 3-second expiry; 12-second activation interval; three-use limit per chapter; cooldown/repeat/scene guards; reset isolation; no hunt reveal; contact preserves budget.');
