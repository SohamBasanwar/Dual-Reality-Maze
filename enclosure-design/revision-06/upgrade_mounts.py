from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'build_revision06.py';s=p.read_text()
# A removable push-in edge clip retains the board without assuming hole locations.
a=s.index('    # UNO cradle uses edge supports')
b=s.index('    # Sliding I2C cable hatches.',a)
s=s[:a]+'''    # Parameter-adjustable UNO cradle with replaceable press-in edge clips.
    # Optional hole pins are NOT placed until a matching PCB drawing/part is verified.
    base=union([base,tray(ux,uy,uno[0],uno[1],z=7,height=2)])
    for xx in [ux+5,ux+uno[0]-9]:
        for yy in [uy+1,uy+uno[1]-5]:base=union([base,box(xx,yy,3.8,4,4,3.2)])
    for side in [0,1]:
        xx=ux-4 if side==0 else ux+uno[0]+2
        yy=uy+22
        foot=box(xx-.8,yy-1,4.1,3.6,10,1.7)
        clip=union([foot,box(xx,yy,5.5,2,8,4.8),
                    box(xx+(1.7 if side==0 else -3.1),yy,8.9,3.4,8,1.4)])
        socket=box(xx-1.2,yy-1.4,3.6,4.4,10.8,2.5).cut(box(xx-1,yy-1.2,3.9,4,10.4,2.1))
        # Bottom ledge and tight slot provide a replaceable prototype press fit.
        base=union([base,socket,box(xx-1.2,yy-1.4,3.6,4.4,10.8,.4)])
        base=base.cut(clip)
        add('UNO_Edge_Clip_'+str(side+1),clip,'bronze',explosion=(0,0,20),notes='Replaceable push-in edge retainer. Parametric clearance; no assumed PCB hole pattern. Fit coupon required.')
''' +s[b:]
# Replace integral joystick carrier with its own cartridge and underside sockets.
a=s.index('            # Captive carrier is part of lid')
b=s.index('            lid=lid.cut(cyl(197,42',a)
s=s[:a]+'''            # Separate cartridge: nominal 34 x 26 PCB held at its edges.
            # Snap ears push into blind receivers on the underside of the lid.
            for xx in [jx-2,jx+34]:
                carrier=union([carrier,box(xx,jy,H-24,2,26,21)])
                out=-1 if xx<cx else 1
                ear=box(xx-1.2 if out<0 else xx+1.8,jy+7,H-5.6,1.4,12,1.2)
                carrier=union([carrier,ear])
                receiver=box(xx-2,jy+4,H-10,6,18,6.8)
                receiver=receiver.cut(box(xx-.3,jy+3.7,H-10.2,2.6,18.6,7.2))
                receiver=receiver.cut(box(xx-1.5 if out<0 else xx+1.5,jy+6.7,H-5.9,2,12.6,1.8))
                lid=union([lid,receiver])
            # Bottom lips support the PCB; short upper lips capture its two edges.
            for xx in [jx-2,jx+33]:
                carrier=union([carrier,box(xx,jy+4,H-25,3,18,1.3)])
                carrier=union([carrier,box(xx,jy+7,H-21.7,3,4,1.2)])
            add('Joystick_Carrier',carrier,'bronze',explosion=(0,0,-22),notes='Replaceable snap-in edge carrier. Width/depth/clip parameters provisional; exact mounting-hole pins deferred.')
''' +s[b:]
# Potentiometer lower bayonet keeper, separate from antirotation detail.
old='            lid=union([lid,potcup])'
new='''            potcup=potcup.cut(ring(cx,cy,H-16.6,9.7,8.0,1.6))
            for dx in [-10.4,7.9]:potcup=potcup.cut(box(cx+dx,cy-1.2,H-17.3,2.5,2.4,2.5))
            lid=union([lid,potcup])
            potkeeper=ring(cx,cy,H-16.8,8.05,5.5,1.5)
            potkeeper=union([potkeeper,box(cx-.9,cy-9.4,H-16.4,1.8,1.5,1),box(cx-.9,cy+7.9,H-16.4,1.8,1.5,1)])
            add('Potentiometer_Keeper',potkeeper,'bronze',explosion=(0,0,-20),notes='Quarter-turn lower retainer. Terminal geometry and body antirotation lug remain unmeasured; tune this replaceable part.')'''
s=s.replace(old,new)
# Clips over the servo body and snapping cassette foot.
s=s.replace("            add('Servo_Cassette',cassette", """            for xx in [gx-12,gx+10.3]:
                cassette=union([cassette,box(xx,sy+5,H+18.5,1.7,9,1.5)])
            for xx,direction in [(gx-16,-1),(gx+14.4,1)]:
                leg=box(xx,gy-5,H-6,1.6,10,9)
                hook=box(xx-2.4 if direction<0 else xx+1.4,gy-5,H-5.3,2.6,10,1.2)
                cassette=union([cassette,leg,hook])
            add('Servo_Cassette',cassette""")
s=s.replace('The tongue keys the cartridge into the collar; ties retain it for servicing.','The tongue keys the cartridge into the collar; two lower snap ears retain it.')
# Positive snap ledges below the switch cassette.
s=s.replace("            lid=union([lid,support])", """            hook=box(xx+(1.7 if xx<px else -3.2),py-4,H-18.6,3.5,8,1.4)
            support=union([support,hook,box(xx,py-4,H-18.6,2,8,2)])
            lid=union([lid,support])""")
# LCD becomes a replaceable press-in frame with edge support.
s=s.replace("        lid=union([lid,lcdframe])", """        for xx in [lx-2,lx+80.6]:
            direction=-1 if xx<lx else 1
            ear=box(xx-1.2 if direction<0 else xx+1.8,ly+12,H-8,1.4,12,1.3)
            lcdframe=union([lcdframe,ear])
            socket=box(xx-2,ly+9,H-12,6,18,9)
            socket=socket.cut(box(xx-.3,ly+8.7,H-12.2,2.6,18.6,9.4))
            socket=socket.cut(box(xx-1.5 if direction<0 else xx+1.5,ly+11.7,H-8.3,2,12.6,1.9))
            lid=union([lid,socket])
        for xx in [lx-2,lx+79.6]:
            lcdframe=union([lcdframe,box(xx,ly+5,H-22,3,26,.8),box(xx,ly+12,H-19.1,3,5,1.2)])
        add('LCD_Carrier',lcdframe,'bronze',explosion=(0,0,-25),notes='Replaceable edge carrier, parameter-adjustable to the measured PCB. Backpack clearance preserved. Hole-mounted inserts deferred until hole pattern is known.')""")
# Buzzer keeper around its lead opening.
s=s.replace("        lid=union([lid,ring(191,114,H-18,12,10.4,15)])", """        buzzerseat=ring(191,114,H-18,12,10.4,15)
        buzzerseat=buzzerseat.cut(ring(191,114,H-18.3,11.6,10.2,1.3))
        for dx in [-12.1,10.2]:buzzerseat=buzzerseat.cut(box(191+dx,112.8,H-18.3,2,2.4,1.6))
        lid=union([lid,buzzerseat])
        buzzerkeeper=ring(191,114,H-18.8,10.2,6,1.5)
        buzzerkeeper=union([buzzerkeeper,box(190.1,102.7,H-18.1,1.8,1.4,1),box(190.1,123.9,H-18.1,1.8,1.4,1)])
        add('Buzzer_Keeper',buzzerkeeper,'bronze',explosion=(0,0,-17),notes='Lower bayonet ring leaves room for leads. Actual buzzer and lead spacing require verification.')""")
p.write_text(s)
print('Replaceable edge carriers and positive retaining parts added')
