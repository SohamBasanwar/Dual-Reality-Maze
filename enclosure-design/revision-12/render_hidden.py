"""Photographs of the actual R12 engraved CAD surfaces, not text overlays."""
from pathlib import Path
src=Path(__file__).with_name('render_review.py').read_text(encoding='utf-8').split("if not requested or 'cases'")[0]
exec(compile(src,__file__,'exec'))
marks=json.loads((R/'HIDDEN_MARKS.json').read_text(encoding='utf-8'))['new_hidden_marks']
shots=[('hidden-base-explorer','explorer','Base','owner',65),('hidden-base-main','main','Base','owner',65),('hidden-button','architect','Button_Cap','code',23),('hidden-shutter','main','USB_Shutter','code',25),('hidden-bezel','main','Light_G1_Bezel','code',28),('hidden-receiver','main','Lid','receiver',30)]
for filename,role,name,kind,width in shots:
    candidates=[r for r in marks if r['role']==role and r['name']==name and r['kind']==kind]
    if not candidates:continue
    mark=candidates[0];records=[r for r in original if r['role']==role and r['name']==name]
    s,m=studio();m['bronze'].diffuse_color=(.64,.65,.66,1);load(role,'all',m)
    W=234 if role=='main' else 246;D=180 if role=='main' else 207
    if 'centre_mm' in mark:
        x,y,z=mark['centre_mm'];z-=2.5;direction=Vector(mark['view_direction'])+Vector((0,0,.1));under=False
    else:
        b=mark.get('bounds_xywh_mm')
        if b:x,y=b[0]+b[2]/2,b[1]+b[3]/2
        else:x,y=mark['xy_mm'][0]+(25 if kind=='owner' else 3),mark['xy_mm'][1]+1
        z=mark['z_mm'];under=mark['underside'];direction=Vector((.04,-.22,1))
        if name=='Light_G1_Bezel':x+=3
        if name=='Button_Cap':y-=5;width=34;direction=Vector((.01,-.01,1))
    center=Vector(((x-W/2)*.001,(y-D/2)*.001,z*.001))
    if 'centre_mm' in mark:
        bpy.context.view_layer.update()
        turn=Matrix.Translation(center)@Vector(mark['view_direction']).rotation_difference(Vector((0,0,1))).to_matrix().to_4x4()@Matrix.Translation(-center)
        for ob in bpy.data.objects:
            if ob.type=='MESH':ob.matrix_world=turn@ob.matrix_world
        direction=Vector((.04,-.15,1))
    if name=='Light_G1_Bezel':direction=Vector((0,-.04,1))
    if under:
        bpy.context.view_layer.update();turn=Matrix.Translation(center)@Matrix.Rotation(math.pi,4,'X')@Matrix.Translation(-center)
        for ob in bpy.data.objects:
            if ob.type=='MESH':ob.matrix_world=turn@ob.matrix_world
    camera(s,center+direction.normalized()*.5,center,width*.001)
    if under:s.camera.rotation_euler.rotate_axis('Z',math.pi)
    s.render.resolution_x=1400;s.render.resolution_y=800;save(s,filename)
    if filename=='hidden-base-explorer':save(s,'engraving-base')
    if filename=='hidden-shutter':save(s,'engraving-shutter')
print('Hidden engraving surfaces rendered')
