// Shared presentation/motion contract for every chapter.
export const CHAPTER_VIEW=Object.freeze({width:1672,height:941,worldWidth:1304,tile:32,ox:64,oy:80,cols:37,rows:23,step:8,stepSeconds:.072,smoothing:24,heroHeight:51,spiritHeight:84});
export const STEP=CHAPTER_VIEW.step,TILE=CHAPTER_VIEW.tile,OX=CHAPTER_VIEW.ox,OY=CHAPTER_VIEW.oy,COLS=CHAPTER_VIEW.cols,ROWS=CHAPTER_VIEW.rows;
export const REVEAL_RULES=Object.freeze({duration:3000,recharge:12000,uses:3});
// One floor-graph search chooses the closest objective by walking distance.
// Gates/bridges are traversable in this plan; the renderer marks those needing power.
export function nearestRevealRoute(grid,start,targets,blocked=[]){
 const id=p=>p.x+','+p.y,closed=new Set(blocked.map(id)),seen=new Map([[id(start),null]]),queue=[start];
 if(!grid[start.y]?.[start.x])return null;
 const goals=new Map();for(const target of targets)for(const p of target.goals||[target])if(grid[p.y]?.[p.x]&&!closed.has(id(p))&&!goals.has(id(p)))goals.set(id(p),target);
 for(let n=0;n<queue.length;n++){const p=queue[n],key=id(p);if(goals.has(key)){const path=[];let k=key;while(k!==null){const [x,y]=k.split(',').map(Number);path.unshift({x,y});k=seen.get(k);}return {target:goals.get(key),path};}
  for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]]){const next={x:p.x+dx,y:p.y+dy},k=id(next);if(grid[next.y]?.[next.x]&&!closed.has(k)&&!seen.has(k)){seen.set(k,key);queue.push(next);}}
 }return null;
}
export const rooms=[
 [12,2,17,4],[15,4,15,7],[7,7,20,7],
 [21,3,23,5],[20,4,21,7],
 [8,3,10,7],[5,5,8,5],[5,5,5,9],[4,9,8,9],
 [8,7,8,14],[8,11,11,14],
 [1,9,3,16],[3,13,8,13],[3,16,6,16],[6,16,6,18],[6,18,10,18],
 [10,17,12,18],[13,11,17,15],[11,13,13,13],[13,7,13,11],
 [19,8,21,10],[19,7,19,8],[21,10,21,12],[21,12,24,12],
 [24,9,27,15],[25,6,25,9],[25,3,28,6],[28,5,31,5],
 [31,10,35,14],[27,15,33,15],[33,14,33,15],
 [14,17,19,20],[14,15,14,17],[11,17,14,17],
 [23,17,27,18],[26,15,26,17],[23,18,23,19]
];
export const cells=Array.from({length:ROWS},()=>Array(COLS).fill(0));
for(const [x1,y1,x2,y2] of rooms)for(let y=y1;y<=y2;y++)for(let x=x1;x<=x2;x++)cells[y][x]=1;
for(const [x,y] of [[2,11],[2,14],[9,12],[10,12],[15,13],[16,13],[26,11],[26,12],[16,18],[17,18],[32,11]])cells[y][x]=0;
export const pitCells=new Set();
for(let y=10;y<=16;y++)for(let x=22;x<=23;x++)pitCells.add(`${x},${y}`);
for(let y=9;y<=10;y++)for(let x=12;x<=14;x++)pitCells.add(`${x},${y}`);
export const center=(x,y)=>({x:OX+x*TILE+20,y:OY+y*TILE+20});
export const START=center(14,3),KEY=center(22,4),EXIT=center(34,12);
export const RUNES=[{...center(1,16),name:'Moon',color:'#bf84ff'},{...center(18,20),name:'Sun',color:'#ffca63'},{...center(28,4),name:'Star',color:'#55e9ff'}];
const tileRect=(x,y,w=1,h=1)=>[OX+x*TILE,OY+y*TILE,w*TILE,h*TILE];
const element=(name,type,color,x,y,w=1,h=1)=>{const r=tileRect(x,y,w,h);return {name,type,color,x,y,w,h,rect:r,barrier:[r[0],r[1],r[0]+r[2]-1,r[1]+r[3]-1]}};
export const ELEMENTS=[
 element('Gate A','gate','#ff343e',15,6),
 element('Gate B','gate','#00baff',12,13),
 element('Gate C','gate','#03f68d',25,8),
 element('Bridge A','bridge','#ffb600',22,12,2,1),
 element('Bridge B','bridge','#139aff',13,9,1,2)
];
export const LOCK=[OX+29*TILE,OY+15*TILE,OX+30*TILE-1,OY+16*TILE-1];
export const props=[
 {kind:'orb',x:17,y:3,color:'#ff354a'},{kind:'orb',x:26,y:4,color:'#15c9ff'},
 {kind:'orb',x:10,y:14,color:'#ffcc39'},{kind:'orb',x:27,y:10,color:'#ff4358'},
 {kind:'orb',x:25,y:18,color:'#36fa8d'},{kind:'orb',x:17,y:20,color:'#ffd653'},
 {kind:'statue',x:2,y:10},{kind:'statue',x:4,y:9},{kind:'statue',x:31,y:10},
 {kind:'barrel',x:8,y:3},{kind:'barrel',x:19,y:9},{kind:'barrel',x:28,y:5},
 {kind:'barrel',x:6,y:18},{kind:'barrel',x:15,y:17},
 {kind:'bones',x:9,y:11},{kind:'bones',x:20,y:10},{kind:'bones',x:24,y:18},
 {kind:'crystal',x:23,y:3},{kind:'crystal',x:27,y:3},{kind:'crystal',x:17,y:15},{kind:'crystal',x:35,y:10}
];
export const walls=[];
for(let y=0;y<ROWS;y++)for(let x=0;x<COLS;x++){
 if(cells[y][x]||pitCells.has(`${x},${y}`))continue;
 if([-1,0,1].some(dy=>[-1,0,1].some(dx=>cells[y+dy]?.[x+dx])))walls.push({x,y});
}
export const inside=(x,y,r)=>x>=r[0]&&y>=r[1]&&x<=r[2]&&y<=r[3];
export const snap=n=>Math.floor(n/STEP)*STEP+STEP/2;
export function walkable(x,y,states,hasKey=false){
 const tx=Math.floor((x-OX)/TILE),ty=Math.floor((y-OY)/TILE);
 if(cells[ty]?.[tx]!==1)return false;
 if(!hasKey&&inside(x,y,LOCK))return false;
 return !ELEMENTS.some((e,i)=>!states[i]&&inside(x,y,e.barrier));
}
export function route(from,to,states,hasKey=false){
 const sx=snap(from.x),sy=snap(from.y),tx=snap(to.x),ty=snap(to.y);
 if(!walkable(tx,ty,states,hasKey))return [];
 const id=(x,y)=>x+','+y,start=id(sx,sy),goal=id(tx,ty),queue=[[sx,sy]],seen=new Map([[start,null]]);
 for(let n=0;n<queue.length;n++){
  const [x,y]=queue[n],here=id(x,y);
  if(here===goal){const path=[];let cur=goal;while(cur!==start){const [px,py]=cur.split(',').map(Number);path.push({x:px,y:py});cur=seen.get(cur)}return path.reverse()}
  for(const [dx,dy] of [[STEP,0],[-STEP,0],[0,STEP],[0,-STEP]]){const nx=x+dx,ny=y+dy,next=id(nx,ny);if(!seen.has(next)&&walkable(nx,ny,states,hasKey)){seen.set(next,here);queue.push([nx,ny])}}
 }
 return [];
}
