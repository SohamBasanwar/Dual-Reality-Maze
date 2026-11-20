"""R12: relocate exposed lettering, preserving the corrected R11 native shapes.
Run with FreeCAD's bundled Python. All dimensions are millimetres.
"""
from pathlib import Path
import json,csv,sys,math
import FreeCAD as A,Part,MeshPart
from safe_save import save_document
from build_revision10 import box,cyl,stroke,oriented
R=Path(__file__).resolve().parent;V=A.Vector
selected=sys.argv[1:] or ['explorer','architect','main']
rows=json.loads((R/('scene.json' if sys.argv[1:] else 'baseline-r11/scene.json')).read_text(encoding='utf-8'))
previous=json.loads((R/'HIDDEN_MARKS.json').read_text(encoding='utf-8')) if sys.argv[1:] else {}
audit=[r for r in previous.get('modified_parts',[]) if r['role'] not in selected]
removed_locations=[r for r in previous.get('restored_exterior_marks',[]) if r['role'] not in selected]
hidden_locations=[r for r in previous.get('new_hidden_marks',[]) if r['role'] not in selected]

def prop(o,n,v):
    if not hasattr(o,n):o.addProperty('App::PropertyString',n)
    setattr(o,n,str(v))

def letters(label,h,width=None):
    q=Part.makeCompound([Part.makeFace(w,'Part::FaceMakerBullseye') for w in Part.makeWireString(label,'C:/Windows/Fonts/','arialbd.ttf',h) if w])
    if width and q.BoundBox.XLength>width:q.scale(width/q.BoundBox.XLength)
    q.translate(V(-q.BoundBox.XMin,-q.BoundBox.YMin,0));return q

def old_text_tool(label,xy,z,h,width,under=False):
    q=letters(label,h,width)
    if under:q=q.mirror(V(q.BoundBox.XLength/2,0,0),V(1,0,0))
    q=q.extrude(V(0,0,.28));q.translate(V(*xy,z-.02 if under else z-.26))
    # Trim to the original surface. Never leave raised lettering outside it.
    return q.common(box(-500,-500,z if under else z-.26,1000,1000,.26))

def code_tool(loc):
    q=letters(loc['label'],loc['height_mm']);q.rotate(V(),V(0,0,1),loc['angle_deg'])
    if loc['underside']:q=q.mirror(V(),V(1,0,0))
    b=q.BoundBox;q.translate(V(loc['xy_mm'][0]-b.XMin,loc['xy_mm'][1]-b.YMin,loc['z_mm']))
    return q.extrude(V(0,0,.24 if loc['underside'] else -.24))

def restore(o,tool,reason,role):
    before=o.Shape;after=before.fuse(tool).removeSplitter()
    added=tool.cut(before).Volume
    assert after.isValid() and len(after.Solids)==1,(role,o.Name,reason,'invalid restoration')
    # Measure the local fill directly, rather than subtracting two large
    # curved-shell integrated volumes. The tool stops at the original face.
    assert added>.1 and added<=tool.Volume+.01,(role,o.Name,reason,added,tool.Volume)
    o.Shape=after
    removed_locations.append(dict(role=role,name=o.Name,reason=reason,restored_mm3=added))

def mark(s,label,h,z,xy,under=False,angle=0,backing=1.25):
    q=letters(label,h);q.rotate(V(),V(0,0,1),angle)
    if under:q=q.mirror(V(),V(1,0,0))
    b=q.BoundBox;q.translate(V(xy[0]-b.XMin,xy[1]-b.YMin,z));b=q.BoundBox
    land=box(b.XMin-.12,b.YMin-.12,z-.01 if under else z-backing,b.XLength+.24,b.YLength+.24,backing+.01)
    if s.common(land).Volume<land.Volume*.985:
        print('MARK no backing',label,xy,s.common(land).Volume/land.Volume,flush=True);return None
    # The lettering must open onto the chosen face, not form a buried void.
    probe=q.copy();probe.translate(V(0,0,-.01 if under else .01))
    probe=probe.extrude(V(0,0,-.03 if under else .03))
    if s.common(probe).Volume>max(.001,probe.Volume*.01):
        print('MARK buried',label,xy,s.common(probe).Volume/probe.Volume,flush=True);return None
    tool=q.extrude(V(0,0,.24 if under else -.24));after=s.cut(tool).removeSplitter()
    if s.common(tool).Volume<tool.Volume*.85 or not after.isValid() or len(after.Solids)!=1:return None
    return after,dict(label=label,xy_mm=list(xy),z_mm=z,angle_deg=angle,underside=under,height_mm=h,bounds_xywh_mm=[b.XMin,b.YMin,b.XLength,b.YLength],removed_mm3=s.Volume-after.Volume,visibility='Hidden when assembled')

