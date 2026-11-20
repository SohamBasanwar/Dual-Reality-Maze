import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
const exec=promisify(execFile),root=path.dirname(fileURLToPath(import.meta.url));
const arg=(name,fallback)=>process.argv.find(a=>a.startsWith(`--${name}=`))?.slice(name.length+3)||fallback;
const board=arg('board','192.168.4.1'),port=Number(arg('port','8080')),boardPort=Number(arg('board-port','80'));
if(!/^\d{1,3}(\.\d{1,3}){3}$/.test(board)||board.split('.').some(n=>Number(n)>255))throw Error('Invalid Main IPv4 address.');
for(const n of [port,boardPort])if(!Number.isInteger(n)||n<1||n>65535)throw Error('Invalid port.');
const json=(res,status,data)=>{if(res.destroyed)return;res.writeHead(status,{'Content-Type':'application/json','Cache-Control':'no-store'});res.end(JSON.stringify(data));};
let queue=Promise.resolve(),waiting=0,joining=null,lastJoin=0;
// Main has one small HTTP server: serialize input and feedback, with a bounded queue.
function boardRequest(route){
 if(waiting>=4)return Promise.reject(Error('Main is busy; retry shortly.'));
 waiting++;
 const result=queue.then(()=>new Promise((resolve,reject)=>{
  const req=http.get({host:board,port:boardPort,path:route,agent:false,headers:{Connection:'close'}},r=>{
   let body='';r.setEncoding('utf8');r.on('data',b=>{body+=b;if(body.length>8192)req.destroy(Error('Unexpected Main response.'));});
   r.on('error',reject);r.on('end',()=>{try{if(r.statusCode!==200)throw Error(`Main HTTP ${r.statusCode}`);resolve(JSON.parse(body));}catch(e){reject(e);}});
  });
  const timer=setTimeout(()=>req.destroy(Error('Main did not respond. Check power and Wi-Fi.')),1300);
  req.on('error',reject);req.on('close',()=>clearTimeout(timer));
 }));
 queue=result.catch(()=>{}).finally(()=>waiting--);return result;
}
async function network(){
 if(process.platform!=='win32')return {supported:false,onMaze:false,message:'Join DualRealityMaze in your operating system Wi-Fi settings.'};
 const {stdout}=await exec('netsh',['wlan','show','interfaces'],{windowsHide:true,timeout:5000,maxBuffer:65536});
 return {supported:true,onMaze:/^\s*SSID\s*:\s*DualRealityMaze\s*$/m.test(stdout)};
}
async function joinNetwork(){
 if(joining)return joining;
 joining=(async()=>{
  const n=await network();if(n.onMaze)return {...n,requested:false,message:'Laptop is on DualRealityMaze. Waiting for Main.'};
  if(!n.supported)return n;
  if(Date.now()-lastJoin<15000)return {...n,requested:false,message:'Waiting before retrying Wi-Fi. Check Main power.'};
  lastJoin=Date.now();
  try{await exec('netsh',['wlan','connect','name=DualRealityMaze','ssid=DualRealityMaze'],{windowsHide:true,timeout:6000,maxBuffer:65536});}
  catch{throw Error('Could not join DualRealityMaze. Connect once in Windows Wi-Fi using password MazeDemo362, then retry.');}
  return {supported:true,onMaze:false,requested:true,message:'Wi-Fi join requested. Keep Main powered; connection may take a few seconds.'};
 })().finally(()=>joining=null);return joining;
}
async function handle(req,res){
 const hosts=[`localhost:${port}`,`127.0.0.1:${port}`];
 if(!hosts.includes(req.headers.host)||req.headers.origin&&!hosts.some(h=>req.headers.origin===`http://${h}`))return json(res,403,{error:'Local game requests only.'});
 try{
  if(req.url==='/hub/health'&&req.method==='GET')return json(res,200,{service:'dual-reality-maze',version:2,board,root});
  if(req.url==='/hub/network'&&req.method==='GET')return json(res,200,await network());
  if(req.url==='/hub/connect'&&req.method==='POST')return json(res,200,await joinNetwork());
  if(req.url==='/hub/input'&&req.method==='GET')return json(res,200,await boardRequest('/input'));
  if(req.url==='/hub/state'&&req.method==='POST'){
   let s='';for await(const b of req){s+=b;if(s.length>80)return json(res,413,{error:'Feedback too large.'});}
   if(!/^S,[01],[012],\d{1,5}$/.test(s))return json(res,400,{error:'Invalid game feedback.'});
   return json(res,200,await boardRequest('/state?cmd='+s));
  }
  if((req.url==='/'||req.url==='/game.html')&&req.method==='GET'){
   res.writeHead(200,{'Content-Type':'text/html; charset=utf-8','Cache-Control':'no-store'});
   const stream=fs.createReadStream(path.join(root,'game.html'));stream.on('error',()=>res.destroy());stream.pipe(res);return;
  }
  json(res,404,{error:'Not found.'});
 }catch(e){json(res,502,{error:e.message});}
}
http.createServer(handle).listen(port,'127.0.0.1',()=>console.log(`Maze bridge ready: http://127.0.0.1:${port} — Main ${board}`));
