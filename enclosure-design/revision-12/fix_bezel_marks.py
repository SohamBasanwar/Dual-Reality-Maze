"""Relocate four underside marks that crossed a clip foot."""
from pathlib import Path
R=Path(__file__).resolve().parent
exec(compile((R/'build_revision12.py').read_text(encoding='utf-8').split('for role in selected:')[0],__file__,'exec'))
rows=json.loads((R/'scene.json').read_text(encoding='utf-8'))
history=json.loads((R/'HIDDEN_MARKS.json').read_text(encoding='utf-8'))
failed=[r for r in json.loads((R/'HIDDEN_FACE_CHECK.json').read_text(encoding='utf-8')) if not r['exposed']]
d=A.openDocument(str(R/'cad/main-revision12.FCStd'));changed=set()
for fault in failed:
    row=next(r for r in rows if r['role']=='main' and r['name']==fault['name']);o=d.getObject(row['name'])
    loc=next(r for r in history['new_hidden_marks'] if r['role']=='main' and r['name']==fault['name'] and r['label']==fault['label'])
    o.Shape=o.Shape.fuse(code_tool(loc)).removeSplitter()
    angle=loc['angle_deg'];xy=loc['xy_mm'];found=None
    for shift in [2,-2,4,-4,6,-6,8,-8]:
        position=[xy[0]+(shift if angle==0 else 0),xy[1]+(shift if angle==90 else 0)]
        found=mark(o.Shape,loc['label'],loc['height_mm'],loc['z_mm'],position,True,angle)
        if found:break
    assert found,(row['name'],loc['label'])
    o.Shape,new=found;new.update(role='main',name=row['name'],kind=loc['kind'])
    history['new_hidden_marks'][history['new_hidden_marks'].index(loc)]=new
    row['owner_location' if loc['kind']=='owner' else 'id_location']=new
    changed.add(row['name']);print('RELOCATED',row['name'],loc['label'],new['xy_mm'],flush=True)
for name in changed:
    o=d.getObject(name);s=o.Shape;assert s.isValid() and len(s.Solids)==1
    row=next(r for r in rows if r['role']=='main' and r['name']==name);row.update(volume_mm3=s.Volume,solids=1)
    mesh=MeshPart.meshFromShape(Shape=s,LinearDeflection=.08,AngularDeflection=.16,Relative=False)
    for folder in ['prototype-stl','render-meshes']:mesh.write(str(R/folder/row['file']))
d.recompute();save_document(d,R/'cad/main-revision12.FCStd');Part.export(d.PrintedParts.Group,str(R/'cad/main-printed-parts.step'));A.closeDocument(d.Name)
(R/'scene.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
history['clip_land_repair']=failed
(R/'HIDDEN_MARKS.json').write_text(json.dumps(history,indent=2),encoding='utf-8')
ids=[dict(code=r['assembly_code'],role=r['role'],name=r['name'],marking=r['id_marking'],location=r.get('id_location')) for r in rows if not r['component']]
(R/'ASSEMBLY_IDS.json').write_text(json.dumps(ids,indent=2),encoding='utf-8')
