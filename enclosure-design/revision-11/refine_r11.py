"""Apply final safe-face labels and lens seating clearance to first-pass R11."""
from pathlib import Path
R=Path(__file__).resolve().parent
src=(R/'build_revision11.py').read_text().split('for role in selected:')[0]
exec(compile(src,__file__,'exec'))
rows=json.loads((R/'scene.json').read_text());ids=json.loads((R/'ASSEMBLY_IDS.json').read_text())
for role in ['explorer','architect','main']:
    d=A.openDocument(str(R/'cad'/f'{role}-revision11.FCStd'));changed=set()
    if role=='main':
        for c in json.loads((R/'LIGHTING_LAYOUT.json').read_text())['channels']:
            d.Lid.Shape=d.Lid.Shape.cut(stroke(c['path_xy_mm'],3.05,64,4)).removeSplitter()
        changed.add('Lid')
    for r in [r for r in rows if r['role']==role and not r['component']]:
        o=d.getObject(r['name']);code=r['assembly_code'];name=r['name']
        if not r.get('id_location') and getattr(o,'AssemblyIdentification','').startswith('Engraved '+code):
            if name.endswith('_Height_Insert'):
                b=o.Shape.BoundBox;loc=dict(label=code,xy_mm=[b.XMax-3,b.YMin+8],z_mm=b.ZMax,angle_deg=90,underside=False,height_mm=2.2)
            elif name=='Gate_Frame':loc=dict(label=code,xy_mm=[40,65],z_mm=40.3,angle_deg=0,underside=True,height_mm=2.2)
            else:raise RuntimeError('Recovery position needs explicit review: '+name)
            r.update(id_location=loc,id_marking=o.AssemblyIdentification);next(i for i in ids if i['code']==code).update(location=loc,marking=o.AssemblyIdentification)
        retry=name.endswith(('_Height_Insert','_Bezel')) or name in ['Base','Lid','Battery_Door','RGB_Isolation_Cap','Gate_Frame','Switch_Cassette']
        if not r.get('id_location') and retry:
            result=mark_id(o.Shape,name,role,code)
            if result:
                o.Shape,loc=result;r.update(id_location=loc,id_marking='Engraved '+code+' on noncontact face');prop(o,'AssemblyIdentification',r['id_marking']);changed.add(name)
                ir=next(i for i in ids if i['code']==code);ir.update(location=loc,marking=r['id_marking'])
                print('ADDED CODE',code,name,flush=True)
        if getattr(o,'Personalization','').startswith('SB'):
            pass
        elif name.startswith('Light_') and name.endswith('_Bezel'):
            tag=name.split('_')[1];xy,angle={'G1':((69,10.2),0),'G2':((169,10.2),0),'G3':((38.3,69),90),'G4':((193.5,69),90)}[tag]
            owner=place_mark(o.Shape,'SB',2.2,66.55,xy,angle=angle)
            if owner:o.Shape=owner[0];prop(o,'Personalization','SB — noncontact upper border');changed.add(name)
            else:prop(o,'Personalization','Unmarked: no safe noncontact ownership land; full name in filename')
        elif name=='RGB_Isolation_Cap':
            owner=place_mark(o.Shape,'SB',2.4,32.3,(113.5,103.8),True)
            if owner:o.Shape=owner[0];prop(o,'Personalization','SB — outside bottom face');changed.add(name)
            else:prop(o,'Personalization','Unmarked: no safe noncontact ownership land; full name in filename')
    if role=='main':
        for tag,xy in {'G1':(55,32),'G2':(173,32),'G3':(52,70),'G4':(174,70)}.items():
            code=next(r['assembly_code'] for r in rows if r['name']=='Light_'+tag+'_Bezel')
            result=place_mark(d.Lid.Shape,code,2.5,64,xy)
            if result:d.Lid.Shape=result[0];print('MATCHING SOCKET',code,flush=True)
        coupon=d.Lid.Shape.common(box(24,7,22,72,39,45)).removeSplitter()
        assert coupon.isValid()
        # Cropping isolates a small fragment of the original rear lid tab,
        # unrelated to the light well. Omit only that coupon fragment.
        solids=sorted(coupon.Solids,key=lambda s:s.Volume,reverse=True)
        assert sum(s.Volume for s in solids[1:])<15
        coupon=solids[0];assert coupon.isValid()
        MeshPart.meshFromShape(Shape=coupon,LinearDeflection=.08,AngularDeflection=.16,Relative=False).write(str(R/'fit-tests'/'M-lighting-G1-coupon-Soham-Basanwar.stl'))
    for r in [r for r in rows if r['role']==role]:
        o=d.getObject(r['name']);s=o.Shape
        assert s.isValid() and (r['component'] or len(s.Solids)==1),(role,r['name'])
        if r['name'] in changed:
            mesh=MeshPart.meshFromShape(Shape=s,LinearDeflection=.02 if r['name']=='Base' and role!='main' else .08,AngularDeflection=.16,Relative=False)
            mesh.write(str(R/'render-meshes'/r['file']))
            if not r['component']:mesh.write(str(R/'prototype-stl'/r['file']))
        r.update(volume_mm3=s.Volume,solids=len(s.Solids),personalization=getattr(o,'Personalization','Reference'),notes=getattr(o,'DesignNotes',''))
    if changed:
        d.recompute();save_document(d,R/'cad'/f'{role}-revision11.FCStd');Part.export(d.PrintedParts.Group,str(R/'cad'/f'{role}-printed-parts.step'))
    A.closeDocument(d.Name)
    print('REFINED',role,len(changed),flush=True)
    (R/'scene.json').write_text(json.dumps(rows,indent=2));(R/'ASSEMBLY_IDS.json').write_text(json.dumps(ids,indent=2))
(R/'scene.json').write_text(json.dumps(rows,indent=2));(R/'ASSEMBLY_IDS.json').write_text(json.dumps(ids,indent=2))
with (R/'PARTS.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=['assembly_code','role','name','quantity','file','id_marking','personalization','notes']);w.writeheader()
    for r in rows:
        if not r['component']:w.writerow({k:(1 if k=='quantity' else r.get(k,'')) for k in w.fieldnames})
# Remove only superseded unprefixed copies in this exact revision's mesh dirs.
for folder,expected in [('prototype-stl',{r['file'] for r in rows if not r['component']}),('render-meshes',{r['file'] for r in rows})]:
    target=(R/folder).resolve();assert target.parent==R.resolve()
    for p in target.glob('*.stl'):
        if p.name not in expected:p.unlink()
print('R11 files synchronised;',sum(i['location'] is not None for i in ids),'physically coded parts')
