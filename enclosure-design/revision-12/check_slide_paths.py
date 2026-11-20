import FreeCAD as A
import json,sys,Part
from pathlib import Path
R=Path(__file__).resolve().parent;results=[]
for role in (sys.argv[1:] or ['explorer','architect','main']):
    d=A.openDocument(str(R/'cad'/f'{role}-revision12.FCStd'));parts=d.getObject('PrintedParts').Group;bad=[];count=0
    for item in json.loads((R/(role+'-adjustments.json')).read_text()):
        for axis in item['axes']:
            jaw=d.getObject(axis['jaw']);key=d.getObject(axis['key']);lo=min(axis['range_mm']);hi=max(axis['range_mm'])
            b=jaw.Shape.BoundBox;region=Part.makeBox(b.XLength+8,b.YLength+8,b.ZLength+1,A.Vector(b.XMin-4,b.YMin-4,b.ZMin-.5))
            nearby=[(f,f.Shape.common(region)) for f in parts if f not in [jaw,key] and f.Shape.BoundBox.intersect(region.BoundBox)]
            for step in range(round((hi-lo)*2)+1):
                delta=lo+step*.5;q=jaw.Shape.copy(True);q.translate(A.Vector(-axis['direction'][0],axis['direction'][1],0)*(-delta));count+=1
                for fixed,local in nearby:
                    if not local.Solids or not q.BoundBox.intersect(local.BoundBox):continue
                    v=q.common(local).Volume
                    if v>.05:bad.append({'jaw':jaw.Name,'delta_mm':delta,'fixed':fixed.Name,'volume_mm3':round(v,3)})
    results.append({'role':role,'jaw_poses_checked':count,'step_mm':.5,'intersections':bad,'key_detent_requires_physical_flexure_test':True});A.closeDocument(d.Name)
    print(role,count,bad,flush=True)
(R/('SLIDE_PATH_CHECK_'+('_'.join(sys.argv[1:] or ['all']))+'.json')).write_text(json.dumps(results,indent=2))
