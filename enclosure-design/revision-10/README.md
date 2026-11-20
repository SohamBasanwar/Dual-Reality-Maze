# Dual-Reality Maze — Revision 10

Open `index.html` for the illustrated guide. Everything works locally after extracting the ZIP. The guide includes all three cases, eight viewing modes per case, adjustable board carriers, gate installation and motion, and renders of the engraved CAD geometry.

These are prototype CAD files. Physical fit, flexure durability, optical transmission and powered operation have not been tested. Use the small rail/jaw/key coupons before full-size prints.

## Files

- `cad`: three native FreeCAD documents and matching STEP assemblies. Native documents contain individually named editable solids; regenerate dimensions with the Python sources.
- `prototype-stl`: separate installed printed pieces in millimetres, in their assembly positions. Arrange and orient these in PrusaSlicer.
- `adjustment-options`: alternate height inserts, servo-width liners and button-reach tips. Each replaces its nominal part.
- `fit-tests`: three small rail/jaw/key samples to test together first.
- `optical-options`: alternative photoresistor roofs. Test transmission and ambient-light response in the actual filament.
- `PRINT_AND_ASSEMBLY.md`: assembly sequence, adjustment limits and print-orientation guidance.
- `PARTS.csv`: installed printed-piece quantities and filenames.
- `REVIEW_VALIDATION.json`: consolidated digital-check results and limits.

The source of the outer form remains the earlier sculpted controller design. Revision 10 changes the board mounting system while retaining the contoured battery covers, removable optical dome, gate and cable shutters. Breadboard and Arduino mounts in handhelds have −3/0/+3 mm length and −3/0 mm breadth settings. Main, joystick and LCD carriers have −3/0/+3 mm on both axes. Height inserts are 0.6, 1.2 or 1.8 mm; use one only.

The source uses FreeCAD's Python environment. OpenSCAD is not required for this revision. Blender scripts generate the visual guide from exported meshes. No additional software purchase is needed.

Electronic shapes and power/ESP32 reservations are reference envelopes, not printed parts. The ESP32 model, power module and actual component dimensions remain to be confirmed. Body-size adjustment cannot compensate for every possible connector, mounting-tab or shaft-offset difference.

Soham Basanwar is engraved where space permits; smaller suitable parts use SB. Thin, optical and fit-sensitive pieces may have no physical lettering. All assembly-part filenames carry Soham Basanwar.
