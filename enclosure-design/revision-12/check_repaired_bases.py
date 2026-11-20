"""Recheck final base edits against every printed part and reference envelope."""
from pathlib import Path
import json
import FreeCAD as A
R=Path(__file__).resolve().parent
report=[]
for role in ['explorer','architect','main']:
    d=A.openDocument(str(R/'cad'/f'{role}-revision12.FCStd'))
    base=d.Base.Shape;conflicts=[];tested=0
    for o in list(d.PrintedParts.Group)+list(d.ComponentEnvelopes.Group):
        if o.Name=='Base' or not base.BoundBox.intersect(o.Shape.BoundBox):continue
        v=base.common(o.Shape).Volume;tested+=1
        if v>.05:conflicts.append(dict(name=o.Name,intersection_mm3=v))
    report.append(dict(role=role,comparisons=tested,conflicts=conflicts))
    print(role,tested,'comparisons',len(conflicts),'conflicts',flush=True)
    A.closeDocument(d.Name)
(R/'BASE_REPAIR_CHECK.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
assert all(not r['conflicts'] for r in report)
