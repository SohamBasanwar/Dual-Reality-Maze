from pathlib import Path
import json
R=Path(__file__).resolve().parent
p=R/'finalize_package.py'
s=p.read_text(encoding='utf-8')
for a,b in [('revision07','revision08'),('Revision07','Revision08'),('Revision 07','Revision 08'),('revision-07','revision-08'),("'revision':7","'revision':8"),('len(parts)==46','len(parts)==49'),("len(meshes['checks'])==64","len(meshes['checks'])==67"),('gate_rotation_intersections','gate_slider_intersections'),("'gate_rotation_checked_deg':[0,110,5]","'gate_crank_checked_deg':[-60,60,5],'gate_lift_mm':12.12436"),("'gate_protrusion_above_nominal_lid_mm':6.8","'gate_protrusion_above_nominal_lid_mm':40"),('Compact rotary gate, rounded battery-door perimeter','Recessed castle portcullis and contoured battery access')]:s=s.replace(a,b)
s=s.replace("'REVIEW_VALIDATION.json']]","'REVIEW_VALIDATION.json','BATTERY_PROFILE_REVIEW.json','check_battery_profile.py']]")
s=s.replace('assert len(assembly)==3',"assert len(assembly)==3\nbattery=json.loads((R/'BATTERY_PROFILE_REVIEW.json').read_text())\nassert len(battery)==2 and all(x['added_external_volume_in_battery_region_mm3']<.05 and x['door_outside_original_grip_mm3']<.05 for x in battery)")
p.write_text(s,encoding='utf-8')
p=R/'make_review.py';s=p.read_text(encoding='utf-8').replace('<strong>39 mm</strong>','<strong>40 mm</strong>').replace('a 21 mm reduction','a 20 mm reduction');p.write_text(s,encoding='utf-8')
p=R/'README.md';s=p.read_text(encoding='utf-8').replace('Z = 97 mm','Z = 98 mm, including its new three-tooth crown').replace('**60 mm and 39 mm**','**60 mm and 40 mm**');p.write_text(s,encoding='utf-8')
p=R/'render_details.py';s=p.read_text().replace('camera(scene,(-.15,.10,.135),(-.067,-.0435,.064),.105)','camera(scene,(-.09,.14,.12),(-.067,-.0435,.067),.132)');p.write_text(s)
p=R/'dimensions.json';v=json.loads(p.read_text());v.update({'gate_mechanism':'Recessed portcullis; original nylon horn and captive yoke pin','gate_drive_recess_mm':21,'gate_external_height_mm':40,'gate_lift_mm':12.12436,'battery_door_skin_vertical_mm':2.4,'battery_door_recess_mm':.15,'battery_external_pad':False});p.write_text(json.dumps(v,indent=2))
print('Release sources and metadata updated')
