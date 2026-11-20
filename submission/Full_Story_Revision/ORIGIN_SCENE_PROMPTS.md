# Origin scene prompts

Use the game's own `comic.png`, `story-cast.png`, `explorer.png`, `architect-waiting-v4.png` and `title-screen.png` as identity and style references. Save the output as one 16:9 landscape frame, not a collage. Preserve detailed pixel art, chibi proportions, purple-blue royal colours, gold trim, recognizable faces and costumes. No captions, interface, title or watermark in the scene images. The built-in image tool generated the origin artwork; PixVerse animates those saved references.

## Reusable image prompts

**Peaceful kingdom:** Before the attack, the elderly white-bearded King in gold crown and purple-gold fur-trimmed robes smiles beside his golden-brown-haired daughter in her white/lavender gown and violet-gem tiara. They overlook the safe castle town from a rose-framed balcony at sunset. Blue-and-gold banners, fountain, warm lights and quiet streets. No enemies, flames or threat.

**Architect alone:** The same brown-haired, brown-bearded royal Architect in purple-blue gold-trimmed robes and turquoise clasp works in his lantern-lit workshop. He constructs a miniature bridge from floating violet stone blocks above a parchment maze plan. Drafting compass, scrolls, brass instruments and a quiet castle view. His work is route design and architectural magic, not combat. No Explorer or Princess.

**Explorer alone:** Rowan, matching his white headband, cream shirt, backpack, brown straps and boots, studies a map by lantern light in ancient forest ruins far from the kingdom. Mossy arches, stone stairs, narrow bridge, ferns, waterfalls and sunbeams. He is thoughtfully choosing his route. No Architect or Princess.

**Attack:** The same castle town at night under attack by the pale host: hooded purple ghosts with glowing cyan eyes sweep over gates and roofs, violet lightning surrounds a distant floating fortress, distant roofs burn, guards help townspeople flee. Urgent, cinematic and readable, without gore or visible injury.

**Kidnapping:** On the royal balcony, spectral captors carry the recognizable Princess toward the remote floating maze along a violet magical trail. Her hair and white/lavender gown move in the wind and she reaches back toward home. Keep the gold tiara and violet jewel. Storybook peril, no injury, no new villains or unrelated style.

**Corrected summons:** See `ORIGIN_REVISION_AND_SOUND.md` for the exact final image prompt. The father must look frightened and desperate, with an open pleading hand and tense posture; the heroes must look empathetic and resolved. The earlier casual performance is rejected.

## Video settings and motion

For the first five scenes: PixVerse V6, 720p, 5 seconds, one output, Multi-Shot OFF. Preserve the uploaded reference. Use restrained continuous camera motion, stable faces and costumes, subtle hair/cloth motion and no cuts or morphing. For the peaceful scene: fountain, evening birds and breeze. Architect: slowly assemble the miniature bridge, stone clicks, parchment and magical chimes. Explorer: study map, one cautious step, swaying lantern, water and leaves. Attack: drifting ghosts, lightning, smoke/fire, alarm bell and thunder. Kidnapping: drift toward the distant maze along the magical trail, spectral wind and portal rumble. Request no music or generated speech; final editorial audio choices are independent of the provider's output.

For the corrected summons: **10 seconds, Audio OFF, 720p, one output**. Exact motion prompt is saved in `../../trailer-kit/origin-v4/corrected-video-prompt.txt`. Its original audio is excluded by the edit even if a later source is substituted. Use the separately recorded English King dialogue, with room around the line and low music underneath. Export each source using **Download → Watermark-free**.

## Narration and title

All exact voice scripts and settings are in `ORIGIN_REVISION_AND_SOUND.md`. Title lettering is typeset and animated in the editable `origin-title.mjs` file, preserving the actual game name. Keep the route drawing, light travel, opposite-side text entrance, magic-seam artwork reveal, assembled subtitle and star glints synchronized to the voice and score. Avoid asking a video generator to draw the final title text.
