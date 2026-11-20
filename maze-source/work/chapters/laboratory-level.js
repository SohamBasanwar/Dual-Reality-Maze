// Chapter II data and navigation are independent of Chapter I's map and save state.
const LAB={cols:CHAPTER_VIEW.cols,rows:CHAPTER_VIEW.rows,tile:CHAPTER_VIEW.tile,ox:CHAPTER_VIEW.ox,oy:CHAPTER_VIEW.oy,limit:600,start:{x:4,y:18},brew:{x:31,y:4},roost:{x:31,y:4}};
function makeLaboratory(){
 const grid=Array.from({length:LAB.rows},()=>Array(LAB.cols).fill(0));
 // Connected irregular terraces, branches and courtyards. Everything beyond the rim is sky.
 const rooms=[[3,17,7,19],[6,14,6,17],[4,14,6,14],[4,12,4,14],[2,10,8,12],[8,9,8,10],[8,9,10,9],[10,5,10,9],[7,3,11,5],[5,4,7,4],[5,4,5,7],[3,7,5,7],[8,11,14,11],[14,8,18,11],[15,5,15,8],[15,5,18,5],[18,3,18,5],[16,11,16,15],[10,15,16,15],[10,15,10,19],[10,19,14,20],[16,15,19,15],[19,15,19,18],[18,18,21,20],[18,9,23,9],[23,8,26,11],[25,11,25,14],[23,14,27,14],[27,14,27,17],[24,17,30,19],[30,16,32,16],[30,16,30,17],[26,8,28,8],[28,5,28,8],[27,2,31,5],[31,3,32,4],[24,5,28,5],[24,3,24,5],[21,3,24,3]];
 const stretch=x=>x>=21?x+2:x;
 for(const [x1,y1,x2,y2] of rooms)for(let y=y1;y<=y2;y++)for(let x=stretch(x1);x<=stretch(x2);x++)grid[y][x]=1;
 for(const [x,y] of [[5,11],[15,9],[17,10],[11,19],[20,19],[26,18],[30,3],[8,4]])grid[y][stretch(x)]=0;
 const stations=[{x:9,y:3,name:'Amber crystal',color:'#ffc86b',sprite:5},{x:3,y:11,name:'Moonblossom',color:'#cf9dff',sprite:6},{x:31,y:18,name:'Dew of the veil',color:'#67e6ed',sprite:7}];
 const controls=[
  {x:12,y:11,w:1,h:1,name:'Gate A',type:'gate',color:'#ff343e'},
  {x:10,y:6,w:1,h:1,name:'Gate B',type:'gate',color:'#00baff'},
  {x:29,y:15,w:1,h:1,name:'Gate C',type:'gate',color:'#03f68d'},
  {x:20,y:9,w:3,h:1,name:'Bridge A',type:'bridge',color:'#ffb600'},
  {x:30,y:7,w:1,h:1,name:'Bridge B',type:'bridge',color:'#139aff'}
 ];
 const gaps=new Set(['20,8','20,9','20,10','21,8','21,9','21,10','22,8','22,9','22,10','29,7','30,7','31,7']),walls=[];
 for(let y=0;y<LAB.rows;y++)for(let x=0;x<LAB.cols;x++)if(!grid[y][x]&&!gaps.has(x+','+y)&&[-1,0,1].some(dy=>[-1,0,1].some(dx=>grid[y+dy]?.[x+dx])))walls.push({x,y});
 return {grid,stations,controls,walls,wallKeys:new Set(walls.map(p=>p.x+','+p.y)),gaps,stairs:[{x:6,y:15},{x:10,y:7},{x:16,y:13},{x:27,y:12},{x:30,y:6}],waterfalls:[{x:7,y:19},{x:14,y:20},{x:32,y:19},{x:33,y:5}],landmarks:[{x:4,y:20,text:'THE SUNKEN GARDENS'},{x:9,y:2,text:'SOLAR OBSERVATORY'},{x:30,y:1,text:'DRAGON’S ROOST'}]};
}
function labRoute(grid,start,goal,closed=[]){
 const queue=[{...start}],seen=new Map([[start.x+','+start.y,null]]),blocked=new Set(closed.map(p=>p.x+','+p.y));
 for(let n=0;n<queue.length;n++){const p=queue[n],id=p.x+','+p.y;if(p.x===goal.x&&p.y===goal.y){const out=[];let key=id;while(key!==null){const [x,y]=key.split(',').map(Number);out.unshift({x,y});key=seen.get(key)}return out;}
  for(const [dx,dy] of [[1,0],[-1,0],[0,1],[0,-1]]){const x=p.x+dx,y=p.y+dy,key=x+','+y;if(grid[y]?.[x]&&!seen.has(key)&&!blocked.has(key)){seen.set(key,id);queue.push({x,y})}}
 }return [];
}
const laboratory=makeLaboratory();

function labOnControl(p,c){return p.x>=c.x-.5&&p.x<c.x+(c.w||1)-.5&&p.y>=c.y-.5&&p.y<c.y+(c.h||1)-.5;}
function labBlockedCells(){return laboratory.controls.flatMap((c,i)=>campaign.open[i]&&campaign.progress[i]>.97?[]:Array.from({length:(c.w||1)*(c.h||1)},(_,j)=>({x:c.x+j%(c.w||1),y:c.y+Math.floor(j/(c.w||1))})));}
