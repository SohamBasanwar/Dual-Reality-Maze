# Dual-Reality Maze — revision 05

Reference-led curved enclosures • 25 October 2026 • **mechanical prototypes, not a full-print release**

Open `index.html` for actual CAD renders and links. The supplied fantasy illustration is the exterior target. The previous box-like wall extrusion has been replaced by curved cross-sections, tapered shoulders, a concave front waist and descending grips. The Architect gate is arched and stays on the upper shoulder. Main has a softened octagonal altar shape, paired sound openings and a rear sliding cable cover.

The render shows bronze-coloured structural polymer. The parts do not require multiple structural filament colours. Translucent emblem inserts are separate. CAD textures, borders and role motifs are real relief or engraving; the small electronic representations are dimensional placeholders.

## What is included

- `cad/*-revision05.FCStd`: FreeCAD documents with individually named solids and a separate `ComponentEnvelopes` group.
- `Open_Revision05.FCMacro`: opens all three native documents with the outer parts visible and the internal reference blocks hidden.
- `cad/*-printed-parts.step`: mechanical printed parts in their assembled positions, excluding electronics.
- `prototype-stl/`: individual parts, in millimetres and assembly coordinates. Orient individually before slicing.
- `fit-tests/`: small battery-door, shell-latch and rear-shutter samples extracted from this revision.
- `build_revision05.py` and `dimensions.json`: editable regeneration source. The native FreeCAD objects are BRep solids; dimensional changes regenerate through this script, not a fully constrained sketch history.
- `previews/`: assembled, internal, exploded and orthographic views, plus Main shutter open/closed views. These are renders of exported CAD, not new concept illustrations.
- `ASSEMBLY_REVIEW.json`, `CAD_VALIDATION.json`, `MESH_VALIDATION.json`: computed checks, with the scope stated in each.
- `PRINT_AND_ASSEMBLY.md` and `DIMENSION_CHECKLIST.csv`: orientation, fit-test and measurement guidance.

## Interior and fallback accommodation

Every unit retains a provisional **166 × 55 × 10 mm full-size breadboard**. The handheld battery sits in a grip with its own toy-style underside door. Main has a separate underside battery door. Battery-snap lead space, routing clearance and serviceable board retention remain.

Each box reserves **60 × 32 × 18 mm** for an optional ESP32 development board above one breadboard section, plus **66 × 40 × 5 mm** of jumper clearance above it. These are explicitly empty planning volumes, not a selected module or universal mount. The user has not chosen an ESP32. Check header-row spacing and access to breadboard contacts; a short jumper harness or movable carrier may be needed. Keep the remaining breadboard accessible for the other circuitry.

Espressif's reference DevKitC V4 is smaller than this allowance in plan, but clone dimensions vary. A metal-contact breadboard underneath an antenna can impair its placement. The eventual board must have its antenna positioned and tested using its manufacturer's guidance; the reserved volume is not radio-performance verification. Leave this area free of batteries, loose wiring, conductive finish and new fixed ribs until selection.

Main uses a conservative **69.2 × 54 mm UNO cradle** for either R3 or R4. Its broad rear access opening avoids committing the enclosure to one USB connector shape. The cover slides approximately **35 mm** to reveal the cable opening. Open before plugging in; close when unplugged. It is a cover, not a clamp or a waterproof seal. A keyed end stop is trapped by the closed lid. Cable-jacket strain relief and the actual USB-B/C plug/bend must be verified with the selected lead. Use a short extension/pigtail if the board's connector orientation requires it.

## Before a full case is printed

The CAD checks do not establish hand comfort, latch fatigue, actual component dimensions, servo torque, electrical integration or one-hour battery life. Print the small fit samples first and measure the real parts. A common 9V battery is the requested mechanical allowance; the regulated servo supply and the final power-control module are still unresolved. This revision does not turn the Main button into a validated master-power circuit.

The reference's extra decorative buttons were not added as unused controls. Explorer retains joystick/reveal input, Architect retains dial/confirm/gate and Main retains display/sound/power actuator. No presentation or firmware was changed by this revision.

No new paid software is needed. Installed FreeCAD, PrusaSlicer and OpenSCAD remain sufficient; Blender is used only for previews. OpenSCAD can inspect the exported meshes, while FreeCAD/Python is the mechanical source.

Regenerate with:

```powershell
& 'C:\Program Files\FreeCAD 1.1\bin\python.exe' 'C:\Users\soham\Documents\CS 362\GP\enclosure-design\revision-05\build_revision05.py'
```

Earlier revisions remain unchanged. Nothing has been submitted to UIC or sent to a printer.
