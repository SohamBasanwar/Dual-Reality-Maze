# Dual-Reality Maze — trailer and voice kit

Prepared October 22, 2026. Prices and free-plan details were checked against the official pages linked below.

The presentation-ready version is now in `../submission/Dual_Reality_Maze_Trailer.mp4`, with the King's opening line exported from Clipchamp and mixed over the score. The completed editable deck embeds this file on slide 3. This folder retains the earlier silent snippets, stills and visual draft for revision. No paid voice or video generation was performed.

## My recommendation

Use **Clipchamp to assemble the trailer**, **Azure Speech F0 to produce the game's fixed dialogue**, and audition **ElevenLabs for the most emotional scenes** if its publishing terms fit your project. The creative preference for ElevenLabs is a recommendation to audition it, not a measured quality ranking. Compare the same three lines before choosing a cast.

The biggest improvement is to **generate each line once, choose a good performance, then ship the audio with the game**. The updated game supports embedded recordings with browser `speechSynthesis` as a fallback. No actor recordings are configured yet. Browser voice quality changes with the computer's installed voices. Fixed audio gives everyone the same performance and lets animation follow the actual recording.

## Your files

- `Dual_Reality_Maze_Trailer_Draft.mp4`: approximately 33.5 seconds, 1920 × 1080, 24 fps, trailer captions and an original synthesized temporary music bed. No voiceover has been generated.
- `clips/`: eight separate MP4 snippets. They are silent so you can add speech and sound effects cleanly.
- `stills/`: one full-size PNG per snippet, suitable for a thumbnail or image-to-video input.
- `Trailer_Contact_Sheet.jpg`: visual overview of the eight shots.
- `VOICE_AND_VIDEO_PROMPTS.md`: copyable voice directions, dialogue and image-to-video prompts.
- `voice-audition.csv`: actual game lines for comparing voices.
- `architect-azure.ssml`: example Azure input with pauses and restrained pacing.
- `shot-manifest.json`: exact timings, source scenes and file names.
- `build-trailer.mjs`: reproducible export script. Requires the bundled Node canvas runtime and FFmpeg. Set `MAZE_FFMPEG` to an FFmpeg executable if it is not in the temporary location used during this export.

These are staged shots exported from the game's existing canvas renderers, rather than a screen recording of a player completing a level. The title end card animates the existing title artwork with an editorial zoom and typography. The game source and existing artwork were not changed. Native renderer animation is retained; this is not an AI-generated reconstruction of gameplay.

## Free tools that fit this project

