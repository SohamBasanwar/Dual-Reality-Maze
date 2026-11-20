# Revision 10 — print and assembly guide

29 October 2026. Millimetres throughout. This is a digitally reviewed prototype, not a physical-fit or print certification. Open `index.html` for the illustrated instructions.

## What is adjustable

The Arduino and breadboard use a fixed datum corner, two captured sliding jaws and removable cross keys. Their mounting holes are not used. The joystick and LCD have the same mechanism inside replaceable carriers. Length and breadth positions are indexed 3 mm apart; a complete cross-key passage identifies a permitted locking position.

The two handheld base mounts permit −3 / 0 / +3 mm length adjustment and −3 / 0 mm breadth adjustment. Their nominal breadth is the maximum because the battery bay and adjacent board occupy the remaining space. Main and the joystick/LCD carriers permit −3 / 0 / +3 mm on both axes. The + arrow means “larger opening,” up to that mount's stated limit. It does not promise that an oversized device or different connector layout will fit.

Each carrier uses one keyed height frame: 0.6, 1.2 (default) or 1.8 mm. The thicker frame raises the underside of a thinner device; a thinner frame accommodates a thicker device under the unchanged top retaining lips. These are alternatives, not stackable layers. The nominal board bottom in the base is Z=9.2 mm. The LCD and joystick retain their original nominal PCB heights and control-opening alignment.

Use thin nonconductive fit pads for small differences between indexed settings if necessary. Do not put pads against chips, solder joints, contacts or antennas. Do not squeeze a PCB to eliminate a large mismatch. A different shaft offset, header placement or LCD glass position still requires a suitable adapter or source change.

## Mounting sequence

1. Open the large lid and disconnect power. Fit the chosen height frame into its locating pockets.
2. Withdraw the cross keys sideways using their accessible handles. Open the jaws enough to insert the component; an unlocked insertion position is not automatically a permitted locked size.
3. Seat the device against the fixed corner and under its retaining lips. Slide the two jaws to the appropriate indexed positions. Check safe contact at the edges and free connector access.
4. Fully insert both keys. Their split tips provide a prototype retaining detent. Confirm that the keys cannot back out under normal handling and that each jaw resists movement without crushing the component.
5. Check the joystick's complete tilt/click, the LCD window alignment, cable bend space and lid closure. Route jumpers below the indicated clearance limits.

The optical pod, potentiometer centre, RGB cups, buzzer outlet and battery bay retain dedicated fixed locations. Their keepers remain removable; they are not universal XYZ stages. The photoresistor dome opens with a quarter turn and lift. Use an opaque seal around its two leads if light leaks from the interior. Test the thin roof, or use the clear-film option.

## Gate installation

Seat the keyed servo liner in the recessed cassette floor, place the servo and latch the removable bridge. Select one of the width inserts if needed; the illustrated nominal servo body is 23 mm wide. The alternative liners change the accepted body width by approximately ±0.6 mm while retaining its centre. Verify actual mounting ears and output-shaft location. An unknown servo variant is not proven compatible by body width alone.

Use the servo's supplied nylon horn. Install the cassette and gate frame into their lid receivers, then feed the gate panel into the open guide rails. Align the horn hole and panel slot; fit the headed drive pin and rear keeper. The frame's bridge provides axial horn retention with running clearance. Attach the removable guard last; its top closes the rail ends.

The nominal crank radius is 7 mm; the modeled −60° to +60° motion produces about 12.12 mm lift. Set conservative powered endpoints first and enlarge them only after checking the real mechanism. Verify the tiny pin, keeper, horn retention and pinch protection. The actual servo needs its properly regulated supply; the reserved power-module block is not an electrical design or an installed part.

## Breadboard pushbutton

The Architect cap operates a switch seated on the breadboard through a guided stem and a replaceable contact shoe. The switch's spring returns the cap. The shoe has split snap tabs; remove the guide, then pinch those tabs through the stem release windows to detach the shoe. With the nominal 10 mm breadboard and 7.3 mm switch height, the rest tip is at Z=26.65 mm, leaving a 0.15 mm gap and a nominal 0.45 mm cap stroke. Alternative tips change reach by ±0.6 mm. Actual installed switch height, travel and retention must be checked; never leave the switch preloaded. A measured height outside this range needs a regenerated shoe, not a forced fit.

## Print these first

The `fit-tests` folder contains the actual rail fixture crop, jaw and key. Test those three before printing full enclosures. The coupon is not a spare assembly component. Verify free travel, key insertion/removal, detent retention and tolerance in the filament and printer that will make the final parts.

The `prototype-stl` folder contains the separate installed assembly pieces. Several pieces can share a build plate; each STL does not require its own print job. `adjustment-options` contains alternative inserts/tips, and `optical-options` contains alternative dome roofs. Print one selected alternative for each location, not all of them for the finished assembly.

Start shells with the open side upward and inspect the curved grips, side latches and shutter overhangs in PrusaSlicer. Use selective supports only where needed and keep support material out of blind tracks and small key passages. Print height inserts flat. Orient sliding jaws and keys on a stable broad face; place flexure bending within layers where possible. Inspect thin split tips and the gate pin/keeper carefully. Carrier and gate undercuts may need local supports; support removal must remain accessible.

The structural parts may use one filament colour. The RGB diffuser and optional clear optical window must transmit light; they may be separate translucent prints or cut sheet inserts. The gallery's reference colours do not imply multiple structural print colours.

FreeCAD, PrusaSlicer and the installed Python/Blender build tools are sufficient. No new software, G-code, print-service form or paid manufacturing order is required by this revision. Check the selected UIC printer's bed and support policy with the operator before the full-size shells.

## Scope of verification

The final reports distinguish valid CAD solids, watertight meshes, nominal component clearances, permitted indexed sizes and moving-gate/shutter checks. They do not establish spring strength, friction, wear, light transmission, battery runtime, firmware operation or physical fit. Do the small coupon and one full enclosure first.
