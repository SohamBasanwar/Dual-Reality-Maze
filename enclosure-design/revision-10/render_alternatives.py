from pathlib import Path
src=Path(__file__).with_name('render_review.py').read_text(encoding='utf-8').split("if not requested or 'cases'")[0]
exec(compile(src,__file__,'exec'))
for kind,name in [('servo-width','Servo_Fit_Insert'),('button-reach','Button_Contact_Shoe')]:
    for mode in ['minus','nominal','plus']:
        records=[r for r in original if r['role']=='architect' and r['name']==name] if mode=='nominal' else []
        s,m=studio();m['bronze'].diffuse_color=(.62,.64,.66,1)
        if mode=='nominal':load('architect','all',m)
        else:extra_mesh(R/'adjustment-options'/f'architect-{kind}-{mode}-Soham-Basanwar.stl','architect',m,kind)
        frame(s,(.5,-.7,1));save(s,kind+'-'+mode)
