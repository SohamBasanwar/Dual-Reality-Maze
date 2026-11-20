# Manufacturing review — Dual-Reality Maze

5 November 2026. Local review following the Makerspace rejection supplied by Soham. This is a proposed recovery plan for discussion with Evan McCarty, not a print request or a revised set of approved models.

## What went wrong

The submission included 95 installed pieces (88 opaque, seven translucent), plus four fit samples. Asking staff to start with samples did not justify attaching the entire unproven assembly. Digital solid, mesh and interference checks did not demonstrate manufacturability. The print-preparation records explicitly mark the orientations as unverified by slicing.

The submitted design also depended on details finer than the lab's published starting process. Requesting a different nozzle did not resolve that mismatch. The staff email does not identify every failing surface, so the findings below must not be presented as their complete diagnosis.

| Confirmed in the submitted sources | Consequence for the redesign |
|---|---|
| Indexed mounts use 0.25/0.30 mm nominal clearances; the key has a 0.4 mm split leaving approximately 0.7 mm-wide fingers. | Replace these delicate locks with a simpler retention method that can be sampled using the lab's standard process. |
| Rail floors are 0.65 mm; rail walls/lips include 1.35 mm sections. | These need redesign or process-specific evidence, not a blanket claim that the mesh is valid. |
| Architect button has a nominal 0.15 mm rest gap and 0.45 mm stroke. | Measure the installed breadboard switch and test an accessible actuator independently before fixing its reach. |
| Curved shells, recessed tracks and integrated internal features were assigned candidate orientations without slicing verification. | Review cross-sections, bed contact, overhangs and support-removal access in the intended orientation. Rounded shapes alone are not the problem; adding supports everywhere is not a solution. |
| Component envelopes and mounting details remain provisional. | Measure actual hardware, connectors and assembled wire heights before printing a full enclosure. |

Source evidence: revision-12/PRINT_PREP.json; revision-12/adjustable_mounts.py; revision-12/build_revision10.py; revision-12/build_revision11.py. The existing CAD is retained as design/reference material, not a print release.

## Smallest useful next step

1. Review one Explorer controller with Evan McCarty: actual hardware, a section through the grip and shell joint, and the proposed print orientation. Preserve the rounded grip silhouette, fantasy styling and screwless access. Revise the split plane and internal construction wherever printing requires it.
2. Consolidate retention into a measured tray and accessible removable bridge where practical, instead of separate jaws, keys and height frames for every component. Retain only useful adjustment; check electrical clearances and service access. This is a proposed simplification, not yet implemented.
3. Design only four structural test pieces initially: a representative shell-joint pair and a representative tray/retainer pair. Use the actual proposed geometry. Include enough of the curved wall and retention feature to test printing and assembly; do not reuse the rejected tiny-key design unchanged.
4. Slice those pieces against the agreed process. Check missing features, bed contact, unsupported spans and whether supports can actually be removed. Ask the instructor to review them. Submit only that small test set when ready; then physically test fit, repeated opening and component retention.
5. After successful tests, print one complete Explorer enclosure. Architect's moving gate and Main's light channels follow as separate, justified steps. Do not re-submit all three assemblies together now.

## Light inserts

Follow the staff recommendation to evaluate resin for the small inserts. Their note explicitly says optical clarity requires manual polishing. The decorative LED windows need diffusion rather than an image-clear view, so evaluate one insert with the real LED before specifying polishing or producing the whole set. The photoresistor window has a different sensing function and needs its own light-response check. Do not claim uniform illumination from a render.

## Process reference

UIC currently lists a 0.6 mm FDM nozzle, 0.3 mm layers and approximately 2 mm minimum features, depending on geometry. Its assembly guidance recommends 0.5 mm horizontal and 1.0 mm vertical separation; these are starting design allowances, not guaranteed measured tolerances. It requires bed contact and access for support removal. Its Form3+ process offers clear resin, with additional constraints on thin parts and trapped resin.

https://makerspace.uic.edu/make/digital-fabrication-lab/ — checked 5 November 2026.

No replacement models, new print request or external message was sent during this review.
