import fs from 'node:fs/promises';
import path from 'node:path';
import {createRequire} from 'node:module';
import {originTitle} from './origin-title.mjs';
const {createCanvas,loadImage}=createRequire(import.meta.url)('C:/Users/soham/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@napi-rs/canvas');
const R=path.resolve(import.meta.dirname,'../..'),art=await loadImage(path.join(R,'images/title-screen.png')),out=createCanvas(1280,1080),g=out.getContext('2d'),c=createCanvas(1920,1080),cg=c.getContext('2d');
for(const [i,t] of [1.7,3.7,5.5,7.5].entries()){originTitle(cg,art,t,1920,1080);g.drawImage(c,i%2*640,Math.floor(i/2)*540,640,360);g.fillStyle='#e6ca96';g.font='24px Arial';g.fillText(t+' seconds',i%2*640+15,Math.floor(i/2)*540+400);}
await fs.writeFile(path.join(R,'trailer-kit/origin-v4/title-animation-proof.jpg'),out.toBuffer('image/jpeg'));
