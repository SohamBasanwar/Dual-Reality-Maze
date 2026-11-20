// Cinematic revision: cold open, shock, animated title, narrated cards, rising action.
import fs from 'node:fs/promises';
import path from 'node:path';
import {execFileSync,spawnSync,spawn} from 'node:child_process';
import {once} from 'node:events';
import {createRequire} from 'node:module';
const req=createRequire(import.meta.url),{createCanvas,loadImage}=req('C:/Users/soham/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@napi-rs/canvas');
const R=path.resolve(import.meta.dirname,'../..'),B=path.join(R,'trailer-kit/cinematic-v3'),G=path.join(R,'trailer-kit/full-story-v2/generated'),N=path.join(R,'trailer-kit/full-story-v2/narration'),O=path.join(R,'submission/Full_Story_Revision');
const FF='C:/Users/soham/AppData/Local/Temp/maze-trailer-tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe';
const W=1920,H=1080,FPS=24;
await fs.mkdir(B,{recursive:true});await fs.mkdir(O,{recursive:true});
const probe=f=>{const p=spawnSync(FF,['-hide_banner','-i',f],{windowsHide:true,encoding:'utf8'});const m=p.stderr.match(/Duration: (\d+):(\d+):([\d.]+)/);if(!m)throw Error('Cannot read '+f);return +m[1]*3600 + +m[2]*60 + +m[3];};
const narrations=['01_two_heroes.mp3','02_cure.mp3','03_memories.mp3','04_oath.mp3'];
const nd=Object.fromEntries(narrations.map(n=>[n,probe(path.join(N,n))]));
const cardDur=(n,min=4)=>Math.ceil(Math.max(min,nd[n]+1.1)*FPS)/FPS;
const shots=[
 {id:'01_cold_open',file:path.join(G,'prologue.mp4'),duration:5,native:true,quote:'“Bring my daughter home.”',sub:'“I am counting on you.”',cross:0},
 {id:'02_portal_surge',file:path.join(G,'opening.mp4'),seek:2.1,duration:2,native:true,cross:.125,surge:true},
 {id:'03_title_reveal',duration:4,title:true,cross:.125},
 {id:'04_two_heroes',duration:cardDur(narrations[0]),card:['TWO HEROES.','ONE SHARED FATE.'],voice:narrations[0],cross:.375},
 {id:'05_maze',file:path.join(R,'trailer-kit/clips/01_maze_and_architect.mp4'),duration:4,label:'PROTOTYPE GAMEPLAY',cross:.375},
 {id:'06_transformation',file:path.join(R,'trailer-kit/clips/02_architect_transformation.mp4'),duration:2.25,cross:.125},
 {id:'07_cure_card',duration:cardDur(narrations[1]),card:['BEYOND THE CLOUDS…','A CURE.'],voice:narrations[1],cross:.375},
 {id:'08_sky_gardens',file:path.join(G,'chapter2.mp4'),duration:5,native:true,cross:.375},
 {id:'09_dragon_flight',file:path.join(R,'trailer-kit/clips/04_dragon_flight.mp4'),duration:3,cross:.125},
 {id:'10_memory_card',duration:cardDur(narrations[2]),card:['SOME MEMORIES','REFUSE TO FADE.'],voice:narrations[2],cross:.375},
 {id:'11_forest',file:path.join(G,'chapter3.mp4'),duration:5,native:true,cross:.375},
 {id:'12_memory_capture',file:path.join(R,'trailer-kit/clips/06_memory_in_the_jar.mp4'),duration:2.5,cross:.125},
 {id:'13_oath_card',duration:cardDur(narrations[3],4.5),card:['BUT THE OATH…','IS NOT YET FULFILLED.'],voice:narrations[3],cross:.375},
 {id:'14_clockwork',file:path.join(G,'chapter4.mp4'),duration:5,native:true,label:'CHAPTER IV · COMING SOON',cross:.375},
 {id:'15_final_seal',file:path.join(G,'chapter5.mp4'),duration:5,native:true,label:'CHAPTER V · COMING SOON',cross:.125},
 {id:'16_homecoming',file:path.join(G,'homecoming.mp4'),duration:4,native:true,label:'PLANNED STORY CONCLUSION',cross:.375},
 {id:'17_end_title',duration:5,title:true,end:true,cross:.375}
];
let duration=0;for(const s of shots){s.start=duration-s.cross;duration=s.start+s.duration;}
const titleArt=await loadImage(path.join(R,'images/title-screen.png'));
function text(g,t,x,y,size,color='#f5e6c7',align='center'){g.save();g.textAlign=align;g.font=`bold ${size}px Georgia`;g.fillStyle=color;g.shadowColor='#000';g.shadowBlur=12;g.fillText(t,x,y);g.restore();}
const renderCanvas=createCanvas(W,H);
function frame(s,t){const c=renderCanvas,g=c.getContext('2d');g.clearRect(0,0,W,H);
 if(s.title){const z=1.025+t*.008;g.drawImage(titleArt,(W-W*z)/2,(H-H*z)/2,W*z,H*z);const shade=g.createLinearGradient(0,0,W,0);shade.addColorStop(0,'#030816f5');shade.addColorStop(.57,'#030816c0');shade.addColorStop(1,'#03081610');g.fillStyle=shade;g.fillRect(0,0,W,H);
  // Precisely typeset title, a traveling metallic glint, particles and portal rings.
  const intro=Math.min(1,t/.8),zoom=1.07-.07*intro;g.save();g.translate(690,500);g.scale(zoom,zoom);g.translate(-690,-500);g.globalAlpha=intro;
  const glint=g.createLinearGradient(70+t*260,0,500+t*260,0);glint.addColorStop(0,'#b69456');glint.addColorStop(.5,'#fff9df');glint.addColorStop(1,'#d4b573');
  g.font='bold 102px Georgia';g.fillStyle=glint;g.shadowBlur=28;g.shadowColor='#e9c88466';g.fillText('DUAL-REALITY',112,420);g.font='bold 143px Georgia';g.fillText('MAZE',112,570);g.shadowBlur=0;g.fillStyle='#c5a264';g.fillRect(116,622,710*intro,3);g.font='27px Georgia';g.fillStyle='#ead8ae';g.fillText('THE ARCHITECT’S OATH',116,681);g.restore();
  for(let j=0;j<60;j++){const x=(j*179+t*11)%W,y=H-((j*71+t*(25+j%11))%(H+60)),a=(.15+(j%5)/14)*Math.min(1,t);g.fillStyle=`rgba(${j%3?226:154},${j%3?194:132},${j%3?117:255},${a})`;g.beginPath();g.arc(x,y,1+j%3,0,Math.PI*2);g.fill();}
  if(!s.end){g.globalAlpha=Math.max(0,1-t/.45)*.7;g.fillStyle='#eae2ff';g.fillRect(0,0,W,H);g.globalAlpha=1;}
  if(s.end){text(g,'Two players. One shared adventure.',116,790,31,'#d7e2ef','left');g.font='22px Arial';g.fillStyle='#c0cedd';g.fillText('CHAPTERS I–III · PLAYABLE PROTOTYPE',116,900);g.fillStyle='#e1c18a';g.fillText('CHAPTERS IV–V · COMING SOON',116,940);g.fillStyle='#98adc3';g.font='18px Arial';g.fillText('Story, game design and workflow · Soham Basanwar',116,1010);}
 }
 else if(s.card){g.fillStyle='#030611';g.fillRect(0,0,W,H);const v=g.createRadialGradient(960,500,40,960,500,900);v.addColorStop(0,'#161627');v.addColorStop(1,'#030611');g.fillStyle=v;g.fillRect(0,0,W,H);g.globalAlpha=Math.max(0,Math.min(1,t/.5,(s.duration-t)/.5));const size=68,spacing=110,base=520-(s.card.length-1)*spacing/2;for(let i=0;i<s.card.length;i++)text(g,s.card[i],960,base+i*spacing,size,'#e8d0a1');g.strokeStyle='#b8995c77';g.lineWidth=2;g.beginPath();g.moveTo(760,705);g.lineTo(1160,705);g.stroke();for(let j=0;j<36;j++){g.fillStyle='#bda36955';g.fillRect((j*337+t*3)%W,(j*173-t*5+H)%H,2,2);}g.globalAlpha=1;}
 else{if(s.quote){const fade=Math.min(1,t/.65,(s.duration-t)/.5);g.globalAlpha=fade;const gr=g.createLinearGradient(0,700,0,H);gr.addColorStop(0,'#02061100');gr.addColorStop(1,'#020611ee');g.fillStyle=gr;g.fillRect(0,700,W,380);text(g,s.quote,960,935,46);text(g,s.sub,960,1000,30,'#c6d1df');g.globalAlpha=1;}if(s.label){g.fillStyle='#05101dd9';g.fillRect(55,55,650,55);g.font='bold 22px Arial';g.fillStyle='#e8d0a1';g.fillText(s.label,78,91);}}
 return c;}
