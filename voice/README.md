# Expressive prerecorded voices

The game still owns all story text, art, chapters and movement. This adds a build-time ElevenLabs generation pipeline and a laptop-side playback layer. It does not generate speech during gameplay or put credentials in the HTML.

## Current state

The manifest covers **50 existing dialogue lines**, seven characters and all three playable chapters, including comics, introductions, rune awakening, flights, brewing, capture and spoken bad endings. Original dialogue is preserved, including punctuation; only outer display quotation marks are removed from provider input. Descriptions are not sent to speech generation.

One take per line is **3,326 provider-input characters** including delivery tags, approximately **3.7 minutes** at 145 words/minute. This is a workload estimate, not a credit or dollar quote. Model pricing and plan eligibility determine actual usage. The initial six-panel Chapter I prologue is **six requests / 332 input characters**.

**No ElevenLabs recordings have been generated.** Provider voice IDs must be selected and the local API key configured. Until recordings exist, the optional browser fallback or captions keep the game playable. The browser tests used a clearly labeled synthetic tone to exercise a real offline audio element, then mock media elements to test lifecycle failures; those fixtures are not shipped as character voices.

The user has approved only the six-line prologue sample after configuration. That authorization is recorded in `task-notes/VOICE_GENERATION_APPROVAL.md`; it does not authorize generating the remaining 44 lines.

## Files

- `voice-config.json`: one logical `castId` per character, provider `voiceId`, personality, register, accent guidance, typical emotions, changing scene delivery and model settings.
- `dialogue-manifest.json`: generated inventory of exact text, stable IDs, chapter, scene, speaker, emotional context, delivery and asset paths.
- `dialogue-overrides.json`: manual per-line performance changes; does not permit replacing story text or speakers.
- `pipeline.mjs`: source extraction, provider request preparation, content hashes, cache verification, local audio output and optional loudness normalization.
- `generate-voices.mjs`: dry-run / reviewed-generation CLI with progress and failure reporting.
- `audio/<chapter>/<character>/<dialogue-id>.mp3`: generated recordings, each with a hash receipt beside it.
- `maze-source/work/story/voice.js`: offline playback, browser fallback, cancellation, replay, mute, captions, progression controls and a music ducking hook.

## Start with the first scene

1. Audition and choose the voices in your own ElevenLabs account. Put a provider voice ID into each needed character's `voiceId` in `voice-config.json`. The first prologue needs Explorer, Princess, King and Architect. Stable cast IDs already exist; the provider IDs are intentionally blank rather than invented.
2. Set `ELEVENLABS_API_KEY` in the environment of the local terminal that will run the generator. Use your local environment editor or secret manager. Do not paste a key into chat, frontend JavaScript, the JSON configuration, a shell command that will be shared, or Git. `.env` files are ignored, but this dependency-free generator does not automatically load them.

   If you prefer a local ignored `.env` file, a current Node runtime can load it explicitly: `node --env-file=.env voice/generate-voices.mjs --scene ch1-prologue`. The key then enters the script through `process.env`; no key belongs in the HTML.
3. Review the actual workload:

```powershell
node voice/generate-voices.mjs --scene ch1-prologue
```

4. Only after approving that exact plan, run:

```powershell
node voice/generate-voices.mjs --scene ch1-prologue --generate --approve-plan THE_HASH_PRINTED_BY_THE_DRY_RUN
```

The placeholder is the dry-run's complete `approvalHash`, not the text shown above. Changing a voice, model, delivery, output format, normalization setting or text changes the plan. The CLI requires a matching reviewed hash before it sends requests. No automatic retries are made after provider errors, because a retry may consume additional credits. Keep successful files and rerun the dry-run to see only the missing work.

5. Rebuild and copy the standalone game:

```powershell
node maze-source/work/build-rendered.mjs
node maze-source/work/build-story.mjs
Copy-Item maze-source/outputs/Dual_Reality_Maze_Story_Edition.html Dual_Reality_Maze_Story_Edition.html
```

The Story builder embeds only audio with a matching configuration hash and intact receipt. The resulting HTML plays those recordings offline without a server or ElevenLabs account. Missing or stale files do not enter the build.

6. Listen to the complete first scene before expanding. Check casting, names, pauses, emotional restraint, captions and skips. Generate another scene with `--scene ch2-comic` or review the entire batch by omitting `--scene`. Full generation still requires approval of its exact plan. `--limit 1` auditions one line; `--force` includes existing recordings in the regeneration plan.

## Emotion and consistency

