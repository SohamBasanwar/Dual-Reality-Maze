// Input adapter for the existing 9600-baud debug lines in the three supplied ZIPs.
// All game state stays on the laptop; this does not flash firmware or move a servo.
const controllerState={enabled:false,direction:'CENTER',neutralRequired:false,context:'',lastPress:-Infinity,lastDirection:-Infinity,lightActive:false,menu:false,resume:null,serial:new Map(),chord:null,lastTick:0,pot:null};
const controllerKeys={UP:'arrowup',DOWN:'arrowdown',LEFT:'arrowleft',RIGHT:'arrowright'};
function controllerClearMovement(){for(const k of Object.values(controllerKeys)){keys.delete(k);campaign.keys.delete(k);forest.keys.delete(k);}}
function controllerContext(){if(voiceEngine.settingsOpen)return 'voices';if(controllerState.menu)return 'menu';if(forest.active)return 'forest:'+forest.mode+':'+(forest.mode==='comic'?forest.panel:'');if(campaign.active)return 'lab:'+campaign.mode+':'+(campaign.mode==='comic'?campaign.panel:'');return story.phase+':'+(story.phase==='comic'?story.panel:state.mode);}
function controllerPlaying(){return !voiceEngine.settingsOpen&&!controllerState.menu&&!story.fade&&!campaign.fade&&!forest.fade&&(forest.active?forestCanMove():campaign.active?campaign.mode==='playing':story.phase==='game'&&state.mode==='playing');}
function controllerComic(){return forest.active?forest.mode==='comic':campaign.active?campaign.mode==='comic':story.phase==='comic';}
function controllerVisible(el){return !!el&&!el.disabled&&!el.hidden&&!el.closest?.('[hidden]')&&!!el.getClientRects?.().length&&getComputedStyle(el).visibility!=='hidden'&&getComputedStyle(el).display!=='none';}
function controllerElements(){const root=voiceEngine.settingsOpen?$('voiceSettings'):controllerState.menu?$('controllerMenu'):forest.active?(forest.mode==='comic'?$('forestComicScreen'):forest.mode==='lost'?$('forestOutcome'):forest.mode==='title'?$('forestTitle'):forest.mode==='preview'?$('forestNextTitle'):$('forestChapter')):campaign.active?(campaign.mode==='comic'?$('labStory'):campaign.mode==='lost'?$('labOutcome'):campaign.mode==='preview'?$('labChapterTitle'):$('campaign')):story.phase==='title'?$('titleScreen'):story.phase==='comingSoon'?$('comingSoon'):state.mode==='lost'?$('ending'):$('storyScreen');return [...root.querySelectorAll('button,input,select')].filter(controllerVisible);}
function setControllerMode(enabled){const entering=enabled&&!controllerState.enabled;controllerState.enabled=!!enabled;$('controllerMode').checked=!!enabled;document.querySelector('.app').classList.toggle('controller-mode',!!enabled);if(entering){story.autoPlay=false;campaign.auto=false;forest.auto=false;story.autoLast=performance.now();paintComicCountdown();}controllerState.neutralRequired=true;controllerClearMovement();$('controllerHint').hidden=!enabled;}
function openControllerMenu(){
 if(controllerState.menu||voiceEngine.settingsOpen)return;controllerClearMovement();controllerState.neutralRequired=true;
 controllerState.resume=forest.active&&forestCanMove()?'forest':campaign.active&&campaign.mode==='playing'?'lab':story.phase==='game'&&state.mode==='playing'?'maze':null;
 if(controllerState.resume==='forest')forestPause();else if(controllerState.resume==='lab')labPause();else if(controllerState.resume==='maze')pause();
 controllerState.menu=true;$('controllerMenu').hidden=false;$('controllerResume').focus();
}
function closeControllerMenu(resume=true){controllerState.menu=false;$('controllerMenu').hidden=true;controllerState.neutralRequired=true;const kind=controllerState.resume;controllerState.resume=null;if(resume){if(kind==='forest'&&forest.mode==='paused')forestPause();if(kind==='lab'&&campaign.mode==='paused')labPause();if(kind==='maze'&&state.mode==='paused')pause();}if(controllerPlaying()&&controllerState.pot)window.mazeArchitect.selectPotentiometer(controllerState.pot.value,controllerState.pot.max);controllerClearMovement();}
function controllerNavigate(direction){
 const items=controllerElements();if(!items.length)return false;let at=items.indexOf(document.activeElement);
 const active=items[at];if(active&&(direction==='LEFT'||direction==='RIGHT')&&['INPUT','SELECT'].includes(active.tagName)){
  const delta=direction==='RIGHT'?1:-1;
  if(active.tagName==='SELECT'){active.selectedIndex=Math.max(0,Math.min(active.options.length-1,active.selectedIndex+delta));active.dispatchEvent(new Event('change',{bubbles:true}));}
  else if(active.type==='range'){active.value=String(Math.max(Number(active.min),Math.min(Number(active.max),Number(active.value)+delta*5)));active.dispatchEvent(new Event('input',{bubbles:true}));}
  else if(active.type==='checkbox'){active.checked=delta>0;active.dispatchEvent(new Event('change',{bubbles:true}));}return true;
 }
 at=(at+(direction==='UP'||direction==='LEFT'?-1:1)+items.length)%items.length;items[at].focus();items[at].scrollIntoView?.({block:'nearest'});return true;
}
function controllerDirection(direction){
 if(!(direction in controllerKeys)&&direction!=='CENTER')return false;
 controllerState.direction=direction;controllerClearMovement();if(direction==='CENTER'){controllerState.neutralRequired=false;return true;}
 if(document.hidden||controllerState.neutralRequired)return false;
 if(!controllerPlaying()){
  if(controllerComic()&&direction==='UP'){openControllerMenu();return true;}
  if(performance.now()-controllerState.lastDirection>=180){controllerState.lastDirection=performance.now();return controllerNavigate(direction);}return false;
 }
 const target=forest.active?forest.keys:campaign.active?campaign.keys:keys;target.add(controllerKeys[direction]);return true;
}
function controllerConfirm(role){
 if(document.hidden||story.fade||campaign.fade||forest.fade||performance.now()-controllerState.lastPress<280)return false;
 controllerState.lastPress=performance.now();controllerClearMovement();
 if(voiceEngine.settingsOpen||controllerState.menu){const items=controllerElements(),el=items.includes(document.activeElement)?document.activeElement:items[0];if(!el)return false;if(el.tagName==='SELECT'||el.type==='range')return controllerNavigate('DOWN');el.click();return true;}
 if(controllerComic()){if(forest.active)forestNext();else if(campaign.active)labNext();else nextComic();return true;}
 if(forest.active){if(forest.mode==='offering')return role==='explorer'?forestPickPear():false;if(forest.mode==='hunt')return role==='architect'?window.mazeArchitect.toggle():(openControllerMenu(),true);if(forestCanMove()){if(role==='explorer')openControllerMenu();return role==='explorer';}if(forest.mode==='paused'){forestPause();return true;}if(forest.mode==='cinema')return false;}
 else if(campaign.active){if(campaign.mode==='playing')return role==='architect'?window.mazeArchitect.toggle():(openControllerMenu(),true);if(campaign.mode==='paused'){labPause();return true;}if(['intro','ascent','homeflight','brewing'].includes(campaign.mode))return false;}
 else if(story.phase==='game'&&state.mode==='playing')return role==='architect'?window.mazeArchitect.toggle():(openControllerMenu(),true);
 else if(state.mode==='paused'){pause();return true;}
 if(['cinematic','ritual','finale','loading','epilogueLoading'].includes(story.phase))return false;
 const items=controllerElements(),focused=document.activeElement;const preferred=forest.active?forest.mode==='lost'?$('forestRetry'):forest.mode==='preview'?$('forestPreviewReturn'):$('forestBegin'):campaign.active?campaign.mode==='lost'?$('labRetry'):$('labChapterSoon'):story.phase==='comingSoon'?$('beginChapter2'):state.mode==='lost'?$('again'):$('titleBegin');const el=items.includes(focused)?focused:preferred;if(controllerVisible(el)){el.click();return true;}return false;
}
function controllerPress(role){
 if(!['explorer','architect'].includes(role))return false;
 if(controllerPlaying()){
  const pending=controllerState.chord;if(pending){if(pending.role!==role){clearTimeout(pending.timer);controllerState.chord=null;openControllerMenu();return true;}return false;}
  const context=controllerContext();controllerState.chord={role,timer:setTimeout(()=>{controllerState.chord=null;if(controllerContext()===context)controllerConfirm(role);},160)};return true;
 }
 return controllerConfirm(role);
}
function controllerPot(value,max=1023){if(!Number.isFinite(value)||!Number.isFinite(max)||max<=0||value<0||value>max)return false;controllerState.pot={value,max};if(!controllerPlaying())return false;return window.mazeArchitect.selectPotentiometer(value,max);}
function controllerLine(role,line){
 if(typeof line!=='string'||line.length>256)return false;
 if(role==='explorer'){
  let m=line.match(/^Direction: (CENTER|UP|DOWN|LEFT|RIGHT)\b/);if(m)return controllerDirection(m[1]);
  if(line.trim()==='Joystick Button: PRESSED')return controllerPress('explorer');
  m=line.match(/^Light Level: (\d+) -> (REVEAL ACTIVATED|Normal)$/);if(m){if(Number(m[1])>1023)return false;const on=m[2]==='REVEAL ACTIVATED',edge=on&&!controllerState.lightActive;controllerState.lightActive=on;if(edge&&controllerPlaying())reveal();return true;}
 }else if(role==='architect'){
  const m=line.match(/^Selected: .+ \| Potentiometer: (\d+)$/);if(m)return controllerPot(Number(m[1]));
  const confirmed=line.match(/^CONFIRMED: (Gate A|Gate B|Gate C|Bridge|Trap)$/);if(confirmed){const index=['Gate A','Gate B','Gate C','Bridge','Trap'].indexOf(confirmed[1]);if(!controllerState.pot)controllerState.pot={value:(index+.5)*1023/5,max:1023};if(controllerPlaying())window.mazeArchitect.select(index);return controllerPress('architect');}
 }return false;
}
async function connectController(role){
 if(!navigator.serial){$('controllerStatus').textContent='Web Serial is unavailable. Use desktop Chrome/Edge on a supported secure local origin, or call the input adapter from your own bridge.';return;}
 if(controllerState.serial.has(role)){ $('controllerStatus').textContent=role+' is already connected.';return;}
 labUnlockAudio();let port;
 try{port=await navigator.serial.requestPort();await port.open({baudRate:9600});const reader=port.readable.getReader();controllerState.serial.set(role,{port,reader});setControllerMode(true);$('controllerStatus').textContent=[...controllerState.serial.keys()].join(' + ')+' connected at 9600 baud.';
  const decoder=new TextDecoder();let partial='';while(true){const {value,done}=await reader.read();if(done)break;partial+=decoder.decode(value,{stream:true});const rows=partial.split(/\r?\n/);partial=rows.pop();if(partial.length>512)partial='';for(const row of rows)controllerLine(role,row.trim());}
 }catch{$('controllerStatus').textContent='Could not connect or read '+role+'. Check the selected USB port and close Serial Monitor.';}
 finally{const entry=controllerState.serial.get(role);if(entry){controllerState.serial.delete(role);try{entry.reader.releaseLock();await entry.port.close();}catch{}}controllerClearMovement();controllerState.direction='CENTER';controllerState.neutralRequired=true;$('controllerStatus').textContent='Connected: '+([...controllerState.serial.keys()].join(', ')||'none')+'. '+role+' disconnected. Movement stopped.';if(!controllerState.menu)openControllerMenu();}
}
async function disconnectControllers(){for(const entry of controllerState.serial.values()){try{await entry.reader.cancel();}catch{}}controllerClearMovement();}
function updateControllerInput(){
 const context=controllerContext();if(context!==controllerState.context){controllerState.context=context;controllerState.neutralRequired=controllerState.direction!=='CENTER';controllerClearMovement();if(controllerPlaying()&&controllerState.pot)window.mazeArchitect.selectPotentiometer(controllerState.pot.value,controllerState.pot.max);if(controllerState.enabled&&!voiceEngine.settingsOpen&&!controllerState.menu){const primary=forest.active?forest.mode==='comic'?$('forestStoryNext'):forest.mode==='title'?$('forestBegin'):forest.mode==='lost'?$('forestRetry'):forest.mode==='preview'?$('forestPreviewReturn'):null:campaign.active?campaign.mode==='comic'?$('labStoryNext'):campaign.mode==='lost'?$('labRetry'):campaign.mode==='preview'?$('labChapterSoon'):null:story.phase==='comic'?$('storyNext'):story.phase==='title'?$('titleBegin'):story.phase==='comingSoon'?$('beginChapter2'):state.mode==='lost'?$('again'):null;if(controllerVisible(primary))primary.focus();}}
 if(document.hidden){controllerClearMovement();return;}
 if(controllerPlaying()&&!controllerState.neutralRequired&&controllerState.direction!=='CENTER'){const target=forest.active?forest.keys:campaign.active?campaign.keys:keys;target.add(controllerKeys[controllerState.direction]);}
 if(controllerState.enabled){$('controllerHint').hidden=!(controllerComic()||voiceEngine.settingsOpen||controllerState.menu);$('controllerHint').textContent=voiceEngine.settingsOpen||controllerState.menu?'Joystick ↑↓ chooses · ←→ adjusts · Either button confirms':'Either button continues · Joystick ↑ opens menu';}
}
$('controllerOpen').onclick=openControllerMenu;$('controllerResume').onclick=()=>closeControllerMenu();$('controllerMode').onchange=e=>setControllerMode(e.target.checked);
$('controllerVoices').onclick=()=>{$('controllerMenu').hidden=true;openVoiceSettings();};$('controllerReplay').onclick=()=>window.mazeVoice.replay();
$('controllerRestart').onclick=()=>{closeControllerMenu(false);if(forest.active)replayForest();else if(campaign.active)labStartIntro();else finishStoryForRestart();};
function finishStoryForRestart(){if(story.phase==='game')restart();else{stopStorySpeech();story.fade=null;story.chapter='prologue';story.phase='game';if(cinematic)cinematic.active=false;for(const id of ['storyScreen','cinemaScreen','comingSoon','titleScreen','ending','storyFade'])$(id).hidden=true;document.querySelector('.app').classList.remove('title-open');storyControls(false);restart();}}
$('controllerTitle').onclick=()=>{closeControllerMenu(false);if(forest.active)leaveForest();else if(campaign.active)leaveLaboratory();else{stopStorySpeech();if(cinematic)cinematic.active=false;story.fade=null;story.phase='title';state.mode='intro';$('storyScreen').hidden=true;$('cinemaScreen').hidden=true;$('ending').hidden=true;$('help').hidden=true;$('comingSoon').hidden=true;$('titleScreen').hidden=false;document.querySelector('.app').classList.add('title-open');$('titleBegin').focus();}};
$('connectExplorer').onclick=()=>connectController('explorer');$('connectArchitect').onclick=()=>connectController('architect');$('disconnectControllers').onclick=disconnectControllers;
function controllerKey(e){if(!controllerState.menu||voiceEngine.settingsOpen)return false;e.preventDefault();e.stopImmediatePropagation();if(e.key==='Escape')closeControllerMenu();else if(['ArrowUp','ArrowDown','ArrowLeft','ArrowRight'].includes(e.key))controllerNavigate(e.key.slice(5).toUpperCase());else if(e.key==='Tab')controllerNavigate(e.shiftKey?'UP':'DOWN');else if(!e.repeat&&['Enter',' '].includes(e.key))controllerConfirm('explorer');return true;}
window.addEventListener('blur',()=>{controllerClearMovement();controllerState.neutralRequired=true;});
window.mazeControllers=Object.freeze({press:controllerPress,direction:controllerDirection,potentiometer:controllerPot,readLine:controllerLine,setMode:setControllerMode,menu:openControllerMenu,diagnostics:()=>({mode:controllerState.enabled,context:controllerContext(),direction:controllerState.direction,neutralRequired:controllerState.neutralRequired,connected:[...controllerState.serial.keys()]})});
