# Revision 12 additions — print and assemble

Revision 10's controller shape, contoured battery doors, adjustable carriers, gate and cable shutters are retained. Revision 12 adds four green light sections to Main, an RGB isolation cap, shallow assembly IDs on suitable parts, and sorting codes for the entire installed set.

## Start small

Print `fit-tests/M-lighting-G1-coupon-Soham-Basanwar.stl` with Main's G1 bezel and G1 diffuser. This cropped sample retains the real well, slot and bezel receivers; a disconnected fragment of an unrelated original rear lid tab is omitted from the sample. Use one actual LED and its resistor. Check brightness, distribution, opaque wall leakage, lens fit, clip release and lead clearance before printing Main's complete lid.

The 0.8 mm diffuser is a prototype thickness. Use translucent/frosted material; a matching opaque bronze print will generally not work as a diffuser. Check the actual material. Optical lenses can alternatively be fabricated from suitable sheet only after matching their shape and retention thickness. They are not generic rectangles.

## Orientations and supports

- Main lid: inspect with the external top face towards the bed; remove all separate bezels and electronics before slicing. Protect the thin decorative edges. The sculpted exterior and RGB cup may need local supports. Its large open emblem aperture allows access before the diffuser and mask are fitted.
- Green optical galleries: exclude supports from the narrow internal channels and LED feed wells, where they could become trapped or block light. The short internal spans must bridge acceptably in the chosen material; test the coupon. A slicer preview, not the CAD rendering, determines whether this orientation works on the selected printer.
- Bezels: begin with their broad exterior face towards the bed, snap legs upward. Inspect the small hook overhangs and lettering in the layer preview. These clips need a physical flex/release test. A brittle filament may need a revised clip or different process.
- Green diffusers: print flat, without supports, using translucent material. Check thickness and flatness before clipping them in.
- RGB isolation cap: start with the outer bottom face on the bed. Avoid trapped supports between its internal baffles; inspect the small bridge spans and wire passages in the preview. Test one cap before final assembly.
- Existing controller parts retain the Revision 10 orientation guidance in PRINT_AND_ASSEMBLY.md. Do not place a complete assembled case on the print bed as one object.

Each STL is a separate part, exported in millimetres at its assembly coordinates. Import, separate, orient, and place each chosen part on the bed in PrusaSlicer. A build plate may hold several parts, but they remain separate items. No printer-specific G-code or slicer profile is supplied because the actual printer/nozzle/material settings have not been confirmed.

## Assembly identification

Use the code at the start of each installed-part filename: E for Explorer, A for Architect and M for Main. Physically engraved codes are shallow cuts on selected noncontact faces. The guide says exactly which pieces carry a code and which use a coded bag or tray. Existing owner marks are retained. The four Main bezel receiver areas carry their matching bezel codes.

Print PART_LABELS.html, or use a labelled compartment box. Sort immediately after removing parts from a build plate. Keep each enclosure in its own tray, and keep alternative inserts separate from the nominal assembly parts. Similar looking pieces are not automatically interchangeable.

## Main lighting installation

1. Assemble the Main board, breadboard and existing controls. The provisional 60 x 32 x 18 mm ESP32 space moves to x=100…160, y=24…56, z=19.2…37.2 mm. Its model, headers and power supply remain unselected.
2. Position G1–G4 LEDs at their nominal x/y targets, above the breadboard. The LED body references span z=24.2…30.2 mm. Actual breadboard rows, lead bends and your chosen LED determine final placement. The roof wells stay fixed when adjusting the breadboard jaws.
3. Put each lens over its roof slot. Match its outline to the corresponding bezel, then press in the bezel. Release the two hooks from inside for service. Avoid pressing on the thin lens.
4. Fit the central RGB LED and its original keeper. Add a flexible wire extension and route it through the new cap's offset passages. Rotate the cap into its captured position. Disconnect the wire extension before rotating the cap for removal; never twist the LED legs.
5. Route wiring away from light wells, moving keys and latches. Close the lid gently with power off. No board, LED, connector or cable should be forced into position.
6. Use the separate wiring notes and test green-only, RGB-only and both together. Use an opaque lining if the printed shell transmits light. These are geometric barriers, not a measured optical isolation specification.

The breathing helper is supplied separately. It has not been integrated into the game firmware, assigned a confirmed spare pin or uploaded. Its software checks do not validate the actual electrical circuit.

The two rear light galleries have raised floors at z=54 mm to clear the LCD key's withdrawal path (key top z=53.2 mm). This leaves 0.8 mm nominal clearance; keep wiring and print debris out of that service path.


Revision 12: exterior owner and assembly text is concealed; consult PRINT_BRIEF.md and the current material plan.
