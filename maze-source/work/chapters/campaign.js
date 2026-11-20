const campaign={active:false,mode:'idle',token:0,ready:false,panel:0,ending:false,auto:true,remaining:600,selected:0,open:[false,false,false,false,false],progress:[0,0,0,0,0],ingredients:[false,false,false],player:{...LAB.start},visual:{...LAB.start},keys:new Set(),move:0,facing:1,path:[],clock:0,phaseTime:0,fade:null,frames:[],tiles:null,cast:0,pot:null,ghost:{x:0,y:0}};
const labPanels=[
 {art:'labComic',frame:0,title:'A route above the clouds',text:'The physician marks the shattered sky gardens. The Great Alchemist has retreated to a sanctuary above them. Only his emerald dragon knows the way.',quote:'Find the dragon at the highest roost. It will carry you to the Alchemist.',speaker:'physician',tone:'grave'},
 {art:'dragonComic',frame:0,title:'The hanging gardens',text:'Water spills from broken terraces. Brass pipes wind through emerald stone. High above the ruins, a dragon guards the last passage to the sanctuary.',quote:'There! Beyond the broken bridge. That must be our way up.',speaker:'explorer',tone:'wonder'},
 {art:'dragonComic',frame:1,title:'Three gifts for a cure',text:'Rowan reads the ancient recipe: amber crystal, moonblossom, and dew of the veil. The Architect prepares to join the ruins and open their doors and bridges. Gather all three, then reach the dragon’s roost.',quote:'I’ll gather the three ingredients. Help me cross these ruins, and the dragon will take us to the Alchemist.',speaker:'explorer',tone:'resolute'},
 {art:'dragonComic',frame:2,title:'The sanctuary in the sky',text:'The dragon lands above the clouds. The Architect has taken human form again. The Great Alchemist receives the three ingredients beside his bronze cauldron.',quote:'You have brought what I need. Her body is safe, but her spirit is lost. Let us light its way home.',speaker:'alchemist',tone:'gentle'},
 {art:'dragonComic',frame:3,title:'A light to guide her home',text:'The Alchemist seals the guiding draught in a golden vial. The dragon waits at the sanctuary’s edge, ready to carry both heroes directly to the kingdom.',quote:'Take this to her. It will reach through the curse and show you where her spirit wandered.',speaker:'alchemist',tone:'resolute'},
 {art:'dragonComic',frame:5,title:'Home on emerald wings',text:'The dragon lands in the royal garden. The physician leads Rowan and the Architect straight to the Princess, the golden cure held safely between them.',quote:'We have it! Take us to the Princess. There is still time.',speaker:'explorer',tone:'joyful'},
 {art:'labComic',frame:4,title:'A voice through the curse',text:'The Architect lifts the draught to the Princess’s lips. Her eyes open for a moment. A leaf of green light slips from the vial: the cure has revealed the next step.',quote:'The forest… I cannot remember the way…',speaker:'princess',tone:'worried'},
 {art:'labComic',frame:5,title:'The forest remembers',text:'The Princess falls asleep again, but the leaf remains. The draught has shown where her lost memories wait. Rowan and the Architect follow its light toward the forest.',quote:'Then we will find your memories, Princess. Every last one.',speaker:'explorer',tone:'resolute'}
];
function labPoint(p){return {x:LAB.ox+(p.x+.5)*LAB.tile,y:LAB.oy+(p.y+.5)*LAB.tile};}
function labControlPoint(c){return labPoint({x:c.x+((c.w||1)-1)/2,y:c.y+((c.h||1)-1)/2});}
function labMessage(text){$('labMessage').textContent=text;}
function labSelectable(){return campaign.active&&campaign.mode==='playing'&&!voiceEngine.settingsOpen&&!campaign.fade;}
function labSelect(index,fromPot=false){if(!labSelectable()||!Number.isInteger(index)||index<0||index>4)return false;campaign.selected=index;if(!fromPot)campaign.pot=null;labUI();return true;}
function labPot(value,max=1023){if(!labSelectable()||!Number.isFinite(value)||!Number.isFinite(max)||max<=0||value<0||value>max)return false;const unit=value/max;let i=Math.min(4,Math.floor(unit*5));if(campaign.pot!==null&&Math.abs(i-campaign.pot)===1&&Math.abs(unit-Math.max(i,campaign.pot)/5)<.012)i=campaign.pot;if(!labSelect(i,true))return false;campaign.pot=i;return true;}
function labToggle(index=campaign.selected,open=!campaign.open[index]){
 if(typeof open!=='boolean'||!labSelect(index))return false;const c=laboratory.controls[index];if(campaign.open[index]===open)return true;
 if(open&&campaign.open.filter(Boolean).length>=2){labMessage('Only two controls can hold power. Switch one off first.');return false;}
 if(!open&&[campaign.player,campaign.visual].some(p=>labOnControl(p,c))){labMessage('Rowan is on that passage. Move clear before closing it.');return false;}
 campaign.open[index]=open;campaign.path=[];campaign.cast=.36;note(open?620:320,.12);labMessage(c.name+(open?' is receiving power.':' is switched off.'));labUI();return true;
}
function labWalk(dx,dy){
 if(!labSelectable()||Math.abs(dx)+Math.abs(dy)!==1)return false;
 const step=CHAPTER_VIEW.step/LAB.tile,x=campaign.player.x+dx*step,y=campaign.player.y+dy*step,p={x,y};
 if(!laboratory.grid[Math.floor(y+.5)]?.[Math.floor(x+.5)]||laboratory.controls.some((c,i)=>labOnControl(p,c)&&(!campaign.open[i]||campaign.progress[i]<.97)))return false;
 campaign.player=p;if(dx)campaign.facing=dx;labVisit();return true;
}
function labSetDestination(x,y){if(!labSelectable())return;const start={x:Math.floor(campaign.player.x+.5),y:Math.floor(campaign.player.y+.5)};campaign.path=labRoute(laboratory.grid,start,{x,y},labBlockedCells());}

