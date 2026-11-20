from pathlib import Path
import json,zipfile,hashlib,re
R=Path(__file__).resolve().parent
scene=json.loads((R/'scene.json').read_text())
cad=json.loads((R/'CAD_VALIDATION.json').read_text())
assembly=json.loads((R/'ASSEMBLY_REVIEW.json').read_text())
meshes=json.loads((R/'MESH_VALIDATION.json').read_text())
parts=[r for r in scene if not r['component']]
assert len(parts)==46
assert len(assembly)==3
assert all(p['valid_brep'] and p['solids']==1 for p in cad['parts'] if not p['component'])
assert len(meshes['checks'])==64
assert all(x['watertight'] and x['consistent_winding'] and x['positive_volume'] for x in meshes['checks'])
for a in assembly:
    for key in ['printed_part_intersections','gate_rotation_intersections','shutter_travel_intersections','reveal_hood_rotation_intersections']:
        assert not a[key],(a['role'],key,a[key])
    assert all(not q['conflicts'] for q in a['reserved_volume_checks'])
for r in parts:
    assert 'Soham-Basanwar' in r['file']
    assert (R/'prototype-stl'/r['file']).is_file()
report={
 'revision':7,'status':'Design-review prototype; physical fit unverified',
 'printed_parts':len(parts),'single_valid_printed_solids':True,'watertight_meshes_including_samples_and_optical_options':len(meshes['checks']),
 'reserved_component_volumes_checked':sum(len(a['reserved_volume_checks']) for a in assembly),
 'printed_part_intersections_mm3_over_0p05':0,'gate_rotation_checked_deg':[0,110,5],
 'shutters_checked':5,'i2c_travel_mm':21,'usb_travel_mm':35,
 'full_name_physical_parts':sum(r['personalization'].startswith('Soham Basanwar') for r in parts),
 'SB_physical_parts':sum(r['personalization'].startswith('SB') for r in parts),
 'unmarked_sensitive_parts':sum(r['personalization'].startswith('Unmarked') for r in parts),
 'gate_protrusion_above_nominal_lid_mm':6.8,
 'physical_fit_verified':False,'powered_gate_test_performed':False,'optical_test_performed':False,
 'source_sha256':hashlib.sha256((R/'build_revision07.py').read_bytes()).hexdigest()}
(R/'REVIEW_VALIDATION.json').write_text(json.dumps(report,indent=2))
for link in re.findall(r'(?:src|href)="([^"]+)"',(R/'index.html').read_text(encoding='utf-8').split('<script>')[0]):
    if not link.startswith(('https:','http:','#')):assert (R/link).is_file(),link
top=R.parent/'README.md'
previous=top.read_text(encoding='utf-8') if top.exists() else ''
header='# Dual-Reality Maze enclosures\n\nLatest: [Revision 07 review](revision-07/index.html). Compact rotary gate, rounded battery-door perimeter and full-name/SB personalization. This is a design-review prototype requiring actual fit and powered tests.\n\n[Download Revision 07](Dual_Reality_Maze_Revision07_Review.zip) · [Revision 06](revision-06/index.html)\n'
top.write_text(header,encoding='utf-8')
roots=['cad','prototype-stl','render-meshes','previews','fit-tests','optical-options']
files=[p for name in roots for p in (R/name).glob('*') if p.is_file() and p.suffix not in ['.FCStd1']]
files += [R/n for n in ['build_revision07.py','dimensions.json','check_assembly.py','check_meshes.py','make_fit_tests.py','make_review.py','render_revision07.py','render_details.py','finalize_package.py','README.md','PRINT_AND_ASSEMBLY.md','DIMENSION_CHECKLIST.csv','PARTS.csv','scene.json','index.html','Open_Revision07.FCMacro','CAD_VALIDATION.json','ASSEMBLY_REVIEW.json','MESH_VALIDATION.json','REVIEW_VALIDATION.json']]
archive=R.parent/'Dual_Reality_Maze_Revision07_Review.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in files:z.write(p,'revision-07/'+str(p.relative_to(R)))
print(json.dumps(report,indent=2));print('Archive bytes:',archive.stat().st_size)
