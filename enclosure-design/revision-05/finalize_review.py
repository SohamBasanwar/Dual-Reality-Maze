"""Validate package contents and write a review archive. Uses standard Python."""
from pathlib import Path
import json,zipfile,hashlib
R=Path(__file__).resolve().parent
cad=json.loads((R/'CAD_VALIDATION.json').read_text())
assembly=json.loads((R/'ASSEMBLY_REVIEW.json').read_text())
meshes=json.loads((R/'MESH_VALIDATION.json').read_text())
assert len(assembly)==3
for r in assembly:
    assert not r['printed_part_intersections'],r
    assert not r['gate_slider_intersections'],r
    assert not r['shutter_travel_intersections'],r
    assert all(not f['conflicts'] for f in r['reserved_volume_checks']),r
printed=[p for p in cad['parts'] if not p['component']]
assert len(printed)==29 and all(p['valid_brep'] and p['solids']==1 for p in printed)
assert len(meshes['checks'])==36
assert all(m['watertight'] and m['consistent_winding'] and m['positive_volume'] for m in meshes['checks'])
assert len(list((R/'previews').glob('*.png')))==25
slice_checks=[]
for role in ['explorer','main']:
    p=R/'slice-review'/(role+'-PREVIEW-NOT-FOR-PRINT.gcode')
    g=p.read_text(errors='replace')
    count=g.count(';TYPE:Support material')
    assert count>0
    slice_checks.append({'role':role,'orientation':'lid inverted; external face downward','slicer':'PrusaSlicer 2.9.6','generic_bed_mm':[300,300,300],'layer_height_mm':.2,'nozzle_mm':.4,'supports':'organic, build plate only','support_path_sections':count,'scope':'Slicing feasibility preview only. Not assigned UIC machine settings. G-code excluded from delivery.'})
(R/'SLICE_REVIEW.json').write_text(json.dumps(slice_checks,indent=2))
receipt={'status':'Design-review prototype; physical fit and fabrication release pending','date':'2026-10-25','printed_solids':29,'fit_test_meshes':7,'watertight_meshes':36,'component_reservations_checked':sum(len(r['reserved_volume_checks']) for r in assembly),'printed_intersections':0,'gate_panel_sweep_step_deg':5,'gate_panel_sweep_range_deg':[-60,60],'shutter_travel_step_mm':1,'shutter_travel_range_mm':[0,35],'physical_fit_verified':False,'electrical_integration_verified':False,'source_sha256':hashlib.sha256((R/'build_revision05.py').read_bytes()).hexdigest()}
(R/'REVIEW_VALIDATION.json').write_text(json.dumps(receipt,indent=2))
root_names={'README.md','REVISION_BRIEF.md','PRINT_AND_ASSEMBLY.md','POWER_AND_STATUS.md','DIMENSION_CHECKLIST.csv','dimensions.json','scene.json','layout-outlines.json','CAD_VALIDATION.json','ASSEMBLY_REVIEW.json','MESH_VALIDATION.json','SLICE_REVIEW.json','REVIEW_VALIDATION.json','index.html','Open_Revision05.FCMacro'}
dirs={'cad','prototype-stl','render-meshes','fit-tests','previews','reference'}
archive=R.parent/'Dual_Reality_Maze_Revision05_Review.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(R.rglob('*')):
        if not p.is_file():continue
        rel=p.relative_to(R)
        include=(len(rel.parts)==1 and (p.name in root_names or p.suffix=='.py')) or rel.parts[0] in dirs
        if p.suffix.lower() in {'.fcbak','.fcstd1','.pyc'} or '__pycache__' in rel.parts:include=False
        if include:z.write(p,'revision-05/'+rel.as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert not any('slice-review/' in n or n.endswith('.gcode') or 'fine-base.stl' in n for n in z.namelist())
print(json.dumps(receipt,indent=2))
print('Review archive:',archive,'bytes:',archive.stat().st_size)
