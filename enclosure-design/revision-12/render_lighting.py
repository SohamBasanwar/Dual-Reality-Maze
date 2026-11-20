"""R12 images from real CAD meshes. Emission is illustrative, not ray-tested LEDs."""
from pathlib import Path
src=Path(__file__).with_name('render_review.py').read_text(encoding='utf-8').split("if not requested or 'cases'")[0]
exec(compile(src,__file__,'exec'))
role='main';original=records[:]

for mode in ['off','on','rgb-only','underside','breadboard','exploded','rgb-shield','rgb-section','coupon']:
    records=[r for r in original if r['role']=='main']
    if mode=='breadboard':records=[r for r in records if isbase(r)]
    if mode in ['underside','exploded']:records=[r for r in records if not isbase(r)]
    if mode in ['rgb-shield','rgb-section']:records=[r for r in records if r['name'] in ['Lid','RGB_Isolation_Cap','RGB_LED_Keeper','RGB_LED_Envelope','Emblem_Diffuser','Emblem_Mask']]
    if mode=='coupon':records=[r for r in records if r['name'] in ['Light_G1_Diffuser','Light_G1_Bezel','Green_G1_LED_Envelope']]
    s,m=studio()
    if mode in ['off','on','rgb-only']:
        s.render.engine='CYCLES';s.cycles.samples=32;s.cycles.use_denoising=True
        s.view_settings.view_transform='AgX';s.view_settings.exposure=-.7
        m['bronze'].node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.24,.095,.032,1)
        for key in ['green_diffuser','green_led']:
            p=m[key].node_tree.nodes.get('Principled BSDF')
            p.inputs['Base Color'].default_value=(.42,.50,.42,1) if mode!='on' else (.02,.75,.11,1)
            p.inputs['Emission Strength'].default_value=3 if mode=='on' else 0
        m['main'].node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=2 if mode in ['on','rgb-only'] else 0
        if mode=='off':m['main'].node_tree.nodes.get('Principled BSDF').inputs['Base Color'].default_value=(.42,.45,.43,1)
        load(role,'assembled',m);frame(s,(.28,.9,1.25),.89)
        tree=bpy.data.node_groups.new('R12 lighting glow','CompositorNodeTree');s.compositing_node_group=tree
        tree.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
        n=tree.nodes;a=n.new('CompositorNodeRLayers');g=n.new('CompositorNodeGlare')
        g.inputs['Type'].default_value='Fog Glow';g.inputs['Quality'].default_value='High';g.inputs['Strength'].default_value=.45
        if g.inputs.get('Threshold'):g.inputs['Threshold'].default_value=1.3
        c=n.new('NodeGroupOutput');tree.links.new(a.outputs['Image'],g.inputs['Image']);tree.links.new(g.outputs['Image'],c.inputs['Image'])
    else:
        load(role,'all',m)
        if mode=='coupon':
            extra_mesh(R/'fit-tests'/'M-lighting-G1-coupon-Soham-Basanwar.stl','main',m,'Actual G1 test coupon')
            bpy.data.objects['main Light_G1_Diffuser'].location.z+=.012
            bpy.data.objects['main Light_G1_Bezel'].location.z+=.025
            frame(s,(.3,.7,1),.87)
        elif mode=='underside':frame(s,(.2,.2,-1),.89)
        elif mode=='breadboard':frame(s,(.05,.1,1.4),.88)
        elif mode=='exploded':
            for r in records:
                o=bpy.data.objects.get(role+' '+r['name'])
                if r['name'].endswith('_Diffuser') and r['name'].startswith('Light_'):o.location.z+=.025
                if r['name'].endswith('_Bezel'):o.location.z+=.048
                if r['name']=='RGB_Isolation_Cap':o.location.z-=.025
            frame(s,(.35,.7,1),.88)
        else:
            # Local clipped assembly for inspection. An exact mesh slice is
            # removed, so internal wall and double-floor cap can be seen.
            for o in list(bpy.data.objects):
                if o.type!='MESH':continue
                if o.name=='main Lid':
                    import bmesh
                    bm=bmesh.new();bm.from_mesh(o.data)
                    for pt,no in [((86,0,0),(-1,0,0)),((148,0,0),(1,0,0)),((0,77,0),(0,-1,0)),((0,139,0),(0,1,0))]:
                        bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.00001,plane_co=pt,plane_no=no,clear_outer=True,clear_inner=False)
                    bm.to_mesh(o.data);bm.free()
                if mode=='rgb-section':
                    import bmesh
                    bm=bmesh.new();bm.from_mesh(o.data)
                    bmesh.ops.bisect_plane(bm,geom=list(bm.verts)+list(bm.edges)+list(bm.faces),dist=.00001,plane_co=(117,108,0),plane_no=(0,1,0),clear_outer=True,clear_inner=False)
                    bm.to_mesh(o.data);bm.free()
            if mode=='rgb-shield':bpy.data.objects['main RGB_Isolation_Cap'].location.z-=.018
            frame(s,(.2,1,-.3) if mode=='rgb-section' else (.3,.8,-1),.8)
    s.render.resolution_x=1600;s.render.resolution_y=1100
    save(s,'lighting-'+mode)
print('Lighting CAD views complete')
