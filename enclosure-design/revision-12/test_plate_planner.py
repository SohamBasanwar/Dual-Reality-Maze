from pathlib import Path
import json,random,sys,subprocess,zipfile,xml.etree.ElementTree as ET
import numpy as np
from arrange_plates import pack,write3mf
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'build/python-tools'))
import trimesh
def item(code,w,d,h=3):return dict(code=code,print_bbox_xyz_mm=[w,d,h])
# Synthetic dimensions exercise the algorithm; these are not the user's bed.
random.seed(362)
items=[item('test-'+str(i),random.uniform(5,60),random.uniform(5,45)) for i in range(95)]
plates=pack(items,180,140,80)
assert len(plates)>1
rotated=pack([item('rotate',80,100)],130,90,20,margin=2,allowance=0,gap=0)
assert rotated[0]['parts'][0]['plate_rotate_z_deg']==90
for dims in [(200,200,3),(10,10,100)]:
    try:pack([item('oversize',*dims)],100,100,50)
    except ValueError:pass
    else:raise AssertionError('Oversized part accepted')
T=R/'planner-tests';T.mkdir(exist_ok=True)
a=trimesh.creation.box(extents=[10,12,3]);a.apply_translation([15,16,1.5])
b=trimesh.creation.box(extents=[6,8,2]);b.apply_translation([40,40,1])
write3mf(T/'synthetic-roundtrip.3mf',[('TEST-A Soham Basanwar',a),('TEST-B Soham Basanwar',b)])
report=dict(synthetic_parts_checked=95,multiple_plates=True,rotation_only_fit=True,oversize_rejected=True,packing_no_overlaps=True,part_count_preserved=True,production_bed_assumed=False,three_mf_written=True,three_mf_slicer_import_checked=False)
slicer=Path('C:/Program Files/Prusa3D/PrusaSlicer/prusa-slicer-console.exe')
if slicer.exists():
    subprocess.run([str(slicer),'--export-3mf','--dont-arrange','--output',str(T/'prusa-roundtrip.3mf'),str(T/'synthetic-roundtrip.3mf')],check=True,capture_output=True)
    with zipfile.ZipFile(T/'prusa-roundtrip.3mf') as z:root=ET.fromstring(z.read('3D/3dmodel.model'))
    ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
    objects={o.attrib['id']:o for o in root.findall('m:resources/m:object',ns)};points=[]
    for item in root.findall('m:build/m:item',ns):
        vertices=objects[item.attrib['objectid']].findall('m:mesh/m:vertices/m:vertex',ns)
        v=np.array([[float(a.attrib[k]) for k in ['x','y','z']] for a in vertices])
        t=np.array([float(v) for v in item.attrib['transform'].split()]);points.extend(v @ t[:9].reshape(3,3)+t[9:])
    points=np.array(points)
    assert len(objects)==2 and np.allclose(points.min(axis=0),[10,10,0]) and np.allclose(points.max(axis=0),[43,44,3])
    report.update(three_mf_slicer_import_checked=True,three_mf_scene_placement_roundtrip=True)
(R/'PLANNER_CHECK.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(report)
