import fs from 'node:fs/promises';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import {START,KEY,EXIT,RUNES,ELEMENTS,inside,route,walkable} from './engine-rendered.mjs';
const root=import.meta.dirname;
const nodes=new Map();
const node=()=>({hidden:true,children:[],style:{setProperty(){}},classList:{add(){},remove(){},toggle(){}},setAttribute(){},addEventListener(){},append(v){this.children.push(v)},focus(){},getContext(){return {imageSmoothingEnabled:false,createImageData(w,h){return {data:new Uint8ClampedArray(w*h*4)}}}}});
const document={getElementById(id){if(!nodes.has(id))nodes.set(id,node());return nodes.get(id)},createElement:node,addEventListener(){}};
const context={document,window:{addEventListener(){}},matchMedia:()=>({matches:false}),Image:class{},performance:{now:()=>context.now},now:100000,setTimeout:()=>0,clearTimeout(){},requestAnimationFrame(){},console,Uint8ClampedArray};
vm.createContext(context);
const code=(await fs.readFile(root+'/engine-rendered.mjs','utf8')).replaceAll('export ','')+'\nconst ASSETS={};\n'+await fs.readFile(root+'/game-rendered.js','utf8')+'\n'+await fs.readFile(root+'/render-scene.js','utf8')+'\n'+await fs.readFile(root+'/architect-spirit.js','utf8');
vm.runInContext(code,context);
const run=s=>vm.runInContext(s,context);
run('loaded=true; restart()');
assert.equal(run('setElement(0,true)'),true);
assert.equal(run('effectiveOpen()[0]'),false,'Gate opening must not instantly allow collision');
run('animation.elements[0]=1');
assert.equal(run('effectiveOpen()[0]'),true);
assert.equal(run('setElement(1,true)'),true);
assert.equal(run('setElement(2,true)'),false,'Cannot exceed two powered controls');
run('setElement(1,false); setElement(3,true); animation.elements[3]=1; state.player={x:ELEMENTS[3].rect[0]+12,y:ELEMENTS[3].rect[1]+12};state.visual={...state.player}');
assert.equal(run('setElement(3,false)'),false,'Occupied bridge cannot retract');
run('restart()');
let moves=0,switches=0;
function travel(target){
 const from=JSON.parse(run('JSON.stringify(state.player)'));
 const path=route(from,target,[true,true,true,true,true],target===EXIT);
 assert.ok(path.length,'Every challenge objective must be reachable');
 for(const next of path){
  const required=ELEMENTS.findIndex(e=>inside(next.x,next.y,e.barrier));
  if(required>=0&&!run(`state.open[${required}]`)){
   if(run('state.open.filter(Boolean).length')>=2){
    const here=JSON.parse(run('JSON.stringify(state.player)'));
    const active=JSON.parse(run('JSON.stringify(state.open)'));
    const close=active.findIndex((v,i)=>v&&!inside(here.x,here.y,ELEMENTS[i].barrier));
    assert.ok(close>=0,'Two-slot puzzle must permit a safe switch');
    assert.equal(run(`setElement(${close},false)`),true);switches++;
   }
   assert.equal(run(`setElement(${required},true)`),true);switches++;
   run(`animation.elements[${required}]=1`);
  }
  const p=JSON.parse(run('JSON.stringify(state.player)'));
  assert.equal(run(`step(${(next.x-p.x)/8},${(next.y-p.y)/8})`),true,'Solution cannot walk through a sealed gate or wall');
  run('state.visual={...state.player}');moves++;
  if(target===EXIT&&run('state.mode')==='won')break;
 }
}
travel(KEY);assert.equal(run('state.key'),false,'Key must remain locked before all three runes');
for(const r of RUNES)travel(r);
assert.equal(run('state.runes.every(Boolean)'),true);
travel(KEY);assert.equal(run('state.key'),true);
travel(EXIT);assert.equal(run('state.mode'),'won','Full playthrough must end in victory');
run('restart(); reveal()');const ready=run('state.revealReady');context.now+=1000;run('reveal()');assert.equal(run('state.revealReady'),ready,'Reveal cooldown must be enforced');context.now+=12000;run('reveal()');assert.ok(run('state.revealReady')>ready);
run('renderScene=()=>{};render(1000)');const remaining=run('state.remaining');run('pause();render(1100)');assert.equal(run('state.remaining'),remaining,'Pause must stop timer');run('pause();state.remaining=.01;render(1200)');assert.equal(run('state.mode'),'lost');
run('restart()');assert.equal(run('state.runes.filter(Boolean).length'),0);assert.equal(run('state.open.filter(Boolean).length'),0);assert.equal(run('state.key'),false);
assert.equal(walkable(10,10,[true,true,true,true,true],true),false);
console.log(`PASS: complete three-rune + key + escape playthrough (${moves} steps, ${switches} power switches); two-slot limit; animated collision threshold; occupied bridge safety; reveal cooldown; pause; timeout; restart; world bounds.`);

