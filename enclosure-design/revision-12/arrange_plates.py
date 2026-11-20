"""Provisional single-material plates after usable dimensions are supplied.
Run using FreeCAD's bundled Python. Example placeholders, not real dimensions:
  arrange_plates.py --width WIDTH --depth DEPTH --height HEIGHT
No scaling, slicing, support generation, sequential-object printing or G-code.
"""
from pathlib import Path
import argparse,json,math,zipfile,html,sys
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent

def intersects(a,b):return a[0]<b[0]+b[2]-1e-7 and a[0]+a[2]>b[0]+1e-7 and a[1]<b[1]+b[3]-1e-7 and a[1]+a[3]>b[1]+1e-7
def contains(a,b):return b[0]>=a[0]-1e-7 and b[1]>=a[1]-1e-7 and b[0]+b[2]<=a[0]+a[2]+1e-7 and b[1]+b[3]<=a[1]+a[3]+1e-7
def occupy(free,used):
    out=[]
    for r in free:
        if not intersects(r,used):out.append(r);continue
        x,y,w,h=r;u,v,a,b=used
        if u>x:out.append((x,y,u-x,h))
        if u+a<x+w:out.append((u+a,y,x+w-u-a,h))
        if v>y:out.append((x,y,w,v-y))
        if v+b<y+h:out.append((x,v+b,w,y+h-v-b))
    out=list(dict.fromkeys(r for r in out if min(r[2:])>1e-6))
    return [r for i,r in enumerate(out) if not any(i!=j and contains(s,r) for j,s in enumerate(out))]

def pack(parts,width,depth,height,margin=8,allowance=5,gap=4):
    assert min(width,depth,height)>0 and margin>=0 and allowance>=0 and gap>=0
    usable=(width-2*margin,depth-2*margin);assert min(usable)>0
    plates=[];pending=sorted(parts,key=lambda r:max(r['print_bbox_xyz_mm'][:2]),reverse=True)
    for row in pending:
        w,d,h=row['print_bbox_xyz_mm'];pw=w+2*allowance+gap;pd=d+2*allowance+gap
        if h>height or not ((pw<=usable[0] and pd<=usable[1]) or (pd<=usable[0] and pw<=usable[1])):
            raise ValueError(f"{row['code']} cannot fit the supplied bed/height with allowances; do not scale it. Bounds {w:.2f} x {d:.2f} x {h:.2f} mm")
        choices=[]
        for pi,p in enumerate(plates):
            for fi,(x,y,fw,fd) in enumerate(p['free']):
                for rotate,(a,b) in enumerate([(pw,pd),(pd,pw)]):
                    if a<=fw+1e-7 and b<=fd+1e-7:choices.append(((min(fw-a,fd-b),max(fw-a,fd-b)),pi,x,y,a,b,rotate))
        if not choices:
            plates.append(dict(free=[(margin,margin,*usable)],parts=[]));pi=len(plates)-1
            options=[(0,pw,pd),(1,pd,pw)];rotate,a,b=min((q for q in options if q[1]<=usable[0] and q[2]<=usable[1]),key=lambda q:min(usable[0]-q[1],usable[1]-q[2]))
            choice=((0,0),pi,margin,margin,a,b,rotate)
        else:choice=min(choices,key=lambda q:q[0])
        _,pi,x,y,a,b,rotate=choice;used=(x,y,a,b)
        plates[pi]['free']=occupy(plates[pi]['free'],used)
        placed=dict(row,plate_rotate_z_deg=90*rotate,reserved_xywh_mm=list(used),placement_xy_mm=[x+allowance+gap/2,y+allowance+gap/2])
        plates[pi]['parts'].append(placed)
    for p in plates:
        for i,a in enumerate(p['parts']):
            assert contains((0,0,width,depth),a['reserved_xywh_mm'])
            assert all(not intersects(a['reserved_xywh_mm'],b['reserved_xywh_mm']) for b in p['parts'][i+1:])
    assert sorted(r['code'] for p in plates for r in p['parts'])==sorted(r['code'] for r in parts)
    return plates

