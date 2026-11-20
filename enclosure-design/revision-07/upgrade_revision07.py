from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'build_revision07.py'
s=p.read_text().replace('Revision 06','Revision 07').replace('revision06','revision07').replace('_R06','_R07')
s=s.replace("land=extr(rr(23.5,122.5,37,68,4),0,4)","""# A broad rolled transition replaces the vertical edge of the flat pad.
        land=Part.makeLoft([moved(rr(23.5-d,122.5-d,37+2*d,68+2*d,4+d),z=z).OuterWire
                            for z,d in [(0,0),(.6,.2),(1.8,1.0),(3.5,2.6),(6,5),(8,7)]],True,False)""")
s=s.replace("door=extr(door_profile,.3,2.1)","""door=extr(door_profile,.3,2.1)
    # Round the exposed underside perimeter before adding the latch geometry.
    door=rounded_edge(door,.3,.65)""")
start=s.index('            # Upper shoulder gate cassette')
end=s.index('            # Actuator at thumb position',start)
s=s[:start]+'''            # R07: horizontal rotary rune gate. SG90 stays below the roof.
            gx,gy=196,32
            # Circular opening includes the horn sweep. Nominal body is upright.
            lid=lid.cut(cyl(gx,gy,H-5.5,21.6,15))
            lid=union([lid,ring(gx,gy,H-2,25,21.6,4)])
            servo=box(gx-5.5,gy-6.1,H-33,23,12.2,28)
            add('SG90_Body_Envelope',servo,'servo',True,notes='Upright nominal body 23 x 12.2 x 28. Shaft offset, mounting ears and actual height remain unmeasured. Replaceable cartridge.')
            # Body cup rests below the lid. Inner clearance .4 mm per side.
            seat=extr(rr(gx-8.5,gy-9,29,18,2).cut(rr(gx-5.9,gy-6.5,23.8,13,1)),H-35,32)
            seat=union([seat,box(gx-8.5,gy-9,H-35,29,18,2)])
            seat=seat.cut(box(gx+13,gy-11,H-31,6,7,5))
            # Two flexible side arms retain the nominal case top; no screw tab pattern assumed.
            for xx in [gx-8.5,gx+18.1]:
                seat=seat.cut(box(xx-.1,gy-4.5,H-16,2.6,9,9))
                seat=union([seat,box(xx,gy-4,H-16,1.8,8,12),box(xx if xx<gx else xx-1.8,gy-4,H-4.8,3.6,8,1.4)])
            # Cartridge flange is trapped between roof collar and cover.
            seat=union([seat,ring(gx,gy,H-3,21.2,18.8,2),box(gx-20,gy-2,H-3,40,4,2)])
            seat=seat.cut(cyl(gx,gy,H-6,5,6))
            # Rim notches locate the cartridge, cover traps upward motion.
            for dy in [-20,18]:seat=union([seat,box(gx-3,gy+dy,H-3,6,3,3)])
            add('Servo_Cassette',seat,'bronze',explosion=(0,0,-18),notes='Removable body cradle below the lid, with flexible upper fingers and captive locating flange. Verify SG90 clone and wire exit.')
            # Model the supplied nylon horn, not an invented printed spline.
            hornprofile=union([capsule(gx,gy,gx+8,gy,2),Part.Face(Part.Wire([Part.makeCircle(3.8,V(gx,gy,0))]))])
            horn=extr(hornprofile,H-2,2)
            add('Original_Horn_Envelope',horn,'white',True,notes='Supplied single-arm nylon horn. Provisional 8 mm arm, 3.8 mm hub radius. Measure and revise pocket before printing.')
            rotor=cyl(gx,gy,H+2,20.8,1.8)
            socket=extr(offset(hornprofile,1.4),H-2.3,4.4).cut(extr(offset(hornprofile,.25),H-2.5,2.8))
            rotor=union([rotor,socket])
            # Arched viewport lies toward the front, clear of the central hub.
            arch=union([rr(gx-6.5,gy+5,13,8,1),Part.Face(Part.Wire([Part.makeCircle(6.5,V(gx,gy+12,0))]))])
            arch=arch.common(face([(gx-7,gy+5),(gx+7,gy+5),(gx+7,gy+19),(gx-7,gy+19)]))
            openhole=extr(arch,H+1.7,2.5)
            openhole.rotate(V(gx,gy,0),V(0,0,1),-110)
            bars=[box(gx+t,gy+5.5,H+1.7,1.6,10,2.5).common(extr(arch,H+1.7,2.5)) for t in [-4.5,-.8,2.9]]
            rotor=cut(rotor,[openhole]+bars)
            add('Gate_Rotor',rotor,'bronze',explosion=(0,0,35),notes='110-degree sweep: narrow slots show closed bars, then the open arched sector aligns. Supplied horn keyed in underside pocket; cover limits lift. Not an iris or tall gate.')
            cover=ring(gx,gy,H+.3,25,21.4,5.7)
            cover=union([cover,cyl(gx,gy,H+4.4,25,1.6)])
            cover=cover.cut(extr(arch,H+4.2,3))
            # Raised arch frame is tactile but stays below 8 mm above the lid.
            cover=union([cover,extr(offset(arch,1.1).cut(arch),H+5.8,1.0)])
            # Deliberate viewing opening; clear PET window can isolate moving disk.
            for dx in [-23,21.4]:
                leg=box(gx+dx,gy-4,H-5,1.6,8,7)
                hook=box(gx+dx+(-1.2 if dx<0 else 1.4),gy-4,H-4.8,1.4,8,1)
                cover=union([cover,leg,hook])
                lid=lid.cut(box(gx+dx-.3,gy-4.3,H-6,2.2,8.6,12))
                lid=lid.cut(box(gx+dx+(-1.5 if dx<0 else 1.2),gy-4.3,H-5,2,8.6,1.5))
            # Collar seat supports flange; cartridge cannot drop into the case.
            ledge=ring(gx,gy,H-4.8,23,20,1.5)
            lid=union([lid,ledge])
            add('Gate_Window_Cover',cover,'bronze',explosion=(0,0,50),notes='6.8 mm above roof. Snap legs retain cover; roof captures rotor/horn axially. Clear PET over viewport recommended to prevent fingers touching the disk; film not included as printed plastic.')
''' + s[end:]
s=s.replace("['Joystick_Carrier','LCD_Carrier','Gate_Shroud']","['Joystick_Carrier','LCD_Carrier','Gate_Window_Cover','Servo_Cassette']")
# Names are applied after the overall X mirror so real text is not reversed.
anchor='def build(role):'
personal='''def text_cut(shape, label, xy, z, height=3, width=70, underside=False):
    wires=Part.makeWireString(label,'C:/Windows/Fonts/','arialbd.ttf',height)
    faces=[Part.makeFace(w,'Part::FaceMakerBullseye') for w in wires]
    text=Part.makeCompound(faces)
    b=text.BoundBox
    if b.XLength>width:text.scale(width/b.XLength)
    b=text.BoundBox;text.translate(V(-b.XMin,-b.YMin,0))
    if underside:
        text=text.mirror(V(text.BoundBox.XLength/2,0,0),V(1,0,0))
        tool=text.extrude(V(0,0,.28));tool.translate(V(xy[0],xy[1],z-.02))
    else:
        tool=text.extrude(V(0,0,.28));tool.translate(V(xy[0],xy[1],z-.26))
    removed=shape.common(tool).Volume
    q=shape.cut(tool).removeSplitter()
    if removed<.1 or not q.isValid() or len(q.Solids)!=1:
        raise RuntimeError('Personalization is not safe/readable: '+label+' '+str(removed))
    return q

def personalize(shape,name,role,W,H):
    # Full name kept away from palms and engagement faces. Tiny parts are
    # only initialled on selected broad, unloaded faces; others remain blank.
    full='Soham Basanwar'; mark='Unmarked: no suitable nonfunctional face'
    if name=='Base':
        shape=text_cut(shape,full,(W/2-32,42 if role!='main' else 76),0,3.6,67,True);mark=full+' — underside central panel'
    elif name=='Lid':
        shape=text_cut(shape,full,(W-155,100 if role!='main' else 80),H-3.8,3.3,61,True);mark=full+' — inside roof'
    elif name=='Battery_Door':
        bx,by=(23,98) if role=='main' else (27,126)
        for line,yy in [('Soham',by+15),('Basanwar',by+21)]:
            shape=text_cut(shape,line,(W-bx-26,yy),2.4,3,24)
        mark=full+' — inner face in two lines'
    elif name=='Button_Cap':
        px,py=(117,145) if role=='main' else (197,95)
        shape=text_cut(shape,'SB',(W-px-2.3,py-6),H+4,2.4,4.7);mark='SB — upper face, clear of icon'
    elif name=='Switch_Cassette':
        px,py=(117,145) if role=='main' else (197,95)
        shape=text_cut(shape,'SB',(W-px-3,py-7),H-17,2.8,6,True);mark='SB — outside bottom plate'
    elif name=='Gate_Window_Cover':
        shape=text_cut(shape,'SB',(W-196-3,32-12),H+6,3,6);mark='SB — rear top rim'
    elif name=='Gate_Rotor':
        shape=text_cut(shape,'SB',(W-196-3,32-8),H+3.8,2.5,5.2);mark='SB — top, outside viewport and bearing region'
    elif name=='Servo_Cassette':
        shape=text_cut(shape,'SB',(W-196-8,32-3),H-35,3,7,True);mark='SB — underside body cradle'
    return shape,mark

'''
s=s.replace(anchor,personal+anchor)
s=s.replace("exported=shape.mirror(V(W/2,0,0),V(1,0,0))","""exported=shape.mirror(V(W/2,0,0),V(1,0,0))
        marking='Reference component — not personalized'
        if not component:exported,marking=personalize(exported,name,role,W,H)
        # Keep assembly-side geometry synchronized with engraved export.
        if not component:shape=exported.mirror(V(W/2,0,0),V(1,0,0))""")
s=s.replace("ob.Label=name.replace('_',' ');ob.Shape=exported","ob.Label=name.replace('_',' ')+(' — Soham Basanwar' if not component else '');ob.Shape=exported")
s=s.replace("ob.DesignNotes=notes","ob.DesignNotes=notes\n        ob.addProperty('App::PropertyString','Personalization');ob.Personalization=marking")
s=s.replace("filename=f'{role}-{name}.stl'","filename=f'{role}-{name}'+('—Soham-Basanwar' if not component else '')+'.stl'")
s=s.replace("'notes':notes}","'notes':notes,'personalization':marking,'file_label':'Soham Basanwar' if not component else ''}")
p.write_text(s,encoding='utf-8')
for n in ['check_assembly.py','make_fit_tests.py']:
    p=R/n;p.write_text(p.read_text().replace('revision06','revision07'),encoding='utf-8')
