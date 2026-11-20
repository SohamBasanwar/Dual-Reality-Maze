"""Incremental R11 master. Uses the validated R10 native solids in baseline/.
Run with FreeCAD 1.1 bin/python.exe. All coordinates are final assembly mm.
R10 contains late fit corrections: do not substitute an older regenerated shell.
"""
from pathlib import Path
import json,math,csv,sys
import FreeCAD as A,Part,MeshPart
from safe_save import save_document
R=Path(__file__).resolve().parent; V=A.Vector
sys.path.insert(0,str(R))
from build_revision10 import box,cyl,ring,union,cut,stroke,text_cut,moved
rows=json.loads((R/'baseline'/'scene.json').read_text())
ids=[]; light_records=[]; geometry_checks=[]
selected=sys.argv[1:] or ['explorer','architect','main']
if sys.argv[1:] and (R/'ASSEMBLY_IDS.json').exists():
    rows=[r for r in json.loads((R/'scene.json').read_text()) if r['role'] not in selected]+[r for r in rows if r['role'] in selected]
    ids=[r for r in json.loads((R/'ASSEMBLY_IDS.json').read_text()) if r['role'] not in selected]
    geometry_checks=[r for r in json.loads((R/'R11_SOLID_CHECK.json').read_text()) if r['role'] not in selected]
    if 'main' not in selected:light_records=json.loads((R/'LIGHTING_LAYOUT.json').read_text())['channels']
for folder in ['cad','prototype-stl','render-meshes']: (R/folder).mkdir(exist_ok=True)

def prop(o,n,value):
    if not hasattr(o,n):o.addProperty('App::PropertyString',n)
    setattr(o,n,str(value))

def add(d,name,s,material='bronze',component=False,note='',explosion=(0,0,-20)):
    s=s.removeSplitter()
    assert s.isValid() and (len(s.Solids)==1 or component),(name,'invalid geometry',len(s.Solids))
    o=d.addObject('PartDesign::Feature',name);o.Shape=s
    (d.ComponentEnvelopes if component else d.PrintedParts).addObject(o)
    prop(o,'DesignNotes',note);prop(o,'Personalization','Unmarked: optical or fit-sensitive' if material!='bronze' else 'Pending safe-face engraving')
    rows.append(dict(role='main',name=name,file='',material=material,component=component,explosion=explosion,notes=note,personalization=o.Personalization,file_label='' if component else 'Soham Basanwar'))
    return o

