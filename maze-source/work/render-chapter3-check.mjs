import fs from 'node:fs/promises';
import vm from 'node:vm';
import {createRequire} from 'node:module';
import path from 'node:path';
import os from 'node:os';
const require=createRequire(import.meta.url);
const {createCanvas,loadImage}=require(path.join(os.homedir(),'.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@napi-rs/canvas'));
const nodes=new Map();
const stub=()=>({hidden:true,children:[],style:{setProperty(){},removeProperty(){}},classList:{add(){},remove(){},toggle(){}},setAttribute(){},addEventListener(){},append(...v){this.children.push(...v)},prepend(){},replaceChildren(){},focus(){}});
function canvas(w=1672,h=941){return Object.assign(createCanvas(w,h),stub());}
const document={hidden:false,getElementById(id){if(!nodes.has(id))nodes.set(id,['world','labCanvas','labComic','forestCanvas','forestComic'].includes(id)?canvas():stub());return nodes.get(id)},createElement:tag=>tag==='canvas'?canvas():stub(),querySelector:stub,addEventListener(){}};
const actual={};for(const [key,file] of Object.entries({atlas:'atlas.png',hero:'explorer.png',spirit:'architect-spirit.png',cast:'story-cast.png',labAtlas:'laboratory-atlas.png',labComic:'chapter2-comic.png',dragonComic:'chapter2-dragon-comic.png',dragon:'emerald-dragon.png',dragonFlight:'emerald-dragon-flight.png',dragonRoar:'emerald-dragon-roar.png',kingdom:'kingdom-homecoming.png',forestCast:'forest-cast.png',forestAtlas:'forest-atlas.png',forestPrologue:'chapter3-prologue.png',forestEpilogue:'chapter3-epilogue-robes-v2.png',forestDefeat:'chapter3-lost-to-forest.png',forestDragon:'emerald-dragon-unmounted.png',dryadAnimation:'dryad-animation-v2.png',memoryAnimation:'memory-animation-v2.png',orchardAtlas:'forest-orchard-v2.png',forestHeroes:'forest-heroes-v2.png',forestRowan:'forest-rowan-v2.png',forestRevisionComic:'forest-revision-comic-v2.png',forestRevisionAfter:'forest-revision-after-v2.png',forestMessenger:'forest-messenger-v3.png',dryadTalk:'dryad-talk-v3.png',architectWaiting:'architect-waiting-v4.png',guardianContact:'guardian-contact-v4.png',forestHeartTree:'forest-heart-tree-v1.png'}))actual[key]=await loadImage(path.resolve('images',file));
const context={document,window:{addEventListener(){}},Image:class{},matchMedia:()=>({matches:false}),performance:{now:()=>100000},setTimeout:()=>0,clearTimeout(){},requestAnimationFrame(){},console,actual};vm.createContext(context);
let script=(await fs.readFile('maze-source/work/engine-rendered.mjs','utf8')).replaceAll('export ','')+'\nconst ASSETS={};';
for(const f of ['game-rendered.js','render-scene.js','architect-spirit.js','story/story.js','story/quests.js','story/title.js','story/voice.js','chapters/laboratory-level.js','chapters/campaign.js','chapters/laboratory-render.js','chapters/laboratory-intro.js','chapters/forest-level.js','chapters/forest.js','chapters/forest-render.js'])script+='\n'+await fs.readFile('maze-source/work/'+f,'utf8');
vm.runInContext(script,context);const run=s=>vm.runInContext(s,context);
run("Object.assign(images,actual);initScene();initArchitectSpiritArt();heroBounds=labTrimSheet(images.hero,1,1)[0];story.cast=labTrimSheet(images.cast,2,2);story.voice=false;forest.active=true;forest.ready=true;initForestArt();forestClearRound();forestBeginOffering();forest.clock=3;drawForest();");
await fs.writeFile('images/Chapter3_Offering_Render.png',nodes.get('forestCanvas').toBuffer('image/png'));
run('forest.area="forest";forest.player={...FOREST.start};forest.visual={...FOREST.start};forestBeginHunt();drawForest()');
await fs.writeFile('images/Chapter3_Forest_Render.png',nodes.get('forestCanvas').toBuffer('image/png'));
run('forestClearRound();forestBeginPath();forest.player={x:4,y:21};forest.visual={...forest.player};drawForest()');
await fs.writeFile('images/Chapter3_Waiting_Render.png',nodes.get('forestCanvas').toBuffer('image/png'));
run('forestBeginOffering();forest.invulnerable=0;forest.player={...forestPlantPoint(forestPlants[0])};forest.visual={...forest.player};forestPlantCollision();forest.contact.elapsed=.3;drawForest()');
await fs.writeFile('images/Chapter3_Contact_Render.png',nodes.get('forestCanvas').toBuffer('image/png'));
run('forestClearRound();forestBeginHunt();forest.invulnerable=0;drawForest()');
const still=nodes.get('forestCanvas').toBuffer('image/png');run('forest.clock=3.7;drawForest()');if(still.equals(nodes.get('forestCanvas').toBuffer('image/png')))throw Error('Forest effects failed to animate');
for(const [seq,shot,time,name] of [['intro',2,2,'Failed_Merge'],['intro',4,2,'Dryad'],['permission',1,2.5,'Blessing'],['capture',3,1.2,'Capture'],['arrival',0,2,'Dragon_Arrival'],['homeflight',0,2.5,'Homecoming']]){
 if(seq==='intro')run('forestClearRound()');if(seq==='capture')run('forestBeginHunt();forest.player={x:33.5,y:9};forest.visual={...forest.player}');
 run("forestStartSequence('"+seq+"');forestEnterShot("+shot+");forest.shotTime="+time+";drawForest()");
 await fs.writeFile('images/Chapter3_'+name+'_Render.png',nodes.get('forestCanvas').toBuffer('image/png'));
}
console.log('PASS: actual Chapter III art renders; forest effects animate; offering, hunt, failed merge, Dryad, blessing, capture and both dragon flights render.');
