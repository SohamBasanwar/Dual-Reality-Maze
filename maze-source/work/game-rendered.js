const canvas=document.getElementById('world'),ctx=canvas.getContext('2d');ctx.imageSmoothingEnabled=false;
const $=id=>document.getElementById(id),reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
const state={player:{...START},visual:{...START},open:[false,false,false,false,false],selected:0,key:false,keyAwakened:false,runes:[false,false,false],remaining:600,mode:'ready',path:[],revealUntil:0,revealReady:0,steps:0,facing:1};
let previous=0,accumulator=0,toastTimer,helpMode='ready',audioContext,soundOn=false,heroBounds=null,loaded=false,lastMove=0,lastNotice=0;
const keys=new Set(),images={};
const uiControls=ELEMENTS.map((e,i)=>{const group=document.createElement('div');group.className='switch';group.style.top=(31.1+i*6.75)+'%';group.style.setProperty('--color',e.color);group.setAttribute('role','group');group.setAttribute('aria-label',e.name);for(const [j,label] of ['OFF','ON'].entries()){const b=document.createElement('button');b.textContent=label;b.setAttribute('aria-label',`${e.name} ${j?'open':'closed'}`);b.addEventListener('click',()=>setElement(i,!!j));group.append(b)}$('architect').append(group);return group});
function effectiveOpen(){return state.open.map((v,i)=>v&&animation.elements[i]>.97)}
function message(text,toast=false){$('message').textContent=text;if(toast){$('toast').textContent=text;$('toast').classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').classList.remove('show'),2700)}}
function note(hz=440,duration=.1){if(!soundOn)return;try{audioContext??=new (window.AudioContext||window.webkitAudioContext)();audioContext.resume();const o=audioContext.createOscillator(),g=audioContext.createGain();o.type='triangle';o.frequency.setValueAtTime(hz,audioContext.currentTime);g.gain.setValueAtTime(.025,audioContext.currentTime);g.gain.exponentialRampToValueAtTime(.0001,audioContext.currentTime+duration);o.connect(g).connect(audioContext.destination);o.start();o.stop(audioContext.currentTime+duration)}catch{}}
function updateUI(){const s=Math.max(0,Math.ceil(state.remaining));$('time').textContent=String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0');$('time').classList.toggle('urgent',s<=25);$('keyCount').innerHTML=`<b>${state.key?1:0}</b> / 1`;uiControls.forEach((g,i)=>{g.classList.toggle('selected',state.selected===i);[...g.children].forEach((b,j)=>b.setAttribute('aria-pressed',String(state.open[i]===!!j)))});$('pause').textContent=state.mode==='paused'?'Resume':'Pause';const n=state.runes.filter(Boolean).length;$('quest').textContent=state.mode==='ready'?'The Three Seals':state.key?'Reach the wormhole':`${n} / 3 RUNES AWAKENED`;$('objective').textContent=`Power ${state.open.filter(Boolean).length} / 2 · ${state.key?'The eastern lock is open':n===3?'Claim the golden key':'Moon · Sun · Star'}`;$('start').textContent=state.mode==='ready'?'Enter the maze':'Restart';$('runeHud').innerHTML=RUNES.map((r,i)=>`<span style="color:${state.runes[i]?r.color:'#736a86'}" title="${r.name} rune ${state.runes[i]?'collected':'missing'}">${['☾','☼','✦'][i]}</span>`).join('');revealButton($('reveal'),state,state.mode==='playing');}
let architectPotIndex=null;
function architectControlAllowed(){return loaded&&['ready','playing'].includes(state.mode)&&$('help').hidden;}
function selectElement(i,source='manual'){
 if(!architectControlAllowed()||!Number.isInteger(i)||i<0||i>=ELEMENTS.length)return false;
 if(source!=='pot')architectPotIndex=null;
 if(state.selected!==i){state.selected=i;moveArchitectSpirit(i);updateUI();}
 return true;
}
function selectArchitectPotentiometer(value,max=1023){
 if(!architectControlAllowed()||!Number.isFinite(value)||!Number.isFinite(max)||max<=0||value<0||value>max)return false;
 const unit=value/max,n=ELEMENTS.length;let index=Math.min(n-1,Math.floor(unit*n));
 // A small dead band prevents a noisy dial from flickering between adjacent passages.
 if(architectPotIndex!==null&&Math.abs(index-architectPotIndex)===1){const boundary=Math.max(index,architectPotIndex)/n;if(Math.abs(unit-boundary)<.012)index=architectPotIndex;}
 if(!selectElement(index,'pot'))return false;architectPotIndex=index;return true;
}
function setElement(i,open){
 if(typeof open!=='boolean'||!selectElement(i))return false;
 const e=ELEMENTS[i];if(state.open[i]===open)return true;
 if(!open&&(inside(state.player.x,state.player.y,e.barrier)||inside(state.visual.x,state.visual.y,e.barrier))){pulseArchitectSpirit(i,true);message(`Explorer is on ${e.name}. Move clear before closing.`,true);return false;}
 if(open&&state.open.filter(Boolean).length>=2){pulseArchitectSpirit(i,true);message('Only two elements can hold power. Close one behind the Explorer.',true);return false;}
 state.open[i]=open;state.path=[];pulseArchitectSpirit(i);note(open?540:260,.2);message(`${e.name} ${open?(e.type==='gate'?'raising…':'extending…'):(e.type==='gate'?'lowering…':'retracting…')}`,true);updateUI();return true;
}
// A controller transport can feed ADC readings and button edges through this same guarded path.
function inMemoryForest(){return typeof forest!=='undefined'&&forest.active;}
function inLaboratory(){return typeof campaign!=='undefined'&&campaign.active;}
window.mazeArchitect=Object.freeze({select:i=>inMemoryForest()?forestSelect(i):inLaboratory()?labSelect(i):selectElement(i),selectPotentiometer:(v,max)=>inMemoryForest()?forestPot(v,max):inLaboratory()?labPot(v,max):selectArchitectPotentiometer(v,max),toggle:()=>inMemoryForest()?forestToggle():inLaboratory()?labToggle():setElement(state.selected,!state.open[state.selected]),setOpen:open=>inMemoryForest()?forestToggle(forest.selected,open):inLaboratory()?labToggle(campaign.selected,open):setElement(state.selected,open)});
function restart(){if(!loaded)return;resetReveal(state);if(typeof resetStoryRound==='function')resetStoryRound();Object.assign(state,{player:{...START},visual:{...START},open:[false,false,false,false,false],selected:0,key:false,keyAwakened:false,runes:[false,false,false],remaining:600,mode:'playing',path:[],revealUntil:0,revealReady:0,steps:0,facing:1});animation.elements.fill(0);architectPotIndex=null;resetArchitectSpirit();keys.clear();$('ending').hidden=true;$('help').hidden=true;message('Awaken Moon, Sun, and Star. Then claim the key and escape.',true);updateUI();canvas.focus();note(420,.25)}
function finish(won){if(!won&&typeof prepareStoryDefeat==='function')prepareStoryDefeat();$('again').textContent='Replay Chapter I';state.mode=won?'won':'lost';state.path=[];keys.clear();updateUI();$('endingTitle').textContent=won?'The realities are aligned.':'The Kingdom Falls';$('endingText').textContent=won?`Three seals awakened. One key recovered. You escaped with ${Math.ceil(state.remaining)} seconds to spare.`:'The last light fades. Ghosts and monsters claim the king’s throne, and the kingdom falls. Begin again and change its fate.';if($('defeatArt')){$('defeatArt').hidden=won;$('ending').classList.toggle('defeated',!won)}$('ending').hidden=false;$('again').focus();message(won?'You escaped the Crystal Abyss!':'Time has run out.');note(won?880:180,.5)}
function visit(){
 RUNES.forEach((r,i)=>{if(!state.runes[i]&&Math.hypot(state.player.x-r.x,state.player.y-r.y)<18){state.runes[i]=true;message(`${r.name} seal awakened. ${state.runes.filter(Boolean).length} of 3 collected.`,true);note(650+i*120,.3);updateUI()}});
 if(state.runes.every(Boolean)&&!state.keyAwakened&&state.mode==='playing'){if(typeof beginRuneAwakening==='function'){beginRuneAwakening();return}else state.keyAwakened=true}
 if(!state.key&&Math.hypot(state.player.x-KEY.x,state.player.y-KEY.y)<21){if(state.keyAwakened){state.key=true;message('Golden key claimed. Return east to the wormhole!',true);note(1000,.35);updateUI()}else if(performance.now()-lastNotice>2200){message('The key is bound by three seals. Find Moon, Sun, and Star.',true);lastNotice=performance.now()}}
 if(state.key&&typeof beginFinale==='function'&&state.player.x>EXIT.x-64&&state.player.y>EXIT.y+20&&state.player.y<EXIT.y+82){beginFinale();return}
 if(state.key&&Math.hypot(state.player.x-EXIT.x,state.player.y-EXIT.y)<22){if(typeof beginFinale==='function')beginFinale();else finish(true)}
}
function step(dx,dy){if(state.mode!=='playing')return false;const x=state.player.x+dx*STEP,y=state.player.y+dy*STEP;if(!walkable(x,y,effectiveOpen(),state.key))return false;state.player={x,y};state.steps++;visit();return true}
function revealContext(){
 if(typeof voiceEngine!=='undefined'&&voiceEngine.settingsOpen||typeof controllerModalOpen==='function'&&controllerModalOpen())return null;
 if(inMemoryForest())return forest.area==='orchard'&&forest.mode==='offering'&&forestCanMove()?{kind:'forest',owner:forest,notify:forestMessage}:null;
 if(inLaboratory())return labSelectable()?{kind:'lab',owner:campaign,notify:labMessage}:null;
 return state.mode==='playing'&&$('help').hidden?{kind:'maze',owner:state,notify:text=>message(text,true)}:null;
}
function resetReveal(owner){owner.revealUntil=0;owner.revealReady=0;owner.revealUsed=0;owner.guidance=null;}
function revealButton(button,owner,allowed=true){const now=performance.now(),left=REVEAL_RULES.uses-(owner.revealUsed||0),cool=Math.ceil(Math.max(0,(owner.revealReady||0)-now)/1000);button.textContent=left===0?'Reveal · 0/3':cool?'Reveal · '+cool+'s · '+left+'/3':'Reveal · R · '+left+'/3';button.disabled=!allowed||left===0||cool>0;button.title='Highlight the nearest objective and its route for 3 seconds. Three uses per chapter; 12 seconds between activations.';}
function revealPlan(context){
 const {kind,owner}=context;let grid,start,targets,blocked=[],point,controls,open;
 if(kind==='maze'){
  grid=cells;const tile=p=>({x:Math.floor((p.x-OX)/TILE),y:Math.floor((p.y-OY)/TILE)});start=tile(owner.player);point=p=>center(p.x,p.y);
  targets=RUNES.filter((r,i)=>!owner.runes[i]).map(r=>({...tile(r),name:r.name+' rune',height:38}));
  if(!targets.length)targets=[{...tile(owner.key?EXIT:KEY),name:owner.key?'Wormhole':'Golden key',height:owner.key?110:40}];
  if(!owner.key)blocked=[tile({x:LOCK[0],y:LOCK[1]})];controls=ELEMENTS;open=effectiveOpen();
 }else if(kind==='lab'){
  grid=laboratory.grid;start={x:Math.floor(owner.player.x+.5),y:Math.floor(owner.player.y+.5)};point=labPoint;controls=laboratory.controls;open=owner.open.map((v,i)=>v&&owner.progress[i]>.97);
  targets=laboratory.stations.filter((s,i)=>!owner.ingredients[i]).map(s=>({...s,height:55}));if(!targets.length)targets=[{...LAB.roost,name:'Dragon’s roost',height:120}];
 }else{
  grid=forestGrid();start={x:Math.floor(owner.player.x+.5),y:Math.floor(owner.player.y+.5)};point=forestPoint;controls=[];open=[];
  targets=forestFruitTrees.filter((s,i)=>!owner.pears[i]).map(s=>({...s,height:145,goals:[[-1,0],[1,0],[0,-1],[0,1]].map(([dx,dy])=>({x:s.x+dx,y:s.y+dy}))}));
  if(!targets.length)targets=[{x:2,y:19,name:'Orchard return',height:32}];
 }
 const found=nearestRevealRoute(grid,start,targets,blocked);if(!found)return null;
 const closed=controls.filter((c,i)=>!open[i]&&found.path.some(p=>p.x>=c.x&&p.x<c.x+(c.w||1)&&p.y>=c.y&&p.y<c.y+(c.h||1)));
 return {...found,points:found.path.map(point),beacon:point(found.target),closed:closed.map(c=>({...c,point:point({x:c.x+((c.w||1)-1)/2,y:c.y+((c.h||1)-1)/2})}))};
}
function revealSignature(context){const o=context.owner;return JSON.stringify([context.kind,o.player,o.open,context.kind==='maze'?effectiveOpen():o.progress?.map(v=>v>.97),o.runes,o.key,o.ingredients,o.pears]);}
function activeReveal(){const context=revealContext();if(!context||performance.now()>=(context.owner.revealUntil||0))return null;const signature=revealSignature(context);if(context.owner.guidance?.cacheKey!==signature){context.owner.guidance=revealPlan(context);if(context.owner.guidance)context.owner.guidance.cacheKey=signature;}const plan=context.owner.guidance;return plan?{...context,plan}:null;}
function reveal(){
 const context=revealContext();if(!context)return false;const {owner,notify}=context,now=performance.now();
 if((owner.revealUsed||0)>=REVEAL_RULES.uses){notify('All three reveals have been used for this chapter.');return false;}
 if(now<(owner.revealReady||0)){notify('The reveal crystal is recharging.');return false;}
 const plan=revealPlan(context);if(!plan){notify('No route to an objective is available from here.');return false;}
 owner.guidance=plan;owner.revealUntil=now+REVEAL_RULES.duration;owner.revealReady=now+REVEAL_RULES.recharge;owner.revealUsed=(owner.revealUsed||0)+1;
 notify(plan.target.name+' revealed for 3 seconds.'+(plan.closed.length?' Amber marks passages the Architect must open: '+plan.closed.map(c=>c.name).join(', ')+'.':' Follow the glowing trail.')+' '+(REVEAL_RULES.uses-owner.revealUsed)+' reveals left.');note(660,.2);
 if(context.kind==='forest')forestUI();else if(context.kind==='lab')labUI();else updateUI();return true;
}
function pause(){if(!['playing','paused'].includes(state.mode)||!$('help').hidden)return;state.mode=state.mode==='playing'?'paused':'playing';keys.clear();message(state.mode==='paused'?'Paused. Press P to continue.':'The dungeon awakens.');updateUI()}
function showHelp(){if(!$('help').hidden)return;helpMode=state.mode;if(state.mode==='playing')state.mode='paused';keys.clear();$('help').hidden=false;$('closeHelp').focus();updateUI()}
function hideHelp(){$('help').hidden=true;state.mode=helpMode;updateUI();canvas.focus()}
canvas.addEventListener('pointerdown',e=>{if(!loaded||state.mode!=='playing')return;const r=canvas.getBoundingClientRect(),target={x:(e.clientX-r.left)*1672/r.width,y:(e.clientY-r.top)*941/r.height};if(target.x>1300)return;if(Math.hypot(target.x-state.player.x,target.y-state.player.y)>52){message('Use WASD / arrows, or tap a nearby tile. The maze must be explored.',true);return}const p=route(state.player,target,effectiveOpen(),state.key);state.path=p.length<=10?p:[];canvas.focus()});
document.addEventListener('keydown',e=>{const k=e.key.toLowerCase();if(!$('help').hidden||!$('ending').hidden){if(k==='escape'&&!$('help').hidden){e.preventDefault();hideHelp()}if(k==='tab'){e.preventDefault();(!$('help').hidden?$('closeHelp'):$('again')).focus()}return}if(e.target.tagName==='BUTTON'&&(k===' '||k==='enter'))return;if(['arrowup','arrowdown','arrowleft','arrowright',' '].includes(k))e.preventDefault();if(['w','a','s','d','arrowup','arrowdown','arrowleft','arrowright'].includes(k))keys.add(k);if(e.repeat)return;if(k==='enter'&&state.mode==='ready')restart();if(k==='p'||k==='escape')pause();if(k==='r'||k==='f')reveal();if(k==='q'||k==='e'){selectElement((state.selected+(k==='q'?ELEMENTS.length-1:1))%ELEMENTS.length)}if(k===' ')setElement(state.selected,!state.open[state.selected])});
document.addEventListener('keyup',e=>keys.delete(e.key.toLowerCase()));window.addEventListener('blur',()=>{keys.clear();if(state.mode==='playing')pause()});document.addEventListener('visibilitychange',()=>{if(document.hidden&&state.mode==='playing')pause()});
$('start').onclick=restart;$('again').onclick=restart;$('pause').onclick=pause;$('reveal').onclick=reveal;$('guide').onclick=showHelp;$('closeHelp').onclick=hideHelp;
$('sound').onclick=()=>{soundOn=!soundOn;$('sound').setAttribute('aria-pressed',String(soundOn));$('sound').textContent=soundOn?'Sound on':'Sound off';note(440,.2)};
$('fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await document.documentElement.requestFullscreen()}catch{message('Fullscreen is unavailable in this browser.',true)}};
function loadImage(src){return new Promise((resolve,reject)=>{const img=new Image();img.onload=()=>{if(typeof reportTitleLoad==='function')reportTitleLoad();resolve(img)};img.onerror=reject;img.src=src})}
async function init(){try{[images.atlas,images.hero,images.spirit]=await Promise.all([loadImage(ASSETS.atlas),loadImage(ASSETS.hero),loadImage(ASSETS.spirit)]);const c=document.createElement('canvas');c.width=images.hero.width;c.height=images.hero.height;const g=c.getContext('2d');g.drawImage(images.hero,0,0);const d=g.getImageData(0,0,c.width,c.height).data;let left=c.width,top=c.height,right=0,bottom=0;for(let y=0;y<c.height;y++)for(let x=0;x<c.width;x++)if(d[(y*c.width+x)*4+3]>80){left=Math.min(left,x);right=Math.max(right,x);top=Math.min(top,y);bottom=Math.max(bottom,y)}heroBounds={x:left,y:top,w:right-left+1,h:bottom-top+1};initScene();initArchitectSpiritArt();loaded=true;$('loading').hidden=true;$('start').disabled=false;updateUI()}catch(err){$('loading').textContent='The artwork could not load. Reopen the complete HTML file.';console.error(err);if(typeof failTitleScreen==='function')failTitleScreen()}requestAnimationFrame(render)}
window.mazeDiagnostics=()=>({loaded,mode:state.mode,player:{...state.player},open:[...state.open],progress:[...animation.elements],runes:[...state.runes],key:state.key,remaining:state.remaining,portalFrames:animation.portalFrames,flameFrames:animation.flameFrames,mapTiles:cells.flat().filter(Boolean).length,walls:walls.length});
init();


