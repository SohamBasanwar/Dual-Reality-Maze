"""Relocate the right height-insert tongue clear of the button-side key."""
import build_revision10 as B
import json
R=B.ROOT
d=B.App.openDocument(str(R/'cad'/'architect-revision10.FCStd'))
fixed,parts,info=B.adjustable_mount('Breadboard',40,68,166,55,3.8,10,B.box,B.cyl,B.union,B.cut,B.moved,B.text_cut,limit_front=True,edge_y=10)
q=next(q for n,q,note in parts if n=='Breadboard_Height_Insert').mirror(B.V(123,0,0),B.V(1,0,0))
q,mark=B.personalize(q,'Breadboard_Height_Insert','architect',246,58)
d.Breadboard_Height_Insert.Shape=q;d.Breadboard_Height_Insert.Personalization=mark
base=d.Base.Shape.fuse(B.box(45.8,71.1,7.1,2.4,2.4,.9)).cut(B.box(45.8,73.6,7.1,2.4,2.4,1.1)).removeSplitter()
assert base.isValid() and len(base.Solids)==1
d.Base.Shape=base
scene=json.loads((R/'scene.json').read_text())
for name in ['Base','Breadboard_Height_Insert']:
    shape=d.getObject(name).Shape
    mesh=B.MeshPart.meshFromShape(Shape=shape,LinearDeflection=.02 if name=='Base' else .13,AngularDeflection=.12 if name=='Base' else .22,Relative=False)
    row=next(r for r in scene if r['role']=='architect' and r['name']==name);row['volume_mm3']=shape.Volume
    for folder in ['prototype-stl','render-meshes']:mesh.write(str(R/folder/row['file']))
for label,q in info['_alternate_shapes']:
    q=q.mirror(B.V(123,0,0),B.V(1,0,0))
    B.MeshPart.meshFromShape(Shape=q,LinearDeflection=.13,AngularDeflection=.22,Relative=False).write(str(R/'adjustment-options'/('architect-Breadboard-height-'+label+'-Soham-Basanwar.stl')))
d.recompute();d.save();B.Part.export(d.PrintedParts.Group,str(R/'cad'/'architect-printed-parts.step'));B.App.closeDocument(d.Name)
(R/'scene.json').write_text(json.dumps(scene,indent=2))
print('Height-insert key moved 2.5 mm clear of the slider handle')