def put(o,row,label,h,z,xy,under=False,angle=0,kind='code',backing=1.25):
    result=mark(o.Shape,label,h,z,xy,under,angle,backing)
    if not result:return False
    o.Shape,loc=result;loc.update(role=row['role'],name=row['name'],kind=kind)
    hidden_locations.append(loc)
    if kind=='code':row.update(id_location=loc,id_marking='Engraved '+label+' on hidden interior/underside face')
    else:row.update(owner_location=loc,personalization=label+' — hidden interior/underside face')
    return True

def shutter_transform(q,name,W):
    if name=='USB_Shutter':q.translate(V(117,0,0))
    elif name=='I2C_Rear_Shutter':q.translate(V(123,0,0))
    elif name=='I2C_Left_Shutter':q=oriented(q,-90,0,125)
    else:q=oriented(q,90,W,95)
    return q.mirror(V(W/2,0,0),V(1,0,0))

def shutter_old_tool(name,W):
    q=letters('SB',2.6);q.translate(V(-q.BoundBox.XLength/2,0,0));q=q.mirror(V(),V(1,0,0))
    q=q.extrude(V(0,0,.28));q.rotate(V(),V(1,0,0),90);q.translate(V(0,-4.94,31 if name=='USB_Shutter' else 22.5))
    q=q.common(box(-50,-5.2,0,100,.26,100))
    return shutter_transform(q,name,W)

def shutter_mark(o,row,label,z,W):
    # Central back face only; clear of the sliding top/bottom/side edges.
    h=2.6;q=letters(label,h);w=q.BoundBox.XLength
    # Before final mirroring: +X goes right for the interior view.
    q.translate(V(-w/2,0,0));q.rotate(V(),V(1,0,0),90);q.translate(V(0,0,z))
    tool=q.extrude(V(0,-.24,0));tool=shutter_transform(tool,o.Name,W)
    if o.Shape.common(tool).Volume<tool.Volume*.98:return False
    after=o.Shape.cut(tool).removeSplitter();assert after.isValid() and len(after.Solids)==1
    o.Shape=after
    # Save the actual centre and inward viewing direction for later rendering.
    point=Part.Vertex(V(0,0,z+1));point=shutter_transform(point,o.Name,W).Point
    back=Part.Vertex(V(0,1,z+1));back=shutter_transform(back,o.Name,W).Point-point
    loc=dict(label=label,role=row['role'],name=o.Name,kind='owner' if label=='SB' else 'code',centre_mm=[point.x,point.y,point.z],view_direction=[back.x,back.y,back.z],height_mm=h,visibility='Interior back face; hidden when shutter is closed')
    hidden_locations.append(loc)
    if label=='SB':row.update(owner_location=loc,personalization='SB — interior back face of shutter')
    else:row.update(id_location=loc,id_marking='Engraved '+label+' on interior back face')
    return True

