from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'build_revision08.py';s=p.read_text(encoding='utf-8-sig').replace('Revision 07','Revision 08').replace('revision07','revision08').replace('_R07','_R08')
# Remove the entire added flat land. The door will follow the real underside.
a=s.index('        # Narrow flat service land')
b=s.index('    cavity=soft_loft',a)
s=s[:a]+'''        # No external pad: preserve the original oval underside exactly.
'''+s[b:]
s=s.replace("base=base.cut(extr(bay,-1,6.5))","base=base.cut(extr(bay,-1,16))")
s=s.replace("base=union([base,baywall]+rails)","base=union([base,baywall.common(body)]+[r.common(body) for r in rails])")
s=s.replace("base=base.cut(extr(offset(door_profile,.3),-.2,2.7))", """if main:
        base=base.cut(extr(offset(door_profile,.3),-.2,2.7))
    else:
        # A real contoured skin, derived from the unpadded outer shell.
        recess=body.cut(moved(body,z=2.75)).common(extr(offset(door_profile,.3),-1,18))
        base=base.cut(recess)""")
s=s.replace("door=extr(door_profile,.3,2.1)\n    # Round the exposed underside perimeter before adding the latch geometry.\n    door=rounded_edge(door,.3,.65)","""if main:
        door=rounded_edge(extr(door_profile,.3,2.1),.3,.65)
    else:
        # 2.4 mm vertical skin follows the original grip, then sits .15 mm
        # inward. The original battery volume and catch positions are retained.
        door=body.cut(moved(body,z=2.4)).common(extr(door_profile,-1,18))
        door=moved(door,z=.15)""")
# The signature is on the flat leading section of the new curved door.
s=s.replace("),2.4,3,24)","),2.55,3,24)")
s=s.replace("if main:\n        door=rounded_edge", "if main:\n        door=rounded_edge")
# Main door is still at 2.4, so give it its own marking depth.
s=s.replace("),2.55,3,24)","),2.4 if role=='main' else 2.55,3,24)")
old=(R.parent/'revision-06'/'build_revision06.py').read_text(encoding='utf-8')
a=old.index('            # Upper shoulder gate cassette')
b=old.index('            # Actuator at thumb position',a)
gate=old[a:b]
# All the existing kinematics are preserved and recessed 21 mm into the body.
gate=gate.replace('            # Upper shoulder gate cassette, separate from thumb and grip area.', '''            # R08: preserve the grand portcullis, recess its drive into the case.
            caseH=H;H=caseH-21''')
gate=gate.replace("lid=lid.cut(box(gx-17,gy-10,H-15,34,20,20))", """# Roof opening follows the guard. Support neck is outside the opening.
            sy=gy-16;fy=gy+19
            lid=lid.cut(extr(rr(gx-25.3,sy-5.3,50.6,fy-sy+13.6,4),caseH-5,14))""")
gate=gate.replace("H-1,4)","H-3.5,caseH-H+4.5)",1)
gate=gate.replace("lid=union([lid,collar])", """neck=extr(rr(gx-28,sy-8,56,fy-sy+19,5).cut(rr(gx-25.3,sy-5.3,50.6,fy-sy+13.6,4)),H-3.5,caseH-H+4.5)
            webs=[box(gx-25,sy-5,H-3.5,50,9,5),box(gx-25,gy+11,H-3.5,50,fy-gy-3,5)]
            lid=union([lid,collar,neck]+webs)""",1)
# A lower drive yoke and narrow guide rails connect to the visible portcullis.
oldpanel="panel=union([box(gx-17,fy,closed_z-3,34,2.2,6),box(gx-17,fy,closed_z+23,34,2.2,3)]+[box(gx+t,fy,closed_z,2,2.2,26) for t in [-17,-9,-1,7,15]])"
newpanel="""panel=union([box(gx-17,fy,closed_z-3,34,2.2,6),
                         box(gx-17,fy,closed_z,2,2.2,34),box(gx+15,fy,closed_z,2,2.2,34),
                         box(gx-17,fy,caseH+3.5,34,2.2,3),box(gx-17,fy,closed_z+31,34,2.2,3)]
                         +[box(gx+t,fy,caseH+4,2,2.2,closed_z+34-caseH-4) for t in [-9,-1,7]])"""
assert oldpanel in gate;gate=gate.replace(oldpanel,newpanel)
gate=gate.replace("box(gx-17.4,fy-.4,H+10,34.8,3,42)","box(gx-17.4,fy-.4,H+10,34.8,3,50)")
gate=gate.replace("nominal lift 12.12 mm.","nominal lift 12.12 mm. Drive yoke is below the roof; visible bars start above the sill.")
# Recessing creates roof interference; use actual component sweep volumes to
# open passages in the hanging collar without guessing hidden intersections.
gate+='''            sweep=[]
            for dz in [0,12.125]:sweep.append(moved(panel,z=dz))
            for angle in range(-60,61,10):
                q=crank.copy();q.rotate(V(axle_x,0,axle_z),V(0,1,0),angle+60);sweep.append(q)
            lid=cut(lid,sweep)
            H=caseH
'''
a=s.index('            # R07: horizontal rotary rune gate')
b=s.index('            # Actuator at thumb position',a)
s=s[:a]+gate+s[b:]
s=s.replace("['Joystick_Carrier','LCD_Carrier','Gate_Window_Cover','Servo_Cassette']","['Joystick_Carrier','LCD_Carrier','Gate_Frame','Gate_Shroud','Servo_Cassette']")
s=s.replace("shape=text_cut(shape,'SB',(W-196-8,32-3),H-36,3,7,True)","shape=text_cut(shape,'SB',(W-196-4,26),H-23,3,7,True)")
s=s.replace("    elif name=='Gate_Window_Cover':", """    elif name=='Gate_Shroud':
        shape=text_cut(shape,'SB',(W-196-3,51),H+40,3,6);mark='SB — top front lintel'
    elif name=='Gate_Frame':
        shape=text_cut(shape,'SB',(W-196-3,53),H-17.7,3,6,True);mark='SB — underside front foundation'
    elif name=='Gate_Window_Cover':""")
p.write_text(s,encoding='utf-8')
for n in ['check_assembly.py','make_fit_tests.py']:
    p=R/n;t=p.read_text(encoding='utf-8').replace('revision06','revision08').replace('revision07','revision08')
    if n=='check_assembly.py':t=t.replace('A.Vector(55,48,76)','A.Vector(55,48,55)')
    p.write_text(t,encoding='utf-8')
