import fs from 'node:fs/promises';
import path from 'node:path';
import {execFileSync,spawnSync} from 'node:child_process';
import {createRequire} from 'node:module';
const req=createRequire(import.meta.url);
const {createCanvas,loadImage}=req('C:/Users/soham/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@napi-rs/canvas');
const root=path.resolve(import.meta.dirname,'../..'),out=import.meta.dirname;
const ff='C:/Users/soham/AppData/Local/Temp/maze-trailer-tools/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe';
await fs.mkdir(path.join(out,'generated'),{recursive:true});
await fs.mkdir(path.join(out,'qa'),{recursive:true});
const specs=[['opening','OPENING'],['chapter2','CHAPTER_II_'],['chapter3','CHAPTER_III_'],['chapter4','CHAPTER_IV_'],['chapter5','CHAPTER_V_'],['homecoming','ENDING']];
const downloads='C:/Users/soham/Downloads',files=await fs.readdir(downloads),manifest=[];
const sheet=createCanvas(1440,6*310+80),g=sheet.getContext('2d');g.fillStyle='#081321';g.fillRect(0,0,sheet.width,sheet.height);g.fillStyle='#f5e8ce';g.font='bold 30px Arial';g.fillText('Full-story trailer: watermark-free export review',25,48);
for(let i=0;i<specs.length;i++){
 const [id,prefix]=specs[i],candidates=files.filter(n=>n.startsWith('PixVerse_V6_Image_Text_720P_'+prefix)&&n.endsWith('.mp4'));
 if(candidates.length!==1)throw Error('Ambiguous export for '+id+': '+candidates);
 const source=path.join(downloads,candidates[0]),dest=path.join(out,'generated',id+'.mp4');await fs.copyFile(source,dest);
 const probe=spawnSync(ff,['-hide_banner','-i',dest],{encoding:'utf8',windowsHide:true});
 if(!probe.stderr.includes('Audio:'))throw Error('Missing generated sound: '+id);
 const duration=probe.stderr.match(/Duration: ([\d:.]+)/)?.[1];
 const frames=[];
 for(let j=0;j<3;j++){
  const img=path.join(out,'qa',`${id}-${j}.jpg`);execFileSync(ff,['-hide_banner','-loglevel','error','-y','-ss',String(.2+j*2),'-i',dest,'-frames:v','1','-update','1',img],{windowsHide:true});
  const im=await loadImage(img);const x=j*480,y=80+i*310;g.drawImage(im,x,y,480,270);frames.push(img);
 }
 g.fillStyle='#c6d5e5';g.font='21px Arial';g.fillText(id+' · '+duration+' · source 720p · audio present',15,80+i*310+296);
 manifest.push({id,file:'generated/'+id+'.mp4',provider:'PixVerse V6',settings:'720p, 5 seconds, audio enabled, multi-shot disabled, preview disabled',credits:50,export:'Watermark-free selected in provider UI',duration,probe:probe.stderr});
 console.log(id+': copied, audio present, review frames extracted');
}
await fs.writeFile(path.join(out,'qa','generated-contact-sheet.jpg'),sheet.toBuffer('image/jpeg'));
await fs.writeFile(path.join(out,'generated-manifest.json'),JSON.stringify({startingCredits:1270,usedCredits:300,remainingCredits:970,shots:manifest},null,2));