| Tool | Use it for | Actual free-plan limit |
|---|---|---|
| [Clipchamp](https://clipchamp.com/en/pricing/) | Easiest browser/Windows trailer editor: import these MP4s, animated titles, transitions, voiceovers | Up to 1080p, no watermark. Use your own media and free stock; premium stock and 4K require a paid plan. A personal Microsoft account is needed. |
| [Clipchamp AI voiceover](https://clipchamp.com/en/features/ai-voice-over-generator/) | Quick trailer voice test without setting up an API | Text-to-speech is free in the editor. It does not expose the same controls or workflow as a full Azure Speech project. |
| [Azure Speech](https://azure.microsoft.com/en-us/pricing/details/speech/) | Larger fixed game-dialogue library | F0 lists 500,000 neural TTS characters per month. Requires an Azure account and an eligible Speech resource. Select F0 and check that the voice/features you use are eligible; do not assume every premium/HD feature shares that allowance. |
| [ElevenLabs](https://elevenlabs.io/pricing) | Audition expressive character performances | Free plan lists 10,000 credits per month. Credit use depends on model. Free audio has no commercial license; published noncommercial use requires attribution. |
| [Runway](https://help.runwayml.com/hc/en-us/articles/50404627334547-Free-plan-details) | Optional image-to-video tests with the supplied stills | 125 one-time credits, not a monthly allowance. Free video has a watermark. The models available to free accounts change; confirm image-to-video is available in your account before spending time on it. |

For a completely free trailer without a generator watermark, use the supplied native clips and Clipchamp. You already have real animation; you do not need an AI video subscription to get moving shots.

Pika was not selected as the free generation recommendation: its current [pricing page](https://pika.art/pricing) lists zero monthly credits on Free, with credit packs instead. A free account label does not guarantee free video generations.

ElevenLabs' exact publication restriction is here: [Can I publish generated content?](https://help.elevenlabs.io/hc/en-us/articles/13313564601361-Can-I-publish-the-content-I-generate-on-the-platform). Use its free tier for a noncommercial class prototype with the required attribution; use appropriately licensed audio for a commercial game or promotion. An upgrade does not retroactively license earlier free generations under the stated policy.

## Assemble or revise the trailer in Clipchamp

1. Open [Clipchamp](https://app.clipchamp.com/) and create a 16:9 project.
2. Import the eight files from `clips/`, or import the assembled draft if you only want to add voiceover.
3. Arrange the separate clips in filename order. The draft demonstrates this sequence. Use straight cuts or short 0.2-second fades; avoid a different transition on every cut.
4. Keep the strongest gameplay visible. The first shot shows the actual maze and Architect controls. The later scenes sell the world and story.
5. Add one short line of animated text at a time. Suggested lines are in the prompt file. Keep text inside a 5% margin and out of the character faces.
6. Add character voices with Text to speech, or import separately generated WAV/MP3 files. Do not paste direction notes into a basic text-to-speech box: it may speak them aloud.
7. Import `temporary-score.wav`, or choose a free music item. Start the music about 12–18 dB below dialogue, then adjust by ear. Use a brief wing sound, portal shimmer and forest ambience only where they help a visible action.
8. Export at 1080p. Check the final file with headphones and laptop speakers.

Clipchamp is principally an editor. Its auto-compose feature uses your imported media and style choices; do not expect the image-to-video prompts below to work as a single text command inside Clipchamp.

## Make voices feel like characters

- Give each role its own consistent voice. Rowan should sound curious and quick; the Architect calm and thoughtful; the King worried but controlled; the Dryad warm and firm.
- Generate one short conversational turn at a time. Audition two or three takes of an important line. Choose intention and clear delivery over a dramatic announcer voice.
- Put the emotion in the delivery and the words. A distressed line needs a small pause or breath, not an extreme pitch change applied to the whole character.
- Keep natural gaps between speakers. Short reaction sounds and a quiet moment after a serious line can do more than constant talking.
- Use restrained gestures while speaking: blink, mouth movement, a small head turn and one meaningful hand gesture. Reserve large magical poses for spells.
- For this pixel-art game, use 2–3 mouth poses, about 6–10 pose changes per second during speech, and hold the closed mouth during silence. An audio amplitude envelope can drive simple open/closed motion; phoneme/viseme timing can improve it later. Do not make the whole face warp with every syllable.

For integration later: add a stable line ID and audio file to each existing dialogue cue; preload upcoming lines; wait for the audio `ended` event before the cinematic advances; stop audio on Skip/Previous/restart; pause with the existing hidden-tab and voice-settings handling; retain captions and a bounded timeout for missing files. Keep generation credentials out of the downloadable HTML. The game already has dialogue-wait and fallback behavior that should be preserved.

The trailers and planning assets are delivered now. This task did not replace in-game speech or alter the game's animation system.

## Optional AI animation workflow

1. Start with one supplied still, not a text-only recreation of the scene.
2. Use an image-to-video tool/model that your free account actually permits.
3. Choose 16:9, 4–5 seconds, gentle movement and a locked camera or small push-in.
4. Paste the corresponding motion prompt from `VOICE_AND_VIDEO_PROMPTS.md`.
5. Reject outputs that change character identity, redraw the maze layout, bend the dragon incorrectly or invent interface text.
6. Treat accepted outputs as cinematic interpretations. Keep real gameplay clips in the trailer so the game is represented accurately.

For reusable assets, generate visuals without text and add titles in the editor. This avoids unstable letters and lets you change the title without regenerating the shot.

## Technical provenance and verification

Source: the project's editable `maze-source/work` scripts and existing `images` assets. All seven scene clips use the game's unmodified render functions at selected states/timestamps. Frames are exported at 1080p from the native 1672 × 941 view; the extra output resolution does not add source detail. The end card uses the existing title illustration. A midpoint frame is checked against the first frame to verify each snippet contains changing pixels. Every MP4 is decoded with FFmpeg after export. This establishes decodability and changing frames, not a complete browser playthrough test.

The accompanying music is a simple original synthesized temporary score, not the game's recorded soundtrack or an AI voice. The draft is ready for a voiceover/editing pass.
