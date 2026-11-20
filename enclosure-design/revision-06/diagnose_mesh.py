from pathlib import Path
import sys,json
R=Path(__file__).resolve().parent;sys.path.insert(0,str(R.parent/'build'/'python-tools'))
import trimesh,numpy as np
for p in sorted((R/'prototype-stl').glob('*.stl'))+sorted((R/'fit-tests').glob('*.stl'))+sorted((R/'optical-options').glob('*.stl')):
    m=trimesh.load(p,force='mesh')
    if m.is_watertight:continue
    n=np.bincount(m.edges_unique_inverse);bad=m.edges_unique[n!=2];vv=m.vertices[bad]
    print(p.name,'bad edges',len(bad),'bounds',vv.reshape(-1,3).min(axis=0),vv.reshape(-1,3).max(axis=0),flush=True)
    print('samples',vv[:6].tolist(),flush=True)
    for dig in [6,5,4,3]:
        c=m.copy();c.merge_vertices(digits_vertex=dig);print(' weld',dig,c.is_watertight,len(c.vertices),flush=True)
