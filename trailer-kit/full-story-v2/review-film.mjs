import fs from 'node:fs/promises';
import path from 'node:path';
import {execFileSync} from 'node:child_process';
import {createRequire} from 'node:module';
const req=createRequire(import.meta.url),{createCanvas,loadImage}=req('C:/Users/soham/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@napi-rs/canvas');
const R=path.resolve(import.meta.dirname,'../..'),movie=path.join(R,'submission/Full_Story_Revision/Dual_Reality_Maze_Full_Story_Trailer.mp4');
const ff='C:/Users/soham/AppData/Local/Temp/maze-trailer-tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe';
const c=createCanvas(1920,1540),g=c.getContext('2d');g.fillStyle='#07111e';g.fillRect(0,0,1920,1540);
for(const [i,t]of [1.5,6.2,12.5,15.5,18.5,23,27,31,36.5,41.5,46.5,51.5].entries()){
 const p=path.join(import.meta.dirname,'qa','film-'+i+'.jpg');execFileSync(ff,['-hide_banner','-loglevel','error','-y','-ss',String(t),'-i',movie,'-frames:v','1','-update','1',p],{windowsHide:true});
 const im=await loadImage(p),x=i%3*640,y=Math.floor(i/3)*385;g.drawImage(im,x,y,640,360);g.font='18px Arial';g.fillStyle='#d8bb80';g.fillText(t.toFixed(1)+' sec',x+12,y+380);
}
await fs.writeFile(path.join(R,'submission/Full_Story_Revision/Trailer_Storyboard.jpg'),c.toBuffer('image/jpeg'));
const builder=path.join(import.meta.dirname,'build-film.mjs');let source=await fs.readFile(builder,'utf8');source=source.replace("'-b:a','256k','-t'","'-b:a','256k','-ar','48000','-t'");await fs.writeFile(builder,source);
console.log('12 timestamped final frames saved; source builder now exports 48 kHz audio.');
