import fs from 'node:fs/promises';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {createRequire} from 'node:module';
const req=createRequire(import.meta.url),{createCanvas,loadImage}=req('C:/Users/soham/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@napi-rs/canvas');
const R=path.resolve(import.meta.dirname,'../..'),B=path.join(R,'trailer-kit/origin-v4'),O=path.join(R,'submission/Full_Story_Revision');
const FF='C:/Users/soham/AppData/Local/Temp/maze-trailer-tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe',movie=path.join(O,'Dual_Reality_Maze_Origin_Trailer.mp4');
const manifest=JSON.parse(await fs.readFile(path.join(B,'cinematic-manifest.json'),'utf8')),c=createCanvas(1600,Math.ceil(manifest.shots.length/3)*327),g=c.getContext('2d');g.fillStyle='#07111e';g.fillRect(0,0,c.width,c.height);
for(let i=0;i<manifest.shots.length;i++){const s=manifest.shots[i],t=s.start+s.duration*.53,p=path.join(B,s.id+'-final.jpg');execFileSync(FF,['-hide_banner','-loglevel','error','-y','-ss',String(t),'-i',movie,'-frames:v','1','-update','1',p],{windowsHide:true});const im=await loadImage(p),x=i%3*533,y=Math.floor(i/3)*327;g.drawImage(im,x,y,533,300);g.font='17px Arial';g.fillStyle='#d8bb80';g.fillText(s.id.replaceAll('_',' ')+' · '+t.toFixed(1)+'s',x+8,y+320);}
await fs.writeFile(path.join(O,'Origin_Trailer_Storyboard.jpg'),c.toBuffer('image/jpeg'));
execFileSync(FF,['-hide_banner','-loglevel','error','-y','-ss',String(manifest.shots.find(s=>s.id==='03_title_reveal').start+6.8),'-i',movie,'-frames:v','1','-update','1',path.join(O,'Origin_Trailer_Poster.png')],{windowsHide:true});console.log('Reviewed all '+manifest.shots.length+' shots; poster extracted from animated title reveal.');
