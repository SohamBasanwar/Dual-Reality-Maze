from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'build_revision06.py'
s=p.read_text().replace('Revision 05','Revision 06').replace('revision05','revision06').replace('_R05','_R06')
marker='def build(role):'
helpers='''def grip_limit(inset=0):
    # Oval X/Z sections along the handle length: true barrel surfaces, not
    # a bevel around a rectangular prism. Flat battery-door land is added below.
    sections=[(106,43,27,62,48),(125,43,27,43,36),
              (145,42,27,35,30),(170,40,26,32,28),
              (190,38,24,29,26),(211,34,22,23,23)]
    grips=[]
    for side in [0,1]:
        wires=[]
        for y,x,z,rx,rz in sections:
            cx=x if side==0 else 246-x
            # Build in XY and rotate to XZ; keep one seam correspondence.
            e=Part.Ellipse(V(0,0,0),max(rx-inset,rz-inset),min(rx-inset,rz-inset)).toShape()
            wire=Part.Wire([e]);wire.rotate(V(0,0,0),V(1,0,0),90)
            wire.translate(V(cx,y,z));wires.append(wire)
        grips.append(Part.makeLoft(wires,True,False))
    return union([box(-40,-40,-50,326,147,180)]+grips)

def oriented(s,angle,x,y):
    q=s.copy();q.rotate(V(0,0,0),V(0,0,1),angle);q.translate(V(x,y,0));return q

'''
s=s.replace(marker,helpers+marker)
s=s.replace("    body=body.common(ceiling(W,H,main))", "    body=body.common(ceiling(W,H,main))\n    if not main:\n        body=body.common(grip_limit())\n        # Narrow flat service land only under the PP3 battery door.\n        land=extr(rr(23.5,122.5,37,68,4),0,6)\n        body=union([body,land])")
s=s.replace("    cavity=cavity.common(ceiling(W,H-3.8,main))", "    cavity=cavity.common(ceiling(W,H-3.8,main))\n    if not main:cavity=cavity.common(grip_limit(3.4))")
a=s.index('    # Cable entry/strain-relief saddle;')
b=s.index('    # Snap latches:',a)
s=s[:a]+'''    # Sliding I2C cable hatches. Coordinates are before the final X mirror.
    # Each aperture accepts a sleeved three-wire bundle; park the shutter open
    # while connected. The cover is never used to clamp individual jumpers.
    ports=[('I2C_Left',-90,0,125),('I2C_Right',90,W,95)] if main else [('I2C_Rear',0,123,0)]
    for name,angle,xx,yy in ports:
        z=24
        trans=lambda a:oriented(a,angle,xx,yy)
        opening=box(-9,-12,z-6,18,30,12)
        channel=box(-10.4,-2.55,z-7.1,42.4,3.1,14.2)
        base=cut(base,[trans(opening),trans(channel)])
        frame=union([box(-12,-4,z-10,47,12,2.9),box(-12,-4,z+7.1,47,12,2.9),
                     box(32,-4,z-10,3,12,20),
                     box(-12,-4,z-10,47,1.4,5),box(-12,-4,z+5,47,1.4,5),
                     box(-12,.6,z-10,47,7.4,5),box(-12,.6,z+5,47,7.4,5)])
        # Flat back lips extend into the sculpted wall, joining the integral rail.
        base=union([base,trans(frame)])
        slide=union([box(-10,-2.2,z-6.7,20,2.2,13.4),box(-4,-5.2,z-3,8,3.1,6)])
        keeper=union([box(-12,-3.6,z-6.5,1.6,5.4,split-z+4.3),
                      box(-12,-3.6,split-2.2,3.6,11.6,1.2)])
        base=cut(base,[trans(box(-12.2,-3.8,z-6.7,2,5.8,split-z+4.7)),
                       trans(box(-12.2,-3.8,split-2.4,4,12,1.6))])
        add(name+'_Shutter',trans(slide),'bronze',explosion=(0,-22,0),notes='18 x 12 mm aperture; slide 21 mm to open. Close only after cable removal. Not a strain clamp.')
        add(name+'_Keeper',trans(keeper),'bronze',explosion=(0,0,18),notes='Top-inserted stop; lid prevents full withdrawal. Service by removing lid.')
        # Open cleat and two transverse slots for a reusable silicone band.
        # Bundle relief is separate from shutter. No pressure on pin connectors.
        cleat=box(-9,9,15,18,6,8).cut(box(-5,8,18,10,8,6))
        cleat=cleat.cut(box(-10,10.5,16,20,2.5,1.4))
        # Bridge to the side/rear wall; does not obstruct the wire path above it.
        cleat=union([cleat,box(-9,5,15,4,6,5),box(5,5,15,4,6,5)])
        base=union([base,trans(cleat)])
''' +s[b:]
s=s.replace("    lid=union([lid,border])", "    if not main:border=border.common(box(-20,-20,-5,286,149,100))\n    lid=union([lid,border])")
p.write_text(s)
print('Updated source with tapered oval grips and four I2C shutters')
