# Dual-Reality Maze — Revision 12

Soham Basanwar · CS 362 · 4 November 2026

Open index.html for the full illustrated assembly guide. Revision 11 is preserved separately. The current revision conceals ownership/assembly lettering on exterior parts, retains the four Main green-light galleries and independent RGB shield, and prepares separate opaque/translucent print jobs.

## Files to use

- index.html: open/closed cases, adjustable carriers, gate installation and motion, concealed engraving photographs, and every printed part.
- print-preparation.html: the 95 installed parts with materials, candidate orientations and support notes.
- PRINT_BRIEF.md: operator settings, sample-first process and remaining physical checks.
- PART_LABELS.html and PRINT_MANIFEST.csv: sorting labels and quantities.
- uic-voron-provisional/index.html: tentative material-separated plates for UIC's published 290 × 290 × 285 mm Voron volume. Staff must review supports and actual usable area.
- cad: three native FreeCAD documents and STEP assemblies.
- prototype-stl: 95 individual installed pieces, all millimetres at 100% scale.
- fit-tests: sample rail, jaw, key and lighting geometry.
- REVIEW_VALIDATION.json: final digital check scope and limitations.

There are 88 opaque structural parts and 7 translucent optical inserts. No electrical component reference geometry is a printed part. Print each component separately, then assemble; do not print the complete closed assembly as one solid. Optional height inserts and optical roofs are substitutions.

## Fabrication status

Digital prototype for staff review and fit sampling. The nominal hardware envelopes are not measurements of the user's actual components. Test clips, sliding fits, optical opacity/diffusion, switch travel and gate movement before printing full shells. UIC's 0.6 mm nozzle / 0.3 mm layers are coarser than several current small features. Ask staff about a smaller nozzle/profile or feature changes; the choice of printer has not been confirmed. No printer-specific G-code is supplied.

The lighting helper in lighting/BreathingAccent.h passes a host-side timing test but has not been flashed or integrated with the game's firmware. Pin allocation, LED driver/current, servo power and battery runtime need bench testing.

## Software and reproducibility

Opening and slicing: installed FreeCAD, PrusaSlicer and optionally OpenSCAD are sufficient. No new paid software is needed. Source scripts use FreeCAD's bundled Python; Blender renders the actual meshes. Standalone packing uses Python 3.11+, numpy and trimesh. requirements-print-prep.txt lists those optional Python dependencies.

build_revision12.py starts with baseline-r11 and moves exterior lettering to concealed faces. fix_base_marks.py is a one-time repair of the earlier R12 checkpoint and must not be rerun on already repaired files. Earlier source helpers and baseline files remain for reproducibility. Do not run a previous revision's main builder over the current native files.
