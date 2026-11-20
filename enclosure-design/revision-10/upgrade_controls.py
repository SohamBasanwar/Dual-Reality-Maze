from pathlib import Path
R=Path(__file__).resolve().parent
p=R/'build_revision10.py';s=p.read_text(encoding='utf-8')
# Shared register routine exports alternative heights independently of the
# installed nominal insert. Reuse for each control carrier.
anchor='    if main:\n        raw=face'
helper='''    def adjustable_control(prefix,carrier,x,y,w,d,pcb_z,t):
        z=pcb_z-5.4
        fixed,newparts,info=adjustable_mount(prefix,x,y,w,d,z,t,box,cyl,union,cut,moved,text_cut,True)
        # Remove old edge lips and clear all moving jaws. Keep original upper
        # snap ears, so the complete adjustable carrier remains replaceable.
        carrier=carrier.cut(box(x-.35,y-.35,z-.2,w+.7,d+.7,7.6))
        for n,q,note in newparts:
            if n.endswith(('_Jaw','_Lock_Key')):
                for delta in [-3,0,3]:
                    axis='x' if '_X_' in n else 'y'
                    q1=moved(q,**{axis:delta})
                    carrier=carrier.cut(q1)
                    for a in ['x','y','z']:
                        for dd in [-.25,.25]:carrier=carrier.cut(moved(q1,**{a:dd}))
        # Vertical strips join the lower mechanism to the unchanged snap ears.
        links=[box(x-2,y+1,z,1.6,3,12),box(x-2,y+d-4,z,1.6,3,12),box(x+w,y+1,z,1.6,3,12),box(x+w,y+d-4,z,1.6,3,12)]
        carrier=union([carrier,fixed]+links)
        for n,q,note in newparts:add(n,q,'bronze',explosion=(0,0,-25),notes=note)
        alt=ROOT/'adjustment-options';alt.mkdir(exist_ok=True)
        for variant,q in info.pop('_alternate_shapes'):
            q=q.mirror(V(W/2,0,0),V(1,0,0))
            MeshPart.meshFromShape(Shape=q,LinearDeflection=.13,AngularDeflection=.22,Relative=False).write(str(alt/(role+'-'+prefix+'-height-'+variant+'-Soham-Basanwar.stl')))
        info.update(role=role);mount_records.append(info)
        return carrier

'''
assert anchor in s;s=s.replace(anchor,helper+anchor)
s=s.replace("            add('Joystick_Carrier',carrier,", "            carrier=adjustable_control('Joystick',carrier,jx,jy,34,26,H-23.5,1.6)\n            add('Joystick_Carrier',carrier,")
s=s.replace("        add('LCD_Carrier',lcdframe,", "        lcdframe=adjustable_control('LCD',lcdframe,lx,ly,80.6,36,pcb_z,pcb_t)\n        add('LCD_Carrier',lcdframe,")
p.write_text(s,encoding='utf-8')
print('Control carriers upgraded')
