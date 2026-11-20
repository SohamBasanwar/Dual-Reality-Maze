# Dual-Reality Maze: chapter development plan

Build and verify one chapter at a time. Chapter I is the established game; Chapter II is the first implementation milestone. Chapters III–V remain planned until their own playable builds and checks are complete.

| Chapter | Story and setting | Main puzzle | Exit transition | Status |
| --- | --- | --- | --- | --- |
| I — The Architect’s Oath | Floating crystal dungeon; rescue the Princess and discover her curse. | Three runes awaken the key; two Architect power slots. | Physician sends the heroes to the Great Alchemist. | Complete; preserve existing behavior. |
| II — The Alchemist’s Cure | Irregular hanging gardens below an Alchemist sanctuary in the clouds. | Collect three ingredients, cross three doors and two bridges, then reach the dragon’s roost. | Automatic dragon ascent, Alchemist brewing, dragon flight home; the Princess reveals the forest clue. | Redesigned playable build; route, cinematic-state and canvas-render checks passed. Browser walkthrough and layout verification passed October 15. |
| III — The Forest of Lost Memories | Moonlit forest ruins and spectral paths; recover home, father, and attack memories. | Architect lanterns reveal otherwise hidden paths; still only two power slots. | The restored memory points to a bell in the Clockwork Citadel. | Planned. |
| IV — The Clockwork Citadel | Brass machinery above the clouds; reveal the Hollow King’s plan to use the royal bloodline to escape. | Rotating corridors, timed platforms and three machine mechanisms. | Restored bell opens the spirit realm; the Hollow King senses the Architect. | Planned. |
| V — The Heart Beyond the Veil | A fractured palace combining earlier environments; the Princess helps from inside the seal. | Break three bindings with learned mechanics; final cooperative sequence. | Architect reforms, Explorer reaches Princess, she seals the throne; homecoming, credits and chapter replay. | Planned final chapter. |

## Delivery order

1. Chapter II: reusable chapter overlay and level data; restored Princess/Alchemist title, dragon sprites and eight comic scenes; playable maze, door/bridge controls, hovering Architect, ingredient collection, brewing animation, victory/defeat/replay; connect Chapter I success to Chapter II. Keep Chapter I timeout isolated from all sequel content.
2. Chapter III: forest tiles and comics, visible/hidden path rules, memory reveals and forest ending. Reuse the chapter shell and input routing after Chapter II validation.
3. Chapter IV: clockwork tiles and comics, safe waiting spaces, rotating routes, machine restoration, bell transition.
4. Chapter V: combined mechanics, Princess assistance, final bindings, rescue cinematic, credits and unlocked chapter replay.

## Shared requirements

- Character dialogue only; no spoken narration. Comic scenes auto-advance after ten seconds and wait for active dialogue; manual next, skip and autoplay pause remain available.
- Clear objective before play, visible progress, keyboard controls and the same guarded potentiometer hook. Controller transport/firmware is a separate integration task.
- Use CHAPTER_VIEW for the Chapter I world scale, tile size, Explorer size, eight-pixel movement and 72 ms cadence. Collectibles are free pickups; Architect controls affect passages only.
- Two Architect power slots, short casting feedback, no gameplay timer pause for casting, and occupied-passage protection.
- Timers pause during story, explicit pause, hidden tabs and chapter completion scenes. Bad endings offer replay without progressing the story.
- Each maze is rendered from individual cells and props, not a static illustration. Save all generated art and prompts in this project.
- Preserve Rowan and the other characters' established identities. Each chapter's playable environment must match its own comic and title artwork: Chapter II uses emerald stone, glass-and-brass machinery, roots, ingredient pedestals and a bronze cauldron. Future environments should have their own distinct appearance.
- Every playable chapter opens with its own illustrated title page. Chapter II restores the Princess dream-vision/Alchemist illustration with **Begin Chapter II** replacing **Coming soon**. All chapter cards must reuse the same franchise, chapter number, title, subheader, story, action and footer template used by II and III. Connect chapters through picture-to-picture comics with fades, rather than unexplained jumps between mazes.
- Verify reachability of every objective, a complete winning route, timeout/replay, invalid controller input, scene locks, and the previous chapter’s regression checks before marking a chapter playable.

## Current scope

Chapters I–III are playable in the Story Edition. Chapter III includes the grounded rainforest, separate three-fruit orchard, Dryad’s three gifts, relocating memory hunt, capture and dragon return, plus independent Lost to the Forest ending. Chapters IV–V remain planned; IV has its own Coming Soon title. Chapter III’s final accepted behavior is documented in task-notes/CHAPTER3_REVISION_PLAN.md.
