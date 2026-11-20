import fs from 'node:fs/promises';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {createRequire} from 'node:module';
const req=createRequire(import.meta.url),{createCanvas,loadImage}=req('C:/Users/soham/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@napi-rs/canvas');
const R=path.resolve(import.meta.dirname,'../..'),B=import.meta.dirname,O=path.join(R,'submission/Full_Story_Revision');
const ff='C:/Users/soham/AppData/Local/Temp/maze-trailer-tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe';
await fs.mkdir(O,{recursive:true});await fs.mkdir(path.join(B,'edit'),{recursive:true});
const W=1920,H=1080,FPS=24;
const shots=[
 {id:'01_oath',file:'images/sleeping-princess.png',still:true,duration:4,head:'A KINGDOM WAITING. A PROMISE MADE.',title:'“Bring my daughter home.”',subtitle:'“I am counting on you.”',type:'Existing game character artwork',voice:true},
 {id:'02_portal',file:'trailer-kit/full-story-v2/generated/opening.mp4',duration:5,head:'THE ARCHITECT’S OATH',title:'Two heroes. One path.',type:'Cinematic preview from game artwork',native:true},
 {id:'03_promise',duration:1.5,card:true,head:'A COOPERATIVE FANTASY ADVENTURE',title:'One explores. One shapes the way.'},
 {id:'04_maze',file:'trailer-kit/clips/01_maze_and_architect.mp4',duration:4,head:'CHAPTER I · THE ARCHITECT’S OATH',title:'Move together. Open the way.',type:'Prototype gameplay · staged capture'},
 {id:'05_transform',file:'trailer-kit/clips/02_architect_transformation.mp4',duration:2,head:'BECOME THE WAY FORWARD',type:'In-game cinematic · staged capture'},
 {id:'06_sky',file:'trailer-kit/full-story-v2/generated/chapter2.mp4',duration:5,head:'CHAPTER II · THE ALCHEMIST’S CURE',title:'A cure beyond the clouds.',type:'Cinematic preview from game artwork',native:true},
 {id:'07_flight',file:'trailer-kit/clips/04_dragon_flight.mp4',duration:3,head:'TAKE TO THE SKY',type:'In-game cinematic · staged capture'},
 {id:'08_forest',file:'trailer-kit/full-story-v2/generated/chapter3.mp4',duration:5,head:'CHAPTER III · FOREST OF LOST MEMORIES',title:'Find what the forest remembers.',type:'Cinematic preview from game artwork',native:true},
 {id:'09_memory',file:'trailer-kit/clips/06_memory_in_the_jar.mp4',duration:3,head:'CARRY HER MEMORIES HOME',type:'In-game cinematic · staged capture'},
 {id:'10_beyond',duration:1.5,card:true,head:'THE STORY CONTINUES',title:'The oath is only the beginning.'},
 {id:'11_citadel',file:'trailer-kit/full-story-v2/generated/chapter4.mp4',duration:5,head:'CHAPTER IV · THE CLOCKWORK CITADEL',title:'Restore the bell. Reveal the truth.',type:'Coming soon · concept cinematic',native:true},
 {id:'12_seal',file:'trailer-kit/full-story-v2/generated/chapter5.mp4',duration:5,head:'CHAPTER V · THE HEART BEYOND THE VEIL',title:'Break the bindings. Seal the throne.',type:'Coming soon · concept cinematic',native:true},
 {id:'13_home',file:'trailer-kit/full-story-v2/generated/homecoming.mp4',duration:5,head:'A PROMISE CARRIED HOME',title:'Every path led here.',type:'Planned story conclusion · concept preview',native:true},
 {id:'14_end',duration:5,card:true,end:true,head:'THE ARCHITECT’S OATH',title:'DUAL-REALITY MAZE',subtitle:'Two players. One shared adventure.'}
];
let cursor=0;for(const s of shots){s.start=cursor;cursor+=s.duration;}const duration=cursor;
function type(g,t,x,y,size,color='#f7eacd',align='center',family='Georgia'){g.save();g.font=`bold ${size}px ${family}`;g.fillStyle=color;g.textAlign=align;g.shadowBlur=10;g.shadowColor='#000b';g.fillText(t,x,y);g.restore();}
for(const s of shots){
 const c=createCanvas(W,H),g=c.getContext('2d');
 if(s.card){g.fillStyle='#07111e';g.fillRect(0,0,W,H);const gr=g.createRadialGradient(960,500,80,960,500,1000);gr.addColorStop(0,'#203047');gr.addColorStop(1,'#07111e');g.fillStyle=gr;g.fillRect(0,0,W,H);g.strokeStyle='#b99557';g.lineWidth=2;g.strokeRect(65,65,W-130,H-130);for(let i=0;i<100;i++){g.fillStyle=`rgba(212,175,104,${.12+(i%7)/30})`;g.fillRect((i*719)%W,(i*349)%H,2,2);}type(g,s.head,960,350,27,'#d8bb80','center','Arial');g.fillStyle='#c5a264';g.fillRect(820,395,280,2);type(g,s.title,960,535,s.end?95:60);if(s.subtitle)type(g,s.subtitle,960,635,37,'#b7ccdc');if(s.end){type(g,'CHAPTERS I–III · PLAYABLE PROTOTYPE',960,790,24,'#cbd8e3','center','Arial');type(g,'CHAPTERS IV–V · COMING SOON',960,835,24,'#d8bb80','center','Arial');type(g,'Story, game design and workflow · Soham Basanwar',960,945,22,'#9cb1c4','center','Arial');}}
 else{const gr=g.createLinearGradient(0,740,0,H);gr.addColorStop(0,'#02071300');gr.addColorStop(1,'#020713f0');g.fillStyle=gr;g.fillRect(0,740,W,340);g.fillStyle='#07111ec9';g.fillRect(0,0,W,92);type(g,s.head,76,59,24,'#f4ddb0','left','Arial');if(s.title)type(g,s.title,960,s.subtitle?885:944,48);if(s.subtitle)type(g,s.subtitle,960,950,35,'#cbd8e3');type(g,s.type,960,1040,20,'#bfd0df','center','Arial');}
 const overlay=path.join(B,'edit',s.id+'.png');await fs.writeFile(overlay,c.toBuffer('image/png'));
 const args=['-hide_banner','-loglevel','error','-y'];
 if(s.card)args.push('-loop','1','-i',overlay);else{if(s.still)args.push('-loop','1');args.push('-i',path.join(R,s.file),'-loop','1','-i',overlay);}
 const soundIndex=s.card?1:2;args.push('-f','lavfi','-i','anullsrc=r=48000:cl=stereo');
 let filters=s.card?'[0:v]format=yuv420p[v0]':'[0:v]scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1[bg];[bg][1:v]overlay=0:0:shortest=1[v0]';
 filters+=`;[v0]fps=${FPS},fade=t=in:d=0.16,fade=t=out:st=${s.duration-.16}:d=0.16[v]`;
 if(s.native)filters+=`;[0:a]aformat=sample_rates=48000:channel_layouts=stereo,volume=0.58,afade=t=in:d=0.13,afade=t=out:st=${s.duration-.2}:d=0.2[a]`;
 args.push('-filter_complex',filters,'-map','[v]','-map',s.native?'[a]':`${soundIndex}:a`,'-t',String(s.duration),'-c:v','libx264','-preset','veryfast','-crf','19','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart',path.join(B,'edit',s.id+'.mp4'));
 execFileSync(ff,args,{windowsHide:true});console.log('Edited '+s.id+' ('+s.duration+'s)');
}
await fs.writeFile(path.join(B,'edit','concat.txt'),shots.map(s=>`file '${s.id}.mp4'`).join('\n'));
execFileSync(ff,['-hide_banner','-loglevel','error','-y','-f','concat','-safe','0','-i',path.join(B,'edit','concat.txt'),'-c','copy',path.join(B,'edit','visuals-and-fx.mp4')],{windowsHide:true});
// Original stereo score: a quiet oath, a growing pulse, and a warm major resolution.
// All notes and synthesized instruments originate here; no stock recording is used.
const SR=44100,n=Math.ceil(duration*SR),wav=Buffer.alloc(44+n*4);wav.write('RIFF');wav.writeUInt32LE(36+n*4,4);wav.write('WAVEfmt ',8);wav.writeUInt32LE(16,16);wav.writeUInt16LE(1,20);wav.writeUInt16LE(2,22);wav.writeUInt32LE(SR,24);wav.writeUInt32LE(SR*4,28);wav.writeUInt16LE(4,32);wav.writeUInt16LE(16,34);wav.write('data',36);wav.writeUInt32LE(n*4,40);
const chords=[[146.832,174.614,220,293.665],[116.541,146.832,174.614,233.082],[130.813,164.814,196,261.626],[110,146.832,164.814,220]],beat=60/84;let seed=362;
for(let i=0;i<n;i++){
 const t=i/SR,bar=Math.floor(t/(beat*4)),ch=t>=44?[146.832,184.997,220,293.665]:chords[bar%4],bp=t%beat,energy=t<9?.25:t<32.5?.6:t<44?1:.4;
 let a=0;for(let k=0;k<4;k++){const f=ch[k],v=Math.sin(2*Math.PI*f*t+.004*Math.sin(2*Math.PI*4.8*t))+.25*Math.sin(4*Math.PI*f*t)+.1*Math.sin(6*Math.PI*f*t);a+=v*.015*(.8+.2*Math.sin(t*.7+k));}
 const note=ch[Math.floor(t/beat)%4]*2;for(let h=1;h<5;h++)a+=Math.sin(2*Math.PI*note*h*bp)*Math.exp(-bp*(3+h))*0.025/(h*h);
 if(t>10.5&&t<44){const b=t%(beat*2);a+=Math.sin(2*Math.PI*(42*b+38*(1-Math.exp(-12*b))/12))*Math.exp(-b*10)*.11*energy;seed=(seed*1664525+1013904223)>>>0;const noise=seed/4294967295*2-1;a+=noise*Math.exp(-bp*65)*.015*energy;if(t>32.5)a+=Math.sin(2*Math.PI*72*bp)*Math.exp(-bp*16)*.025;}
 a*=Math.min(1,t/1.5,(duration-t)/2)*(.8+energy*.2)*(t<4?.35:1);const val=Math.round(Math.max(-.95,Math.min(.95,a))*32767);wav.writeInt16LE(val,44+i*4);wav.writeInt16LE(Math.round(val*(.97+.02*Math.sin(t*.4))),46+i*4);
}
await fs.writeFile(path.join(B,'original-score.wav'),wav);
execFileSync(ff,['-hide_banner','-loglevel','error','-y','-i',path.join(B,'edit','visuals-and-fx.mp4'),'-i',path.join(B,'original-score.wav'),'-i',path.join(R,'trailer-kit/voice/King-trailer-line.m4a'),'-filter_complex',`[1:a]volume=0.72[m];[2:a]adelay=400|400,volume=1.15[v];[0:a][m][v]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=9[a]`,'-map','0:v','-map','[a]','-c:v','copy','-c:a','aac','-b:a','256k','-ar','48000','-t',String(duration),'-movflags','+faststart',path.join(O,'Dual_Reality_Maze_Full_Story_Trailer.mp4')],{windowsHide:true});
await fs.writeFile(path.join(B,'edit-manifest.json'),JSON.stringify({duration,width:W,height:H,fps:FPS,generatedSourceResolution:'720p; resized to 1080p delivery frame without watermark removal or invented detail',generatedCreditCost:300,creditsRemainingAfterBatch:970,gameCapture:'Staged animation using unmodified game canvas renderers, not a recorded player completing levels',audio:'PixVerse scene sound effects; original synthesized score; existing Clipchamp Adam Multilingual King line',shots},null,2));
console.log('FINISHED '+duration+' seconds: '+path.join(O,'Dual_Reality_Maze_Full_Story_Trailer.mp4'));