def write3mf(path,meshes):
    ns='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';ET.register_namespace('',ns)
    q=lambda s:'{'+ns+'}'+s
    model=ET.Element(q('model'),unit='millimeter');ET.SubElement(model,q('metadata'),name='Title').text='Dual-Reality Maze / Soham Basanwar / provisional plate'
    resources=ET.SubElement(model,q('resources'));build=ET.SubElement(model,q('build'))
    for i,(name,m) in enumerate(meshes,1):
        ob=ET.SubElement(resources,q('object'),id=str(i),type='model',name=name);me=ET.SubElement(ob,q('mesh'));vs=ET.SubElement(me,q('vertices'));ts=ET.SubElement(me,q('triangles'))
        for x,y,z in m.vertices:ET.SubElement(vs,q('vertex'),x=f'{x:.5f}',y=f'{y:.5f}',z=f'{z:.5f}')
        for a,b,c in m.faces:ET.SubElement(ts,q('triangle'),v1=str(a),v2=str(b),v3=str(c))
        ET.SubElement(build,q('item'),objectid=str(i))
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml','<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/></Types>')
        z.writestr('_rels/.rels','<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rel0" Target="/3D/3dmodel.model" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>')
        z.writestr('3D/3dmodel.model',ET.tostring(model,encoding='utf-8',xml_declaration=True))

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--width',type=float,required=True);p.add_argument('--depth',type=float,required=True);p.add_argument('--height',type=float,required=True)
    p.add_argument('--margin',type=float,default=8);p.add_argument('--allowance',type=float,default=5);p.add_argument('--gap',type=float,default=4);p.add_argument('--output',default='provisional-plates')
    p.add_argument('--refresh',action='store_true',help='Refresh an existing layout for the same installed part set; does not delete files.')
    a=p.parse_args();manifest=json.loads((R/'PRINT_PREP.json').read_text(encoding='utf-8'));all_plates=[]
    for material in ['OPAQUE','TRANSLUCENT']:
        group=[r for r in manifest['parts'] if r['material_group']==material]
        for i,plate in enumerate(pack(group,a.width,a.depth,a.height,a.margin,a.allowance,a.gap),1):plate.update(id=f'{material}-{i:02}',material=material);all_plates.append(plate)
    import numpy as np
    sys.path.insert(0,str(R.parent/'build/python-tools'))
    import trimesh
    from prepare_printing import rotation
    out=(R/a.output).resolve()
    if out.exists():
        if not a.refresh:raise RuntimeError('Use a new output directory or explicitly refresh this same layout.')
        previous=json.loads((out/'PLACEMENTS.json').read_text(encoding='utf-8'))
        assert {p['id'] for p in previous['plates']}=={p['id'] for p in all_plates}
        assert sorted(r['code'] for p in previous['plates'] for r in p['parts'])==sorted(r['code'] for p in all_plates for r in p['parts'])
    out.mkdir(parents=True,exist_ok=True);links=[]
    for plate in all_plates:
        folder=out/plate['id'];folder.mkdir(exist_ok=True);meshes=[]
        svg=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {a.width} {a.depth}"><rect width="100%" height="100%" fill="#18212a"/>']
        for r in plate['parts']:
            mesh=trimesh.load(R/r['file'],force='mesh');v=np.asarray(mesh.vertices) @ rotation(*r['rotation_xyz_deg']).T
            v=v @ rotation(0,0,r['plate_rotate_z_deg']).T;v-=v.min(axis=0);v[:,:2]+=r['placement_xy_mm'];mesh.vertices=v
            mesh.export(folder/Path(r['file']).name);meshes.append((r['code']+' '+r['name']+' Soham Basanwar',mesh))
            x,y,w,d=r['reserved_xywh_mm'];svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{d}" fill="#6b5138" stroke="#c9b080" stroke-width=".5"/><text x="{x+2}" y="{y+5}" font-family="sans-serif" font-size="4" fill="white">{r["code"]}</text>')
        svg.append('</svg>');(out/(plate['id']+'.svg')).write_text(''.join(svg),encoding='utf-8');write3mf(out/(plate['id']+'.3mf'),meshes)
        links.append(f'<h2>{plate["id"]} · {len(plate["parts"])} pieces</h2><img width="600" src="{plate["id"]}.svg"><p><a href="{plate["id"]}.3mf">3MF</a></p>')
        del plate['free']
    (out/'PLACEMENTS.json').write_text(json.dumps(dict(provisional=True,units='mm',settings=vars(a),plates=all_plates),indent=2),encoding='utf-8')
    (out/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>Provisional plates</title><h1>Provisional print plates</h1><p>Not sliced. Review orientation, supports, bed exclusions and clips. One material per plate; no scaling. Print by layer, not sequential objects. Boxes show reserved bounding footprints, not supports.</p>'+''.join(links),encoding='utf-8')
    print('Prepared',len(all_plates),'provisional plates at',out)

if __name__=='__main__':main()
