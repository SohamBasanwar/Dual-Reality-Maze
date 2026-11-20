# Revision 04 — setup before modelling

Prepared 23 October 2026. This is a preflight guide, not a finished CAD revision.

## Software

- FreeCAD: recommended mechanical authoring tool for dimensioned solids, editable FCStd models and STEP/STL exports. Download the current stable Windows x86_64 installer from https://www.freecad.org/downloads.php . Use default installation options; no additional workbenches are required initially. Open it once and use millimetres for this project. Avoid weekly/development builds for the primary project.
- OpenSCAD: existing editable models are in `../ergonomic-v2/cad/ergonomic_enclosures.scad`. A portable runtime is already included at `../build/openscad-portable/openscad-2021.01/`. A separate install is optional; official downloads: https://openscad.org/downloads.html . It remains useful for reviewing the existing parameterized geometry. An STL-to-STEP conversion is not a substitute for editable mechanical solids.
- Blender: installation folders for 4.4 and 5.2 were found. Use for sculptural details, materials and presentation renders; retain dimensioned mounting geometry in the mechanical CAD source.
- PrusaSlicer: optional print preview, support and orientation review. https://www.prusa3d.com/p/prusaslicer/ . Select a printer/material profile only after the printing facility confirms the actual machine. Generic previews do not establish fit, print time, strength or final manufacturing settings.
- No separate Python, Node, paid CAD subscription or add-on is required from the user for this preflight. Existing project scripts/runtimes can be used for supporting work.

## Design requirements captured

Three matching fantasy devices: two handheld controllers with rounded textured grips; one stable, sculpted desktop altar. Keep the reference image's overall visual direction, not its unverified interior arrangement or illustrated battery selection.

Screwless means exterior AND component retention: board edge cradles with removable locking bars, breadboard trays with stops, joystick carrier, servo cartridge, captured LCD bezel, cable strain relief and serviceable lid locks. The servo horn/linkage needs a positive captive keeper and a physical trial; a friction-fit horn alone is not a verified solution.

Architect: raised upper-shoulder gate opposite the potentiometer, concealed SG90 body, protected movement, removable linkage. Explorer: accessible joystick and light sensor. Main: angled LCD, buzzer openings and a real power-control actuator within the central emblem.

Each emblem includes a concealed multicolor indicator, light cavity and diffuser. Proposed blue/green/amber/red/purple status colors should also use blink patterns so color is not the only signal. Select the exact LED/module before defining its pocket, driver and current limit. A diffuser may require a separate translucent insert even when all structural parts use one filament.

Preserve wired I2C, common ground and Main's built-in Wi-Fi link to the laptop. No external radio compartments.

## Information needed before critical dimensions

Provide top, bottom and side photos of actual boards/modules next to a ruler, plus markings or product links. Measure body/PCB length, width, total height, mounting tabs, connector projections and plug bend room. Priority: all full-size breadboards, joystick, potentiometer/knob, pushbutton, SG90 plus horns, LCD plus I2C backpack, light sensor, buzzer, cables/connectors, RGB indicator and power switch/module.

The new brief mentions rectangular 9V batteries; the previous accepted plan used USB and regulated 5V. Resolve this before designing a fixed power compartment. Battery suitability requires a current budget, regulation losses, runtime target and servo peak-load assessment. The master button requires a real switched power path; switching SDA/SCL or sending a software command does not remove power. Independent USB supplies cannot all be cut off by a simple switch in Main.

## Fabrication checks

Split the geometry into printable shell halves and removable detail parts. Determine supports from actual overhangs and print orientation, not from the concept image alone. Keep support-contact surfaces away from grip faces and mating/locking surfaces where practical. Print small latch, cradle and horn-keeper fit samples before the complete shells.

UIC Engineering Makerspace lists multiple printer types: https://makerspace.uic.edu/learn/tools/ . Confirm the assigned printer, build volume, filament and staff's preferred submission settings before final export.

The separately linked Education Technology Services page specifies STL, single-color printing and College of Education eligibility/director preapproval: https://etl.ed.uic.edu/services/3d-printing/ . This is a different service from Engineering Makerspace. No form is being filled or submitted.

## Revision sequence

1. Identify actual components and resolve power architecture.
2. Fit component envelopes and wire paths inside an ergonomic silhouette.
3. Model screwless retention and removable mechanism parts.
4. Add story-based relief artwork, light cavities and diffusers.
5. Check collisions, service access, gate sweep, print orientation and test coupons.
6. Deliver editable source, appropriate STEP/STL exports, assembled/internal/exploded views, assembly guide and unresolved physical-verification list.

Existing revision 2 remains a design study. Revision 04 geometry has not been created during this preflight.
