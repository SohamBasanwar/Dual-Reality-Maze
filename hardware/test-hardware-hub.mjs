import vm from 'node:vm';import fs from 'node:fs';import assert from 'node:assert/strict';
const elements=new Map(),calls=[];let now=0,tick;
const element=id=>{if(!elements.has(id))elements.set(id,{value:300,checked:true,textContent:'',style:{}});return elements.get(id);};
const s={active:false,open:[true,false,false,false,false],selected:0,mode:'playing',remaining:597,player:{x:10,y:10}};
const ctx={document:{createElement:()=>({style:{},click(){}}),body:{append(){}},getElementById:element,hidden:false},window:{},performance:{now:()=>now},Date,Math,Number,JSON,console,Blob,URL,AbortSignal,TextEncoder,TextDecoder,navigator:{},setTimeout:()=>0,setInterval:f=>tick=f,forest:{...s},campaign:{...s},state:s,controllerState:{menu:false,neutralRequired:false},voiceEngine:{settingsOpen:false},controllerPlaying:()=>true,controllerDirection:d=>calls.push(['dir',d]),controllerPress:r=>calls.push(['press',r]),controllerPot:v=>calls.push(['pot',v]),controllerLine:(r,l)=>calls.push(['line',l]),setControllerMode(){},disconnectControllers:async()=>{},fetch:async()=>{throw Error('offline');}};
vm.createContext(ctx);vm.runInContext(fs.readFileSync('maze-source/work/story/hardware-hub.js','utf8'),ctx);
ctx.story={ready:true};ctx.splash={artReady:true};
const hub=ctx.window.mazeHardware,p={v:1,exchange:true,ms:100,eOK:true,aOK:true,x:512,y:512,light:700,pot:400,ep:0,ap:0};
assert(hub.accept(p));assert.equal(calls.filter(x=>x[0]==='press').length,0);
hub.accept({...p,ms:150,x:800,ep:1});hub.accept({...p,ms:200,x:800,ep:1});
assert.equal(calls.filter(x=>x[0]==='press').length,1);assert(calls.some(x=>x[0]==='dir'&&x[1]==='RIGHT'));
assert.equal(hub.feedback(),'S,1,1,597');
s.selected=1;assert.equal(hub.feedback(),'S,0,1,597','selecting a closed mechanism must close the physical servo');
s.open[1]=true;assert.equal(hub.feedback(),'S,1,1,597','opening the selected mechanism must open the servo');
s.open[1]=false;assert.equal(hub.feedback(),'S,0,1,597','closing the selected mechanism must close the servo');
s.selected=0;assert.equal(hub.feedback(),'S,1,1,597','returning to an open mechanism must restore its open position');
assert.equal(hub.accept({...p,x:1024}),false);
assert.equal(hub.config.dark,1000);assert.equal(hub.config.lightFitted,true);
for(const [light,on] of [[1023,false],[1000,false],[999,true],[980,true],[1000,false],[999,true]]){
 hub.accept({...p,light,ms:200});
 assert.equal(calls.filter(x=>x[0]==='line').at(-1)[1],`Light Level: ${light} -> ${on?'REVEAL ACTIVATED':'Normal'}`);
}
hub.accept({...p,ms:250,eOK:false,ep:50});hub.accept({...p,ms:300,ep:50});
assert.equal(calls.filter(x=>x[0]==='press').length,1,'reconnect must baseline counters');
hub.accept({...p,ms:1,ep:0,ap:0});assert.equal(calls.filter(x=>x[0]==='press').length,1,'reboot must baseline counters');
ctx.document.hidden=true;assert.equal(hub.feedback(),'S,0,0,597');ctx.document.hidden=false;
await element('hubWiFi').onclick();now=100;hub.accept({...p,ms:350});now=900;await tick();
assert(ctx.controllerState.neutralRequired,'watchdog must require neutral after disconnection');
assert.equal(calls.filter(x=>x[0]==='dir').at(-1)[1],'CENTER');
// A response already in flight must not re-enable movement after Disconnect.
let deliver;ctx.fetch=async()=>({ok:true,json:()=>new Promise(resolve=>deliver=resolve)});
const flight=tick();await Promise.resolve();await hub.disconnect();deliver({...p,x:900,ms:500});await flight;
assert.equal(calls.filter(x=>x[0]==='dir').at(-1)[1],'CENTER');
let joins=0;
ctx.fetch=async url=>{if(url==='/hub/connect'){joins++;return {ok:true,json:async()=>({message:'Join requested'})};}throw Error('Main offline');};
now=20000;await element('hubWiFi').onclick();assert.equal(joins,1);
now=40000;await tick();await tick();await new Promise(r=>setImmediate(r));assert.equal(joins,2,'repeated loss requests a rejoin');
await tick();await new Promise(r=>setImmediate(r));assert.equal(joins,2,'rejoin is rate limited');
await hub.disconnect();now=80000;await tick();assert.equal(joins,2,'Disconnect stops retries');
// Switching from Wi-Fi to USB must open the picker and assert the R4 CDC signals.
let signals,resolveRead,closed=false,firstRead=true;const writes=[];
const serialReader={read:()=>firstRead?(firstRead=false,Promise.resolve({done:false,value:new TextEncoder().encode(JSON.stringify(p)+'\n')})):new Promise(resolve=>resolveRead=resolve),cancel:async()=>{resolveRead?.({done:true});},releaseLock(){}};
ctx.navigator.serial={requestPort:async()=>({open:async()=>{},setSignals:async s=>signals=s,readable:{getReader:()=>serialReader},writable:{getWriter:()=>({write:async b=>writes.push(new TextDecoder().decode(b)),releaseLock(){}})},close:async()=>closed=true})};
now=100000;await element('hubWiFi').onclick();
const usb=element('hubUSB').onclick();await new Promise(r=>setImmediate(r));
assert.equal(signals.dataTerminalReady,true);assert.equal(signals.requestToSend,true);
await tick();assert(writes.some(s=>s.startsWith('S,')),'USB must transmit game feedback');
await hub.disconnect();await usb;assert(closed,'Disconnect must release the USB port');
console.log('PASS: packet validation, movement, counters, feedback, exact 1000 Reveal boundary, stale-input release, late-response cancellation, rate-limited reconnect and cancellation.');
