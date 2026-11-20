import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
const require=createRequire(import.meta.url);
const {createCanvas,loadImage}=require('C:/Users/soham/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@napi-rs/canvas');
const R=path.resolve(import.meta.dirname,'../..');
const c=createCanvas(1920,1080),g=c.getContext('2d');
g.fillStyle='#081321';g.fillRect(0,0,1920,1080);
function t(s,x,y,size,color='#F5E8CE'){g.fillStyle=color;g.font='bold '+size+'px Arial';g.fillText(s,x,y);}
t('The story continues',92,125,63);g.fillStyle='#D4AF68';g.fillRect(92,169,114,4);
for(const [i,f,chapter,title,lines]of [[0,'images/chapter4-title.png','CHAPTER IV','The Clockwork Citadel',['Restore the bell and reveal the Hollow King’s plan.','Rotating routes and timed machinery.']],[1,'images/chapter5-finale-concept.png','CHAPTER V','The Heart Beyond the Veil',['Break three bindings and reunite the heroes.','The Princess seals the throne. Homecoming follows.']]]){
 const x=92+i*882,im=await loadImage(path.join(R,f));g.drawImage(im,x,224,844,475);
 t(chapter,x,766,26,'#85BFE0');t(title,x,825,39);
 g.font='29px Arial';g.fillStyle='#B8C7D5';for(let j=0;j<lines.length;j++)g.fillText(lines[j],x,884+j*40);
 g.fillStyle='#203B50';g.fillRect(x+592,728,252,52);t('COMING SOON',x+615,763,25,'#D4AF68');
}
g.font='24px Arial';g.fillStyle='#B8C7D5';g.fillText('Planned chapters • concept artwork • Chapters I–III are playable in the current prototype',92,1025);
await fs.writeFile(path.join(R,'trailer-kit/full-story-v2/Upcoming_Chapters_IV_V.png'),c.toBuffer('image/png'));
console.log('Created upcoming-chapter artwork panel.');

