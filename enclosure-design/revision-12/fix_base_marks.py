"""Repair the three base marks from their checkpoint, preserving other R12 work."""
from pathlib import Path
R=Path(__file__).resolve().parent
exec(compile((R/'build_revision12.py').read_text(encoding='utf-8').split('for role in selected:')[0],__file__,'exec'))
rows=json.loads((R/'scene.json').read_text(encoding='utf-8'))
history=json.loads((R/'HIDDEN_MARKS.json').read_text(encoding='utf-8'))
checks=[]
for role in ['explorer','architect','main']:
    d=A.openDocument(str(R/'cad'/f'{role}-revision12.FCStd'))
    row=next(r for r in rows if r['role']==role and r['name']=='Base')
    o=d.Base;initial=o.Shape.copy()
    for key in ['owner_location','id_location']:
        loc=row[key]
        assert loc['z_mm']==3.8,'Repair applies once to the saved checkpoint'
        o.Shape=o.Shape.fuse(code_tool(loc)).removeSplitter()
    for key in ['owner_location','id_location']:
        loc=row[key]
        candidates=([90,20],[100,76],[100,82]) if role=='main' else ([65,105],[145,105],[90,20])
        if key=='id_location':candidates=[loc['xy_mm'],[110,130],[110,70],[150,76]]
        result=None
        for xy in candidates:
            result=mark(o.Shape,loc['label'],loc['height_mm'],4.0,xy,backing=2)
            if result:break
        assert result,(role,key)
        o.Shape,new=result;new.update(role=role,name='Base',kind=loc['kind'])
        row[key]=new
        for i,v in enumerate(history['new_hidden_marks']):
            if v['role']==role and v['name']=='Base' and v['kind']==loc['kind']:history['new_hidden_marks'][i]=new
    s=o.Shape
    # Any added material is confined below the inner floor; no new protrusions.
    added=s.cut(initial);assert added.common(box(-500,-500,4.001,1000,1000,100)).Volume<.001
    assert s.isValid() and len(s.Solids)==1
    row.update(volume_mm3=s.Volume,solids=1)
    mesh=MeshPart.meshFromShape(Shape=s,LinearDeflection=.02 if role!='main' else .08,AngularDeflection=.16,Relative=False)
    for folder in ['prototype-stl','render-meshes']:mesh.write(str(R/folder/row['file']))
    d.recompute();save_document(d,R/'cad'/f'{role}-revision12.FCStd')
    Part.export(d.PrintedParts.Group,str(R/'cad'/f'{role}-printed-parts.step'))
    checks.append(dict(role=role,inner_floor_z_mm=4.0,valid=True,added_above_inner_floor_mm3=0))
    A.closeDocument(d.Name)
(R/'scene.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
history['base_face_repair']=checks
(R/'HIDDEN_MARKS.json').write_text(json.dumps(history,indent=2),encoding='utf-8')
ids=[dict(code=r['assembly_code'],role=r['role'],name=r['name'],marking=r['id_marking'],location=r.get('id_location')) for r in rows if not r['component']]
(R/'ASSEMBLY_IDS.json').write_text(json.dumps(ids,indent=2),encoding='utf-8')
print('Corrected and surface-checked all six base engravings',flush=True)
