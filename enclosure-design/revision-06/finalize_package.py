from pathlib import Path
import json,hashlib,zipfile,re,shutil
R=Path(__file__).resolve().parent
cad=json.loads((R/'CAD_VALIDATION.json').read_text())
asm=json.loads((R/'ASSEMBLY_REVIEW.json').read_text())
mesh=json.loads((R/'MESH_VALIDATION.json').read_text())
assert len(asm)==3
for r in asm:
    for key in ['printed_part_intersections','gate_slider_intersections','shutter_travel_intersections','reveal_hood_rotation_intersections']:assert not r[key],(r['role'],key,r[key])
    assert all(not x['conflicts'] for x in r['reserved_volume_checks'])
assert all(r['valid_brep'] and r['solids']==1 for r in cad['parts'] if not r['component'])
assert all(all(r[k] for k in ['watertight','consistent_winding','positive_volume']) for r in mesh['checks'])
expected=['family-'+x+'.png' for x in ['charcoal','stone','forest','bronze']]
for role in ['explorer','architect','main']:
    expected += [role+'-'+x+'.png' for x in ['assembled','internal','exploded','front','side','battery-door']]
    expected += [role+'-'+x+'.png' for x in (['side-open','side-closed','shutter-open'] if role=='main' else ['rear-open','rear-closed'])]
expected += ['controller-features.png','explorer-reveal-cutaway.png','architect-gate-cutaway.png']
assert all((R/'previews'/n).is_file() for n in expected),[n for n in expected if not (R/'previews'/n).exists()]
page=(R/'index.html').read_text(encoding='utf-8')
for link in re.findall(r'(?:src|href)="([^"]+)"',page):
    if not link.startswith(('https:','http:','#')):assert (R/link).exists(),link
report={'status':'Digital review passed; physical fit and optical tests outstanding','printed_parts':sum(not p['component'] for p in cad['parts']),'fit_samples':len(list((R/'fit-tests').glob('*.stl'))),'alternative_optical_hoods':len(list((R/'optical-options').glob('*.stl'))),'verified_meshes':len(mesh['checks']),'preview_files':len(expected),'component_reservations_checked':sum(len(x['reserved_volume_checks']) for x in asm),'source_sha256':hashlib.sha256((R/'build_revision06.py').read_bytes()).hexdigest(),'checks':['Valid single-solid printed BReps','Watertight meshes, consistent winding, positive volume','No printed-part or nominal component conflicts','Five shutter travel paths','Gate slider, horn and drive pin sweep','Reveal hood quarter-turn sweep'],'physical_fit_verified':False,'optical_isolation_verified':False,'powered_servo_test_performed':False,'uic_print_profile_selected':False}
(R/'REVIEW_VALIDATION.json').write_text(json.dumps(report,indent=2))
rootreadme=R.parent/'README.md';text=rootreadme.read_text(encoding='utf-8')
old=next(line for line in text.splitlines() if line.startswith('**Latest design review'))
new='**Latest design review (October 25, 2026):** open [revision-06/index.html](revision-06/index.html). Revision 06 adds tapered oval grips, rear controller shutters, side Main shutters, replaceable screwless carriers, and a raised isolated reveal dome. Its [README](revision-06/README.md) supersedes older geometry and assumptions below. This is a mechanical review prototype; physical fit, optical response, power and printer setup remain to be verified. Earlier revisions are preserved.'
rootreadme.write_text(text.replace(old,new),encoding='utf-8')
files=['README.md','PRINT_AND_ASSEMBLY.md','dimensions.json','DIMENSION_CHECKLIST.csv','index.html','Open_Revision06.FCMacro','build_revision06.py','render_revision06.py','render_details.py','export_details.py','draw_controls.py','make_fit_tests.py','check_assembly.py','check_meshes.py','make_review.py','prepare_final.py','finalize_package.py','scene.json','detail-scene.json','CAD_VALIDATION.json','ASSEMBLY_REVIEW.json','MESH_VALIDATION.json','REVIEW_VALIDATION.json']
package=R.parent/'Dual_Reality_Maze_Revision06_Review.zip'
with zipfile.ZipFile(package,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for name in files:
        p=R/name
        if p.exists():z.write(p,'revision-06/'+name)
    for folder in ['cad','prototype-stl','fit-tests','optical-options','previews','render-meshes','detail-meshes']:
        for p in sorted((R/folder).glob('*')):
            if p.is_file() and p.suffix.lower() in ['.fcstd','.step','.scad','.stl','.json','.png','.svg']:
                z.write(p,'revision-06/'+p.relative_to(R).as_posix())
with zipfile.ZipFile(package) as z:assert z.testzip() is None
print(json.dumps(report,indent=2));print('Package:',package,'bytes:',package.stat().st_size)
