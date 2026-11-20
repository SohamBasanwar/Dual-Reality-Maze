"""R10 indexed edge mounts. Units mm. Model coordinates before export X mirror.

An L-shaped pair of datum edges locates a board; two captured jaws adjust
length/depth independently. Cross keys lock the slide, not clamp force.
Thin one-piece height inserts are alternatives, never loose stacked washers.
"""
import FreeCAD as A
import Part, math
V=A.Vector

def jaw_sweep(axis,t,box,union):
    """Continuous clearance for the UNSLOTTED jaw, including its cross-hole.
    Subtracting only indexed, slotted jaw poses leaves blocking islands.
    """
    lo=-max(axis['range_mm']);hi=-min(axis['range_mm']);span=hi-lo
    raw=[(-1,-2.95,.95,16,5.9,1.6),(-1,-1.55,2.5,16,3.1,1.6),
         (-2,-5,.95,1.8,10,4.85+t),(-2,-5,5.65+t,3.4,10,1.4)]
    q=union([box(u+lo-.2,v-.2,z-.2,w+span+.4,d+.4,h+.4) for u,v,z,w,d,h in raw])
    q.rotate(V(),V(0,0,1),180 if axis['axis']=='X' else 270)
    q.translate(V(*axis['origin']));return q

def key_sweep(axis,box,union):
    """Clear rigid key and handle withdrawal; retain the flexible tip detent."""
    reverse=axis['axis']=='X' and axis.get('key_release_pre',[0,-1,0])[1]>0
    raw=[(8.1,-4.75,1.12,1.8,12.15,1.2),(8.1,5,1.12,1.8,2.4,2.68),
         (-7,5,2.6,16,2.4,1.2),(-8,3.5,2.6,3.6,5.4,1.4)]
    shapes=[]
    for delta in axis['range_mm']:
        q=union([box(u-delta-.12,v-.12,z-.12,w+.24,d+10.5+.24,h+.24) for u,v,z,w,d,h in raw])
        if reverse:q=q.mirror(V(),V(0,1,0))
        q.rotate(V(),V(0,0,1),180 if axis['axis']=='X' else 270);q.translate(V(*axis['origin']));shapes.append(q)
    return union(shapes)