function labVisit(){
 if(campaign.mode!=='playing')return;
 laboratory.stations.forEach((s,i)=>{if(Math.hypot(campaign.player.x-s.x,campaign.player.y-s.y)<.42&&!campaign.ingredients[i]){campaign.ingredients[i]=true;note(800+i*120,.2);labMessage(s.name+' collected. Find the other ingredients, then reach the dragon.');labUI();}});
 if(Math.hypot(campaign.player.x-LAB.roost.x,campaign.player.y-LAB.roost.y)<.42){if(campaign.ingredients.every(Boolean)){labStartFlight('ascent');}else labMessage('The dragon is waiting. Gather all three ingredients before boarding.');}
}
function labUI(){revealButton($('labReveal'),campaign,labSelectable());
 $('campaign').classList.toggle('lab-cinematic',['loading','error','comic','lost','intro','ascent','homeflight','brewing'].includes(campaign.mode));$('labFlightSkip').hidden=!['ascent','homeflight'].includes(campaign.mode);

 const seconds=Math.max(0,Math.ceil(campaign.remaining));$('labTime').textContent=String(Math.floor(seconds/60)).padStart(2,'0')+':'+String(seconds%60).padStart(2,'0');$('labPower').textContent='Power '+campaign.open.filter(Boolean).length+' / 2';
 const disabled=!labSelectable();for(let i=0;i<5;i++){const group=$('lab-control-'+i);group.classList.toggle('selected',campaign.selected===i);$('lab-select-'+i).disabled=disabled;$('lab-toggle-'+i).disabled=disabled;$('lab-off-'+i).disabled=disabled;$('lab-off-'+i).setAttribute('aria-pressed',String(!campaign.open[i]));$('lab-toggle-'+i).setAttribute('aria-pressed',String(campaign.open[i]));$('lab-select-'+i).setAttribute('aria-pressed',String(campaign.selected===i));}
 $('labCount').textContent=campaign.ingredients.filter(Boolean).length+' / 3';$('labIngredients').innerHTML=laboratory.stations.map((s,i)=>'<span class="'+(campaign.ingredients[i]?'collected':'')+'">'+(campaign.ingredients[i]?'✓':'○')+' '+['Amber','Blossom','Dew'][i]+'</span>').join('');$('labObjective').textContent=campaign.ingredients.every(Boolean)?'Reach the dragon’s roost':'Collect the three ingredients';$('labPause').textContent=campaign.mode==='paused'?'Resume':'Pause';$('labPause').disabled=!['playing','paused'].includes(campaign.mode);
}
function labReset(){resetReveal(campaign);stopStorySpeech();labStopRoar();campaign.intro=null;$('labIntro').hidden=true;$('labOutcome').classList.remove('forest-preview');$('labChapterTitle').hidden=true;Object.assign(campaign,{mode:'playing',remaining:600,selected:0,open:[false,false,false,false,false],progress:[0,0,0,0,0],ingredients:[false,false,false],player:{...LAB.start},visual:{...LAB.start},move:0,facing:1,path:[],phaseTime:0,cast:0,pot:null,pendingSpeech:null});campaign.keys.clear();campaign.ghost=labControlPoint(laboratory.controls[0]);$('labStory').hidden=true;$('labOutcome').hidden=true;labMessage('Walk onto ingredients to collect them. Q/E selects a door or bridge; Space opens or closes it. Only two can stay open.');labUI();$('labCanvas').focus();}
function labShowComic(index){
 stopStorySpeech();campaign.mode='comic';campaign.panel=index;campaign.panelRemaining=10;campaign.ending=index>=3;campaign.keys.clear();campaign.path=[];$('labChapterTitle').hidden=true;$('labStory').hidden=false;$('labOutcome').hidden=true;
 const p=labPanels[index],g=$('labComic').getContext('2d'),img=images[p.art],w=img.width/3,h=img.height/2;g.clearRect(0,0,768,768);g.drawImage(img,(p.frame%3)*w+3,Math.floor(p.frame/3)*h+3,w-6,h-6,0,0,768,768);
 $('labStoryBack').disabled=index===(campaign.ending?3:0);$('labStoryDots').innerHTML=labPanels.slice(campaign.ending?3:0,campaign.ending?8:3).map((_,i)=>'<i class="'+(i===index-(campaign.ending?3:0)?'active':'')+'"></i>').join('');$('labComic').setAttribute('aria-label',p.title);$('labStoryNumber').textContent=(campaign.ending?'CHAPTER II · EPILOGUE':'CHAPTER II · PROLOGUE')+' · '+(campaign.ending?index-2:index+1)+' / '+(campaign.ending?5:3);$('labStoryTitle').textContent=p.title;$('labSpeaker').textContent=voiceCast[p.speaker].label;$('labStoryMute').textContent=story.voice?'Voice on':'Voice off';$('labStoryMute').setAttribute('aria-pressed',String(story.voice));$('labStoryText').textContent=p.text;$('labStoryQuote').textContent='“'+p.quote+'”';$('labStoryNext').textContent=index===2?'Enter the sky gardens →':index===3?'Brew the cure →':index===4?'Fly to the kingdom →':index===7?'Chapter III →':'Continue →';$('labStorySkip').textContent=campaign.ending?'Chapter III':'Skip to sky gardens';$('labStoryAuto').textContent=campaign.auto?'Auto-play on':'Auto-play off';$('labStoryAuto').setAttribute('aria-pressed',String(campaign.auto));$('labCountdown').textContent='Next in 10s';campaign.pendingSpeech=p;labUI();$('labStoryNext').focus();
}
function labTransition(action){if(campaign.fade)return;stopStorySpeech();campaign.pendingSpeech=null;campaign.fade={elapsed:0,done:false,action};}
function labNext(){if(campaign.mode!=='comic'||campaign.fade)return;labTransition(()=>{if(campaign.panel===2)labStartIntro();else if(campaign.panel===3)labStartBrew();else if(campaign.panel===4)labStartFlight('homeflight');else if(campaign.panel===7)labForestPreview();else labShowComic(campaign.panel+1);});}
function labForestPreview(){if(campaign.mode==='lost')return;stopStorySpeech();campaign.pendingSpeech=null;campaign.mode='preview';campaign.keys.clear();$('labStory').hidden=true;$('labOutcome').hidden=true;$('labChapterTitle').hidden=false;labUI();$('labChapterReplay').focus();}
function labDefeat(){stopStorySpeech();labStopRoar();$('labIntro').hidden=true;$('labFade').hidden=true;$('labChapterTitle').hidden=true;$('labDefeatArt').src=ASSETS.labDefeat;$('labOutcome').classList.remove('forest-preview');campaign.mode='lost';campaign.keys.clear();campaign.fade=null;campaign.pendingSpeech=null;$('labStory').hidden=true;$('labOutcome').hidden=false;$('labOutcomeTitle').textContent='The Eternal Slumber';$('labOutcomeText').textContent='The cure never arrives. The Princess sleeps forever. Grief drives the King to forbidden magic, and his desperate ritual strikes down those who tried to help.';$('labRetry').textContent='Replay Chapter II';labMessage('Time has run out.');labUI();say('I will not lose you. If the light cannot save you… then let the darkness answer.','king','grave','ch2-defeat');$('labRetry').focus();}
function labPause(){if(!campaign.active||!['playing','paused'].includes(campaign.mode))return;campaign.mode=campaign.mode==='paused'?'playing':'paused';campaign.keys.clear();labUI();}
async function openLaboratory(){
 if(campaign.active)return;stopStorySpeech();labStopRoar();const token=++campaign.token;
 Object.assign(campaign,{active:true,mode:'loading',intro:null,fade:null,pendingSpeech:null,path:[]});campaign.keys.clear();
 // Cover the first visible frame, including cached re-entry from a previous game.
 for(const id of ['labStory','labIntro','labOutcome','labChapterTitle'])$(id).hidden=true;
 $('labLoading').hidden=false;$('labLoadingText').textContent='Opening the hanging gardens…';$('labFade').hidden=false;$('labFade').style.opacity='1';
 story.phase='campaign';story.fade=null;if(cinematic)cinematic.active=false;state.mode='chapter2';keys.clear();document.querySelector('.app').classList.remove('title-open');
 for(const id of ['comingSoon','titleScreen','storyScreen','cinemaScreen','storyFade','ending'])$(id).hidden=true;
 labUI();$('campaign').hidden=false;$('labLoadingReturn').focus();
 try{
  if(!campaign.ready){
   const art=await Promise.all([loadImage(ASSETS.labComic),loadImage(ASSETS.labAtlas),loadImage(ASSETS.dragonComic),loadImage(ASSETS.dragon),loadImage(ASSETS.dragonFlight),loadImage(ASSETS.kingdom),loadImage(ASSETS.dragonRoar),loadImage(ASSETS.labDefeat)]);
   if(token!==campaign.token||!campaign.active)return;
   [images.labComic,images.labAtlas,images.dragonComic,images.dragon,images.dragonFlight,images.kingdom,images.dragonRoar,images.labDefeat]=art;
   initLaboratoryArt();campaign.ready=true;
  }
  if(token!==campaign.token||!campaign.active)return;
  labShowComic(0);$('labLoading').hidden=true;campaign.fade={elapsed:.3,done:true,action(){}};
 }catch(error){if(token!==campaign.token||!campaign.active)return;campaign.mode='error';$('labLoadingText').textContent='The chapter artwork could not load. Return to the title screen and try again.';labUI();console.error(error);}
}
function leaveLaboratory(){$('labLoading').hidden=true;labStopRoar();campaign.intro=null;$('labIntro').hidden=true;campaign.token++;campaign.active=false;campaign.keys.clear();$('labFade').hidden=true;campaign.fade=null;campaign.pendingSpeech=null;stopStorySpeech();voiceEngine.settingsOpen=false;$('voiceSettings').hidden=true;$('campaign').hidden=true;$('labChapterTitle').hidden=true;$('labOutcome').hidden=true;$('comingSoon').hidden=true;$('ending').hidden=true;story.phase='title';story.chapter='prologue';story.fade=null;state.mode='intro';$('titleScreen').hidden=false;document.querySelector('.app').classList.add('title-open');$('titleBegin').focus();}
function labUpdate(dt){
 if(!campaign.active||document.hidden||voiceEngine.settingsOpen||controllerModalOpen())return;campaign.clock+=dt;
 if(['loading','error'].includes(campaign.mode))return;
 if(campaign.fade){const f=campaign.fade;f.elapsed+=dt;$('labFade').hidden=false;$('labFade').style.opacity=String(f.elapsed<.3?f.elapsed/.3:Math.max(0,1-(f.elapsed-.3)/.4));if(f.elapsed>=.3&&!f.done){f.done=true;f.action();}if(f.elapsed>=.7){campaign.fade=null;$('labFade').hidden=true;}return;}
 $('labFade').hidden=true;
 if(campaign.pendingSpeech){const p=campaign.pendingSpeech;campaign.pendingSpeech=null;say(p.quote,p.speaker,p.tone,p.voiceId);}
 if(campaign.mode==='intro'){labUpdateIntro(dt);return;}
 if(campaign.mode==='comic'){if(campaign.auto)campaign.panelRemaining=Math.max(0,campaign.panelRemaining-dt);$('labCountdownFill').style.width=(campaign.panelRemaining/10*100)+'%';$('labCountdown').textContent=!campaign.auto?'Auto-play paused':campaign.panelRemaining===0&&storySpeechActive()?'Finishing dialogue…':'Next in '+Math.ceil(campaign.panelRemaining)+'s';if(campaign.auto&&campaign.panelRemaining===0&&!storySpeechActive())labNext();return;}
 if(['ascent','homeflight','brewing'].includes(campaign.mode)){campaign.phaseTime+=dt;const duration=campaign.mode==='ascent'?18:campaign.mode==='homeflight'?17:7;if(campaign.phaseTime>=duration&&!storySpeechActive())labTransition(()=>labShowComic(campaign.mode==='ascent'?3:campaign.mode==='homeflight'?5:4));return;}
 if(campaign.mode!=='playing')return;
 campaign.remaining=Math.max(0,campaign.remaining-dt);if(campaign.remaining===0){labDefeat();return;}
 campaign.cast=Math.max(0,campaign.cast-dt);for(let i=0;i<5;i++){const target=campaign.open[i]?1:0;campaign.progress[i]+=Math.sign(target-campaign.progress[i])*Math.min(Math.abs(target-campaign.progress[i]),dt*2.5);}
 campaign.move-=dt;if(campaign.move<=0){const k=campaign.keys;let d=k.has('w')||k.has('arrowup')?[0,-1]:k.has('s')||k.has('arrowdown')?[0,1]:k.has('a')||k.has('arrowleft')?[-1,0]:k.has('d')||k.has('arrowright')?[1,0]:null;
  if(d)campaign.path=[];else {while(campaign.path.length&&Math.hypot(campaign.path[0].x-campaign.player.x,campaign.path[0].y-campaign.player.y)<.01)campaign.path.shift();const target=campaign.path[0];if(target)d=Math.abs(target.x-campaign.player.x)>.01?[Math.sign(target.x-campaign.player.x),0]:[0,Math.sign(target.y-campaign.player.y)];}
  if(d){if(!labWalk(...d))campaign.path=[];campaign.move=CHAPTER_VIEW.stepSeconds;}}

 const p=1-Math.exp(-dt*CHAPTER_VIEW.smoothing);campaign.visual.x+=(campaign.player.x-campaign.visual.x)*p;campaign.visual.y+=(campaign.player.y-campaign.visual.y)*p;const g=labControlPoint(laboratory.controls[campaign.selected]),q=reduced?1:1-Math.exp(-dt*15);campaign.ghost.x+=(g.x-campaign.ghost.x)*q;campaign.ghost.y+=(g.y-campaign.ghost.y)*q;labVisit();labUI();
}
for(const [i,c] of laboratory.controls.entries()){const row=document.createElement('div');row.className='lab-control';row.id='lab-control-'+i;row.style.top=(31.1+i*6.75)+'%';row.style.setProperty('--color',c.color);const select=document.createElement('button');select.id='lab-select-'+i;select.className='lab-select';select.textContent=c.name;select.setAttribute('aria-label','Select '+c.name);select.onclick=()=>labSelect(i);const off=document.createElement('button');off.id='lab-off-'+i;off.className='lab-power-button';off.textContent='OFF';off.setAttribute('aria-label','Close '+c.name);off.onclick=()=>labToggle(i,false);const on=document.createElement('button');on.id='lab-toggle-'+i;on.className='lab-power-button';on.textContent='ON';on.setAttribute('aria-label','Open '+c.name);on.onclick=()=>labToggle(i,true);row.append(select,off,on);$('labControls').append(row);}
$('labReveal').onclick=reveal;$('labPause').onclick=labPause;$('labRestart').onclick=()=>{if(campaign.ready)labStartIntro()};$('labExit').onclick=leaveLaboratory;$('labReturn').onclick=leaveLaboratory;$('labRetry').onclick=labStartIntro;$('labStoryNext').onclick=labNext;$('labStoryAuto').onclick=()=>{campaign.auto=!campaign.auto;$('labStoryAuto').textContent=campaign.auto?'Auto-play on':'Auto-play off';$('labStoryAuto').setAttribute('aria-pressed',String(campaign.auto));};$('labStorySkip').onclick=()=>{if(campaign.mode==='comic')labTransition(campaign.ending?labForestPreview:labStartIntro)};$('labVoices').onclick=()=>{campaign.keys.clear();openVoiceSettings()};
$('labCanvas').addEventListener('pointerdown',event=>{if(!labSelectable())return;const rect=$('labCanvas').getBoundingClientRect(),x=Math.floor(((event.clientX-rect.left)*1672/rect.width-LAB.ox)/LAB.tile),y=Math.floor(((event.clientY-rect.top)*941/rect.height-LAB.oy)/LAB.tile);labSetDestination(x,y);$('labCanvas').focus();});
function campaignKey(event){
 if(!campaign.active||voiceEngine.settingsOpen)return false;const k=event.key.toLowerCase();if(k==='tab'||event.ctrlKey||event.altKey||event.metaKey)return false;
 if(event.target.tagName==='BUTTON'&&(k==='enter'||k===' '))return false;
 if(campaign.mode==='comic'){event.preventDefault();event.stopImmediatePropagation();if(!event.repeat&&(k==='enter'||k===' '))labNext();return true;}
 if(['w','a','s','d','arrowup','arrowdown','arrowleft','arrowright','q','e','r','f',' ','p','escape','enter'].includes(k)){event.preventDefault();event.stopImmediatePropagation();if(event.repeat)return true;if(campaign.mode==='comic'){if(k==='enter'||k===' ')labNext();return true;}if(k==='r'||k==='f')reveal();else if(k==='p'||k==='escape')labPause();else if(k==='q'||k==='e')labSelect((campaign.selected+(k==='q'?4:1))%5);else if(k===' ')labToggle();else if(labSelectable())campaign.keys.add(k);return true;}return false;
}
document.addEventListener('keyup',e=>campaign.keys.delete(e.key.toLowerCase()));window.addEventListener('blur',()=>{if(campaign.active&&campaign.mode==='playing')labPause()});document.addEventListener('visibilitychange',()=>{if(document.hidden&&campaign.active&&campaign.mode==='playing')labPause()});
$('beginChapter2').onclick=()=>{labUnlockAudio();openLaboratory()};
$('titleChapter2').onclick=()=>{if(!story.ready)return;$('titleScreen').hidden=true;document.querySelector('.app').classList.remove('title-open');state.mode='complete';showComingSoon();};
window.campaignDiagnostics=()=>({active:campaign.active,mode:campaign.mode,panel:campaign.panel,remaining:campaign.remaining,ingredients:[...campaign.ingredients],open:[...campaign.open],selected:campaign.selected,player:{...campaign.player},ready:campaign.ready});

