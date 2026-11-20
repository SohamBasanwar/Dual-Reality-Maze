from pathlib import Path
import json
import FreeCAD as A
R=Path(__file__).resolve().parent
report=json.loads((R/'CAD_VALIDATION.json').read_text());rows=[]
for role in ['explorer','architect','main']:
    d=A.openDocument(str(R/'cad'/f'{role}-revision10.FCStd'))
    for group,iscomponent in [('PrintedParts',False),('ComponentEnvelopes',True)]:
        for o in d.getObject(group).Group:
            assert o.Shape.isValid() and o.Shape.Solids
            if not iscomponent:assert len(o.Shape.Solids)==1
            rows.append({'role':role,'part':o.Name,'valid_brep':True,'solids':len(o.Shape.Solids),'volume_mm3':round(o.Shape.Volume,2),'component':iscomponent})
    A.closeDocument(d.Name)
report['parts']=rows;report['scope']='Re-read final native solids; source-level nominal envelope layout and independent full-assembly reports accompany this file. Physical fit unverified.'
(R/'CAD_VALIDATION.json').write_text(json.dumps(report,indent=2))
print(len(rows),'native printed/component solids checked')
