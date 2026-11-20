# Dual-Reality Maze — Revision 07

Design-review prototype, 25 October 2026. Revision 06 remains available for comparison. These are actual CAD solids and meshes; no render establishes physical fit or print readiness.

## Compact gate choice

The Architect now has a low-profile **rotary rune-gate window**. The SG90 body is inside the upper shoulder, separate from the breadboard and UNO reservations. A removable cover presents a small arched viewport. In the closed position, narrow slots in the rotating disk read as gate bars; after a nominal 110-degree turn, the open sector aligns with the viewport. The top of its decorative arch is 6.8 mm above the nominal 58 mm lid plane, compared with the old guard's approximately 61 mm protrusion.

The supplied nylon servo horn engages the real servo spline. A matching pocket in the printed disk transfers torque from the horn. The fixed cover limits upward movement of the disk and horn, replacing the usual centre screw's retention function. This is a provisional capture concept: measure the actual horn's hub, arm, seating depth and axial engagement before printing. It is not a verified universal SG90 spline. The cartridge locates the servo body; the cover and collar capture the cartridge. Use regulated servo power and a common signal ground.

A thin clear PET shield over the viewport is recommended so fingers cannot touch the moving disk. Its attachment and the physical horn-retention test remain to be resolved. The render shows the open viewport so the mechanism is visible. Do not infer a sealed window from it.

Other styles considered:

| Idea | Advantage | Trade-off |
|---|---|---|
| Rotary rune window — modeled here | Low height; recognizably changes from bars to an open arch; no external swinging arm | Requires a fitted horn pocket and a small viewing shield |
| Lock/unlock pointer | Fewest parts; easy to read | Indicates the gate state rather than showing a gate |
| Small drawbridge or barrier | Literal opening motion | Still projects above the controller when raised |

The window is our own mechanical proposal. A creator's [SG90 shutter project](https://projecthub.arduino.cc/jkiiski/electronic-shutter-control-for-pinhole-camera-2f25e6) supports the general servo/shutter approach; it does not validate this geometry. [TowerPro's SG90 specification](https://towerpro.com.tw/product/sg90-analog/) lists a nominal 23 × 12.2 × 29 mm servo, but clones, horns, tabs and cable exits vary.

## Battery-door comfort

The handheld service pad now has a broader rolled transition, and the exposed battery-door perimeter is rounded. The door remains a separate underside part with two locating tabs and a cantilever catch. The signature is on its inner surface, away from the hand. Cell, clip and wiring reservations stay in place. The actual grip/battery fit coupons must be held and cycled before a full enclosure print; a digital fillet cannot establish comfort or latch durability.

## Personalization

“Soham Basanwar” is engraved on the large shells and inside the battery doors. Selected small parts carry “SB” on accessible faces away from their running or latching surfaces: button caps, switch cassettes, shutter finger tabs and the compact gate parts. Very small keepers, thin optical parts and narrow clips remain unmarked where lettering would damage function or legibility. Every printed part has the full name in its STL filename, native CAD label and parts list. The `PARTS.csv` marking column specifies the actual treatment of each part; no blanket claim is made that every tiny clip is engraved.

## Preserved requirements

- Explorer: joystick, isolated raised photoresistor dome with two lead passages, RGB emblem.
- Architect: potentiometer, pushbutton, internal SG90 and visible gate-state window, RGB emblem.
- Main: I2C LCD/backpack, buzzer, power actuator, RGB emblem and universal provisional UNO cradle.
- Three full-size breadboards, PP3 battery reservations, removable screwless carriers, optional ESP32/wiring space.
- Rear controller I2C shutters, both Main side I2C shutters, separate Main rear USB shutter for the R3/USB fallback.
- Short wired I2C links; no HC-12 or assumed wireless hardware added.

The dimensions remain nominal. Adjustable means editable and replaceable carriers, not a guaranteed fit across all boards. Do not print fixed hole pins until the actual hole patterns are known. The photoresistor's thin printed dome may block light in opaque filament; the separate clear-film option remains available. One-hour battery runtime and power switching have not been demonstrated.

## Files and validation

Open `index.html` for actual model views and the open/closed gate comparison. `cad/` contains native FreeCAD assemblies and STEP files; `prototype-stl/` contains individual parts. `fit-tests/` contains samples cropped from the real models. `CAD_VALIDATION.json`, `ASSEMBLY_REVIEW.json` and `MESH_VALIDATION.json` describe checks that have actually run.

Use FreeCAD 1.1 to inspect or regenerate and PrusaSlicer to orient and prepare test pieces. No additional software installation is required. The installed OpenSCAD remains optional. Check the selected UIC printer/profile, material and support removal access before arranging a print; no print request has been submitted.
