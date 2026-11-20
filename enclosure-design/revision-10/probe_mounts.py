import build_revision10 as B
import json,sys
results=[]
for name,w,d,t,control in [('Breadboard',166,55,10,False),('UNO',68.6,53.4,1.6,False),('Joystick',34,26,1.6,True),('LCD',80.6,36,1.6,True)]:
    if sys.argv[1:] and name not in sys.argv[1:]:continue
    fixed,parts,info=B.adjustable_mount(name,0,0,w,d,0,t,B.box,B.cyl,B.union,B.cut,B.moved,B.text_cut,control)
    row={'name':name,'fixed_solids':len(fixed.Solids),'valid':fixed.isValid(),'parts':[],'intersections':[]}
    allparts=[('fixed',fixed)]+[(n,q) for n,q,_ in parts]
    for n,q in allparts:row['parts'].append([n,q.isValid(),len(q.Solids)])
    for i,(n,q) in enumerate(allparts):
        for nn,qq in allparts[i+1:]:
            if q.BoundBox.intersect(qq.BoundBox):
                v=q.common(qq).Volume
                if v>.02:row['intersections'].append([n,nn,round(v,3)])
    for n,q in allparts:
        if not n.endswith(('_Jaw','_Lock_Key')):continue
        axis='x' if '_X_' in n else 'y'
        for delta in [-3,3]:
            q1=B.moved(q,**{axis:delta});v=q1.common(fixed).Volume
            if v>.02:row['intersections'].append([n,'fixed@'+str(delta),round(v,3)])
            for nn,qq in allparts:
                if nn in ['fixed',n] or ('_X_' in n and '_X_' in nn) or ('_Y_' in n and '_Y_' in nn):continue
                v=q1.common(qq).Volume
                if v>.02:row['intersections'].append([n,nn+'@'+str(delta),round(v,3)])
    results.append(row);print(json.dumps(row),flush=True)
(B.ROOT/'MOUNT_UNIT_CHECK.json').write_text(json.dumps(results,indent=2))
