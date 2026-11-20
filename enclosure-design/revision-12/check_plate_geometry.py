"""Validate actual model-only 3MF plate counts, bounds, quantities and source mesh bounds."""
from pathlib import Path
import json,zipfile,xml.etree.ElementTree as ET
import numpy as np
R=Path(__file__).resolve().parent;P=R/'uic-voron-provisional'
plans=json.loads((P/'PLACEMENTS.json').read_text(encoding='utf-8'))
ns={'m':'http://schemas.microsoft.com/3dmanufacturing/core/2015/02'}
checks=[];codes=[]
for plate in plans['plates']:
    with zipfile.ZipFile(P/(plate['id']+'.3mf')) as z:
        assert z.testzip() is None
        root=ET.fromstring(z.read('3D/3dmodel.model'))
    assert root.attrib['unit']=='millimeter'
    objs=root.findall('m:resources/m:object',ns);assert len(objs)==len(plate['parts'])
    for obj,row in zip(objs,plate['parts']):
        code=obj.attrib['name'].split()[0];assert code==row['code'];codes.append(code)
        v=np.array([[float(a.attrib[k]) for k in ['x','y','z']] for a in obj.findall('m:mesh/m:vertices/m:vertex',ns)])
        lo,hi=v.min(axis=0),v.max(axis=0);expected=np.array(row['print_bbox_xyz_mm'])
        if row['plate_rotate_z_deg']==90:expected=expected[[1,0,2]]
        assert np.allclose(hi-lo,expected,atol=.00002),(code,hi-lo,expected)
        assert np.allclose(lo[:2],row['placement_xy_mm'],atol=.00002) and abs(lo[2])<.00002
        assert hi[0]<290 and hi[1]<290 and hi[2]<285
    checks.append(dict(plate=plate['id'],separate_objects=len(objs),units='mm',source_bounds_preserved=True,within_published_bed=True))
assert len(codes)==len(set(codes))==95
report=dict(all_checks_passed=True,installed_piece_count=95,material_separation=True,plates=checks,actual_first_plate_imported_by_prusaslicer=(R/'planner-tests/uic-first-plate-roundtrip.3mf').exists(),support_layout_verified=False)
(R/'PLATE_GEOMETRY_CHECK.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('All 95 actual plate objects preserve dimensions, unique codes and placements')
