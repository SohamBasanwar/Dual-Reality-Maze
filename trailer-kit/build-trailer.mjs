// Export staged shots using the game's unmodified canvas renderers and source art.
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import vm from 'node:vm';
import {createRequire} from 'node:module';
import {spawn,execFileSync} from 'node:child_process';
import {once} from 'node:events';
const root=path.resolve(import.meta.dirname,'..');
process.chdir(root);
const out=import.meta.dirname;
const require=createRequire(import.meta.url);
const deps=path.join(os.homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies');
const {createCanvas,loadImage}=require(path.join(deps,'node/node_modules/@napi-rs/canvas'));
let binDir=path.join(os.tmpdir(),'maze-trailer-tools/imageio_ffmpeg/binaries');
try{await fs.access(binDir);}catch{binDir=path.join(os.homedir(),'AppData/Local/Temp/maze-trailer-tools/imageio_ffmpeg/binaries');}
const ffmpeg=process.env.MAZE_FFMPEG||path.join(binDir,(await fs.readdir(binDir)).find(n=>n.endsWith('.exe')));
const W=1920,H=1080,FPS=24;
for(const folder of ['clips','stills'])await fs.mkdir(path.join(out,folder),{recursive:true});
const nodes=new Map();
const stub=()=>({hidden:true,children:[],style:{setProperty(){},removeProperty(){}},classList:{add(){},remove(){},toggle(){}},setAttribute(){},addEventListener(){},append(...v){this.children.push(...v)},prepend(){},replaceChildren(){},focus(){}});
const canvas=(w=1672,h=941)=>Object.assign(createCanvas(w,h),stub());
const document={hidden:false,getElementById(id){if(!nodes.has(id))nodes.set(id,['world','labCanvas','labComic','forestCanvas','forestComic'].includes(id)?canvas():stub());return nodes.get(id)},createElement:tag=>tag==='canvas'?canvas():stub(),querySelector:stub,addEventListener(){}};
const actual={};
const assets={atlas:'atlas.png',hero:'explorer.png',spirit:'architect-spirit.png',cast:'story-cast.png',labAtlas:'laboratory-atlas.png',labComic:'chapter2-comic.png',dragonComic:'chapter2-dragon-comic.png',dragon:'emerald-dragon.png',dragonFlight:'emerald-dragon-flight.png',dragonRoar:'emerald-dragon-roar.png',kingdom:'kingdom-homecoming.png',forestCast:'forest-cast.png',forestAtlas:'forest-atlas.png',forestPrologue:'chapter3-prologue.png',forestEpilogue:'chapter3-epilogue-robes-v2.png',forestDefeat:'chapter3-lost-to-forest.png',forestDragon:'emerald-dragon-unmounted.png',dryadAnimation:'dryad-animation-v2.png',memoryAnimation:'memory-animation-v2.png',orchardAtlas:'forest-orchard-v2.png',forestHeroes:'forest-heroes-v2.png',forestRowan:'forest-rowan-v2.png',forestRevisionComic:'forest-revision-comic-v2.png',forestRevisionAfter:'forest-revision-after-v2.png',forestMessenger:'forest-messenger-v3.png',dryadTalk:'dryad-talk-v3.png',architectWaiting:'architect-waiting-v4.png',guardianContact:'guardian-contact-v4.png',forestHeartTree:'forest-heart-tree-v1.png',title:'title-screen.png'};
for(const [key,file]of Object.entries(assets))actual[key]=await loadImage(path.join(root,'images',file));
const context={document,window:{addEventListener(){}},Image:class{},matchMedia:()=>({matches:false}),performance:{now:()=>100000},setTimeout:()=>0,clearTimeout(){},requestAnimationFrame(){},console,actual};
vm.createContext(context);
let script=(await fs.readFile('maze-source/work/engine-rendered.mjs','utf8')).replaceAll('export ','')+'\nconst ASSETS={};';
for(const f of ['game-rendered.js','render-scene.js','architect-spirit.js','story/story.js','story/quests.js','story/title.js','story/voice.js','chapters/laboratory-level.js','chapters/campaign.js','chapters/laboratory-render.js','chapters/laboratory-intro.js','chapters/forest-level.js','chapters/forest.js','chapters/forest-render.js'])script+='\n'+await fs.readFile('maze-source/work/'+f,'utf8');
vm.runInContext(script,context);
const run=s=>vm.runInContext(s,context);
run('Object.assign(images,actual);initScene();initArchitectSpiritArt();heroBounds=labTrimSheet(images.hero,1,1)[0];story.cast=labTrimSheet(images.cast,2,2);story.voice=false;loaded=true;initLaboratoryArt();campaign.active=true;campaign.ready=true;campaign.roarSound=false;labReset();forest.active=true;forest.ready=true;initForestArt();forestClearRound();');
const shots=[
 {id:'01_maze_and_architect',duration:5,source:'Chapter I game renderer; staged Gate A activation',caption:'TWO HEROES. ONE PATH.',setup:"if(cinematic)cinematic.active=false;state.mode='playing';state.selected=0;state.open=[true,false,false,false,false];state.revealUntil=0;animation.elements=[0,0,0,0,0];moveArchitectSpirit(0);",frame:t=>`animation.time=${t*1000};animation.elements[0]=Math.min(1,${t}*1.9);state.remaining=600-${t};updateArchitectSpirit(1/24);renderScene(${t*1000});`,canvas:'world'},
 {id:'02_architect_transformation',duration:4.8,source:'Chapter II opening, merge shot',caption:'BECOME THE WAY FORWARD.',setup:'labStartIntro();labEnterIntroShot(8);',frame:t=>`campaign.clock=${t};campaign.intro.elapsed=${t};drawLaboratory();`,canvas:'labCanvas'},
 {id:'03_emerald_guardian',duration:2.6,source:'Chapter II opening, dragon roar shot',caption:'AWAKEN AN ANCIENT ALLY.',setup:'labStartIntro();labEnterIntroShot(3);',frame:t=>`campaign.clock=${t};campaign.intro.elapsed=${t};drawLaboratory();`,canvas:'labCanvas'},
 {id:'04_dragon_flight',duration:5,source:'Chapter II ascent, sky flight from 7 to 12 seconds',caption:'RISE ABOVE THE SHATTERED GARDENS.',setup:"labReset();campaign.mode='ascent';campaign.ingredients=[true,true,true];",frame:t=>`campaign.clock=${t+7};campaign.phaseTime=${t+7};drawLaboratory();`,canvas:'labCanvas'},
 {id:'05_heart_tree_and_dryad',duration:3.5,source:'Chapter III introduction, Dryad dialogue shot',caption:'ENTER A FOREST THAT REMEMBERS.',setup:"forestClearRound();forestStartSequence('intro');forestEnterShot(4);",frame:t=>`forest.clock=${t};forest.shotTime=${t};drawForest();`,canvas:'forestCanvas'},
 {id:'06_memory_in_the_jar',duration:3.6,source:'Chapter III capture, jarOpen and jarEnter shots',caption:'BRING HER MEMORIES HOME.',setup:"forestClearRound();forestBeginHunt();forest.player={x:33.5,y:9};forest.visual={...forest.player};forestStartSequence('capture');forestEnterShot(2);",frame:t=>`forest.clock=${t};forest.shot=${t<1.2?2:3};forest.shotTime=${t<1.2?t:t-1.2};drawForest();`,canvas:'forestCanvas'},
 {id:'07_home_on_emerald_wings',duration:5,source:'Chapter III homeflight cinematic',caption:'A PROMISE CARRIED HOME.',setup:"forestClearRound();forestBeginHunt();forestStartSequence('homeflight');",frame:t=>`forest.clock=${t};forest.shotTime=${t};drawForest();`,canvas:'forestCanvas'},
 {id:'08_title_end_card',duration:4,source:'Existing title-screen.png, editorial slow zoom and typography',caption:'',setup:'',frame:()=>'',canvas:null}
];
const clean=createCanvas(W,H),g=clean.getContext('2d');
const edit=createCanvas(W,H),eg=edit.getContext('2d');
function text(c,str,x,y,size,color='#f8e9c8',align='center'){
 c.save();c.font=`bold ${size}px Georgia`;c.textAlign=align;c.fillStyle=color;c.shadowColor='#000';c.shadowBlur=14;c.shadowOffsetY=3;c.fillText(str,x,y);c.restore();
}
function titleCard(t){
 const z=1.015+t*.007;g.drawImage(actual.title,(W-W*z)/2,(H-H*z)/2,W*z,H*z);
 const shade=g.createLinearGradient(0,0,W,0);shade.addColorStop(0,'#03081cf5');shade.addColorStop(.55,'#03081c99');shade.addColorStop(1,'#03081c00');g.fillStyle=shade;g.fillRect(0,0,W,H);
 text(g,'DUAL-REALITY',115,360,88,'#fff1cc','left');text(g,'MAZE',115,467,116,'#fff1cc','left');
 g.fillStyle='#d7b96a';g.fillRect(119,515,535,3);text(g,'THE ARCHITECT’S OATH',120,570,37,'#d8c39a','left');
 text(g,'Two heroes. One path.',120,680,38,'#e3e9f5','left');text(g,'A fantasy puzzle adventure',120,917,29,'#d4dbea','left');
}
function makeEncoder(file){
 const p=spawn(ffmpeg,['-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgba','-s',`${W}x${H}`,'-r',String(FPS),'-i','pipe:0','-an','-c:v','libx264','-preset','veryfast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',file],{windowsHide:true});
 let error='';p.stderr.on('data',d=>error+=d);const done=new Promise((resolve,reject)=>{p.on('error',reject);p.on('exit',c=>c===0?resolve():reject(Error(error||`Encoder exit ${c}`)));});p.stdin.on('error',()=>{});return{p,done};
}
async function put(encoder,c){const b=c.getContext('2d').getImageData(0,0,W,H).data;if(!encoder.p.stdin.write(Buffer.from(b.buffer,b.byteOffset,b.byteLength)))await once(encoder.p.stdin,'drain');}
const draft=makeEncoder(path.join(out,'trailer-visuals.mp4'));
let cursor=0;const manifest=[];const thumbnails=[];
for(const shot of shots){
 run(shot.setup);const clip=makeEncoder(path.join(out,'clips',shot.id+'.mp4'));let first,changed=false;
 const count=Math.round(shot.duration*FPS),saveAt=Math.floor(count*.52);
 for(let i=0;i<count;i++){
  const t=i/FPS;run(shot.frame(t));g.clearRect(0,0,W,H);
  if(shot.canvas)g.drawImage(nodes.get(shot.canvas),0,0,W,H);else titleCard(t);
  if(i===0)first=clean.toBuffer('image/png');
  if(i===saveAt){const png=clean.toBuffer('image/png');changed=!first.equals(png);await fs.writeFile(path.join(out,'stills',shot.id+'.png'),png);thumbnails.push({id:shot.id,img:await loadImage(png)});}
  await put(clip,clean);eg.drawImage(clean,0,0);
  if(shot.caption){const grad=eg.createLinearGradient(0,790,0,H);grad.addColorStop(0,'#02081600');grad.addColorStop(1,'#020816ee');eg.fillStyle=grad;eg.fillRect(0,790,W,290);eg.globalAlpha=Math.min(1,t/.25);text(eg,shot.caption,W/2,996,42);eg.globalAlpha=1;}
  // Gentle fades apply to the assembled draft only. Source clips stay clean.
  const fade=Math.max(0,1-t/.18,1-(count-1-i)/FPS/.18);if(fade>0){eg.fillStyle=`rgba(0,0,0,${Math.min(1,fade)})`;eg.fillRect(0,0,W,H);}
  await put(draft,edit);
 }
 clip.p.stdin.end();await clip.done;
 if(!changed)throw Error('No animation in '+shot.id);
 manifest.push({...shot,setup:undefined,frame:undefined,canvas:undefined,start:cursor,duration:count/FPS,width:W,height:H,fps:FPS,animated:true,clip:'clips/'+shot.id+'.mp4',still:'stills/'+shot.id+'.png'});cursor+=count/FPS;
 console.log(`Exported ${shot.id} (${count/FPS}s); animation verified`);
}
draft.p.stdin.end();await draft.done;
// Original synthesized temporary score; no downloaded music or cloned voices.
const SR=44100,n=Math.ceil(cursor*SR),wave=Buffer.alloc(44+n*4);wave.write('RIFF');wave.writeUInt32LE(36+n*4,4);wave.write('WAVEfmt ',8);wave.writeUInt32LE(16,16);wave.writeUInt16LE(1,20);wave.writeUInt16LE(2,22);wave.writeUInt32LE(SR,24);wave.writeUInt32LE(SR*4,28);wave.writeUInt16LE(4,32);wave.writeUInt16LE(16,34);wave.write('data',36);wave.writeUInt32LE(n*4,40);
const chords=[[146.83,220,293.66,349.23],[116.54,174.61,233.08,293.66],[130.81,196,261.63,329.63],[110,164.81,220,293.66]];
for(let i=0;i<n;i++){const t=i/SR,bar=Math.floor(t/4),phase=(t%4)/4,chord=chords[bar%4];let a=0;
 for(let k=0;k<4;k++)a+=Math.sin(t*Math.PI*2*chord[k]+Math.sin(t*.4+k)*.2)*(.026+Math.sin(Math.PI*phase)*.008);
 const beat=t%(.5),bell=chord[Math.floor(t*2)%4]*4;a+=Math.sin(2*Math.PI*bell*t)*Math.exp(-beat*11)*.025;
 a*=Math.min(1,t/2,(cursor-t)/2)*.67;const v=Math.round(Math.max(-.9,Math.min(.9,a))*32767);wave.writeInt16LE(v,44+i*4);wave.writeInt16LE(v,46+i*4);
}
await fs.writeFile(path.join(out,'temporary-score.wav'),wave);
execFileSync(ffmpeg,['-hide_banner','-loglevel','error','-y','-i',path.join(out,'trailer-visuals.mp4'),'-i',path.join(out,'temporary-score.wav'),'-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',path.join(out,'Dual_Reality_Maze_Trailer_Draft.mp4')],{windowsHide:true});
await fs.unlink(path.join(out,'trailer-visuals.mp4'));
const board=createCanvas(1600,2020),bg=board.getContext('2d');bg.fillStyle='#080e1b';bg.fillRect(0,0,1600,2020);text(bg,'DUAL-REALITY MAZE · TRAILER SHOTS',48,60,31,'#f4e2b6','left');
for(let i=0;i<thumbnails.length;i++){const x=40+(i%2)*780,y=95+Math.floor(i/2)*475;bg.drawImage(thumbnails[i].img,x,y,740,416.25);text(bg,thumbnails[i].id.replaceAll('_',' '),x,y+448,19,'#dce5f3','left');}
await fs.writeFile(path.join(out,'Trailer_Contact_Sheet.jpg'),board.toBuffer('image/jpeg'));
await fs.writeFile(path.join(out,'shot-manifest.json'),JSON.stringify({captureMethod:'Deterministic staged shots from unmodified game canvas renderers. Not a recorded player session. Title card uses existing game artwork with editorial typography and zoom. Snippets have no audio. Draft has an original synthesized temporary score and no voiceover.',duration:cursor,shots:manifest},null,2));
console.log(`DONE: ${manifest.length} clips, ${cursor.toFixed(2)}s trailer, stills and contact sheet.`);
