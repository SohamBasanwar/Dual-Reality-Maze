# Dual-Reality Maze — Revision 06

**Design-review prototype, 25 October 2026. Not a final print release.**

Open `index.html` for actual CAD views, colour alternatives and the gate-motion explanation. Earlier revisions remain unchanged.

## Changes

- Explorer and Architect now use tapered oval grip cross-sections, inspired by the wraparound grip surfaces of the Xbox controller. The large breadboard and PP3 battery still dictate a larger enclosure; this is not an Xbox-sized shell or a proven ergonomic fit.
- One rear sliding I2C hatch on each controller. Main has one sliding I2C hatch on each side, plus its separate rear USB hatch for the R3/USB fallback.
- The I2C openings are nominally 18 × 12 mm with 21 mm shutter travel. Main USB remains 30 × 20 mm with 35 mm travel. Park a shutter fully open while the cable is connected. The shutter does not clamp or seal a cable.
- Replaceable push-in UNO edge clips, separate joystick/LCD carriers, captive button cassettes, and retainers for the light sensor, potentiometer, buzzer and RGB LEDs.
- The reveal sensor is now above the case roof, inside a raised removable half-dome at the centre of the face, below the RGB emblem and above the front cut-out. Its opaque floor has two individual lead passages. The default 0.4 mm printed roof is an optical test; alternative 0.6/0.8 mm roofs and a clear-film frame are included.
- Gate frame and servo cassette have separate snap feet. A frame-mounted bridge captures the supplied servo horn axially. A headed pin and C keeper drive a slotted vertical gate.

## What “adjustable” means here

The unmeasured joystick/LCD/servo interfaces remain **parameter-adjustable and replaceable prototype parts**. They are not universal self-adjusting mounts and do not guarantee a fit with every clone board. The source contains each carrier's nominal width, depth, clip positions and clearances. Change the carrier rather than redesigning the enclosure once actual measurements are available.

No imaginary hole coordinates have been drilled into the design. A locating pin prevents sideways motion but requires a head, clip or cap to prevent lift. Hole-based inserts can be substituted after the actual hole diameter, spacing and nearby component clearances are measured. Do not put locating pins into electrical breadboard sockets or solder pads.

## Retention status

| Component | Current mechanical provision | Still to verify |
|---|---|---|
| Full-size breadboard, all three | Perimeter tray and four retaining fingers | Actual 166 × 55 × 10 mm assumption, adhesive backing thickness, rail features |
| UNO R3 / Main R3-or-R4 | Edge cradle and two replaceable push-in edge clips | PCB outline and components near the clip contacts; print fit |
| Joystick PCB | Separate edge carrier with blind snap receivers | Actual PCB size, mounting holes, joystick tilt envelope and edge clearance |
| Bare photoresistor | Raised half-dome, opaque floor, edge seat, two lead passages; removable quarter-turn hood | Disc diameter, thickness, 2.54 mm provisional lead spacing, optical transmission and light seals |
| Potentiometer | Body cup and lower bayonet keeper | Terminal clearance and exact antirotation tab/flat; torque restraint is not yet proven |
| Pushbutton | Flanged guided cap, cassette and lower snap ledges | Switch height, travel, pin layout and return action |
| SG90 | Sideways cassette, body lips and snap feet | Actual body/ear/shaft dimensions and insertion flex |
| Gate / horn | Rail-guided portcullis, frame feet, horn retaining bridge, headed pin + C keeper | Actual supplied horn, hole radius, spline seating, tiny pin/keeper durability; decorative guard fit |
| LCD + backpack | Separate edge carrier, viewing window and backpack reservation | Actual board/window/hole pattern, backpack height and connector direction |
| Buzzer | Cylindrical seat and lower bayonet keeper | Actual diameter, body height and wire exit |
| RGB LED, all three | Flange seat and quarter-turn keeper | Actual LED package, lead clearance and diffuser attachment |
| PP3 battery | Separate bay, upper stop and toy-style underside door | Selected cell, snap connector and cable bend |
| Optional ESP32 / power board | Reserved volumes | Boards not selected; fixed mounts and RF/power validation remain open |

All specified retention parts are screwless. Digital non-interference does **not** demonstrate zero movement, adequate clamping force, latch life or safe loaded gate operation. Those require fit coupons and a physical assembly.

## Gate mechanism

The gate is a **vertical portcullis**, not a directly hinged door. The SG90 lies on its side. Its supplied nylon horn engages the original servo spline. A pin nominally 7 mm from the shaft runs through a horizontal slot in the gate crossbar. The frame rails constrain the gate to vertical movement; the slot accommodates the sideways part of the crank motion.

