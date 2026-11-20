import fs from 'node:fs/promises';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const nodes=new Map();
const node=()=>({hidden:true,children:[],style:{setProperty(){},removeProperty(){}},classList:{add(){},remove(){},toggle(){}},replaceChildren(){},setAttribute(){},addEventListener(){},append(...items){this.children.push(...items)},prepend(){},focus(){},getContext(){return {clearRect(){},drawImage(){},createImageData(w,h){return {data:new Uint8ClampedArray(w*h*4)}}}}});
const document={hidden:false,getElementById(id){if(!nodes.has(id))nodes.set(id,node());return nodes.get(id)},createElement:node,querySelector:node,addEventListener(){}};
const context={document,window:{addEventListener(){}},matchMedia:()=>({matches:false}),Image:class{},performance:{now:()=>100000},setTimeout:()=>0,clearTimeout(){},requestAnimationFrame(){},console,Uint8ClampedArray};vm.createContext(context);
const read=f=>fs.readFile(new URL(f,import.meta.url),'utf8');
let script=(await read('engine-rendered.mjs')).replaceAll('export ','')+'\nconst ASSETS={};';
for(const file of ['game-rendered.js','render-scene.js','architect-spirit.js','story/story.js','story/quests.js','story/title.js','story/voice.js','chapters/laboratory-level.js','chapters/campaign.js','chapters/laboratory-render.js','chapters/laboratory-intro.js'])script+='\n'+await read(file);
vm.runInContext(script,context);const run=s=>vm.runInContext(s,context);
run('loaded=true;story.ready=true;story.voice=false;campaign.active=true;campaign.ready=true;state.mode="chapter2";images.labComic={width:1536,height:1024};images.dragonComic={width:1536,height:1024};labReset()');
assert.equal(run('laboratory.controls.length'),5);assert.equal(run('new Set(laboratory.controls.map(c=>c.x+","+c.y)).size'),5);
assert(run('laboratory.stations.every(s=>labRoute(laboratory.grid,LAB.start,s).length>0)'),'Every ingredient is reachable');
assert(run('labRoute(laboratory.grid,LAB.start,LAB.brew).length>0'));
const original=run('JSON.stringify({player:state.player,open:state.open,remaining:state.remaining})');
function power(index){if(run(`campaign.open[${index}]`))return;const open=run('campaign.open.map((v,i)=>v&&!labOnControl(campaign.player,laboratory.controls[i])?i:-1).filter(i=>i>=0)');for(const other of open)if(run('campaign.open.filter(Boolean).length')>=2)assert(run(`labToggle(${other},false)`),'Free a power slot');assert(run(`labToggle(${index},true)`));run('labUpdate(.41)');}
let moves=0;
function travel(goal){const path=run(`labRoute(laboratory.grid,campaign.player,${goal})`);assert(path.length>0);for(const point of path.slice(1)){const required=run(`laboratory.controls.findIndex(c=>labOnControl(${JSON.stringify(point)},c))`);if(required>=0)power(required);const from=run('({...campaign.player})');for(let j=0;j<4&&run('campaign.mode')==='playing';j++){assert(run(`labWalk(${point.x-from.x},${point.y-from.y})`));run('labUpdate(.073)');moves++;}}}
assert(run('laboratory.controls.every(c=>["gate","bridge"].includes(c.type))'));
assert(run('laboratory.stations.every(s=>!("control" in s))'),'Pickups have no power prerequisite');
assert.equal(run('LAB.tile'),run('TILE'));assert.equal(run('LAB.ox'),run('OX'));assert.equal(run('LAB.oy'),run('OY'));
assert.equal(run('CHAPTER_VIEW.step'),8);assert.equal(run('CHAPTER_VIEW.stepSeconds'),.072);
for(const i of [0,1,2]){travel(`laboratory.stations[${i}]`);assert.equal(run(`campaign.ingredients[${i}]`),true,'Walking onto an ingredient collects it without powering a station');}
assert.equal(run('campaign.mode'),'playing');assert(run('campaign.remaining<600'),'Playing and casting consume time');travel('LAB.roost');assert.equal(run('campaign.mode'),'ascent');
const held=run('campaign.remaining');
for(const mode of ['ascent','brewing','homeflight']){
 run(`campaign.mode='${mode}'`);
 assert.equal(run('labWalk(1,0)'),false);assert.equal(run('window.mazeArchitect.toggle()'),false);assert.equal(run('window.mazeArchitect.selectPotentiometer(1023)'),false);
 run('labUpdate(.2)');assert.equal(run('campaign.remaining'),held,'Flights and brewing pause the timer');
}
run("campaign.mode='ascent';campaign.phaseTime=18;labUpdate(.1);labUpdate(.31);labUpdate(.5)");assert.equal(run('campaign.panel'),3);
run('labNext();labNext();labUpdate(.2)');assert.equal(run('campaign.panel'),3,'Fade keeps old panel until dark');run('labUpdate(.2);labUpdate(.4)');assert.equal(run('campaign.mode'),'brewing');
run('labUpdate(7.1);labUpdate(.4);labUpdate(.4)');assert.equal(run('campaign.panel'),4);assert.equal(run('campaign.mode'),'comic');
run('labNext();labUpdate(.4);labUpdate(.4)');assert.equal(run('campaign.mode'),'homeflight');
run('labUpdate(17.1);labUpdate(.4);labUpdate(.4)');assert.equal(run('campaign.panel'),5);
for(const index of [6,7]){run('labNext();labUpdate(.4);labUpdate(.4)');assert.equal(run('campaign.panel'),index);}
run('labNext();labUpdate(.4);labUpdate(.4)');assert.equal(run('campaign.mode'),'preview');assert.equal(nodes.get('labChapterTitle').hidden,false);assert.equal(nodes.get('labOutcome').hidden,true);
assert.equal(run('campaign.remaining'),held,'Entire dragon/Alchemist/return sequence holds timer');
assert.equal(run('JSON.stringify({player:state.player,open:state.open,remaining:state.remaining})'),original,'Chapter II never mutates Chapter I progress');
run('labReset();campaign.remaining=.01;labUpdate(.05)');assert.equal(run('campaign.mode'),'lost');assert.equal(nodes.get('labStory').hidden,true);run('labNext();labForestPreview();labUpdate(20)');assert.equal(run('campaign.mode'),'lost','Timeout cannot advance to the forest');run('labReset()');assert.equal(run('campaign.remaining'),600);assert.equal(run('campaign.ingredients.some(Boolean)'),false);
run('labToggle(0,true);labToggle(1,true)');assert.equal(run('labToggle(2,true)'),false,'Two power slots enforced');
run('labReset();labToggle(3,true);labUpdate(.41);campaign.player={x:laboratory.controls[3].x,y:laboratory.controls[3].y};campaign.visual={...campaign.player}');assert.equal(run('labToggle(3,false)'),false,'Occupied passage stays open');
run('labReset();campaign.mode="paused"');assert.equal(run('window.mazeArchitect.toggle()'),false);const paused=run('campaign.remaining');run('labUpdate(4)');assert.equal(run('campaign.remaining'),paused);
run('campaign.mode="playing"');for(const [v,i] of [[0,0],[300,1],[512,2],[750,3],[1023,4]]){assert(run(`window.mazeArchitect.selectPotentiometer(${v})`));assert.equal(run('campaign.selected'),i);}
run('labShowComic(0);campaign.fade=null;campaign.pendingSpeech=null;campaign.panelRemaining=1;voiceEngine.busy=true;labUpdate(1.1)');assert.equal(run('campaign.fade'),null,'Comic waits for dialogue');run('voiceEngine.busy=false;labUpdate(.01)');assert(run('!!campaign.fade'));run('labUpdate(.4);labUpdate(.4)');assert.equal(run('campaign.panel'),1);
run('campaign.auto=false');const countdown=run('campaign.panelRemaining');run('labUpdate(5)');assert.equal(run('campaign.panelRemaining'),countdown);run('campaign.auto=true;document.hidden=true;labUpdate(5)');assert.equal(run('campaign.panelRemaining'),countdown);run('document.hidden=false;voiceEngine.settingsOpen=true;labUpdate(5)');assert.equal(run('campaign.panelRemaining'),countdown);
run('voiceEngine.settingsOpen=false;labShowComic(2);campaign.pendingSpeech=null;labNext();labUpdate(.4);labUpdate(.4)');assert.equal(run('campaign.mode'),'intro');assert.equal(nodes.get('labFade').hidden,true,'Entering the opening completes fade-in');run('labFinishIntro()');
run('leaveLaboratory()');assert.equal(run('campaign.active'),false);assert.equal(run('story.phase'),'title');assert.equal(nodes.get('campaign').hidden,true);
run(`var utterances=[];var speechSynthesis=window.speechSynthesis={getVoices:()=>[{name:'Microsoft George',lang:'en-GB',localService:true},{name:'Microsoft Mark',lang:'en-US',localService:true},{name:'Microsoft Zira',lang:'en-US',localService:true}],cancel(){},speak(u){utterances.push(u)}};var SpeechSynthesisUtterance=window.SpeechSynthesisUtterance=class{constructor(text){this.text=text}};refreshStoryVoices();story.voice=true;campaign.active=true;campaign.auto=false;campaign.fade=null;`);
for(let i=0;i<8;i++){run(`utterances=[];labShowComic(${i});labUpdate(.01)`);assert.equal(run('utterances.length'),1);assert.equal(run('utterances[0].text'),run(`labPanels[${i}].quote`));run('utterances[0].onend()');assert.equal(run('storySpeechActive()'),false,'No narrator follows chapter dialogue');}
run('labShowComic(3);labUpdate(.01)');assert.equal(run('utterances.at(-1).voice.name'),'Microsoft George','Alchemist gets the deep character voice');run('labNext()');assert.equal(run('storySpeechActive()'),false,'Manual transition cancels dialogue');
console.log(`PASS: Chapter II complete ingredient-to-dragon route (${moves} eight-pixel steps); free pickups and passage protection; live timer/paused ascent, brewing and return flights; eight-panel transitions; shared chapter title; timeout/replay isolation; controller routing; hidden-tab/settings/dialogue/auto-play pauses; Chapter I state isolation.`);
console.log('PASS: character-only dialogue for all eight Chapter II panels, Alchemist casting, and speech cancellation on transition.');

