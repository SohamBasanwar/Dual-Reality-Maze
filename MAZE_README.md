# Dual-Reality Maze — The Architect’s Oath

On Windows, double-click **Start Maze.bat** to open the game in your default browser. Keep it beside **Dual_Reality_Maze_Story_Edition.html**. You can also open the HTML directly, or run **bash start-maze.sh** from Git Bash. The Bash launcher also supports macOS, Linux, and WSL. Everything needed to play is embedded in the HTML; no server, installation, or internet connection is required.

## Chapter I

The illustrated title screen opens with drifting magical particles, glowing light, and an artwork loading bar. Select **Begin adventure** to enter the six-panel prologue, or **Skip the prologue · Play** to start the maze directly.

Each prologue and epilogue comic panel has a visible **10-second countdown**, then fades automatically into the next scene. If dialogue is still playing, **Finishing dialogue…** appears until the last spoken line ends. Continue, Enter/Space, or either controller button advances early and stops the previous dialogue; Previous returns to an earlier panel and resets its countdown. **Auto-play** pauses or resumes automatic advancement. The countdown also pauses while the browser tab is hidden or voice settings are open. Cinematics wait at character dialogue transitions when needed so lines are not cut off.

The Princess approaches the front stairs before entering the portal. The camera returns to the heroes, and the Explorer explains that collecting the Sun, Moon, and Star runes awakens the key. A speech bubble above him shows the three matching rune symbols. His line finishes before the Architect's oath and transformation begin. The Architect then dissolves into purple stars and awakens the gray maze. The fourth prologue panel, **Magic and knowledge**, shows the Architect controlling stone while the Explorer studies maps and ancient maze lore.

Play for **10 minutes**. Find the Moon, Sun, and Star runes. The Star rune is in the northeastern chamber, farther inside the room so the wall cannot cover it. When all three runes are collected, gameplay pauses while their symbols rise, merge into light, and awaken the ornate golden Aether Key. The Explorer celebrates with a spoken caption: “The runes united! The golden key is ready. Let’s claim it!” The timer and controls stay paused until his line finishes (or you select Continue). Collect the key and head toward the portal.

Near the portal, control passes to the finale: the Architect reforms, the walls return to gray, both heroes enter the wormhole, and they find the Princess asleep under a curse. Four epilogue panels show their return and the physician's discovery. The last button says **Continue to Chapter II**, leading to **Chapter II — The Alchemist's Cure**. Its restored Princess-and-Alchemist title illustration has a **Begin Chapter II** button. **Replay Chapter I** returns to the prologue. Chapter II is also accessible from the opening title screen.

If time runs out, **The Kingdom Falls** shows the monster throne illustration and a single **Replay Chapter I** button. The rescue epilogue and Chapter II preview are blocked after a loss. Replay starts a fresh maze round with 10 minutes, no key, and no collected runes.

Controls: WASD/arrows move; Q/E select an Architect control; Space toggles it; R/F reveals; P/Escape pauses. Only two gates or bridges may be powered at once. Bridges/gates must finish opening before crossing. Story scenes, the guide, and pause do not consume the timer.

A purple Architect spirit hovers beside the selected gate or bridge. Both chapters now use the same enlarged 84-pixel spirit (previously 58 pixels in I and 48 in II). Q/E or selecting an OFF/ON button moves the spirit in a 280 ms glide. A purple outline and passage label identify the target immediately. Successful toggles use a separate casting sprite and a 360 ms magical pulse; rejected actions use a short warning pulse. These effects never pause the timer or movement. Selection alone does not activate anything, and the two-power limit and occupied-passage protection still apply. Reduced-motion mode uses immediate selection changes without the glide, bobbing, or travelling sparks.

Only character dialogue is spoken. Comic descriptions and scene narration remain visible text and are never read aloud. The opening and rescue cinematics use the same cast. The King and Architect have deeper delivery, the Explorer a brighter voice, and the Princess a separate female voice. Urgent, worried, gentle, grave, and resolute lines use different pacing and pitch. The playback system prefers verified prerecorded character audio when it has been generated and embedded. Until then, browser speech remains an optional fallback, with captions available throughout.

Open **Voices & volume** on the title screen, or **Voice settings** during the story, to choose and preview each of the seven character roles, including the Great Alchemist and Dryad. Speech starts at 100% game volume; computer volume still applies. Adjust volume and pace in the same panel. Local English voices are preferred; any online voices are labeled. Choices apply to the current game session. **Voice off** stops speech and clears queued dialogue. Missing voices or speech failures leave captions available and do not trap automatic scene progression.

