// Prefer verified, embedded voice recordings. Browser speech is an optional fallback.
const voiceLibrary=typeof VOICE_LIBRARY==='object'?VOICE_LIBRARY:{lines:[],audio:{},characters:{}};
const voiceCast={
 dryad:{label:'Dryad',gender:'female',pitch:.94,rate:.91,sample:'These roots are my home. Guide them gently, and the forest will remember your kindness.'},
 alchemist:{label:'Great Alchemist',gender:'male',pitch:.76,rate:.87,sample:'Her body returned. Her spirit did not. We must light her way home.'},
 king:{label:'King',gender:'male',pitch:.72,rate:.88,sample:'Bring my daughter home. I am counting on you.'},
 architect:{label:'Architect',gender:'male',pitch:.8,rate:.94,sample:'You walk the path. I will become it.'},
 explorer:{label:'Explorer',gender:'male',pitch:1.05,rate:1.04,sample:'Hold on, Princess. We are coming for you!'},
 princess:{label:'Princess',gender:'female',pitch:1.08,rate:1.02,sample:'Please, help me! Is someone there?'},
 physician:{label:'Physician',gender:'male',pitch:.94,rate:.9,sample:'This is no ordinary sleep. An ancient curse holds her.'}
};
const voiceTones={joyful:{rate:1.04,pitch:.08},steady:{rate:1,pitch:0},grave:{rate:.94,pitch:-.04},urgent:{rate:1.08,pitch:.06},resolute:{rate:.97,pitch:-.02},gentle:{rate:.94,pitch:.02},worried:{rate:.96,pitch:.03},wonder:{rate:.96,pitch:.05}};
const voiceEngine={voices:[],choices:{},volume:1,speed:1,token:0,queue:[],pending:null,current:null,busy:false,deadline:0,settingsOpen:false,lastError:'',hiddenAt:0,returnFocus:null,audio:null,fallback:'browser',subtitles:true,lastLines:[],currentLine:null,preloads:[],music:new Map(),paused:false};
const voiceNormalize=text=>text.replace(/^[“”]|[“”]$/g,'').trim();
function recordedVoiceLine(part){
 if(part.id)return voiceLibrary.lines.find(l=>l.id===part.id&&l.character===part.role&&voiceNormalize(l.text)===voiceNormalize(part.text));
 return voiceLibrary.lines.find(l=>l.character===part.role&&voiceNormalize(l.text)===voiceNormalize(part.text)&&(!part.tone||l.tone===part.tone));
}
function setVoiceDucking(active){for(const [audio,entry]of voiceEngine.music){entry.target=entry.volume*(active?.25:1);}}
function releaseVoiceAudio(){const audio=voiceEngine.audio;if(!audio)return;voiceEngine.audio=null;audio.onended=null;audio.onerror=null;audio.onloadedmetadata=null;audio.volume=0;audio.pause();audio.removeAttribute?.('src');audio.load?.();}
function voicePlaybackDeadline(text,audio){const duration=Number.isFinite(audio?.duration)?audio.duration/(audio.playbackRate||1)*1000+6000:0;return performance.now()+Math.max(12000,duration,text.split(/\s+/).length*900+6000);}
function controllerModalOpen(){return typeof controllerState!=='undefined'&&controllerState.menu;}
function pauseVoicePlayback(paused){
 if(voiceEngine.paused===paused)return;
 voiceEngine.paused=paused;
 if(paused){voiceEngine.hiddenAt=performance.now();voiceEngine.audio?.pause();if('speechSynthesis' in window)speechSynthesis.pause();}
 else{voiceEngine.deadline+=Math.max(0,performance.now()-voiceEngine.hiddenAt);voiceEngine.hiddenAt=0;const token=voiceEngine.token;if(voiceEngine.audio){try{voiceEngine.audio.play()?.catch(()=>{if(token===voiceEngine.token)stopStorySpeech();});}catch{stopStorySpeech();}}if('speechSynthesis' in window)speechSynthesis.resume();}
}
function preloadVoiceLines(lines){
 voiceEngine.preloads=[];if(typeof Audio!=='function')return;
 for(const part of lines.slice(0,2)){const line=recordedVoiceLine(part),src=line&&voiceLibrary.audio[line.id];if(src){const audio=new Audio();audio.preload='auto';audio.src=src;voiceEngine.preloads.push(audio);}}
}
const maleVoiceNames=/\b(david|mark|george|ravi|james|guy|ryan|christopher|eric|roger|daniel|alex|fred|thomas|oliver|male)\b/i;
const femaleVoiceNames=/\b(zira|hazel|heera|susan|jenny|aria|sonia|samantha|victoria|karen|moira|tessa|siri female|female)\b/i;
const preferredStoryVoices={dryad:['Hazel','Samantha','Zira'],alchemist:['George','Ravi','David'],king:['David','George'],architect:['George','Daniel','David'],explorer:['Mark','Alex','David'],princess:['Zira','Samantha','Hazel'],physician:['Ravi','George','David']};
function pickStoryVoice(role){
 const profile=voiceCast[role],all=voiceEngine.voices;if(!profile)return null;
 const selected=all.find(v=>(v.voiceURI||v.name)===voiceEngine.choices[role]);if(selected)return selected;
 for(const name of preferredStoryVoices[role]||[]){const local=all.find(v=>v.localService&&new RegExp('\\b'+name+'\\b','i').test(v.name));if(local)return local}
 const matches=all.filter(v=>(profile.gender==='female'?femaleVoiceNames:maleVoiceNames).test(v.name));
 const pool=matches.length?matches:all.filter(v=>!(profile.gender==='female'?maleVoiceNames:femaleVoiceNames).test(v.name));
 const candidates=pool.length?pool:all;
 const index=role==='explorer'||role==='physician'?1:0;
 return candidates[Math.min(index,candidates.length-1)]||null;
}
function refreshStoryVoices(){
 voiceEngine.voices=('speechSynthesis' in window?speechSynthesis.getVoices():[]).filter(v=>/^en(?:[-_]|$)/i.test(v.lang)).sort((a,b)=>Number(b.localService)-Number(a.localService)||a.name.localeCompare(b.name));
 for(const role of Object.keys(voiceCast)){const select=$('voice-'+role);if(!select)continue;select.replaceChildren();const auto=document.createElement('option');auto.value='';auto.textContent='Automatic · '+(pickStoryVoice(role)?.name||'No English voice');select.append(auto);for(const v of voiceEngine.voices){const opt=document.createElement('option');opt.value=v.voiceURI||v.name;opt.textContent=v.name+(v.localService?'':' · online');select.append(opt)}select.value=voiceEngine.choices[role]||'';}
 const hasMale=voiceEngine.voices.some(v=>maleVoiceNames.test(v.name)),hasFemale=voiceEngine.voices.some(v=>femaleVoiceNames.test(v.name));
 $('voiceAvailability').textContent=Object.keys(voiceLibrary.audio).length+' / '+voiceLibrary.lines.length+' character recordings ready. '+(!voiceEngine.voices.length?'No browser English voice is available; missing recordings will remain captioned.':hasMale&&hasFemale?'Browser fallback voices are available.':'Preview browser fallback voices to check your cast.');
}
function stopStorySpeech(){voiceEngine.token++;releaseVoiceAudio();voiceEngine.queue=[];voiceEngine.pending=null;voiceEngine.current=null;voiceEngine.currentLine=null;voiceEngine.busy=false;voiceEngine.deadline=0;voiceEngine.paused=false;setVoiceDucking(false);if('speechSynthesis' in window)speechSynthesis.cancel();}
function speakStoryLines(lines,{preview=false}={}){
 stopStorySpeech();if(!story.voice&&!preview)return;
 voiceEngine.lastLines=lines.filter(l=>l.text&&voiceCast[l.role]).map(l=>({...l}));voiceEngine.queue=[...voiceEngine.lastLines];voiceEngine.busy=voiceEngine.queue.length>0;preloadVoiceLines(voiceEngine.queue);setVoiceDucking(voiceEngine.busy);playNextStoryLine(voiceEngine.token);
}
function playNextStoryLine(token){
 if(token!==voiceEngine.token)return;releaseVoiceAudio();const part=voiceEngine.queue.shift();if(!part){voiceEngine.current=null;voiceEngine.currentLine=null;voiceEngine.busy=false;setVoiceDucking(false);return}
 voiceEngine.currentLine=part;const line=recordedVoiceLine(part),src=line&&voiceLibrary.audio[line.id];
 if(src&&typeof Audio==='function'){
  const audio=new Audio();voiceEngine.audio=audio;voiceEngine.current=audio;voiceEngine.deadline=voicePlaybackDeadline(part.text,audio);voiceEngine.lastError='';
  audio.preload='auto';audio.volume=voiceEngine.volume;audio.playbackRate=voiceEngine.speed;audio.preservesPitch=true;
  const fallback=()=>{if(token!==voiceEngine.token||voiceEngine.audio!==audio)return;releaseVoiceAudio();voiceEngine.lastError='Recording unavailable; using the selected fallback.';playBrowserStoryLine(part,token);};
  audio.onended=()=>{if(token===voiceEngine.token&&voiceEngine.audio===audio)playNextStoryLine(token);};audio.onerror=fallback;
  audio.onloadedmetadata=()=>{if(token===voiceEngine.token&&voiceEngine.audio===audio)voiceEngine.deadline=voicePlaybackDeadline(part.text,audio);};
  audio.src=src;
  if(voiceEngine.settingsOpen)$('voiceSample').textContent=voiceCast[part.role].label+': “'+voiceNormalize(part.text)+'”';
  try{const promise=audio.play();promise?.then(()=>{if(token!==voiceEngine.token||voiceEngine.audio!==audio)return;if(document.hidden||voiceEngine.paused)audio.pause();}).catch(fallback);}catch{fallback();}return;
 }
 playBrowserStoryLine(part,token);
}
function playBrowserStoryLine(part,token){
 if(token!==voiceEngine.token)return;
 if(voiceEngine.fallback!=='browser'||!('speechSynthesis' in window)||!('SpeechSynthesisUtterance' in window)){playNextStoryLine(token);return;}
 const profile=voiceCast[part.role],tone=voiceTones[part.tone]||voiceTones.steady,voice=pickStoryVoice(part.role);
 if(!voice){voiceEngine.lastError='No English voice is available; captions remain available.';playNextStoryLine(token);return}
 const utterance=new SpeechSynthesisUtterance(part.text.replace(/[“”]/g,''));utterance.voice=voice;utterance.lang=voice.lang;
 utterance.pitch=Math.max(.5,Math.min(1.5,profile.pitch+tone.pitch));utterance.rate=Math.max(.7,Math.min(1.3,profile.rate*tone.rate*voiceEngine.speed));utterance.volume=voiceEngine.volume;
 voiceEngine.current=utterance;voiceEngine.deadline=performance.now()+Math.max(12000,part.text.split(/\s+/).length*900+6000);voiceEngine.lastError='';
 if(voiceEngine.settingsOpen)$('voiceSample').textContent=profile.label+': “'+utterance.text+'”';
 utterance.onend=()=>{if(token===voiceEngine.token)playNextStoryLine(token)};
 utterance.onerror=e=>{if(token!==voiceEngine.token)return;voiceEngine.lastError='Speech unavailable: '+e.error;stopStorySpeech();$('voiceAvailability').textContent='Speech could not play. Choose another voice or use Preview to retry.';};
 try{speechSynthesis.speak(utterance)}catch{voiceEngine.lastError='Speech could not start.';stopStorySpeech()}
}
function say(text,role,tone='steady',id){speakStoryLines([{text,role,tone,id}]);}
function speakStoryPanel(panel){
 stopStorySpeech();if(!story.voice)return;
 if(!Object.keys(voiceLibrary.audio).length&&(voiceEngine.fallback!=='browser'||!voiceEngine.voices.length||!('SpeechSynthesisUtterance' in window)))return;
 if(panel.quote&&voiceCast[panel.speaker]){voiceEngine.pending=[{text:panel.quote,role:panel.speaker,tone:panel.tone||'resolute',id:panel.voiceId}];preloadVoiceLines(voiceEngine.pending);}
}
function updateStoryVoice(now){
 for(const [audio,entry]of voiceEngine.music){audio.volume+=(entry.target-audio.volume)*.16;}
 pauseVoicePlayback(document.hidden||controllerModalOpen()&&!voiceEngine.settingsOpen);
 if(voiceEngine.paused)return;
 if(document.hidden)return;
 if(voiceEngine.busy&&now>voiceEngine.deadline){voiceEngine.lastError='Speech timed out.';stopStorySpeech()}
 if(voiceEngine.pending&&!story.fade&&!voiceEngine.settingsOpen){const lines=voiceEngine.pending;speakStoryLines(lines)}
}
function storySpeechActive(){return voiceEngine.busy||!!voiceEngine.pending;}
function voiceTimelineStep(elapsed,dt,kind='intro'){
 if(voiceEngine.settingsOpen||controllerModalOpen())return 0;
 const cuts=kind==='finale'?[6.5,16.5,20]:kind==='intro'?[8.4,15.6,21.6,25.3]:kind==='ritual'?[6.8]:[];
 if(storySpeechActive()&&cuts.some(t=>elapsed<t&&elapsed+dt>=t))return 0;
 return dt;
}
function toggleStoryVoice(){story.voice=!story.voice;$('storyVoice').textContent=story.voice?'Voice on':'Voice off';$('storyVoice').setAttribute('aria-pressed',String(story.voice));if(!story.voice)stopStorySpeech();else if(story.phase==='comic')speakStoryPanel((story.chapter==='epilogue'?epiloguePanels:storyPanels)[story.panel]);}
function openVoiceSettings(){voiceEngine.returnFocus=document.activeElement;voiceEngine.settingsOpen=true;stopStorySpeech();refreshStoryVoices();$('voiceMute').checked=!story.voice;$('voiceSubtitles').checked=voiceEngine.subtitles;$('voiceAuto').checked=typeof forest!=='undefined'&&forest.active?forest.auto:typeof campaign!=='undefined'&&campaign.active?campaign.auto:story.autoPlay!==false;$('voiceSettings').hidden=false;$('closeVoices').focus();}
function closeVoiceSettings(){stopStorySpeech();voiceEngine.settingsOpen=false;$('voiceSettings').hidden=true;story.autoLast=performance.now();if(typeof forest!=='undefined'&&forest.active&&forest.mode==='comic')forest.pendingSpeech=forestPanels[forest.panel];else if(typeof campaign!=='undefined'&&campaign.active&&campaign.mode==='comic')campaign.pendingSpeech=labPanels[campaign.panel];else if(story.phase==='comic')speakStoryPanel((story.chapter==='epilogue'?epiloguePanels:storyPanels)[story.panel]);if(controllerModalOpen()){$('controllerMenu').hidden=false;$('controllerVoices').focus();}else voiceEngine.returnFocus?.focus();}
for(const role of Object.keys(voiceCast)){
 $('voice-'+role).onchange=e=>{voiceEngine.choices[role]=e.target.value;stopStorySpeech()};
 $('preview-'+role).onclick=()=>{const line=voiceLibrary.lines.find(l=>l.character===role&&voiceLibrary.audio[l.id]);speakStoryLines([{text:line?.text||voiceCast[role].sample,role,tone:line?.tone||(role==='princess'?'urgent':role==='king'?'grave':'resolute'),id:line?.id}],{preview:true});};
}
$('voiceVolume').oninput=e=>{voiceEngine.volume=Number(e.target.value)/100;$('voiceVolumeValue').textContent=e.target.value+'%';if(voiceEngine.current)stopStorySpeech()};
$('voiceSpeed').oninput=e=>{voiceEngine.speed=Number(e.target.value)/100;$('voiceSpeedValue').textContent=voiceEngine.speed.toFixed(2)+'×';if(voiceEngine.current)stopStorySpeech()};
$('storyVoice').onclick=toggleStoryVoice;for(const id of ['openVoices','titleVoices','cinemaVoices'])$(id).onclick=openVoiceSettings;$('closeVoices').onclick=closeVoiceSettings;
document.addEventListener('visibilitychange',()=>pauseVoicePlayback(document.hidden||controllerModalOpen()&&!voiceEngine.settingsOpen));
window.addEventListener('pagehide',stopStorySpeech);
if('speechSynthesis' in window)speechSynthesis.addEventListener('voiceschanged',refreshStoryVoices);
refreshStoryVoices();
window.voiceDiagnostics=()=>({available:voiceEngine.voices.map(v=>v.name),cast:Object.fromEntries(Object.keys(voiceCast).map(role=>[role,{voice:pickStoryVoice(role)?.name,pitch:voiceCast[role].pitch,rate:voiceCast[role].rate}])),busy:storySpeechActive(),error:voiceEngine.lastError,volume:voiceEngine.volume,speed:voiceEngine.speed});
function bindVoiceManifest(){
 for(const [prefix,panels]of [['ch1-prologue',storyPanels],['ch1-epilogue',typeof epiloguePanels==='undefined'?[]:epiloguePanels],['ch2-comic',typeof labPanels==='undefined'?[]:labPanels],['ch3-comic',typeof forestPanels==='undefined'?[]:forestPanels]])panels.forEach((p,i)=>p.voiceId=prefix+'-'+String(i+1).padStart(2,'0'));
}
$('voiceFallback').onchange=e=>{voiceEngine.fallback=e.target.value==='browser'?'browser':'silent';stopStorySpeech();};
$('voiceMute').onchange=e=>{story.voice=!e.target.checked;if(!story.voice)stopStorySpeech();};
$('voiceSubtitles').onchange=e=>{voiceEngine.subtitles=e.target.checked;document.querySelector('.app').classList.toggle('voice-subtitles-off',!voiceEngine.subtitles);};
$('voiceAuto').onchange=e=>{const enabled=e.target.checked;story.autoPlay=enabled;if(typeof campaign!=='undefined')campaign.auto=enabled;if(typeof forest!=='undefined')forest.auto=enabled;story.autoLast=performance.now();if(typeof paintComicCountdown==='function')paintComicCountdown();};
$('voiceReplay').onclick=()=>{if(voiceEngine.lastLines.length)speakStoryLines(voiceEngine.lastLines.map(l=>({...l})),{preview:true});};
window.mazeVoice=Object.freeze({replay:()=>{if(voiceEngine.lastLines.length)speakStoryLines(voiceEngine.lastLines.map(l=>({...l})));},registerMusic:audio=>{if(!audio||typeof audio.volume!=='number')return false;voiceEngine.music.set(audio,{volume:audio.volume,target:audio.volume});setVoiceDucking(storySpeechActive());return true;},unregisterMusic:audio=>{const entry=voiceEngine.music.get(audio);if(entry)audio.volume=entry.volume;voiceEngine.music.delete(audio);},diagnostics:()=>({recordedLines:Object.keys(voiceLibrary.audio).length,manifestLines:voiceLibrary.lines.length,source:voiceEngine.audio?'recording':voiceEngine.current?'browser':'silent',lineId:voiceEngine.currentLine?.id||recordedVoiceLine(voiceEngine.currentLine||{text:'',role:''})?.id||null})});
