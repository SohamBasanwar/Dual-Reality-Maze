import FreeCAD as A
import Part,json,sys
from pathlib import Path
R=Path(__file__).resolve().parent;selected=sys.argv[1:] or ['explorer','architect','main'];results=[]
for role in selected:
    d=A.openDocument(str(R/'cad'/f'{role}-revision10.FCStd'))
    pp=d.getObject('PrintedParts').Group;rows=[]
    local_cache={}
    def volume(q,f,key):
        cachekey=(f.Name,key)
        if cachekey not in local_cache:
            b=q.BoundBox
            region=Part.makeBox(b.XLength+14,b.YLength+14,b.ZLength+2,A.Vector(b.XMin-7,b.YMin-7,b.ZMin-1))
            local_cache[cachekey]=(region.BoundBox,f.Shape.common(region))
        b,local=local_cache[cachekey];a=q.BoundBox
        assert b.XMin<=a.XMin and b.YMin<=a.YMin and b.ZMin<=a.ZMin and b.XMax>=a.XMax and b.YMax>=a.YMax and b.ZMax>=a.ZMax
        return q.common(local).Volume if local.Solids else 0
    for item in json.loads((R/(role+'-adjustments.json')).read_text()):
        name=item['prefix'];component={'UNO':'UNO_PCB_Envelope','Breadboard':'Breadboard_Envelope','Joystick':'Joystick_PCB','LCD':'LCD_PCB_Envelope'}[name]
        for axis in item['axes']:
            moving=[d.getObject(axis[k]) for k in ['jaw','key']]
            for delta in axis['range_mm']:
                vec=A.Vector(-axis['direction'][0],axis['direction'][1],0)*(-delta)
                conflicts=[]
                for o in moving:
                    q=o.Shape.copy(True);q.translate(vec)
                    for f in pp:
                        if f in moving or not q.BoundBox.intersect(f.Shape.BoundBox):continue
                        v=volume(q,f,o.Name)
                        if v>.05:conflicts.append([o.Name,f.Name,round(v,3)])
                # Rectangular PCB/body variation with fixed corner. Does not
                # establish fit of different connector/shaft offsets.
                x,y,z=item['origin'];w,h,t=item['nominal_mm'];W=234 if role=='main' else 246
                if axis['axis']=='X':w+=delta
                else:h+=delta
                q=Part.makeBox(w,h,t,A.Vector(W-x-w,y,item['board_bottom_z']))
                for f in pp:
                    if f in moving:continue
                    if not q.BoundBox.intersect(f.Shape.BoundBox):continue
                    v=volume(q,f,component+axis['axis'])
                    if v>.05:conflicts.append([component+' adjusted',f.Name,round(v,3)])
                rows.append({'mount':name,'axis':axis['axis'],'dimension_delta_mm':delta,'conflicts':conflicts})
    results.append({'role':role,'settings':rows});A.closeDocument(d.Name)
    print(role,[(x['mount'],x['axis'],x['dimension_delta_mm'],x['conflicts']) for x in rows if x['conflicts']],flush=True)
(R/('ADJUSTMENT_CHECK_'+('_'.join(selected))+'.json')).write_text(json.dumps(results,indent=2))
