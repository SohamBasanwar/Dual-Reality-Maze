from pathlib import Path
import json, shutil
root=Path(__file__).resolve().parent
old=root/'revision-08'; new=root/'revision-09'
new.mkdir(exist_ok=True)
for name in ['build_revision08.py','check_assembly.py','check_meshes.py','check_battery_profile.py','make_fit_tests.py','render_revision08.py','render_details.py','make_review.py','finalize_package.py','dimensions.json','DIMENSION_CHECKLIST.csv','README.md','PRINT_AND_ASSEMBLY.md']:
    target=name.replace('revision08','revision09')
    s=(old/name).read_text(encoding='utf-8').replace('revision08','revision09').replace('revision-08','revision-09').replace('Revision08','Revision09').replace('Revision 08','Revision 09').replace('_R08','_R09')
    (new/target).write_text(s,encoding='utf-8')
p=json.loads((new/'dimensions.json').read_text())
p.update({'architect_button_switch_height_above_breadboard_mm':7.3,
          'architect_button_rest_gap_mm':0.15,'architect_button_max_stroke_mm':0.45,
          'architect_button_xy_before_mirror':[197,95],
          'button_fit_status':'Nominal 12 mm projected-plunger switch; installed actuator height, pin spacing and stroke must be checked on the real breadboard.',
          'lcd_reference_pcb_bottom_z_mm':54.6,'lcd_reference_pcb_thickness_mm':1.6,
          'lcd_reference_total_height_mm':8.4,
          'servo_mounting_ear_span_mm':32.3,'servo_ear_y_from_bottom_mm':17,
          'servo_ear_thickness_mm':2,
          'mounting_status':'Screwless edge-capture carriers and quarter-turn keepers. No unverified hole-location pins. Servo ear clearance is provisional.'})
(new/'dimensions.json').write_text(json.dumps(p,indent=2),encoding='utf-8')
s=(new/'build_revision09.py').read_text(encoding='utf-8')
# LCD: keep the real screen/PCB stack together; flat mount, not a fictitious tilt.
s=s.replace("# LCD roof opening with bezel; small tilt is carried by the separate wedge cradle.","# Flat LCD stack, with accessible PCB edge clips and backpack clearance.")
start=s.index('        lcdframe=extr(')
end=s.index('        for yy in [103,109,115,121]',start)
s=s[:start]+'''        pcb_z=P['lcd_reference_pcb_bottom_z_mm']
        pcb_t=P['lcd_reference_pcb_thickness_mm']
        lcd_top=pcb_z+P['lcd_reference_total_height_mm']
        lcdframe=extr(rr(lx-2,ly-2,84.6,40,3).cut(rr(lx-.4,ly-.4,81.4,36.8,1)),pcb_z-1.0,H-5-(pcb_z-1.0))
        for xx in [lx-2,lx+80.6]:
            direction=-1 if xx<lx else 1
            ear=box(xx-1.2 if direction<0 else xx+1.8,ly+12,H-8,1.4,12,1.3)
            lcdframe=union([lcdframe,ear])
            socket=box(xx-2,ly+9,H-12,6,18,9)
            socket=socket.cut(box(xx-.3,ly+8.7,H-12.2,2.6,18.6,9.4))
            socket=socket.cut(box(xx-1.5 if direction<0 else xx+1.5,ly+11.7,H-8.3,2,12.6,1.9))
            lid=union([lid,socket])
        for xx in [lx-2,lx+79.6]:
            lcdframe=union([lcdframe,box(xx,ly+5,pcb_z-.8,3,26,.6),box(xx,ly+12,pcb_z+pcb_t+.2,3,5,1.2)])
        add('LCD_Carrier',lcdframe,'bronze',explosion=(0,0,-25),notes='Replaceable PCB edge-capture carrier. Flat reference LCD stack, 0.2 mm vertical edge clearance. No fixed mounting-hole pins; measure actual LCD and backpack before printing.')
        add('LCD_PCB_Envelope',box(lx,ly,pcb_z,80.6,36,pcb_t),'pcb',True)
        add('LCD_Display_Envelope',box(lx+5.8,ly+6,pcb_z+pcb_t,69,24,lcd_top-pcb_z-pcb_t),'lcd',True,notes='Reference 8.4 mm total PCB/display stack. Manufacturer-family reference, not a confirmed match to the photographed unit.')
        add('LCD_Backpack_Envelope',box(lx+8,ly+7,pcb_z-9,42,20,9),'black',True)
''' +s[end:]
# Architect breadboard button. Preserve Main's short power-control actuator.
s=s.replace("cap=union([cyl(px,py,H-4.3,10,1.5),cyl(px,py,H-3,7.9,7),cyl(px,py,H-9.3,2.5,5.3)])", """tip_z=H-9.3 if main else 5+bb[2]+P['architect_button_switch_height_above_breadboard_mm']+P['architect_button_rest_gap_mm']
        cap=union([cyl(px,py,H-4.3,10,1.5),cyl(px,py,H-3,7.9,7),cyl(px,py,tip_z,2.5,H-4-tip_z)])""")
