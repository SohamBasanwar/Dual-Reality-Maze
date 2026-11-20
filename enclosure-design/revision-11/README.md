# Dual-Reality Maze — Revision 11

Open index.html for the full local visual guide. Revision 10 is preserved separately.

This revision adds four green rune windows on Main, four enclosed LED feed wells over the breadboard, captured translucent diffusers, screwless bezels, and an additional opaque RGB shield. The green LEDs fade together; the central RGB status light stays independent. The supplied pictures illustrate the intended appearance, not measured light distribution.

There are 95 installed printed pieces. 25 have physically engraved assembly codes; the remainder use matching bag/tray codes. Existing Soham Basanwar / SB marks are retained. The code at the start of each installed-part STL filename matches its image card and sorting label.

## Open these first

- index.html — the three enclosures, lighting preview, adjustment views, gate instructions, engraving close-ups and illustrated part lookup.
- PART_LABELS.html — printable sorting labels for the installed set.
- PARTS.csv / ASSEMBLY_IDS.json — part codes, filenames and physical mark status.
- R11_PRINT_NOTES.md — new light parts, optical test piece, print orientation, support access and installation.
- PRINT_AND_ASSEMBLY.md — retained instructions for the existing mechanisms.
- lighting/README.md — LED driver, current limits and fade integration notes.
- REVIEW_VALIDATION.json — digital check scope and remaining physical tests.

## CAD and printing

cad contains three FreeCAD documents and STEP assemblies. prototype-stl contains one file per installed printed piece, in millimetres at assembly coordinates. Import individual files into PrusaSlicer, orient them for printing and place them on the bed. Do not print an assembled CAD model as one object. adjustment-options contains substitutions, not additional layers or required duplicate parts. optical-options contains existing Explorer sensor-roof experiments.

Print the small rail/jaw/key coupons and the new G1 lighting coupon before full-size shells. Use the G1 bezel and diffuser with that lighting coupon. Test real components and filament. The structural parts may be bronze, but the optical lenses must transmit light.

The code is in lighting/BreathingAccent.h. It passes a host-side C++ timing test, but has not been integrated into the game firmware, assigned a confirmed spare pin or flashed. No new software purchase is required.

## Source and limitations

build_revision11.py uses the corrected native Revision 10 shapes in baseline, then adds the new geometry and assembly labels. Run refine_r11.py afterwards to create the test coupon and complete the safe-face labels. build_revision10.py supplies geometry helper functions; do not run it in place of the R11 builder because the baseline includes later R10 fit corrections. FreeCAD's bundled Python runs the CAD tools; Blender generates the illustrated views from the actual exported meshes.

Physical component dimensions, clip retention, print strength, optical uniformity, unwanted light leakage, power wiring, battery runtime and powered game operation are not verified. Nominal digital fit is not a physical-fit certification. The ESP32 is still a provisional space, and body adjustment does not establish every connector or header-pitch compatibility.
