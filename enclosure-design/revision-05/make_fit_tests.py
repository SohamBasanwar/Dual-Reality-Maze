"""Extract small test pieces from the actual revision-05 solids (FreeCAD Python)."""
from pathlib import Path
import json
import FreeCAD as A
import Part, MeshPart
R=Path(__file__).resolve().parent
out=R/'fit-tests';out.mkdir(exist_ok=True)
checks=[]
def save(name,shape,notes):
    shape=shape.removeSplitter()
    assert shape.isValid() and len(shape.Solids)==1,(name,len(shape.Solids))
    b=shape.BoundBox
    shape.translate(A.Vector(-b.XMin,-b.YMin,-b.ZMin))
    mesh=MeshPart.meshFromShape(Shape=shape,LinearDeflection=.10,AngularDeflection=.15,Relative=False)
    mesh.write(str(out/(name+'.stl')))
    checks.append({'file':name+'.stl','valid_brep':shape.isValid(),'solids':len(shape.Solids),'purpose':notes})
d=A.openDocument(str(R/'cad'/'explorer-revision05.FCStd'))
crop=Part.makeBox(58,77,34,A.Vector(177,119,0))
save('01-battery-grip-receiver',d.getObject('Base').Shape.common(crop),'Actual curved-grip battery receiver; use with door 02 and chosen cell/snap.')
save('02-battery-door',d.getObject('Battery_Door').Shape.copy(),'Door tabs and release tongue. Test in the intended material.')
crop=Part.makeBox(27,24,37,A.Vector(0,77,21))
save('03-latch-base',d.getObject('Base').Shape.common(crop),'Curved side receiver sample.')
save('04-latch-lid',d.getObject('Lid').Shape.common(crop),'Matching flexing lid latch sample; align original upper/lower shell surfaces.')
A.closeDocument(d.Name)
d=A.openDocument(str(R/'cad'/'main-revision05.FCStd'))
crop=Part.makeBox(82,18,31,A.Vector(58,-5,18))
save('05-shutter-receiver',d.getObject('Base').Shape.common(crop),'Rear guide-rail and aperture test section; verify unobstructed sliding.')
save('06-usb-shutter',d.getObject('USB_Shutter').Shape.copy(),'Sliding plate with thumb grip.')
save('07-shutter-end-keeper',d.getObject('USB_Shutter_Keeper').Shape.copy(),'End stop: retained by Main lid in the full assembly.')
A.closeDocument(d.Name)
(out/'VALIDATION.json').write_text(json.dumps(checks,indent=2))
print('Seven fit-test parts exported.')
