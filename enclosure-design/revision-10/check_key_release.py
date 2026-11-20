"""Check rigid key body travel separately from its intentionally flexible detent."""
import FreeCAD as A
import Part,json
from pathlib import Path
R=Path(__file__).resolve().parent;reports=[];V=A.Vector
for role in ['explorer','architect','main']:
    doc=A.openDocument(str(R/'cad'/f'{role}-revision10.FCStd'));rows=[]
    for item in json.loads((R/(role+'-adjustments.json')).read_text()):
        for axis in item['axes']:
            key=doc.getObject(axis['key']);origin=axis['origin'];edge=axis['axis']
            reverse=edge=='X' and axis['key_release_pre'][1]>0
            tip=Part.makeBox(2.6,1.15,1.2,V(7.7,-5.9,1.12))
            if reverse:tip=tip.mirror(V(),V(0,1,0))
            tip.rotate(V(),V(0,0,1),180 if edge=='X' else 270);tip.translate(V(*origin))
            tip=tip.mirror(V(117 if role=='main' else 123,0,0),V(1,0,0))
            rigid=key.Shape.cut(tip)
            direction=axis['key_release_pre'];direction=V(-direction[0],direction[1],direction[2])
            b=rigid.BoundBox;lower=V(b.XMin,b.YMin,b.ZMin);upper=V(b.XMax,b.YMax,b.ZMax)
            b.add(lower+direction*10.5);b.add(upper+direction*10.5)
            region=Part.makeBox(b.XLength+1,b.YLength+1,b.ZLength+1,V(b.XMin-.5,b.YMin-.5,b.ZMin-.5))
            nearby=[(f,f.Shape.common(region)) for f in doc.PrintedParts.Group if f!=key and f.Shape.BoundBox.intersect(region.BoundBox)]
            issues=[]
            for step in range(22):
                travel=step*.5;q=rigid.copy(True);q.translate(direction*travel)
                for fixed,local in nearby:
                    if not local.Solids or not q.BoundBox.intersect(local.BoundBox):continue
                    volume=q.common(local).Volume
                    if volume>.05:issues.append({'travel_mm':travel,'fixed':fixed.Name,'volume_mm3':round(volume,3)})
            rows.append({'key':key.Name,'release_mm':10.5,'intersections':issues})
    reports.append({'role':role,'keys':rows,'excluded_flexible_tip_requires_physical_test':True})
    A.closeDocument(doc.Name);print(role,[(r['key'],r['intersections']) for r in rows if r['intersections']],flush=True)
(R/'KEY_RELEASE_CHECK.json').write_text(json.dumps(reports,indent=2))