Performance comes from the authored scene context, not keyword sentiment. Each comic line carries the panel's actual story situation. Cinematic lines have explicit rescue, transformation, discovery, return, capture or defeat contexts. Voices are shared across chapters.

Change a line by ID in `dialogue-overrides.json`, for example:

```json
{
  "ch1-cue-oath": {
    "emotion": "quiet determination",
    "tags": ["determined"],
    "delivery": "A promise made directly to Rowan; restrained and sincere."
  }
}
```

The human-readable delivery/context fields are audition guidance and cache inputs. The expressive model receives the selected supported audio tags and original dialogue; it does not receive the prose direction as spoken text. Regeneration changes the cache key even when you adjust a performance direction for a new audition. Listen to every important take: audio tags are suggestions, not a guarantee of emotional quality.

The default is `eleven_v3`, stability `0.5`, MP3 44.1 kHz / 128 kbps. Audio tags are emitted only for the explicitly supported v3/v4 model IDs. Other model IDs receive plain text. Eleven v3 stability is constrained to 0, 0.5 or 1; v4 does not receive the older voice-settings payload. Check model availability, current product status and your account's terms before release. No accent is invented where the story specifies none.

Optional emotions such as anger, humor, shouting or whispering should be manually assigned only when justified by the actual scene. This story currently calls mainly for urgency, concern, wonder, determination, gentleness, relief and sorrow; it should not acquire inappropriate sarcasm or constant shouting simply to demonstrate a feature.

## Playback and settings

The existing `say`, panel and speech-wait entry points now prefer a line's embedded recording. Every mapped cue uses a stable ID. Playback uses one active voice, waits for `ended`, cancels stale callbacks on Skip/Previous/restart, and has a deadline if media stalls. Failed or unavailable recordings use the selected browser fallback or release to captions. Playback pauses with a hidden tab or controller menu. Upcoming queued recordings are preloaded.

Voice settings provide master volume, mute, pace, dialogue subtitles, automatic comic progression, replay and a browser/captions-only fallback. Cast selectors affect browser fallback only; provider voices are chosen in the build-time configuration. Captions remain enabled by default. Playback and preferences are session-local; this task does not introduce a save system.

No existing music or sound effects are removed. There is currently no background music element in the game source to wire automatically. A future music element can be registered without changing effects:

```js
mazeVoice.registerMusic(backgroundMusicElement);
// Its volume smoothly ducks to 25% while dialogue plays, then restores.
mazeVoice.unregisterMusic(backgroundMusicElement);
```

Natural recording endings, gradual music duck/restore and prompt cancellation handle transitions. Explicit skips immediately mute and stop the previous recording so another line cannot overlap it. This is not a phoneme/viseme or lip-sync implementation; existing character and spell animations are preserved.

For consistent mastered loudness, enable `normalization.enabled` and set `VOICE_FFMPEG` to your local FFmpeg executable. The pipeline applies a target of -18 LUFS and -2 dB true peak. Missing normalization tooling is detected before an API request. Normalization is optional so the student project does not acquire a mandatory media dependency.

## Provider setup and licensing references

- [ElevenLabs create-speech API](https://elevenlabs.io/docs/api-reference/text-to-speech/convert)
- [Audio tags in expressive models](https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-do-audio-tags-work-with-eleven-v3-and-v4)
- [Publishing and commercial-use rules](https://help.elevenlabs.io/hc/en-us/articles/13313564601361-Can-I-publish-the-content-I-generate-on-the-platform)

The free plan excludes commercial use and requires attribution when publishing noncommercial output. Verify the current terms and the chosen model's eligibility for your planned use. Existing accounts and subscriptions were not inspected.

To add another provider later, keep the manifest/playback contract and add a generation adapter alongside `requestFor` / `generateItem`. The game receives only validated local audio; it does not know provider credentials or call provider endpoints.

## Validation

```powershell
node voice/test-pipeline.mjs
node maze-source/work/test-rendered.mjs
node maze-source/work/test-story.mjs
node maze-source/work/test-chapter2.mjs
node maze-source/work/test-chapter3.mjs
node task-notes/test-voice-controllers-browser.mjs
```

The browser test uses the locally installed Chrome and bundled Playwright runtime. It checks offline audio playback with a tone fixture, all dialogue IDs, lifecycle recovery, music ducking, settings, controller navigation and supplied serial-message formats. Physical boards, paid generation, artistic voice quality and real-world wiring require separate testing.

The controller pin review and mappings are in `hardware/CONTROLS_AND_CIRCUITS.md`.