function encoder(file){const p=spawn(FF,['-hide_banner','-loglevel','error','-y','-threads','2','-f','rawvideo','-pix_fmt','rgba','-s',`${W}x${H}`,'-r',String(FPS),'-i','pipe:0','-an','-c:v','qtrle','-pix_fmt','argb',file],{windowsHide:true});let err='';p.stderr.on('data',d=>err+=d);const done=new Promise((ok,no)=>{p.on('exit',code=>code===0?ok():no(Error(err)));p.on('error',no)});return{p,done};}
for(const s of shots){
 if(process.argv.includes('--reuse-segments')){const existing=await fs.stat(path.join(B,s.id+'.mp4')).catch(()=>null);if(existing?.size>1000){console.log('Reusing '+s.id);continue;}}
 const visual=path.join(B,s.id+'-art.mov'),e=encoder(visual);for(let n=0;n<Math.round(s.duration*FPS);n++){const c=frame(s,n/FPS),d=c.getContext('2d').getImageData(0,0,W,H).data;if(!e.p.stdin.write(Buffer.from(d.buffer,d.byteOffset,d.byteLength)))await once(e.p.stdin,'drain');if(n===Math.round(FPS*s.duration/2))await fs.writeFile(path.join(B,s.id+'-review.jpg'),c.toBuffer('image/jpeg'));}e.p.stdin.end();await e.done;
 const args=['-hide_banner','-loglevel','error','-y','-threads','2'];if(s.file){if(s.seek)args.push('-ss',String(s.seek));args.push('-i',s.file);}else args.push('-i',visual);if(s.file)args.push('-i',visual);args.push('-f','lavfi','-i','anullsrc=r=48000:cl=stereo');
 let filter=s.file?'[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1[bg];[bg][1:v]overlay=0:0:shortest=1[v]':'[0:v]setsar=1[v]';
 const ai=s.file?2:1;if(s.native)filter+=';[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.53[a]';
 args.push('-filter_complex',filter,'-map','[v]','-map',s.native?'[a]':`${ai}:a`,'-t',String(s.duration),'-c:v','libx264','-threads','2','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-c:a','aac','-ar','48000','-b:a','192k',path.join(B,s.id+'.mp4'));
 execFileSync(FF,args,{windowsHide:true});console.log('Built '+s.id+' at '+s.start.toFixed(3)+'s');
}
const join=['-hide_banner','-loglevel','error','-y','-filter_complex_threads','2'];for(const s of shots)join.push('-threads','2','-i',path.join(B,s.id+'.mp4'));
const f=[];for(let i=0;i<shots.length;i++){f.push(`[${i}:v]settb=AVTB,setpts=PTS-STARTPTS,format=yuv420p,fps=24[v${i}]`);f.push(`[${i}:a]aresample=48000,atrim=duration=${shots[i].duration},apad=whole_dur=${shots[i].duration},atrim=duration=${shots[i].duration},asetpts=PTS-STARTPTS[a${i}]`);}
let pv='v0',pa='a0';for(let i=1;i<shots.length;i++){f.push(`[${pv}][v${i}]xfade=transition=fade:duration=${shots[i].cross}:offset=${shots[i].start},fps=24[x${i}]`);f.push(`[${pa}][a${i}]acrossfade=d=${shots[i].cross}:c1=tri:c2=tri[m${i}]`);pv='x'+i;pa='m'+i;}
f.push(`[${pv}]fade=t=in:d=0.45,fade=t=out:st=${duration-.6}:d=0.6,format=yuv420p[video]`);join.push('-filter_complex',f.join(';'),'-map','[video]','-map',`[${pa}]`,'-t',String(duration),'-c:v','libx264','-threads','4','-preset','fast','-crf','19','-c:a','aac','-ar','48000','-b:a','192k',path.join(B,'continuous-visuals-and-fx.mp4'));execFileSync(FF,join,{windowsHide:true,maxBuffer:8e6});console.log('Visual and ambience transitions joined.');
// Original musical score and trailer sound design. The opening is restrained; the
// title hits, rhythm accelerates, and the homecoming resolves the minor harmony.
const SR=48000,n=Math.ceil(duration*SR),wave=Buffer.alloc(44+n*4);wave.write('RIFF');wave.writeUInt32LE(36+n*4,4);wave.write('WAVEfmt ',8);wave.writeUInt32LE(16,16);wave.writeUInt16LE(1,20);wave.writeUInt16LE(2,22);wave.writeUInt32LE(SR,24);wave.writeUInt32LE(SR*4,28);wave.writeUInt16LE(4,32);wave.writeUInt16LE(16,34);wave.write('data',36);wave.writeUInt32LE(n*4,40);
const chords=[[73.416,110,146.832,174.614],[58.27,87.307,116.54,146.832],[65.406,98,130.813,164.814],[55,82.407,110,146.832]],beat=60/88,titleAt=shots[2].start,homeAt=shots.find(s=>s.id==='16_homecoming').start;let seed=362,lowNoise=0;
for(let i=0;i<n;i++){const t=i/SR,energy=t<5?.13:t<titleAt?Math.min(1,(t-5)/2):t<20?.48:t<40?.68:t<homeAt?1:.35,ch=t>=homeAt?[73.416,110,146.832,184.997]:chords[Math.floor(t/(beat*4))%4],bp=t%beat;seed=(seed*1664525+1013904223)>>>0;const noise=seed/4294967295*2-1;lowNoise=.97*lowNoise+.03*noise;let a=0;
 for(let k=0;k<4;k++){const freq=ch[k];a+=(Math.sin(2*Math.PI*freq*t)+.22*Math.sin(4*Math.PI*freq*t)+.1*Math.sin(6*Math.PI*freq*t))*.014*(.75+.25*Math.sin(t*.6+k));}
 const pn=ch[Math.floor(t/beat)%4]*4;for(let h=1;h<=4;h++)a+=Math.sin(2*Math.PI*pn*h*bp)*Math.exp(-bp*(3+h))*.025/(h*h);
 if(t>titleAt+4&&t<homeAt){const kick=t%(beat*2);a+=Math.sin(2*Math.PI*(42*kick+30*(1-Math.exp(-12*kick))/12))*Math.exp(-kick*11)*.13*energy;a+=noise*Math.exp(-bp*55)*.014*energy;}
 const rise=t-(titleAt-1.3);if(rise>=0&&rise<1.3)a+=lowNoise*(rise/1.3)**2*.6;
 for(const impact of [titleAt,shots.find(s=>s.id==='14_clockwork').start,shots.find(s=>s.id==='15_final_seal').start]){const q=t-impact;if(q>=0&&q<2){a+=Math.sin(2*Math.PI*(35*q+30*(1-Math.exp(-9*q))/9))*Math.exp(-q*4)*.23;a+=lowNoise*Math.exp(-q*9)*.25;}}
 const duck=shots.some(s=>s.voice&&t>s.start&&t<s.start+s.duration)? .48:t>1&&t<4.5?.35:1;a*=Math.min(1,t/1.2,(duration-t)/1.5)*duck;const value=Math.round(Math.max(-.95,Math.min(.95,a))*32767);wave.writeInt16LE(value,44+i*4);wave.writeInt16LE(Math.round(value*(.975+.02*Math.sin(t*.4))),46+i*4);}