## Chapter II — The Alchemist’s Cure

Select **Chapter II** from the opening title screen, or finish Chapter I successfully. The original title illustration shows the sleeping Princess in a dream above Rowan, the Architect and the Great Alchemist. Its Begin Chapter II button introduces the dragon journey. Three introductory comic scenes explain the route and the three ingredients. Character dialogue remains spoken; descriptions are silent. Comics retain ten-second auto-next, fades, manual advance, auto-play pause and voice controls.

Chapter II now begins with a rendered opening cinematic: both heroes enter the gray ruins, the camera reveals the whole maze, then closes in on the dragon. Its closed/half-open/open-mouth poses play with a synthesized roar. The camera returns to Rowan and the Architect for character-only dialogue, then the Architect dissolves into green stars and an emerald wave awakens the gardens. One continuous camera move settles into the exact gameplay view. The ten-minute timer and all movement/Architect inputs stay locked until the opening finishes. Skip opening is optional; skipping the preceding comic still plays this opening. Restart/replay also replays it. Voice settings pause it, hidden tabs pause it, and a bounded speech fallback prevents a stalled speech engine from blocking progress. Sound on/off controls the roar independently of character voices.

The rectangular laboratory has been replaced by an irregular **hanging-garden ruin** with separate terraces, broken outer edges, visible rock undersides, stairways, waterfalls, swaying plants, flickering torches, crystal glints and drifting clouds. Every passage and prop is rendered individually. The internal 37×23 collision grid supports the irregular outline. Both chapters share the 1672×941 view, 1304-pixel world area, 32-pixel tiles, 51-pixel Explorer, eight-pixel steps at the same 72 ms interval, and smooth movement interpolation.

Walk directly onto amber crystal, moonblossom and dew of the veil to collect them. Ingredients have no cages, locks or power requirement. The Architect controls three colored doors and two bridges, with a maximum of two open at once. Passages animate before becoming walkable and cannot close while Rowan is on them. The Chapter II sidebar uses an emerald-and-sky palette, a dragon crest, wind ornaments and a cloud objective area while preserving the colored OFF/ON buttons and their positions. The darker emerald Architect spirit follows the selected passage and casts without pausing the timer. His hand spell, casting beam, merge stars and reformation glow share the wall-green palette; Chapter I retains its purple magic. WASD/arrows move, Q/E selects, Space toggles, and P pauses. Clicking a reachable floor also follows a path at the same walking speed.

Bring all three ingredients to the **dragon’s roost in the northeast**. Boarding starts automatically. Controls lock and the timer pauses while the Architect materializes, the heroes board the emerald dragon, and it flies to the **upper sanctuary**. The Alchemist greets them in a new comic. Continue starts the rendered brewing sequence; the next comic presents the cure. The dragon then flies both heroes directly to the kingdom. Flight now uses one complete transparent dragon silhouette with continuous wing flex, eliminating the incompatible sprite crops that made its edges disappear. The return backdrop shows a grounded town, farms, a river and the Princess’s castle on solid land. Further comics show the palace arrival, the Princess briefly waking, and the forest clue. This leads to the playable Chapter III title; Chapters IV–V remain planned. Chapter II and III share the same title-page template: franchise, chapter number, title, subheader, story, Begin/Coming soon action, replay and footer details. Chapter II comics reuse Chapter I’s layout and Previous, Continue, Skip, auto-play, countdown and voice controls.

If Chapter II’s timer expires, **The Eternal Slumber** shows a single 1536 × 1024 comic illustration, matching Chapter I’s bad-ending image dimensions and 86% × 87% card layout. The Princess sleeps forever while the grieving King turns to forbidden magic; guards and an attendant lie fallen around the failed ritual. Only the King’s dialogue is spoken. Replay Chapter II restarts the opening with ten minutes; Title screen exits. There is no success epilogue or Chapter III continuation after a loss.

Chapter entry keeps an opaque loading curtain until the first comic is drawn, then fades into that comic. Cached visits clear old cinematic/end states; a canceled load cannot reopen the chapter.

The upper sanctuary is an automatic story destination, not a second controllable maze. Flight scenes have a **Skip flight** button and pause when the tab is hidden or voice settings are open. Chapter II retains its ten-minute timer, timeout/replay isolation, two-power limit and controller input hook. Physical Arduino transport remains unconnected.

