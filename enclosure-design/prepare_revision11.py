from pathlib import Path
import json, shutil
R=Path(__file__).resolve().parent
S=R/'revision-10'; D=R/'revision-11';D.mkdir(exist_ok=True)
for rel in json.loads((S/'SHA256.json').read_text()):
    p=S/rel;q=D/rel
    if p.is_file():q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
(D/'baseline').mkdir(exist_ok=True)
for role in ['explorer','architect','main']:
    shutil.copy2(S/'cad'/f'{role}-revision10.FCStd',D/'baseline'/f'{role}-revision10.FCStd')
for f in ['check_assembly.py','check_adjustments.py','check_slide_paths.py','check_key_release.py','refresh_solid_validation.py','refresh_scene.py','render_review.py','render_engraving.py','render_printed_inventory.py','render_alternatives.py','render_mounts.py','render_revision10.py','make_visual_guide.py']:
    (D/f.replace('revision10','revision11')).write_text((S/f).read_text(encoding='utf-8').replace('revision10','revision11').replace('R10','R11').replace('Revision 10','Revision 11'),encoding='utf-8')
shutil.copy2(S/'scene.json',D/'baseline'/'scene.json')
print('Revision 11 workspace prepared; Revision 10 preserved.')