def alter_main(d):
    lid=d.Lid.Shape
    # Fill the obsolete side exit in the original 52 mm light cup. Keep the
    # mask's upper retention slots and the existing RGB flange keeper intact.
    lid=union([lid,ring(117,108,46.8,26,24,13.6)])
    # A second concentric opaque skirt captures a removable labyrinth cap.
    skirt=ring(117,108,34.5,11.5,9,12.1)
    skirt=skirt.cut(ring(117,108,35.9,10.5,8.8,1.5))
    for dy in [-11.2,8.8]:skirt=skirt.cut(box(116.1,108+dy,34.4,1.8,2.6,3.1))
    lid=union([lid,skirt])
    shield=union([cyl(117,108,32.3,10.8,1.8),ring(117,108,34.0,8.7,7.1,4.7)])
    shield=union([shield,box(125.5,107.4,36.2,1.7,1.2,.9),box(106.8,107.4,36.2,1.7,1.2,.9)])
    # Offset passages, with an intervening opaque floor: cable route turns
    # inside the cap. Loose wires need a service loop; never twist LED leads.
    shield=union([shield,cyl(117,108,35.8,8,1.2)])
    shield=cut(shield,[box(113.5,111.5,32.1,7,2,2.2),box(113.5,102.9,35.6,7,2,1.6)])
    add(d,'RGB_Isolation_Cap',shield,note='Quarter-turn opaque cap under the existing RGB keeper. Offset cable passages reduce light escape. Disconnect flexible wire extension before rotating; do not twist LED legs. Physical light leakage and fit untested.')
    # Provisional space stays 60 x 32 x 18, centrally over the breadboard.
    # It is not a selected ESP32 or an assertion of header-pitch compatibility.
    for n in ['ESP32_Optional_Envelope','ESP32_Wiring_Clearance']:
        o=d.getObject(n);s=o.Shape.copy();s.translate(V(63,0,0));o.Shape=s
        prop(o,'DesignNotes',o.DesignNotes+' R11: shifted +63 mm in X to leave the four corner light wells clear.')
    rear=[(32,35),(42,20),(59,14),(79,14),(87,14)]
    front=[(42,60),(43,76),(60,87),(72,99)]
    specifications=[('G1',rear,(42,20)),('G2',[(234-x,y) for x,y in rear],(192,20)),('G3',front,(42,60)),('G4',[(234-x,y) for x,y in front],(192,60))]
    for tag,path,(x,y) in specifications:
        # An enclosed shallow optical gallery and a vertical feed well. The
        # four wells open over 5 mm LED references at breadboard corners.
        # Rear galleries bridge above the LCD key's entire withdrawal path.
        # Key top is z53.2; z54 leaves 0.8 mm nominal service clearance.
        floor_z=54 if tag in ['G1','G2'] else 52
        footprint=stroke(path,5.2,floor_z,64.2-floor_z)
        interior=stroke(path,3.6,floor_z+1.8,13)
        body=footprint.cut(interior)
        pipe=ring(x,y,22.8,7,5.5,floor_z+2.1-22.8)
        body=union([body,pipe]).cut(cyl(x,y,22.6,5.5,floor_z+3.3-22.6))
        # Roof slit is narrower than its diffuser, preserving a bearing ledge.
        slit=stroke(path,1.25,59.8,8)
        lid=union([lid,body]).cut(slit)
        # Clear any pre-existing raised decorative border underneath the lens.
        lid=lid.cut(stroke(path,3.05,64,4))
        lens=stroke(path,2.8,64.05,.8)
        # Low-profile bronze bezel; a 2.5 mm luminous line remains exposed.
        bezel=stroke(path,4.5,64.95,1.6).cut(stroke(path,1.25,64.8,2))
        # Two flexible snap legs on short straight portions. Nominal 0.2 mm
        # side clearance; 0.35 mm under-roof hook. Coupon/real-fit test needed.
        if tag in ['G1','G2']:
            mounts=[(42,17),(73,11)]
            if tag=='G2':mounts=[(234-a,b) for a,b in mounts]
        else:
            mounts=[(39,65),(57,88)]
            if tag=='G4':mounts=[(234-a,b) for a,b in mounts]
        for mx,my in mounts:
            leg=box(mx-1.5,my-.45,59.1,3,.9,6)
            # Hook faces outside the local light aperture; notch only through
            # roof, so the detent catches the underside at z60.2.
            hook=box(mx-1.5,my-.8,59.2,3,.7,.8)
            bezel=union([bezel,leg,hook])
            hole=box(mx-1.7,my-.65,60.05,3.4,1.3,5.2)
            lid=lid.cut(hole)
            # Locally clear the optical housing below the roof for the hook.
            lid=lid.cut(box(mx-1.8,my-1.1,58.8,3.6,1.9,1.3))
            lens=lens.cut(box(mx-1.7,my-.7,63.9,3.4,1.4,1.2))
        add(d,'Light_'+tag+'_Diffuser',lens,'green_diffuser',note=tag+': separate translucent/frosted lens; 0.8 mm nominal, not opaque bronze. Trapped beneath matching bezel. Thickness and illumination require a printed optical sample.',explosion=(0,0,25))
        add(d,'Light_'+tag+'_Bezel',bezel,note=tag+': low-profile bronze rune bezel. Insert lens first, then press two flexible legs into matching lid slots. Release from inside before removing. Prototype snap fit.',explosion=(0,0,35))
        led=union([cyl(x,y,24.2,2.5,6),cyl(x,y,23.4,2.9,1)]+[cyl(x+dx,y,19.3,.25,5) for dx in [-1.27,1.27]])
        add(d,'Green_'+tag+'_LED_Envelope',led,'green_led',True,tag+': nominal diffused 5 mm green LED on breadboard; lead spacing and exact row positions provisional.',(0,0,0))
        light_records.append(dict(tag=tag,path_xy_mm=path,led_xy_mm=[x,y],led_body_z_mm=[24.2,30.2],diffuser_thickness_mm=.8,window_width_mm=2.5,well_inner_diameter_mm=11,well_outer_diameter_mm=14,well_bottom_z_mm=22.8,gallery_floor_z_mm=floor_z))
    d.Lid.Shape=lid.removeSplitter()
    prop(d.Lid,'DesignNotes',d.Lid.DesignNotes+' R11: four enclosed green light galleries and 11 mm feed wells, sealed RGB cup side opening, secondary RGB skirt. Four green LEDs are breadboard mounted; no wire is to pass under a snap hook.')

def text_shape(label,h):
    wires=Part.makeWireString(label,'C:/Windows/Fonts/','arialbd.ttf',h)
    q=Part.makeCompound([Part.makeFace(w,'Part::FaceMakerBullseye') for w in wires if w])
    q.translate(V(-q.BoundBox.XMin,-q.BoundBox.YMin,0));return q

