from pathlib import Path
import json
R=Path(__file__).resolve().parent
S=R/'revision-09'; D=R/'revision-10';D.mkdir(exist_ok=True)
for name in ['check_meshes.py','check_assembly.py','check_battery_profile.py','make_fit_tests.py','make_inspection_crops.py','render_details.py','render_mounts.py','render_printed_inventory.py','compose_inventory.py','make_print_plan.py','refresh_solid_validation.py','render_revision09.py']:
    text=(S/name).read_text(encoding='utf-8').replace('revision09','revision10').replace('Revision 09','Revision 10').replace('R09','R10')
    (D/name.replace('revision09','revision10')).write_text(text,encoding='utf-8')
p=json.loads((S/'dimensions.json').read_text())
p.update({'carrier_status':'Manually indexed XY jaws and keyed height inserts; nominal CAD prototype, physical fit unverified.', 'mounting_status':'R10 adjustable rails replace fixed base cradles. Constrained controls retain fixed optical/shaft datums.', 'base_board_bottom_z_mm':9.2,'indexed_edge_travel_mm':[-3,0,3],'height_insert_thickness_mm':[0.6,1.2,1.8]})
(D/'dimensions.json').write_text(json.dumps(p,indent=2))
s=(S/'build_revision09.py').read_text(encoding='utf-8').replace('revision09','revision10').replace('Revision 09','Revision 10').replace('R09','R10')
# Install a reusable, board-edge datum system. The outer shells are unchanged.
s=s.replace('def build(role):','from adjustable_mounts import adjustable_mount, engrave_adjustment\n\ndef build(role):')
start=s.index('    # Breadboard is located in three axes')
end=s.index('    # Sliding I2C cable hatches.',start)
s=s[:start]+'''    mount_records=[]
    for prefix,x,y,w,d,t in [('Breadboard',bx,by,bb[0],bb[1],bb[2]),('UNO',ux,uy,uno[0],uno[1],1.6)]:
        fixed,newparts,info=adjustable_mount(prefix,x,y,w,d,3.8,t,box,cyl,union,cut,moved,text_cut)
        base=union([base,fixed])
        for n,q,note in newparts:add(n,q,'bronze',explosion=(0,0,20),notes=note)
        info.update(role=role);mount_records.append(info)
''' +s[end:]
# Match actual reference and breadboard-button height to the new support datum.
s=s.replace('5+bb[2]+P[','P[\'base_board_bottom_z_mm\']+bb[2]+P[')
s=s.replace("sh=P['architect_button_switch_height_above_breadboard_mm']; sz=5+bb[2]","sh=P['architect_button_switch_height_above_breadboard_mm']; sz=P['base_board_bottom_z_mm']+bb[2]")
s=s.replace("box(bx,by,5,bb[0],bb[1],bb[2])","box(bx,by,P['base_board_bottom_z_mm'],bb[0],bb[1],bb[2])")
s=s.replace("box(ux,uy,7,uno[0],uno[1],1.6)","box(ux,uy,P['base_board_bottom_z_mm'],uno[0],uno[1],1.6)")
s=s.replace('uy+2,8.6','uy+2,11.0').replace('uy+uno[1]-7,8.6','uy+uno[1]-7,11.0')
s=s.replace("esp_x,esp_y=(137,24) if main else (49,86)","esp_x,esp_y=(137,24) if main else (42,86)")
s=s.replace('box(esp_x,esp_y,16,60,32,18)','box(esp_x,esp_y,19.2,60,32,18)').replace('box(esp_x-3,esp_y-4,34,66,40,5)','box(esp_x-3,esp_y-4,37.2,66,40,5)')
# New labels are cut after the common export mirror, so text is readable.
s=s.replace("    return shape,mark\n\ndef build", "    return shape,mark\n\ndef build")
anchor="    return shape,mark\n\nfrom adjustable_mounts"
s=s.replace(anchor,"    shape,mark=engrave_adjustment(shape,name,mark,text_cut)\n    return shape,mark\n\nfrom adjustable_mounts")
s=s.replace("    doc.recompute()\n    doc.saveAs", "    (ROOT/(role+'-adjustments.json')).write_text(json.dumps(mount_records,indent=2))\n    doc.recompute()\n    doc.saveAs")
(D/'build_revision10.py').write_text(s,encoding='utf-8')
print(D)