s=s.replace("notes='Guided actuator, retaining flange and adjustable pusher. 0.3 mm radial clearance; tune switch travel.'", "notes=('Short captured power-control actuator; requires a load-switch circuit, not direct battery switching.' if main else 'One-piece cap with long 5 mm-diameter stem to the breadboard switch. Nominal rest tip Z22.45, free gap 0.15 mm, maximum stroke 0.45 mm. Regenerate stem height from the measured installed switch; do not preload it.')")
start=s.index('        # Switch cassette slides')
end=s.index('    if main:\n        # Flat LCD',start)
oldblock=s[start:end]
mainblock='\n'.join('    '+line if line else line for line in oldblock.rstrip().splitlines())+'\n'
s=s[:start]+'''        if main:
'''+mainblock+'''        else:
            # Separate snap-in guide/stop. Switch itself stays on the breadboard.
            # The stem slides through both rings; flange stops against the upper ring.
            stroke_mm=P['architect_button_max_stroke_mm']
            stop_top=H-4.3-stroke_mm
            guide_part=union([ring(px,py,stop_top-1.6,10.1,3.0,1.6),
                              ring(px,py,31,6.5,2.85,3),
                              box(px-7,py-2,31,2,4,stop_top-31),
                              box(px+5,py-2,31,2,4,stop_top-31)])
            for sign in [-1,1]:
                x=px+sign*10.7
                # Outboard beams terminate in hooks under roof-mounted shoulders.
                beam=box(x-.7,py-3,stop_top-7,1.4,6,7)
                bridge=box(px-11.4 if sign<0 else px+8.5,py-3,stop_top-1.8,2.9,6,1.8)
                hook=box(px-12.4 if sign<0 else px+10.7,py-3,stop_top-7.0,1.7,6,1)
                guide_part=union([guide_part,beam,bridge,hook])
                support=box(px-14.5 if sign<0 else px+12.5,py-5,stop_top-7.4,2,10,H-3.8-(stop_top-7.4))
                shoulder=box(px-14.5 if sign<0 else px+11.8,py-4,stop_top-7.4,2.7,8,.2)
                lid=union([lid,support,shoulder])
            add('Button_Stem_Guide',guide_part,'bronze',explosion=(0,0,-15),notes='Removable snap-in guide with two stem bearings and a cap-flange stop. Releases from below. Stop travel is nominal 0.45 mm; real switch travel and return must be checked.')
            sh=P['architect_button_switch_height_above_breadboard_mm']; sz=5+bb[2]
            sw=union([box(px-6,py-6,sz,12,12,3.6),box(px-2.15,py-2.15,sz+3.6,4.3,4.3,sh-3.6)])
            add('Tactile_Switch_Envelope',sw,'black',True,notes='Reference 12 x 12 mm projected actuator switch on breadboard. Height above breadboard is parametric, default 7.3 mm; pin fit and operating travel unverified.')
            add('Button_Wiring_Clearance',box(px-8,py-9,sz,16,18,10).cut(sw),'clearance',True,notes='Keep this breadboard area clear except the switch and its wires. Actuator path above it must remain clear.')
''' +s[end:]
# Give the guide initials on the wide lower ring, outside running faces.
needle="    elif name=='Switch_Cassette':"
s=s.replace(needle,"""    elif name=='Button_Stem_Guide':
        shape=text_cut(shape,'SB',(W-197-2.5,95+3.5),31,2.2,5,True);mark='SB — underside guide ring, away from stem bore'
"""+needle)
# Include SG90 ears in the provisional component and relieve carrier walls.
s=s.replace("servo=box(gx-11.5,sy,H+6,23,29,12.2)","""servo_body=box(gx-11.5,sy,H+6,23,29,12.2)
            ear_span=P['servo_mounting_ear_span_mm']; ear_y=sy+P['servo_ear_y_from_bottom_mm']
            servo_ears=box(gx-ear_span/2,ear_y,H+6,ear_span,P['servo_ear_thickness_mm'],12.2)
            servo=union([servo_body,servo_ears])""")
s=s.replace("notes='Sideways placement. Shaft offset, ears and exact horn geometry require measurement.'", "notes='Sideways SG90 family reservation, including provisional 32.3 mm mounting-ear span. Original nylon horn retained. Ear position/thickness and shaft geometry must match actual servo before print.'")
s=s.replace("            add('Servo_Cassette',cassette,'bronze',explosion=(0,0,38))", """            cassette=cassette.cut(box(gx-ear_span/2-.3,ear_y-.3,H+5.7,ear_span+.6,P['servo_ear_thickness_mm']+.6,12.8))
            add('Servo_Cassette',cassette,'bronze',explosion=(0,0,38),notes='Body-capture cassette with top retaining lips, keyed foot and lower push-in latches. Slots accommodate provisional SG90 ears; no guessed hole pins. Fit actual servo with cassette removed, then insert cassette into frame.')""")
(new/'build_revision09.py').write_text(s,encoding='utf-8')
print(new)
