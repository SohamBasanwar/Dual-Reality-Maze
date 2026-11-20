import FreeCAD as A
import json
from pathlib import Path
R=Path(__file__).resolve().parent
reports=[]
for role in ['explorer','architect','main']:
    d=A.openDocument(str(R/'cad'/f'{role}-revision04.FCStd'))
    parts=d.getObject('PrintedParts').Group
    overlaps=[]
    for i,a in enumerate(parts):
        for b in parts[i+1:]:
            # Bounding-box reject before expensive solid intersection.
            if not a.Shape.BoundBox.intersect(b.Shape.BoundBox):continue
            v=a.Shape.common(b.Shape).Volume
            if v>.05:overlaps.append({'a':a.Name,'b':b.Name,'volume_mm3':round(v,3)})
    # Check the moving gate against frame and guard at 5 degree increments.
    motion=[]
    if role=='architect':
        gate=d.getObject('Gate_Panel').Shape
        for angle in range(-60,61,5):
            import math
            lift=7*(math.sin(math.radians(angle))+math.sin(math.pi/3))
            moved=gate.copy();moved.translate(A.Vector(0,0,lift))
            for fixed in ['Gate_Frame','Gate_Shroud']:
                v=moved.common(d.getObject(fixed).Shape).Volume
                if v>.05:motion.append({'angle_deg':angle,'fixed':fixed,'volume_mm3':round(v,3)})
    report={'role':role,'printed_part_intersections':overlaps,'gate_slider_intersections':motion,'physical_fit_verified':False}
    print(json.dumps(report),flush=True);reports.append(report);A.closeDocument(d.Name)
(R/'ASSEMBLY_REVIEW.json').write_text(json.dumps(reports,indent=2))