def adjustable_mount(prefix,x,y,w,d,z,t,box,cyl,union,cut,moved,text_cut,control=False,limit_front=False,edge_y=None):
    # Board underside is z+5.4 with the nominal 1.2 mm keyed frame installed.
    board_z=z+5.4; ledge_z=z+4.2; parts=[]; tracks=[]; fixed=[]
    # Three separated datum corners leave USB/header and key access open.
    for xx,yy in [(x+1,y+1),(x+w-10,y+1),(x+1,y+d-14)]:
        fixed.append(box(xx,yy,z,4.4 if control else 10,4.4 if control else 8.5,4.2))
    for yy in [y+3,y+d-12]:
        fixed += [box(x-1.6,yy,z,1.4,8,5.4+t+.25),box(x-1.6,yy,z+5.65+t,2.6,8,1.2)]
    for xx in [x+3,x+w-12]:
        fixed += [box(xx,y-1.6,z,8,1.4,5.4+t+.25),box(xx,y-1.6,z+5.65+t,8,2.6,1.2)]
    # Narrow perimeter webs connect all fixed supports while clearing the
    # board underside. These are fixed to the base or carrier, not loose.
    fixed += [box(x-1.6,y-1.6,z,w+3.2,1.6,1.6),box(x-1.6,y-1.6,z,1.6,d+3.2,1.6),
              box(x-1.6,y+d,z,w+3.2,1.6,1.6),box(x+w,y-1.6,z,1.6,d+3.2,1.6)]
    fixed += [box(x-1.6,y-1.6,z,w+3.2,7.2,1.0),box(x-1.6,y-1.6,z,7.2,d+3.2,1.0)]
    cross_y=edge_y if edge_y is not None else 8 if prefix=='Joystick' else 4 if prefix=='LCD' else d*.5
    cross_x=8 if prefix=='Joystick' else w-24 if prefix=='LCD' else w*.5
    def pose(s,edge):
        q=s.copy(True)
        angle,px,py= (180,x+w,y+cross_y) if edge=='X' else (270,x+cross_x,y+d)
        q.rotate(V(0,0,0),V(0,0,1),angle);q.translate(V(px,py,z));return q
    for edge in ['X','Y']:
        reverse_key=prefix=='Breadboard' and edge_y==10 and edge=='X'
        # Captured T channel: 0.25/0.30 mm nominal clearances, open insertion end.
        rail=union([box(-4,-4.6,0,23,9.2,.65),box(-4,-4.6,.65,23,1.35,3.55),box(-4,3.25,.65,23,1.35,3.55),
                    box(-4,-4.6,2.85,23,2.7,1.35),box(-4,1.9,2.85,23,2.7,1.35)])
        allowed=[-3,0] if limit_front and edge=='Y' else [-3,0,3]
        for u in [9-delta for delta in allowed]:rail=rail.cut(box(u-1.15,-5,.9,2.3,10,1.65))
        # Arrow plaque outside board. Engraving added after mirror at export.
        rail=union([rail,box(-10,-6,0,7,12,2.2)])
        # +/- and a double-ended arrow are real recessed geometry. Symmetric
        # symbols remain readable after the assembly X mirror.
        grooves=[box(-8.9,-4,1.93,2.0,.45,.4),box(-8.125,-4.775,1.93,.45,2,.4),box(-5.6,-4,1.93,2,.45,.4),box(-9,-1.1,1.93,5.2,.45,.4)]
        for u,sgn in [(-9,1),(-3.8,-1)]:
            for dy in [-1,1]:
                a=V(u,-.875,2.16);b=V(u+sgn*1.3,-.875+dy*.9,2.16)
                line=Part.makeCylinder(.22,(b-a).Length,a,(b-a))
                grooves.append(line)
        if reverse_key:grooves=[q.mirror(V(0,0,0),V(0,1,0)) for q in grooves]
        rail=cut(rail,grooves)
        fixed.append(pose(rail,edge))
        jaw=union([box(-1,-2.95,.95,16,5.9,1.6),box(-1,-1.55,2.5,16,3.1,1.6),
                   box(-2.0,-5,.95,1.8,10,4.85+t),box(-2,-5,5.65+t,3.4,10,1.4)])
        jaw=jaw.cut(box(7.85,-3.3,.9,2.3,6.6,1.65))
        # Cross key with an accessible L handle. Small split tip provides a
        # release detent outside the rail; validate a coupon before use.
        key=union([box(8.1,-5.9,1.12,1.8,13.3,1.2),box(8.1,5,1.12,1.8,2.4,2.68),box(-7,5.0,2.6,16,2.4,1.2),box(-8,3.5,2.6,3.6,5.4,1.4),
                   box(7.7,-5.9,1.12,2.6,1.15,1.2)])
        key=key.cut(box(8.8,-6.1,.9,.4,6.0,2))
        if reverse_key:key=key.mirror(V(0,0,0),V(0,1,0))
        parts += [(prefix+'_'+edge+'_Jaw',pose(jaw,edge),'Indexed edge jaw; +/-3 mm from nominal, 3 mm increments. Lift top retention lip slightly for insertion; do not force PCB.'),
                  (prefix+'_'+edge+'_Lock_Key',pose(key,edge),'Pull sideways to release; slide jaw; fully insert cross key. Split-tip detent is a prototype. Positive cross engagement carries slide load.')]
        tracks.append({'axis':edge,'jaw':prefix+'_'+edge+'_Jaw','key':prefix+'_'+edge+'_Lock_Key','origin':[x+w,y+cross_y,z] if edge=='X' else [x+cross_x,y+d,z],
                       'direction':[-1,0,0] if edge=='X' else [0,-1,0],'range_mm':allowed,
                       'key_release_pre':[0,1 if reverse_key else -1,0] if edge=='X' else [1,0,0],
                       'key_release_mm':10.5,
                       'nominal_dimension_mm':w if edge=='X' else d,'slot_pitch_mm':3})
    # Height insert is a single thin U frame. Two underside locating tongues
    # fit pockets in the fixed supports; it cannot be stacked on another.
    right_peg_y=5.8 if prefix=='Breadboard' and edge_y==10 else 3.3
    right_peg_x=x+w*.5 if prefix=='LCD' else x+w-8
    if prefix=='LCD':fixed.append(box(right_peg_x-1,y+1,z,4.4,4.4,4.2))
    def insert(h):
        q=union([box(x+1.5,y+1.5,ledge_z,4,d-6,h),box(x+1.5,y+1.5,ledge_z,w-6,4,h),box(x+w-9,y+1.5,ledge_z,4,10,h)])
        q=union([q,box(x+2.5,y+3.3,ledge_z-.7,2,2,.8),box(right_peg_x,y+right_peg_y,ledge_z-.7,2,2,.8)])
        return q
    fi=union(fixed)
    for n,q,note in parts:
        axis='x' if '_X_' in n else 'y'
        allowed=[-3,0] if limit_front and axis=='y' and n.endswith('_Lock_Key') else [-3,0,3]
        for delta in allowed:
            q1=moved(q,**{axis:delta})
            fi=fi.cut(q1)
            for a in ['x','y','z']:
                for dd in [-.2,.2]:fi=fi.cut(moved(q1,**{a:dd}))
    for xx,yy in [(x+2.5,y+3.3),(right_peg_x,y+right_peg_y)]:fi=fi.cut(box(xx-.2,yy-.2,ledge_z-.9,2.4,2.4,1.1))
    for axis in tracks:fi=fi.cut(jaw_sweep(axis,t,box,union))
    for axis in tracks:fi=fi.cut(key_sweep(axis,box,union))
    parts.append((prefix+'_Height_Insert',insert(1.2),'One-piece keyed 1.2 mm nominal height insert. Alternative 0.6 / 1.8 mm inserts adjust supported thickness by +/-0.6 mm; use one only.'))
    info={'prefix':prefix,'origin':[x,y,z],'nominal_mm':[w,d,t],'board_bottom_z':board_z,'axes':tracks,'height_options_mm':[.6,1.2,1.8],
          'height_meaning':'Insert thickness changes support height. Thicker insert accepts a thinner body under the fixed top lips; no stacking.',
          'fixed_component_corner':[x,y],'local_frame_z':z}
    # Return alternatives in metadata as serialized BREP later, not assembly parts.
    info['_alternate_shapes']=[('minus',insert(.6)),('plus',insert(1.8))]
    return fi,parts,info

