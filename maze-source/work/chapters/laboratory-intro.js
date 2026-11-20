// Chapter II arrives in the same rendered world that becomes playable.
const LAB_INTRO_SHOTS=[
 {key:'arrival',duration:3,title:'The hanging gardens',text:'Rowan and the Architect enter the silent ruins.'},
 {key:'overview',duration:2.5,title:'A path above the clouds',text:'Beyond the broken terraces, a guardian waits.'},
 {key:'dragon',duration:2.2,title:'The emerald guardian',text:'High above the gardens…'},
 {key:'roar',duration:2.6,title:'The emerald guardian',text:'[The dragon roars]'},
 {key:'wide',duration:2,title:'The way to the sanctuary',text:'Three ingredients. One way up.'},
 {key:'heroes',duration:2.2,title:'Back at the entrance',text:'The heroes have found their destination.'},
 {key:'explorer',duration:4.5,title:'Rowan · Explorer',text:'That’s our ride! Let’s find the three ingredients and reach that dragon.',role:'explorer',tone:'wonder'},
 {key:'architect',duration:4.5,title:'The Architect',text:'You gather them. I’ll become one with these ruins and open the way. Try not to keep our ride waiting.',role:'architect',tone:'resolute'},
 {key:'merge',duration:4.8,title:'The Architect’s oath',text:'His light flows into the stone. The gardens awaken.'},
 {key:'reveal',duration:3,title:'Two heroes. One path.',text:'Gather amber, moonblossom and dew. Then reach the dragon’s roost.'}
];
let labRoarSources=[],labRoarBus=null;
function labUnlockAudio(){try{audioContext??=new (window.AudioContext||window.webkitAudioContext)();if(audioContext.state==='suspended')audioContext.resume().catch(()=>{});}catch{}}
function labStopRoar(){for(const s of labRoarSources){try{s.stop();s.disconnect()}catch{}}labRoarSources=[];if(labRoarBus){labRoarBus.disconnect();labRoarBus=null;}}
function labDragonRoar(){
 labStopRoar();if(campaign.roarSound===false)return;labUnlockAudio();if(!audioContext||audioContext.state!=='running')return;
 try{
  const ac=audioContext,now=ac.currentTime,duration=2.1,bus=ac.createGain();labRoarBus=bus;
  bus.gain.setValueAtTime(.0001,now);bus.gain.exponentialRampToValueAtTime(.16,now+.18);bus.gain.exponentialRampToValueAtTime(.09,now+1.15);bus.gain.exponentialRampToValueAtTime(.0001,now+duration);bus.connect(ac.destination);
  const filter=ac.createBiquadFilter();filter.type='lowpass';filter.frequency.setValueAtTime(1250,now);filter.frequency.exponentialRampToValueAtTime(230,now+duration);filter.Q.value=.8;filter.connect(bus);
  const buffer=ac.createBuffer(1,Math.ceil(ac.sampleRate*duration),ac.sampleRate),samples=buffer.getChannelData(0);let last=0;
  for(let i=0;i<samples.length;i++){last=(last+.075*(Math.random()*2-1))/1.075;samples[i]=last*4*(.75+.25*Math.sin(i/ac.sampleRate*47));}
  const noise=ac.createBufferSource();noise.buffer=buffer;noise.connect(filter);noise.start(now);noise.stop(now+duration);labRoarSources.push(noise);
  for(const pitch of [83,127]){const osc=ac.createOscillator(),gain=ac.createGain();osc.type='sawtooth';osc.frequency.setValueAtTime(pitch,now);osc.frequency.exponentialRampToValueAtTime(pitch*.57,now+duration);gain.gain.value=.2;osc.connect(gain).connect(filter);osc.start(now);osc.stop(now+duration);labRoarSources.push(osc);}
 }catch{labStopRoar();}
}
function labIntroShot(){return LAB_INTRO_SHOTS[campaign.intro?.shot||0];}
function labEnterIntroShot(index){
 campaign.intro.shot=index;campaign.intro.elapsed=0;campaign.intro.speechWait=0;const shot=labIntroShot();
 $('labIntroTitle').textContent=shot.title;$('labIntroText').textContent=shot.role?'“'+shot.text+'”':shot.text;
 if(shot.role)say(shot.text,shot.role,shot.tone,'ch2-intro-'+shot.key);
 if(shot.key==='roar'){campaign.intro.roars++;labDragonRoar();}
}
function labStartIntro(){
 labReset();campaign.mode='intro';campaign.intro={shot:0,elapsed:0,roars:0};campaign.keys.clear();campaign.path=[];
 $('labIntro').hidden=false;$('labIntroSound').textContent=campaign.roarSound===false?'Sound off':'Sound on';$('labIntroSound').setAttribute('aria-pressed',String(campaign.roarSound!==false));
 labEnterIntroShot(0);labUI();$('labIntroSkip').focus();
}
function labFinishIntro(){if(campaign.mode!=='intro')return;labReset();}
function labUpdateIntro(dt){
 const shot=labIntroShot(),intro=campaign.intro;intro.elapsed=Math.min(shot.duration,intro.elapsed+dt);
 if(intro.elapsed<shot.duration)return;
 if(shot.role&&storySpeechActive()){intro.speechWait+=dt;if(intro.speechWait<10)return;stopStorySpeech();}
 if(intro.shot===LAB_INTRO_SHOTS.length-1){labFinishIntro();return;}
 labEnterIntroShot(intro.shot+1);
}
function labIntroCamera(){
 const p=labPoint(LAB.start),dragon=labPoint(LAB.roost),wide={x:652,y:470,z:1},heroes={x:p.x+20,y:p.y-25,z:2.65},close={x:dragon.x+8,y:dragon.y-40,z:2.65};
 const k=labIntroShot().key,q=smooth(campaign.intro.elapsed/labIntroShot().duration),mix=(a,b)=>({x:a.x+(b.x-a.x)*q,y:a.y+(b.y-a.y)*q,z:a.z+(b.z-a.z)*q});
 if(reduced)return {...wide,sx:652};
 if(k==='arrival')return {...heroes,z:1.85};
 if(k==='overview')return mix({...heroes,z:1.85},wide);
 if(k==='dragon')return mix(wide,close);
 if(k==='roar')return close;
 if(k==='wide')return mix(close,wide);
 if(k==='heroes')return mix(wide,heroes);
 if(k==='reveal')return {...mix(heroes,wide),sx:836+(652-836)*q};
 return heroes;
}
function labIntroColor(){const key=labIntroShot().key;return key==='reveal'?1:key==='merge'?smooth(campaign.intro.elapsed/4.3):0;}
function labDrawIntro(t){
 const g=labCtx,shot=labIntroShot(),p=labPoint(LAB.start),q=campaign.intro.elapsed/shot.duration,c=labIntroCamera(),merge=labIntroColor();
 labSky(t);g.save();g.translate(c.sx??836,470);g.scale(c.z,c.z);g.translate(-c.x,-c.y);labRuins(t,false,false);
 const entry=shot.key==='arrival'?1-smooth(q):0,bob=reduced?0:Math.sin(t/90)*entry*1.5;
 labHero(p.x-entry*24,p.y+4+bob,CHAPTER_VIEW.heroHeight);
 if(merge<1){const ax=p.x+40-entry*26,ay=p.y+1;
  labGlow(ax,ay-24,38+merge*44,LAB_MAGIC.glow,merge*.6);labArchitect(ax,ay,56,1-smooth(Math.min(1,merge*1.7)));
  if(merge>0)for(let i=0;i<48;i++){const a=i*2.399,r=9+merge*(32+i*2),x=ax+Math.cos(a)*r,y=ay-22+Math.sin(a)*r*.6-merge*30;labSpark(x,y,t+i*80,LAB_MAGIC.light);}
 }
 if(merge>0){g.save();g.strokeStyle=LAB_MAGIC.ring;g.globalAlpha=(1-merge)*.7;g.lineWidth=2;g.beginPath();g.ellipse(p.x+40,p.y-5,20+merge*1100,12+merge*600,0,0,Math.PI*2);g.stroke();g.restore();}
 if(shot.key==='reveal'){g.save();g.globalAlpha=smooth(q);labSpirit(t);g.restore();}
 g.restore();
 // Arrive at the gameplay transform once; never blend two differently positioned mazes.
 if(shot.key==='reveal'&&q>.7){g.save();g.globalAlpha=smooth((q-.7)/.3);if(campaign.panelArt)g.drawImage(campaign.panelArt,1304,0);g.restore();}
 $('labIntroCaption').style.opacity=shot.key==='reveal'?String(1-smooth(Math.max(0,(q-.7)/.3))):'1';
}
$('labIntroSkip').onclick=labFinishIntro;
$('labIntroVoices').onclick=()=>{labStopRoar();openVoiceSettings()};
$('labIntroSound').onclick=()=>{campaign.roarSound=campaign.roarSound===false;labUnlockAudio();if(!campaign.roarSound)labStopRoar();$('labIntroSound').textContent=campaign.roarSound?'Sound on':'Sound off';$('labIntroSound').setAttribute('aria-pressed',String(campaign.roarSound));};
document.addEventListener('visibilitychange',()=>{if(document.hidden)labStopRoar()});
window.addEventListener('pagehide',labStopRoar);
