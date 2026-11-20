from pathlib import Path
import json
import FreeCAD as A
import Part,MeshPart
R=Path(__file__).resolve().parent;O=R/'detail-meshes';O.mkdir(exist_ok=True)
d=A.openDocument(str(R/'cad'/'explorer-revision06.FCStd'));records=[]
# Cut along the middle Y plane: both separate pin passages remain visible.
crop=Part.makeBox(30,15,31,A.Vector(108,102,43))
for n,mat in [('Lid','bronze'),('Reveal_Dome','bronze'),('Bare_Light_Sensor','sensor')]:
    s=d.getObject(n).Shape.common(crop)
    fn=n+'.stl';MeshPart.meshFromShape(Shape=s,LinearDeflection=.06,AngularDeflection=.15,Relative=False).write(str(O/fn))
    records.append({'role':'explorer','name':n,'file':fn,'material':mat,'component':n=='Bare_Light_Sensor','explosion':[0,0,0]})
(R/'detail-scene.json').write_text(json.dumps(records,indent=2));A.closeDocument(d.Name)
print('Actual CAD reveal cross-section exported')
