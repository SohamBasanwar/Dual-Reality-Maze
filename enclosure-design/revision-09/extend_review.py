from pathlib import Path
import runpy,json,csv
R=Path(__file__).resolve().parent
runpy.run_path(str(R/'make_review.py'))
runpy.run_path(str(R/'make_print_plan.py'))
def pic(name,c):return f'<figure><a href="previews/{name}"><img src="previews/{name}" loading="lazy" alt="{c}"></a><figcaption>{c}</figcaption></figure>'
s=(R/'index.html').read_text(encoding='utf-8')
s=s.replace('Revision 09 · recessed castle gate, contoured battery access and personalized parts.','Revision 09 · screwless component holders, breadboard button linkage, and a removable servo bridge.')
block='''<h2>Component mounts: the missing underside views</h2><p>The old internal views showed the lower bases. Most controls attach to the removable lids. These new views expose those holders. <strong>No threaded screws:</strong> the design uses snap-in edge carriers, clips and quarter-turn keepers. Fixed PCB-hole pins remain deferred until the actual holes are verified.</p><p><a href="MOUNTING_AUDIT.md">Mounting audit, assembly instructions and component references</a>. Joystick belongs to Explorer; Main has the LCD, buzzer, RGB and power-control actuator.</p>'''
info={'explorer':'Joystick carrier, RGB light cup and isolated photoresistor lead passages. The sensor sits above the roof.','architect':'Potentiometer cup, RGB light cup, recessed servo cartridge and long button stem/guide.','main':'LCD carrier and backpack clearance, buzzer cup, RGB light cup and short power-control switch cassette.'}
for role in info:
    block+=f'<h3>{role.title()} — underside of lid</h3><div class="grid">'+pic(role+'-lid-holders.png','Printed holders only. '+info[role])+pic(role+'-lid-installed.png','With nominal purchased component shapes. '+info[role])+'</div>'
block+='<h2>Removable carriers and keepers</h2><div class="grid">'
for n,c in [('joystick-mount.png','Explorer: fit the PCB in its separate edge carrier, then snap the carrier into the lid. Confirm full stick and click travel.'),('lcd-mount.png','Main: corrected, connected nominal LCD stack. The carrier supports and captures the PCB edges, with backpack space below.'),('servo-mount.png','Architect: place the servo in the cassette, then fit the new SB-marked snap bridge. Release both side beams to remove it.'),('pot-mount.png','Architect: roof cup and removable quarter-turn lower keeper. Body, terminal lugs and antirotation feature remain fit items.'),('buzzer-mount.png','Main: round sounder cup and lower bayonet keeper with a central wire opening. Confirm actual sounder diameter.')]:block+=pic(n,c)
block+='</div><h2>The Architect button reaches the breadboard</h2><p>The previous lid-mounted switch cassette is replaced with a long printed stem and a removable two-bearing guide. Pressing the outer cap presses the actual switch down; its spring returns the cap. A flange stop limits travel. Main retains its short power-control cassette.</p>'
block+=pic('button-linkage.png','Printed cap/stem and guide above a black tactile switch and beige breadboard slice. The two electronic reference shapes are not printed.')
block+='<p>Nominal dimensions: breadboard top Z15, switch actuator Z22.3, stem tip Z22.45 mm. Free gap is 0.15 mm and drawn travel is 0.45 mm. These settings must be adjusted to the actual installed switch height and stroke. Do not let an overlong stem hold the switch on at rest. Use fit samples 15–17 before printing a full lid.</p><h2>The photoresistor dome opens</h2>'
block+=pic('ldr-open.png','Dome lifted off the isolated sensor seat. Turn 90 degrees to align the tabs with the collar slots before lifting. Do not rotate the sensor or twist its leads.')
block+='<p>The opaque floor separates the sensor from internal lighting. Only two small lead passages enter the case; seal around the real leads if light leaks through. The thin printed roof remains an optical test. Use the separate clear-film alternative if your filament blocks ambient light.</p>'
s=s.replace('<h2>The castle gate returns</h2>',block+'<h2>The castle gate returns</h2>')
s=s.replace('<h2>Battery access and internal layout</h2>','<h2>Battery access and internal layout</h2><p><strong>Orange block:</strong> reserved space for an unselected regulator/load-switch circuit. <strong>Green block:</strong> optional ESP32 space. Neither is an extra printed component.</p>')
sheet='<h2>Every printed assembly part</h2><p><strong>9 full-name engravings · 12 SB markings · 29 unmarked parts.</strong> All 50 printed assembly pieces appear below, with no electrical components. Each part is enlarged to fit its card, so thumbnail sizes are not comparable.</p>'
sheet+=pic('printed-parts-all.png','Complete 50-part inventory, rendered from the final STL meshes. Click for full resolution. Optical roof alternatives substitute for the default dome; test crops are not additional assembly parts.')
sheet+='<p><a href="previews/printed-parts-full-name.png">Full-name sheet</a> · <a href="previews/printed-parts-sb.png">SB sheet</a> · <a href="previews/printed-parts-unmarked.png">Unmarked sheet</a></p>'
s=s.replace('<h2>Your name and initials</h2>',sheet+'<h2>Your name and initials</h2>')
s=s.replace('<h2>Review and files</h2>','<h2>Printing and review files</h2><p>Your installed FreeCAD and PrusaSlicer are sufficient; OpenSCAD is optional. No additional application is required. Curved shells, roof spans, latch undercuts and gate arches may need selective supports. Keep support removable and away from blind shutter tracks, optical passages and sliding guides.</p><p><a href="PRINT_PLAN.csv">Part-by-part orientation and support plan</a> · <a href="MOUNTING_AUDIT.md">Mounting audit and references</a> · <a href="../Dual_Reality_Maze_Revision09_Review.zip">Complete CAD/STL review package</a></p>')
s=s.replace('../revision-06/index.html','../revision-08/index.html')
(R/'index.html').write_text(s,encoding='utf-8')
# Keep the new audit first in the readme; retain R08 mechanism context below.
readme=(R/'README.md').read_text(encoding='utf-8')
if '## Mounting audit and corrections' not in readme:
    readme=readme.replace('## Castle gate, at a smaller scale','''## Mounting audit and corrections

Read [MOUNTING_AUDIT.md](MOUNTING_AUDIT.md) for the per-component attachment and installation steps. Revision 09 adds a long Architect button stem to reach the breadboard switch, a removable guide/stop, and a separate snap-in servo retaining bridge. The LCD reference stack and carrier have been corrected. The sensor dome is removable by quarter turn and lift.

The review page includes empty and populated underside views of every lid, component close-ups, and final printed-part sheets. There are 50 assembly parts: 9 full-name, 12 SB, 29 physically unmarked. No fixed PCB-hole pins are assumed. Use the replaceable edge carriers until real mounting holes are confirmed. The orange block is an unselected power-module reservation, not a part to print.

See [PRINT_PLAN.csv](PRINT_PLAN.csv) for suggested orientations/supports. There are 21 actual-part fit samples and four optical variants (alternatives, not four additional installed domes). Physical testing is still required. FreeCAD and PrusaSlicer are sufficient; no additional application is needed.

## Castle gate, at a smaller scale''')
    (R/'README.md').write_text(readme,encoding='utf-8')