for role in selected:
    print('BEGIN',role,flush=True)
    W,H=(234,64) if role=='main' else (246,58)
    d=A.openDocument(str(R/'baseline-r11'/f'{role}-revision11.FCStd'))
    changed=set();source_shapes={o.Name:o.Shape.copy() for o in d.PrintedParts.Group}
    for row in [r for r in rows if r['role']==role and not r['component']]:
        name=row['name'];o=d.getObject(name);code=row['assembly_code']
        exterior=name in ['Base','Button_Cap','Servo_Retainer'] or name in ['I2C_Rear_Shutter','I2C_Left_Shutter','I2C_Right_Shutter','USB_Shutter'] or (name.startswith('Light_') and name.endswith('_Bezel'))
        if not exterior:
            row['mark_visibility']='Internal component or concealed face' if row['personalization'].startswith(('SB','Soham')) or row.get('id_location') else 'No physical mark'
            continue
        changed.add(name)
        # Restore exposed R11 assembly codes before placing hidden replacements.
        if row.get('id_location'):
            restore(o,code_tool(row['id_location']),'exposed assembly code '+code,role)
        row.update(id_location=None,id_marking='Bag/tray label only; no hidden safe code land')
        if name=='Base':
            restore(o,old_text_tool('Soham Basanwar',(W/2-32,76 if role=='main' else 42),0,3.6,67,True),'exterior base owner name',role)
            row['personalization']='Unmarked: owner name requires a verified interior land'
            # The base's inner floor is at z=4.0. Avoid mount jaws and palm skin.
            for xy in ([(90,20),(100,76),(100,82)] if role=='main' else [(65,105),(145,105),(90,20)]):
                if put(o,row,'Soham Basanwar',3.6,4.0,xy,kind='owner',backing=2.0):break
            assert row.get('owner_location'),(role,'No inner base name land')
            for xy in ([(93,70),(140,76),(105,154),(170,150)] if role=='main' else [(150,76),(93,118),(100,37),(110,43)]):
                if put(o,row,code,3,4.0,xy,backing=2.0):break
            assert row.get('id_location'),(role,'No inner base code land')
        elif name=='Button_Cap':
            px,py=(117,145) if role=='main' else (49,95)
            restore(o,old_text_tool('SB',(px-2.3,py-6),H+4,2.4,4.7),'button top initials',role)
            row['personalization']='Unmarked: no safe hidden face'
            put(o,row,'SB',2.4,H-4.3,(px-2.4,py-6.6),True,kind='owner',backing=1.0)
            put(o,row,code,2.4,H-4.3,(px-3.8,py+3.5),True,backing=1.0)
        elif name=='Servo_Retainer':
            restore(o,old_text_tool('SB',(W-190-3,37),57.1,2.8,6),'servo retainer top initials',role)
            # Its underside is a servo contact and its arms flex. Leave it
            # unmarked physically rather than engrave those functional faces.
            row['personalization']='Unmarked: underside is servo contact; identify by bag and filename'
        elif name.endswith('_Shutter'):
            restore(o,shutter_old_tool(name,W),'external finger-tab initials',role)
            row['personalization']='Unmarked: no safe hidden face'
            shutter_mark(o,row,'SB',30 if name=='USB_Shutter' else 20,W)
            shutter_mark(o,row,code,35 if name=='USB_Shutter' else 25,W)
        elif name.startswith('Light_'):
            tag=name.split('_')[1]
            owner_xy,angle={'G1':((69,10.2),0),'G2':((169,10.2),0),'G3':((38.3,69),90),'G4':((193.5,69),90)}[tag]
            if row['personalization'].startswith('SB'):
                restore(o,code_tool(dict(label='SB',height_mm=2.2,angle_deg=angle,underside=False,xy_mm=owner_xy,z_mm=66.55)),'light bezel top initials',role)
            row['personalization']='Unmarked: thin bezel; owner name in filename'
            hidden_owner_xy=(67,10.2) if tag=='G1' else owner_xy
            put(o,row,'SB',2.2,64.95,hidden_owner_xy,True,angle,kind='owner')
            code_xy,angle={'G1':((61,10.2),0),'G2':((154,10.2),0),'G3':((38.3,59),90),'G4':((193.5,59),90)}[tag]
            put(o,row,code,2.2,64.95,code_xy,True,angle)
        row['mark_visibility']='Hidden when assembled' if row.get('owner_location') or row.get('id_location') else 'Bag/tray identification only'
        print('HIDDEN',role,name,row.get('id_location') is not None,row.get('owner_location') is not None,flush=True)
    if role=='main':
        row=next(r for r in rows if r['role']==role and r['name']=='Lid');o=d.Lid
        for tag,xy in {'G1':(55,32),'G2':(173,32),'G3':(52,70),'G4':(174,70)}.items():
            code=next(r['assembly_code'] for r in rows if r['name']=='Light_'+tag+'_Bezel')
            restore(o,code_tool(dict(label=code,height_mm=2.5,angle_deg=0,underside=False,xy_mm=xy,z_mm=64)),'top receiver code '+code,role)
            xy2,angle,z={'G1':((61,13),0,54),'G2':((159,13),0,54),'G3':((41,69),90,52),'G4':((190,69),90,52)}[tag]
            result=mark(o.Shape,code,2.6,z,xy2,True,angle)
            assert result,('hidden receiver',tag)
            o.Shape,loc=result;loc.update(role=role,name='Lid',kind='receiver',tag=tag)
            hidden_locations.append(loc)
        changed.add('Lid')
        coupon=d.Lid.Shape.common(box(24,7,22,72,39,45)).removeSplitter()
        solids=sorted(coupon.Solids,key=lambda s:s.Volume,reverse=True)
        assert sum(s.Volume for s in solids[1:])<15
        MeshPart.meshFromShape(Shape=solids[0],LinearDeflection=.08,AngularDeflection=.16,Relative=False).write(str(R/'fit-tests/M-lighting-G1-coupon-Soham-Basanwar.stl'))
    for row in [r for r in rows if r['role']==role]:
        o=d.getObject(row['name']);s=o.Shape
        assert s.isValid() and (row['component'] or len(s.Solids)==1)
        if not row['component']:
            prop(o,'Personalization',row['personalization']);prop(o,'AssemblyIdentification',row['id_marking']);prop(o,'MarkVisibility',row.get('mark_visibility','Internal or unmarked'))
        if row['name'] in changed:
            mesh=MeshPart.meshFromShape(Shape=s,LinearDeflection=.02 if row['name']=='Base' and role!='main' else .08,AngularDeflection=.16,Relative=False)
            for folder in ['render-meshes','prototype-stl']:mesh.write(str(R/folder/row['file']))
            before=source_shapes[row['name']]
            audit.append(dict(role=role,name=row['name'],added_mm3=s.cut(before).Volume,removed_mm3=before.cut(s).Volume,valid=True,solids=len(s.Solids)))
        row.update(volume_mm3=s.Volume,solids=len(s.Solids))
    d.recompute();save_document(d,R/'cad'/f'{role}-revision12.FCStd')
    Part.export(d.PrintedParts.Group,str(R/'cad'/f'{role}-printed-parts.step'))
    A.closeDocument(d.Name)
    print('SAVED',role,flush=True)
    (R/'scene.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    (R/'HIDDEN_MARKS.json').write_text(json.dumps(dict(restored_exterior_marks=removed_locations,new_hidden_marks=hidden_locations,modified_parts=audit),indent=2),encoding='utf-8')
ids=[dict(code=r['assembly_code'],role=r['role'],name=r['name'],marking=r['id_marking'],location=r.get('id_location')) for r in rows if not r['component']]
(R/'ASSEMBLY_IDS.json').write_text(json.dumps(ids,indent=2),encoding='utf-8')
(R/'HIDDEN_MARKS.json').write_text(json.dumps(dict(restored_exterior_marks=removed_locations,new_hidden_marks=hidden_locations,modified_parts=audit,policy='No ownership or assembly lettering on assembled exterior. Preserve functional symbols and internal adjustment arrows.'),indent=2),encoding='utf-8')
with (R/'PARTS.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=['assembly_code','role','name','quantity','file','id_marking','personalization','mark_visibility','notes']);w.writeheader()
    for r in rows:
        if not r['component']:w.writerow({k:(1 if k=='quantity' else r.get(k,'')) for k in w.fieldnames})
print('R12 COMPLETE',len(audit),'modified parts;',len(removed_locations),'exterior marks relocated/removed',flush=True)
