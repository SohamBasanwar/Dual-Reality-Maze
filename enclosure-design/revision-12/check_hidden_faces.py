from pathlib import Path
R=Path(__file__).resolve().parent
exec(compile((R/'build_revision12.py').read_text(encoding='utf-8').split('for role in selected:')[0],__file__,'exec'))
records=json.loads((R/'HIDDEN_MARKS.json').read_text(encoding='utf-8'))['new_hidden_marks']
report=[]
for role in ['explorer','architect','main']:
    d=A.openDocument(str(R/'cad'/f'{role}-revision12.FCStd'))
    for loc in records:
        if loc['role']!=role or 'z_mm' not in loc:continue
        q=code_tool(loc);q.translate(V(0,0,-.25 if loc['underside'] else .25))
        # Check immediately outside the face; a distant clip lip may occlude
        # a straight view without making the engraving an enclosed void.
        q=q.common(box(-500,-500,loc['z_mm']-.04 if loc['underside'] else loc['z_mm']+.01,1000,1000,.03))
        blocked=d.getObject(loc['name']).Shape.common(q).Volume
        report.append(dict(role=role,name=loc['name'],label=loc['label'],outside_probe_intersection_mm3=blocked,exposed=blocked<.001))
    A.closeDocument(d.Name)
(R/'HIDDEN_FACE_CHECK.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
assert all(r['exposed'] for r in report),[r for r in report if not r['exposed']]
print(len(report),'flat-face lettering cuts open onto actual surfaces')