run('restart();renderScene=()=>{};previous=0');
const beforeSelection=run('JSON.stringify(state.open)');
assert.equal(run('window.mazeArchitect.select(4)'),true);
assert.equal(run('JSON.stringify(state.open)'),beforeSelection,'Selection must never toggle a passage');
run('updateArchitectSpirit(.1)');const mid=run('architectSpirit.x');
assert.equal(run('window.mazeArchitect.select(2)'),true);assert.equal(run('architectSpirit.fromX'),mid,'Rapid selections begin at the current spirit position');
run('updateArchitectSpirit(.28)');assert.equal(run('architectSpirit.x'),run('spiritAnchor(2).x'));assert.equal(run('architectSpirit.y'),run('spiritAnchor(2).y'));
for(const [reading,index] of [[0,0],[300,1],[512,2],[750,3],[1023,4]]){
 assert.equal(run(`window.mazeArchitect.selectPotentiometer(${reading})`),true);assert.equal(run('state.selected'),index);
}
run('window.mazeArchitect.selectPotentiometer(0);window.mazeArchitect.selectPotentiometer(207)');assert.equal(run('state.selected'),0,'Dial jitter near the boundary keeps the selection stable');
run('window.mazeArchitect.selectPotentiometer(230)');assert.equal(run('state.selected'),1);
for(const invalid of ['NaN','Infinity','-1','1024'])assert.equal(run(`window.mazeArchitect.selectPotentiometer(${invalid})`),false);
for(const invalid of ['-1','5','.5','NaN'])assert.equal(run(`window.mazeArchitect.select(${invalid})`),false);
assert.equal(run('window.mazeArchitect.selectPotentiometer(4095,4095)'),true);assert.equal(run('state.selected'),4);
run('restart();setElement(0,true)');assert.equal(run('architectSpirit.pulses[0].blocked'),false);
const timerBefore=run('state.remaining');for(let t=50;t<=400;t+=50)run(`render(${t})`);
assert.equal(run('state.mode'),'playing');assert(run('state.remaining')<timerBefore-.35,'Casting never pauses the game timer');assert.equal(run('architectSpirit.pulses.length'),0,'Cast ends within 400ms');
run('setElement(1,true)');assert.equal(run('setElement(2,true)'),false);assert.equal(run('state.selected'),2,'A blocked action still identifies the targeted gate');assert.equal(run('architectSpirit.pulses.at(-1).blocked'),true);assert.equal(run('state.open.filter(Boolean).length'),2);
for(const mode of ['paused','intro','ritual','finale','epilogue','lost','complete']){
 run(`state.mode='${mode}'`);const saved=run('JSON.stringify({selected:state.selected,open:state.open})');
 assert.equal(run('window.mazeArchitect.selectPotentiometer(0)'),false);assert.equal(run('window.mazeArchitect.toggle()'),false);
 assert.equal(run('JSON.stringify({selected:state.selected,open:state.open})'),saved,'Controller cannot change a locked scene');
}
run('restart()');assert.equal(run('architectSpirit.pulses.length'),0);assert.equal(run('architectSpirit.selected'),0);assert.equal(run('architectSpirit.travel'),1);
console.log('PASS: spirit travel and rapid retargeting; selection without toggling; all potentiometer bands, jitter and invalid readings; 360ms casting with live timer; blocked controls and scene guards; restart cleanup.');
