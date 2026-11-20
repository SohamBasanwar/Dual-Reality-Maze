import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import {project,workload,requestFor,cachedRecording,generateItem} from './pipeline.mjs';
const result=await workload(),{config,manifest}=result;
assert.equal(manifest.lines.length,50);
assert.equal(new Set(manifest.lines.map(l=>l.id)).size,50);
assert.equal(Object.keys(manifest.characters).length,7);
for(const line of manifest.lines){assert(config.characters[line.character]);assert(line.text&&line.emotionalContext&&line.delivery&&line.audioPath);assert(!line.text.includes('[excited]'),'Original subtitles are unmodified');}
const sample=manifest.lines.find(l=>l.id==='ch1-prologue-03');
assert.equal(sample.character,'king');assert.equal(sample.text,'“Bring my daughter home. I am counting on you.”');
const proof=await workload({scene:'ch1-prologue'});assert.equal(proof.plan.pendingLines,6);
for(const mutation of [{voiceSettings:{stability:1}},{modelId:'eleven_multilingual_v2'},{characters:{...config.characters,king:{...config.characters.king,voiceId:'different'}}}])assert.notEqual(requestFor(sample,{...config,...mutation}).hash,requestFor(sample,config).hash);
assert.notEqual(requestFor({...sample,delivery:'A manually revised performance direction.'},config).hash,requestFor(sample,config).hash);
assert(!requestFor(sample,{...config,modelId:'eleven_multilingual_v2'}).body.text.startsWith('['),'Non-tag models receive plain spoken text');
assert.throws(()=>requestFor({...sample,tags:['invented-unsupported-tag']},config));
assert.throws(()=>requestFor(sample,{...config,voiceSettings:{stability:.3}}));
let calls=0;
const fakeFetch=async(url,options)=>{calls++;assert(url.startsWith('https://api.elevenlabs.io/v1/text-to-speech/'));assert.equal(options.headers['xi-api-key'],'test-only-secret');assert(!options.body.includes('test-only-secret'));return{ok:true,headers:new Map([['content-type','audio/mpeg']]),arrayBuffer:async()=>Buffer.alloc(256,7)};};
const fixture={...sample,id:'test-fixture',audioPath:'voice/audio/test-fixture.mp3'};
const chosen={...config,characters:{...config.characters,king:{...config.characters.king,voiceId:'test-voice'}}};
const item={line:fixture,request:requestFor(fixture,chosen)};
const target=path.join(project,fixture.audioPath);
try{
 await assert.rejects(generateItem(item,chosen,{fetchImpl:fakeFetch,key:''}),/ELEVENLABS_API_KEY/);assert.equal(calls,0);
 await assert.rejects(generateItem(item,{...chosen,normalization:{enabled:true}},{fetchImpl:fakeFetch,key:'test-only-secret'}));assert.equal(calls,0,'Missing normalization tool must fail before a paid request');
 await generateItem(item,chosen,{fetchImpl:fakeFetch,key:'test-only-secret'});assert.equal(calls,1);
 assert(await cachedRecording(fixture,item.request));
 assert.equal(await cachedRecording(fixture,{...item.request,hash:'changed'}),null);
 assert(!(await fs.readFile(target+'.json','utf8')).includes('test-only-secret'));
 await fs.writeFile(target,Buffer.alloc(256,9));assert.equal(await cachedRecording(fixture,item.request),null,'Corrupted audio cannot enter the offline build');
 await assert.rejects(generateItem(item,chosen,{key:'test-only-secret',fetchImpl:async()=>({ok:false,status:429})}),/No automatic paid retry/);
}finally{await fs.rm(target,{force:true});await fs.rm(target+'.json',{force:true});await fs.rm(target+'.pending',{force:true});}
console.log(`PASS: 50 exact source lines, seven stable cast profiles, six-line proof scene, cache/settings invalidation, corruption checks, tag/model guards, credential isolation, and normalization preflight. No live API requests. Proof scene: ${proof.plan.requestCharacters} request characters.`);
