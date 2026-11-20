# Copyable prompts for this game

## Trailer sequence

| Approximate time | File | On-screen text |
|---|---|---|
| 0–5 s | 01_maze_and_architect | TWO HEROES. ONE PATH. |
| 5–9.8 s | 02_architect_transformation | BECOME THE WAY FORWARD. |
| 9.8–12.4 s | 03_emerald_guardian | AWAKEN AN ANCIENT ALLY. |
| 12.4–17.4 s | 04_dragon_flight | RISE ABOVE THE SHATTERED GARDENS. |
| 17.4–20.9 s | 05_heart_tree_and_dryad | ENTER A FOREST THAT REMEMBERS. |
| 20.9–24.5 s | 06_memory_in_the_jar | BRING HER MEMORIES HOME. |
| 24.5–29.5 s | 07_home_on_emerald_wings | A PROMISE CARRIED HOME. |
| 29.5–33.5 s | 08_title_end_card | DUAL-REALITY MAZE / THE ARCHITECT'S OATH |

Exact frame-rounded timings are in `shot-manifest.json`. This short draft intentionally avoids spoiling the Princess's final reunion.

## Voice directions

Use these in a voice-design or performance-direction field if the tool has one. In a plain text-to-speech field, paste only the spoken line. Use an original library voice rather than an imitation of a named actor.

**Architect**
> Adult male fantasy scholar with a warm, grounded lower register. Quiet confidence, thoughtful pauses and an understated sense of wonder. Speak to the friend beside you. Natural conversational rhythm; keep the emotion restrained and sincere.

Audition line from the game:
> You walk the path. I will become it.

**Rowan / Explorer**
> Young adult male adventurer. Bright, curious and brave, with a little nervous excitement. Conversational, clear and lightly breathless when danger is close. Keep him believable and warm.

Audition line from the game:
> Hold on, Princess. We are coming for you!

**Dryad**
> Adult female guardian of an ancient forest. Warm, patient and quietly powerful. A gentle voice with a firm boundary when her home is threatened. Unhurried, intimate delivery with natural pauses.

Audition line from the game:
> These roots are my home. Ask for their help; do not try to become their master.

**King**
> Older adult male king speaking privately to two people he trusts. His worry for his daughter is just beneath a controlled, steady voice. One small pause before the final appeal.

Audition line from the game:
> Bring my daughter home. I am counting on you.

**Princess**
> Young adult female, frightened and disoriented but still trying to understand. Soft, clear speech with genuine uncertainty. Let the question feel like a thought she has only just formed.

Audition line from the game:
> I know this is my room… why can’t I remember any of you?

**Great Alchemist**
> Older adult male healer with a warm, textured voice. Thoughtful and concerned. Explain something difficult to friends who need hope. Allow the two short statements to settle before the final sentence.

Audition line from the game:
> Her body returned. Her spirit did not. We must light her way home.

**Physician**
> Adult male physician, precise but compassionate. A calm, serious assessment delivered to a worried family. Keep the sentence clear and human, with a brief pause between the diagnosis and the explanation.

Audition line from the game:
> This is no ordinary sleep. An ancient curse holds her.

## Short ElevenLabs audition inputs

