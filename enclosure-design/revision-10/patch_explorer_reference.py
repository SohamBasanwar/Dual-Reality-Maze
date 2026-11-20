"""Update only the provisional electronics reservations after the fit review."""
import FreeCAD as A
import Part,MeshPart,json
from pathlib import Path
R=Path(__file__).resolve().parent
d=A.openDocument(str(R/'cad'/'explorer-revision10.FCStd'))
for name,p,size in [('ESP32_Optional_Envelope',(144,90,19.2),(60,32,18)),('ESP32_Wiring_Clearance',(141,86,37.2),(66,40,5))]:
    ob=d.getObject(name);ob.Shape=Part.makeBox(*size,A.Vector(*p))
    MeshPart.meshFromShape(Shape=ob.Shape,LinearDeflection=.13,AngularDeflection=.22,Relative=False).write(str(R/'render-meshes'/('explorer-'+name+'.stl')))
d.recompute();d.save();A.closeDocument(d.Name)
print('Explorer ESP32 reference shifted 2 mm clear of the new edge lip')
