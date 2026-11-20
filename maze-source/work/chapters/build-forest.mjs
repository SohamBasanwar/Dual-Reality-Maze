// Keep each chapter's title hierarchy and proportions anchored to the same template.
export function makeForestMarkup(template,assets,source){
 const base=template.slice(template.indexOf('<section'));
 function card({id,chapter,name,promise,summary,art,alt,actionId,action,returnId,returnText,footer,disabled=false}){
  return base.replace('id="comingSoon"',`id="${id}"`).replace('Chapter II — The Alchemist’s Cure',chapter+' — '+name.replace(/<[^>]*>/g,' '))
   .replace('__SEQUEL_ART__',()=>assets[art]).replace('The sleeping Princess appears in a magical vision above Rowan, the Architect and the Great Alchemist.',alt)
   .replace('Chapter II · A new journey',chapter+' · '+(disabled?'The next journey':'Roots and remembrance'))
   .replace('The Alchemist’s<span>Cure</span>',name).replace('She is home. But she has not awakened.',promise)
   .replace(/<p class="sequel-summary">[\s\S]*?<\/p>/,()=>'<p class="sequel-summary">'+summary+'</p>')
   .replace('id="beginChapter2"',`id="${actionId}"${disabled?' disabled':''}`).replace('Begin Chapter II',action)
   .replace('id="replayChapter"',`id="${returnId}"`).replace('↶ Replay Chapter I',returnText)
   .replace('A SLEEPING PRINCESS · A FORGOTTEN CURE',footer);
 }
 const forestTitle=card({id:'forestTitle',chapter:'Chapter III',name:'The Forest of<span>Lost Memories</span>',promise:'She has awakened. The forest remembers what she cannot.',summary:'Meet the Dryad, earn her trust, and follow a playful memory through the rainforest.<br>A gifted jar. A wandering leaf. Ten minutes to bring her past home.',art:'forestTitle',alt:'Rowan and the Architect meet the Dryad beneath the Heart Tree as the Princess’s childhood memory rides a golden leaf.',actionId:'forestBegin',action:'Begin Chapter III',returnId:'forestTitleReturn',returnText:'Title screen',footer:'A LIVING FOREST · A CHILDHOOD LOST'});
 const clockTitle=card({id:'forestNextTitle',chapter:'Chapter IV',name:'The Clockwork<span>Citadel</span>',promise:'Her memories are home. The source of the curse remains.',summary:'A remembered bell leads Rowan and the Architect to a fortress of turning gears.<br>Beyond its clockwork gates, the shadows are still counting down.',art:'clockTitle',alt:'Rowan and the Architect face an immense brass clock tower and its ancient bell.',actionId:'forestComingSoon',action:'Coming soon',returnId:'forestPreviewReplay',returnText:'↶ Replay Chapter III',footer:'A BRASS BELL · THE SHADOW’S SOURCE',disabled:true}).replace('</button><p><strong>','</button><button id="forestPreviewReturn" class="sequel-replay">Title screen</button><p><strong>');
 const laboratoryTitle=forestTitle.replace('id="forestTitle"','id="labChapterTitle"').replace('id="forestBegin"','id="labChapterSoon"').replace('id="forestTitleReturn"','id="labChapterReplay"').replace('>Title screen</button>','>↶ Replay Chapter II</button><button id="labChapterReturn" class="sequel-replay">Title screen</button>');
 return {markup:source.replace('__FOREST_TITLE__',()=>forestTitle).replace('__CLOCK_TITLE__',()=>clockTitle),laboratoryTitle};
}