guide=(R/'PRINT_AND_ASSEMBLY.md').read_text(encoding='utf-8')
if '## Revision 09 installation order' not in guide:
    guide+='''

## Revision 09 installation order

1. Fit the Arduino, breadboard and battery in their base restraints. Keep reserved optional space clear. Test the independent contoured battery door before wiring.
2. Fit joystick and LCD into their loose edge carriers, then snap the carriers into their lid receivers. Fit pot and buzzer from the underside and turn their lower keepers into place. Test antirotation and terminal clearance on the real potentiometer.
3. Remove the photoresistor hood by quarter turn and lift. Insert the sensor into its above-roof seat, feed its two leads through the isolated bores, seal light leaks and replace the hood. Do not twist the sensor leads.
4. Architect: fit the actual switch into the breadboard first. Verify the installed actuator height. Insert the long printed cap from below the lid; fit the two-bearing guide by its snap beams. Bring the lid into position and confirm the cap is not preloaded. Test free return, alignment and the 0.45 mm nominal stop. Change the stem-height parameters if needed; do not scale the STL.
5. Architect: place the SG90 in the separate cassette from above, latch the new retaining bridge, then fit the cartridge/frame and original nylon horn drive. No forced insertion under stiff integral top lips is required. Confirm real servo ear and wire clearance.
6. Fit RGB LEDs, keepers, selected optical diffusers and masks. Route wiring with service slack. Keep every moving part and guide free of wires before closing the shell.

Print the new button cap/guide/roof samples, servo cassette/retainer, and reveal pod/dome samples before full shells. `PRINT_PLAN.csv` gives a starting orientation and support caution for each of the 50 assembly parts. Review supports in PrusaSlicer; this is not an automatically validated machine setup. General support guidance: https://help.prusa3d.com/article/support-material_1698 . No printer-specific G-code is supplied.

Main's momentary power-control button still needs a suitable load-switch/latching circuit; it is not an electrical mains or battery switch by itself. Independent battery-powered controllers cannot be switched fully off/on through an unpowered I2C link alone.
'''
    (R/'PRINT_AND_ASSEMBLY.md').write_text(guide,encoding='utf-8')
check=(R/'DIMENSION_CHECKLIST.csv').read_text(encoding='utf-8')
check=check.replace('12 x 12 x 6 mm placeholder','12 x 12 mm; Architect installed actuator height 7.3 mm provisional').replace('34 x 26 mm PCB,','34 x 26 mm PCB provisional,')
(R/'DIMENSION_CHECKLIST.csv').write_text(check,encoding='utf-8')
print('Extended component/printing/marking review complete')
