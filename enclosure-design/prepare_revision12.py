from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parent;S=R/'revision-11';D=R/'revision-12'
D.mkdir(exist_ok=True)
for rel in json.loads((S/'SHA256.json').read_text(encoding='utf-8')):
    p=S/rel;q=D/rel
    if p.is_file():q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
(D/'baseline-r11').mkdir(exist_ok=True)
for role in ['explorer','architect','main']:
    shutil.copy2(S/'cad'/f'{role}-revision11.FCStd',D/'baseline-r11'/f'{role}-revision11.FCStd')
for name in ['scene.json','ASSEMBLY_IDS.json','REVIEW_VALIDATION.json']:
    shutil.copy2(S/name,D/'baseline-r11'/name)
for name in ['check_assembly.py','check_adjustments.py','check_slide_paths.py','check_key_release.py','check_lighting.py','refresh_solid_validation.py','render_review.py','render_engraving.py','render_ids.py','render_printed_inventory.py','compose_inventory.py','render_lighting.py','render_revision11.py']:
    out=name.replace('revision11','revision12')
    text=(S/name).read_text(encoding='utf-8').replace('revision11','revision12').replace('R11','R12').replace('Revision 11','Revision 12').replace('REVISION 11','REVISION 12')
    (D/out).write_text(text,encoding='utf-8')
print('Revision 12 workspace prepared')
