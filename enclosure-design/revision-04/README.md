# Dual-Reality Maze — Fantasy controller revision 04

24 October 2026 · Mechanical prototype for review and fit testing

Open `index.html` for the review gallery. The images are renders of the exported CAD, not concept illustrations. The electronic parts are simplified dimensional envelopes, not scans of your components.

## What changed

- Explorer and Architect have rounded gamepad silhouettes and separate PP3/9V battery bays in a grip. Main has a rounded, chamfered altar silhouette and an underside battery bay.
- Every battery bay has an independent toy-style door: two locating tabs, a recessed release tongue, terminal/lead space and internal battery stops. Opening a battery door does not require opening the electronics lid.
- All three use the same full-size breadboard reservation, 166 × 55 × 10 mm. This is still a planning dimension, not a measurement obtained from the photographs.
- The new photographs replace the earlier module assumptions: bare LDR holder, 12 mm-family tactile-switch cassette, joystick PCB carrier and LCD/backpack space. The clear R4 shipping/base plate is not included; the board sits in the new cradle.
- Screwless retention uses rear locating tabs and side-release lid latches, breadboard fingers, component cradles and reusable nonmetallic straps through anchors. There are no screw bosses. Straps and insulating pads are additional assembly materials; they are not shown as installed in the render.
- Architect has a raised upper-shoulder gate, sideways SG90 cartridge, guide frame, slotted slider, drive-pin prototype and removable guard. The 7 mm crank concept produces about 12.12 mm lift over a 120-degree sweep. Do not command that sweep until checking the actual servo and horn.
- The Architect button has a separate guided cap, captive flange, pusher and cassette stop. Main has the same actuator family for a real latching power-control module, which remains to be selected and wired.
- Explorer's reveal-eye, Architect's gate/crown and Main's portal use restrained fantasy linework. Their masks have light apertures, a concealed LED cup and a separate diffuser. These motifs follow the existing reveal, gate and portal mechanics; the detailed character portraits remain available in the older artwork package.
- Bronze is a proposed colour/finish. The mechanical model assumes a printable insulating polymer, not solid metal or metal-filled filament. A translucent diffuser insert is required for useful light transmission.

## Files

- `cad/*-revision04.FCStd`: native FreeCAD documents with separately named printed parts and reference envelopes. Hide `ComponentEnvelopes` to inspect printable parts. These are editable BRep solids; their source dimensions regenerate through the script, rather than a fully constrained manual sketch history.
- `cad/*-printed-parts.step`: separate solid parts in assembled positions. Electronic envelopes are excluded.
- `prototype-stl/`: individual prototype meshes in assembly coordinates. A valid STL is not a manufacturing approval.
- `build_revision04.py` + `dimensions.json`: regeneration source. Dimensions are millimetres. Output is mirrored in X so the joystick/potentiometer is on the player's left when viewed from the grip side.
- `render_revision04.py`: Blender renders from the exported meshes; small render-only edge highlights do not modify CAD.
- `CAD_VALIDATION.json`, `MESH_VALIDATION.json`, `ASSEMBLY_REVIEW.json`: geometric checks and any known unresolved interference.
- `DIMENSION_CHECKLIST.csv`: actual component measurements still required.
- `POWER_AND_STATUS.md`: battery, power switching, RGB and one-hour runtime plan.
- `PRINT_AND_ASSEMBLY.md`: proposed orientations, trial prints and assembly order.

Nominal enclosure envelopes: handheld units approximately 246 × 203 × 58 mm, excluding joystick/knob/gate; Main approximately 234 × 172 × 64 mm. These are intentionally larger than a commercial controller because a full-size breadboard, UNO and serviceable battery must fit. Hand comfort is not verified until a grip or shell sample is held.

## Important limits of this revision

The photos have no ruler and cannot establish mounting tolerances. Board headers, plug bends, breadboard interlocks, servo tabs/horn, switch travel and potentiometer shaft dimensions need verification. Some retention uses straps rather than a fully printed clip because it accommodates component variation without metal fasteners.

The gate is a mechanical prototype, not a tested actuator. The guard and motor/horn interface require a powered clearance and pinch-access check. The Main power actuator is not a working master-power circuit merely because it exists in CAD. Firmware and integrated circuit changes were not made as part of this enclosure revision.

One-hour operation with three store-bought alkaline 9V batteries has not been demonstrated. The Architect supply needs particular attention during servo movement. Do not print the complete cases until the power modules, connectors, component fits and material have been settled.

## Installed software verified

FreeCAD 1.1.4, OpenSCAD 2021.01 and PrusaSlicer 2.9.6 were found and their command-line tools ran. Blender 5.2.1 is available for rendering. No extra paid software is required.

To regenerate on this computer:

```powershell
& 'C:\Program Files\FreeCAD 1.1\bin\python.exe' 'C:\Users\soham\Documents\CS 362\GP\enclosure-design\revision-04\build_revision04.py'
```

Older enclosure revisions and presentation materials have not been overwritten. Nothing has been submitted to UIC or sent for printing.
