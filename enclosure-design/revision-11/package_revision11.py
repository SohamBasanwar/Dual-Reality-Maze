from pathlib import Path
from html.parser import HTMLParser
import json,hashlib,zipfile
R=Path(__file__).resolve().parent
read=lambda n:json.loads((R/n).read_text())
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
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ['href','src'] and v and not v.startswith(('#','http','data:')):assert (R/v).is_file(),v
for n in ['index.html','PART_LABELS.html']:LocalLinks().feed((R/n).read_text(encoding='utf-8'))
for name in ['off','on','rgb-only','underside','breadboard','exploded','rgb-shield','rgb-section']:
    assert (R/'previews'/('lighting-'+name+'.png')).is_file()
for p in parts:assert (R/'previews'/'part-thumbnails'/(p['role']+'-'+p['name']+'.png')).is_file()
report=dict(revision=11,date='2026-10-31',status='Digital prototype checks passed; physical validation required',installed_printed_parts=len(parts),physically_coded_parts=sum(p.get('id_location') is not None for p in parts),native_solids_checked=len(read('CAD_VALIDATION.json')['parts']),stl_meshes_checked=len(meshes['checks']),green_led_count=4,main_rgb_secondary_shield=True,main_receiver_codes=4,intersection_threshold_mm3=.05,checks_repeated_for_revision11=['All STL mesh integrity','All final native solid validity','Main assembly static and component-envelope intersections','Main cable shutter travel','Main indexed adjustment settings','Main jaw travel','Main rigid key withdrawal','New green LED envelopes','New bezel rigid insertion paths (flexible hooks excluded)','RGB cap rotation and withdrawal','Compiled host test of actual fade helper','Guide links and gallery handler test'],inherited_checks='Explorer and Architect mechanical motion checks from Revision 10; changes there are subtractive identification engravings only. Their current solids and meshes are rechecked.',physical_fit_verified=False,optical_uniformity_measured=False,battery_runtime_measured=False,firmware_integrated=False,limits=['Nominal component dimensions and provisional ESP32 space; actual components not measured.','Clip strength, support accessibility, material opacity and actual light distribution require the sample prints.','Rendered glow and browser fading illustrate the intended effect; they are not measured illumination.','Power driver, spare PWM pin and battery runtime need bench verification.','A host Arduino stub verifies the helper, not board firmware or library timer coexistence.'],guide=read('GUIDE_CHECK.json'))
(R/'REVIEW_VALIDATION.json').write_text(json.dumps(report,indent=2))
files=[]
top=['index.html','PART_LABELS.html','README.md','R11_PRINT_NOTES.md','PRINT_AND_ASSEMBLY.md','PARTS.csv','ASSEMBLY_IDS.json','LIGHTING_LAYOUT.json','dimensions.json','scene.json','REVIEW_VALIDATION.json','CAD_VALIDATION.json','MESH_VALIDATION.json','ASSEMBLY_REVIEW.json','LIGHTING_CHECK.json','ADJUSTMENT_CHECK_main.json','SLIDE_PATH_CHECK_main.json','KEY_RELEASE_CHECK.json','GUIDE_CHECK.json','FADE_CHECK.json','build_revision11.py','build_revision10.py','adjustable_mounts.py','button_contact.py','safe_save.py','refine_r11.py','render_revision11.py','render_review.py','render_lighting.py','render_ids.py','render_engraving.py','render_printed_inventory.py','compose_inventory.py','make_r11_guide.py','prepare_r11_delivery.py','package_revision11.py','check_lighting.py','check_assembly.py','check_adjustments.py','check_slide_paths.py','check_key_release.py','check_meshes.py','check_guide.js','refresh_solid_validation.py']
files += [R/n for n in top]
files += [R/(role+'-adjustments.json') for role in ['explorer','architect','main']]
files += list((R/'cad').glob('*-revision11.FCStd'))+list((R/'cad').glob('*-printed-parts.step'))
for folder in ['baseline','prototype-stl','render-meshes','inspection-meshes','previews','adjustment-options','optical-options','fit-tests','lighting']:
    files += [p for p in (R/folder).rglob('*') if p.is_file() and p.suffix.lower() in ['.fcstd','.stl','.png','.svg','.json','.md','.h','.cpp']]
manifest={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(files))}
(R/'SHA256.json').write_text(json.dumps(manifest,indent=2));files.append(R/'SHA256.json')
archive=R.parent/'Dual-Reality-Maze-Revision-11-Soham-Basanwar.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(set(files)):z.write(p,'revision-11/'+str(p.relative_to(R)))
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(json.dumps(report,indent=2));print('ARCHIVE',str(archive),archive.stat().st_size,flush=True)
