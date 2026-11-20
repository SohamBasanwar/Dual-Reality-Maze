// Main-board transport; shares the game's existing controller rules and scene locks.
(()=>{
 const cfg={cx:499,cy:527,dead:150,invertX:false,invertY:false,dark:1000,darkLow:true,lightFitted:true,potFitted:true};
 let active='',port,reader,writer,busy=false,last=0,prior=null,latest=null,session=0,reconnectAt=0,joining=false,failures=0;
 const history=[],events=[];
 const ui=document.createElement('details');ui.open=true;ui.id='mazeHub';
 ui.style.cssText='position:fixed;bottom:12px;left:12px;z-index:10000;background:#142031f5;color:#f4efdf;padding:12px;border:1px solid #b9a46d;border-radius:12px;width:min(470px,calc(100vw - 48px));max-height:70vh;overflow:auto;box-shadow:0 8px 32px #0008;font:14px/1.45 system-ui';
 ui.innerHTML=`<summary style="cursor:pointer;color:#e1c98b;font-weight:700">Main Arduino connection</summary>
 <style>#mazeHub button{background:#22354b;color:#f4efdf;border:1px solid #9e8958;border-radius:6px;padding:6px 8px;margin:2px 0;cursor:pointer}#mazeHub button:hover{background:#354d67}#mazeHub #hubWiFi{background:#d4b577;color:#142031;font-weight:700}#mazeHub input{accent-color:#d4b577}.app.controller-mode #titleQuickPlay{display:inline-block!important}</style>
 <p>Power all three boards, then connect here. Once connected, fold this panel and choose <b>Begin Adventure</b> or <b>Skip the prologue · Play</b>.</p>
 <p><button id="hubWiFi">Connect Main Wi-Fi</button> <button id="hubUSB">Connect Main USB</button> <button id="hubStop">Disconnect</button></p>
 <p style="font-size:12px">Wi-Fi: <b>DualRealityMaze</b> · password <b>MazeDemo362</b><br>The button joins Main's network on Windows. This network has no Internet; the game runs locally. If Windows asks, stay connected.</p>
 <p><label><input id="hubRecover" type="checkbox" checked> Rejoin Main Wi-Fi after a connection loss</label></p>
 <p><button id="hubCentre">Calibrate centred joystick</button> <label><input id="hubIX" type="checkbox">Invert X</label> <label><input id="hubIY" type="checkbox">Invert Y</label></p>
 <p><label><input type="checkbox" id="hubLightFitted" checked> Photoresistor fitted</label> <label><input type="checkbox" id="hubPotFitted" checked> Potentiometer fitted</label></p>
 <p>Reveal below <input id="hubDark" type="number" min="0" max="1023" value="1000" style="width:65px"> <label><input id="hubLow" type="checkbox" checked>Dark reads lower</label></p>
 <pre id="hubValues" style="white-space:pre-wrap">Not connected. Choose Wi-Fi or USB above.</pre><p id="hubNetwork" style="font-size:12px"></p>
 <button id="hubFold">Fold connection panel</button> <button id="hubLog">Download diagnostic log</button>`;
 document.body.append(ui);
 const el=id=>document.getElementById(id),note=s=>el('hubValues').textContent=s;
 el('openMainConnection').onclick=()=>{closeControllerMenu();ui.open=true;};
 function event(message){events.push({time:new Date().toISOString(),message});if(events.length>200)events.shift();}
 function stopMovement(){controllerDirection('CENTER');controllerState.neutralRequired=true;}
 function feedback(){const s=forest.active?forest:campaign.active?campaign:state;const playing=controllerPlaying()&&!document.hidden&&!controllerState.menu&&!voiceEngine.settingsOpen;return `S,${playing&&s.open?.[s.selected]?1:0},${playing?1:s.mode==='paused'?2:0},${Math.max(0,Math.min(36000,Math.ceil(s.remaining||0)))}`;}
 function accept(p){
  if(p.v!==1||typeof p.eOK!=='boolean'||typeof p.aOK!=='boolean'||!['x','y','light','pot'].every(k=>Number.isInteger(p[k])&&p[k]>=0&&p[k]<=1023)||!['ep','ap'].every(k=>Number.isInteger(p[k])&&p[k]>=0&&p[k]<=65535)||!Number.isFinite(p.ms))return false;
  last=performance.now();latest=p;if(prior&&p.ms<prior.ms){prior=null;stopMovement();event('Main restarted; controls require neutral.');}
  if(p.eOK){
   let dx=(p.x-cfg.cx)*(cfg.invertX?-1:1),dy=(p.y-cfg.cy)*(cfg.invertY?-1:1);
   const dir=Math.max(Math.abs(dx),Math.abs(dy))<cfg.dead?'CENTER':Math.abs(dx)>Math.abs(dy)?dx>0?'RIGHT':'LEFT':dy>0?'DOWN':'UP';controllerDirection(dir);
   if(prior?.eOK&&p.ep!==prior.ep&&((p.ep-prior.ep)&65535)<20)controllerPress('explorer');
   if(cfg.lightFitted){
    const reveal=cfg.darkLow?p.light<cfg.dark:p.light>cfg.dark;
    controllerLine('explorer',`Light Level: ${p.light} -> ${reveal?'REVEAL ACTIVATED':'Normal'}`);
   }
  }else{stopMovement();controllerState.lightActive=false;}
  if(p.aOK){if(cfg.potFitted)controllerPot(p.pot);if(prior?.aOK&&p.ap!==prior.ap&&((p.ap-prior.ap)&65535)<20)controllerPress('architect');}
  prior=p;history.push({time:new Date().toISOString(),...p,feedback:feedback(),player:{...(forest.active?forest:campaign.active?campaign:state).player}});if(history.length>1200)history.shift();
  note(`${active||'Input'} | Explorer ${p.eOK?'OK':'OFFLINE'} | Architect ${p.aOK?'OK':'OFFLINE'}\nX ${p.x} Y ${p.y} light ${p.light} pot ${p.pot}\nPresses E ${p.ep} A ${p.ap} | LED ${p.led||'--'}\nReveal ${cfg.lightFitted&&(cfg.darkLow?p.light<cfg.dark:p.light>cfg.dark)?'ON':'OFF'} | Explorer position ${Math.round(history.at(-1).player.x)}, ${Math.round(history.at(-1).player.y)}`);
  return true;
 }
 async function stop(){active='';session++;prior=null;last=0;failures=0;stopMovement();controllerState.lightActive=false;setControllerMode(false);if(reader)await reader.cancel().catch(()=>{});note('Disconnected; movement released.');el('hubNetwork').textContent='Automatic reconnection stopped.';event('Disconnected by player.');}
 async function joinWiFi(token){
  if(joining||token!==session||active!=='Wi-Fi')return;
  joining=true;reconnectAt=performance.now()+15000;
  try{
   el('hubNetwork').textContent='Asking Windows to join DualRealityMaze…';
   const r=await fetch('/hub/connect',{method:'POST',signal:AbortSignal.timeout(12000)}),p=await r.json();
   if(token!==session||active!=='Wi-Fi')return;
   if(!r.ok)throw Error(p.error||'Wi-Fi join failed.');
   el('hubNetwork').textContent=p.message;event(p.message);
  }catch(e){if(token===session){el('hubNetwork').textContent=e.message+' You can also join DualRealityMaze in Windows Wi-Fi settings.';event(e.message);}}
  finally{joining=false;}
 }
 el('hubUSB').onclick=async()=>{
  if(active)return;
  if(!navigator.serial){note('USB requires Chrome or Edge. Wi-Fi works through this launcher.');return;}
  await disconnectControllers();const token=++session;
  try{
   port=await navigator.serial.requestPort();if(token!==session)return;
   await port.open({baudRate:115200});if(token!==session){await port.close();return;}
   active='USB';prior=null;setControllerMode(true);stopMovement();reader=port.readable.getReader();writer=port.writable.getWriter();let partial='';const dec=new TextDecoder();
   while(active==='USB'&&token===session){const r=await reader.read();if(r.done)break;if(token!==session)break;partial+=dec.decode(r.value,{stream:true});const lines=partial.split('\n');partial=lines.pop();if(partial.length>1024)partial='';for(const line of lines){try{accept(JSON.parse(line));}catch{}}}
  }catch(e){note('USB: '+e.message);}
  finally{if(token===session){active='';stopMovement();}try{reader?.releaseLock();writer?.releaseLock();await port?.close();}catch{}reader=writer=port=null;}
 };
 el('hubWiFi').onclick=async()=>{
  if(active)return;await disconnectControllers();active='Wi-Fi';const token=++session;prior=null;last=0;failures=0;setControllerMode(true);stopMovement();note('Connecting to Main…');event('Wi-Fi selected.');await joinWiFi(token);
 };
 el('hubStop').onclick=stop;el('hubFold').onclick=()=>ui.open=false;
 el('hubCentre').onclick=()=>{if(latest?.eOK){cfg.cx=latest.x;cfg.cy=latest.y;stopMovement();}};
 el('hubIX').onchange=e=>cfg.invertX=e.target.checked;el('hubIY').onchange=e=>cfg.invertY=e.target.checked;el('hubLow').onchange=e=>cfg.darkLow=e.target.checked;
 el('hubLightFitted').onchange=e=>{cfg.lightFitted=e.target.checked;controllerState.lightActive=false;};
 el('hubPotFitted').onchange=e=>{cfg.potFitted=e.target.checked;controllerState.pot=null;};
 el('hubDark').onchange=e=>cfg.dark=Math.max(0,Math.min(1023,Number(e.target.value)||0));
 el('hubLog').onclick=()=>{const a=document.createElement('a');const u=URL.createObjectURL(new Blob([JSON.stringify({cfg,events,history},null,2)],{type:'application/json'}));a.href=u;a.download='maze-hardware-log.json';a.click();setTimeout(()=>URL.revokeObjectURL(u),1000);};
 setInterval(async()=>{
  if(!active)return;
  if(last&&performance.now()-last>800){stopMovement();prior=null;note('No fresh input — movement stopped. Reconnecting; centre the joystick.');}
  if(busy)return;busy=true;const token=session;
  try{
   if(active==='USB'&&writer)await writer.write(new TextEncoder().encode(feedback()+'\n'));
   else if(active==='Wi-Fi'){
    const r=await fetch('/hub/input',{signal:AbortSignal.timeout(1800),cache:'no-store'});
    const p=await r.json();if(token!==session||active!=='Wi-Fi')return;
    if(!r.ok)throw Error(p.error||'Main is not reachable.');
    if(!accept(p))throw Error('Unexpected Main board data.');
    if(!document.hidden&&story.ready&&splash.artReady){
     const ack=await fetch('/hub/state',{method:'POST',body:feedback(),signal:AbortSignal.timeout(1800)});
     const reply=await ack.json();if(token!==session)return;
     if(!ack.ok||!reply.ok)throw Error('Game feedback was not acknowledged.');
    }
    if(failures)event('Main connection recovered.');failures=0;
   }
  }catch(e){
   if(token===session){stopMovement();prior=null;failures++;note(e.message+'\nMovement stopped. Keep Main powered and centre the joystick.');if(failures===1)event(e.message);
    if(active==='Wi-Fi'&&failures>=2&&el('hubRecover').checked&&!document.hidden&&performance.now()>=reconnectAt)void joinWiFi(token);
   }
  }finally{busy=false;}
 },100);
 window.mazeHardware={accept,feedback,config:cfg,disconnect:stop,log:()=>history.slice()};
})();
