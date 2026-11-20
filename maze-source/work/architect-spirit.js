// Selection feedback shares the game's existing control state; it never owns a timer or passage.
const architectSpirit={selected:0,x:0,y:0,fromX:0,fromY:0,travel:1,pulses:[],frames:[]};
function spiritAnchor(index){const [x,y,w,h]=ELEMENTS[index].rect;return {x:x+w/2-34,y:y+h/2-20};}
function resetArchitectSpirit(){const p=spiritAnchor(state.selected);Object.assign(architectSpirit,{selected:state.selected,x:p.x,y:p.y,fromX:p.x,fromY:p.y,travel:1,pulses:[]});}
function moveArchitectSpirit(index){
 const s=architectSpirit;if(s.selected===index)return;
 s.selected=index;s.fromX=s.x;s.fromY=s.y;s.travel=reduced?1:0;
 if(reduced){const p=spiritAnchor(index);s.x=p.x;s.y=p.y;}
}
function pulseArchitectSpirit(index,blocked=false){
 const s=architectSpirit;s.pulses=s.pulses.filter(p=>p.index!==index);
 s.pulses.push({index,blocked,age:0,duration:blocked?.24:.36});
}
function initArchitectSpiritArt(){
 const img=images.spirit,c=document.createElement('canvas');c.width=img.width;c.height=img.height;
 const g=c.getContext('2d');g.drawImage(img,0,0);const pixels=g.getImageData(0,0,c.width,c.height).data,cw=Math.floor(c.width/2);
 architectSpirit.frames=[];
 for(let i=0;i<2;i++){
  let left=cw,top=c.height,right=-1,bottom=-1;
  for(let y=0;y<c.height;y++)for(let x=0;x<cw;x++)if(pixels[(y*c.width+i*cw+x)*4+3]>50){left=Math.min(left,x);top=Math.min(top,y);right=Math.max(right,x);bottom=Math.max(bottom,y);}
  if(right<left)throw Error('Architect spirit artwork is empty');
  architectSpirit.frames.push({x:i*cw+left,y:top,w:right-left+1,h:bottom-top+1});
 }
 resetArchitectSpirit();
}
function updateArchitectSpirit(dt){
 if(state.mode!=='playing')return;
 const s=architectSpirit;moveArchitectSpirit(state.selected);
 s.travel=Math.min(1,s.travel+dt/.28);const p=s.travel*s.travel*(3-2*s.travel),to=spiritAnchor(s.selected);
 s.x=s.fromX+(to.x-s.fromX)*p;s.y=s.fromY+(to.y-s.fromY)*p-(reduced?0:Math.sin(s.travel*Math.PI)*22);
 for(const pulse of s.pulses)pulse.age+=dt;s.pulses=s.pulses.filter(p=>p.age<p.duration);
}
function drawArchitectSpirit(t){
 if(!['playing','paused'].includes(state.mode)||cinematic?.active||!architectSpirit.frames.length)return;
 const s=architectSpirit,e=ELEMENTS[state.selected],[x,y,w,h]=e.rect,cx=x+w/2,cy=y+h/2;
 const cast=s.pulses.find(p=>p.index===state.selected&&!p.blocked),blocked=s.pulses.some(p=>p.index===state.selected&&p.blocked);
 const color=blocked?'#ff9caa':'#dbadff',bob=reduced?0:Math.sin(t/340)*2.5,base=s.y+bob;
 ctx.save();
 // Always show the exact selected passage, including while the spirit is travelling.
 glow(cx,cy,43,'#a45aff',.2);ctx.strokeStyle=color;ctx.lineWidth=2;ctx.setLineDash([5,3]);ctx.strokeRect(x-5,y-7,w+10,h+12);ctx.setLineDash([]);
 ctx.globalAlpha=.65;ctx.strokeStyle=color;ctx.lineWidth=1;ctx.beginPath();ctx.moveTo(s.x+8,base-10);ctx.quadraticCurveTo((s.x+cx)/2,base+12,cx,cy);ctx.stroke();ctx.globalAlpha=1;
 if(!reduced&&s.travel<1)for(let i=1;i<=5;i++){const q=Math.max(0,s.travel-i*.045);ctx.globalAlpha=(1-i/6)*.45;pixel(s.fromX+(spiritAnchor(s.selected).x-s.fromX)*q,s.fromY+(spiritAnchor(s.selected).y-s.fromY)*q-16,3,3,'#dcb6ff');}
 ctx.globalAlpha=1;glow(s.x,base-26,37,'#a55bff',cast?.28:.13);
 const frame=s.frames[cast?1:0],height=CHAPTER_VIEW.spiritHeight,width=height*frame.w/frame.h;
 ctx.globalAlpha=.78;ctx.drawImage(images.spirit,frame.x,frame.y,frame.w,frame.h,s.x-width/2,base-height,width,height);ctx.globalAlpha=1;
 // Keep the passage label fixed to the target so rapid dial movements remain legible.
 const label=e.name+' · '+(state.open[state.selected]?'ON':'OFF');ctx.font='bold 11px Georgia';ctx.textAlign='center';
 const labelWidth=ctx.measureText(label).width+16;pixel(cx-labelWidth/2,y+h+10,labelWidth,18,'#150e29ed');ctx.fillStyle='#f3dfff';ctx.fillText(label,cx,y+h+23);
 for(const pulse of s.pulses){
  const [px,py,pw,ph]=ELEMENTS[pulse.index].rect,tx=px+pw/2,ty=py+ph/2,q=pulse.age/pulse.duration;
  ctx.globalAlpha=(1-q)*.8;ctx.strokeStyle=pulse.blocked?'#ff9caa':'#f1cbff';ctx.lineWidth=2;
  ctx.beginPath();ctx.ellipse(tx,ty,Math.max(pw/2,18)+(reduced?2:q*24),Math.max(ph/2,12)+(reduced?2:q*13),0,0,Math.PI*2);ctx.stroke();
  if(!pulse.blocked&&!reduced){for(let i=0;i<8;i++){const a=i*Math.PI/4,r=12+q*28;pixel(tx+Math.cos(a)*r,ty+Math.sin(a)*r,2,4,'#ead1ff');}glow(tx,ty,35,'#c38aff',(1-q)*.3);}
 }
 ctx.restore();
}
resetArchitectSpirit();
window.architectDiagnostics=()=>({selected:state.selected,name:ELEMENTS[state.selected].name,x:architectSpirit.x,y:architectSpirit.y,travel:architectSpirit.travel,pulses:architectSpirit.pulses.map(p=>({...p})),visible:['playing','paused'].includes(state.mode)&&!cinematic?.active});
