# Dual-Reality Maze — Revision 09

26 October 2026. Design-review prototype, pending real component and printed-fit tests.

## Mounting audit and corrections

Read [MOUNTING_AUDIT.md](MOUNTING_AUDIT.md) for the per-component attachment and installation steps. Revision 09 adds a long Architect button stem to reach the breadboard switch, a removable guide/stop, and a separate snap-in servo retaining bridge. The LCD reference stack and carrier have been corrected. The sensor dome is removable by quarter turn and lift.

The review page includes empty and populated underside views of every lid, component close-ups, and final printed-part sheets. There are 50 assembly parts: 9 full-name, 12 SB, 29 physically unmarked. No fixed PCB-hole pins are assumed. Use the replaceable edge carriers until real mounting holes are confirmed. The orange block is an unselected power-module reservation, not a part to print.

See [PRINT_PLAN.csv](PRINT_PLAN.csv) for suggested orientations/supports. There are 21 actual-part fit samples and four optical variants (alternatives, not four additional installed domes). Physical testing is still required. FreeCAD and PrusaSlicer are sufficient; no additional application is needed.

## Castle gate, at a smaller scale

This revision restores the original arched portcullis, visible bars and lifting action. The mechanism is recessed 21 mm into the upper shoulder. The original guard mesh reaches Z = 118 mm above the assembly datum; the new guard reaches Z = 98 mm, including its new three-tooth crown. With the nominal lid at Z = 58 mm, the visible heights are **60 mm and 40 mm** respectively. The external guard footprint remains approximately 50 × 48 mm. This preserves the gate's appearance while concealing the servo body and lower drive.

The servo is sideways inside the controller. Its original nylon horn engages its actual spline. A 7 mm-radius captive pin in that horn slides in a horizontal slot in the gate's lower yoke. Turning through the nominal −60° to +60° crank range lifts the gate by about 12.12 mm. Two side rails guide the gate. The visible bars start above the case sill; two narrow guides connect them to the concealed yoke. The guard closes the upper travel pocket. The frame's bridge captures the horn hub axially, and a headed pin with a C keeper couples it to the yoke.

The mounting collar hangs below the lid and uses two connecting webs outside the drive path. Servo cartridge, frame and guard remain separate parts. The guarded roof opening allows the concealed drive to move without hitting the lid. This is a screwless prototype arrangement: the exact supplied horn, tiny pin/keeper, latch flex, gate load and full powered travel remain unverified. No invented printed servo spline is used.

The rotating-window alternative remains in Revision 07. It has not been substituted here. This revision uses the earlier castle-gate vocabulary and the same physical lifting principle. [TowerPro's SG90 data](https://towerpro.com.tw/product/sg90-analog/) gives the general servo family dimensions; it does not establish a fit for an unmeasured clone or its horn.

## Battery-cover correction

The added service pad from Revision 07 has been removed. A broader flare made that area bulkier, which was the wrong direction for hand comfort.

The handheld door is now cut from the original unpadded oval outer shell, using a second copy shifted 2.4 mm upward to define a contoured skin. The resulting door follows the grip and sits 0.15 mm inward from it. The receiver follows the same surface with 0.2 mm nominal vertical clearance. The two leading tabs and release catch retain their positions. Internal bay walls and rails are clipped to the original outer envelope so they cannot create another external pad.

The battery body, connector and wiring reservations remain. The name is engraved inside the door's leading flat area. `BATTERY_PROFILE_REVIEW.json` measures added volume outside the original grip around the access region, rather than relying only on a render. Physical grip feel and repeated latch cycling are still required.

## Personalization and preserved components

Large shells and battery doors carry “Soham Basanwar”. Suitable small components carry “SB”, including shutter finger tabs, button caps, switch cassettes and selected gate parts. Tiny keepers, thin optical parts and functional guard surfaces remain unmarked where lettering would reduce strength or fit. All printed-part STL filenames, CAD labels and `PARTS.csv` entries include the full name.

- Explorer: joystick, isolated raised photoresistor dome with two lead passages, RGB emblem.
- Architect: potentiometer, pushbutton, SG90 and castle gate, RGB emblem.
- Main: LCD/backpack, buzzer, power actuator, RGB emblem and provisional universal UNO cradle.
- All three: full-size breadboard reservation, PP3 battery space, screwless carriers and provisional ESP32/jumper space.
- Controller rear I2C shutters, Main side I2C shutters and Main rear USB shutter remain. Openings are intended for short wired links and the R3/USB fallback.

Exact component dimensions, mounting holes, material, printer clearances, servo power, optical transmission and one-hour battery runtime remain to be verified. Adjustable carriers are editable/replaceable parts, not universal self-adjusting mounts.

## Review files

Open `index.html` for the actual CAD views and open/closed comparison. Native FreeCAD and STEP assemblies are in `cad/`; individual meshes are in `prototype-stl/`. Use the actual cropped grip/door and carrier samples in `fit-tests/` before printing a full set. Validation reports state only tests that have run.

FreeCAD and PrusaSlicer are already installed. No additional software is required for inspection and slicing. No UIC print form or machine-specific G-code has been submitted.