await fs.writeFile(path.join(B,'cinematic-score.wav'),wave);
const mix=['-hide_banner','-loglevel','error','-y','-i',path.join(B,'continuous-visuals-and-fx.mp4'),'-i',path.join(B,'cinematic-score.wav'),'-i',path.join(R,'trailer-kit/voice/King-trailer-line.m4a')];for(const file of narrations)mix.push('-i',path.join(N,file));
const af=['[1:a]volume=0.82[score]','[2:a]adelay=1000|1000,volume=1.08[king]'];const tracks=['[0:a]','[score]','[king]'];for(let i=0;i<narrations.length;i++){const s=shots.find(s=>s.voice===narrations[i]),delay=Math.round((s.start+.5)*1000);af.push(`[${i+3}:a]highpass=f=65,lowpass=f=12000,aecho=0.8:0.8:90:0.13,adelay=${delay}|${delay},volume=1.02[n${i}]`);tracks.push(`[n${i}]`);}af.push(tracks.join('')+`amix=inputs=${tracks.length}:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=10[audio]`);
const final=path.join(O,'Dual_Reality_Maze_Cinematic_Trailer.mp4');mix.push('-filter_complex',af.join(';'),'-map','0:v','-map','[audio]','-c:v','copy','-c:a','aac','-ar','48000','-b:a','256k','-t',String(duration),'-movflags','+faststart',final);execFileSync(FF,mix,{windowsHide:true});
await fs.writeFile(path.join(B,'cinematic-manifest.json'),JSON.stringify({duration,width:W,height:H,fps:FPS,structure:'Quiet prologue → portal surge → animated game-title reveal → four fading narrated cards → growing action → coming-soon finale → homecoming',videoCreditCost:350,pixverseCreditsRemaining:920,narrator:'ElevenLabs Brian, deep/resonant voice, Eleven v4, existing free allowance',sourceDisclosure:'Chapters I–III prototype renderer captures are staged. Cinematic previews animate project artwork. Chapters IV–V and final homecoming are planned, labelled coming soon.',narrationDurations:nd,shots},null,2));console.log('FINISHED '+duration.toFixed(3)+' seconds: '+final);
