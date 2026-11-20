const labCanvas=$('labCanvas'),labCtx=labCanvas.getContext('2d');
const LAB_MAGIC=Object.freeze({glow:'#75d3a0',light:'#c2f3cd',ring:'#98dbac',shadow:'#277f60'});
// Chapter-local palette shaders preserve the original Chapter I artwork.
function labMagicSprite(source,spirit=false){
 const c=document.createElement('canvas');c.width=source.width;c.height=source.height;const g=c.getContext('2d');g.drawImage(source,0,0);
 const pixels=g.getImageData(0,0,c.width,c.height),d=pixels.data;
 for(let y=0;y<c.height;y++)for(let x=0;x<c.width;x++){
  const i=(y*c.width+x)*4;if(!d[i+3])continue;const r=d[i],green=d[i+1],b=d[i+2];
  // Only the violet spell above the raised hand; skin, clothes and other cast members stay intact.
  if(!spirit&&!(x>c.width*.342&&x<c.width*.49&&y>c.height*.10&&y<c.height*.235&&b>r*.9&&b>green*1.04))continue;
  const light=(Math.max(r,green,b)+Math.min(r,green,b))/2/255;
  const stops=spirit?[[7,30,24],[39,127,96],[174,231,185]]:[[15,77,45],[100,207,132],[226,255,226]];
  const k=light<.58?0:1,q=light<.58?light/.58:(light-.58)/.42;
  for(let j=0;j<3;j++)d[i+j]=Math.round(stops[k][j]+(stops[k+1][j]-stops[k][j])*q);
 }
 g.putImageData(pixels,0,0);return c;
}
function labCreatePanel(){
 const c=document.createElement('canvas');c.width=368;c.height=941;const g=c.getContext('2d');
 const bg=g.createLinearGradient(0,0,368,941);bg.addColorStop(0,'#244f58');bg.addColorStop(.3,'#102f31');bg.addColorStop(1,'#071e29');g.fillStyle=bg;g.fillRect(0,0,368,941);
 const box=(x,y,w,h)=>{g.fillStyle='#071f26dd';g.fillRect(x,y,w,h);g.strokeStyle='#709e85';g.lineWidth=1;g.strokeRect(x+.5,y+.5,w-1,h-1);};
 g.strokeStyle='#c9c598';g.lineWidth=2;g.strokeRect(8,6,352,929);g.strokeStyle='#4b8876';g.strokeRect(14,12,340,917);
 for(const x of [9,359])for(const y of [9,932]){g.fillStyle='#c6dcac';g.save();g.translate(x,y);g.rotate(Math.PI/4);g.fillRect(-3,-3,6,6);g.restore();}
 g.textAlign='center';g.fillStyle='#e2edc6';g.font='small-caps 35px Georgia';g.fillText('Dual-Reality',184,49);g.font='small-caps 38px Georgia';g.fillText('Maze',184,86);
 const f=campaign.roarFrames[0],w=99,h=w*f.h/f.w;g.drawImage(images.dragonRoar,f.x,f.y,f.w,f.h,184-w/2,153-h,w,h);
 for(const side of [-1,1]){g.save();g.translate(184,125);g.scale(side,1);for(let i=0;i<3;i++){g.strokeStyle=['#a9d8c1','#6ca493','#446f70'][i];g.beginPath();g.moveTo(58,8+i*6);g.bezierCurveTo(86,8+i*6,95,-10+i*5,145,-5+i*6);g.stroke();}g.restore();}
 box(25,160,320,114);g.fillStyle='#d8e9b8';g.font='small-caps 28px Georgia';g.fillText('The Architect',184,200);g.fillStyle='#b5d9cf';g.font='19px Georgia';g.fillText('Warden of wind and stone',184,232);g.font='14px Georgia';g.fillText('THE EMERALD GUARDIAN',184,257);
 for(const [i,e] of laboratory.controls.entries()){const y=294+i*63.5;box(28,y-5,312,53);g.strokeStyle=e.color;g.lineWidth=2;g.strokeRect(36,y,43,43);g.strokeRect(40,y+4,35,35);g.fillStyle=e.color;
  if(e.type==='bridge'){for(let n=0;n<4;n++)g.fillRect(44+n*7,y+10,4,25);g.fillRect(42,y+9,31,2);g.fillRect(42,y+34,31,2);}else{for(let n=0;n<3;n++)g.fillRect(46+n*10,y+7,3,30);g.fillRect(43,y+7,30,3);}
  g.fillStyle='#e8eddb';g.font='21px Georgia';g.textAlign='left';g.fillText(e.name,100,y+29);
 }
 box(25,626,320,129);g.fillStyle='#cce4ca';g.font='23px Georgia';g.fillText('Time',101,672);g.fillText('Items',101,727);
 g.strokeStyle='#c8dca7';g.lineWidth=3;g.beginPath();g.arc(64,663,14,0,Math.PI*2);g.moveTo(64,652);g.lineTo(64,663);g.lineTo(71,669);g.stroke();g.fillStyle='#c8dca7';g.fillRect(58,641,12,4);
 g.strokeStyle='#8cd8bb';g.beginPath();g.moveTo(59,705);g.lineTo(69,705);g.lineTo(69,712);g.lineTo(78,731);g.lineTo(50,731);g.lineTo(59,712);g.closePath();g.stroke();g.fillStyle='#65bea0';g.fillRect(57,721,14,6);
 g.strokeStyle='#477d70';g.lineWidth=1;g.beginPath();g.moveTo(36,690);g.lineTo(334,690);g.stroke();
 box(25,770,320,143);g.save();g.beginPath();g.rect(27,772,316,139);g.clip();const sky=g.createLinearGradient(0,772,0,911);sky.addColorStop(0,'#173f4b');sky.addColorStop(1,'#397b75');g.fillStyle=sky;g.fillRect(27,772,316,139);
 for(let i=0;i<7;i++){g.fillStyle=i%2?'#8bb5a520':'#b8d4bf18';g.beginPath();g.ellipse(40+i*52,805+i%3*33,85,14,0,0,Math.PI*2);g.fill();}g.restore();
 g.textAlign='center';g.fillStyle='#9ccfb3';g.font='10px Georgia';g.fillText('THE HANGING GARDENS · SKY SANCTUARY',184,925);return c;
}
function labSprite(g,index,x,base,height,alpha=1){const f=campaign.frames[index];if(!f)return;const width=height*f.w/f.h;g.save();g.globalAlpha=alpha;g.drawImage(images.labAtlas,f.x,f.y,f.w,f.h,x-width/2,base-height,width,height);g.restore();}
function labAtlas(g,index,x,base,w,h=w){const f=art.sprites[index];if(f)g.drawImage(images.atlas,f.x,f.y,f.w,f.h,x-w/2,base-h,w,h);}
function labPoly(g,points,color){g.fillStyle=color;g.beginPath();points.forEach(([x,y],i)=>i?g.lineTo(x,y):g.moveTo(x,y));g.closePath();g.fill();}
function labTrimSheet(img,cols,rows){const c=document.createElement('canvas');c.width=img.width;c.height=img.height;const g=c.getContext('2d');g.drawImage(img,0,0);const data=g.getImageData(0,0,c.width,c.height).data,cw=Math.floor(c.width/cols),ch=Math.floor(c.height/rows),frames=[];for(let i=0;i<cols*rows;i++){let l=cw,t=ch,r=-1,b=-1;const ox=i%cols*cw,oy=Math.floor(i/cols)*ch;for(let y=0;y<ch;y++)for(let x=0;x<cw;x++)if(data[((oy+y)*c.width+ox+x)*4+3]>80){l=Math.min(l,x);t=Math.min(t,y);r=Math.max(r,x);b=Math.max(b,y);}frames.push({x:ox+l,y:oy+t,w:r-l+1,h:b-t+1});}return frames;}
function initLaboratoryArt(){
 const roar=labTrimSheet(images.dragonRoar,3,1),cw=Math.floor(images.dragonRoar.width/3),left=Math.min(...roar.map((f,i)=>f.x-i*cw)),right=Math.max(...roar.map((f,i)=>f.x-i*cw+f.w)),top=Math.min(...roar.map(f=>f.y)),bottom=Math.max(...roar.map(f=>f.y+f.h));
 campaign.roarFrames=roar.map((f,i)=>({x:i*cw+left,y:top,w:right-left,h:bottom-top}));
 campaign.frames=labTrimSheet(images.labAtlas,4,2);campaign.dragonFrames=labTrimSheet(images.dragon,3,2);campaign.flightBounds=labTrimSheet(images.dragonFlight,1,1)[0];
 // Sheet gutters contain a few pixels from neighbouring poses; keep source rectangles inside each subject.
 campaign.frames[2].w=Math.min(campaign.frames[2].w,Math.floor(images.labAtlas.width*.704)-campaign.frames[2].x);
 
 const c=document.createElement('canvas');c.width=1672;c.height=941;const g=c.getContext('2d');g.imageSmoothingEnabled=false;const size=LAB.tile;
 // Bake only the individual island surfaces. Open sky remains transparent between the terraces.
 const occupied=(x,y)=>laboratory.grid[y]?.[x]||laboratory.wallKeys.has(x+','+y);
 for(const w of laboratory.walls){if(occupied(w.x,w.y+1))continue;const x=LAB.ox+w.x*size,y=LAB.oy+(w.y+1)*size,depth=38+rand(w.x,w.y)*64; if(w.x%2===0){const rock=art.sprites[12];g.save();g.filter='hue-rotate(210deg) saturate(.5)';g.drawImage(images.atlas,rock.x,rock.y+rock.h*.4,rock.w,rock.h*.6,x-16,y-5,65,depth+18);g.restore();}
  labPoly(g,[[x,y-9],[x+size,y-9],[x+size-3,y+depth*.55],[x+18,y+depth],[x+6,y+depth*.65]],'#133b43');
  labPoly(g,[[x+3,y],[x+12,y],[x+16,y+depth-5],[x+7,y+depth*.6]],'#2b6664');
  labPoly(g,[[x+20,y],[x+31,y],[x+25,y+depth*.7],[x+19,y+depth*.85]],'#092633');
  for(let j=0;j<6;j++){g.fillStyle=['#36766b','#19494e','#497f6d'][j%3];g.fillRect(x+4+hash(w.x,w.y,j)%19,y+j*9,3+hash(j,w.x)%7,3);}
 }
 for(let y=0;y<LAB.rows;y++)for(let x=0;x<LAB.cols;x++)if(laboratory.grid[y][x]){if(laboratory.controls.some(c=>c.type==='bridge'&&labOnControl({x,y},c)))continue;const px=LAB.ox+x*size,py=LAB.oy+y*size,f=art.sprites[0];if(f){g.save();g.filter='hue-rotate(-38deg) saturate(.6) brightness(.9)';g.drawImage(images.atlas,f.x+(x%2)*f.w/2,f.y+(y%2)*f.h/2,f.w/2,f.h/2,px,py,size,size);g.restore();}else{g.fillStyle='#23504f';g.fillRect(px,py,size,size);}g.fillStyle='#4e99852a';g.fillRect(px,py,size,size);g.strokeStyle='#0b353c';g.lineWidth=1;g.strokeRect(px+.5,py+.5,size-1,size-1);g.fillStyle='#8fbca04d';g.fillRect(px+2,py+2,size-4,1);if(hash(x,y)%4===0){g.strokeStyle='#0b2932';g.beginPath();g.moveTo(px+6,py+5);g.lineTo(px+11,py+13);g.lineTo(px+9,py+20);g.stroke();}}
 for(const s of laboratory.stairs){const p=labPoint(s);for(let n=0;n<8;n++){const yy=p.y-15+n*4;g.fillStyle=n%2?'#82ac9c':'#366b67';g.fillRect(p.x-14,yy,28,3);g.fillStyle='#d4d6af';g.fillRect(p.x-13,yy,26,1);}g.fillStyle='#c59f59';g.fillRect(p.x-16,p.y-15,2,31);g.fillRect(p.x+14,p.y-15,2,31);}
 for(const w of laboratory.walls){const x=LAB.ox+w.x*size,y=LAB.oy+w.y*size,f=art.sprites[1],v=hash(w.x,w.y)%3;
  g.save();g.filter='hue-rotate(215deg) saturate(.45) brightness(1.12)';
  if(!laboratory.wallKeys.has(w.x+','+(w.y+1)))g.drawImage(images.atlas,f.x+f.w*(.04+v*.30),f.y+f.h*.56,f.w*.27,f.h*.35,x,y+1,size,30);
  g.drawImage(images.atlas,f.x+f.w*(.04+v*.30),f.y+f.h*.045,f.w*.255,f.h*.42,x,y-12,size,25);g.restore();
  g.fillStyle='#bbcfaa';g.fillRect(x+1,y-12,size-2,1);g.fillStyle='#193e39';g.fillRect(x+1,y+11,size-2,2);
  if(hash(w.x,w.y)%3===0){g.fillStyle='#568b59';g.fillRect(x+3,y-9,4,2);g.fillRect(x+6,y-7,6,2);g.fillStyle='#96b37a';g.fillRect(x+4,y-10,3,1);}
  if(laboratory.grid[w.y+1]?.[w.x]){const shadow=g.createLinearGradient(x,y+size,x,y+size+10);shadow.addColorStop(0,'#001a2788');shadow.addColorStop(1,'transparent');g.fillStyle=shadow;g.fillRect(x,y+size,size,10);}
 }
 // Brass machines, broken columns and tiny garden beds frame the navigable route.
 for(const p of [{x:7,y:3},{x:17,y:8},{x:24,y:10},{x:25,y:18},{x:30,y:2}]){const q=labPoint(p);labSprite(g,2,q.x,q.y+14,65);}
 for(const p of [{x:4,y:17},{x:7,y:12},{x:18,y:15},{x:27,y:19}]){const q=labPoint(p);labAtlas(g,6,q.x,q.y+12,22,28);}
 campaign.tiles=c;
 campaign.panelArt=labCreatePanel();campaign.greenCast=labMagicSprite(images.cast);campaign.greenSpirit=labMagicSprite(images.spirit,true);
 const gray=document.createElement('canvas');gray.width=c.width;gray.height=c.height;const gg=gray.getContext('2d');gg.filter='saturate(0)';gg.drawImage(c,0,0);campaign.grayTiles=gray;
}
function labGlow(x,y,r,color,opacity){const g=labCtx;g.save();g.globalAlpha=opacity;const gradient=g.createRadialGradient(x,y,1,x,y,r);gradient.addColorStop(0,color);gradient.addColorStop(1,'transparent');g.fillStyle=gradient;g.fillRect(x-r,y-r,r*2,r*2);g.restore();}
function labCloud(x,y,w,alpha){const g=labCtx;g.save();g.translate(x,y);g.scale(1,.3);g.globalAlpha=alpha;const grad=g.createRadialGradient(0,0,0,0,0,w);grad.addColorStop(0,'#d8ede0');grad.addColorStop(.45,'#9acdd055');grad.addColorStop(1,'transparent');g.fillStyle=grad;g.fillRect(-w,-w,w*2,w*2);g.restore();}
function labSky(t,flight=false){const g=labCtx,bg=g.createLinearGradient(0,0,0,941);bg.addColorStop(0,flight?'#306a86':'#062839');bg.addColorStop(.55,flight?'#6fa7b3':'#174857');bg.addColorStop(1,flight?'#d9dab1':'#629795');g.fillStyle=bg;g.fillRect(0,0,1672,941);
 for(let i=0;i<12;i++){const x=(i*173+70-(reduced?0:t/(flight?55:250))%1850+1850)%1850-90,y=160+(i*139)%690;labCloud(x,y,130+i%3*75,.22);}
 for(let i=0;i<9;i++){const x=90+i*145,y=120+(i*177)%660;g.save();g.globalAlpha=.28;g.filter='hue-rotate(210deg) saturate(.35)';labAtlas(g,12,x,y+80,60+i%3*13,110);g.restore();}
}
function labSpark(x,y,t,color){const a=Math.max(0,Math.sin(t/430+x+y));if(a<.6)return;const g=labCtx;g.save();g.globalAlpha=a;g.fillStyle=color;g.fillRect(x-1,y-5,2,10);g.fillRect(x-5,y-1,10,2);g.restore();}
function labTorch(x,y,t,phase){const g=labCtx;labAtlas(g,4,x,y,16,28);labGlow(x,y-32,52,'#ffa74a',.19+.04*Math.sin(t/67+phase));for(let j=0;j<9;j++){const width=(9-j)*.75,xx=x+Math.sin(t/100+phase+j/3)*j*.3;g.fillStyle=j>5?'#f58a20':'#ffd16a';g.fillRect(xx-width/2,y-25-j*2,width,3);if(j<4){g.fillStyle='#fff4be';g.fillRect(xx-1,y-25-j*2,3,2);}}}
function labPlants(t){const g=labCtx;for(const w of laboratory.walls){const p=labPoint(w);if(hash(w.x,w.y)%5===0){const f=art.sprites[3];if(f){const h=42+rand(w.x,w.y)*29;for(let sy=0;sy<h;sy+=4){const k=sy/h,shift=Math.sin(t/1000+w.x+k*2)*k*3;g.drawImage(images.atlas,f.x,f.y+k*f.h,f.w,Math.min(4/h*f.h,f.h-k*f.h),p.x-9+shift,p.y+10+sy,18,Math.min(4,h-sy));}}}if(hash(w.x,w.y)%11===0&&laboratory.grid[w.y+1]?.[w.x])labTorch(p.x,p.y+36,t,w.x+w.y);}
 for(let y=0;y<LAB.rows;y++)for(let x=0;x<LAB.cols;x++)if(laboratory.grid[y][x]&&hash(x,y)%7===0){const p=labPoint({x,y});g.strokeStyle='#64aa76';g.lineWidth=2;for(let j=0;j<4;j++){g.beginPath();g.moveTo(p.x-12+j*2,p.y+10);g.quadraticCurveTo(p.x-14+j*3,p.y+4,p.x-16+j*3+Math.sin(t/650+x+j)*2,p.y-2-j%2*5);g.stroke();}}
}
function labWaterfalls(t){const g=labCtx;for(const s of laboratory.waterfalls){const p=labPoint(s),h=55+rand(s.x,s.y)*40;const grad=g.createLinearGradient(p.x,p.y, p.x,p.y+h);grad.addColorStop(0,'#87f5e2a0');grad.addColorStop(.7,'#54bdda70');grad.addColorStop(1,'transparent');g.fillStyle=grad;g.fillRect(p.x-8,p.y+17,16,h);for(let n=0;n<5;n++){g.fillStyle=n%2?'#d2fff2aa':'#81d7e9aa';g.fillRect(p.x-6+n*3,p.y+18+(t/35+n*19)%h,2,12);}labCloud(p.x,p.y+h,32,.25);}}
function labHero(x,y,h=CHAPTER_VIEW.heroHeight,alpha=1,facing=1){if(!heroBounds)return;const g=labCtx,b=heroBounds,w=h*b.w/b.h;g.save();g.globalAlpha=alpha;g.translate(x,y);g.scale(facing,1);g.drawImage(images.hero,b.x,b.y,b.w,b.h,-w/2,-h,w,h);g.restore();}
function labArchitect(x,y,h=50,alpha=1){const f=story.cast[0];if(!f)return;const g=labCtx;g.save();g.globalAlpha=alpha;g.drawImage(campaign.greenCast||images.cast,f.x,f.y,f.w,f.h,x-h*f.w/f.h/2,y-h,h*f.w/f.h,h);g.restore();}
function labDragon(x,y,width,t,riding=false,flight=false){const g=labCtx;
 if(riding){const f=campaign.flightBounds;if(!f)return;const scale=width/f.w,phase=reduced?0:Math.sin(t/320);
  // One complete silhouette: upper-wing strips flex continuously, while the body and riders keep a fixed anchor.
  // No switching between incompatible poses or sampling across sprite-sheet gutters.
  g.save();g.translate(x,y+(reduced?0:Math.sin(t/580)*3));g.rotate(reduced?0:Math.sin(t/900)*.012);
  for(let sy=0;sy<f.h;sy+=3){const h=Math.min(3,f.h-sy),weight=Math.pow(Math.max(0,1-sy/(f.h*.48)),2),shift=phase*width*.035*weight;g.drawImage(images.dragonFlight,f.x,f.y+sy,f.w,h,-width/2+shift,-f.h*scale*.64+sy*scale,width,h*scale+.5);}g.restore();return;
 }
 const roaring=campaign.mode==='intro'&&labIntroShot().key==='roar',elapsed=campaign.intro?.elapsed||0,index=roaring?(elapsed<.18?0:elapsed<.42?1:elapsed<1.85?2:elapsed<2.2?1:0):0,f=campaign.roarFrames?.[index];if(!f)return;const h=width*f.h/f.w;g.drawImage(images.dragonRoar,f.x,f.y,f.w,f.h,x-width/2,y+width*.25-h,width,h);
}
function labShrines(t){const g=labCtx;laboratory.stations.forEach((s,i)=>{const p=labPoint(s),collected=campaign.ingredients[i];labGlow(p.x,p.y-16,58,s.color,collected?.06:.22);labSprite(g,s.sprite,p.x,p.y+6+(reduced?0:Math.sin(t/520+i)*2),48,collected?.22:1);if(!collected)labSpark(p.x+10,p.y-28,t+i*380,s.color);g.font='bold 10px Georgia';g.textAlign='center';g.fillStyle=collected?'#b5f5c8':s.color;g.fillText(collected?'COLLECTED':s.name.toUpperCase(),p.x,p.y+29);});}
function labPassages(t){const g=labCtx;laboratory.controls.forEach((c,i)=>{const p=labPoint(c),a=campaign.progress[i],width=(c.w||1)*LAB.tile;p.x+=(width-LAB.tile)/2;
 if(c.type==='bridge'){for(const yy of [p.y-13,p.y+13]){g.strokeStyle='#b68d4d';g.lineWidth=2;g.beginPath();g.moveTo(p.x-width/2,yy);g.lineTo(p.x+width/2,yy);g.stroke();}for(const side of [-1,1]){g.save();g.translate(p.x+side*width/2,p.y);g.scale(-side,1);const len=width/2*a;g.fillStyle='#805532';g.fillRect(0,-12,len,24);for(let n=0;n<len;n+=6){g.fillStyle=c.color;g.fillRect(n,-11,Math.min(5,len-n),22);g.fillStyle='#f7daa0';g.fillRect(n,-11,Math.min(5,len-n),2);}g.restore();}}
 else{for(const xx of [p.x-16,p.x+12]){g.fillStyle='#465f4e';g.fillRect(xx,p.y-32,5,45);g.fillStyle=c.color;g.fillRect(xx+1,p.y-30,2,40);}g.save();g.beginPath();g.rect(p.x-12,p.y-29,24,42);g.clip();for(let n=0;n<4;n++){g.fillStyle=c.color;g.fillRect(p.x-11+n*7,p.y-29-a*44,3,42);}g.fillRect(p.x-12,p.y+3-a*44,25,3);g.restore();g.fillStyle='#b5bd86';g.fillRect(p.x-17,p.y-35,35,5);}labGlow(p.x,p.y-10,35,c.color,.18);
 });}