assert(run('laboratory.walls.length < LAB.cols*LAB.rows*.6'),'Irregular outside silhouette leaves open sky');
assert.equal(run('labRoute(laboratory.grid,LAB.start,LAB.roost,[laboratory.controls[4]]).length'),0,'Sky bridge is required to reach the dragon');
assert.equal(run('labRoute(laboratory.grid,LAB.start,laboratory.stations[2],Array.from({length:3},(_,i)=>({x:20+i,y:9}))).length'),0,'Bridge A spans the eastern terraces');
run('story.voice=false;labReset();campaign.player={...LAB.roost};labVisit()');assert.equal(run('campaign.mode'),'playing','Dragon requires all ingredients');
run("labStartFlight('ascent');campaign.fade=null;labReset();labUpdate(.1)");assert.equal(run('campaign.mode'),'playing','Restart cancels flight');assert(run('campaign.remaining<600'));
run("labStartFlight('homeflight');campaign.phaseTime=3;document.hidden=true;labUpdate(20)");assert.equal(run('campaign.phaseTime'),3,'Hidden tabs pause cinematics');run('document.hidden=false;leaveLaboratory();labUpdate(30)');assert.equal(run('campaign.active'),false);
console.log('PASS: irregular map, compulsory bridge/gate, premature boarding guard, cinematic restart and hidden-tab isolation.');

