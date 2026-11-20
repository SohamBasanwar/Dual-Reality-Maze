"""Prepare material batches and candidate print orientation; no assumed bed size."""
from pathlib import Path
import sys,json,csv,math
import numpy as np
R=Path(__file__).resolve().parent
sys.path.insert(0,str(R.parent/'build/python-tools'))
import trimesh

def rotation(rx,ry,rz):
    a,b,c=np.radians([rx,ry,rz]);cx,sx=np.cos(a),np.sin(a);cy,sy=np.cos(b),np.sin(b);cz,sz=np.cos(c),np.sin(c)
    return np.array([[cz,-sz,0],[sz,cz,0],[0,0,1]]) @ np.array([[cy,0,sy],[0,1,0],[-sy,0,cy]]) @ np.array([[1,0,0],[0,cx,-sx],[0,sx,cx]])

def settings(name,material):
    angles=[0,0,0];support='Review overhangs and bed contact in slicer; keep supports out of fitted slots.'
    if material=='TRANSLUCENT':return angles,'Flat optical insert; no support expected. Check solid thin layers and actual light diffusion.',4
    if name=='Base':return angles,'Open side up. Review grip curvature and cable-hatch overhangs; no trapped supports in rails.',2
    if name=='Lid':return [180,0,0],'Candidate exterior face down. Sculpted surfaces need contact/support review. Block supports in enclosed light galleries; coupon first.',2
    if name=='Battery_Door':return [180,0,0],'Candidate interior face down; inspect latching projections and support access. Preserve the smooth hand-contact surface.',3
    if name.startswith('Light_') and name.endswith('_Bezel'):return [180,0,0],'Broad clean exterior face down, legs up. Inspect hook bridges and clip-layer strength.',3
    if name in ['Gate_Panel','Gate_Frame','Gate_Shroud']:return [90,0,0],'Candidate broad back face down; review gate rail bridges and removeable supports before approving.',3
    if name in ['I2C_Rear_Shutter','USB_Shutter']:return [-90,0,0],'Interior flat plate face toward bed; external finger tab up. Keep running faces support-free.',3
    if name=='I2C_Left_Shutter':return [0,-90,0],'Interior flat plate face toward bed; external finger tab up. Check first-layer expansion.',3
    if name=='I2C_Right_Shutter':return [0,90,0],'Interior flat plate face toward bed; external finger tab up. Check first-layer expansion.',3
    if name=='Reveal_Dome':support='Opaque sensor pod with thin trial roof. Optical sample required; use existing clear-window alternative if the roof blocks light.'
    if name in ['Button_Cap','Gate_Drive_Pin','Gate_Pin_Keeper']:
        support='Small working part: orientation, stem/pin strength and support removal require individual slicer review.'
    if name.endswith(('_Lock_Key','_Height_Insert')):support='Flat orientation candidate. Keep flexible detent and narrow indexed slots free of support; test fit.'
    return angles,support,3

def main():
    records=[]
    for row in json.loads((R/'scene.json').read_text(encoding='utf-8')):
        if row['component']:continue
        material='TRANSLUCENT' if row['material'] in ['diffuser','green_diffuser'] else 'OPAQUE'
        angles,note,stage=settings(row['name'],material)
        mesh=trimesh.load(R/'prototype-stl'/row['file'],force='mesh');v=np.asarray(mesh.vertices) @ rotation(*angles).T
        low=v.min(axis=0);size=v.max(axis=0)-low
        records.append(dict(code=row['assembly_code'],role=row['role'],name=row['name'],file='prototype-stl/'+row['file'],quantity=1,material_group=material,material='Neutral translucent PLA' if material=='TRANSLUCENT' else 'Opaque PLA prototype; bronze if available, black stock fallback',stage=stage,rotation_xyz_deg=angles,orientation_min_xyz_mm=low.tolist(),print_bbox_xyz_mm=size.tolist(),nominal_solid_volume_mm3=float(mesh.volume),support_review=note,orientation_verified_by_slicing=False))
    result=dict(revision=12,units='mm',usable_bed_width_mm=None,usable_bed_depth_mm=None,usable_bed_height_mm=None,printer=None,nozzle_mm=None,production_released=False,material_groups={'OPAQUE':sum(r['material_group']=='OPAQUE' for r in records),'TRANSLUCENT':sum(r['material_group']=='TRANSLUCENT' for r in records)},parts=records)
    (R/'PRINT_PREP.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    with (R/'PRINT_MANIFEST.csv').open('w',newline='',encoding='utf-8-sig') as f:
        keys=['code','role','name','quantity','material_group','material','stage','rotation_xyz_deg','print_bbox_xyz_mm','support_review','file'];w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
        for r in records:w.writerow({k:r[k] for k in keys})
    print('Prepared',len(records),'parts:',result['material_groups'],'; bed dimensions remain unset.')

if __name__=='__main__':main()
