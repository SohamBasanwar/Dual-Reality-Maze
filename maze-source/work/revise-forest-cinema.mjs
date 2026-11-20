import fs from 'node:fs';
const p='maze-source/work/chapters/forest-render.js';let s=fs.readFileSync(p,'utf8'),a=s.indexOf('function forestCinematic('),b=s.indexOf('function drawForest()',a);
s=s.slice(0,a)+`function forestCinematic(g,t){const shot=forestSequences[forest.sequence][forest.shot],key=shot.key,q=smooth(forest.shotTime/shot.duration),p=forestPoint(forest.player),origin=forestPoint(FOREST.dryad),rescue=['capture','summon','arrival'].includes(forest.sequence),d=rescue?{x:p.x+84,y:p.y+4}:origin,close=rescue?{x:p.x+40,y:p.y-35,z:2.1}:{x:origin.x-22,y:origin.y-25,z:2.2},wide={x:652,y:470,z:1};let camera=close;
 if(key==='wide')camera=wide;else if(key==='heroes')camera={x:wide.x+(close.x-wide.x)*q,y:wide.y+(close.y-wide.y)*q,z:1+(close.z-1)*q};else if(key==='reveal'||key==='pathGrow')camera={x:close.x+(652-close.x)*q,y:close.y+(470-close.y)*q,z:close.z+(1-close.z)*q};if(reduced)camera=wide;
 if(key==='homeflight'){g.drawImage(images.kingdom,-q*30,-q*12,1672+q*40,941+q*30);forestDragon(g,260+q*820,480-Math.sin(q*Math.PI)*90,430-q*90,t,true);return;}
 g.fillStyle='#071e22';g.fillRect(0,0,1672,941);g.save();const sx=key==='wide'||reduced?652:['reveal','pathGrow'].includes(key)?836+(652-836)*q:836;g.translate(sx,470);g.scale(camera.z,camera.z);g.translate(-camera.x,-camera.y);forestWorld(g,t,false);
 const jarKeys=['jarOpen','jarEnter','jarClose','emerge','congratulate','summon','incoming'];if(jarKeys.includes(key))forestJarHero(g,p,!['jarOpen','jarEnter'].includes(key));else forestHero(g,p);
 const ax=p.x+45,ay=p.y+3;let alpha=key==='reform'?q:key==='merge'?1-smooth(Math.min(1,q*1.5)):key==='reveal'?0:1;forestArchitect(g,ax,ay,FOREST.architectSize,alpha,forest.robes||['seal','merge','reveal'].includes(key));
 if(key==='attempt'||key==='rejected'){const strength=key==='attempt'?q:1-q;forestGlow(g,ax+18,ay-55,65,'#cf9bff',strength*.5);g.strokeStyle=key==='attempt'?'#c293ef':'#e8efad';g.lineWidth=2;g.beginPath();g.ellipse(d.x,d.y-12,25+strength*55,15+strength*30,0,0,7);g.stroke();for(let i=0;i<16;i++)forestLeaf(g,ax+Math.cos(i*2.4)*strength*55,ay-35-Math.sin(i*2.4)*strength*35,4,strength);}
 if(key==='dryad')forestDryad(g,d.x,d.y+5,'talk',q);
 if(key==='pathRaise'){forestDryad(g,d.x,d.y+5,q<.45?'raise':'cast');forestGlow(g,d.x+25,d.y-75,65,'#ffe084',q*.6);}
 if(key==='pathGrow'){forestRootPath(g,q);for(let i=0;i<20;i++)forestLeaf(g,origin.x*(1-q)+Math.sin(i*2.4)*20,forestPoint({x:0,y:18}).y-20-i*3,4,(1-q)*.8);}
 if(key==='gift'){forestProp(g,6,p.x+15,p.y-36-q*12,42);forestGlow(g,p.x+15,p.y-50,50,'#f3ee9f',.35);}
 if(key==='robes'||key==='seal'){const cx=key==='robes'?p.x:ax;forestGlow(g,cx,p.y-35,75,'#f4d67f',Math.sin(q*Math.PI)*.5);for(let i=0;i<22;i++)forestLeaf(g,cx+Math.cos(i*2.4+q*4)*32,p.y-q*95+i%4*10,4,Math.sin(q*Math.PI));}
 if(key==='merge'||key==='reform'){const v=key==='merge'?q:1-q;forestGlow(g,ax,ay-40,45+v*75,'#f2db7f',.45*(1-v));for(let i=0;i<36;i++){const angle=i*2.4,r=10+v*(30+i*2);forestLeaf(g,ax+Math.cos(angle)*r,ay-35+Math.sin(angle)*r*.55-v*25,4,1-v);}if(key==='merge'){g.strokeStyle='#e9d78c';g.globalAlpha=.5*(1-q);g.beginPath();g.ellipse(ax,ay,25+q*1200,15+q*650,0,0,7);g.stroke();g.globalAlpha=1;}}
 if(key==='reveal')forestSpirit(g,t,q);
 if(['reform','play','jarOpen'].includes(key)){const angle=key==='play'?q*Math.PI*2.7:0,x=key==='play'?p.x+24+Math.cos(angle)*64:p.x-24,y=key==='play'?p.y-42+Math.sin(angle)*18:p.y-38;forestEcho(g,x,y,Math.floor(t/500)%2,FOREST.memorySize);}
 if(key==='jarEnter'){const x=p.x-24+(44*q),y=p.y-38-8*q;forestEcho(g,x,y,1,FOREST.memorySize*(1-q)+2,1-q);forestGlow(g,p.x+20,p.y-36,50,'#ffe89c',q*.5);}
 if(key==='jarClose')forestGlow(g,p.x+20,p.y-35,55,'#ffe89c',.5*(1-q));
 if(key==='emerge'){g.save();g.beginPath();g.rect(d.x-80,d.y-FOREST.dryadSize*q,160,FOREST.dryadSize*q+10);g.clip();forestDryad(g,d.x,d.y+FOREST.dryadSize*(1-q),'emerge',Math.min(1,q*2));g.restore();for(let i=0;i<22;i++)forestLeaf(g,d.x+Math.cos(i*2.4)*q*50,d.y-i*2*q,4,1-q);}
 if(['congratulate','summon','incoming'].includes(key))forestDryad(g,d.x,d.y,key==='congratulate'?'talk':key==='summon'?'cast':'idle');
 if(key==='summon'){const x=d.x+18+(-140-d.x)*q,y=d.y-75-q*360;for(let i=1;i<14;i++){const k=Math.max(0,q-i*.018);forestLeaf(g,d.x+18+(-140-d.x)*k,d.y-75-k*360,7,(1-i/14)*.5);}forestGlow(g,x,y,65,'#ffe596',.6);forestLeaf(g,x,y,23);g.strokeStyle='#fff8c6';g.lineWidth=2;g.beginPath();g.arc(x,y,32,t/350,t/350+4);g.stroke();}
 if(key==='incoming')forestDragon(g,p.x-250+q*220,p.y-170+q*90,125+q*130,t);
 g.restore();if(['reveal','pathGrow'].includes(key)&&q>.7){g.save();g.globalAlpha=smooth((q-.7)/.3);g.drawImage(forest.panelArt,1304,0);g.restore();}}
`+s.slice(b);
s=s.replace("['offering','hunt','paused','cinema']", "['path','offering','offeringReturn','hunt','paused','cinema']");fs.writeFileSync(p,s);
const root='C:/Users/soham/.codex/generated_images/01a1334a-bc04-7801-aacf-702fbd94575d/';for(const dir of ['images/','maze-source/work/assets/'])fs.copyFileSync(root+'exec-1e0f9252-28d6-466c-8626-16023cbf1196.png',dir+'forest-rowan-v2.png');
let f='maze-source/work/chapters/forest.js',v=fs.readFileSync(f,'utf8').replace("'forestHeroes','forestRevisionComic'", "'forestHeroes','forestRowan','forestRevisionComic'");fs.writeFileSync(f,v);
