"""Compare the revised access area to the original unpadded grip envelope."""
import importlib.util,json
from pathlib import Path
import FreeCAD as A
import Part
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('cad_source',R/'build_revision08.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
outer=m.sculpted_outline()
levels=[(0,-6),(3,-4.5),(8,-2.5),(15,-1),(24,-.2),(33,-1.2),(42,-3),(48,-4.8),(53,-7.5),(58,-11)]
body=m.soft_loft(outer,levels).common(m.ceiling(246,58,False)).common(m.grip_limit())
original=body.mirror(A.Vector(123,0,0),A.Vector(1,0,0))
reports=[]
for role in ['explorer','architect']:
    d=A.openDocument(str(R/'cad'/f'{role}-revision08.FCStd'))
    door=d.Battery_Door.Shape
    crop=Part.makeBox(42,73,15,A.Vector(183,120,-1))
    area=d.Base.Shape.fuse(door).common(crop)
    excess=area.cut(original).Volume
    door_excess=door.cut(original).Volume
    row={'role':role,'added_external_volume_in_battery_region_mm3':excess,'door_outside_original_grip_mm3':door_excess,
         'door_skin_vertical_thickness_mm':2.4,'door_recess_mm':.15,'mating_clearance_vertical_mm':.2,
         'battery_body_clearance_mm3':door.common(d.Battery_Envelope.Shape).Volume,
         'note':'Compares against the original oval outer shell with no service pad. Digital geometry only; physical feel/latch test remains.'}
    assert excess<.05 and door_excess<.05,row
    assert row['battery_body_clearance_mm3']<.05,row
    reports.append(row);A.closeDocument(d.Name)
(R/'BATTERY_PROFILE_REVIEW.json').write_text(json.dumps(reports,indent=2))
print(json.dumps(reports,indent=2))
