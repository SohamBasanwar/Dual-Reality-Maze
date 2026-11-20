import {spawn} from 'node:child_process';
import http from 'node:http';
import assert from 'node:assert/strict';
let active=0,maxActive=0,stall=false;
const board=http.createServer((req,res)=>{active++;maxActive=Math.max(active,maxActive);res.on('close',()=>active--);if(stall)return;setTimeout(()=>{res.setHeader('Content-Type','application/json');res.end(JSON.stringify(req.url==='/input'?{v:1,ms:42}:{ok:true}));},60);});
await new Promise(r=>board.listen(18089,'127.0.0.1',r));
const child=spawn(process.execPath,['hardware/arduino-system/server.mjs','--port=18088','--board=127.0.0.1','--board-port=18089'],{stdio:['ignore','pipe','pipe']});
const request=(url,options={})=>fetch('http://127.0.0.1:18088'+url,{...options,signal:AbortSignal.timeout(5000)});
try{
 await new Promise((resolve,reject)=>{const timer=setTimeout(()=>reject(Error('server did not start')),8000);child.stdout.once('data',()=>{clearTimeout(timer);resolve();});child.once('exit',()=>{clearTimeout(timer);reject(Error('server exited'));});});
 assert.equal((await request('/missing')).status,404);
 assert.equal((await request('/hub/state',{headers:{Origin:'https://unrelated.example'}})).status,403);
 assert.equal((await request('/hub/health')).status,200);
 assert.equal((await request('/hub/state',{method:'POST',body:'bad'})).status,400);
 assert.equal((await request('/hub/state',{method:'POST',body:'X'.repeat(81)})).status,413);
 const responses=await Promise.all([request('/hub/input'),request('/hub/state',{method:'POST',body:'S,0,0,100'}),request('/hub/input')]);
 assert(responses.every(r=>r.status===200));assert.equal(maxActive,1,'Main requests must be serialized');
 stall=true;const timed=await request('/hub/input');assert.equal(timed.status,502);assert.match((await timed.json()).error,/respond/);
 stall=false;assert.equal((await request('/hub/input')).status,200,'bridge must recover after a timeout');
 const game=await request('/');assert.equal(game.status,200);assert((await game.arrayBuffer()).byteLength>1000000);
 console.log('PASS: game/health routes, origin protection, feedback validation, serialized transport, timeout and recovery.');
}finally{child.kill();board.closeAllConnections();board.close();}
