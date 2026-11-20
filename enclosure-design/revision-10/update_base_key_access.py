from safe_save import save_document
"""Apply the final key-access delta to the already-built handheld bases.
Uses exact old/new mounting solids; preserves the outer shell and battery bay.
"""
import build_revision10 as B
import adjustable_mounts_before_release_review as OLD
import json
R=B.ROOT;scene=json.loads((R/'scene.json').read_text())
for role in ['explorer','architect']:
    d=B.App.openDocument(str(R/'cad'/f'{role}-revision10.FCStd'));base=d.Base.Shape.copy(True)
    skin=B.Part.Shape();skin.read(str(R.parent/'revision-09'/(role+'-pretray.brep')));skin=skin.mirror(B.V(123,0,0),B.V(1,0,0))
    updates=[]
    for prefix,x,y,w,depth,t in [('Breadboard',40,68,166,55,10),('UNO',89,10,68.6,53.4,1.6)]:
        ey=10 if role=='architect' and prefix=='Breadboard' else None
        args=(prefix,x,y,w,depth,3.8,t,B.box,B.cyl,B.union,B.cut,B.moved,B.text_cut)
        old,_,_=OLD.adjustable_mount(*args,limit_front=True,edge_y=ey)
        fixed,parts,info=B.adjustable_mount(*args,limit_front=True,edge_y=ey)
        removed=old.cut(fixed).mirror(B.V(123,0,0),B.V(1,0,0));added=fixed.cut(old).mirror(B.V(123,0,0),B.V(1,0,0))
        restore=removed.common(skin)
        base=base.cut(removed).fuse(added).fuse(restore).removeSplitter()
        for name,q,note in parts:
            q=q.mirror(B.V(123,0,0),B.V(1,0,0));q,mark=B.personalize(q,name,role,246,58)
            ob=d.getObject(name);ob.Shape=q;ob.Personalization=mark;ob.DesignNotes=note
            row=next(r for r in scene if r['role']==role and r['name']==name);row.update(volume_mm3=q.Volume,personalization=mark)
            mesh=B.MeshPart.meshFromShape(Shape=q,LinearDeflection=.13,AngularDeflection=.22,Relative=False)
            for folder in ['prototype-stl','render-meshes']:mesh.write(str(R/folder/row['file']))
        for variant,q in info.pop('_alternate_shapes'):
            q=q.mirror(B.V(123,0,0),B.V(1,0,0))
            B.MeshPart.meshFromShape(Shape=q,LinearDeflection=.13,AngularDeflection=.22,Relative=False).write(str(R/'adjustment-options'/(role+'-'+prefix+'-height-'+variant+'-Soham-Basanwar.stl')))
        info.update(role=role);updates.append(info)
        q=fixed.mirror(B.V(123,0,0),B.V(1,0,0))
        B.MeshPart.meshFromShape(Shape=q,LinearDeflection=.13,AngularDeflection=.22,Relative=False).write(str(R/'inspection-meshes'/(role+'-'+prefix+'-fixed.stl')))
    assert base.isValid() and len(base.Solids)==1,(role,[(s.Volume,str(s.BoundBox)) for s in base.Solids])
    d.Base.Shape=base;d.recompute()
    temporary=R/'cad'/f'{role}-key-access-updated.FCStd'
    save_document(d,temporary)
    row=next(r for r in scene if r['role']==role and r['name']=='Base');row['volume_mm3']=base.Volume
    mesh=B.MeshPart.meshFromShape(Shape=base,LinearDeflection=.02,AngularDeflection=.12,Relative=False)
    for folder in ['prototype-stl','render-meshes']:mesh.write(str(R/folder/row['file']))
    info=json.loads((R/(role+'-adjustments.json')).read_text());info=[r for r in info if r['prefix'] not in ['Breadboard','UNO']]+updates
    (R/(role+'-adjustments.json')).write_text(json.dumps(info,indent=2))
    B.Part.export(d.PrintedParts.Group,str(R/'cad'/f'{role}-printed-parts.step'));B.App.closeDocument(d.Name)
    temporary.replace(R/'cad'/f'{role}-revision10.FCStd')
    print(role,'final key handles and support clearances installed',flush=True)
(R/'scene.json').write_text(json.dumps(scene,indent=2))
