from pathlib import Path
import json
import FreeCAD as A,Part
R=Path(__file__).resolve().parent;V=A.Vector
d=A.openDocument(str(R/'cad'/'main-revision12.FCStd'))
printed=d.PrintedParts.Group
checks=[];faults=[]
for tag in ['G1','G2','G3','G4']:
    led=d.getObject('Green_'+tag+'_LED_Envelope').Shape
    for p in printed:
        if not led.BoundBox.intersect(p.Shape.BoundBox):continue
        v=led.common(p.Shape).Volume
        if v>.05:faults.append(dict(kind='LED envelope',led=tag,part=p.Name,volume=v))
    # Bezel assembly path: the final hooks must flex. Test the rigid body and
    # legs excluding the 0.35 mm snap hooks. No claim of flexure force/strength.
    bezel=d.getObject('Light_'+tag+'_Bezel').Shape
    if tag in ['G1','G2']:
        mounts=[(42,17),(73,11)]
        if tag=='G2':mounts=[(234-a,b) for a,b in mounts]
    else:
        mounts=[(39,65),(57,88)]
        if tag=='G4':mounts=[(234-a,b) for a,b in mounts]
    rigid=bezel
    for x,y in mounts:rigid=rigid.cut(Part.makeBox(3.1,.36,.9,V(x-1.55,y-.81,59.15)))
    for n in range(0,13):
        q=rigid.copy();q.translate(V(0,0,n*.5))
        v=q.common(d.Lid.Shape).Volume
        if v>.05:faults.append(dict(kind='bezel insertion rigid sweep',part=tag,lift_mm=n*.5,volume=v))
    checks.append(dict(tag=tag,led_envelope_checked=True,insertion_poses=13,flexible_hook_tested=False))
# New cap must rotate to its entry slots then withdraw downwards.
for deg in range(0,91,5):
    q=d.RGB_Isolation_Cap.Shape.copy();q.rotate(V(117,108,0),V(0,0,1),deg)
    for fixed in ['Lid','RGB_LED_Keeper','RGB_LED_Envelope']:
        v=q.common(d.getObject(fixed).Shape).Volume
        if v>.05:faults.append(dict(kind='RGB cap turn',angle=deg,fixed=fixed,volume=v))
for n in range(1,21):
    q=d.RGB_Isolation_Cap.Shape.copy();q.rotate(V(117,108,0),V(0,0,1),90);q.translate(V(0,0,-n*.5))
    for fixed in ['Lid','RGB_LED_Keeper','RGB_LED_Envelope']:
        v=q.common(d.getObject(fixed).Shape).Volume
        if v>.05:faults.append(dict(kind='RGB cap withdrawal',travel=n*.5,fixed=fixed,volume=v))
report=dict(led_count=4,checks=checks,conflicts=faults,optical_uniformity_measured=False,light_leakage_measured=False,physical_fit_tested=False,threshold_mm3=.05)
(R/'LIGHTING_CHECK.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2),flush=True)
assert not faults
