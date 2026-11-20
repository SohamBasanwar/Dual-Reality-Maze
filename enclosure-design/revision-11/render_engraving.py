from pathlib import Path
src=Path(__file__).with_name('render_review.py').read_text(encoding='utf-8').split("if not requested or 'cases'")[0]
exec(compile(src,__file__,'exec'))
# Coordinates are exported assembly coordinates in mm. Tight camera crops
# show real recessed cuts; no lettering is composited onto a smooth model.
shots=[
('engraving-base','explorer','Base',(111,44,0),(.08,-.25,-1),64),
('engraving-lid','explorer','Lid',(110,102,54.2),(.08,-.25,-1),61),
('engraving-door','explorer','Battery_Door',(204,146,2.55),(.08,-.25,1),42),
('engraving-insert','explorer','Breadboard_Height_Insert',(123,71.5,9.2),(.04,-.25,1),56),
('engraving-jaw','explorer','Breadboard_X_Jaw',(40,95.5,20.85),(.2,-.35,1),21),
('engraving-shutter','main','USB_Shutter',(117,-5.1,32.5),(.0,-1,.35),24)]
for filename,role,name,target,direction,scale_mm in shots:
    records=[r for r in original if r['role']==role and r['name']==name]
    s,m=studio();m['bronze'].diffuse_color=(.61,.62,.64,1);load(role,'all',m)
    W=234 if role=='main' else 246;D=180 if role=='main' else 207
    center=Vector(((target[0]-W/2)*.001,(target[1]-D/2)*.001,target[2]*.001))
    if name in ['Base','Lid']:
        # Turn the solid over for studio lighting and upright underside text.
        turn=Matrix.Translation(center) @ Matrix.Rotation(math.pi,4,'X') @ Matrix.Translation(-center)
        bpy.context.view_layer.update()
        for ob in bpy.data.objects:
            if ob.type=='MESH':ob.matrix_world=turn @ ob.matrix_world
        direction=(.04,-.3,1)
    camera(s,center+Vector(direction).normalized()*.5,center,scale_mm*.001)
    if name in ['Base','Lid']:
        s.camera.rotation_euler.rotate_axis('Z',math.pi)
    s.render.resolution_x=1400;s.render.resolution_y=800
    save(s,filename)
print('Six real engraving close-ups rendered')