// Opening cinematic: all normal entry/replay paths preserve the Architect transformation.
run('campaign.active=true;story.voice=false;campaign.fade=null;labStartIntro()');
assert.equal(run('campaign.mode'),'intro');assert.equal(nodes.get('labIntro').hidden,false);
assert.equal(run('labWalk(1,0)'),false);assert.equal(run('window.mazeArchitect.toggle()'),false);assert.equal(run('window.mazeArchitect.selectPotentiometer(1023)'),false);
assert.equal(run('labIntroColor()'),0);assert.equal(run('CHAPTER_VIEW.spiritHeight'),84);
run('document.hidden=true;labUpdate(5)');assert.equal(run('campaign.intro.elapsed'),0);run('document.hidden=false;voiceEngine.settingsOpen=true;labUpdate(5)');assert.equal(run('campaign.intro.elapsed'),0);run('voiceEngine.settingsOpen=false');
const seen=[];let roars=0;for(let i=0;i<500&&run('campaign.mode')==='intro';i++){const key=run('labIntroShot().key');if(seen.at(-1)!==key)seen.push(key);run('labUpdate(.1)');if(run('campaign.intro!==null'))roars=run('campaign.intro.roars');assert.equal(run('campaign.remaining'),600);}
assert.deepEqual(seen,['arrival','overview','dragon','roar','wide','heroes','explorer','architect','merge','reveal']);assert.equal(roars,1);assert.equal(run('campaign.mode'),'playing');assert.equal(nodes.get('labIntro').hidden,true);
run('story.voice=true;labStartIntro();utterances=[];labEnterIntroShot(6)');assert.equal(run('utterances[0].text'),run('LAB_INTRO_SHOTS[6].text'));assert.equal(run('utterances[0].voice.name'),'Microsoft Mark');run('labUpdate(6)');assert.equal(run('campaign.intro.shot'),6,'Hold for Explorer speech');run('utterances[0].onend();labUpdate(.1)');assert.equal(run('campaign.intro.shot'),7);assert.equal(run('utterances.at(-1).voice.name'),'Microsoft George');run('labUpdate(6)');assert.equal(run('campaign.intro.shot'),7,'Hold for Architect speech');run('utterances.at(-1).onend();labUpdate(.1)');assert.equal(run('campaign.intro.shot'),8);run('labUpdate(2.4)');assert(run('labIntroColor()>0 && labIntroColor()<1'));
run('labFinishIntro()');assert.equal(run('storySpeechActive()'),false);assert.equal(run('campaign.remaining'),600);assert.equal(run('campaign.mode'),'playing');
run('story.voice=false;labStartIntro();labUpdate(1);labStartIntro()');assert.equal(run('campaign.intro.shot'),0);assert.equal(run('campaign.intro.elapsed'),0);run('leaveLaboratory()');assert.equal(nodes.get('labIntro').hidden,true);assert.equal(run('campaign.intro'),null);
console.log('PASS: ordered Chapter II entry, overview, dragon/one roar, return camera, two speech-aware dialogues, gray-to-awakened merge, shared 84px spirit; timer/input lock; hidden/settings pause; skip, restart and exit cleanup.');

