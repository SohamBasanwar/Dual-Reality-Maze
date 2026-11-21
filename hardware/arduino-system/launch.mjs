import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import {fileURLToPath} from 'node:url';
import {spawn,execFileSync} from 'node:child_process';
const root=path.dirname(fileURLToPath(import.meta.url)),url='http://127.0.0.1:8080';
const delay=ms=>new Promise(r=>setTimeout(r,ms));
async function health(){
 try{
  const r=await fetch(url+'/hub/health',{signal:AbortSignal.timeout(800)});
  const p=await r.json().catch(()=>({}));
  if(p.service!=='dual-reality-maze'||p.version!==3||path.resolve(p.root||'').toLowerCase()!==root.toLowerCase())throw Error('Port 8080 is occupied by another or older bridge. Close that bridge and launch again.');
  return true;
 }catch(e){if(e.message.startsWith('Port 8080'))throw e;return false;}
}
try{
 if(!fs.existsSync(path.join(root,'game.html'))){
  const builder=path.resolve(root,'../build-hardware-game.mjs');
  const source=path.resolve(root,'../../Dual_Reality_Maze_Story_Edition.html');
  if(!fs.existsSync(builder)||!fs.existsSync(source))throw Error('Game source is missing. Clone the complete repository and run git lfs pull.');
  const sourceFd=fs.openSync(source,'r'),prefix=Buffer.alloc(120);fs.readSync(sourceFd,prefix,0,120,0);fs.closeSync(sourceFd);
  if(prefix.toString().startsWith('version https://git-lfs.github.com/spec/v1'))throw Error('Large game file has not downloaded. Run git lfs pull in the project folder, then launch again.');
  console.log('Preparing the hardware game for first launch...');
  execFileSync(process.execPath,[builder],{windowsHide:true,stdio:'inherit'});
 }
 for(const file of ['server.mjs','game.html'])if(!fs.existsSync(path.join(root,file)))throw Error(`Missing ${file}. Keep the complete arduino-system folder together.`);
 if(process.argv.includes('--check')){console.log('Ready: Node, game and hardware bridge found.');process.exit(0);}
 if(!await health()){
  const logdir=path.join(process.env.LOCALAPPDATA||os.tmpdir(),'DualRealityMaze');fs.mkdirSync(logdir,{recursive:true});
  const fd=fs.openSync(path.join(logdir,'bridge.log'),'a');
  const child=spawn(process.execPath,[path.join(root,'server.mjs')],{cwd:root,detached:true,windowsHide:true,stdio:['ignore',fd,fd]});
  child.on('error',e=>console.error(e.message));child.unref();fs.closeSync(fd);
  let ready=false;for(let n=0;n<25;n++){await delay(300);if(await health()){ready=true;break;}}
  if(!ready)throw Error(`Bridge did not start. See ${path.join(logdir,'bridge.log')}.`);
 }
 if(!process.argv.includes('--no-browser'))execFileSync('powershell.exe',['-NoProfile','-NonInteractive','-Command',`Start-Process '${url}/'`],{windowsHide:true,stdio:'ignore'});
 console.log(`Game ready: ${url}/ — use Connect Main Wi-Fi in the game.`);
}catch(e){console.error(e.message);process.exitCode=1;}
