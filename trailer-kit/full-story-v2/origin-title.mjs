// Editable title choreography: architectural construction and an exploring light.
const clamp=v=>Math.max(0,Math.min(1,v)),ease=v=>{v=clamp(v);return v*v*(3-2*v)};
function lettering(g,value,x,y,size,progress,color,dir=1){
 g.save();g.font=`bold ${size}px Georgia`;g.textBaseline='alphabetic';const inheritedAlpha=g.globalAlpha;
 for(let i=0;i<value.length;i++){const p=ease(progress*1.9-i/value.length*.9),w=g.measureText(value[i]).width;g.globalAlpha=inheritedAlpha*p;g.fillStyle=color;g.shadowColor='#cfb47788';g.shadowBlur=16*p;g.fillText(value[i],x+(1-p)*dir*100,y+(1-p)*24);x+=w;}g.restore();
}
function star(g,x,y,r,a){g.save();g.globalAlpha=a;g.strokeStyle='#fff0bf';g.lineWidth=1.5;g.beginPath();g.moveTo(x-r,y);g.lineTo(x+r,y);g.moveTo(x,y-r);g.lineTo(x,y+r);g.stroke();g.restore();}
export function originTitle(g,art,t,W,H){
 g.fillStyle='#030713';g.fillRect(0,0,W,H);const halo=g.createRadialGradient(960,500,0,960,500,1000);halo.addColorStop(0,'#231735');halo.addColorStop(1,'#020612');g.fillStyle=halo;g.fillRect(0,0,W,H);
 // A blueprint route is drawn from the Architect's side toward the Explorer.
 const route=[[170,720],[430,720],[430,590],[690,590],[690,770],[1030,770],[1030,610],[1390,610],[1390,420],[1750,420]],p=clamp(t/3.2),steps=route.length-1;
 g.save();g.strokeStyle='#a28df488';g.lineWidth=3;g.setLineDash([7,9]);g.beginPath();g.moveTo(...route[0]);
 for(let j=0;j<steps;j++){const q=clamp(p*steps-j);if(q>0){const a=route[j],b=route[j+1];g.lineTo(a[0]+(b[0]-a[0])*q,a[1]+(b[1]-a[1])*q);}}g.stroke();g.setLineDash([]);
 const ix=Math.min(steps-1,Math.floor(p*steps)),part=Math.min(1,p*steps-ix),a=route[ix],b=route[ix+1],lx=a[0]+(b[0]-a[0])*part,ly=a[1]+(b[1]-a[1])*part;
 const light=g.createRadialGradient(lx,ly,0,lx,ly,70);light.addColorStop(0,'#fff0aaee');light.addColorStop(.2,'#e1b35199');light.addColorStop(1,'#e1b35100');g.fillStyle=light;g.fillRect(lx-70,ly-70,140,140);star(g,lx,ly,12,.9);g.restore();
 const phraseFade=1-ease((t-2.9)/.8);g.save();g.globalAlpha=phraseFade;
 lettering(g,'One shapes the path.',220,430,65,ease(t/.95),'#e7d4b1',-1);
 lettering(g,'One dares to follow.',650,550,65,ease((t-.95)/1.05),'#e7d4b1',1);g.restore();
 // Portal artwork spreads outward from a magical seam, revealing the world.
 const reveal=ease((t-3.1)/1.05);g.save();g.beginPath();g.rect(0,0,W*reveal,H);g.clip();const z=1.045+(t-3.1)*.005;g.globalAlpha=reveal;g.drawImage(art,(W-W*z)/2,(H-H*z)/2,W*z,H*z);
 const shade=g.createLinearGradient(0,0,W,0);shade.addColorStop(0,'#030713f2');shade.addColorStop(.58,'#030713bb');shade.addColorStop(1,'#03071305');g.fillStyle=shade;g.fillRect(0,0,W,H);g.restore();
 if(reveal>0&&reveal<1){const x=W*reveal,glow=g.createLinearGradient(x-70,0,x+30,0);glow.addColorStop(0,'#b8a4ff00');glow.addColorStop(.8,'#e9d9ff99');glow.addColorStop(1,'#b8a4ff00');g.fillStyle=glow;g.fillRect(x-70,0,100,H);}
 const glint=g.createLinearGradient((t-3.5)*250-300,0,(t-3.5)*250+170,0);glint.addColorStop(0,'#d2b779');glint.addColorStop(.5,'#fff9df');glint.addColorStop(1,'#c3a05c');
 lettering(g,'DUAL-REALITY',130,400,94,clamp((t-3.65)/1.25),glint,-1);
 // MAZE letters slide in along the route; the golden point explores their faces.
 lettering(g,'MAZE',130,580,153,clamp((t-4.35)/1.25),glint,1);
 const sub='THE ARCHITECT’S OATH',subP=clamp((t-5.15)/1.2);g.save();g.font='bold 32px Georgia';let sx=138;
 for(let i=0;i<sub.length;i++){const q=ease(subP*1.75-i/sub.length*.75);g.globalAlpha=q;g.fillStyle='#e8cf9d';g.fillText(sub[i],sx,725-(1-q)*38);sx+=g.measureText(sub[i]).width;}g.restore();
 g.save();g.globalAlpha=ease((t-4.9)/.8);g.strokeStyle='#b89b64';g.lineWidth=2;g.beginPath();g.moveTo(136,645);g.lineTo(780,645);g.stroke();g.restore();
 for(let j=0;j<84;j++){const x=(j*179+t*(j%3?9:-5))%W,y=H-((j*71+t*(15+j%11))%(H+50)),alpha=(.15+j%5*.1)*clamp(t/.7);g.fillStyle=`rgba(${j%3?226:154},${j%3?194:132},${j%3?117:255},${alpha})`;g.beginPath();g.arc(x,y,1+j%3,0,Math.PI*2);g.fill();if(j%9===0)star(g,x,y,5+3*Math.sin(t+j),alpha);}
 const flash=Math.max(0,1-Math.abs(t-3.65)/.15)*.18;g.fillStyle=`rgba(234,222,255,${flash})`;g.fillRect(0,0,W,H);
}
