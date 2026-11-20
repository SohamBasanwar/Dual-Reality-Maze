import http from 'node:http';
import fs from 'node:fs';
const html=fs.readFileSync(new URL('./index.html',import.meta.url));
const log=fs.createWriteStream(new URL('./wifi-live.jsonl',import.meta.url),{flags:'a'});
let tail=Promise.resolve();
function board(path){
 const run=tail.then(async()=>{
  const t=Date.now();
  const r=await fetch('http://192.168.4.1'+path,{signal:AbortSignal.timeout(2200),headers:{Connection:'close'}});
  if(!r.ok)throw Error('Board HTTP '+r.status);
  const data=await r.json();
  const result={receivedAt:new Date().toISOString(),latencyMs:Date.now()-t,...data};
  log.write(JSON.stringify({path,...result})+'\n');
  return result;
 });
 tail=run.catch(()=>{});
 return run;
}
http.createServer(async(req,res)=>{
 res.setHeader('Cache-Control','no-store');
 const origin=req.headers.origin;
 if(origin&&origin!=='http://127.0.0.1:8086'&&origin!=='http://localhost:8086'){res.writeHead(403);res.end();return;}
 if(req.method==='GET'&&req.url==='/'){res.setHeader('Content-Type','text/html');res.end(html);return;}
 let path;
 if(req.method==='GET'&&req.url==='/api/status')path='/';
 if(req.method==='POST'&&req.url==='/api/sweep')path='/servo?cmd=sweep';
 if(req.method==='POST'&&req.url==='/api/stop')path='/servo?cmd=stop';
 if(!path){res.writeHead(404);res.end();return;}
 try{const result=await board(path);res.setHeader('Content-Type','application/json');res.end(JSON.stringify(result));}
 catch(e){log.write(JSON.stringify({time:new Date().toISOString(),path,error:e.message})+'\n');res.writeHead(502,{'Content-Type':'application/json'});res.end(JSON.stringify({error:e.message}));}
}).listen(8086,'127.0.0.1',()=>console.log('Live hardware test: http://127.0.0.1:8086'));
