// Chapter events pause gameplay while the same tile renderer remains alive.
function trimBounds(img){const c=document.createElement('canvas');c.width=img.width;c.height=img.height;const g=c.getContext('2d');g.drawImage(img,0,0);const a=g.getImageData(0,0,c.width,c.height).data;let l=c.width,t=c.height,r=0,b=0;for(let y=0;y<c.height;y++)for(let x=0;x<c.width;x++)if(a[(y*c.width+x)*4+3]>50){l=Math.min(l,x);r=Math.max(r,x);t=Math.min(t,y);b=Math.max(b,y)}return {x:l,y:t,w:r-l+1,h:b-t+1}}
const epiloguePanels=[
 {title:'Beyond the wormhole',text:'Beyond the veil, they found the Princess alive. But no voice could wake her. A violet mark shimmered above her heart.',quote:'“Princess… we’re here. Please, open your eyes.”',speaker:'explorer',tone:'worried'},
 {title:'Home, but not awakened',text:'The Architect carried her home through the returning dawn. The king waited at the palace gates.',quote:'“My child… you are safe now. Please wake up.”',speaker:'king',tone:'gentle'},
 {title:'The physician’s discovery',text:'The royal physician examined the Princess. An ancient curse held her between this world and the realm beyond the maze.',quote:'“This is no ordinary sleep. We must find the cure.”',speaker:'physician',tone:'grave'},
 {title:'The Great Alchemist',text:'Only the Great Alchemist knew the cure. To wake the Princess, the heroes would have to return to the dungeon.',quote:'“Then we go back. Together. Our promise still stands.”',speaker:'architect',tone:'resolute'}
];
function sceneMode(phase,speaker,line){stopStorySpeech();hideExplorerBubble();story.phase=phase;state.mode=phase;state.path=[];keys.clear();storyControls(true);$('stage').classList.add('cinematic');$('stage').style.setProperty('--hud-visibility','0');$('storyScreen').hidden=true;$('cinemaScreen').hidden=false;$('chapterCard').style.opacity='0';$('cinemaSpeaker').textContent=speaker;$('cinemaLine').textContent=line;story.lastCue='';}
function beginRuneAwakening(){
 if(state.mode!=='playing'||!state.runes.every(Boolean)||state.keyAwakened)return;
 sceneMode('ritual','The three seals','Their light rises. The bound key is awakening.');$('skipIntro').textContent='Continue →';
 cinematic={active:true,kind:'ritual',elapsed:0,uiFade:0,camera:{x:652,y:470,zoom:1,screenX:652},wallColor:()=>1,actors:()=>[],
  update(dt){if(document.hidden||voiceEngine.settingsOpen)return;this.elapsed+=voiceTimelineStep(this.elapsed,dt,'ritual');const s=this.elapsed;if(s>4.7&&!state.keyAwakened){state.keyAwakened=true;note(990,.5);cue('key','Explorer',runeCelebration,1)}if(s>=6.8)finishRuneAwakening()},
  effects(t){const s=this.elapsed,merge={x:690,y:280},target={x:KEY.x,y:KEY.y-13};
   if(s<3.5)RUNES.forEach((r,i)=>{const lift=smooth(s/1.3),p=smooth((s-1.3)/2.2),x=mix(r.x,merge.x,p),y=mix(r.y-32-lift*76,merge.y,p);glow(x,y,40,r.color,.5);ctx.save();ctx.translate(x,y);ctx.rotate(Math.sin(p*Math.PI)*.4);ctx.fillStyle=r.color;ctx.font='32px Georgia';ctx.textAlign='center';ctx.fillText(['☾','☼','✦'][i],0,10);ctx.restore();for(let j=0;j<8;j++)sparkle(x+Math.sin(t/340+j)*19,y+Math.cos(t/400+j)*19,t+j*100,r.color,.45)});
   if(s>=2.8&&s<5.3){const p=smooth((s-3.6)/1.1),x=mix(merge.x,target.x,p),y=mix(merge.y,target.y,p)-Math.sin(p*Math.PI)*42,alpha=Math.min(1,(s-2.8)*2)*(1-smooth((s-4.8)/.5));glow(x,y,85,'#e9d6ff',alpha*.65);glow(x,y,30,'#fff2bf',alpha);for(let i=0;i<16;i++){const a=i*Math.PI/8+t/700,r=16+Math.sin(t/200+i)*5;pixel(x+Math.cos(a)*r,y+Math.sin(a)*r,3,3,'#fff0bf')}}
   if(s>=4.6){const p=clamp01((s-4.6)/2.2);glow(target.x,target.y,110,'#ffdc65',.45*(1-p));ctx.save();ctx.globalAlpha=1-p;ctx.strokeStyle='#ffecaa';ctx.lineWidth=2;ctx.beginPath();ctx.arc(target.x,target.y,12+p*90,0,Math.PI*2);ctx.stroke();ctx.restore()}
  }
 };
}
function finishRuneAwakening(){stopStorySpeech();hideExplorerBubble();state.keyAwakened=true;if(cinematic)cinematic.active=false;story.phase='game';state.mode='playing';keys.clear();storyControls(false);$('cinemaScreen').hidden=true;$('stage').classList.remove('cinematic');$('stage').style.removeProperty('--hud-visibility');message('The Aether Key is golden. Claim it in the northern chamber.',true);updateUI();canvas.focus();}
function explorerSprite(x,cy,scale=1,alpha=1){const b=heroBounds;if(!b)return;ctx.save();ctx.globalAlpha=alpha;const h=51*scale,w=h*b.w/b.h;ctx.drawImage(images.hero,b.x,b.y,b.w,b.h,x-w/2,cy-h/2,w,h);ctx.restore()}
function followPoints(points,p){if(points.length<2)return points[0];const distances=[0];for(let i=1;i<points.length;i++)distances.push(distances[i-1]+Math.hypot(points[i].x-points[i-1].x,points[i].y-points[i-1].y));const d=clamp01(p)*distances.at(-1);for(let i=1;i<points.length;i++)if(d<=distances[i]){const q=(d-distances[i-1])/Math.max(.001,distances[i]-distances[i-1]);return {x:mix(points[i-1].x,points[i].x,q),y:mix(points[i-1].y,points[i].y,q)}}return points.at(-1)}
function beginFinale(){
 if(state.mode!=='playing'||!state.key)return;
 sceneMode('finale','At the threshold','The Explorer reaches the gate. The Architect’s work is done.');$('skipIntro').textContent='Skip to epilogue →';
 const origin={...state.visual},architect={x:EXIT.x-40,y:EXIT.y+43},front={x:EXIT.x-4,y:EXIT.y+34};
 const path=[origin,...route(state.player,{x:EXIT.x-4,y:EXIT.y+28},effectiveOpen(),true)];if(path.length===1)path.push(front);
 cinematic={active:true,kind:'finale',hideHero:true,elapsed:0,uiFade:0,camera:{x:652,y:470,zoom:1,screenX:652},
  wallColor(x,y){return 1-smooth((this.elapsed-2-Math.hypot(x-architect.x,y-architect.y)/310)/1.1)},
  update(dt){if(document.hidden)return;this.elapsed+=voiceTimelineStep(this.elapsed,dt,'finale');const s=this.elapsed,p=smooth(s/2.3);this.camera={x:mix(652,EXIT.x-12,p),y:mix(470,EXIT.y-12,p),zoom:mix(1,2.6,p),screenX:mix(652,836,p)};
   if(s<2.5)cue('end-gate','At the threshold','The Explorer reaches the gate. The Architect’s work is done.');else if(s<6.5)cue('return-form','Architect','“The stone releases me. We finish this together.”',.8);else if(s<10)cue('through','Beyond the veil','Together, they climb the steps into the wormhole.');else if(s<13)cue('crossing','The passage opens','A hidden chamber waits on the other side.');else if(s<16.5)cue('sleep','Explorer','“She’s here… but she won’t wake.”',1);else cue('curse','Architect','“This sleep is woven from magic.”',.8);
   if(s>=20)openEpilogue();
  },
  actors(t){const s=this.elapsed,result=[],walk=smooth((s-6.6)/2.3),enter=smooth((s-9)/2),vanish=1-smooth((enter-.6)/.4),scale=1-enter*.97,pos=followPoints(path,walk),heroY=mix(pos.y-25.5,EXIT.y-40,enter),heroX=mix(pos.x,EXIT.x-4,enter),archX=mix(mix(architect.x,EXIT.x-20,walk),EXIT.x-4,enter),archY=mix(mix(architect.y-27.5,EXIT.y+7,walk),EXIT.y-40,enter),material=smooth((s-3.3)/2.5);if(s<11.2){result.push({y:EXIT.y+24,draw:()=>explorerSprite(heroX,heroY,scale,vanish)});result.push({y:EXIT.y+25,draw:()=>castSprite(0,archX,archY+27.5*scale,55,material*vanish,scale,1+(1-material)*.8)})}return result},
  effects(t){const s=this.elapsed;if(s>2&&s<6.6){const p=smooth((s-2)/4.5);for(let i=0;i<150;i++){const w=walls[(i*37)%walls.length],q=smooth((p-(i%7)*.015)/.88),x=mix(OX+w.x*TILE+16,architect.x,q),y=mix(OY+w.y*TILE,architect.y-25,q)-Math.sin(q*Math.PI)*30;ctx.save();ctx.globalAlpha=Math.sin(q*Math.PI)*.9;pixel(x-1,y-3,2,6,'#d5a7ff');pixel(x-3,y-1,6,2,'#bd7dff');ctx.restore()}glow(architect.x,architect.y-28,65,'#bb7cff',Math.sin(p*Math.PI)*.6)}if(s>10.75&&s<11.3){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.globalAlpha=smooth((s-10.75)/.55);pixel(0,0,1672,941,'#030511');ctx.restore()}} ,
  renderOverride(t){if(this.elapsed<11.3)return false;const s=this.elapsed;ctx.save();pixel(0,0,1672,941,'#030511');if(s>=12){renderRescueChamber(t,s);ctx.globalAlpha=1-smooth((s-12)/.8);pixel(0,0,1672,941,'#030511')}ctx.restore();return true}
 };
}
function renderRescueChamber(t,s){
 const g=ctx.createRadialGradient(980,430,80,860,470,760);g.addColorStop(0,'#343059');g.addColorStop(1,'#070c1d');ctx.fillStyle=g;ctx.fillRect(0,0,1672,941);
 for(let row=0;row<8;row++)for(let col=0;col<18;col++){const x=190+col*72,y=405+row*48;const b=art.sprites[0];ctx.drawImage(images.atlas,b.x+(col%2)*b.w/2,b.y+(row%2)*b.h/2,b.w/2,b.h/2,x,y,70,46);pixel(x+3,y+2,64,2,'#38425b33')}
 for(let row=0;row<5;row++)for(let col=0;col<18;col++){const x=188+col*72+(row%2)*-36,y=170+row*47;const b=art.sprites[1];ctx.drawImage(images.atlas,b.x+b.w*.05,b.y+b.h*.56,b.w*.26,b.h*.35,x,y,70,44);pixel(x+3,y+2,64,3,'#62516b')}
 for(const x of [270,1400]){sprite(8,x,510,90,220);torch({x:x+65,y:380,phase:x},t)}
 // The sleeping Princess rests across a raised bed beneath the curse sigil.
 const bed=story.bedBounds;if(bed){const w=405,h=w*bed.h/bed.w;ctx.drawImage(images.bed,bed.x,bed.y,bed.w,bed.h,859,620-h,w,h);glow(1110,470,60,'#b89aff',.09+.025*Math.sin(t/750))}
 const walk=smooth((s-12)/2.9);explorerSprite(mix(560,820,walk),620,2.2);castSprite(0,mix(430,730,walk),619,124);
 const cy=365+Math.sin(t/500)*6;glow(1050,cy,80,'#a569ff',.4);ctx.save();ctx.translate(1050,cy);ctx.rotate(t/1800);ctx.strokeStyle='#c79aff';ctx.lineWidth=3;ctx.strokeRect(-25,-25,50,50);ctx.rotate(Math.PI/4);ctx.strokeRect(-25,-25,50,50);ctx.restore();sparkle(1050,cy,t,'#f0d5ff',1.3);
}
async function openEpilogue(){
 if(state.mode==='lost')return;
 stopStorySpeech();
 if(story.phase==='epilogueLoading'||story.chapter==='epilogue'&&story.phase==='comic')return;
 if(cinematic)cinematic.active=false;story.phase='epilogueLoading';story.chapter='epilogue';$('skipStory').textContent='Chapter II';state.mode='epilogue';storyControls(true);$('cinemaScreen').hidden=true;$('storyScreen').hidden=false;$('storyLoading').hidden=false;$('storyLoading').textContent='Beyond the veil…';
 try{images.epilogue??=await loadImage(ASSETS.epilogue);if(story.phase!=='epilogueLoading')return;$('storyLoading').hidden=true;showComic(0);$('storyFade').hidden=false;$('storyFade').style.opacity='1';story.fade={elapsed:reduced?.12:.35,switched:true,action(){}};}catch(err){$('storyLoading').textContent='The epilogue could not load. Select Chapter II to continue.';console.error(err)}
}
function showComingSoon(){if(state.mode==='lost')return;if(cinematic)cinematic.active=false;story.phase='comingSoon';state.mode='complete';$('storyScreen').hidden=true;$('cinemaScreen').hidden=true;$('comingSoon').hidden=false;storyControls(true);stopStorySpeech();$('beginChapter2').focus();}
function skipStoryScene(){if(story.phase==='comingSoon')return;if(story.phase==='ritual'){finishRuneAwakening();return}if(story.phase==='finale'){openEpilogue();return}if(story.chapter==='epilogue'){transitionStory(showComingSoon);return}finishStory()}
$('skipStory').onclick=skipStoryScene;$('skipIntro').onclick=skipStoryScene;
$('replayChapter').onclick=()=>{story.chapter='prologue';$('comingSoon').hidden=true;replay.onclick()};
window.questDiagnostics=()=>({keyAwakened:state.keyAwakened,chapter:story.chapter??'prologue',phase:story.phase,scene:cinematic?.kind,elapsed:cinematic?.elapsed??0,star:{...RUNES[2]},remaining:state.remaining});
