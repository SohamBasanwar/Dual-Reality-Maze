from pathlib import Path
p=Path(__file__).with_name('build_revision06.py');s=p.read_text()
a=s.index('            sx,sy=123,117');b=s.index('        else:\n            lid=lid.cut(cyl(cx,cy',a)
t='''            sx,sy=123,117  # deliberate centre-face reach, away from grips/cable/joystick
            # Raised, closed-bottom reveal pod. The sensor is ABOVE the case
            # roof; only two small lead bores connect to the electronics cavity.
            pod=cyl(sx,sy,H-.3,8.1,1.7)
            collar=ring(sx,sy,H-.3,12,10.3,2.7)
            collar=collar.cut(ring(sx,sy,H+.4,11.5,10.2,1.2))
            for dy in [-12.2,10.1]:collar=collar.cut(box(sx-1.3,sy+dy,H+.2,2.6,2.4,3))
            pod=union([pod,collar,ring(sx,sy,H+1.4,3.5,2.9,3.1),ring(sx,sy,H+1.4,3.0,1.9,.8)])
            for dx in [-3.4,2.4]:pod=union([pod,box(sx+dx,sy-.8,H+4.6,1,1.6,.8)])
            # Long individual lead guides reduce light entry; snug opaque
            # sleeves/seals are still needed if the real bores leak light.
            for dx in [-1.27,1.27]:pod=union([pod,cyl(sx+dx,sy,H-3.8,1.4,4)])
            lid=union([lid,pod])
            for dx in [-1.27,1.27]:lid=lid.cut(cyl(sx+dx,sy,H-4.1,.5,7))
            dome=Part.makeSphere(10,V(sx,sy,H+1)).common(box(sx-11,sy-11,H+1,22,22,11))
            dome=dome.cut(Part.makeSphere(8.4,V(sx,sy,H+1)))
            dome=union([dome,ring(sx,sy,H+.2,10,8.4,1.0)])
            dome=dome.cut(cyl(sx,sy,H+7,3.3,6))
            for dx in [-11.1,9.8]:dome=union([dome,box(sx+dx,sy-.9,H+.6,1.3,1.8,.8)])
            # All roofs use the same bayonet housing. Start by testing the
            # user's single-filament membrane; colour and thickness alone do
            # not establish optical transmission.
            options=ROOT/'optical-options';options.mkdir(exist_ok=True)
            for thickness in [0,.4,.6,.8]:
                variant=dome if thickness==0 else union([dome,cyl(sx,sy,H+9.7,3.6,thickness)])
                label='clear-film-frame' if thickness==0 else 'printed-roof-'+str(thickness).replace('.','p')+'mm'
                exported=variant.mirror(V(W/2,0,0),V(1,0,0))
                MeshPart.meshFromShape(Shape=exported,LinearDeflection=.13,AngularDeflection=.22,Relative=False).write(str(options/(label+'.stl')))
            dome=union([dome,cyl(sx,sy,H+9.7,3.6,.4)])
            add('Reveal_Dome',dome,'bronze',explosion=(0,0,28),notes='Raised half-dome, quarter-turn removable. Default 0.4 mm printed roof is an optical TEST, not guaranteed transparent. Alternate roofs and open frame supplied separately.')
            add('Joystick_PCB',box(jx,jy,H-23.5,34,26,1.6),'pcb',True)
            thumbcap=Part.makeSphere(12,V(cx,cy,H+4)).common(box(cx-13,cy-13,H+2,26,26,6))
            thumbcap=thumbcap.cut(Part.makeSphere(17,V(cx,cy,H+24)))
            add('Joystick_Mechanism',union([box(cx-9,cy-9,H-22,18,18,15),cyl(cx,cy,H-7,6,12),thumbcap]),'black',True,notes='Recognisable reference cap; actual module, cap and full tilt envelope remain unmeasured.')
            sensor=union([cyl(sx,sy,H+2.4,2.7,2)]+[cyl(sx+dx,sy,H-4,.25,6.5) for dx in [-1.27,1.27]])
            add('Bare_Light_Sensor',sensor,'sensor',True,notes='Nominal 5.4 mm disc, two 0.5 mm leads at 2.54 mm pitch. Measure actual part; roof optical transmission and lead seals need testing.')
'''
s=s[:a]+t+s[b:];p.write_text(s)
print('Installed external reveal dome with two lead passages and optical test roofs')
