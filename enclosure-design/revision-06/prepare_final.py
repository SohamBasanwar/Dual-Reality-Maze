from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parent
records=json.loads((R/'scene.json').read_text())
obsolete=R/'build-debug'/'obsolete-parts';obsolete.mkdir(parents=True,exist_ok=True)
for dirname,keep in [('prototype-stl',{r['file'] for r in records if not r['component']}),('render-meshes',{r['file'] for r in records})]:
    parent=(R/dirname).resolve()
    for p in parent.glob('*.stl'):
        if p.name not in keep:
            assert p.resolve().parent==parent and parent.is_relative_to(R)
            shutil.move(str(p),str(obsolete/(dirname+'-'+p.name)))
P=json.loads((R/'dimensions.json').read_text())
P.update({'reveal_sensor_centre_xy':[123,117],'reveal_dome_outer_diameter':20,'reveal_base_collar_diameter':24,'reveal_dome_height_above_lid':11,'reveal_lead_bore_diameter':1.0,'reveal_lead_pitch_provisional':2.54,'reveal_default_roof_thickness':.4,'reveal_optical_status':'Untested. Thin opaque filament may block light. Test roofs or use clear-film alternative.'})
(R/'dimensions.json').write_text(json.dumps(P,indent=2))
print('Active printed parts',sum(not r['component'] for r in records))
