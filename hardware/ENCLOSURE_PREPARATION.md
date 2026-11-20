# Screwless enclosure preparation

**Superseded planning record.** The user has now confirmed USB power for all boards, wired I²C and Main-to-laptop built-in Wi-Fi. Engineering Makerspace in RRB and handheld gamepad grips are confirmed. No battery compartments are included. Use `CURRENT_HARDWARE_ARCHITECTURE.md` and `../enclosure-design/DESIGN_PLAN.md` for the current design, measurements and assets. The older preparation notes below remain as history only.

The presentation, written milestone document and trailer are complete in `submission/`. This is the next-phase requirements brief. No CAD, STL or print submission has started. The confirmed scope is one Main Uno R4 WiFi box and two Uno R3 controller housings. Professor permission is already provided.

## UIC rules checked October 22, 2026

For the **Engineering Makerspace Digital Fabrication Lab**:

- Staff operate the printers. Submit STL in millimeters. Accepted alternatives include 3MF, OBJ and limited STEP. Closed meshes must avoid self-intersections. Native CAD and slicer project files are not printable submissions.
- Voron Trident lists a 290×290×285 mm machine envelope, 0.6 mm nozzle, 0.3 mm layers, 20% gyroid infill and roughly 2 mm minimum features, depending on geometry. Actual usable size depends on the part and orientation.
- Its assembly guidance recommends 0.5 mm horizontal and 1.0 mm vertical separation. Internal geometry should avoid supports and use no more than 45° overhang walls. Parts need bed contact and access for support removal.
- PLA is recommended for initial prototypes. Color is single-material. Availability can change.

Source: [Digital Fabrication Lab](https://makerspace.uic.edu/make/digital-fabrication-lab/).

The submission system accepts multiple files. Include rough dimensions so staff can check units. Projects needing edits are dropped after seven days without resubmission. Source: [Project Submission](https://makerspace.uic.edu/make/digital-fabrication-lab/project-submission/).

These rules apply to Engineering Makerspace. Confirm the intended facility before selecting a printer. No new professor approval is needed.

## Design approach after component confirmation

Use a removable internal tray with rails that support the PCB edges and leave the underside clear. Retention clips should touch safe board areas and leave headers, solder joints and connectors free. Capture breadboards in measured pockets. Provide separate wire channels and retain cables near enclosure exits so pulling a cable does not pull a jumper from a header. The joystick cap, knob and button need clearance through their full travel.

Use an accessible battery compartment with a screwless door, room for the battery clip and wire bend, and protection against terminal contact with exposed circuitry. Confirm servo load and regulation before choosing the internal power layout. The power switch opening must match the actual switch body and retention tabs.

A sliding lid with a releasable latch is a candidate for frequent access. Each joint needs its own clearance test. Do not uniformly scale a finished case to fix a tight lid: scaling would also change board locations and connector openings. Parameters should control the component pockets, wall thickness, fit allowances and wire space independently.

Snap features depend on material, geometry and print direction. Small local test pieces should establish a working fit before printing full housings. Design references: [Prusa modeling guidance](https://help.prusa3d.com/article/modeling-with-3d-printing-in-mind_164135) and [Formlabs enclosure and snap-fit guidance](https://formlabs.com/global/blog/designing-3d-printed-snap-fit-enclosures/). These are general design references, not substitutes for UIC’s printer settings.

## Measurements needed

Fill `ENCLOSURE_MEASUREMENTS.csv` in millimeters. Model numbers or product links can establish nominal dimensions, but compare them with the actual modules, especially clone boards and breadboards. Measure total assembled height, including headers, USB/barrel connectors, servo horn, knobs and wires. Record connector locations relative to one consistent board corner. Keep the installed battery clip and intended cable plugged in while measuring their occupied space.

Pending decisions: exact facility, controller shape, Main power source, module and breadboard sizes, switch type, battery format/clip and final cable exits. Controller power is planned as 9V batteries. Do not invent these dimensions to produce a nominally printable model.

## Later output and verification plan

After the brief is answered: create adjustable source CAD, a small fit coupon, separate base/lid/battery-door STLs for three housings, assembly drawings and a dimensional manifest. Check watertight meshes, physical clearances, module retention, full control travel, cable access, lid release and battery replacement. Record exact part dimensions in the print request. Staff will choose final print settings and orientation.
