// No API requests without both --generate and a matching reviewed --approve-plan hash.
import {workload,generateItem} from './pipeline.mjs';
const args=process.argv.slice(2),value=k=>{const i=args.indexOf(k);return i<0?undefined:args[i+1];};
const permitted=new Set(['--scene','--limit','--force','--generate','--approve-plan']);
for(let i=0;i<args.length;i++){if(!permitted.has(args[i]))throw Error('Unknown option '+args[i]);if(['--scene','--limit','--approve-plan'].includes(args[i])){if(!args[i+1]||args[i+1].startsWith('--'))throw Error('Missing option value');i++;}}
const limit=value('--limit')===undefined?undefined:Number(value('--limit'));if(limit!==undefined&&(!Number.isInteger(limit)||limit<1))throw Error('--limit must be a positive integer.');
const result=await workload({scene:value('--scene'),limit,force:args.includes('--force')});
console.log(JSON.stringify({...result.plan,approvalHash:result.approvalHash,notice:'Character workload is not a credit or dollar quote. Check the chosen model and account rate. No live API calls have been made.'},null,2));
if(args.includes('--generate')){
 if(value('--approve-plan')!==result.approvalHash)throw Error('Generation blocked: review this exact workload, then supply its --approve-plan hash.');
 if(result.plan.unconfiguredCharacters.length)throw Error('Choose voice IDs for: '+result.plan.unconfiguredCharacters.join(', '));
 let completed=0;for(const item of result.items){if(item.cached){console.log('CACHED '+item.line.id);continue;}await generateItem(item,result.config);console.log(`GENERATED ${++completed}/${result.plan.pendingLines}: ${item.line.id}`);}
 console.log('Generation complete. Rebuild the Story Edition to embed verified audio for offline play.');
}
