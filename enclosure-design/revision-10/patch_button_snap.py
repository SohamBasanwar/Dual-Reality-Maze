from safe_save import save_document
import build_revision10 as B
import json
R=B.ROOT;d=B.App.openDocument(str(R/'cad'/'architect-revision10.FCStd'));scene=json.loads((R/'scene.json').read_text())
# Exported X=49 is the mirrored source X=197. Cuts are symmetric about stem.
px,py,z=49,95,26.65
cap=B.cut(d.Button_Cap.Shape,B.release_cuts(px,py,z,B.box))
shoe=B.contact_shoe(px,py,z,0,B.box,B.cyl,B.union)
for name,q in [('Button_Cap',cap),('Button_Contact_Shoe',shoe)]:
    assert q.isValid() and len(q.Solids)==1
    d.getObject(name).Shape=q
    row=next(r for r in scene if r['role']=='architect' and r['name']==name);row['volume_mm3']=q.Volume
    if name=='Button_Contact_Shoe':
        row['notes']='Keyed removable contact shoe with split snap tabs. Remove guide and pinch tabs through stem windows to release; physical fit test required.';d.getObject(name).DesignNotes=row['notes']
    mesh=B.MeshPart.meshFromShape(Shape=q,LinearDeflection=.08,AngularDeflection=.15,Relative=False)
    for folder in ['prototype-stl','render-meshes']:mesh.write(str(R/folder/row['file']))
for label,delta in [('minus',-.6),('plus',.6)]:
    q=B.contact_shoe(px,py,z,delta,B.box,B.cyl,B.union)
    B.MeshPart.meshFromShape(Shape=q,LinearDeflection=.08,AngularDeflection=.15,Relative=False).write(str(R/'adjustment-options'/('architect-button-reach-'+label+'-Soham-Basanwar.stl')))
temporary=R/'cad'/'architect-tip-updated.FCStd';d.recompute();save_document(d,temporary);B.Part.export(d.PrintedParts.Group,str(R/'cad'/'architect-printed-parts.step'));B.App.closeDocument(d.Name);temporary.replace(R/'cad'/'architect-revision10.FCStd')
(R/'scene.json').write_text(json.dumps(scene,indent=2));print('Positive snap retention added to the replaceable contact shoe')
