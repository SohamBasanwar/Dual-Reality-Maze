// Every surface and object below is rendered independently from a tile map.
// Art comes from isolated tiles and sprites; no screenshot is used as a backdrop.
const art={sprites:[],torches:[],grass:[],vines:[],wallKeys:new Set(walls.map(p=>`${p.x},${p.y}`))};
const animation={elements:[0,0,0,0,0],time:0,portalFrames:0,flameFrames:0};
let cinematic=null;
const portalCanvas=document.createElement('canvas');portalCanvas.width=64;portalCanvas.height=88;
const portalCtx=portalCanvas.getContext('2d');const portalPixels=portalCtx.createImageData(64,88);
const hash=(x,y=0,k=0)=>{let a=Math.imul(x+17,374761393)^Math.imul(y+23,668265263)^Math.imul(k+7,1442695041);a=Math.imul(a^(a>>>13),1274126177);return (a^(a>>>16))>>>0};
const rand=(x,y=0,k=0)=>(hash(x,y,k)%10000)/10000;
const pixel=(x,y,w,h,color)=>{ctx.fillStyle=color;ctx.fillRect(Math.round(x),Math.round(y),w,h)};
function glow(x,y,r,color,alpha=1){ctx.save();ctx.globalAlpha=alpha;const g=ctx.createRadialGradient(x,y,0,x,y,r);g.addColorStop(0,color);g.addColorStop(1,'transparent');ctx.fillStyle=g;ctx.fillRect(x-r,y-r,r*2,r*2);ctx.restore()}
function polygon(points,color){ctx.fillStyle=color;ctx.beginPath();points.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();ctx.fill()}
function initScene(){
 const sheet=images.atlas,c=document.createElement('canvas');c.width=sheet.width;c.height=sheet.height;const g=c.getContext('2d');g.drawImage(sheet,0,0);const pixels=g.getImageData(0,0,c.width,c.height).data,cw=Math.floor(c.width/4),ch=Math.floor(c.height/4);
 for(let i=0;i<16;i++){const ox=i%4*cw,oy=Math.floor(i/4)*ch;let l=cw,t=ch,r=0,b=0;for(let y=2;y<ch-2;y++)for(let x=2;x<cw-2;x++)if(pixels[((oy+y)*c.width+ox+x)*4+3]>100){l=Math.min(l,x);r=Math.max(r,x);t=Math.min(t,y);b=Math.max(b,y)}art.sprites.push({x:ox+l,y:oy+t,w:r-l+1,h:b-t+1})}
 walls.forEach(({x,y})=>{
  if(cells[y+1]?.[x]&&hash(x,y)%5===0)art.torches.push({x:OX+x*TILE+16,y:OY+y*TILE+42,phase:rand(x,y)*9});
  if(!cells[y+1]?.[x]&&!art.wallKeys.has(`${x},${y+1}`)&&hash(x,y)%3===0)art.vines.push({x:OX+x*TILE+16,y:OY+y*TILE+22,h:35+rand(x,y)*60,phase:rand(y,x)*6});
 });
 for(let y=0;y<ROWS;y++)for(let x=0;x<COLS;x++)if(cells[y][x]&&hash(x,y)%3===0&&!RUNES.some(r=>Math.hypot(r.x-(OX+x*TILE+16),r.y-(OY+y*TILE+16))<42)&&!ELEMENTS.some(e=>inside(OX+x*TILE+16,OY+y*TILE+16,e.barrier)))art.grass.push({x:OX+x*TILE+(hash(y,x)%2?4:28),y:OY+y*TILE+24,h:15+rand(x,y)*13,phase:rand(x,y)*10});
 // Bake each wall once in both realities; avoid hundreds of live canvas filters.
 const cached=new Map();
 for(const w of walls){const px=OX+w.x*TILE,py=OY+w.y*TILE;ctx.clearRect(0,0,1672,941);ctx.save();ctx.translate(-px,22-py);wallTile(w.x,w.y);ctx.restore();const color=document.createElement('canvas');color.width=32;color.height=68;color.getContext('2d').drawImage(canvas,0,0,32,68,0,0,32,68);const gray=document.createElement('canvas');gray.width=32;gray.height=68;const gg=gray.getContext('2d');gg.filter='saturate(0)';gg.drawImage(color,0,0);cached.set(`${w.x},${w.y}`,{color,gray})}
 art.wallSprites=cached;
}
function sprite(index,x,base,w,h){const b=art.sprites[index];if(!b||b.w<1)return;h??=w*b.h/b.w;ctx.drawImage(images.atlas,b.x,b.y,b.w,b.h,Math.round(x-w/2),Math.round(base-h),w,h)}
function swaySprite(index,x,base,w,h,t,phase,hang=false){
 const b=art.sprites[index];if(!b)return;const strip=4;
 for(let sy=0;sy<h;sy+=strip){const f=sy/h,shift=(hang?f*f:(1-f)*(1-f))*Math.sin(t/650+phase+f*1.7)*3.5;ctx.drawImage(images.atlas,b.x,b.y+f*b.h,b.w,Math.min(strip/h*b.h,b.h-f*b.h),Math.round(x-w/2+shift),Math.round(base-h+sy),w,Math.min(strip,h-sy))}
}
function background(t){
 const g=ctx.createLinearGradient(0,0,0,941);g.addColorStop(0,'#02071a');g.addColorStop(.55,'#062048');g.addColorStop(1,'#005798');ctx.fillStyle=g;ctx.fillRect(0,0,1304,941);
 for(let layer=0;layer<3;layer++)for(let i=0;i<23;i++){
  const x=i*69-70+layer*13,y=rand(i,layer)*220,w=23+rand(i,layer,1)*63,h=170+rand(i,layer,2)*400;
  polygon([[x,y],[x+w,y+24],[x+w-9,y+h*.7],[x+w/2,y+h],[x+9,y+h*.6]],['#02081be6','#061336aa','#09255277'][layer]);
 }
 for(let i=0;i<15;i++){const x=(i*179+37)%1300,y=640+(i*71)%290;glow(x,y,80,'#047fee',.08+.035*Math.sin(t/1900+i))}
 const islands=[[95,88,115],[1242,121,115],[92,812,135],[260,850,100],[400,925,96],[985,886,105],[1210,816,156],[816,932,98]];
 islands.forEach(([x,y,w],i)=>{const bob=reduced?0:Math.sin(t/1800+i)*3;sprite(12,x,y+bob,w,w*1.1);if(i%2===0){sprite(5,x+5,y-w*.82+bob,30,42);sparkle(x+5,y-w*1.1+bob,t+i*290,'#5ceaff',1)}swaySprite(3,x+18,y+20+bob,20,54,t,i,true)});
}
function rockUnderside(){
 walls.forEach(({x,y})=>{
  if(cells[y+1]?.[x]||art.wallKeys.has(`${x},${y+1}`)||pitCells.has(`${x},${y+1}`))return;
  const px=OX+x*TILE,py=OY+(y+1)*TILE,depth=42+rand(x,y)*90;
  if(x%3===0){const b=art.sprites[12];ctx.drawImage(images.atlas,b.x,b.y+b.h*.39,b.w,b.h*.61,px-25,py-5,85,100+rand(x,y)*22)}
  polygon([[px,py-5],[px+32,py-5],[px+30,py+depth*.4],[px+23,py+depth*.77],[px+13,py+depth],[px+4,py+depth*.6]],'#160c37');
  polygon([[px+3,py],[px+14,py],[px+17,py+depth-5],[px+9,py+depth*.75]],'#27134f');
  polygon([[px+19,py],[px+30,py],[px+27,py+depth*.55],[px+20,py+depth*.82]],'#100b2b');
  for(let j=0;j<7;j++){const yy=py+j*11,xx=px+3+(hash(x,y,j)%16);if(yy<py+depth*.7)pixel(xx,yy,3+hash(x,j)%8,3,['#311955','#231348','#402061'][j%3])}
 });
}
function floorTile(x,y){const px=OX+x*TILE,py=OY+y*TILE;
 const b=art.sprites[0],variant=hash(x,y)%4;ctx.drawImage(images.atlas,b.x+(variant%2)*b.w/2,b.y+Math.floor(variant/2)*b.h/2,b.w/2,b.h/2,px,py,32,32);
 ctx.fillStyle=(hash(x,y)%3===0)?'#163a6018':'#02162719';ctx.fillRect(px,py,32,32);
 ctx.strokeStyle='#05243c';ctx.lineWidth=1;ctx.strokeRect(px+.5,py+.5,31,31);
 if(hash(x,y)%4===0){ctx.strokeStyle='#071e34';ctx.beginPath();ctx.moveTo(px+5,py+6);ctx.lineTo(px+12,py+13);ctx.lineTo(px+9,py+22);ctx.stroke()}
 if(hash(x,y)%3===0){pixel(px+5,py+5,2,2,'#215275');pixel(px+26,py+24,2,2,'#102d4d')}
}
function pitTile(x,y,t){const px=OX+x*TILE,py=OY+y*TILE;pixel(px,py,32,32,'#02162a');
 const shine=(Math.sin(t/800+x+y)+1)/2;pixel(px+2,py,2,32,'#036093');
 for(let i=0;i<4;i++){const yy=py+(i*8+t/40)%32,xx=px+7+Math.sin(t/550+i+x)*5;pixel(xx,yy,8+shine*5,1,i%2?'#125888':'#08739c')}
}
function wallTile(x,y){const px=OX+x*TILE,py=OY+y*TILE;
 const cached=art.wallSprites?.get(`${x},${y}`);if(cached){const p=cinematic?.active?cinematic.wallColor(px+16,py+16):1;if(p<1)ctx.drawImage(cached.gray,px,py-22);if(p>0){ctx.save();ctx.globalAlpha=p;ctx.drawImage(cached.color,px,py-22);ctx.restore()}return}
 ctx.save();if(cinematic?.active)ctx.filter=`saturate(${cinematic.wallColor(px+16,py+16)})`;
 const b=art.sprites[1];
 // A shaded side face and a separate top cap, placed by map occupancy.
 if(!art.wallKeys.has(`${x},${y+1}`)){
  ctx.drawImage(images.atlas,b.x+b.w*(.04+(hash(x,y)%3)*.30),b.y+b.h*.56,b.w*.27,b.h*.35,px,py+1,32,31);
  pixel(px,py+30,32,3,'#100b28');pixel(px+1,py+24,30,2,'#51256e');
 }
 ctx.drawImage(images.atlas,b.x+b.w*(.04+(hash(x,y)%3)*.30),b.y+b.h*.045,b.w*.255,b.h*.42,px,py-21,32,26);
 pixel(px+1,py-20,30,2,'#d899df');pixel(px,py-20,1,25,'#5f3684');pixel(px+31,py-20,1,25,'#472566');pixel(px+1,py+4,30,2,'#522974');
 if(hash(x,y)%3===0){pixel(px+5,py-11,2,2,'#b17cc4');pixel(px+22,py-3,3,1,'#5f3c87')}
 // Low, translucent contact shadows fall onto the neighbouring floor.
 if(cells[y+1]?.[x]){const g=ctx.createLinearGradient(px,py+32,px,py+44);g.addColorStop(0,'#05091f99');g.addColorStop(1,'#05091f00');ctx.fillStyle=g;ctx.fillRect(px,py+32,32,12)}
 ctx.restore();
}
function sparkle(x,y,t,color='#adfaff',size=1){const a=Math.max(0,Math.sin(t/470+x*1.8+y));if(a<.45)return;ctx.save();ctx.globalAlpha=a;pixel(x-1,y-5*size,2,10*size,color);pixel(x-5*size,y-1,10*size,2,color);pixel(x-1,y-1,3,3,'#f1ffff');ctx.restore()}
function torch(o,t){const {x,y,phase}=o;const flicker=Math.sin(t/89+phase)*.3+Math.sin(t/41+phase)*.15;
 glow(x,y-33,70,'#ff822b',.29+flicker*.10);sprite(4,x,y,21,31);
 for(let row=0;row<13;row++){const taper=(13-row)/13,sw=Math.sin(t/115+phase+row*.33)*(row/4),half=2+taper*4,yy=y-28-row*2;
  pixel(x+sw-half,yy,half*2,3,row>7?'#ff6c13':'#ff9b24');if(row<10)pixel(x+sw-half*.5,yy+1,half,2,row<5?'#fff4a3':'#ffd44d')}
 for(let i=0;i<3;i++){const f=((t/650+phase+i*.31)%1),sx=x+Math.sin(f*8+phase)*7;ctx.save();ctx.globalAlpha=1-f;pixel(sx,y-48-f*27,2,2,'#ffd679');ctx.restore()}
 animation.flameFrames++;
}
function crystal(x,y,t,w=33){sprite(5,x,y,w,w*1.28);glow(x,y-w*.5,35,'#29baff',.14+.04*Math.sin(t/500));sparkle(x+6,y-w*.82,t,'#99ffff');sparkle(x-11,y-w*.4,t+500,'#71d6ff',.7)}
function prop(o,t){const p=center(o.x,o.y),x=p.x-4,y=p.y+8;
 if(o.kind==='crystal'){crystal(x,y,t+o.x*73);return}
 if(o.kind==='statue'){sprite(8,x,y,41,73);return}
 if(o.kind==='barrel'){sprite(6,x,y,24,30);return}
 if(o.kind==='bones'){sprite(7,x,y,22,15);return}
 if(o.kind==='orb'){sprite(11,x,y,36,40);glow(x,y-27,16,o.color,.55);ctx.save();ctx.fillStyle=o.color;ctx.shadowColor=o.color;ctx.shadowBlur=10;ctx.beginPath();ctx.ellipse(x,y-29,8,10,0,0,Math.PI*2);ctx.fill();ctx.restore();pixel(x-3,y-35,4,4,'#eafffb');sparkle(x+4,y-34,t+o.x*91,o.color,.65)}
}
function drawGate(e,i,t){const [x,y,w,h]=e.rect,p=animation.elements[i],base=y+h-1,top=base-45;
 glow(x+w/2,base-18,40,e.color,.1);
 // Fixed masonry columns and moving portcullis share the same collision tile.
 for(const xx of [x+1,x+w-7]){pixel(xx,top-2,6,49,'#100e26');pixel(xx+1,top,4,45,'#665774');pixel(xx+1,top+6,2,34,e.color);for(let j=0;j<3;j++)pixel(xx,top+j*17,7,2,'#b5a0c9')}
 pixel(x,top-4,w,7,'#19122d');pixel(x+2,top-4,w-4,2,e.color);
 ctx.save();ctx.beginPath();ctx.rect(x+7,top+3,w-14,42);ctx.clip();const lift=p*44;
 for(let j=0;j<3;j++){const xx=x+9+j*6;pixel(xx,top+3-lift,3,41,e.color);pixel(xx,top+3-lift,1,41,'#fff3e0');polygon([[xx-1,base-lift-4],[xx+4,base-lift-4],[xx+1.5,base+2-lift]],e.color)}
 pixel(x+6,base-12-lift,w-12,3,e.color);ctx.restore();
 if(p>0&&p<1){for(let k=0;k<3;k++){pixel(x+4,top-7+k*3+(t/70)%3,2,2,'#c7b77a');pixel(x+w-5,top-7+k*3+(t/70)%3,2,2,'#c7b77a')}}
}
function drawBridge(e,i,t){const [x,y,w,h]=e.rect,p=animation.elements[i],vertical=h>w;ctx.save();ctx.translate(x+w/2,y+h/2);if(vertical)ctx.rotate(Math.PI/2);const len=vertical?h:w,wide=vertical?w:h;
 for(const yy of [-wide/2+2,wide/2-4]){pixel(-len/2,yy,len,3,'#4e4660');pixel(-len/2,yy,len,1,'#c0a783')}
 // Two hinged leaves deploy from opposite banks; collision waits for extension.
 for(const side of [-1,1]){
  const ext=(len/2-2)*p;ctx.save();ctx.translate(side*(len/2-1),0);ctx.scale(-side,1);
  if(ext>1){pixel(0,-wide/2+5,ext,wide-10,'#78501e');for(let j=0;j<ext;j+=7){pixel(j,-wide/2+6,Math.min(6,ext-j),wide-12,e.color);pixel(j,-wide/2+7,Math.min(6,ext-j),2,'#ffe2a0');pixel(j+2,wide/2-10,2,2,'#815624')}pixel(0,-wide/2+5,ext,2,'#eee0b5')}
  pixel(-2,-wide/2+1,5,wide-2,'#78502a');pixel(-1,-wide/2+1,2,wide-2,e.color);ctx.restore();
 }
 ctx.restore();if(p>.95)sparkle(x+w/2,y+h/2,t,e.color,.6);
}
function drawRunes(t){RUNES.forEach((r,i)=>{const active=state.runes[i],bob=Math.sin(t/550+i)*2;
 pixel(r.x-15,r.y-11,30,23,'#131d3f');pixel(r.x-13,r.y-10,26,2,'#617daf');pixel(r.x-12,r.y+8,24,2,'#080d20');
 if(state.mode==='ritual')return;glow(r.x,r.y-32,active?42:33,r.color,active?.32:.19);ctx.save();ctx.strokeStyle=active?'#f4edcc':r.color;ctx.lineWidth=2;ctx.translate(r.x,r.y-32+bob);ctx.beginPath();ctx.moveTo(0,-15);ctx.lineTo(13,0);ctx.lineTo(0,15);ctx.lineTo(-13,0);ctx.closePath();ctx.stroke();ctx.font='19px Georgia';ctx.fillStyle=r.color;ctx.textAlign='center';ctx.fillText(['☾','☼','✦'][i],0,6);ctx.font='bold 9px Georgia';ctx.fillStyle=active?'#fff1c9':r.color;ctx.fillText(r.name.toUpperCase(),0,-22);ctx.restore();sparkle(r.x+13,r.y-47,t+i*400,r.color,.65);
})}
function drawKey(t){if(state.key)return;const x=KEY.x,y=KEY.y-13+Math.sin(t/420)*3,unlocked=state.keyAwakened;
 glow(x,y,unlocked?54:27,unlocked?'#ffd45a':'#55416f',unlocked?.32:.14);ctx.save();ctx.translate(x,y);ctx.rotate(.25);ctx.strokeStyle=unlocked?'#ffdf78':'#55475f';ctx.lineWidth=3;
 ctx.beginPath();ctx.moveTo(0,-25);ctx.bezierCurveTo(-4,-19,-13,-22,-13,-12);ctx.bezierCurveTo(-13,-4,-5,-2,0,-7);ctx.bezierCurveTo(5,-2,13,-4,13,-12);ctx.bezierCurveTo(13,-22,4,-19,0,-25);ctx.stroke();
 polygon([[0,-20],[5,-13],[0,-8],[-5,-13]],unlocked?'#58e8fa':'#242233');pixel(-2,-5,4,33,unlocked?'#e9aa32':'#423b50');pixel(-1,-4,1,30,unlocked?'#fff0a5':'#63536a');
 for(const [xx,yy] of [[0,15],[0,24]]){pixel(xx,yy,12,3,unlocked?'#edba43':'#494152');pixel(9,yy,3,7,unlocked?'#ffe58c':'#665371')}
 for(const xx of [-16,16])polygon([[xx,-14],[xx+3,-11],[xx,-8],[xx-3,-11]],unlocked?'#ffd863':'#40354e');ctx.restore();
 if(unlocked){sparkle(x-13,y-23,t,'#fff4b8',.7);sparkle(x+15,y+15,t+700,'#ffe499',.5)}else{ctx.save();ctx.strokeStyle='#77618d';ctx.globalAlpha=.45;ctx.setLineDash([3,5]);ctx.lineDashOffset=-t/70;ctx.beginPath();ctx.ellipse(x,y,24,34,0,0,Math.PI*2);ctx.stroke();ctx.restore()}
}
function portal(t){const x=EXIT.x-4,base=EXIT.y+14,cy=base-60,sec=t/1000;
 const d=portalPixels.data;
 for(let yy=0;yy<88;yy++)for(let xx=0;xx<64;xx++){
  const u=(xx-31.5)/30,v=(yy-43.5)/41,r=Math.hypot(u,v),idx=(yy*64+xx)*4;
  if(r>1){d[idx+3]=0;continue}
  const a=Math.atan2(v,u),tunnel=Math.sin(a*3+r*19-sec*5)+Math.sin(a*5-r*25+sec*3)*.4;
  const ring=Math.pow((Math.sin(r*34-sec*6+a*2)+1)/2,5),core=Math.exp(-r*11),edge=Math.pow(r,8),wave=(tunnel+1.5)/3;
  d[idx]=24+wave*30+ring*60+core*160+edge*80;
  d[idx+1]=8+wave*45+ring*155+core*180+edge*40;
  d[idx+2]=180+wave*70+ring*40+core*100;d[idx+3]=255;
 }
 portalCtx.putImageData(portalPixels,0,0);ctx.drawImage(portalCanvas,x-31,cy-43,62,86);
 sprite(10,x,base+14,105,150);
 // Keep the opening visibly alive even if the atlas has a narrow arch opening.
 ctx.save();ctx.beginPath();ctx.ellipse(x,cy+6,25,36,0,0,Math.PI*2);ctx.clip();ctx.drawImage(portalCanvas,x-26,cy-31,52,74);ctx.restore();
 glow(x,cy,78,state.key?'#43cdff':'#7d4cff',.2+.05*Math.sin(sec*3));
 for(let i=0;i<8;i++){const a=sec*(i%2?.65:-.45)+i*.785,r=37+Math.sin(sec+i)*4;const px=x+Math.cos(a)*r,py=cy+Math.sin(a)*r*1.18;pixel(px,py,2,2,i%2?'#c8faff':'#9774ff')}
 animation.portalFrames++;
}
function drawHero(t){const p=state.visual,moving=Math.hypot(p.x-state.player.x,p.y-state.player.y)>1;const bob=moving?Math.sin(t/57)*2:Math.sin(t/650)*.6;ctx.save();ctx.fillStyle='#02030c77';ctx.beginPath();ctx.ellipse(p.x,p.y+2,13,4,0,0,Math.PI*2);ctx.fill();const b=heroBounds,h=CHAPTER_VIEW.heroHeight,w=h*b.w/b.h;ctx.translate(Math.round(p.x),Math.round(p.y+bob));if(state.facing<0)ctx.scale(-1,1);ctx.drawImage(images.hero,b.x,b.y,b.w,b.h,-w/2,-h,w,h);ctx.restore()}
function drawFog(t){if(!['playing','paused','lost'].includes(state.mode)||performance.now()<state.revealUntil)return;const p=state.visual,g=ctx.createRadialGradient(p.x,p.y,80,p.x,p.y,260);g.addColorStop(0,'#02061700');g.addColorStop(.48,'#0206170a');g.addColorStop(1,'#02061775');ctx.fillStyle=g;ctx.fillRect(0,0,1304,941)}
function ornament(x,y,w){ctx.strokeStyle='#88643e';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+w,y);ctx.stroke();for(const xx of [x,x+w/2,x+w])polygon([[xx,y-3],[xx+3,y],[xx,y+3],[xx-3,y]],'#d8b773')}
function panelBox(x,y,w,h){pixel(x,y,w,h,'#0b0e1a');ctx.strokeStyle='#414054';ctx.lineWidth=2;ctx.strokeRect(x,y,w,h);for(const [xx,yy,sx,sy] of [[x,y,1,1],[x+w,y,-1,1],[x,y+h,1,-1],[x+w,y+h,-1,-1]]){ctx.strokeStyle='#7a6774';ctx.lineWidth=2;ctx.beginPath();ctx.moveTo(xx,yy+16*sy);ctx.lineTo(xx+5*sx,yy+10*sy);ctx.lineTo(xx+4*sx,yy+4*sy);ctx.lineTo(xx+10*sx,yy+5*sy);ctx.lineTo(xx+16*sx,yy);ctx.stroke();pixel(xx+6*sx,yy+6*sy,2,2,'#bd9560')}}
function panelGem(x,y){polygon([[x,y-15],[x+14,y],[x,y+15],[x-14,y]],'#b18647');polygon([[x,y-11],[x+10,y],[x,y+11],[x-10,y]],'#06345f');polygon([[x,y-7],[x+5,y],[x,y+7],[x-5,y]],'#19c6ff');pixel(x-1,y-5,2,4,'#d0ffff')}
function renderPanel(elements=ELEMENTS,itemLabel='Key'){
 const g=ctx.createLinearGradient(1304,0,1672,941);g.addColorStop(0,'#080b17');g.addColorStop(.5,'#0a0d18');g.addColorStop(1,'#060811');ctx.fillStyle=g;ctx.fillRect(1304,0,368,941);
 pixel(1304,0,6,941,'#25223d');pixel(1310,0,3,941,'#8584a0');pixel(1313,0,3,941,'#16172c');pixel(1666,0,6,941,'#29263d');pixel(1662,0,3,941,'#747189');pixel(1313,0,351,6,'#514a6c');pixel(1313,934,351,7,'#514a6c');
 for(let i=0;i<66;i++){pixel(1306+(hash(i,1)%5),i*15,2,3,['#626887','#17162c','#90889d'][i%3]);pixel(1666+(hash(i,2)%4),i*15,2,2,'#858198')}
 panelBox(1320,12,337,916);
 ctx.textAlign='center';ctx.fillStyle='#ffe3a4';ctx.font='small-caps 49px Georgia';ctx.fillText('Dual-Reality',1488,77);ctx.font='small-caps 55px Georgia';ctx.fillText('Maze',1488,121);
 ornament(1343,107,68);ornament(1564,107,70);ornament(1407,141,164);panelGem(1488,141);
 panelBox(1329,160,320,114);ctx.fillStyle='#f9daa0';ctx.font='small-caps 28px Georgia';ctx.fillText('The Architect',1488,200);ctx.fillStyle='#bcb6cb';ctx.font='22px Georgia';ctx.fillText('Control the maze elements',1488,233);ctx.fillText('between realities.',1488,259);
 for(let i=0;i<5;i++){
  const e=elements[i],y=294+i*63.5,x=1340;ctx.strokeStyle='#27273b';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(1336,y+49);ctx.lineTo(1639,y+49);ctx.stroke();
  ctx.save();ctx.shadowColor=e.color;ctx.shadowBlur=7;ctx.strokeStyle=e.color;ctx.lineWidth=2;ctx.strokeRect(x,y,43,43);ctx.strokeRect(x+4,y+4,35,35);ctx.restore();
  for(const xx of [x+10,x+21,x+32]){pixel(xx,y+7,3,29,e.color);pixel(xx,y+7,1,29,'#efffff')}
  if(e.type==='bridge'){polygon([[x+21,y+10],[x+29,y+20],[x+21,y+30],[x+13,y+20]],e.color);pixel(x+20,y+15,2,11,'#10152f')}
  ctx.textAlign='left';ctx.fillStyle='#f4efea';ctx.font='22px Georgia';ctx.fillText(e.name,1404,y+29);
 }
 ornament(1338,612,302);panelBox(1329,626,320,129);
 ctx.textAlign='left';ctx.font='23px Georgia';ctx.fillStyle='#efe8dc';ctx.fillText('Time',1405,672);ctx.fillText(itemLabel,1405,727);
 ctx.strokeStyle='#e7c47a';ctx.lineWidth=4;ctx.beginPath();ctx.arc(1368,663,14,0,Math.PI*2);ctx.stroke();pixel(1365,640,6,7,'#e7c47a');pixel(1360,639,16,3,'#e7c47a');ctx.beginPath();ctx.moveTo(1368,654);ctx.lineTo(1368,664);ctx.lineTo(1375,669);ctx.stroke();
 ctx.save();ctx.translate(1368,720);ctx.rotate(.45);ctx.strokeStyle='#ffd358';ctx.lineWidth=5;ctx.beginPath();ctx.arc(0,-11,8,0,Math.PI*2);ctx.stroke();pixel(-2,-4,4,24,'#ffd358');pixel(0,12,10,4,'#ffd358');pixel(7,12,4,9,'#ffd358');ctx.restore();
 ctx.strokeStyle='#28283b';ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(1340,690);ctx.lineTo(1638,690);ctx.stroke();
 ornament(1340,771,298);
 panelBox(1329,786,321,126);pixel(1335,792,309,113,'#6c4b35');
 polygon([[1343,800],[1384,797],[1454,801],[1533,796],[1634,801],[1630,825],[1637,856],[1630,898],[1550,895],[1470,900],[1411,895],[1343,899],[1346,868],[1340,836]],'#cba574');
 for(let i=0;i<130;i++)pixel(1348+hash(i,5)%280,805+hash(i,6)%86,1+hash(i)%2,1,'#8c633334');
 for(const [x,y] of [[1375,864],[1598,862]]){for(let j=0;j<3;j++){const xx=x+j*14;polygon([[xx-19,y],[xx,y-36-j*4],[xx+22,y]],'#825f4180');polygon([[xx-7,y-22],[xx,y-36-j*4],[xx+8,y-21],[xx+2,y-25],[xx-1,y-22]],'#ddba8d66')}}
 ctx.textAlign='left';
}
function drawRevealGuidance(g,t){
 const current=activeReveal();if(!current)return;const {plan,owner}=current,points=plan.points,target=plan.beacon,now=performance.now(),fade=Math.min(1,(owner.revealUntil-now)/450),pulse=reduced?1:.85+.15*Math.sin(t/140);
 g.save();g.beginPath();g.rect(0,0,1304,941);g.clip();g.globalAlpha=fade;g.lineCap='round';g.lineJoin='round';
 const trace=()=>{g.beginPath();const p=current.kind==='maze'?owner.visual:current.kind==='lab'?labPoint(owner.visual):forestPoint(owner.visual);g.moveTo(p.x,p.y);for(const v of points)g.lineTo(v.x,v.y);};
 g.strokeStyle='#071921';g.lineWidth=9;trace();g.stroke();g.shadowBlur=14;g.shadowColor='#75fff4';g.strokeStyle='#4bf4e2';g.lineWidth=5;trace();g.stroke();g.shadowBlur=0;g.strokeStyle='#efffff';g.lineWidth=1.8;g.setLineDash([7,8]);g.lineDashOffset=reduced?0:-t/45;trace();g.stroke();g.setLineDash([]);
 for(const c of plan.closed){const p=c.point;g.strokeStyle='#ffbd52';g.shadowColor='#ffbd52';g.shadowBlur=12;g.lineWidth=4;g.strokeRect(p.x-17,p.y-23,34,39);g.fillStyle='#ffd995';g.font='bold 11px Georgia';g.textAlign='center';g.fillText(c.name,p.x,p.y+31);}
 const top=Math.max(90,target.y-(plan.target.height||45));g.shadowColor='#ffe889';g.shadowBlur=22;g.strokeStyle='#ffe889';g.lineWidth=3;g.globalAlpha=fade*pulse;g.beginPath();g.ellipse(target.x,target.y,27,11,0,0,Math.PI*2);g.stroke();g.fillStyle='#fff0a5';g.beginPath();g.moveTo(target.x,top+13);g.lineTo(target.x-9,top);g.lineTo(target.x+9,top);g.closePath();g.fill();g.shadowBlur=0;
 const label=plan.target.name;g.font='bold 13px Georgia';g.textAlign='center';const width=g.measureText(label).width+20,x=Math.max(width/2+8,Math.min(1296-width/2,target.x));g.fillStyle='#071921e8';g.fillRect(x-width/2,top-25,width,22);g.fillStyle='#fff0ad';g.fillText(label,x,top-9);g.restore();
}
function renderScene(t){
 if(cinematic?.active&&cinematic.renderOverride?.(t))return;
 pixel(0,0,1672,941,'#030614');ctx.save();
 if(cinematic?.active){const c=cinematic.camera;ctx.translate(c.screenX,470);ctx.scale(c.zoom,c.zoom);ctx.translate(-c.x,-c.y)}
 background(t);rockUnderside();
 for(const key of pitCells){const [x,y]=key.split(',').map(Number);pitTile(x,y,t)}
 for(let y=0;y<ROWS;y++)for(let x=0;x<COLS;x++)if(cells[y][x]&&!pitCells.has(`${x},${y}`))floorTile(x,y);
 ELEMENTS.forEach((e,i)=>{if(e.type==='bridge')drawBridge(e,i,t)});
 drawKey(t);
 const depth=[];
 walls.forEach(w=>depth.push({y:OY+(w.y+1)*TILE,draw:()=>wallTile(w.x,w.y)}));
 props.forEach(p=>depth.push({y:center(p.x,p.y).y+4,draw:()=>prop(p,t)}));
 art.grass.forEach(p=>depth.push({y:p.y,draw:()=>swaySprite(2,p.x,p.y,30,p.h+5,t,p.phase)}));
 ELEMENTS.forEach((e,i)=>{if(e.type==='gate')depth.push({y:e.rect[1]+e.rect[3],draw:()=>drawGate(e,i,t)})});
 art.torches.forEach(p=>depth.push({y:p.y,draw:()=>torch(p,t)}));
 depth.push({y:EXIT.y+15,draw:()=>portal(t)});
 if(!(cinematic?.active&&cinematic.hideHero))depth.push({y:state.visual.y,draw:()=>drawHero(t)});
 if(cinematic?.active)depth.push(...cinematic.actors(t));
 depth.sort((a,b)=>a.y-b.y).forEach(p=>p.draw());
 for(const p of art.vines)swaySprite(3,p.x,p.y+p.h,22,p.h,t,p.phase,true);
 for(const [x,y] of [[10,1],[1,12],[30,10]])swaySprite(9,OX+x*TILE+16,OY+y*TILE+58,31,64,t,x);
 drawRunes(t);if(cinematic?.active)cinematic.effects(t);
 if(!state.key){pixel(LOCK[0]+7,LOCK[1]+8,18,21,'#241e39');ctx.strokeStyle='#f5c762';ctx.lineWidth=3;ctx.strokeRect(LOCK[0]+10,LOCK[1]+2,12,15);pixel(LOCK[0]+8,LOCK[1]+14,16,12,'#ca943d');pixel(LOCK[0]+15,LOCK[1]+17,3,6,'#322044')}
 drawFog(t);drawRevealGuidance(ctx,t);
 for(let i=0;i<34;i++){const x=45+(i*137.7)%1230,y=100+((i*61.3-t/65)%790+790)%790;ctx.save();ctx.globalAlpha=.2+.2*Math.sin(t/600+i);pixel(x,y,2,2,i%3?'#43cbff':'#bc86ff');ctx.restore()}
 if(performance.now()<state.revealUntil){ctx.strokeStyle='#84dfff';ctx.lineWidth=1;ctx.globalAlpha=.14;for(let i=0;i<4;i++){ctx.beginPath();ctx.arc(state.visual.x,state.visual.y,((t/5+i*70)%350),0,Math.PI*2);ctx.stroke()}ctx.globalAlpha=1}
 drawArchitectSpirit(t);
 ctx.restore();ctx.save();if(cinematic?.active)ctx.globalAlpha=cinematic.uiFade;renderPanel();ctx.restore();
 if(state.mode==='paused'&&$('help').hidden){pixel(0,0,1304,941,'#03061788');ctx.textAlign='center';ctx.fillStyle='#ffe3a3';ctx.font='36px Georgia';ctx.fillText('PAUSED',650,455);ctx.font='19px Georgia';ctx.fillStyle='#cbc3dc';ctx.fillText('Press P to return',650,490)}
}
function render(t){
 const dt=Math.min((t-previous)/1000||0,.05);previous=t;
 if(loaded){
  if(typeof updateControllerInput==='function')updateControllerInput();
  if(typeof updateStoryVoice==='function')updateStoryVoice(t);
  if(typeof labUpdate==='function'&&campaign.active){labUpdate(dt);drawLaboratory();}
  if(typeof forestUpdate==='function'&&forest.active){forestUpdate(dt);drawForest();}
  if(typeof updateComicCountdown==='function')updateComicCountdown(t);
  if(typeof updateStoryFade==='function')updateStoryFade(dt);
  if(state.mode!=='paused')animation.time+=dt*1000;
  if(cinematic?.active)cinematic.update(dt);
  updateArchitectSpirit(dt);
  for(let i=0;i<5;i++){const target=state.open[i]?1:0;if(state.mode!=='paused'){const change=dt*(ELEMENTS[i].type==='bridge'?1.45:1.9);animation.elements[i]=Math.max(0,Math.min(1,animation.elements[i]+Math.sign(target-animation.elements[i])*Math.min(change,Math.abs(target-animation.elements[i]))))}}
  if(state.mode==='playing'){
   state.remaining=Math.max(0,state.remaining-dt);accumulator+=dt;if(accumulator>.15){updateUI();accumulator=0}if(state.remaining<=0)finish(false);
   if(state.mode==='playing'&&t-lastMove>CHAPTER_VIEW.stepSeconds*1000){
    const d=keys.has('w')||keys.has('arrowup')?[0,-1]:keys.has('s')||keys.has('arrowdown')?[0,1]:keys.has('a')||keys.has('arrowleft')?[-1,0]:keys.has('d')||keys.has('arrowright')?[1,0]:null;
    if(d){state.path=[];if(d[0])state.facing=d[0];step(...d);lastMove=t}else if(state.path.length){const next=state.path.shift();if(walkable(next.x,next.y,effectiveOpen(),state.key)){state.facing=Math.sign(next.x-state.player.x)||state.facing;state.player=next;state.steps++;visit()}else state.path=[];lastMove=t}
   }
  }
  const lerp=1-Math.exp(-dt*CHAPTER_VIEW.smoothing);state.visual.x+=(state.player.x-state.visual.x)*lerp;state.visual.y+=(state.player.y-state.visual.y)*lerp;
  if(typeof story==='undefined'||!['title','comic','comingSoon','epilogueLoading','campaign'].includes(story.phase))renderScene(reduced?0:animation.time);
 }
 requestAnimationFrame(render);
}
