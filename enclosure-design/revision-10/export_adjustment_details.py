import FreeCAD as A
import Part,MeshPart,json,sys
from pathlib import Path
R=Path(__file__).resolve().parent;out=R/'inspection-meshes';out.mkdir(exist_ok=True)
coupons=R/'fit-tests';coupons.mkdir(exist_ok=True)
for role in (sys.argv[1:] or ['explorer','architect','main']):
    d=A.openDocument(str(R/'cad'/f'{role}-revision10.FCStd'))
    for item in json.loads((R/(role+'-adjustments.json')).read_text()):
        name=item['prefix'];j=d.getObject(name+'_X_Jaw').Shape;k=d.getObject(name+'_X_Lock_Key').Shape
        bb=j.BoundBox;bb.add(k.BoundBox)
        crop=Part.makeBox(bb.XLength+6,bb.YLength+6,bb.ZLength+6,A.Vector(bb.XMin-3,bb.YMin-3,item['local_frame_z']-.2))
        fixture=d.getObject(name+'_Carrier' if name in ['Joystick','LCD'] else 'Base').Shape.common(crop)
        MeshPart.meshFromShape(Shape=fixture,LinearDeflection=.13,AngularDeflection=.22,Relative=False).write(str(out/(role+'-'+name+'-rail-detail.stl')))
        # A compact actual-geometry test is supplied for the common rail.
        if role=='explorer' and name=='UNO':
            # Use integral fixture portion but retain only the connected major solid.
            q=max(fixture.Solids,key=lambda s:s.Volume).copy(True)
            for label,shape in [('01-indexed-rail-coupon',q),('02-indexed-jaw-coupon',j),('03-indexed-key-coupon',k)]:
                shape=shape.copy(True);b=shape.BoundBox;shape.translate(A.Vector(-b.XMin,-b.YMin,-b.ZMin))
                assert shape.isValid() and len(shape.Solids)==1
                MeshPart.meshFromShape(Shape=shape,LinearDeflection=.08,AngularDeflection=.15,Relative=False).write(str(coupons/(label+'-Soham-Basanwar.stl')))
    A.closeDocument(d.Name)
print('Actual rail detail crops and three first-fit coupons exported')