def place_mark(s,label,h,z,xy,underside=False,angle=0,backing=1.25):
    q=text_shape(label,h);q.rotate(V(),V(0,0,1),angle)
    if underside:q=q.mirror(V(),V(1,0,0))
    q.translate(V(xy[0]-q.BoundBox.XMin,xy[1]-q.BoundBox.YMin,z))
    b=q.BoundBox
    depth=.22
    # Verify whole label land, including space between strokes; preserve >1mm
    # of solid material behind it. Existing name/arrow cuts reject candidates.
    land=box(b.XMin-.12,b.YMin-.12,z-backing if not underside else z-.01,b.XLength+.24,b.YLength+.24,backing+.01)
    if s.common(land).Volume<land.Volume*.985:return None
    tool=q.extrude(V(0,0,depth+.02 if underside else -depth-.02))
    if s.common(tool).Volume<tool.Volume*.85:return None
    result=s.cut(tool).removeSplitter()
    if not result.isValid() or len(result.Solids)!=1:return None
    return result,dict(label=label,xy_mm=xy,z_mm=z,angle_deg=angle,underside=underside,height_mm=h,removed_mm3=s.Volume-result.Volume)

def mark_id(s,name,role,code):
    # Explicit noncontact lands for shells. Avoid palm surfaces and existing
    # owner lettering. All other marks are limited to selected rigid families.
    if name=='Base':
        return place_mark(s,code,3,0,(93,64 if role=='main' else 62),True)
    if name=='Lid':return place_mark(s,code,2.8,60.2 if role=='main' else 54.2,(76,75) if role=='main' else (100,91),True)
    if name=='Battery_Door':
        return place_mark(s,code,2.4,2.4 if role=='main' else 2.55,(185,132) if role=='main' else (195,154))
    if name.endswith('_Height_Insert'):
        b=s.BoundBox
        # Long return bar is clear of existing ownership text on the rear bar.
        return place_mark(s,code,2.2,b.ZMax,(b.XMax-3.0,b.YMin+8),angle=90,backing=.9)
    if name=='RGB_Isolation_Cap':return place_mark(s,code,2.4,32.3,(113,107.7),True)
    if name.startswith('Light_') and name.endswith('_Bezel'):
        tag=name.split('_')[1]
        xy,angle={'G1':((61,10.2),0),'G2':((160,10.2),0),'G3':((38.3,61),90),'G4':((193.5,61),90)}[tag]
        r=place_mark(s,code,2.2,66.55,xy,angle=angle)
        if r:return r
        return None
    if name=='Gate_Frame':return place_mark(s,code,2.2,40.3,(40,65),True)
    if name=='Switch_Cassette':return place_mark(s,code,2.2,59.25,(114.3713,136.0298))
    if name.endswith(('_Jaw','_Lock_Key','_Carrier')):return None
    allowed=name.endswith(('_Height_Insert','_Jaw','_Carrier','_Bezel')) or name in ['Servo_Cassette','Servo_Retainer','Gate_Frame','Switch_Cassette','RGB_Isolation_Cap']
    if not allowed:return None
    z=s.BoundBox.ZMax
    for f in sorted([f for f in s.Faces if f.BoundBox.ZLength<1e-6 and abs(f.BoundBox.ZMax-z)<1e-6],key=lambda f:f.Area,reverse=True):
        b=f.BoundBox
        for h in [2.2,2.0]:
            for angle in [0,90]:
                q=text_shape(code,h);q.rotate(V(),V(0,0,1),angle);w=q.BoundBox.XLength;d=q.BoundBox.YLength
                if w+.5>b.XLength or d+.5>b.YLength:continue
                # Deterministic search, small bounded number of lands.
                for fy in [.05,.95,.5,.25,.75]:
                    for fx in [.05,.95,.5,.25,.75]:
                        xy=(b.XMin+.25+(b.XLength-w-.5)*fx,b.YMin+.25+(b.YLength-d-.5)*fy)
                        r=place_mark(s,code,h,z,xy,angle=angle,backing=.9 if name.endswith('_Height_Insert') else 1.25)
                        if r:return r
    return None

