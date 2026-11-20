from pathlib import Path
import sys,json
import numpy  # use FreeCAD's matching binary, before the pure-Python helpers
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'build'/'python-tools'))
import trimesh
result=[]
for p in sorted((R/'prototype-stl').glob('*.stl'))+sorted((R/'fit-tests').glob('*.stl'))+sorted((R/'optical-options').glob('*.stl'))+sorted((R/'adjustment-options').glob('*.stl')):
    m=trimesh.load(p,force='mesh')
    row={'file':str(p.relative_to(R)),'watertight':bool(m.is_watertight),'consistent_winding':bool(m.is_winding_consistent),'positive_volume':bool(m.volume>0),'bounds_mm':m.extents.tolist(),'faces':len(m.faces)}
    if not all(row[k] for k in ['watertight','consistent_winding','positive_volume']):raise RuntimeError(str(row))
    result.append(row)
(R/'MESH_VALIDATION.json').write_text(json.dumps({'scope':'Mesh integrity only; physical fit, material strength and print settings unverified.','checks':result},indent=2))
print(f'{len(result)} meshes passed watertightness, winding and positive-volume checks.')
