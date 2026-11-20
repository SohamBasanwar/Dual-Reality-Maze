// Pure JavaScript unit check of local gallery handlers; no browser automation.
const fs=require('fs'),path=require('path'),vm=require('vm');
const root=__dirname,html=fs.readFileSync(path.join(root,'index.html'),'utf8');
const ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]);
if(new Set(ids).size!==ids.length)throw new Error('Duplicate gallery ID');
const elements=Object.fromEntries(ids.map(id=>[id,{id,src:'',href:'',textContent:'',classList:{remove(){},add(){}}}]));
const buttons=[{classList:{remove(){},add(){}}},{classList:{remove(){},add(){}}}];
const button={classList:{remove(){},add(){}},parentElement:{querySelectorAll:()=>buttons}};
const context=vm.createContext({document:{getElementById(id){if(!elements[id])throw new Error('Unknown ID: '+id);return elements[id]}},button});
const scripts=[...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
for(const s of scripts)vm.runInContext(s[1],context);
let count=0;
for(const call of html.matchAll(/onclick="([^"]+)"/g)){
    vm.runInContext(call[1].replace(/\bthis\b/g,'button'),context);count++;
    for(const e of Object.values(elements))for(const field of ['src','href'])if(e[field]&&!fs.existsSync(path.join(root,e[field])))throw new Error('Missing '+e[field]);
}
const report={handler_calls_checked:count,unique_element_ids:ids.length,all_handler_image_paths_exist:true,live_browser_render_verified:false,live_browser_limitation:'In-app browser URL policy rejected the file:// protocol.'};
fs.writeFileSync(path.join(root,'GUIDE_CHECK.json'),JSON.stringify(report,null,2));console.log(report);
