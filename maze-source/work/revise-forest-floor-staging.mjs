import fs from 'node:fs/promises';
const dir='maze-source/work/';async function edit(f,fn){await fs.writeFile(dir+f,fn(await fs.readFile(dir+f,'utf8')));}
await edit('chapters/forest-level.js',s=>s.replace('dryad:{x:9,y:19},','dryad:{x:9,y:19},waiting:{x:7,y:19},')+`
// Cinematic feet use reachable floor cells, never guessed pixel offsets or passages.
function forestStagePositions(player){const grid=memoryForest.grid,start={x:Math.round(player.x),y:Math.round(player.y)},seen=new Set([start.x+','+start.y]),queue=[{...start,steps:0}],candidates=[];
 for(let n=0;n<queue.length;n++){const p=queue[n];if(!memoryForest.controls.some(c=>labOnControl(p,c)))candidates.push(p);if(p.steps>=18)continue;for(const [dx,dy] of [[-1,0],[1,0],[0,-1],[0,1]]){const v={x:p.x+dx,y:p.y+dy,steps:p.steps+1},key=v.x+','+v.y;if(seen.has(key)||!grid[v.y]?.[v.x]||memoryForest.controls.some((c,i)=>labOnControl(v,c)&&(!forest.open[i]||forest.progress[i]<.97)))continue;seen.add(key);queue.push(v);}}
 const clear=(a,b)=>Math.abs(a.x-b.x)*32>=84||Math.abs(a.y-b.y)*32>=108;
 let best=null,score=Infinity;for(const a of candidates){if(!clear(a,player))continue;for(const d of candidates){if(!clear(d,player)||!clear(a,d))continue;const cost=Math.hypot(a.x-player.x,a.y-player.y)+Math.hypot(d.x-player.x,d.y-player.y)+.1*(a.steps+d.steps)+(a.x>player.x?.2:0)+(d.x<player.x?.2:0);if(cost<score){score=cost;best={architect:{x:a.x,y:a.y},dryad:{x:d.x,y:d.y}};}}}
 if(!best)throw new Error('No safe cinematic floor staging near memory grove');return best;
}
function forestWaitingVisible(){return forest.area==='forest'&&['path','offeringReturn'].includes(forest.mode==='paused'?forest.resumeMode:forest.mode);}
`);
await edit('chapters/forest.js',s=>{
 s=s.replaceAll('capturePoint:null,','capturePoint:null,stage:null,contact:null,');s=s.replace("key:'summon',duration:3.8","key:'summon',duration:6.5");
 s=s.replace('The Dryad opens the southern wall','The Architect waits beside the Heart Tree while Rowan explores alone. The Dryad opens the southern wall');
 s=s.replace("'forestMessenger','dryadTalk'];","'forestMessenger','dryadTalk','architectWaiting','guardianContact'];");
 s=s.replace("function forestStartSequence(name){stopStorySpeech();","function forestStartSequence(name){if(['capture','summon','arrival'].includes(name)&&!forest.stage)forest.stage=forestStagePositions(forest.player);stopStorySpeech();");
 const a=s.indexOf('function forestPlantCollision()'),b=s.indexOf('\nfunction ',a+1);
 s=s.slice(0,a)+`function forestPlantCollision(){if(forest.area!=='orchard'||forest.mode!=='offering'||forest.invulnerable>0)return false;for(const [i,m] of forestPlants.entries()){const p=forestPlantPoint(m);if([forest.player,forest.visual].some(v=>Math.abs(p.x-v.x)*32<=42&&Math.abs(p.y-v.y)*32<=50)){forest.mode='orchardHit';forest.contact={index:i,point:{...p},elapsed:0};forest.keys.clear();forest.path=[];forest.pears=[false,false,false];forest.pickFlash=0;forest.move=0;forestUI();forestMessage('Caught by a guardian! All three fruits return to their trees. Rowan must start again.');note(170,.2);return true;}}return false;}
function forestFinishContact(){forest.player={x:3,y:19};forest.visual={...forest.player};forest.contact=null;forest.mode='offering';forest.invulnerable=1.5;forestMessage('Back at the orchard entrance. Collect all three fruits again; give the guardians room.');forestUI();}
`+s.slice(b);
 s=s.replace("const film=!['path','offering','offeringReturn','hunt','paused']","const film=!['path','offering','orchardHit','offeringReturn','hunt','paused']").replace("const offer=['path','offering','offeringReturn']","const offer=['path','offering','orchardHit','offeringReturn']");
 s=s.replace(" if(!forestCanMove())return;"," if(forest.mode==='orchardHit'){forest.contact.elapsed+=dt;if(forest.contact.elapsed>=.85)forestFinishContact();return;}\n if(!forestCanMove())return;");
 s=s.replace('forestPlantCollision();forest.cast=', 'if(forestPlantCollision())return;forest.cast=');
 s=s.replace('forest.ghost.y+=(target.y-forest.ghost.y)*p;forestVisit();','forest.ghost.y+=(target.y-forest.ghost.y)*p;if(forestPlantCollision())return;forestVisit();');
 return s;
});
await edit('chapters/forest-render.js',s=>{
 s=s.replace('function initForestArt(){','function initForestArt(){forest.waitingFrame=labTrimSheet(images.architectWaiting,1,1)[0];forest.guardianFrames=labTrimSheet(images.guardianContact,4,1);');
 const a=s.indexOf(' for(const m of forestPlants){'),b=s.indexOf('\n const e=',a);
 s=s.slice(0,a)+` for(const [i,m] of forestPlants.entries()){const hit=forest.contact?.index===i,at=hit?forest.contact.point:forestPlantPoint(m),p=forestPoint(at),elapsed=hit?forest.contact.elapsed:0,frame=hit?(elapsed<.13?1:elapsed<.65?2:3):0;g.fillStyle='#00181c66';g.beginPath();g.ellipse(p.x,p.y+7,23,9,0,0,7);g.fill();forestSprite(g,images.guardianContact,forest.guardianFrames[frame],p.x,p.y+3,68);if(hit){forestGlow(g,p.x,p.y-35,55,'#ffb156',.3);g.strokeStyle='#ffda8e';g.lineWidth=2;for(let n=0;n<5;n++){const angle=-Math.PI+n*Math.PI/4;g.beginPath();g.moveTo(p.x+Math.cos(angle)*35,p.y-38+Math.sin(angle)*35);g.lineTo(p.x+Math.cos(angle)*47,p.y-38+Math.sin(angle)*47);g.stroke();}}}
`+s.slice(b);
 s=s.replace('else forestArchitect(g,p.x+88,p.y+22,FOREST.architectSize,1,forest.jar);',"else if(forestWaitingVisible()){const a=forestPoint(FOREST.waiting);forestSprite(g,images.architectWaiting,forest.waitingFrame,a.x,a.y,FOREST.architectSize);}else if(forest.area!=='orchard')forestArchitect(g,p.x+88,p.y+22,FOREST.architectSize,1,forest.jar);");
 s=s.replace("['path','offering','offeringReturn','hunt','paused','cinema']","['path','offering','orchardHit','offeringReturn','hunt','paused','cinema']");
 s=s.replace("d=rescue?{x:p.x+112,y:p.y+24}:origin,close=rescue?{x:p.x+8,y:p.y-30,z:2.1}","stage=forest.stage,d=rescue?forestPoint(stage.dryad):origin,ap=rescue?forestPoint(stage.architect):null,close=rescue?{x:(Math.min(p.x,ap.x,d.x)+Math.max(p.x,ap.x,d.x))/2,y:(Math.min(p.y,ap.y,d.y)+Math.max(p.y,ap.y,d.y))/2-38,z:2.1}");
 s=s.replace('const ax=p.x+(rescue?-92:88),ay=p.y+17','const ax=rescue?ap.x:p.x+88,ay=rescue?ap.y:p.y+17');
 s=s.replace("if(key==='incoming')forestDragon(g,p.x-250+q*220,p.y-170+q*90,125+q*130,t);","if(key==='incoming'){const x=-190+(close.x+190)*q,y=-210+(Math.min(p.y,ap.y,d.y)+145)*q;forestDragon(g,x,y,210+q*65,t);}");
 return s;
});
for(const f of ['build-story.mjs','render-chapter3-check.mjs'])await edit(f,s=>s.replace("dryadTalk:'dryad-talk-v3.png'","dryadTalk:'dryad-talk-v3.png',architectWaiting:'architect-waiting-v4.png',guardianContact:'guardian-contact-v4.png'"));
console.log('Solo orchard, floor-based staging, corner arrival, slower messenger and guardian contact reaction implemented.');