def engrave_adjustment(shape,name,mark,text_cut):
    if name.endswith(('_Jaw','_Lock_Key','_Height_Insert')):
        label='Soham Basanwar' if name.endswith('_Height_Insert') else 'SB'
        z=shape.BoundBox.ZMax
        faces=sorted([f for f in shape.Faces if f.BoundBox.ZLength<1e-6 and abs(f.BoundBox.ZMax-z)<1e-6],key=lambda f:f.Area,reverse=True)
        candidates=[]
        for f in faces:
            b=f.BoundBox;rot=b.YLength>b.XLength
            if name.endswith('_Height_Insert'):
                # A U-shaped top face has an empty centre. Use the actual
                # broad rear bar rather than its bounding-box centre.
                b=A.BoundBox(b.XMin,b.YMin,b.ZMin,b.XMax,b.YMin+4,b.ZMax);rot=False
            long=max(b.XLength,b.YLength);short=min(b.XLength,b.YLength)
            h=min(2.2,short-.7)
            if h<1.5:continue
            wires=Part.makeWireString(label,'C:/Windows/Fonts/','arialbd.ttf',h)
            q=Part.makeCompound([Part.makeFace(ws,'Part::FaceMakerBullseye') for ws in wires if ws])
            if q.BoundBox.XLength>long-.8:q.scale((long-.8)/q.BoundBox.XLength)
            if q.BoundBox.YLength<1.3:continue
            q.translate(V(-q.BoundBox.XMin,-q.BoundBox.YMin,0))
            if rot:q.rotate(V(0,0,0),V(0,0,1),90)
            qb=q.BoundBox;q.translate(V(b.Center.x-qb.Center.x,b.Center.y-qb.Center.y,z-.24))
            tool=q.extrude(V(0,0,.25));removed=shape.common(tool).Volume
            if removed<tool.Volume*.85:continue
            engraved=shape.cut(tool).removeSplitter()
            if engraved.isValid() and len(engraved.Solids)==1:shape=engraved;mark=label+' — noncontact upper face';break
    return shape,mark
