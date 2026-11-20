const splash={loaded:0,total:8,artReady:false,failed:false};
function reportTitleLoad(){splash.loaded=Math.min(splash.total,splash.loaded+1);syncTitleScreen()}
function syncTitleScreen(){
 const ready=story.ready&&splash.artReady&&!splash.failed,percent=Math.round(splash.loaded/splash.total*100);
 $('titleProgressFill').style.width=percent+'%';$('titlePercent').textContent=percent+'%';$('titleProgress').setAttribute('aria-valuenow',String(percent));
 $('titleBegin').disabled=!ready;$('titleQuickPlay').disabled=!ready;
 if(splash.failed)return;
 $('titleBegin').textContent=ready?'Begin adventure':'Awakening…';$('titleStatus').textContent=ready?'Your adventure awaits':percent<40?'Shaping the labyrinth…':percent<80?'Gathering the kingdom’s stories…':'Lighting the way…';
}
function failTitleScreen(){splash.failed=true;$('titleStatus').textContent='Artwork could not load. Reopen the complete game file.';syncTitleScreen()}
function startTitleAdventure(skip=false){if(!story.ready||!splash.artReady||story.phase!=='title'||story.fade)return;transitionStory(()=>{$('titleScreen').hidden=true;document.querySelector('.app').classList.remove('title-open');if(skip)finishStory();else{story.chapter='prologue';showComic(0)}})}
function updateComicCountdown(now){
 const dt=Math.max(0,(now-(story.autoLast??now))/1000);story.autoLast=now;
 if(story.phase!=='comic'||story.fade||document.hidden||story.autoPlay===false||voiceEngine.settingsOpen||controllerModalOpen())return;
 story.panelRemaining=Math.max(0,(story.panelRemaining??10)-dt);paintComicCountdown();
 if(story.panelRemaining<=0&&!storySpeechActive())nextComic();
}
function paintComicCountdown(){const remaining=story.panelRemaining??10,seconds=Math.ceil(remaining);$('storyCountdown').textContent=story.autoPlay===false?'Auto-play paused':remaining<=0&&storySpeechActive()?'Finishing dialogue…':`Next in ${seconds}s`;$('storyCountdownFill').style.width=(remaining*10)+'%';$('storyAuto').textContent=story.autoPlay===false?'Auto-play off':'Auto-play on';$('storyAuto').setAttribute('aria-pressed',String(story.autoPlay!==false))}
$('storyAuto').onclick=()=>{story.autoPlay=story.autoPlay===false;story.autoLast=performance.now();paintComicCountdown()};
document.addEventListener('visibilitychange',()=>{story.autoLast=performance.now()});
$('titleBegin').onclick=()=>startTitleAdventure();$('titleQuickPlay').onclick=()=>startTitleAdventure(true);
$('titleMotes').innerHTML=Array.from({length:20},(_,i)=>`<i style="--x:${13+(i*37)%82}%;--duration:${7+i%6}s;--delay:${-i*.73}s"></i>`).join('');
loadImage(ASSETS.title).then(img=>{$('titleArt').src=img.src;splash.artReady=true;syncTitleScreen()}).catch(err=>{console.error(err);failTitleScreen()});
