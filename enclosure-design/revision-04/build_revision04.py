"""Revision 04: dimensioned prototype solids, not a physical-fit certification.
Run with FreeCAD's bundled bin/python.exe. Millimetres throughout.
The source and dimensions.json are the parametric master; FCStd contains editable solids.
"""
import json, math, os
from pathlib import Path
import FreeCAD as App
import Part, MeshPart

ROOT=Path(__file__).resolve().parent
P=json.loads((ROOT/'dimensions.json').read_text())
V=App.Vector
OUT=ROOT/'cad'; OUT.mkdir(exist_ok=True)
STL=ROOT/'prototype-stl'; STL.mkdir(exist_ok=True)
RENDER=ROOT/'render-meshes'; RENDER.mkdir(exist_ok=True)
all_records=[]; checks=[]

def box(x,y,z,w,d,h): return Part.makeBox(w,d,h,V(x,y,z))
def cyl(x,y,z,r,h): return Part.makeCylinder(r,h,V(x,y,z))
def face(points): return Part.Face(Part.makePolygon([V(x,y,0) for x,y in points+[points[0]]]))
def union(shapes):
    if all(s.BoundBox.ZLength<1e-7 for s in shapes):
        solids=[s.extrude(V(0,0,1)) for s in shapes]
        s=solids[0].multiFuse(solids[1:]).removeSplitter() if len(solids)>1 else solids[0]
        top=max([f for f in s.Faces if f.BoundBox.ZLength<1e-7],key=lambda f:f.CenterOfMass.z)
        top.translate(V(0,0,-1));return top
    a=shapes[0]
    if len(shapes)>1: a=a.multiFuse(shapes[1:])
    return a.removeSplitter()
def cut(a,shapes):
    return a.cut(Part.makeCompound(shapes)).removeSplitter() if shapes else a
def moved(shape,x=0,y=0,z=0):
    a=shape.copy(); a.translate(V(x,y,z)); return a
def extr(f,z,h): return moved(f,z=z).extrude(V(0,0,h))
def rr(x,y,w,d,r):
    es=[]
    pts=[(x+r,y),(x+w-r,y),(x+w,y+r),(x+w,y+d-r),(x+w-r,y+d),(x+r,y+d),(x,y+d-r),(x,y+r)]
    mids=[(x+w-r+r/math.sqrt(2),y+r-r/math.sqrt(2)),(x+w-r+r/math.sqrt(2),y+d-r+r/math.sqrt(2)),(x+r-r/math.sqrt(2),y+d-r+r/math.sqrt(2)),(x+r-r/math.sqrt(2),y+r-r/math.sqrt(2))]
    for i in range(4):
        p1=V(*pts[2*i],0);p2=V(*pts[2*i+1],0);p3=V(*pts[(2*i+2)%8],0)
        es.extend([Part.makeLine(p1,p2),Part.Arc(p2,V(*mids[i],0),p3).toShape()])
    return Part.Face(Part.Wire(es))
def capsule(x1,y1,x2,y2,r):
    dx=x2-x1;dy=y2-y1;L=math.hypot(dx,dy);nx=-dy/L*r;ny=dx/L*r
    return union([Part.Face(Part.Wire([Part.makeCircle(r,V(x1,y1,0))])),Part.Face(Part.Wire([Part.makeCircle(r,V(x2,y2,0))])),face([(x1+nx,y1+ny),(x2+nx,y2+ny),(x2-nx,y2-ny),(x1-nx,y1-ny)])])
def offset(f,d):
    if f.ShapeType not in ['Face','Wire','Edge']: f=Part.Face(f.Wires)
    a=f.makeOffset2D(d,join=0).removeSplitter()
    return a.Faces[0] if len(a.Faces)==1 else a
def loft(f,levels):
    return Part.makeLoft([moved(offset(f,inset) if inset else f,z=z).OuterWire for z,inset in levels],True,True)
def stroke(points,r=0.65,z=0,h=0.8):
    return union([extr(capsule(*a,*b,r),z,h) for a,b in zip(points,points[1:])])
