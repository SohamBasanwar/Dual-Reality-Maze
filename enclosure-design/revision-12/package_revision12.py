from pathlib import Path
from html.parser import HTMLParser
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
read=lambda n:json.loads((R/n).read_text(encoding='utf-8'))
parts=[r for r in read('scene.json') if not r['component']]
assert all(p['valid_brep'] and p['solids']>0 for p in read('CAD_VALIDATION.json')['parts'])
main=next(r for r in read('ASSEMBLY_REVIEW.json') if r['role']=='main')
for key in ['printed_part_intersections','shutter_travel_intersections']:
    assert not main[key],(key,main[key])
assert all(not a['conflicts'] for a in main['reserved_volume_checks'])
assert not read('LIGHTING_CHECK.json')['conflicts']
assert all(not s['conflicts'] for a in read('ADJUSTMENT_CHECK_main.json') for s in a['settings'])
assert all(not a['intersections'] for a in read('SLIDE_PATH_CHECK_main.json'))
assert all(not k['intersections'] for a in read('KEY_RELEASE_CHECK.json') for k in a['keys'])
meshes=read('MESH_VALIDATION.json');assert all(all(m[k] for k in ['watertight','consistent_winding','positive_volume']) for m in meshes['checks'])
assert len(parts)==len(list((R/'prototype-stl').glob('*.stl')))==95
assert len({r['assembly_code'] for r in parts})==len(parts)
assert all((R/'render-meshes'/r['file']).is_file() for r in read('scene.json'))
class LocalLinks(HTMLParser):
    def __init__(self,root): super().__init__(); self.root=root
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ['href','src'] and v and not v.startswith(('#','http','data:')):assert (self.root/v).is_file(),v
for n in ['index.html','PART_LABELS.html','print-preparation.html','uic-voron-provisional/index.html']:LocalLinks((R/n).parent).feed((R/n).read_text(encoding='utf-8'))
for name in ['off','on','rgb-only','underside','breadboard','exploded','rgb-shield','rgb-section']:
    assert (R/'previews'/('lighting-'+name+'.png')).is_file()
for p in parts:assert (R/'previews'/'part-thumbnails'/(p['role']+'-'+p['name']+'.png')).is_file()
for role_report in read('ASSEMBLY_REVIEW.json'):
    for key in ['printed_part_intersections','gate_slider_intersections','shutter_travel_intersections','reveal_hood_rotation_and_removal_intersections','button_stroke_intersections']:
        assert not role_report[key],(role_report['role'],key)
    assert all(not v['conflicts'] for v in role_report['reserved_volume_checks'])