$('labComicVoices').onclick=openVoiceSettings;$('labStoryMute').onclick=()=>{story.voice=!story.voice;stopStorySpeech();$('labStoryMute').textContent=story.voice?'Voice on':'Voice off';$('labStoryMute').setAttribute('aria-pressed',String(story.voice));if(story.voice&&campaign.mode==='comic')campaign.pendingSpeech=labPanels[campaign.panel];};

// Flights are explicit locked states; physical controls use labSelectable() too.
function labStartFlight(mode){
 stopStorySpeech();campaign.pendingSpeech=null;campaign.mode=mode;campaign.phaseTime=0;campaign.keys.clear();$('labStory').hidden=true;labMessage(mode==='ascent'?'The Architect reforms. The dragon carries them to the sanctuary.':'With the cure secured, the dragon flies straight to the kingdom.');
 say(mode==='ascent'?'The ingredients are safe. Come back to us, Architect. It’s time to fly!':'Hold tight! We’re taking the cure home.','explorer',mode==='ascent'?'wonder':'joyful',mode==='ascent'?'ch2-flight-ascent':'ch2-flight-home');labUI();
}
function labStartBrew(){stopStorySpeech();campaign.mode='brewing';campaign.phaseTime=0;campaign.keys.clear();$('labStory').hidden=true;labMessage('At the upper sanctuary, the Alchemist unites the three ingredients.');say('Amber, blossom, and dew. Let this light find her.','alchemist','resolute','ch2-brewing');labUI();}
$('labFlightSkip').onclick=()=>{if(['ascent','homeflight'].includes(campaign.mode))labTransition(()=>labShowComic(campaign.mode==='ascent'?3:5));};

$('labStoryBack').onclick=()=>{const first=campaign.ending?3:0;if(campaign.mode==='comic'&&campaign.panel>first)labTransition(()=>labShowComic(campaign.panel-1));};
$('labChapterReplay').onclick=labStartIntro;$('labChapterReturn').onclick=leaveLaboratory;
$('labLoadingReturn').onclick=leaveLaboratory;