function labSpirit(t){if(!architectSpirit.frames.length)return;const g=labCtx,target=labControlPoint(laboratory.controls[campaign.selected]),ghost=campaign.ghost,casting=campaign.cast>0,f=architectSpirit.frames[casting?1:0],h=CHAPTER_VIEW.spiritHeight,w=h*f.w/f.h,x=ghost.x-20,y=ghost.y-17+(reduced?0:Math.sin(t/300)*2);labGlow(x,y-20,33,LAB_MAGIC.glow,.25);g.save();g.globalAlpha=.87;g.drawImage(campaign.greenSpirit||images.spirit,f.x,f.y,f.w,f.h,x-w/2,y-h,w,h);g.strokeStyle=LAB_MAGIC.ring;g.lineWidth=2;g.setLineDash([4,4]);g.lineDashOffset=-t/70;const width=(laboratory.controls[campaign.selected].w||1)*LAB.tile+14;g.strokeRect(target.x-width/2,target.y-30,width,48);g.restore();if(casting){g.strokeStyle=LAB_MAGIC.light;g.beginPath();g.moveTo(x,y-20);g.quadraticCurveTo(x+18,y-45,target.x,target.y-10);g.stroke();labGlow(target.x,target.y,40,LAB_MAGIC.glow,campaign.cast);}}
function labRuins(t,actors=true,background=true){const g=labCtx;if(background)labSky(t);if(campaign.mode==='intro'&&campaign.grayTiles){g.drawImage(campaign.grayTiles,0,0);const color=labIntroColor();if(color>0){g.save();const p=labPoint(LAB.start);g.beginPath();g.arc(p.x+28,p.y,Math.max(1,color*1600),0,Math.PI*2);g.clip();g.globalAlpha=Math.min(1,color*3);g.drawImage(campaign.tiles,0,0);g.restore();}}else g.drawImage(campaign.tiles,0,0);if(campaign.mode==='ascent'&&campaign.grayTiles){g.save();g.globalAlpha=smooth((campaign.phaseTime-.6)/2.2);g.drawImage(campaign.grayTiles,0,0);g.restore();}labWaterfalls(t);labPlants(t);labShrines(t);labPassages(t);
 const roost=labPoint(LAB.roost);g.strokeStyle='#d4bd79';g.lineWidth=2;g.beginPath();g.ellipse(roost.x,roost.y+6,42,16,0,0,Math.PI*2);g.stroke();g.save();if(campaign.mode==='intro'&&labIntroShot().key==='roar'){const q=campaign.intro.elapsed/2.6,pulse=reduced?0:Math.sin(q*Math.PI);g.translate(roost.x+10,roost.y-10);g.scale(1+pulse*.045,1+pulse*.08);g.translate(-roost.x-10,-roost.y+10);}labDragon(roost.x+10,roost.y-10,118,t);g.restore();if(campaign.mode==='intro'&&labIntroShot().key==='roar'){const q=campaign.intro.elapsed/2.6;g.save();g.strokeStyle='#e9e4b7';g.lineWidth=1.5;for(let i=0;i<3;i++){const wave=(q*1.8+i/3)%1;g.globalAlpha=(1-wave)*.5;g.beginPath();g.ellipse(roost.x+53,roost.y-49,9+wave*53,6+wave*28,-.3,-1.2,1.2);g.stroke();}g.restore();}g.fillStyle=campaign.ingredients.every(Boolean)?'#ffdf8e':'#b3d1bf';g.font='bold 11px Georgia';g.textAlign='center';g.fillText(campaign.ingredients.every(Boolean)?'BOARD THE DRAGON':'DRAGON’S ROOST',roost.x,roost.y+37);
 for(const l of laboratory.landmarks.slice(0,1)){const p=labPoint(l);g.font='10px Georgia';g.textAlign='center';g.fillStyle='#d6dbb6';g.fillText(l.text,p.x,p.y+24);}
 if(actors){const p=labPoint(campaign.visual),moving=Math.hypot(campaign.player.x-campaign.visual.x,campaign.player.y-campaign.visual.y)*LAB.tile>1,bob=reduced?0:moving?Math.sin(t/57)*2:Math.sin(t/650)*.6;g.fillStyle='#02030c77';g.beginPath();g.ellipse(p.x,p.y+6,13,4,0,0,Math.PI*2);g.fill();labHero(p.x,p.y+4+bob,CHAPTER_VIEW.heroHeight,1,campaign.facing);labSpirit(t);}
 for(let i=0;i<28;i++){const x=70+(i*97)%1050,y=170+((i*101-t/80)%650+650)%650;g.fillStyle=i%3?'#bce6b477':'#ffe7a5aa';g.fillRect(x,y,2,2);}
}
function labSanctuary(t,backdrop=true){const g=labCtx;if(backdrop){labSky(t,true);labCloud(800,650,650,.35);}
 for(let i=0;i<8;i++){g.save();g.filter='hue-rotate(210deg) saturate(.45)';labAtlas(g,12,480+i*96,800,160,240);g.restore();}
 const outline=[[380,535],[570,390],[1100,390],[1300,535],[1130,650],[550,650]];
 g.save();g.beginPath();outline.forEach(([x,y],i)=>i?g.lineTo(x,y):g.moveTo(x,y));g.closePath();g.clip();const f=art.sprites[0];g.filter='hue-rotate(-38deg) saturate(.5) brightness(1.4)';for(let y=380;y<670;y+=40)for(let x=370;x<1310;x+=40)g.drawImage(images.atlas,f.x,f.y,f.w/2,f.h/2,x,y,40,40);g.restore();g.strokeStyle='#b8bb92';g.lineWidth=6;g.beginPath();outline.forEach(([x,y],i)=>i?g.lineTo(x,y):g.moveTo(x,y));g.closePath();g.stroke();
 for(const x of [570,1110]){const f=art.sprites[1];for(let y=290;y<530;y+=30){g.save();g.filter='hue-rotate(215deg) saturate(.4)';g.drawImage(images.atlas,f.x+f.w*.05,f.y+f.h*.55,f.w*.25,f.h*.35,x,y,38,30);g.restore();}g.fillStyle='#c7c5a0';g.fillRect(x-7,280,52,15);g.fillRect(x-8,520,54,20);labSprite(g,2,x+18,470,170);labTorch(x+18,370,t,x);}
 for(let i=0;i<20;i++){const a=Math.PI+i/19*Math.PI,x=859+Math.cos(a)*270,y=300+Math.sin(a)*120;g.save();g.translate(x,y);g.rotate(a+Math.PI/2);g.fillStyle=i%3?'#8fa98e':'#9cb398';g.fillRect(-20,-16,40,32);g.strokeStyle='#526e61';g.lineWidth=2;g.strokeRect(-20,-16,40,32);g.fillStyle='#d4d7b0';g.fillRect(-18,-15,36,3);g.restore();}
 for(const [x,y] of [[510,525],[1180,520],[1070,640],[610,630]]){labAtlas(g,5,x,y,35,48);labGlow(x,y-25,45,'#55e4cb',.16);labSpark(x,y-35,t+x,'#c3fff5');}
 labSprite(g,3,855,568,170);labSprite(g,4,995,532,125);if(backdrop){labHero(694,600,82);labArchitect(752,573,107);labDragon(1240,590,240,t);}labGlow(855,480,150,'#ffd66e',.28+.05*Math.sin(t/170));
}
function labCastle(t){const g=labCtx,img=images.kingdom;if(!img)return;const q=smooth(campaign.phaseTime/17),zoom=1+q*.07,w=1672*zoom,h=941*zoom;g.drawImage(img,(1672-w)*.65,(941-h)*.4,w,h);}
function labCaption(title,text){const g=labCtx;const shade=g.createLinearGradient(0,730,0,941);shade.addColorStop(0,'transparent');shade.addColorStop(1,'#031220ee');g.fillStyle=shade;g.fillRect(0,700,1672,241);g.textAlign='center';g.fillStyle='#f7dda6';g.font='32px Georgia';g.fillText(title,836,823);g.fillStyle='#d7e5d8';g.font='19px Georgia';g.fillText(text,836,860);}
function labFlight(t){const g=labCtx,p=campaign.phaseTime,up=campaign.mode==='ascent',roost=labPoint(LAB.roost);
 if(up&&p<6){const q=smooth(p/3),zoom=1+q*.65;g.save();g.translate(790,440);g.scale(zoom,zoom);g.translate(-roost.x,-roost.y);labRuins(t,false);labHero(roost.x-43+Math.min(p/6,1)*20,roost.y+28,38,1-smooth((p-4.7)/1));const reform=smooth((p-.6)/2.2);labArchitect(roost.x-12,roost.y+33,49,reform*(1-smooth((p-4.7)/1)));for(let i=0;i<24;i++){const angle=i*2.4+t/1100,r=(1-reform)*65+8;labSpark(roost.x-12+Math.cos(angle)*r,roost.y+5+Math.sin(angle)*r,t+i*70,LAB_MAGIC.light);}labGlow(roost.x-10,roost.y,70,LAB_MAGIC.glow,.3*(1-reform));g.restore();labCaption('The Architect returns','With all three ingredients secured, the heroes board the emerald dragon.');
 }else{labSky(t,true);if(up){g.save();g.translate(880,370);g.scale(.44,.44);g.translate(-836,-470);labSanctuary(t,false);g.restore();}else labCastle(t);
 const q=smooth((p-(up?6:0))/(up?12:17)),x=up?520+q*480:340+q*700,y=up?610-q*190:480+Math.sin(q*Math.PI)*-85;labDragon(x,y,up?420-q*125:450-q*90,t,true,true);for(let i=0;i<7;i++){g.strokeStyle='#dbf4e055';g.lineWidth=2;const xx=(t/3+i*270)%1800;g.beginPath();g.moveTo(xx,200+i*80);g.lineTo(xx-65,200+i*80);g.stroke();}labCaption(up?'Above the shattered gardens':'Home on emerald wings',up?'The Great Alchemist waits in the sanctuary above the clouds.':'The dragon carries the cure directly to the royal kingdom.');}
 // Crossfade masks the camera handoff from the rendered maze to the sky.
 const blackout=up?Math.max(0,1-Math.abs(p-6)/.7):0;if(blackout){g.fillStyle='rgba(226,241,220,'+blackout+')';g.fillRect(0,0,1672,941);}
}
function drawLaboratory(){if(!campaign.active)return;const g=labCtx,t=reduced?0:campaign.clock*1000;g.imageSmoothingEnabled=false;if(['loading','error','comic','lost'].includes(campaign.mode)){g.fillStyle='#040d15';g.fillRect(0,0,1672,941);return;}if(campaign.mode==='preview'&&images.labComic){const img=images.labComic,w=img.width/3,h=img.height/2,sw=w-6,sh=sw*941/1672;g.drawImage(img,w*2+3,h+(h-sh)*.68,sw,sh,0,0,1672,941);return;}if(!campaign.tiles){labSky(t);return;}
 if(campaign.mode==='intro'){labDrawIntro(t);return;}
 if(['ascent','homeflight'].includes(campaign.mode)){labFlight(t);return;}
 if(campaign.mode==='brewing'){labSanctuary(t);const q=Math.min(1,campaign.phaseTime/4);laboratory.stations.forEach((s,i)=>{const angle=i*Math.PI*2/3+t/650,r=160*(1-q);const x=855+Math.cos(angle)*r,y=460+Math.sin(angle)*r*.4-q*40;labSprite(g,s.sprite,x,y,55*(1-q)+6);labGlow(x,y-20,40,s.color,.3);});labGlow(855,430,130,'#ffe99b',.3+.1*Math.sin(t/110));if(q===1){g.strokeStyle='#fff0a7';g.lineWidth=3;g.strokeRect(843,395,24,40);g.fillStyle='#ffd85d';g.fillRect(846,402,18,30);labSpark(856,390,t,'#fffbe1');}labCaption('The guiding draught','Three gifts become a light that can reach through the curse.');return;}
 labRuins(t);drawRevealGuidance(g,t);if(campaign.panelArt)g.drawImage(campaign.panelArt,1304,0);if(campaign.mode==='paused'){g.fillStyle='#031222bb';g.fillRect(0,0,1304,941);g.fillStyle='#f7d898';g.font='38px Georgia';g.textAlign='center';g.fillText('PAUSED',590,450);g.font='20px Georgia';g.fillText('Press P or Resume to continue',590,490);}
}