Choose an expressive model available in your account. Models supporting audio tags include Eleven v3/v4; other models may behave differently. Try one cue at a time and listen for accidental spoken directions. See [official audio-tag guidance](https://elevenlabs.io/docs/help-center/product/core-capabilities/text-to-speech/how-do-audio-tags-work-with-eleven-v3-and-v4).

Architect:
```text
[determined] You walk the path. [short pause] I will become it.
```

Rowan:
```text
[excited] That’s our ride! Let’s find the three ingredients and reach that dragon.
```

Dryad:
```text
[calm] These roots are my home. Ask for their help; do not try to become their master.
```

Princess:
```text
[confused] I know this is my room… why can’t I remember any of you?
```

Use supported tags as performance suggestions, not guaranteed exact timings. Keep one voice per character. Confirm the model's current status and publication eligibility before using generated audio in a released game.

## Suggested trailer voiceover pass

These are existing game lines or excerpts, arranged as an optional trailer edit. The delivered draft contains none of these recordings yet. Adjust timing after you hear the takes.

- 0.4–4.5 s, King: “Bring my daughter home. I am counting on you.”
- 5.1–9.3 s, Architect: “You walk the path. I will become it.”
- 10.0–12.1 s, Rowan: “That’s our ride!”
- 12.4–17.4 s: let the dragon flight breathe; use wings and music.
- 17.6–20.8 s, Dryad: “Who stirs the roots of my home?”
- 21.0–24.4 s, Rowan: “Come along. We’re taking you home.”
- 24.5–33.5 s: music and title. Leave enough time to read the game name.

## Image-to-video prompts

Upload the named PNG first. Use a single 4–5-second shot, 16:9, low motion and high reference consistency where those settings exist. Prompt adherence is probabilistic; these prompts do not guarantee an unchanged scene. All of these are optional cinematic interpretations, not replacements for genuine gameplay capture.

### Portal / title artwork
Reference: original `images/title-screen.png` or the supplied title still.

```text
The supplied fantasy pixel-art composition holds its character designs and palette. The purple portal rotates slowly within its existing stone arch. Tiny violet sparks drift upward, distant waterfall mist moves gently, and warm lantern flames flicker. The two heroes hold their original poses with subtle breathing. A very slow cinematic push-in brings the viewer toward the portal. Crisp illustrated pixel-art texture, stable architecture and a continuous shot.
```

### Architect transformation
Reference: `stills/02_architect_transformation.png`.

```text
The same small purple-robed Architect releases a gentle stream of emerald magical particles into the surrounding stone. His silhouette gradually dissolves into light while a thin green ripple spreads across the existing ruin. The nearby Explorer watches with a restrained reaction. Preserve the supplied character proportions, costume colors and maze geometry. Fixed camera, fantasy pixel-art texture, one clear magical action over five seconds.
```

### Emerald dragon
Reference: `stills/03_emerald_guardian.png`.

```text
The emerald dragon in the supplied reference slowly lifts its head, takes a breath and opens its mouth in a short roar. Its existing wings make a small settling motion. The camera holds steady and the original garden terrace stays fixed behind it. Preserve the dragon's green scales, gold accents, anatomy and illustrated pixel-art appearance. One restrained motion in a continuous five-second shot.
```

### Flight above the clouds
Reference: `stills/04_dragon_flight.png`.

```text
The same emerald dragon carries the same two heroes through the sky with slow, even wingbeats. The riders remain seated in their existing positions. Soft clouds drift past at a different speed from the distant floating sanctuary, giving gentle depth. The camera tracks smoothly beside the dragon. Preserve the reference's fantasy pixel-art style, emerald and gold palette, wing anatomy and rider costumes. A single graceful flight shot.
```

### Heart Tree / Dryad
Reference: `stills/05_heart_tree_and_dryad.png`.

```text
The Heart Tree's existing golden center pulses softly as small leaves drift through the clearing. The Dryad blinks, inclines her head once and makes a small conversational gesture. The two heroes listen. The camera stays still, preserving the reference's forest paths, stone walls and character positions. Gentle foliage movement, warm magical light and the same detailed fantasy pixel-art texture. A quiet five-second encounter.
```

### Memory entering the jar
Reference: `stills/06_memory_in_the_jar.png`.

```text
The little golden memory drifts gently toward the open glass bottle held by Rowan. A few warm sparks trail behind it as the jar's glow increases slightly. Rowan holds the bottle steady and the Architect watches from his original position. Preserve the supplied faces, clothes, anatomy, forest setting and illustrated pixel-art style. Locked camera and one slow, readable action.
```

### Return toward the kingdom
Reference: `stills/07_home_on_emerald_wings.png`.

```text
The reference's emerald dragon and its two seated riders glide calmly toward the existing kingdom, with gentle wingbeats and a small natural rise and fall. Distant castle rooftops and the river move slowly in parallax. The jar stays secure with Rowan. Preserve the reference's character identities, fantasy pixel-art finish, green dragon silhouette and grounded landscape. Smooth tracking camera in a continuous five-second shot.
```

If the generator has a separate exclusion field, try: `character redesign, photorealism, extra limbs, changing faces, distorted hands, warped architecture, invented text, changing UI, camera shake`. Some tools prefer positive prompts and do not have a negative-prompt field; do not force this list into every tool.

## Editing brief for a tool or person that accepts a brief

This is an editing brief, not a promise that Clipchamp has a text-command field:

```text
Build a 30–35-second, 16:9 fantasy puzzle-adventure trailer for Dual-Reality Maze: The Architect's Oath using the supplied real game clips. Open with readable gameplay and the Explorer/Architect partnership, then show the Architect transformation, emerald dragon, flight and Heart Tree encounter. Finish with the memory rescue and title artwork. Keep the real game's pixel-art look. Use short, readable titles, restrained transitions and a gentle build in music. Leave space for character dialogue, duck music beneath speech, and avoid revealing the Princess's final reunion. End on the exact game title with enough reading time. Export 1080p.
```
