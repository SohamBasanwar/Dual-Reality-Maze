from pathlib import Path
import json
R=Path(__file__).resolve().parent
p=json.loads((R/'dimensions.json').read_text());p.update(revision=11,finish='Bronze structural polymer; separate translucent optical parts. Actual filament and printing settings require testing.',main_green_led_count=4,main_rgb_isolation='Closed original cup side exit, secondary opaque cylinder and removable cap with offset wire passages.',main_green_light_well_inner_diameter_mm=11,main_green_light_well_bottom_z_mm=22.8,main_green_diffuser_thickness_mm=.8,main_esp32_reservation_origin_xyz_mm=[100,24,19.2])
(R/'dimensions.json').write_text(json.dumps(p,indent=2))
ids=json.loads((R/'ASSEMBLY_IDS.json').read_text());marked=sum(i['location'] is not None for i in ids)
(R/'README.md').write_text(f'''# Dual-Reality Maze — Revision 11

Open index.html for the full local visual guide. Revision 10 is preserved separately.

This revision adds four green rune windows on Main, four enclosed LED feed wells over the breadboard, captured translucent diffusers, screwless bezels, and an additional opaque RGB shield. The green LEDs fade together; the central RGB status light stays independent. The supplied pictures illustrate the intended appearance, not measured light distribution.

There are {len(ids)} installed printed pieces. {marked} have physically engraved assembly codes; the remainder use matching bag/tray codes. Existing Soham Basanwar / SB marks are retained. The code at the start of each installed-part STL filename matches its image card and sorting label.

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
''',encoding='utf-8')
(R/'FADE_CHECK.json').write_text(json.dumps(dict(test='Actual BreathingAccent.h compiled and executed with a host Arduino stub using g++ C++11',passed=True,checks=['monotonic brightening and dimming','0 to configured ceiling','20 ms update rate limit','off and restart','millis rollover','minimum cycle duration'],board_firmware_compiled=False,flashed=False,hardware_tested=False),indent=2))
print('Delivery notes prepared;',len(ids),'parts,',marked,'physical codes')
