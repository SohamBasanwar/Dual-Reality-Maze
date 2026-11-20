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
const document={hidden:false,getElementById(id){if(!nodes.has(id))nodes.set(id,['world','labCanvas','labComic'].includes(id)?canvas():stub());return nodes.get(id)},createElement:tag=>tag==='canvas'?canvas():stub(),querySelector:stub,addEventListener(){}};
const actual={};for(const [key,file] of Object.entries({atlas:'atlas.png',hero:'explorer.png',spirit:'architect-spirit.png',cast:'story-cast.png',labAtlas:'laboratory-atlas.png',labComic:'chapter2-comic.png',dragonComic:'chapter2-dragon-comic.png',dragon:'emerald-dragon.png',dragonFlight:'emerald-dragon-flight.png',dragonRoar:'emerald-dragon-roar.png',kingdom:'kingdom-homecoming.png'}))actual[key]=await loadImage(path.resolve('images',file));
const context={document,window:{addEventListener(){}},Image:class{},matchMedia:()=>({matches:false}),performance:{now:()=>100000},setTimeout:()=>0,clearTimeout(){},requestAnimationFrame(){},console,actual};vm.createContext(context);
let script=(await fs.readFile('maze-source/work/engine-rendered.mjs','utf8')).replaceAll('export ','')+'\nconst ASSETS={};';
for(const f of ['game-rendered.js','render-scene.js','architect-spirit.js','story/story.js','story/quests.js','story/title.js','story/voice.js','chapters/laboratory-level.js','chapters/campaign.js','chapters/laboratory-render.js','chapters/laboratory-intro.js'])script+='\n'+await fs.readFile('maze-source/work/'+f,'utf8');
vm.runInContext(script,context);const run=s=>vm.runInContext(s,context);
run("Object.assign(images,actual);initScene();initArchitectSpiritArt();heroBounds=labTrimSheet(images.hero,1,1)[0];story.cast=labTrimSheet(images.cast,2,2);initLaboratoryArt();story.voice=false;campaign.active=true;campaign.ready=true;labReset();campaign.clock=3;drawLaboratory();");
await fs.writeFile('images/Chapter2_Ruins_Render.png',nodes.get('labCanvas').toBuffer('image/png'));
for(const [mode,time,name] of [['ascent',3,'Reformation'],['ascent',11,'Dragon_Ascent'],['brewing',5,'Upper_Sanctuary'],['homeflight',9,'Dragon_Homecoming']]){run(`campaign.mode='${mode}';campaign.phaseTime=${time};drawLaboratory()`);await fs.writeFile('images/Chapter2_'+name+'_Render.png',nodes.get('labCanvas').toBuffer('image/png'));}
// Prove that the live effects actually change pixels, including the dragon poses.
run("campaign.mode='playing';campaign.clock=3;drawLaboratory()");const still=nodes.get('labCanvas').toBuffer('image/png');run('campaign.clock=3.7;drawLaboratory()');if(still.equals(nodes.get('labCanvas').toBuffer('image/png')))throw Error('Environmental animation did not advance');
run("campaign.mode='homeflight';campaign.phaseTime=8;campaign.clock=1;drawLaboratory()");const flight=nodes.get('labCanvas').toBuffer('image/png');run('campaign.clock=1.16;drawLaboratory()');if(flight.equals(nodes.get('labCanvas').toBuffer('image/png')))throw Error('Dragon animation did not advance');
console.log('PASS: actual canvas renderer, continuous dragon animation, reformation, sanctuary brewing and grounded homecoming; environmental and flight animation change rendered pixels.');


for(const [shot,elapsed,name] of [[0,1.8,'Entry'],[3,1,'Dragon_Roar'],[6,1,'Entry_Dialogue'],[8,2.1,'Architect_Merge']]){run(`labStartIntro();labEnterIntroShot(${shot});campaign.intro.elapsed=${elapsed};drawLaboratory()`);await fs.writeFile('images/Chapter2_'+name+'_Render.png',nodes.get('labCanvas').toBuffer('image/png'));}
run('labFinishIntro();drawLaboratory()');await fs.writeFile('images/Chapter2_Large_Spirit_Render.png',nodes.get('labCanvas').toBuffer('image/png'));
console.log('PASS: Chapter II entry, roaring dragon, hero dialogue, Architect merge and enlarged spirit render with actual assets.');

// Persist the chapter-local shader outputs as project art references.
await fs.writeFile('images/chapter2-architect-green-cast.png',run('campaign.greenCast').toBuffer('image/png'));
await fs.writeFile('images/chapter2-architect-green-spirit.png',run('campaign.greenSpirit').toBuffer('image/png'));
await fs.writeFile('images/chapter2-sky-dragon-panel.png',run('campaign.panelArt').toBuffer('image/png'));
const castSource=createCanvas(actual.cast.width,actual.cast.height);castSource.getContext('2d').drawImage(actual.cast,0,0);
const sourceData=castSource.getContext('2d').getImageData(0,0,castSource.width,castSource.height).data;
const shadedData=run('campaign.greenCast').getContext('2d').getImageData(0,0,castSource.width,castSource.height).data;
let magicChanges=0;
for(let y=0;y<castSource.height;y++)for(let x=0;x<castSource.width;x++){
 const i=(y*castSource.width+x)*4,changed=sourceData[i]!==shadedData[i]||sourceData[i+1]!==shadedData[i+1]||sourceData[i+2]!==shadedData[i+2];
 if(changed){magicChanges++;if(!(x>castSource.width*.342&&x<castSource.width*.49&&y>castSource.height*.10&&y<castSource.height*.235))throw Error('Hand spell shader changed clothing or another character');}
 if(sourceData[i+3]!==shadedData[i+3])throw Error('Shader changed alpha');
}
if(magicChanges<1000)throw Error('Spell was not recolored');
console.log('PASS: green spell shader preserves clothing, skin, other characters and transparency; project copies of green cast/spirit and sky panel saved.');
