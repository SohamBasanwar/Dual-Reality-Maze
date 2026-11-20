import FreeCAD as A,json
from pathlib import Path
R=Path(__file__).resolve().parent;scene=json.loads((R/'scene.json').read_text())
for role in ['explorer','architect','main']:
    d=A.openDocument(str(R/'cad'/f'{role}-revision10.FCStd'))
    for row in [r for r in scene if r['role']==role]:
        obj=d.getObject(row['name']);assert obj
        row['volume_mm3']=obj.Shape.Volume;row['solids']=len(obj.Shape.Solids)
        if hasattr(obj,'DesignNotes'):row['notes']=obj.DesignNotes
        if hasattr(obj,'Personalization'):row['personalization']=obj.Personalization
        if role!='main' and row['name'] in ['UNO_Y_Jaw','Breadboard_Y_Jaw']:
            row['notes']='Captured edge jaw. Breadth settings: nominal or 3 mm smaller; nominal is the largest permitted setting.'
    A.closeDocument(d.Name)
(R/'scene.json').write_text(json.dumps(scene,indent=2))
print('Scene manifest refreshed from final native documents')
