from safe_save import save_document
"""Apply the reviewed rear-saddle relocation without repeating shell lofts.
The corresponding construction is in build_revision10.py for regeneration.
"""
import FreeCAD as A
import Part,MeshPart,json
from pathlib import Path
R=Path(__file__).resolve().parent
scene=json.loads((R/'scene.json').read_text())
V=A.Vector
def box(x,y,z,w,d,h):return Part.makeBox(w,d,h,V(x,y,z))
for role in ['explorer','architect']:
    d=A.openDocument(str(R/'cad'/f'{role}-revision10.FCStd'))
    b=d.Base.Shape.copy(True)
    # The removed area is wholly inside the case; no external curved skin
    # or shutter track occupies this Y>=9 mm, Z>=15 mm box.
    b=b.cut(box(114,9,15,18,6,8))
    q=box(-9,3.5,15,18,6,8).cut(box(-5,2.5,18,10,8,6)).cut(box(-10,5,16,20,2.5,1.4))
    q=q.fuse(box(-9,1,15,4,6,5)).fuse(box(5,1,15,4,6,5));q.translate(V(123,0,0))
    q=q.mirror(V(123,0,0),V(1,0,0));b=b.fuse(q).removeSplitter()
    assert b.isValid() and len(b.Solids)==1
    d.Base.Shape=b;d.recompute();temporary=R/'cad'/f'{role}-saddle-updated.FCStd';save_document(d,temporary)
    row=next(r for r in scene if r['role']==role and r['name']=='Base');row['volume_mm3']=b.Volume
    mesh=MeshPart.meshFromShape(Shape=b,LinearDeflection=.02,AngularDeflection=.12,Relative=False)
    for folder in ['prototype-stl','render-meshes']:mesh.write(str(R/folder/row['file']))
    Part.export(d.getObject('PrintedParts').Group,str(R/'cad'/f'{role}-printed-parts.step'))
    A.closeDocument(d.Name);temporary.replace(R/'cad'/f'{role}-revision10.FCStd');print(role,'rear saddle clear of UNO header envelope',flush=True)
(R/'scene.json').write_text(json.dumps(scene,indent=2))