run('campaign.active=true;story.voice=false;labStartIntro();labEnterIntroShot(7);voiceEngine.busy=true');for(let i=0;i<160;i++)run('labUpdate(.1)');assert.equal(run('labIntroShot().key'),'merge','Stalled speech has a bounded fallback');assert.equal(run('storySpeechActive()'),false);run('labEnterIntroShot(9);campaign.intro.elapsed=LAB_INTRO_SHOTS[9].duration');assert.equal(run('labIntroCamera().sx'),652);assert.equal(run('labIntroCamera().x'),652);assert.equal(run('labIntroCamera().z'),1);run('labFinishIntro();leaveLaboratory()');console.log('PASS: stalled-speech recovery and exact final gameplay camera (no duplicate-world blend).');

// Regression: never expose the maze before Chapter II comic, including slow loads and cached visits.
run("leaveLaboratory();story.voice=false;campaign.ready=false;var savedLoad=loadImage,savedArt=initLaboratoryArt;var pendingArt=[];loadImage=()=>new Promise((resolve,reject)=>pendingArt.push({resolve,reject}));initLaboratoryArt=()=>{};");
const cold=run('openLaboratory()');
assert.equal(run('campaign.mode'),'loading');assert.equal(nodes.get('labLoading').hidden,false);assert.equal(nodes.get('labFade').hidden,false);assert.equal(nodes.get('labFade').style.opacity,'1');assert.equal(nodes.get('labStory').hidden,true);
const loadingTime=run('campaign.remaining');run('labUpdate(5)');assert.equal(run('campaign.remaining'),loadingTime);assert.equal(nodes.get('labFade').hidden,false);assert.equal(run('labWalk(1,0)'),false);
run('pendingArt.forEach(p=>p.resolve({width:1536,height:1024}))');await cold;
assert.equal(run('campaign.mode'),'comic');assert.equal(run('campaign.panel'),0);assert.equal(nodes.get('labStory').hidden,false);assert.equal(nodes.get('labLoading').hidden,true);assert.equal(nodes.get('labFade').style.opacity,'1');run('labUpdate(.5)');assert.equal(nodes.get('labFade').hidden,true);
run('leaveLaboratory()');await run('openLaboratory()');assert.equal(run('campaign.panel'),0);assert.equal(nodes.get('labFade').hidden,false);assert.equal(nodes.get('labFade').style.opacity,'1');assert.equal(nodes.get('labStory').hidden,false);
run('leaveLaboratory();campaign.ready=false;pendingArt=[]');const cancelled=run('openLaboratory()');run('leaveLaboratory();pendingArt.forEach(p=>p.resolve({width:1536,height:1024}))');await cancelled;assert.equal(run('campaign.active'),false);assert.equal(run('campaign.ready'),false);assert.equal(nodes.get('labLoading').hidden,true);
run('pendingArt=[]');const failed=run('openLaboratory()');run('var savedError=console.error;console.error=()=>{};pendingArt[0].reject(Error("fixture load failure"))');await failed;run('console.error=savedError');assert.equal(run('campaign.mode'),'error');assert.equal(nodes.get('labLoading').hidden,false);assert(nodes.get('labLoadingText').textContent.includes('could not load'));assert.equal(run('labWalk(1,0)'),false);run('leaveLaboratory();loadImage=savedLoad;initLaboratoryArt=savedArt');
run('campaign.active=true;campaign.ready=true;ASSETS.labDefeat="fixture-bad-ending";story.voice=true;labReset();campaign.remaining=.01;utterances=[];labUpdate(.05)');
assert.equal(run('campaign.mode'),'lost');assert.equal(nodes.get('labDefeatArt').src,'fixture-bad-ending');assert.equal(nodes.get('labOutcomeTitle').textContent,'The Eternal Slumber');assert(nodes.get('labOutcomeText').textContent.includes('sleeps forever'));assert.equal(run('utterances.length'),1);assert(run('utterances[0].text.includes("I will not lose you")'));
run('labNext();labForestPreview();labUpdate(60)');assert.equal(run('campaign.mode'),'lost');assert.equal(nodes.get('labChapterTitle').hidden,true);assert.equal(nodes.get('labStory').hidden,true);assert.equal(run('labToggle(0)'),false);
run("$('labRetry').onclick()");assert.equal(run('campaign.mode'),'intro');assert.equal(run('campaign.remaining'),600);assert.equal(nodes.get('labOutcome').hidden,true);assert.equal(run('storySpeechActive()'),false);run('leaveLaboratory()');
console.log('PASS: covered cold/cached Chapter II entry, delayed assets, cancellation and failed loading; single bad-ending art and King-only speech; no success continuation; replay resets into opening.');
