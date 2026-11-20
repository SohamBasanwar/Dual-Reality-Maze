const FOREST={...CHAPTER_VIEW,limit:600,jumpEvery:120,start:{x:4,y:18},dryad:{x:9,y:19},waiting:{x:7,y:19},heroSize:76,architectSize:86,dryadSize:98,memorySize:78,spiritSize:110};
function makeMemoryForest(){
 const grid=Array.from({length:FOREST.rows},()=>Array(FOREST.cols).fill(0));
 const clearings=[[3,17,7,19],[3,12,5,15],[4,15,4,17],[7,18,10,20],[9,14,11,16],[10,16,10,18],[5,14,9,14],
 [11,14,16,14],[15,11,18,15],[16,8,16,11],[13,7,17,9],[10,8,13,8],[9,3,11,8],[4,3,9,5],[3,5,5,8],
 [17,15,17,19],[14,19,20,20],[20,19,25,19],[25,16,29,20],[29,18,33,18],[32,14,34,18],[29,14,32,14],[28,11,30,14],
 [18,12,25,12],[24,9,28,12],[26,6,26,9],[25,3,29,6],[29,4,33,4],[32,4,32,9],[31,8,34,10],
 [16,4,16,7],[15,3,19,5],[19,4,25,4]];
 for(const [a,b,c,d] of clearings)for(let y=b;y<=d;y++)for(let x=a;x<=c;x++)grid[y][x]=1;
 for(const [x,y] of [[5,18],[10,15],[16,12],[5,4],[10,4],[15,8],[18,4],[27,5],[27,10],[28,18],[33,16]])grid[y][x]=0;
 const controls=[
  {x:12,y:14,name:'Root Gate A',type:'gate',color:'#edb85f'},
  {x:10,y:6,name:'Root Gate B',type:'gate',color:'#6bcfe9'},
  {x:26,y:7,name:'Root Gate C',type:'gate',color:'#9be16b'},
  {x:20,y:12,w:3,name:'Vine Bridge A',type:'bridge',color:'#f4d874'},
  {x:21,y:19,w:3,name:'Vine Bridge B',type:'bridge',color:'#6fe1bd'}
 ];
 const pears=[{x:3,y:13},{x:9,y:20},{x:11,y:15}];
 const groves=[{x:4,y:4,name:'First Light Grove'},{x:18,y:3,name:'Whispering Crown'},{x:33,y:9,name:'Rainfall Hollow'},{x:27,y:19,name:'The Old Orchard'},{x:15,y:20,name:'Yesterday’s Pool'},{x:25,y:10,name:'Fernheart Glade'}];
 const gapKeys=new Set(controls.filter(c=>c.type==='bridge').flatMap(c=>Array.from({length:c.w},(_,i)=>(c.x+i)+','+c.y))),walls=[];
 for(let y=0;y<FOREST.rows;y++)for(let x=0;x<FOREST.cols;x++)if(!grid[y][x]&&[-1,0,1].some(dy=>[-1,0,1].some(dx=>grid[y+dy]?.[x+dx])))walls.push({x,y});
 return {grid,controls,pears,groves,walls,gapKeys};
}
const memoryForest=makeMemoryForest();
const forestFruitTrees=[{x:7,y:5,name:'Golden Moonpear',color:'#ffdc69'},{x:28,y:5,name:'Emberheart',color:'#ff6961'},{x:28,y:20,name:'Violet Starplum',color:'#cb9aff'}];
function makeForestOrchard(){const grid=Array.from({length:23},()=>Array(37).fill(0));for(const [x1,y1,x2,y2] of [[1,18,7,20],[5,6,8,19],[3,3,11,9],[7,11,28,13],[24,3,32,9],[26,8,29,18],[23,15,33,21]])for(let y=y1;y<=y2;y++)for(let x=x1;x<=x2;x++)grid[y][x]=1;const walls=[];for(let y=0;y<23;y++)for(let x=0;x<37;x++)if(!grid[y][x]&&[-1,0,1].some(dy=>[-1,0,1].some(dx=>grid[y+dy]?.[x+dx])))walls.push({x,y});return {grid,walls,controls:[],gapKeys:new Set(),groves:[]};}
const forestOrchard=makeForestOrchard();
const forestPlants=[{a:{x:4,y:7},b:{x:10,y:7},speed:.9,offset:0},{a:{x:25,y:7},b:{x:31,y:7},speed:1.05,offset:3},{a:{x:24,y:16},b:{x:32,y:16},speed:.95,offset:7}];
function forestMap(){return forest.area==='orchard'?forestOrchard:memoryForest;}
function forestGrid(){if(forest.area==='orchard'){const grid=forestOrchard.grid.map(r=>r.slice());for(const p of forestFruitTrees)grid[p.y][p.x]=0;return grid;}if(forest.pathOpen){const grid=memoryForest.grid.map(r=>r.slice());for(let y=20;y<23;y++)for(let x=3;x<=5;x++)grid[y][x]=1;return grid;}return memoryForest.grid;}
function forestPlantPoint(m){const d=Math.hypot(m.b.x-m.a.x,m.b.y-m.a.y),v=((forest.clock*m.speed+m.offset)%(d*2)),q=(v>d?d*2-v:v)/d;return {x:m.a.x+(m.b.x-m.a.x)*q,y:m.a.y+(m.b.y-m.a.y)*q};}
function forestPoint(p){return {x:FOREST.ox+(p.x+.5)*FOREST.tile,y:FOREST.oy+(p.y+.5)*FOREST.tile};}
function forestControlPoint(c){return forestPoint({x:c.x+((c.w||1)-1)/2,y:c.y});}
function forestBlocked(){return forestMap().controls.flatMap((c,i)=>forest.open[i]&&forest.progress[i]>.97?[]:Array.from({length:c.w||1},(_,j)=>({x:c.x+j,y:c.y})));}