assert all(r['exposed'] for r in read('HIDDEN_FACE_CHECK.json'))
assert all(not r['conflicts'] for r in read('BASE_REPAIR_CHECK.json'))
assert read('PLATE_GEOMETRY_CHECK.json')['all_checks_passed']
assert read('PLANNER_CHECK.json')['three_mf_scene_placement_roundtrip']
plates=read('uic-voron-provisional/PLACEMENTS.json')['plates']
assert sum(len(p['parts']) for p in plates)==95
report=dict(revision=12,date='2026-11-04',status='Digital prototype checked; staff review and physical fit samples required',installed_printed_parts=95,physically_coded_parts=sum(p.get('id_location') is not None for p in parts),native_solids_checked=len(read('CAD_VALIDATION.json')['parts']),stl_meshes_checked=len(meshes['checks']),opaque_parts=88,translucent_parts=7,provisional_plate_count=len(plates),published_bed_mm=[290,290,285],printer_assignment_confirmed=False,production_released=False,green_led_count=4,main_rgb_secondary_shield=True,checks_repeated_for_revision12=['All final native solid validity','All STL mesh integrity','All three R12 assemblies and nominal component envelopes; final base repairs separately rechecked against every part/envelope','Gate, shutters, sensor hood and button sampled motion','Hidden lettering surface exposure','Lighting and bezel insertion checks','Synthetic plate packing and Prusa 3MF roundtrip','Guide handlers and local file links'],inherited_checks='Detailed indexed adjustment settings, jaw travel and key release retained from R11/R10; R12 changes only ownership and identification cuts. Lighting fade helper host test retained.',physical_fit_verified=False,optical_uniformity_measured=False,battery_runtime_measured=False,firmware_integrated=False,limits=['Nominal dimensions and provisional ESP32 envelope; real components require fit testing.','UIC default 0.6 mm nozzle / 0.3 mm layers is coarser than several current fits. Staff must review small features; print coupons first.','Part orientation and support access require slicer/staff review. No G-code or confirmed print duration provided.','Rendered glow is illustrative, not measured illumination.','Servo power, LED driver/current and battery runtime need bench testing.'],guide=read('GUIDE_CHECK.json'))
(R/'REVIEW_VALIDATION.json').write_text(json.dumps(report,indent=2))
files=[]
top=['index.html','PART_LABELS.html','README.md','R12_PRINT_NOTES.md','PRINT_AND_ASSEMBLY.md','PARTS.csv','ASSEMBLY_IDS.json','LIGHTING_LAYOUT.json','dimensions.json','scene.json','REVIEW_VALIDATION.json','CAD_VALIDATION.json','MESH_VALIDATION.json','ASSEMBLY_REVIEW.json','LIGHTING_CHECK.json','ADJUSTMENT_CHECK_main.json','SLIDE_PATH_CHECK_main.json','KEY_RELEASE_CHECK.json','GUIDE_CHECK.json','FADE_CHECK.json','build_revision11.py','build_revision10.py','adjustable_mounts.py','button_contact.py','safe_save.py','refine_r11.py','render_revision11.py','render_review.py','render_lighting.py','render_ids.py','render_engraving.py','render_printed_inventory.py','compose_inventory.py','make_r11_guide.py','prepare_r11_delivery.py','package_revision11.py','check_lighting.py','check_assembly.py','check_adjustments.py','check_slide_paths.py','check_key_release.py','check_meshes.py','check_guide.js','refresh_solid_validation.py']
top += ['UIC-Makerspace-receipt.jpg','UIC-Box-sharing.jpg','UIC-Box-public-access.jpg','UIC-Makerspace-0389-Box.jpg','UIC-Makerspace-0390-Box.jpg','SUBMISSION_MANIFEST.json','print-preparation.html','PRINT_BRIEF.md','PRINT_MANIFEST.csv','PRINT_PREP.json','HIDDEN_MARKS.json','HIDDEN_FACE_CHECK.json','PLANNER_CHECK.json','requirements-print-prep.txt','BASE_REPAIR_CHECK.json','PLATE_GEOMETRY_CHECK.json','check_repaired_bases.py','check_plate_geometry.py','fix_bezel_marks.py','build_revision12.py','fix_base_marks.py','check_hidden_faces.py','render_revision12.py','render_hidden.py','make_r12_guide.py','prepare_printing.py','arrange_plates.py','test_plate_planner.py','package_revision12.py']
files += [R/n for n in top]
files += [R/(role+'-adjustments.json') for role in ['explorer','architect','main']]
files += list((R/'cad').glob('*-revision12.FCStd'))+list((R/'cad').glob('*-printed-parts.step'))
for folder in ['baseline','baseline-r11','uic-voron-provisional','prototype-stl','render-meshes','inspection-meshes','previews','adjustment-options','optical-options','fit-tests','lighting']:
    files += [p for p in (R/folder).rglob('*') if p.is_file() and p.suffix.lower() in ['.fcstd','.stl','.3mf','.html','.png','.svg','.json','.md','.h','.cpp']]
manifest={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(files))}
(R/'SHA256.json').write_text(json.dumps(manifest,indent=2));files.append(R/'SHA256.json')
archive=R.parent/'Dual-Reality-Maze-Revision-12-Soham-Basanwar.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(set(files)):z.write(p,'revision-12/'+str(p.relative_to(R)))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(json.dumps(report,indent=2));print('ARCHIVE',str(archive),archive.stat().st_size,flush=True)