Verification: the complete ingredient-to-dragon route passes in 419 eight-pixel movement steps. Checks cover free pickups, required bridges, passage occupancy, premature boarding, timer/control locks throughout flights and brewing, eight comic dialogues, fades, auto-next, defeat/replay and Chapter I regressions. Real canvas renders verify the new assets and changing animation pixels. Browser verification completed on October 15 after restarting an unresponsive preview server: restored title, comic controls and real-time auto-next, live maze panel, keyboard movement, two-control limit, accelerated full route, ascent, brewing, homecoming, Chapter III card, timeout and replay. No browser console warnings or errors were observed. The Auto-play button’s accessible pressed state was corrected and checked after rebuilding. Run `node maze-source/work/test-chapter2.mjs` from the project root. `node maze-source/work/render-chapter2-check.mjs` saves actual canvas previews using the bundled canvas runtime.

## Project contents

- **images/**: every original reference and generated image from this task, including early unused art and UI preview captures.
- **maze-source/work/**: editable JavaScript, HTML, builders, tests, and a copy of the source assets.
- **art-prompts/**: generation prompts for story artwork.
- **Dual_Reality_Maze_Animated_Challenge.html**: the standalone challenge without the story scenes.

From **maze-source/**, use Node.js to rebuild and verify:

```
node work/build-rendered.mjs
node work/build-story.mjs
node work/test-rendered.mjs
node work/test-story.mjs
```

Builders write to maze-source/outputs. Copy the rebuilt Story Edition into this project root to update the launcher target.

## Validation and hardware

Automated checks cover a complete 644-step run through all three runes, the key and escape, power limits, animated passage collision, reveal cooldown, pause, defeat, replay, comic fades, the front-stairs portal path, timer pauses, rune awakening, reverse Architect transformation, the epilogue and Coming soon state. They also cover title loading, the ten-second panel countdown, countdown pauses and resets, and automatic transitions into the maze and Coming soon. Browser checks confirm the title layout, actual countdown timing, the Auto-play toggle, and no console errors.

This is a laptop game. The supplied R4 firmware has a different 15×10 authoritative map and one bridge. This game has a larger map, three runes and five elements. The Story Edition now accepts the Explorer and Architect test sketches through separate USB serial connections. The Main ZIP does not relay inputs; a three-board R4 hub still requires firmware/state integration. The existing Arduino ZIPs and original HTML files are preserved.

### Architect controller input hook

The HTML exposes `window.mazeArchitect` for a future serial/controller transport. The Story Edition has a separate optional Web Serial input adapter for the supplied R3 debug messages. No firmware was changed or flashed. Call `selectPotentiometer(reading, maximum)` for a numeric ADC reading: maximum defaults to 1023; use 4095 for a 12-bit reading. The five equal dial regions select Gate A, Gate B, Gate C, Bridge A, Bridge B in that order. A 1.2% dead band around boundaries prevents noisy readings from flickering between selections. Invalid readings are rejected.

`select(index)` selects a zero-based control directly. `toggle()` toggles the selected passage and should be called once per button press edge; `setOpen(true)` / `setOpen(false)` can apply an explicit state. These methods return whether the request was accepted and share the same guards as the keyboard and on-screen controls, including scene locks, pause, the two-power limit, and occupied passages. The spirit follows the same selected state automatically.

Automated spirit checks cover every dial region, input jitter, rapid retargeting, invalid readings, short casting with a live timer, scene locks, and restart cleanup. Browser checks verify the generated hover/cast sprites, keyboard selection, the bridge spell effect, and no console errors.


## Chapter III — The Forest of Lost Memories

Chapter III is playable from the title screen and Chapter II success. The rainforest uses raised stone walls and paths on grass, leafy wind-swaying vines, rain and drifting leaves. Larger chapter-local characters retain the shared camera dimensions and eight-pixel / 72 ms movement.

The Architect first fails to merge. The Dryad appears to the right of the separated heroes. Her conversation uses quiet facial animation; raised-hand magic is reserved for spells. She breaks the southern wall and assembles a stone road downward. Walk down it into the separate Hidden Orchard. Three distinct groves contain Golden Moonpear, red Emberheart and Violet Starplum. Beside each tree, use **SPACE** when the large semicircle needle reaches gold. There is no central corridor guardian. The purple tree is below its guarding patrol. Touching a guardian resets all three fruits and returns Rowan to the orchard entrance. The offering has no time limit. Return through the marked exit and approach the Dryad.

The three-gift comic awards a soul-collecting bottle, protective rainforest robes for Rowan, and a golden circular nature seal for the Architect. Rowan changes clothes during the blessing and retains those robes through the return comics. The ten-minute hunt then begins: the memory moves to a different grove at 8, 6, 4 and 2 minutes remaining. It cannot be caught during teleportation. The Architect can open only two passages simultaneously.

Capture pauses the timer and controls. The Architect reforms with clear space beside Rowan; the child memory plays, enters the open jar voluntarily, and the lid closes. The Dryad rises at that capture location. Comics alternate with the golden messenger leaf flight, camera pullback, dragon arrival zoom and a five-second home flight. The Princess recovers her memories; Chapter IV remains Coming Soon. Timeout shows only **Lost to the Forest**, with Chapter III replay and title return; it never enters the success story.

All generated art is in images/ and build copies in maze-source/work/assets/. Chapter III art provenance and available prompts are in art-prompts/CHAPTER3_FOREST.md and art-prompts/CHAPTER3_REVISION.md. Verification details are in task-notes/CHAPTER3_VERIFICATION.md.

### October 19 refinements

Only Rowan enters the orchard. The Architect waits at the Heart Tree with his hands down. Even grazing guardian contact plays a brief open-mouth reaction, clears every fruit immediately, then returns Rowan to the orchard entrance.

Rescue staging selects reachable floor cells away from passages, with space between actors and clearance from raised wall edges. The messenger leaf flight lasts 6.5 seconds. The dragon approaches from offscreen at the upper-left and flies toward Rowan as the camera closes in.

The Dryad's new Heart Tree is a larger original landmark with a glowing golden heart, ivory blossoms, hanging golden leaves, subtle sway and leaf drift. It fades when Rowan would be hidden behind it. Reduced-motion mode keeps its decorative motion still. Research, exact prompt and asset paths: art-prompts/HEART_TREE_REFERENCE.md.


## Expressive voices and physical story controls

Open **Controllers / pause** to enable the simplified interface and connect Explorer / Architect USB ports at 9600 baud. Either player's button continues comics; directional input no longer skips them. Optional Previous, Skip and Auto-play shortcuts are hidden in controller mode. Joystick up opens the comic menu; joystick click pauses in normal play and picks fruit in the orchard. Press both existing buttons together to pause in the orchard. Return the joystick to center after a scene change.

See **hardware/CONTROLS_AND_CIRCUITS.md** for the actual ZIP pin review, state-by-state actions, serial formats and the original Architect servo limitation. The Main sketch remains a standalone LCD/buzzer test. Physical hardware was not tested.

The local ElevenLabs pipeline covers 50 existing dialogue lines with seven consistent cast profiles, authored emotional contexts, manual overrides, cache receipts and reviewed batch generation. Generated recordings embed into the standalone HTML and play offline. Voice settings add mute, subtitles, automatic progression, replay and browser/captions-only fallback. No provider key is placed in frontend code.

See **voice/README.md** for setup and generation. The user approved only the six-line prologue sample after configuring a local key and four provider voice IDs. At this build, provider recordings remain ungenerated; no paid API request has been made. The remaining 44 lines require separate authorization.

Validation includes the existing four gameplay/story suites, `node voice/test-pipeline.mjs`, and real Chrome checks in `node task-notes/test-voice-controllers-browser.mjs`. Browser playback was tested with a synthetic tone fixture, not a generated actor recording. Artistic voice quality, actual ElevenLabs generation and physical board behavior remain to be checked after configuration.

## Objective reveal — November 5, 2026

R (or F), the Reveal button, and the Explorer light-sensor rising edge share the same chapter-specific rules. Each activation highlights the nearest remaining objective by shortest floor-route distance, with a luminous trail and a gold target marker. Closed gates/bridges on that route are marked amber; the Architect must still power them. Reveal never opens passages, moves Rowan, picks fruit, or avoids guardians automatically.

- Chapter I: remaining runes, then the golden key, then the wormhole. The eastern lock is excluded until the key is held.
- Chapter II: remaining ingredients, then the dragon's roost.
- Chapter III: Hidden Orchard only—remaining fruit trees, then the return exit. A route ends beside the tree where SPACE picking is available. No reveal during the memory hunt or other forest sequences.
- The trail and target glow last 3 seconds and fade together. The next activation is allowed 12 seconds after the preceding activation (9 seconds after the effect ends).
- Each chapter has three activations per attempt. Remaining charges and the recharge countdown are shown on the Reveal button. Rejected inputs do not spend charges. Guardian contact resets fruit but never replenishes reveals. Restarting the chapter restores its three charges.

Checks: maze-source/work/test-reveal.mjs and task-notes/REVEAL_VERIFICATION.md.