The proposed −60° to +60° crank sweep produces approximately **12.1 mm of lift**. This is a kinematic design value, not permission to drive an uncalibrated servo to those limits. Centre the servo first, install the horn, and slowly establish actual endpoints without forcing the gate against a stop. Use regulated servo power and common signal ground as appropriate to the final circuit; no runtime or power test has been performed here.

The frame bridge sits in front of the horn hub with nominal running clearance so the horn cannot simply slide off. The headed drive pin is kept from backing out by a small C keeper behind the horn. Both interfaces are provisional because the exact horn is unmeasured. A suitably sized **nylon push-rivet** can replace the tiny printed pin/keeper without introducing screws. Do not substitute a fabricated spline or rely only on friction to retain the horn.

## Cable routing

Bundle SDA, SCL and common GND in a soft sleeve. Use a reusable silicone band on the internal cleat for strain relief; do not crush individual wires or Dupont housings. Leave a short service loop inside. A 30 cm jumper's length includes its internal routing, so the usable distance between enclosures will be less than 30 cm. Confirm the actual setup spacing before cutting or buying cables.

The side labels refer to the assembled CAD. Source geometry is mirrored during export. Do not infer pin numbering from a mechanical rendering. Keep each local battery supply separate unless a reviewed power circuit intentionally connects them.

## Reveal dome and optical test

The new location requires a deliberate centre-face reach. It is away from the joystick, rear cable exit and both grips. The photoresistor sits above a solid opaque floor, so there is no open chamber leading down to the RGB LED or breadboard. Two nominal 1 mm lead bores run through the floor and underside guide tubes, with provisional 2.54 mm spacing. Measure the actual leads and use snug opaque sleeves or a removable opaque seal if light enters around them.

The default raised hood has a **0.4 mm printed membrane** over its small upper opening. `optical-options/` contains complete interchangeable hoods with 0.4, 0.6 and 0.8 mm membranes, plus a hood with a recessed seat for a clear disc. Thin filament is not automatically translucent: dark graphite/black can block too much light even at a small thickness. Test the actual material before committing to it.

For the clear-film version, cut a nominal **7.2 mm diameter, 0.2–0.3 mm thick** clear PET/acetate disc and secure its perimeter on the internal ledge with a thin adhesive ring. Keep adhesive outside the optical opening. The structural enclosure can still be one colour. The roof variants are alternatives, not parts to install together.

Test in the intended room: record the uncovered and finger-covered readings, then repeat while cycling the RGB LED through red, green, blue and mixed colours. The covered state should remain below the calibrated reveal threshold across those changes. Check incidental hand shadows as well. There is no claim of optical isolation until that test passes; no firmware thresholds were changed in this CAD revision.

## One structural colour

Recommended: **charcoal / graphite grey**. Other previews: stone grey, dark forest green, muted bronze. These are appearance comparisons, not confirmations of UIC filament stock. Raised/engraved details use the same material; no painting is required. RGB light needs a separate clear/translucent insert or open light window—opaque shell material will not glow through itself.

Choose a structural material and print settings with the Makerspace, especially for repeatedly flexed clips. Do not choose a brittle or metal-filled decorative filament solely for its colour. A material coupon is required even when the nominal CAD gap is correct.

## Files and tools

- `cad/*.FCStd`: native FreeCAD solid assemblies; geometry is regenerated from the Python source, not a constrained sketch feature history.
- `cad/*-printed-parts.step`: interchangeable solid parts.
- `prototype-stl/`: individual prototype meshes; placement is the assembled coordinate system. Arrange/orient parts in the slicer.
- `fit-tests/`: small samples extracted from this revision.
- `build_revision06.py`: dimensional master. Run with FreeCAD 1.1's bundled Python.
- `render_revision06.py`: Blender renders of actual exported CAD; no illustrative geometry substitutions.
- `CAD_VALIDATION.json`, `ASSEMBLY_REVIEW.json`, `MESH_VALIDATION.json`: digital checks and explicit limitations.

FreeCAD, PrusaSlicer and OpenSCAD are already installed. No additional user installation is required for reviewing these files. No form or print job has been submitted.

## Reference sources

- Xbox controller geometry / official product gallery: https://www.xbox.com/en-US/accessories/controllers/xbox-wireless-controller
- SG90 manufacturer reference (clones may differ): https://towerpro.com.tw/product/sg90-analog/
- UNO R3 reference: https://docs.arduino.cc/resources/datasheets/A000066-datasheet.pdf
- UNO R4 WiFi reference: https://docs.arduino.cc/resources/datasheets/ABX00087-datasheet.pdf
- Colour/material examples, not Makerspace inventory: https://prusament.com/materials/pla/
- UIC service references: https://etl.ed.uic.edu/services/3d-printing/ and https://project.mksp.uic.edu/auth/login
