import fs from 'node:fs/promises';
import path from 'node:path';
import crypto from 'node:crypto';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
import {execFile} from 'node:child_process';
import {promisify} from 'node:util';
export const project=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
export const voiceRoot=path.join(project,'voice');
export const normalizeText=s=>s.replace(/^[“”]|[“”]$/g,'').trim();
const digest=v=>crypto.createHash('sha256').update(JSON.stringify(v)).digest('hex');
const readSource=f=>fs.readFile(path.join(project,'maze-source/work',f),'utf8');
function declaration(source,name){const m=source.match(new RegExp('const '+name+'=([\\s\\S]*?\\n[\\]\\}]);'));if(!m)throw Error('Missing dialogue collection '+name);return vm.runInNewContext('('+m[1]+')',{}, {timeout:1000});}
const tones={urgent:{emotion:'fear / urgency',tags:['worried'],delivery:'Quick, clear appeal; a person asking for help, not a theatrical scream.'},grave:{emotion:'concern / grief',tags:['sad'],delivery:'Measured, restrained gravity. Let difficult news settle.'},gentle:{emotion:'reassurance',tags:['calm'],delivery:'Soft, sincere conversation; protect the listener without whispering unnecessarily.'},resolute:{emotion:'determination',tags:['determined'],delivery:'Steady conviction directed toward a companion.'},joyful:{emotion:'joy / relief',tags:['excited'],delivery:'Warm relief or discovery; avoid excessive volume.'},worried:{emotion:'uncertainty / concern',tags:['worried'],delivery:'A small hesitation and genuine concern.'},wonder:{emotion:'curiosity / wonder',tags:['curious'],delivery:'Bright discovery with room for a small breath.'},steady:{emotion:'composure',tags:[],delivery:'Natural conversational delivery.'}};
export async function compileManifest(){
 const config=JSON.parse(await fs.readFile(path.join(voiceRoot,'voice-config.json'),'utf8'));
 const overrides=JSON.parse(await fs.readFile(path.join(voiceRoot,'dialogue-overrides.json'),'utf8'));
 const story=await readSource('story/story.js'),quests=await readSource('story/quests.js'),lab=await readSource('chapters/campaign.js'),intro=await readSource('chapters/laboratory-intro.js'),forest=await readSource('chapters/forest.js');
 const lines=[];
 function add(id,chapter,scene,role,text,tone,context,source){
  if(!config.characters[role])throw Error('Unknown speaker '+role);
  const performance=tones[tone]||tones.steady;
  const line={id,chapter,scene,character:role,text,tone,emotionalContext:context,...performance,source,audioPath:`voice/audio/${chapter}/${role}/${id}.mp3`};
  const override=overrides[id]||{};
  for(const key of Object.keys(override))if(!['emotion','tags','delivery','emotionalContext','voiceSettings','modelId'].includes(key))throw Error(`Unsupported override ${id}.${key}; original text and speaker are immutable.`);
  Object.assign(line,override);lines.push(line);
 }
 const collections=[['ch1','prologue',story,'storyPanels','story/story.js'],['ch1','epilogue',quests,'epiloguePanels','story/quests.js'],['ch2','comic',lab,'labPanels','chapters/campaign.js'],['ch3','comic',forest,'forestPanels','chapters/forest.js']];
 for(const [chapter,scene,source,name,file]of collections){const panels=declaration(source,name);panels.forEach((p,i)=>add(`${chapter}-${scene}-${String(i+1).padStart(2,'0')}`,chapter,`${scene}:${p.title}`,p.speaker,p.quote,p.tone||'steady',p.text,file));}
 const constants={};for(const name of ['runeInstruction','runeCelebration'])constants[name]=vm.runInNewContext(story.match(new RegExp('const '+name+'=([^;]+);'))[1]);
 for(const [source,file,scene]of [[story,'story/story.js','opening'],[quests,'story/quests.js','finale']]){
  const pattern=/cue\('([^']+)','([^']*)',('(?:\\.|[^'\\])*'|runeInstruction|runeCelebration),([.\d]+)\)/g;
  for(const m of source.matchAll(pattern)){const text=vm.runInNewContext(m[3],constants),role=m[2].toLowerCase(),key=m[1],tone=key==='key'?'joyful':role==='princess'?'urgent':key==='sleep'?'worried':key==='curse'?'grave':'resolute';
   add('ch1-cue-'+key,'ch1',key==='key'?'rune-awakening':scene,role,text,tone,key==='sleep'?'The heroes have reached the Princess, but she will not wake.':key==='oath'?'The Architect promises to become the path before dissolving into the maze.':key==='key'?'The three collected runes awaken the golden key.':scene==='opening'?'The Princess is taken through the portal; the companions plan their rescue.':'The Architect reforms and both companions discover the sleeping Princess. ',file);
  }
 }
 declaration(intro,'LAB_INTRO_SHOTS').forEach((s,i)=>{if(s.role)add('ch2-intro-'+s.key,'ch2','opening:'+s.key,s.role,s.text,s.tone,s.key==='explorer'?'After the dragon roars, Rowan recognizes their ride.':'The Architect offers to enter the ruins and help gather the ingredients.','chapters/laboratory-intro.js');});
 for(const [name,shots]of Object.entries(declaration(forest,'forestSequences')))for(const s of shots)if(s.role)add('ch3-sequence-'+name+'-'+s.key,'ch3',name+':'+s.key,s.role,s.text,s.tone,name==='capture'?'The memory is treated gently and chooses to enter the jar.':name==='intro'?'The living forest resists the Architect; its guardian questions the intrusion.':'The Dryad invites cooperation with her forest.','chapters/forest.js');
 // Standalone game events. Match the exact original literal; fail if a story edit invalidates a mapping.
 const events=[
  ['ch2-defeat','ch2','bad-ending','king','I will not lose you. If the light cannot save you… then let the darkness answer.','grave','The cure failed to arrive; grief drives the King toward forbidden magic.',lab,'chapters/campaign.js'],
  ['ch2-flight-ascent','ch2','ascent','explorer','The ingredients are safe. Come back to us, Architect. It’s time to fly!','wonder','The ingredients are gathered and the Architect can rejoin Rowan.',lab,'chapters/campaign.js'],
  ['ch2-flight-home','ch2','homeflight','explorer','Hold tight! We’re taking the cure home.','joyful','The cure is ready; the heroes return on the emerald dragon.',lab,'chapters/campaign.js'],
  ['ch2-brewing','ch2','brewing','alchemist','Amber, blossom, and dew. Let this light find her.','resolute','The Alchemist carefully unites the three ingredients.',lab,'chapters/campaign.js'],
  ['ch3-defeat','ch3','bad-ending','dryad','The forest will keep her safe. But the little memory has taken root… and cannot return.','grave','The memory hunt timed out. The guardian offers sorrowful comfort, not a threat.',forest,'chapters/forest.js']
 ];
 for(const [id,ch,scene,role,text,tone,context,source,file]of events){if(!source.includes(text))throw Error('Dialogue changed; update event mapping '+id);add(id,ch,scene,role,text,tone,context,file);}
 const ids=new Set(lines.map(l=>l.id));if(ids.size!==lines.length)throw Error('Duplicate dialogue IDs');for(const id of Object.keys(overrides))if(!ids.has(id))throw Error('Unknown dialogue override '+id);
 const manifest={version:1,sourceOfTruth:'Existing story dialogue; descriptions remain silent.',characters:config.characters,lines};
 await fs.writeFile(path.join(voiceRoot,'dialogue-manifest.json'),JSON.stringify(manifest,null,2)+'\n');
 return{config,manifest};
}
export function requestFor(line,config){
 const cast=config.characters[line.character],modelId=line.modelId||config.modelId;
 const tags=config.audioTagsEnabled&&['eleven_v3','eleven_v4'].includes(modelId)?line.tags:[];
 const allowed=new Set(['worried','sad','calm','determined','excited','curious','whispers','whispering','shouting','laughs','laughing','crying','happy','angry','annoyed','sarcastic','thoughtful','surprised','sighs','frustrated sigh','short pause','long pause']);
 if(!Array.isArray(tags)||tags.some(t=>!allowed.has(t)))throw Error('Review unsupported audio tag for '+line.id);
 const settings={...config.voiceSettings,...cast.voiceSettings,...line.voiceSettings};
 if(modelId==='eleven_v3'&&settings.stability!==undefined&&![0,.5,1].includes(settings.stability))throw Error('Eleven v3 stability must be 0, 0.5 or 1');
 if(!config.outputFormat.startsWith('mp3_'))throw Error('This offline asset pipeline currently exports MP3 only.');
 const body={text:(tags.length?tags.map(t=>'['+t+']').join(' ')+' ':'')+normalizeText(line.text),model_id:modelId};
 if(modelId!=='eleven_v4'&&Object.keys(settings).length)body.voice_settings=settings;
 const input={provider:config.provider,voiceId:cast.voiceId,castId:cast.castId,outputFormat:config.outputFormat,body,normalization:config.normalization,emotion:line.emotion,delivery:line.delivery,context:line.emotionalContext,profile:cast};
 return{...input,hash:digest(input)};
}
export async function cachedRecording(line,request){
 const target=path.join(project,line.audioPath);
 try{const receipt=JSON.parse(await fs.readFile(target+'.json','utf8'));const audio=await fs.readFile(target);if(receipt.inputHash!==request.hash||receipt.audioHash!==crypto.createHash('sha256').update(audio).digest('hex')||audio.length<64)return null;return{target,audio,receipt};}catch{return null;}
}
export async function workload({scene,limit,force=false}={}){
 const {config,manifest}=await compileManifest();
 let lines=manifest.lines.filter(l=>!scene||l.id.startsWith(scene)||l.scene===scene);if(limit!==undefined)lines=lines.slice(0,limit);
 if(!lines.length)throw Error('No matching dialogue lines.');
 const items=[];for(const line of lines){const request=requestFor(line,config);const cached=!force&&await cachedRecording(line,request);items.push({line,request,cached});}
 const pending=items.filter(i=>!i.cached),characters=pending.reduce((n,i)=>n+i.request.body.text.length,0);
 const plan={provider:config.provider,totalLines:items.length,cachedLines:items.length-pending.length,pendingLines:pending.length,requestCharacters:characters,estimatedSpeechMinutes:Number((pending.reduce((n,i)=>n+normalizeText(i.line.text).split(/\s+/).length,0)/145).toFixed(2)),unconfiguredCharacters:[...new Set(pending.filter(i=>!i.request.voiceId).map(i=>i.line.character))],requests:pending.map(i=>({id:i.line.id,hash:i.request.hash,characters:i.request.body.text.length}))};
 return{config,manifest,items,plan,approvalHash:digest(plan)};
}
export async function generateItem(item,config,{fetchImpl=fetch,key=process.env.ELEVENLABS_API_KEY}={}){
 if(config.provider!=='elevenlabs')throw Error('No generator registered for provider '+config.provider);
 if(!key)throw Error('Set ELEVENLABS_API_KEY in the local process environment.');
 if(config.normalization.enabled){if(!process.env.VOICE_FFMPEG)throw Error('Set VOICE_FFMPEG before enabling normalization.');await fs.access(process.env.VOICE_FFMPEG);}
 const {line,request}=item;if(!request.voiceId||!/^[a-zA-Z0-9_-]+$/.test(request.voiceId))throw Error('Select a valid voiceId for '+line.character);
 const target=path.join(project,line.audioPath);await fs.mkdir(path.dirname(target),{recursive:true});
 const url='https://api.elevenlabs.io/v1/text-to-speech/'+encodeURIComponent(request.voiceId)+'?output_format='+encodeURIComponent(request.outputFormat);
 const response=await fetchImpl(url,{method:'POST',headers:{'xi-api-key':key,'Content-Type':'application/json'},body:JSON.stringify(request.body),signal:AbortSignal.timeout(120000)});
 if(!response.ok)throw Error(`ElevenLabs returned HTTP ${response.status} for ${line.id}. No automatic paid retry was made.`);
 let audio=Buffer.from(await response.arrayBuffer());if(audio.length<64||!response.headers.get('content-type')?.includes('audio'))throw Error('Provider did not return audio for '+line.id);
 const temp=target+'.pending';await fs.writeFile(temp,audio);
 try{if(config.normalization.enabled){if(!process.env.VOICE_FFMPEG)throw Error('Set VOICE_FFMPEG before enabling normalization.');const normalized=target+'.normalized.mp3';try{await promisify(execFile)(process.env.VOICE_FFMPEG,['-hide_banner','-loglevel','error','-y','-i',temp,'-af',`loudnorm=I=${config.normalization.integratedLUFS}:TP=${config.normalization.truePeakDB}:LRA=7`,'-c:a','libmp3lame','-b:a','128k',normalized],{windowsHide:true});audio=await fs.readFile(normalized);}finally{await fs.rm(normalized,{force:true});}}
  await fs.writeFile(temp,audio);await fs.rename(temp,target);
  await fs.writeFile(target+'.json',JSON.stringify({id:line.id,provider:config.provider,modelId:request.body.model_id,voiceId:request.voiceId,inputHash:request.hash,audioHash:crypto.createHash('sha256').update(audio).digest('hex'),generatedAt:new Date().toISOString(),normalized:config.normalization.enabled},null,2));
 }finally{await fs.rm(temp,{force:true});}
}
