from pathlib import Path
R=Path(__file__).resolve().parent;p=R/'build_revision10.py';s=p.read_text(encoding='utf-8')
s=s.replace("rr(gx-12,sy-.4,24,29.8,1)","rr(gx-12.9,sy-.7,25.8,30.4,1)")
anchor="            add('Servo_Cassette',cassette,"
block='''            # Replaceable keyed liner fits the servo body without moving the
            # external cassette/frame datum. Side walls are interchangeable.
            def servo_insert(side_thickness=1.2):
                ins=box(gx-12.6,sy-.45,H+4.15,25.2,29.9,1.85)
                for sign in [-1,1]:
                    xx=gx-12.6 if sign<0 else gx+12.6-side_thickness
                    ins=union([ins,box(xx,sy-.45,H+5.8,side_thickness,29.9,8)])
                ins=ins.cut(box(gx-ear_span/2-.3,ear_y-.3,H+5.7,ear_span+.6,P['servo_ear_thickness_mm']+.6,12.8))
                # The sides join beneath the ear slots through the broad floor.
                ins=union([ins,box(gx-8,sy+1,H+3.5,2,4,.8),box(gx+6,sy+1,H+3.5,2,4,.8)])
                return ins
            liner=servo_insert()
            cassette=cassette.cut(box(gx-8.2,sy+.8,H+3.3,2.4,4.4,1.1)).cut(box(gx+5.8,sy+.8,H+3.3,2.4,4.4,1.1))
            add('Servo_Fit_Insert',liner,'bronze',explosion=(0,0,43),notes='Keyed removable servo-body liner. Alternative side thicknesses 0.9 / 1.5 mm fit nominal body width +/-0.6 mm while preserving the shaft centre. Ear slots and actual shaft datum still require fit testing.')
            alt=ROOT/'adjustment-options';alt.mkdir(exist_ok=True)
            for width,st in [('minus',1.5),('plus',.9)]:
                q=servo_insert(st).mirror(V(W/2,0,0),V(1,0,0))
                MeshPart.meshFromShape(Shape=q,LinearDeflection=.13,AngularDeflection=.22,Relative=False).write(str(alt/('architect-servo-width-'+width+'-Soham-Basanwar.stl')))
'''
assert anchor in s;s=s.replace(anchor,block+anchor)
anchor="        add('Button_Cap',cap,"
block='''        if not main:
            # The lower contact shoe can be replaced without reprinting the
            # decorative cap. Keyed press fit; actual retention test required.
            cap=cap.cut(cyl(px,py,tip_z-.2,2.6,4.2))
            cap=cap.cut(box(px-1.4,py-1.4,tip_z+3.8,2.8,2.8,3.5))
            def shoe(delta=0):
                return union([cyl(px,py,tip_z-delta,2.5,4+delta),box(px-1.2,py-1.2,tip_z+3.9,2.4,2.4,3.2)])
            add('Button_Contact_Shoe',shoe(),'bronze',explosion=(0,0,-15),notes='Keyed replaceable lower actuator tip, nominal / +/-0.6 mm reach. Select using real switch rest gap; do not preload the switch. Prototype press retention, verify before use.')
            alt=ROOT/'adjustment-options';alt.mkdir(exist_ok=True)
            for label,delta in [('minus',-.6),('plus',.6)]:
                q=shoe(delta).mirror(V(W/2,0,0),V(1,0,0))
                MeshPart.meshFromShape(Shape=q,LinearDeflection=.13,AngularDeflection=.22,Relative=False).write(str(alt/('architect-button-reach-'+label+'-Soham-Basanwar.stl')))
'''
assert anchor in s;s=s.replace(anchor,block+anchor)
s=s.replace('One-piece cap with long 5 mm-diameter stem to the breadboard switch. Nominal rest tip Z22.45, free gap 0.15 mm, maximum stroke 0.45 mm. Regenerate stem height from the measured installed switch; do not preload it.','Long guided stem with replaceable keyed contact shoe; nominal rest tip Z26.65, free gap 0.15 mm, stroke 0.45 mm. Check installed switch and select reach insert.')
p.write_text(s,encoding='utf-8')
print('Servo liner and replaceable button shoe added')
