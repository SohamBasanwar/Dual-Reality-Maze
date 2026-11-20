"""Small physical-fit coupons cut from the actual revision geometry."""
from pathlib import Path
import FreeCAD as A, Part, MeshPart, json
R=Path(__file__).resolve().parent;out=R/'fit-tests';out.mkdir(exist_ok=True)
d=A.openDocument(str(R/'cad'/'architect-revision04.FCStd'))
V=A.Vector;checks=[]
def save(name,s,flip=False):
    s=s.copy().removeSplitter()
    if flip:s.rotate(V(0,0,0),V(1,0,0),180)
    b=s.BoundBox;s.translate(V(-b.XMin,-b.YMin,-b.ZMin))
    if not s.isValid() or len(s.Solids)!=1:raise RuntimeError(name+' invalid or disconnected')
    MeshPart.meshFromShape(Shape=s,LinearDeflection=.08,AngularDeflection=.15,Relative=False).write(str(out/(name+'.stl')))
    checks.append({'part':name,'valid':True,'solids':len(s.Solids),'size_mm':[round(v,2) for v in [s.BoundBox.XLength,s.BoundBox.YLength,s.BoundBox.ZLength]]})
def b(x,y,z,w,dd,h):return Part.makeBox(w,dd,h,V(x,y,z))
door=d.getObject('Battery_Door').Shape
bb=door.BoundBox
fixture=d.getObject('Base').Shape.common(b(bb.XMin-5,bb.YMin-4,0,bb.XLength+10,bb.YLength+8,12))
save('01-battery-bay-rim',fixture)
save('02-battery-door',door)
base=d.getObject('Base').Shape.common(b(0,76,27,12,24,16))
base=base.fuse(b(0,76,25,12,24,2.2)).removeSplitter()
lid=d.getObject('Lid').Shape.common(b(0,76,27,12,24,33))
save('03-side-latch-base',base)
save('04-side-latch-lid',lid,True)
button=d.getObject('Lid').Shape.common(b(33,79,38,32,32,22))
save('05-button-guide',button,True)
save('06-button-cap',d.getObject('Button_Cap').Shape,True)
save('07-switch-cassette',d.getObject('Switch_Cassette').Shape)
(out/'VALIDATION.json').write_text(json.dumps(checks,indent=2))
print('Seven normalized fit-test parts exported. Use supports where the slicer indicates; no printer profile assumed.')
