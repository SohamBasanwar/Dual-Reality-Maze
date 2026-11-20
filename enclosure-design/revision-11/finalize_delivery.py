"""Package only current, verified deliverables; exclude logs and intermediate CAD."""
from pathlib import Path
import json,hashlib,zipfile,re
from html.parser import HTMLParser
R=Path(__file__).resolve().parent
read=lambda f:json.loads((R/f).read_text())
assembly=read('ASSEMBLY_REVIEW.json');adjustments=read('ADJUSTMENT_CHECK_explorer_architect_main.json')
slides=read('SLIDE_PATH_CHECK_all.json');keys=read('KEY_RELEASE_CHECK.json');meshes=read('MESH_VALIDATION.json');solids=read('CAD_VALIDATION.json')
assert {a['role'] for a in assembly}=={'explorer','architect','main'}
for a in assembly:
    for k in ['printed_part_intersections','gate_slider_intersections','shutter_travel_intersections','reveal_hood_rotation_and_removal_intersections','button_stroke_intersections']:assert not a[k],(a['role'],k)
    assert all(not x['conflicts'] for x in a['reserved_volume_checks']),a['role']
assert all(not x['conflicts'] for a in adjustments for x in a['settings'])
assert all(not a['intersections'] for a in slides)
assert all(not k['intersections'] for a in keys for k in a['keys'])
assert all(m['watertight'] and m['consistent_winding'] and m['positive_volume'] for m in meshes['checks'])
scene=read('scene.json');parts=[r for r in scene if not r['component']]
assert len(parts)==len(list((R/'prototype-stl').glob('*.stl')))
expected_images=[]
for role in ['explorer','architect','main']:
    expected_images += [f'{role}-{m}' for m in ['closed','open','base','lid','battery-closed','battery-open','cables-closed','cables-open']]
    for a in read(role+'-adjustments.json'):
        expected_images += [role+'-'+a['prefix'].lower()+'-'+s for s in ['nominal','minus','plus','unlocked','height','arrows']]
expected_images += ['gate-'+s for s in ['01-servo','02-horn','03-frame-panel','04-pin','05-guard','06-closed','07-open']]
expected_images += ['engraving-'+s for s in ['base','lid','door','insert','jaw','shutter']]
expected_images += ['ldr-open','pot-mount','button-linkage','buzzer-mount','printed-parts-full-name','printed-parts-sb','printed-parts-unmarked']
expected_images += [k+'-'+m for k in ['servo-width','button-reach'] for m in ['minus','nominal','plus']]
assert all((R/'previews'/(s+'.png')).is_file() for s in expected_images)
report={'revision':10,'date':'2026-10-29','status':'Digital prototype checks passed; physical validation required',
        'installed_printed_parts':len(parts),'native_solids_checked':len(solids['parts']),'stl_meshes_checked':len(meshes['checks']),
        'guide_views':len(expected_images),'indexed_settings_checked':sum(len(a['settings']) for a in adjustments),
        'jaw_travel_poses_checked':sum(a['jaw_poses_checked'] for a in slides),'jaw_step_mm':.5,
        'locking_keys_checked':sum(len(a['keys']) for a in keys),'key_release_mm':10.5,
        'intersection_threshold_mm3':.05,'physical_fit_verified':False,
        'limitations':['Flexible snap tips excluded from rigid key-travel test; coupon flexure and retention test required.',
          'Component envelopes use nominal dimensions, not measured user components.',
          'Safe powered servo endpoints, battery runtime, structural strength and optical response remain untested.',
          'Body adjustments do not establish compatibility with every connector, tab or shaft offset.'],
        'gallery_check':read('GUIDE_CHECK.json'),
        'reports':['CAD_VALIDATION.json','MESH_VALIDATION.json','ASSEMBLY_REVIEW.json','ADJUSTMENT_CHECK_explorer_architect_main.json','SLIDE_PATH_CHECK_all.json','KEY_RELEASE_CHECK.json','GUIDE_CHECK.json'],
        'native_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'cad').glob('*-revision10.FCStd')}}
(R/'REVIEW_VALIDATION.json').write_text(json.dumps(report,indent=2))
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key in ['src','href'] and value and not value.startswith(('#','http','data:')):
                assert (R/value).is_file(),value
Links().feed((R/'index.html').read_text())
names=['index.html','README.md','PARTS.csv','PRINT_AND_ASSEMBLY.md','REVIEW_VALIDATION.json','scene.json','dimensions.json',
       'build_revision10.py','adjustable_mounts.py','button_contact.py','safe_save.py','render_revision10.py','render_review.py','render_mounts.py','render_engraving.py','render_alternatives.py','render_printed_inventory.py','compose_inventory.py','make_visual_guide.py','export_adjustment_details.py','make_inspection_crops.py','finalize_delivery.py']+report['reports']
files=[R/n for n in names]
files += [R/(role+'-adjustments.json') for role in ['explorer','architect','main']]
files += list((R/'cad').glob('*-revision10.FCStd'))+list((R/'cad').glob('*-printed-parts.step'))
for directory in ['prototype-stl','adjustment-options','optical-options','fit-tests','previews','render-meshes','inspection-meshes']:
    files += [p for p in (R/directory).rglob('*') if p.is_file() and p.suffix.lower() in ['.stl','.png']]
files += [R/f for f in ['check_assembly.py','check_adjustments.py','check_slide_paths.py','check_key_release.py','check_meshes.py','check_guide.js','refresh_solid_validation.py','refresh_scene.py']]
manifest={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(files))}
(R/'SHA256.json').write_text(json.dumps(manifest,indent=2));files.append(R/'SHA256.json')
archive=R.parent/'Dual-Reality-Maze-Revision-10-Soham-Basanwar.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(set(files)):z.write(p,'revision-10/'+str(p.relative_to(R)))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(json.dumps(report,indent=2));print('Delivery archive:',archive,archive.stat().st_size)