// Cinematic feet use reachable floor cells, never guessed pixel offsets or passages.
function forestStagePositions(player){const grid=memoryForest.grid,start={x:Math.round(player.x),y:Math.round(player.y)},seen=new Set([start.x+','+start.y]),queue=[{...start,steps:0}],candidates=[];
 for(let n=0;n<queue.length;n++){const p=queue[n];if(grid[p.y+1]?.[p.x]&&grid[p.y]?.[p.x-1]&&grid[p.y]?.[p.x+1]&&!memoryForest.controls.some(c=>labOnControl(p,c)))candidates.push(p);if(p.steps>=18)continue;for(const [dx,dy] of [[-1,0],[1,0],[0,-1],[0,1]]){const v={x:p.x+dx,y:p.y+dy,steps:p.steps+1},key=v.x+','+v.y;if(seen.has(key)||!grid[v.y]?.[v.x]||memoryForest.controls.some((c,i)=>labOnControl(v,c)&&(!forest.open[i]||forest.progress[i]<.97)))continue;seen.add(key);queue.push(v);}}
 const wallPenalty=p=>(Number(!grid[p.y+1]?.[p.x-1])+Number(!grid[p.y+1]?.[p.x+1]))*6;
 const clear=(a,b)=>Math.abs(a.x-b.x)*32>=84||Math.abs(a.y-b.y)*32>=108;
 let best=null,score=Infinity;for(const a of candidates){if(!clear(a,player))continue;for(const d of candidates){if(!clear(d,player)||!clear(a,d))continue;const cost=wallPenalty(a)+wallPenalty(d)+Math.hypot(a.x-player.x,a.y-player.y)+Math.hypot(d.x-player.x,d.y-player.y)+.1*(a.steps+d.steps)+(a.x>player.x?.2:0)+(d.x<player.x?.2:0);if(cost<score){score=cost;best={architect:{x:a.x,y:a.y},dryad:{x:d.x,y:d.y}};}}}
 if(!best)throw new Error('No safe cinematic floor staging near memory grove');return best;
}
function forestWaitingVisible(){return forest.area==='forest'&&['path','offeringReturn'].includes(forest.mode==='paused'?forest.resumeMode:forest.mode);}
