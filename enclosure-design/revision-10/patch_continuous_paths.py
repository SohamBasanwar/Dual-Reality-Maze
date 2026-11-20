import build_revision10 as B,json
from adjustable_mounts import jaw_sweep,key_sweep
from safe_save import save_document
R=B.ROOT;scene=json.loads((R/'scene.json').read_text())
for role in ['explorer','architect','main']:
    d=B.App.openDocument(str(R/'cad'/f'{role}-revision10.FCStd'));changed=set();W=234 if role=='main' else 246
    for item in json.loads((R/(role+'-adjustments.json')).read_text()):
        prefix=item['prefix'];name=prefix+'_Carrier' if prefix in ['Joystick','LCD'] else 'Base'
        obj=d.getObject(name);q=obj.Shape.copy(True)
        for axis in item['axes']:
            cutter=jaw_sweep(axis,item['nominal_mm'][2],B.box,B.union).mirror(B.V(W/2,0,0),B.V(1,0,0))
            q=q.cut(cutter)
            cutter=key_sweep(axis,B.box,B.union).mirror(B.V(W/2,0,0),B.V(1,0,0));q=q.cut(cutter)
        q=q.removeSplitter();assert q.isValid() and len(q.Solids)==1,(role,name,len(q.Solids))
        obj.Shape=q;changed.add(name)
        if name=='Base':
            args=(prefix,*item['origin'][:2],*item['nominal_mm'][:2],item['origin'][2],item['nominal_mm'][2],B.box,B.cyl,B.union,B.cut,B.moved,B.text_cut)
            fixed,_,_=B.adjustable_mount(*args,limit_front=role!='main',edge_y=10 if role=='architect' and prefix=='Breadboard' else None)
            fixed=fixed.mirror(B.V(W/2,0,0),B.V(1,0,0))
            B.MeshPart.meshFromShape(Shape=fixed,LinearDeflection=.13,AngularDeflection=.22,Relative=False).write(str(R/'inspection-meshes'/(role+'-'+prefix+'-fixed.stl')))
    d.recompute();temp=R/'cad'/f'{role}-continuous.FCStd';save_document(d,temp)
    for name in changed:
        q=d.getObject(name).Shape;row=next(r for r in scene if r['role']==role and r['name']==name);row['volume_mm3']=q.Volume
        mesh=B.MeshPart.meshFromShape(Shape=q,LinearDeflection=.02 if name=='Base' else .08,AngularDeflection=.12,Relative=False)
        for folder in ['prototype-stl','render-meshes']:mesh.write(str(R/folder/row['file']))
    B.Part.export(d.PrintedParts.Group,str(R/'cad'/f'{role}-printed-parts.step'));B.App.closeDocument(d.Name);temp.replace(R/'cad'/f'{role}-revision10.FCStd')
    print(role,'continuous jaw clearance installed',flush=True)
(R/'scene.json').write_text(json.dumps(scene,indent=2))