for role in selected:
    print('BEGIN',role,flush=True)
    doc=A.openDocument(str(R/'baseline'/f'{role}-revision10.FCStd'))
    if role=='main':alter_main(doc)
    role_rows=[r for r in rows if r['role']==role]
    ordered=sorted([r for r in role_rows if not r['component']],key=lambda r:(['Base','Lid','Battery_Door'].index(r['name']) if r['name'] in ['Base','Lid','Battery_Door'] else 3,r['name']))
    for i,r in enumerate(ordered,1):
        code=role[0].upper()+f'{i:02}'
        obj=doc.getObject(r['name']);res=mark_id(obj.Shape,r['name'],role,code)
        marking='Bag/tray label only; no safe readable noncontact engraving land'
        location=None
        if res:obj.Shape,location=res;marking='Engraved '+code+' on noncontact face'
        if r['name'].startswith('Light_') and r['name'].endswith('_Bezel'):
            tag=r['name'].split('_')[1]
            xy,angle={'G1':((69,10.2),0),'G2':((169,10.2),0),'G3':((38.3,69),90),'G4':((193.5,69),90)}[tag]
            owner=place_mark(obj.Shape,'SB',2.2,66.55,xy,angle=angle)
            prop(obj,'Personalization','SB — noncontact upper border' if owner else 'Unmarked: no safe noncontact ownership land; full name in filename')
            if owner:obj.Shape=owner[0]
        elif r['name']=='RGB_Isolation_Cap':
            owner=place_mark(obj.Shape,'SB',2.4,32.3,(113.5,103.8),True)
            if owner:obj.Shape=owner[0];prop(obj,'Personalization','SB — outside bottom face')
            else:prop(obj,'Personalization','Unmarked: no safe noncontact ownership land; full name in filename')
        prop(obj,'AssemblyCode',code);prop(obj,'AssemblyIdentification',marking)
        r.update(assembly_code=code,id_marking=marking,id_location=location)
        obj.Label=code+' | '+r['name'].replace('_',' ')+' | Soham Basanwar'
        ids.append(dict(code=code,role=role,name=r['name'],marking=marking,location=location))
        print(code,r['name'],bool(res),flush=True)
    if role=='main':
        # Matching receiver codes, visible when placing each bezel. These
        # are shallow cuts in solid roof lands away from light apertures.
        for tag,xy in {'G1':(55,32),'G2':(173,32),'G3':(52,70),'G4':(174,70)}.items():
            code=next(r['assembly_code'] for r in ordered if r['name']=='Light_'+tag+'_Bezel')
            match=place_mark(doc.Lid.Shape,code,2.5,64,xy)
            if match:doc.Lid.Shape=match[0]
    for r in role_rows:
        o=doc.getObject(r['name']);s=o.Shape
        assert s.isValid() and (r['component'] or len(s.Solids)==1),(role,r['name'],'solid check')
        filename=(r.get('assembly_code','REF')+'-'+role+'-'+r['name']+('—Soham-Basanwar' if not r['component'] else '')+'.stl')
        mesh=MeshPart.meshFromShape(Shape=s,LinearDeflection=.02 if r['name']=='Base' and role!='main' else .08,AngularDeflection=.16,Relative=False)
        mesh.write(str(R/'render-meshes'/filename))
        if not r['component']:mesh.write(str(R/'prototype-stl'/filename))
        r.update(file=filename,volume_mm3=s.Volume,solids=len(s.Solids),notes=getattr(o,'DesignNotes',''),personalization=getattr(o,'Personalization','Reference'))
        geometry_checks.append(dict(role=role,name=r['name'],component=r['component'],valid=s.isValid(),solids=len(s.Solids),volume_mm3=s.Volume))
    prop(doc.DesignParameters,'Regeneration','Run build_revision11.py against included baseline R10 native files. R11 adds lighting and IDs without discarding late R10 fit corrections.')
    doc.recompute();save_document(doc,R/'cad'/f'{role}-revision11.FCStd')
    Part.export(doc.PrintedParts.Group,str(R/'cad'/f'{role}-printed-parts.step'))
    A.closeDocument(doc.Name)
    print('EXPORTED',role,flush=True)
(R/'scene.json').write_text(json.dumps(rows,indent=2))
(R/'ASSEMBLY_IDS.json').write_text(json.dumps(ids,indent=2))
(R/'LIGHTING_LAYOUT.json').write_text(json.dumps(dict(colour='green',led_count=4,rgb_isolated=True,channels=light_records,physical_optical_test=False,uniformity_verified=False),indent=2))
(R/'R11_SOLID_CHECK.json').write_text(json.dumps(geometry_checks,indent=2))
with (R/'PARTS.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.DictWriter(f,fieldnames=['assembly_code','role','name','quantity','file','id_marking','personalization','notes']);w.writeheader()
    for r in rows:
        if not r['component']:w.writerow({k:(1 if k=='quantity' else r.get(k,'')) for k in w.fieldnames})
print('R11 complete',len(ids),'installed pieces;',sum(i['location'] is not None for i in ids),'physically coded',flush=True)