def ring(x,y,z,ro,ri,h):return cyl(x,y,z,ro,h).cut(cyl(x,y,z-0.1,ri,h+0.2))
def rounded_edge(s,z,radius):
    edges=[e for e in s.Edges if e.BoundBox.ZLength<1e-6 and abs(e.BoundBox.ZMin-z)<1e-6]
    for r in [radius,1.5,.8]:
        try:
            candidate=s.makeFillet(r,edges)
            if candidate.isValid():return candidate
        except Exception:pass
    raise RuntimeError('Could not round shell edge')

def build(role):
    main=role=='main'; W=234 if main else 246; D=172 if main else 203; H=64 if main else 58; split=H-16
    doc=App.newDocument('DRM_'+role+'_R04')
    meta=doc.addObject('App::FeaturePython','DesignParameters')
    meta.addProperty('App::PropertyString','Status');meta.Status='PROTOTYPE — component measurements and powered tests required'
    meta.addProperty('App::PropertyString','Regeneration');meta.Regeneration='Edit dimensions.json and run build_revision04.py with FreeCAD Python'
    for name,value in [('NominalWidth',W),('NominalDepth',D),('ShellHeight',H)]:
        meta.addProperty('App::PropertyLength',name);setattr(meta,name,value)
    shell_group=doc.addObject('App::DocumentObjectGroup','PrintedParts')
    env_group=doc.addObject('App::DocumentObjectGroup','ComponentEnvelopes')
    records=[]; bodies={}; envs={}
    def add(name,shape,material='bronze',component=False,explosion=(0,0,0),notes=''):
        shape=shape.removeSplitter()
        if not shape.isValid() or not shape.Solids: raise RuntimeError(f'{role}/{name}: invalid solid')
        if not component and len(shape.Solids)!=1: raise RuntimeError(f'{role}/{name}: disconnected printed part')
        exported=shape.mirror(V(W/2,0,0),V(1,0,0))
        ob=doc.addObject('PartDesign::Feature',name);ob.Label=name.replace('_',' ');ob.Shape=exported
        ob.addProperty('App::PropertyString','ManufacturingStatus');ob.ManufacturingStatus='REFERENCE ENVELOPE' if component else 'Prototype; fit unverified'
        ob.addProperty('App::PropertyString','DesignNotes');ob.DesignNotes=notes
        (env_group if component else shell_group).addObject(ob)
        mesh=MeshPart.meshFromShape(Shape=exported,LinearDeflection=0.13,AngularDeflection=0.22,Relative=False)
        filename=f'{role}-{name}.stl';mesh.write(str(RENDER/filename))
        if not component: mesh.write(str(STL/filename));bodies[name]=shape
        else:envs[name]=shape
        rec={'role':role,'name':name,'file':filename,'material':material,'component':component,'explosion':explosion,'volume_mm3':shape.Volume,'solids':len(shape.Solids),'notes':notes}
        records.append(rec)
        checks.append({'role':role,'part':name,'valid_brep':shape.isValid(),'solids':len(shape.Solids),'volume_mm3':round(shape.Volume,2),'component':component})
        return shape

    if main:
        raw=face([(28,6),(206,6),(228,28),(228,144),(206,166),(28,166),(6,144),(6,28)])
        outer=offset(raw,6)
    else: outer=union([rr(0,0,W,138,30),capsule(42,119,36,174,29),capsule(W-42,119,W-36,174,29)])
    outer=Part.Face(outer.Wires)
    inner=offset(outer,-3.2)
    # Sculpted bottom and upper shoulder; broad surfaces keep palms away from seams.
    base=rounded_edge(extr(outer,0,split),0,2.5).cut(extr(inner,4,split+1))
    lid=rounded_edge(extr(outer,split,H-split),H,3.5).cut(extr(inner,split-.1,H-split-3.9))
    skirt=extr(offset(outer,-3.65).cut(offset(outer,-5.45)),split-4,5)
    skirt_bridge=extr(offset(outer,-2.8).cut(offset(outer,-5.45)),split,2)
    lid=union([lid,skirt,skirt_bridge])
    bb=P['breadboard']; uno=P['uno_r4' if main else 'uno_r3']
    bx,by=(34,12) if main else (40,70)
    ux,uy=(88,91) if main else (89,10)
    batx,baty=(23,98) if main else (25,129)
    batt=P['battery_reservation']; bay=rr(batx-.6,baty-.6,batt[0]+1.2,batt[1]+1.2,2)
    base=base.cut(extr(bay,-1,6.5))
    # Battery is loaded through the underside, independently of the electronics lid.
    baywall=extr(offset(bay,2.0).cut(bay),3.5,24)
    baywall=cut(baywall,[box(batx+9,baty-4,17,12,6,7)]) # terminal/wire passage
    # Internal battery ledges allow a 2.5 mm latch clearance beneath the cell.
    rails=[box(batx-2,baty+10,4.8,4.8,45,2.2),box(batx+27.5,baty+10,4.8,4.5,45,2.2)]
    base=union([base,baywall]+rails)
    # Door rim recess, static locating-tab pockets, and a separate release opening.
    door_profile=rr(batx-2.2,baty-2.2,batt[0]+4.4,batt[1]+4.4,3)
    base=base.cut(extr(offset(door_profile,.3),-.2,2.7))
    base=cut(base,[box(batx+3,baty-5,2.2,7,4.4,1.6),box(batx+20,baty-5,2.2,7,4.4,1.6),box(batx+10,baty+batt[1]-1,2.4,10,4.6,2.3)])
    door=extr(door_profile,.3,2.1)
    door=cut(door,[box(batx+9.2,baty+45,0,0.8,19,4),box(batx+20,baty+45,0,.8,19,4)])
    tabs=[box(batx+3.4,baty-4.4,2.2,6.2,3.5,1.0),box(batx+20.4,baty-4.4,2.2,6.2,3.5,1.0)]
    hook=box(batx+10.1,baty+batt[1]-.5,2.0,9.7,2.2,1.7)
    door=union([door,hook]+tabs)
    # Underside recessed finger purchase; never pry against the battery terminals.
    door=door.cut(extr(rr(batx+11,baty+49,8,8,2),-.1,1.0))
    add('Battery_Door',door,'bronze',explosion=(0,0,-28),notes='Two leading tabs plus recessed cantilever latch. Trial fit coupon before use.')
    # Internal stop prevents the battery rising into wiring. Removable through the large lid.
    stop=box(batx-1.8,baty+22,26,33.6,5,2)
    base=union([base,stop])

    def tray(x,y,w,d,z=5,height=4):
        return extr(rr(x-2,y-2,w+4,d+4,2).cut(rr(x-.3,y-.3,w+.6,d+.6,1)),3.8,height+z-3.8)
    # Breadboard is located in three axes by rails and four flexible retaining fingers.
    base=union([base,tray(bx,by,bb[0],bb[1])])
    for xx in [bx+15,bx+bb[0]-23]:
        for yy,s in [(by-2.8,1),(by+bb[1]+1.4,-1)]:
            leaf=box(xx,yy,3.8,8,1.4,13)
            lip=box(xx,yy+(1.2 if s==1 else -1.4),15.1,8,1.6,1.7)
            base=union([base,leaf,lip])
    # UNO cradle uses edge supports and reusable non-metallic straps through anchor tunnels.
    # No PCB screw holes are assumed from unscaled photographs.
    base=union([base,tray(ux,uy,uno[0],uno[1],z=7,height=2)])
    for xx in [ux+5,ux+uno[0]-9]:
        for yy in [uy+1,uy+uno[1]-5]: base=union([base,box(xx,yy,3.8,4,4,3.2)])
    for xx in [ux-7,ux+uno[0]+2]:
        for yy in [uy+10,uy+uno[1]-18]:
            anch=box(xx,yy,3.8,5,8,5.2).cut(box(xx-1,yy+2,5.2,7,4,2))
            base=union([base,anch])
    # Cable entry/strain-relief saddle; one sleeved tether per handheld device.
    cablexs=[78,156] if main else [123]
    for xx in cablexs:
        entry=Part.makeCylinder(5.2,16,V(xx,-3,24),V(0,1,0));base=base.cut(entry)
        saddle=box(xx-9,1,20,18,11,11).cut(Part.makeCylinder(4.8,14,V(xx,0,24),V(0,1,0)))
        saddle=saddle.cut(box(xx-10,7,28,20,3,2))
        base=union([base,saddle])
    # Snap latches: press recessed side windows to release; no screws anywhere.
    latchys=[82] if not main else [77]
    for side in [0,1]:
        xx=3.65 if side==0 else W-5.05
        for yy in latchys:
            lid=lid.cut(box(xx-.6,yy-1,split-4.1,2.7,14,16.1))
            leaf=box(xx,yy,H-29,1.4,12,25)
            anchor=box(xx if side==0 else xx-3,yy,H-6,4.4,12,2.5)
            hook=box(xx-1 if side==0 else xx+1.2,yy,H-28,1.2,12,2.1)
            lid=union([lid,leaf,anchor,hook])
            base=base.cut(box(-1 if side==0 else W-4,yy-.4,H-28.3,5,12.8,2.8))
    # Two rear tabs locate the lid; side snaps retain it. Lift the front then disengage rear.
    for xx in [63,W-69]:
        tab=box(xx,2.4,split-3.8,6,5.5,2.2)
        bridge=box(xx,4.5,split-3.8,6,2.2,6)
        lid=union([lid,tab,bridge])
        base=base.cut(box(xx-.35,1.9,split-4.15,6.7,5.9,2.9))

    emblem=(117,108) if main else (123,42)
    ex,ey=emblem
    lid=lid.cut(cyl(ex,ey,H-16,24.3,20))
    # Light cup hangs from the lid, with a 5 mm LED seat and lead exit.
    cup=ring(ex,ey,H-17,26,24,17)
    cup=union([cup,cyl(ex,ey,H-18,26,2.4)])
    cup=cut(cup,[cyl(ex,ey,H-19,2.65,5),box(ex-4,ey-27,H-15,8,5,3)])
    lid=union([lid,cup])
    # Diffuser disk seats on the lower ring; face mask is retained by two small opposed tabs.
    lens=cyl(ex,ey,H+.05,24,1.2)
    lens=cut(lens,[box(ex+dx-.2,ey-3.2,H,1.7,6.4,2) for dx in [-25,23.7]])
    add('Emblem_Diffuser',lens,'diffuser',explosion=(0,0,52),notes='Separate translucent sheet/print; opaque bronze cannot transmit light.')
    mask=cyl(ex,ey,H+1.3,26,1.8)
    mask_slots=[]
    # All apertures remain open-ended; no loose floating islands in the mask.
    if role=='explorer':
        mask_slots += [stroke([(ex-15,ey),(ex-7,ey-7),(ex,ey-9),(ex+7,ey-7),(ex+15,ey)],.9,H+1,3),stroke([(ex-13,ey+2),(ex-6,ey+7),(ex+6,ey+7),(ex+13,ey+2)],.9,H+1,3)]
        mask_slots += [stroke([(ex,ey-19),(ex,ey-13)],1,H+1,3),stroke([(ex,ey+12),(ex,ey+19)],1,H+1,3),stroke([(ex-21,ey),(ex-18,ey)],1,H+1,3),stroke([(ex+18,ey),(ex+21,ey)],1,H+1,3)]
        # A split pupil glows without separating the central mask island.
        for a,b in [(-65,65),(115,245)]:
            pts=[(ex+4.5*math.cos(math.radians(t)),ey+4.5*math.sin(math.radians(t))) for t in range(a,b+1,10)]
            mask_slots.append(stroke(pts,.8,H+1,3))
    elif role=='architect':
        mask_slots += [stroke([(ex-12,ey+14),(ex-12,ey-5),(ex-7,ey-12),(ex+7,ey-12),(ex+12,ey-5),(ex+12,ey+14)],1,H+1,3)]
        for dx in [-5,0,5]:mask_slots.append(stroke([(ex+dx,ey-5),(ex+dx,ey+12)],.8,H+1,3))
        mask_slots.append(stroke([(ex-6,ey-16),(ex,ey-21),(ex+6,ey-16)],.8,H+1,3))
    else:
        for rad,a,b in [(18,20,320),(11,-20,260)]:
            pts=[(ex+rad*math.cos(math.radians(t)),ey+rad*math.sin(math.radians(t))) for t in range(a,b+1,10)]
            mask_slots.append(stroke(pts,.9,H+1,3))
        mask_slots.append(stroke([(ex,ey-6),(ex+4,ey),(ex,ey+6),(ex-4,ey)],.8,H+1,3))
    mask=cut(mask,mask_slots)
    # Positive press tabs to be fitted by coupon; edges trap lens against the cup rim.
    for dx in [-25,23.7]:mask=union([mask,box(ex+dx,ey-3,H-2,1.3,6,4)])
    lid=cut(lid,[box(ex+dx-.2,ey-3.2,H-2.3,1.7,6.4,5) for dx in [-25,23.7]])
    add('Emblem_Mask',mask,'bronze',explosion=(0,0,57))
    # Low relief ornamental border, printable in one structural filament.
    border=extr(offset(outer,-8).cut(offset(outer,-9.2)),H-.35,.95)
    # Trim away decoration on sloping grip tips: remaining detail joins the lid roof.
    border=border.common(extr(offset(outer,-4),H-.4,1.1))
    lid=union([lid,border])
    # Local control placement and holders.
    if not main:
        cx,cy=49,42
        if role=='explorer':
            lid=lid.cut(cyl(cx,cy,H-12,14.2,20))
            jx,jy=cx-17,cy-13
            carrier=extr(rr(jx-2,jy-2,38,30,3).cut(rr(jx-.35,jy-.35,34.7,26.7,2)),H-24,15)
            # Captive carrier is part of lid, with removable strap tunnels at its corners.
            for xx in [jx-2,jx+34]:carrier=union([carrier,box(xx,jy,H-24,2,26,20)])
            lid=union([lid,carrier])
            for xx in [jx-3,jx+33]:lid=lid.cut(box(xx,jy+5,H-22,5,5,2.5))
            lid=lid.cut(cyl(197,42,H-8,3.2,15))
            sensor=ring(197,42,H-9,5.2,3.2,9)
            lid=union([lid,sensor])
            add('Joystick_PCB',box(jx,jy,H-23.5,34,26,1.6),'pcb',True)
            add('Joystick_Mechanism',union([box(cx-9,cy-9,H-22,18,18,15),cyl(cx,cy,H-7,6,12),cyl(cx,cy,H+3,12,5)]),'black',True)
            add('Bare_Light_Sensor',cyl(197,42,H-2,2.7,2),'sensor',True)
        else:
            lid=lid.cut(cyl(cx,cy,H-18,4,25))
            potcup=ring(cx,cy,H-17,10.3,8.3,17)
            potcup=cut(potcup,[box(cx-12,cy-4,H-17,24,8,8)])
            lid=union([lid,potcup])
            add('Potentiometer_Envelope',union([cyl(cx,cy,H-15,8,10),cyl(cx,cy,H-5,3,18)]),'metal',True,notes='16 mm body / 6 mm shaft placeholder. Product image does not establish actual dimensions.')
            add('Bronze_Knob_Envelope',cyl(cx,cy,H+1,11,14),'knob',True)
            # Upper shoulder gate cassette, separate from thumb and grip area.
            gx,gy=196,32
            lid=lid.cut(box(gx-17,gy-10,H-15,34,20,20))
            collar=extr(rr(gx-23,gy-15,46,30,5).cut(rr(gx-17.3,gy-10.3,34.6,20.6,3)),H-1,4)
            lid=union([lid,collar])
            # Sideways servo: horn axis points forward (+Y); crank turns in the XZ plane.
            # This converts rotation into vertical travel through a slotted gate crossbar.
            sy=gy-16; axle_x=gx-5; axle_z=H+18
            servo=box(gx-11.5,sy,H+6,23,29,12.2)
            add('SG90_Body_Envelope',servo,'servo',True,notes='Sideways placement. Shaft offset, ears and exact horn geometry require measurement.')
            cassette=extr(rr(gx-15,sy-2,30,34,3).cut(rr(gx-12,sy-.4,24,29.8,1)),H+3,19)
            cassette=union([cassette,box(gx-15,sy-2,H+3,30,34,2.5)])
            cassette=cut(cassette,[box(gx-4,sy-3,H+9,8,6,6)])
            cassette=cassette.cut(Part.makeCylinder(10.2,7,V(axle_x,sy+27,axle_z),V(0,1,0)))
            # The tongue keys the cartridge into the collar; ties retain it for servicing.
            cassette=union([cassette,box(gx-16,gy-9,H-2,32,18,6)])
            for xx in [gx-14,gx+11]:cassette=cassette.cut(box(xx,sy+8,H+5,3,6,5))
            add('Servo_Cassette',cassette,'bronze',explosion=(0,0,38))
            fy=gy+19
            frame=union([box(gx-22,fy-3,H+3,6,8,53),box(gx+16,fy-3,H+3,6,8,53),box(gx-22,fy-3,H+52,44,8,6)])
            frame=cut(frame,[box(gx-18,fy-.4,H+6,2.4,3.1,45),box(gx+15.6,fy-.4,H+6,2.4,3.1,45)])
            # Foundation joins the lower collar and protects the rotating drive below the opening.
            foot=box(gx-23,sy-3,H+3.3,46,fy-sy+8,3)
            frame=union([frame,foot])
            frame=frame.cut(box(gx-16.4,gy-9.4,H,32.8,18.8,5))
            frame=frame.cut(box(gx-15.4,sy-2.4,H+2.7,30.8,34.8,4))
            for xx in [gx-20,gx+17]:frame=frame.cut(box(xx,gy-10,H,3,6,5))
            add('Gate_Frame',frame,'bronze',explosion=(0,0,65))
            # Closed pose theta=-60deg. Radius 7 gives 12.12 mm lift over -60..+60deg.
            closed_z=axle_z-7*math.sin(math.pi/3)
            panel=union([box(gx-17,fy,closed_z-3,34,2.2,6),box(gx-17,fy,closed_z+23,34,2.2,3)]+[box(gx+t,fy,closed_z,2,2.2,26) for t in [-17,-9,-1,7,15]])
            # Yoke slot faces the crank and accepts a captive sliding pin; no thread.
            panel=panel.cut(box(axle_x+1.5,fy-.2,closed_z-1.5,8,3,3))
            add('Gate_Panel',panel,'bronze',explosion=(0,0,80),notes='Scotch-yoke concept: 7 mm crank, +/-60 degrees, nominal lift 12.12 mm. Load and horn fit unverified.')
            crank=Part.makeCylinder(4,2,V(axle_x,fy-3,axle_z),V(0,1,0))
            crank=union([crank,box(axle_x,fy-3,closed_z-1,5.5,2,axle_z-closed_z+2)])
            add('Original_Horn_Envelope',crank,'white',True,notes='Placeholder for supplied nylon horn, not a fabricated spline.')
            pin=union([Part.makeCylinder(1.2,6.3,V(axle_x+3.5,fy-4,closed_z),V(0,1,0)),Part.makeCylinder(2.1,1.2,V(axle_x+3.5,fy+2.2,closed_z),V(0,1,0))])
            add('Gate_Drive_Pin',pin,'bronze',explosion=(0,18,65),notes='Trial captive pin. Match supplied horn hole before printing; keeper limits axial movement.')
            # Back/side shroud conceals the motor. Slotted front shield isolates moving fingers.
            shroud=extr(rr(gx-25,sy-5,50,fy-sy+13,4).cut(rr(gx-22.5,sy-2.5,45,fy-sy+8,.5)),H+6.6,54.4)
            frontslots=[box(gx-19+i*6,fy+5,H+26,3,6,29) for i in range(7)]
            backslots=[box(gx-19+i*6,sy-6,H+27,3,6,28) for i in range(7)]
            sideslots=[box(gx+xx,sy+3+i*6,H+27,6,3,28) for xx in [-26,20] for i in range(5)]
            shroud=cut(shroud,frontslots+backslots+sideslots+[box(gx-8,sy-7,H+5,16,7,10)])
            # Top keeper closes the rail ends so the slider cannot escape upward.
            shroud=union([shroud,box(gx-23,fy-3,H+59,46,9,2)])
            add('Gate_Shroud',shroud,'bronze',explosion=(0,0,92),notes='Removable guard and axial keeper concept; check pinch access, slot widths and full servo sweep physically.')
            # Actuator at thumb position, away from moving gate.
    # Captured tactile button: Architect confirmation / Main power-control input.
    if role!='explorer':
        px,py=(117,145) if main else (197,95)
        lid=lid.cut(cyl(px,py,H-17,8.4,25))
        guide=ring(px,py,H-13,11.2,8.4,14)
        guide=guide.cut(cyl(px,py,H-13.1,10.35,10.5))
        lid=union([lid,guide]).cut(cyl(px,py,H-13.1,10.35,10.5))
        lid=lid.cut(extr(rr(px-9.3,py-9.3,18.6,18.6,2),H-13.1,2.6))
        # Cap is inserted from below. Flange prevents loss; hard stop limits downward travel.
        cap=union([cyl(px,py,H-4.3,10,1.5),cyl(px,py,H-3,7.9,7),cyl(px,py,H-9.3,2.5,5.3)])
        if main:
            cap=cap.cut(stroke([(px,py-4),(px,py+.2)],.55,H+3.35,1))
        else:
            cap=cap.cut(stroke([(px-3,py),(px-.5,py+2.5),(px+4,py-3)],.65,H+3.35,1))
        add('Button_Cap',cap,'bronze',explosion=(0,0,35),notes='Guided actuator, retaining flange and adjustable pusher. 0.3 mm radial clearance; tune switch travel.')
        # Switch cassette slides in from below and is retained by a removable U clip.
        cradle=extr(rr(px-9,py-9,18,18,2).cut(rr(px-6.35,py-6.35,12.7,12.7,1)),H-17,6.2)
        cradle=union([cradle,box(px-9,py-9,H-17,18,18,1.4)])
        cradle=cut(cradle,[box(px-10,py-4,H-16,20,8,2.2)])
        cradle=union([cradle,ring(px,py,H-6,10.1,4,1.25),box(px-8.5,py-2,H-15,2,4,10),box(px+6.5,py-2,H-15,2,4,10)])
        add('Switch_Cassette',cradle,'bronze',explosion=(0,0,-10))
        add('Tactile_Switch_Envelope',box(px-6,py-6,H-15.4,12,12,6),'black',True,notes='Looks like 12 mm family in photos; body size and operating travel unmeasured.')
        # Mounting pillars connect to roof, leaving two strap tunnels for screwless service retention.
        for xx in [px-13,px+11]:
            support=box(xx,py-9,H-17,2,18,14)
            support=support.cut(box(xx-1,py-3,H-15.5,4,6,2))
            lid=union([lid,support])
    if main:
        # LCD roof opening with bezel; small tilt is carried by the separate wedge cradle.
        lx,ly=76.7,25
        lid=lid.cut(box(lx+4,ly+4,H-20,72,26,25))
        bezel=extr(rr(lx-2,ly-2,84.6,40,4).cut(rr(lx+3.5,ly+3.5,73,27,2)),H-.3,2.1)
        lid=union([lid,bezel])
        lcdframe=extr(rr(lx-2,ly-2,84.6,40,3).cut(rr(lx-.4,ly-.4,81.4,36.8,1)),H-22,17)
        # Rear support is 2 mm higher over 36 mm: nominal ~3 degree tilt, verify viewing aperture.
        lcdframe=union([lcdframe,box(lx-2,ly-2,H-8,84.6,2,6),box(lx-2,ly+34,H-8,84.6,4,4)])
        lid=union([lid,lcdframe])
        add('LCD_PCB_Envelope',box(lx,ly,H-21,80.6,36,1.6),'pcb',True)
        add('LCD_Display_Envelope',box(lx+5,ly+5,H-8,70,25,8),'lcd',True)
        add('LCD_Backpack_Envelope',box(lx+8,ly+7,H-30,42,20,9),'black',True)
        for yy in [103,109,115,121]:lid=lid.cut(extr(rr(181,yy,20,2.5,1.1),H-5,8))
        lid=union([lid,ring(191,114,H-18,12,10.4,15)])
        add('Buzzer_Envelope',cyl(191,114,H-17,10,11),'black',True)
    # Subtle raised grip ridges, each connected to the upper shell surface.
    if not main:
        for side in [0,1]:
            for yy in [145,153,161,169,177]:
                xx=34 if side==0 else W-42
                rib=extr(rr(xx,yy,10,2,0.9),H-.5,.8)
                lid=union([lid,rib])
    add('Base',base,'bronze',notes='Cradles, battery bay, strap anchors and cable saddles are integral. No screw bosses.')
    add('Lid',lid,'bronze',explosion=(0,0,40),notes='Rear locating tabs + two press-release side latches. All fits require coupons.')
    # Full-size parts are shown at their reserved envelopes, not inferred photo dimensions.
    add('Breadboard_Envelope',box(bx,by,5,bb[0],bb[1],bb[2]),'breadboard',True)
    add('UNO_PCB_Envelope',box(ux,uy,7,uno[0],uno[1],1.6),'pcb',True)
    add('UNO_Header_Envelope',union([box(ux+2,uy+2,8.6,uno[0]-4,5,9),box(ux+2,uy+uno[1]-7,8.6,uno[0]-4,5,9)]),'black',True)
    add('Battery_Envelope',box(batx+1.75,baty+11,7,26.5,48.5,17.5),'battery',True,notes='Common PP3 maximum envelope, not brand-specific; snap/lead space at bay leading end.')
    add('Battery_Clip_Envelope',box(batx+2,baty+4,7,26,7,18),'black',True)
    # Electrical branch remains provisional; reserved in opposite grip / Main side zone.
    mx,my=(172,72) if main else (189,139)
    add('Power_Module_Reservation',box(mx,my,6,30,22,12),'reservation',True,notes='REGULATOR / LOAD SWITCH: component not selected; not an installed part.')
    doc.recompute()
    doc.saveAs(str(OUT/f'{role}-revision04.FCStd'))
    printable=[o for o in shell_group.Group]
    Part.export(printable,str(OUT/f'{role}-printed-parts.step'))
    # Bounds checks compare the primary component volumes, not only a pretty rendering.
    primary={k:v for k,v in envs.items() if k in ['Breadboard_Envelope','UNO_PCB_Envelope','Battery_Envelope','Power_Module_Reservation','SG90_Body_Envelope']}
    pairs=[]
    for i,(a,sa) in enumerate(primary.items()):
        for b,sb in list(primary.items())[i+1:]:
            overlap=sa.common(sb).Volume
            pairs.append({'a':a,'b':b,'intersection_mm3':round(overlap,4)})
            if overlap>0.01:raise RuntimeError(f'Envelope collision {role}: {a}/{b}: {overlap}')
    # Retention contact is intentional; report shell interference separately for review.
    fit=[]
    for n,s in primary.items():
        fit.append({'component':n,'base_intersection_mm3':round(s.common(base).Volume,3),'lid_intersection_mm3':round(s.common(lid).Volume,3)})
    all_records.extend(records)
    App.closeDocument(doc.Name)
    print(role,':',len(printable),'printed parts;',len(envs),'reference envelopes',flush=True)
    return {'role':role,'nominal_size_mm':[W,D,H],'primary_envelope_pairs':pairs,'shell_contact_review':fit,'physical_fit_verified':False}

if __name__=='__main__':
    reviews=[build(r) for r in ['explorer','architect','main']]
    (ROOT/'scene.json').write_text(json.dumps(all_records,indent=2))
    (ROOT/'CAD_VALIDATION.json').write_text(json.dumps({'scope':'Prototype solid validity and basic envelope checks only; not a print release.','parts':checks,'layout':reviews},indent=2))
    print('CAD, STEP and prototype STL exports complete.',flush=True)
