"""Revision 06: reference-led sculpted solids, not a physical-fit certification.
Run with FreeCAD's bundled bin/python.exe. Millimetres throughout.
The source and dimensions.json are the parametric master; FCStd contains editable solids.
"""
import json, math, os
from pathlib import Path
import FreeCAD as App
import Part, MeshPart
ROOT = Path(__file__).resolve().parent
P = json.loads((ROOT / 'dimensions.json').read_text())
V = App.Vector
OUT = ROOT / 'cad'
OUT.mkdir(exist_ok=True)
STL = ROOT / 'prototype-stl'
STL.mkdir(exist_ok=True)
RENDER = ROOT / 'render-meshes'
RENDER.mkdir(exist_ok=True)
all_records = []
checks = []

def box(x, y, z, w, d, h):
    return Part.makeBox(w, d, h, V(x, y, z))

def cyl(x, y, z, r, h):
    return Part.makeCylinder(r, h, V(x, y, z))

def face(points):
    return Part.Face(Part.makePolygon([V(x, y, 0) for x, y in points + [points[0]]]))

def union(shapes):
    if all((s.BoundBox.ZLength < 1e-07 for s in shapes)):
        solids = [s.extrude(V(0, 0, 1)) for s in shapes]
        s = solids[0].multiFuse(solids[1:]).removeSplitter() if len(solids) > 1 else solids[0]
        top = max([f for f in s.Faces if f.BoundBox.ZLength < 1e-07], key=lambda f: f.CenterOfMass.z)
        top.translate(V(0, 0, -1))
        return top
    a = shapes[0]
    if len(shapes) > 1:
        a = a.multiFuse(shapes[1:])
    return a.removeSplitter()

def cut(a, shapes):
    return a.cut(Part.makeCompound(shapes)).removeSplitter() if shapes else a

def moved(shape, x=0, y=0, z=0):
    a = shape.copy()
    a.translate(V(x, y, z))
    return a

def extr(f, z, h):
    return moved(f, z=z).extrude(V(0, 0, h))

def rr(x, y, w, d, r):
    es = []
    pts = [(x + r, y), (x + w - r, y), (x + w, y + r), (x + w, y + d - r), (x + w - r, y + d), (x + r, y + d), (x, y + d - r), (x, y + r)]
    mids = [(x + w - r + r / math.sqrt(2), y + r - r / math.sqrt(2)), (x + w - r + r / math.sqrt(2), y + d - r + r / math.sqrt(2)), (x + r - r / math.sqrt(2), y + d - r + r / math.sqrt(2)), (x + r - r / math.sqrt(2), y + r - r / math.sqrt(2))]
    for i in range(4):
        p1 = V(*pts[2 * i], 0)
        p2 = V(*pts[2 * i + 1], 0)
        p3 = V(*pts[(2 * i + 2) % 8], 0)
        es.extend([Part.makeLine(p1, p2), Part.Arc(p2, V(*mids[i], 0), p3).toShape()])
    return Part.Face(Part.Wire(es))

def capsule(x1, y1, x2, y2, r):
    dx = x2 - x1
    dy = y2 - y1
    L = math.hypot(dx, dy)
    nx = -dy / L * r
    ny = dx / L * r
    return union([Part.Face(Part.Wire([Part.makeCircle(r, V(x1, y1, 0))])), Part.Face(Part.Wire([Part.makeCircle(r, V(x2, y2, 0))])), face([(x1 + nx, y1 + ny), (x2 + nx, y2 + ny), (x2 - nx, y2 - ny), (x1 - nx, y1 - ny)])])

def offset(f, d):
    if f.ShapeType not in ['Face', 'Wire', 'Edge']:
        f = Part.Face(f.Wires)
    a = f.makeOffset2D(d, join=0).removeSplitter()
    return a.Faces[0] if len(a.Faces) == 1 else a

def loft(f, levels):
    return Part.makeLoft([moved(offset(f, inset) if inset else f, z=z).OuterWire for z, inset in levels], True, True)

def stroke(points, r=0.65, z=0, h=0.8):
    return union([extr(capsule(*a, *b, r), z, h) for a, b in zip(points, points[1:])])

def ring(x, y, z, ro, ri, h):
    return cyl(x, y, z, ro, h).cut(cyl(x, y, z - 0.1, ri, h + 0.2))

def rounded_edge(s, z, radius):
    edges = [e for e in s.Edges if e.BoundBox.ZLength < 1e-06 and abs(e.BoundBox.ZMin - z) < 1e-06]
    for r in [radius, 1.5, 0.8]:
        try:
            candidate = s.makeFillet(r, edges)
            if candidate.isValid():
                return candidate
        except Exception:
            pass
    raise RuntimeError('Could not round shell edge')

def sculpted_outline():
    right = [[(123, 0), (173, 0), (216, 5)], [(216, 5), (239, 20), (246, 48)], [(246, 48), (242, 90), (237, 128)], [(237, 128), (236, 169), (221, 199)], [(221, 199), (199, 205), (181, 188)], [(181, 188), (175, 157), (161, 144)], [(161, 144), (143, 139), (123, 138)]]
    segments = right + [[(246 - x, y) for x, y in seg[::-1]] for seg in right[::-1]]
    edges = []
    for segment in segments:
        edges.append(Part.Arc(*[V(x, y, 0) for x, y in segment]).toShape())
    return Part.Face(Part.Wire(edges))

def ceiling(W, H, main=False):
    x = -30
    end = 240
    if main:
        return box(x, -30, -50, W + 60, 300, H + 50)
    curve = Part.BezierCurve()
    curve.setPoles([V(x, 130, H), V(x, 160, H), V(x, 198, H - 14), V(x, end, H - 37)])
    e = [Part.makeLine(V(x, -30, -50), V(x, end, -50)), Part.makeLine(V(x, end, -50), V(x, end, H - 37)), curve.toShape(), Part.makeLine(V(x, 130, H), V(x, -30, H)), Part.makeLine(V(x, -30, H), V(x, -30, -50))]
    return Part.Face(Part.Wire(Part.__sortEdges__(e))).extrude(V(W + 60, 0, 0))

def soft_loft(f, levels):
    wires = [moved(offset(f, inset), z=z).OuterWire for z, inset in levels]
    return Part.makeLoft(wires, True, False)

def grip_limit(inset=0):
    sections = [(106, 43, 27, 62, 48), (125, 43, 27, 43, 36), (145, 42, 27, 35, 30), (170, 40, 26, 32, 28), (190, 38, 24, 29, 26), (211, 34, 22, 23, 23)]
    grips = []
    for side in [0, 1]:
        wires = []
        for y, x, z, rx, rz in sections:
            cx = x if side == 0 else 246 - x
            e = Part.Ellipse(V(0, 0, 0), max(rx - inset, rz - inset), min(rx - inset, rz - inset)).toShape()
            wire = Part.Wire([e])
            wire.rotate(V(0, 0, 0), V(1, 0, 0), 90)
            wire.translate(V(cx, y, z))
            wires.append(wire)
        grips.append(Part.makeLoft(wires, True, False))
    return union([box(-40, -40, -50, 326, 147, 180)] + grips)

def oriented(s, angle, x, y):
    q = s.copy()
    q.rotate(V(0, 0, 0), V(0, 0, 1), angle)
    q.translate(V(x, y, 0))
    return q

def build(role):
    main = role == 'main'
    W = 234 if main else 246
    D = 180 if main else 207
    H = 64 if main else 58
    split = H - 16
    doc = App.newDocument('DRM_' + role + '_R06')
    meta = doc.addObject('App::FeaturePython', 'DesignParameters')
    meta.addProperty('App::PropertyString', 'Status')
    meta.Status = 'PROTOTYPE — component measurements and powered tests required'
    meta.addProperty('App::PropertyString', 'Regeneration')
    meta.Regeneration = 'Edit dimensions.json and run build_revision06.py with FreeCAD Python'
    for name, value in [('NominalWidth', W), ('NominalDepth', D), ('ShellHeight', H)]:
        meta.addProperty('App::PropertyLength', name)
        setattr(meta, name, value)
    shell_group = doc.addObject('App::DocumentObjectGroup', 'PrintedParts')
    env_group = doc.addObject('App::DocumentObjectGroup', 'ComponentEnvelopes')
    records = []
    bodies = {}
    envs = {}

    def add(name, shape, material='bronze', component=False, explosion=(0, 0, 0), notes=''):
        shape = shape.removeSplitter()
        if not shape.isValid() or not shape.Solids:
            raise RuntimeError(f'{role}/{name}: invalid solid')
        if not component and len(shape.Solids) != 1:
            print([(round(s.Volume, 2), str(s.BoundBox)) for s in shape.Solids], flush=True)
            raise RuntimeError(f'{role}/{name}: disconnected printed part')
        exported = shape.mirror(V(W / 2, 0, 0), V(1, 0, 0))
        ob = doc.addObject('PartDesign::Feature', name)
        ob.Label = name.replace('_', ' ')
        ob.Shape = exported
        ob.addProperty('App::PropertyString', 'ManufacturingStatus')
        ob.ManufacturingStatus = 'REFERENCE ENVELOPE' if component else 'Prototype; fit unverified'
        ob.addProperty('App::PropertyString', 'DesignNotes')
        ob.DesignNotes = notes
        (env_group if component else shell_group).addObject(ob)
        mesh = MeshPart.meshFromShape(Shape=exported, LinearDeflection=0.13, AngularDeflection=0.22, Relative=False)
        filename = f'{role}-{name}.stl'
        mesh.write(str(RENDER / filename))
        if not component:
            mesh.write(str(STL / filename))
            bodies[name] = shape
        else:
            envs[name] = shape
        rec = {'role': role, 'name': name, 'file': filename, 'material': material, 'component': component, 'explosion': explosion, 'volume_mm3': shape.Volume, 'solids': len(shape.Solids), 'notes': notes}
        records.append(rec)
        checks.append({'role': role, 'part': name, 'valid_brep': shape.isValid(), 'solids': len(shape.Solids), 'volume_mm3': round(shape.Volume, 2), 'component': component})
        return shape
    if main:
        raw = face([(40, 16), (194, 16), (218, 40), (218, 140), (194, 164), (40, 164), (16, 140), (16, 40)])
        outer = offset(raw, 16)
    else:
        outer = sculpted_outline()
    outer = Part.Face(outer.Wires)
    inner = offset(outer, -3.4)
    print(role, 'sculpting shell', flush=True)
    levels = [(0, -6), (3, -4.5), (8, -2.5), (15, -1), (24, -0.2), (33, -1.2), (split, -3), (H - 10, -4.8), (H - 5, -7.5), (H, -11)]
    body = soft_loft(outer, levels)
    print(role, 'outer loft ready', flush=True)
    body = body.common(ceiling(W, H, main))
    if not main:
        body = body.common(grip_limit())
        land = extr(rr(23.5, 122.5, 37, 68, 4), 0, 6)
        body = union([body, land])
    cavity = soft_loft(outer, [(4, -7.8), (8, -6), (15, -4.4), (24, -3.6), (33, -4.6), (split, -6.4), (H - 10, -8.2), (H - 4, -11.5), (H + 1, -14)])
    print(role, 'inner loft ready', flush=True)
    cavity = cavity.common(ceiling(W, H - 3.8, main))
    if not main:
        cavity = cavity.common(grip_limit(3.4))
    hollow = body.cut(cavity)
    print(role, 'hollow shell ready', flush=True)
    base = hollow.common(ceiling(W, split, main))
    print('TRACE base line 172', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
    lid = hollow.cut(ceiling(W, split + 0.28, main))
    print('TRACE lid line 173', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
    skirt = extr(offset(outer, -5.2).cut(offset(outer, -7.1)), 10, H).cut(ceiling(W, split - 4, main)).common(ceiling(W, split + 1, main))
    skirt_bridge = extr(offset(outer, -3.4).cut(offset(outer, -7.1)), 10, H).cut(ceiling(W, split + 0.28, main)).common(ceiling(W, split + 2.4, main))
    bb = P['breadboard']
    uno = [69.2, 54, 20] if main else P['uno_r3']
    bx, by = (34, 12) if main else (40, 68)
    ux, uy = (88, 91) if main else (89, 10)
    batx, baty = (23, 98) if main else (27, 126)
    batt = P['battery_reservation']
    bay = rr(batx - 0.6, baty - 0.6, batt[0] + 1.2, batt[1] + 1.2, 2)
    base = base.cut(extr(bay, -1, 6.5))
    print('TRACE base line 183', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
    baywall = extr(offset(bay, 2.0).cut(bay), 3.5, 24)
    baywall = cut(baywall, [box(batx + 9, baty - 4, 17, 12, 6, 7)])
    rails = [box(batx - 2, baty + 10, 4.8, 4.8, 45, 2.2), box(batx + 27.5, baty + 10, 4.8, 4.5, 45, 2.2)]
    base = union([base, baywall] + rails)
    print('TRACE base line 189', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
    door_profile = rr(batx - 2.2, baty - 2.2, batt[0] + 4.4, batt[1] + 4.4, 3)
    base = base.cut(extr(offset(door_profile, 0.3), -0.2, 2.7))
    print('TRACE base line 192', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
    base = cut(base, [box(batx + 3, baty - 5, 2.2, 7, 4.4, 1.6), box(batx + 20, baty - 5, 2.2, 7, 4.4, 1.6), box(batx + 10, baty + batt[1] - 1, 2.4, 10, 4.6, 2.3)])
    print('TRACE base line 193', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
    door = extr(door_profile, 0.3, 2.1)
    door = cut(door, [box(batx + 9.2, baty + 45, 0, 0.8, 19, 4), box(batx + 20, baty + 45, 0, 0.8, 19, 4)])
    tabs = [box(batx + 3.4, baty - 4.4, 2.2, 6.2, 3.5, 1.0), box(batx + 20.4, baty - 4.4, 2.2, 6.2, 3.5, 1.0)]
    hook = box(batx + 10.1, baty + batt[1] - 0.5, 2.0, 9.7, 2.2, 1.7)
    door = union([door, hook] + tabs)
    door = door.cut(extr(rr(batx + 11, baty + 49, 8, 8, 2), -0.1, 1.0))
    add('Battery_Door', door, 'bronze', explosion=(0, 0, -28), notes='Two leading tabs plus recessed cantilever latch. Trial fit coupon before use.')
    stop = box(batx - 1.8, baty + 22, 26, 33.6, 5, 2)
    base = union([base, stop])
    print('TRACE base line 204', round(base.Volume), len(base.Solids), base.isValid(), flush=True)

    def tray(x, y, w, d, z=5, height=4):
        return extr(rr(x - 2, y - 2, w + 4, d + 4, 2).cut(rr(x - 0.3, y - 0.3, w + 0.6, d + 0.6, 1)), 3.8, height + z - 3.8)
    base = union([base, tray(bx, by, bb[0], bb[1])])
    print('TRACE base line 209', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
    for xx in [bx + 15, bx + bb[0] - 23]:
        for yy, s in [(by - 2.8, 1), (by + bb[1] + 1.4, -1)]:
            leaf = box(xx, yy, 3.8, 8, 1.4, 13)
            lip = box(xx, yy + (1.2 if s == 1 else -1.4), 15.1, 8, 1.6, 1.7)
            base = union([base, leaf, lip])
            print('TRACE base line 214', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
    base = union([base, tray(ux, uy, uno[0], uno[1], z=7, height=2)])
    print('TRACE base line 217', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
    for xx in [ux + 5, ux + uno[0] - 9]:
        for yy in [uy + 1, uy + uno[1] - 5]:
            base = union([base, box(xx, yy, 3.8, 4, 4, 3.2)])
            print('TRACE base line 219', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
    for side in [0, 1]:
        xx = ux - 4 if side == 0 else ux + uno[0] + 2
        yy = uy + 22
        foot = box(xx - 0.8, yy - 1, 4.1, 3.6, 10, 1.7)
        clip = union([foot, box(xx, yy, 5.5, 2, 8, 4.8), box(xx + (1.7 if side == 0 else -3.1), yy, 8.9, 3.4, 8, 1.4)])
        socket = box(xx - 1.2, yy - 1.4, 3.6, 4.4, 10.8, 2.5).cut(box(xx - 1, yy - 1.2, 3.9, 4, 10.4, 2.1))
        base = union([base, socket, box(xx - 1.2, yy - 1.4, 3.6, 4.4, 10.8, 0.4)])
        print('TRACE base line 228', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
        base = base.cut(clip)
        print('TRACE base line 229', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
        add('UNO_Edge_Clip_' + str(side + 1), clip, 'bronze', explosion=(0, 0, 20), notes='Replaceable push-in edge retainer. Parametric clearance; no assumed PCB hole pattern. Fit coupon required.')
    ports = [('I2C_Left', -90, 0, 125), ('I2C_Right', 90, W, 95)] if main else [('I2C_Rear', 0, 123, 0)]
    for name, angle, xx, yy in ports:
        z = 24
        trans = lambda a: oriented(a, angle, xx, yy)
        opening = box(-9, -12, z - 6, 18, 30, 12)
        channel = box(-10.4, -2.55, z - 7.1, 42.4, 3.1, 14.2)
        base = cut(base, [trans(opening), trans(channel)])
        print('TRACE base line 240', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
        frame = union([box(-12, -4, z - 10, 47, 12, 2.9), box(-12, -4, z + 7.1, 47, 12, 2.9), box(32, -4, z - 10, 3, 12, 20), box(-12, -4, z - 10, 47, 1.4, 5), box(-12, -4, z + 5, 47, 1.4, 5), box(-12, 0.6, z - 10, 47, 7.4, 5), box(-12, 0.6, z + 5, 47, 7.4, 5)])
        base = union([base, trans(frame)])
        print('TRACE base line 246', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
        slide = union([box(-10, -2.2, z - 6.7, 20, 2.2, 13.4), box(-4, -5.2, z - 3, 8, 3.1, 6)])
        keeper = union([box(-12, -3.6, z - 6.5, 1.6, 5.4, split - z + 4.3), box(-12, -3.6, split - 2.2, 3.6, 11.6, 1.2)])
        base = cut(base, [trans(box(-12.2, -3.8, z - 6.7, 2, 5.8, split - z + 4.7)), trans(box(-12.2, -3.8, split - 2.4, 4, 12, 1.6))])
        print('TRACE base line 250', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
        add(name + '_Shutter', trans(slide), 'bronze', explosion=(0, -22, 0), notes='18 x 12 mm aperture; slide 21 mm to open. Close only after cable removal. Not a strain clamp.')
        add(name + '_Keeper', trans(keeper), 'bronze', explosion=(0, 0, 18), notes='Top-inserted stop; lid prevents full withdrawal. Service by removing lid.')
        cleat = box(-9, 9, 15, 18, 6, 8).cut(box(-5, 8, 18, 10, 8, 6))
        cleat = cleat.cut(box(-10, 10.5, 16, 20, 2.5, 1.4))
        cleat = union([cleat, box(-9, 5, 15, 4, 6, 5), box(5, 5, 15, 4, 6, 5)])
        base = union([base, trans(cleat)])
        print('TRACE base line 260', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
    latchys = [82] if not main else [77]
    for side in [0, 1]:
        xx = 10.5 if side == 0 else W - 11.9
        for yy in latchys:
            lid = lid.cut(box(xx - 0.6, yy - 1, split - 4.1, 2.7, 14, 16.1))
            print('TRACE lid line 266', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
            leaf = box(xx, yy, H - 29, 1.4, 12, 25)
            anchor = box(xx if side == 0 else xx - 5, yy, H - 6, 6.4, 12, 2.5)
            hook = box(xx - 1 if side == 0 else xx + 1.2, yy, H - 28, 1.2, 12, 2.1)
            lid = union([lid, leaf, anchor, hook])
            print('TRACE lid line 270', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
            base = base.cut(box(-1 if side == 0 else W - 17, yy - 0.4, H - 28.3, 18, 12.8, 2.8))
            print('TRACE base line 271', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
    for xx in [63, W - 69]:
        tab = box(xx, 2.4, split - 3.8, 6, 5.5, 2.2)
        bridge = box(xx, 4.5, split - 3.8, 6, 2.2, 6)
        lid = union([lid, tab, bridge])
        print('TRACE lid line 276', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
        base = base.cut(box(xx - 0.35, 1.9, split - 4.15, 6.7, 5.9, 2.9))
        print('TRACE base line 277', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
    emblem = (117, 108) if main else (123, 67)
    ex, ey = emblem
    lid = lid.cut(cyl(ex, ey, H - 16, 24.3, 20))
    print('TRACE lid line 281', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
    cup = ring(ex, ey, H - 17, 26, 24, 17)
    cup = union([cup, cyl(ex, ey, H - 18, 26, 2.4)])
    cup = cut(cup, [cyl(ex, ey, H - 19, 2.65, 5), box(ex - 4, ey - 27, H - 15, 8, 5, 3)])
    boss = ring(ex, ey, H - 23, 7.2, 3.3, 5.4)
    boss = boss.cut(ring(ex, ey, H - 22.1, 6.2, 3.0, 1.6))
    for dy in [-7.3, 3.0]:
        boss = boss.cut(box(ex - 1, ey + dy, H - 23.2, 2, 4.3, 2.8))
    cup = union([cup, boss])
    lid = union([lid, cup])
    print('TRACE lid line 291', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
    led = union([cyl(ex, ey, H - 18.5, 2.5, 6), cyl(ex, ey, H - 19.4, 3, 1)])
    led = union([led] + [cyl(ex + dx, ey, H - 25.4, 0.25, 6.1) for dx in [-1.5, -0.5, 0.5, 1.5]])
    add('RGB_LED_Envelope', led, 'diffuser', True, notes='Nominal 5 mm four-lead RGB package behind emblem. Body, flange, lead order and resistors require actual-part verification.')
    ledkeeper = ring(ex, ey, H - 22.7, 3.05, 2.25, 3)
    ledkeeper = union([ledkeeper, box(ex + 2.8, ey - 0.6, H - 21.8, 3, 1.2, 1), box(ex - 5.8, ey - 0.6, H - 21.8, 3, 1.2, 1)])
    add('RGB_LED_Keeper', ledkeeper, 'bronze', explosion=(0, 0, -18), notes='Insert the two tabs through the Y keyways, then rotate 90 degrees. Captures the LED flange; leads pass through centre. Verify physical fit.')
    lens = cyl(ex, ey, H + 0.05, 24, 1.2)
    lens = cut(lens, [box(ex + dx - 0.2, ey - 3.2, H, 1.7, 6.4, 2) for dx in [-25, 23.7]])
    add('Emblem_Diffuser', lens, 'diffuser', explosion=(0, 0, 52), notes='Separate translucent sheet/print; opaque bronze cannot transmit light.')
    mask = cyl(ex, ey, H + 1.3, 26, 1.8)
    mask_slots = []
    if role == 'explorer':
        mask_slots += [stroke([(ex - 15, ey), (ex - 7, ey - 7), (ex, ey - 9), (ex + 7, ey - 7), (ex + 15, ey)], 0.9, H + 1, 3), stroke([(ex - 13, ey + 2), (ex - 6, ey + 7), (ex + 6, ey + 7), (ex + 13, ey + 2)], 0.9, H + 1, 3)]
        mask_slots += [stroke([(ex, ey - 19), (ex, ey - 13)], 1, H + 1, 3), stroke([(ex, ey + 12), (ex, ey + 19)], 1, H + 1, 3), stroke([(ex - 21, ey), (ex - 18, ey)], 1, H + 1, 3), stroke([(ex + 18, ey), (ex + 21, ey)], 1, H + 1, 3)]
        for a, b in [(-65, 65), (115, 245)]:
            pts = [(ex + 4.5 * math.cos(math.radians(t)), ey + 4.5 * math.sin(math.radians(t))) for t in range(a, b + 1, 10)]
            mask_slots.append(stroke(pts, 0.8, H + 1, 3))
    elif role == 'architect':
        mask_slots += [stroke([(ex - 12, ey + 14), (ex - 12, ey - 5), (ex - 7, ey - 12), (ex + 7, ey - 12), (ex + 12, ey - 5), (ex + 12, ey + 14)], 1, H + 1, 3)]
        for dx in [-5, 0, 5]:
            mask_slots.append(stroke([(ex + dx, ey - 5), (ex + dx, ey + 12)], 0.8, H + 1, 3))
        mask_slots.append(stroke([(ex - 6, ey - 16), (ex, ey - 21), (ex + 6, ey - 16)], 0.8, H + 1, 3))
    else:
        for rad, a, b in [(18, 20, 320), (11, -20, 260)]:
            pts = [(ex + rad * math.cos(math.radians(t)), ey + rad * math.sin(math.radians(t))) for t in range(a, b + 1, 10)]
            mask_slots.append(stroke(pts, 0.9, H + 1, 3))
        mask_slots.append(stroke([(ex, ey - 6), (ex + 4, ey), (ex, ey + 6), (ex - 4, ey)], 0.8, H + 1, 3))
    mask = cut(mask, mask_slots)
    for dx in [-25, 23.7]:
        mask = union([mask, box(ex + dx, ey - 3, H - 2, 1.3, 6, 4)])
    lid = cut(lid, [box(ex + dx - 0.2, ey - 3.2, H - 2.3, 1.7, 6.4, 5) for dx in [-25, 23.7]])
    print('TRACE lid line 324', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
    add('Emblem_Mask', mask, 'bronze', explosion=(0, 0, 57))
    border = extr(offset(outer, -13).cut(offset(outer, -14.3)), 10, H).cut(ceiling(W, H - 0.4, main)).common(ceiling(W, H + 0.8, main))
    if not main:
        border = border.common(box(-20, -20, -5, 286, 149, 100))
    lid = union([lid, border])
    print('TRACE lid line 329', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
    if not main:
        cx, cy = (49, 42)
        if role == 'explorer':
            lid = lid.cut(cyl(cx, cy, H - 12, 14.2, 20))
            print('TRACE lid line 334', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
            jx, jy = (cx - 17, cy - 13)
            carrier = extr(rr(jx - 2, jy - 2, 38, 30, 3).cut(rr(jx - 0.35, jy - 0.35, 34.7, 26.7, 0.3)), H - 24, 15)
            for xx in [jx - 2, jx + 34]:
                carrier = union([carrier, box(xx, jy, H - 24, 2, 26, 21)])
                out = -1 if xx < cx else 1
                ear = box(xx - 1.2 if out < 0 else xx + 1.8, jy + 7, H - 5.6, 1.4, 12, 1.2)
                carrier = union([carrier, ear])
                receiver = box(xx - 2, jy + 4, H - 10, 6, 18, 6.8)
                receiver = receiver.cut(box(xx - 0.3, jy + 3.7, H - 10.2, 2.6, 18.6, 7.2))
                receiver = receiver.cut(box(xx - 1.5 if out < 0 else xx + 1.5, jy + 6.7, H - 5.9, 2, 12.6, 1.8))
                lid = union([lid, receiver])
                print('TRACE lid line 347', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
            for xx in [jx - 2, jx + 33]:
                carrier = union([carrier, box(xx, jy + 4, H - 25, 3, 18, 1.3)])
                carrier = union([carrier, box(xx, jy + 7, H - 21.7, 3, 4, 1.2)])
            add('Joystick_Carrier', carrier, 'bronze', explosion=(0, 0, -22), notes='Replaceable snap-in edge carrier. Width/depth/clip parameters provisional; exact mounting-hole pins deferred.')
            lid = lid.cut(cyl(197, 42, H - 8, 3.2, 15))
            print('TRACE lid line 353', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
            sensor = ring(197, 42, H - 9, 5.2, 3.2, 9)
            lid = union([lid, sensor])
            print('TRACE lid line 355', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
            add('Joystick_PCB', box(jx, jy, H - 23.5, 34, 26, 1.6), 'pcb', True)
            add('Joystick_Mechanism', union([box(cx - 9, cy - 9, H - 22, 18, 18, 15), cyl(cx, cy, H - 7, 6, 12), cyl(cx, cy, H + 3, 12, 5)]), 'black', True)
            add('Bare_Light_Sensor', cyl(197, 42, H - 2, 2.7, 2), 'sensor', True)
        else:
            lid = lid.cut(cyl(cx, cy, H - 18, 4, 25))
            print('TRACE lid line 360', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
            potcup = ring(cx, cy, H - 17, 10.3, 8.3, 17)
            potcup = cut(potcup, [box(cx - 12, cy - 4, H - 17, 24, 8, 8)])
            potcup = potcup.cut(ring(cx, cy, H - 16.6, 9.7, 8.0, 1.6))
            for dx in [-10.4, 7.9]:
                potcup = potcup.cut(box(cx + dx, cy - 1.2, H - 17.3, 2.5, 2.4, 2.5))
            lid = union([lid, potcup])
            print('TRACE lid line 365', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
            potkeeper = ring(cx, cy, H - 16.8, 8.05, 5.5, 1.5)
            potkeeper = union([potkeeper, box(cx - 0.9, cy - 9.4, H - 16.4, 1.8, 1.5, 1), box(cx - 0.9, cy + 7.9, H - 16.4, 1.8, 1.5, 1)])
            add('Potentiometer_Keeper', potkeeper, 'bronze', explosion=(0, 0, -20), notes='Quarter-turn lower retainer. Terminal geometry and body antirotation lug remain unmeasured; tune this replaceable part.')
            add('Potentiometer_Envelope', union([cyl(cx, cy, H - 15, 8, 10), cyl(cx, cy, H - 5, 3, 18)]), 'metal', True, notes='16 mm body / 6 mm shaft placeholder. Product image does not establish actual dimensions.')
            add('Bronze_Knob_Envelope', cyl(cx, cy, H + 1, 11, 14), 'knob', True)
            gx, gy = (196, 32)
            lid = lid.cut(box(gx - 17, gy - 10, H - 15, 34, 20, 20))
            print('TRACE lid line 373', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
            collar = extr(rr(gx - 23, gy - 15, 46, 30, 5).cut(rr(gx - 17.3, gy - 10.3, 34.6, 20.6, 3)), H - 1, 4)
            lid = union([lid, collar])
            print('TRACE lid line 375', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
            sy = gy - 16
            axle_x = gx - 5
            axle_z = H + 18
            servo = box(gx - 11.5, sy, H + 6, 23, 29, 12.2)
            add('SG90_Body_Envelope', servo, 'servo', True, notes='Sideways placement. Shaft offset, ears and exact horn geometry require measurement.')
            cassette = extr(rr(gx - 15, sy - 2, 30, 34, 3).cut(rr(gx - 12, sy - 0.4, 24, 29.8, 1)), H + 3, 19)
            cassette = union([cassette, box(gx - 15, sy - 2, H + 3, 30, 34, 2.5)])
            cassette = cut(cassette, [box(gx - 4, sy - 3, H + 9, 8, 6, 6)])
            cassette = cassette.cut(Part.makeCylinder(10.2, 7, V(axle_x, sy + 27, axle_z), V(0, 1, 0)))
            cassette = union([cassette, box(gx - 16, gy - 9, H - 2, 32, 18, 6)])
            for xx in [gx - 14, gx + 11]:
                cassette = cassette.cut(box(xx, sy + 8, H + 5, 3, 6, 5))
            for xx in [gx - 12, gx + 10.3]:
                cassette = union([cassette, box(xx, sy + 5, H + 18.5, 1.7, 9, 1.5)])
            for xx, direction in [(gx - 16, -1), (gx + 14.4, 1)]:
                leg = box(xx, gy - 5, H - 6, 1.6, 10, 9)
                hook = box(xx - 2.4 if direction < 0 else xx + 1.4, gy - 5, H - 5.3, 2.6, 10, 1.2)
                cassette = union([cassette, leg, hook])
            add('Servo_Cassette', cassette, 'bronze', explosion=(0, 0, 38))
            fy = gy + 19
            arch = Part.makeCylinder(22, 8, V(gx, fy - 3, H + 35), V(0, 1, 0)).cut(Part.makeCylinder(16, 10, V(gx, fy - 4, H + 35), V(0, 1, 0)))
            arch = arch.common(box(gx - 23, fy - 4, H + 35, 46, 10, 24))
            frame = union([box(gx - 22, fy - 3, H + 3, 6, 8, 33), box(gx + 16, fy - 3, H + 3, 6, 8, 33), arch])
            frame = cut(frame, [box(gx - 18, fy - 0.4, H + 6, 2.4, 3.1, 45), box(gx + 15.6, fy - 0.4, H + 6, 2.4, 3.1, 45)])
            foot = box(gx - 23, sy - 3, H + 3.3, 46, fy - sy + 8, 3)
            frame = union([frame, foot])
            frame = frame.cut(box(gx - 16.4, gy - 9.4, H, 32.8, 18.8, 5))
            frame = frame.cut(box(gx - 15.4, sy - 2.4, H + 2.7, 30.8, 34.8, 4))
            for xx in [gx - 20, gx + 17]:
                frame = frame.cut(box(xx, gy - 10, H, 3, 6, 5))
            frame = frame.cut(box(gx - 17.4, fy - 0.4, H + 10, 34.8, 3, 42))
            hubstop = Part.makeCylinder(4.3, 1.4, V(axle_x, fy - 2.6, axle_z), V(0, 1, 0)).cut(Part.makeCylinder(2.4, 2, V(axle_x, fy - 2.9, axle_z), V(0, 1, 0)))
            hubstop = union([hubstop, box(axle_x - 0.9, fy - 2.6, axle_z + 3, 1.8, 1.4, 12), box(gx - 20, fy - 2.6, axle_z + 13, axle_x - gx + 21, 1.4, 2)])
            frame = union([frame, hubstop])
            for xx, direction in [(gx - 21, -1), (gx + 19, 1)]:
                leg = box(xx, gy - 12, H - 6, 2, 6, 11)
                hook = box(xx - 2 if direction < 0 else xx + 1.8, gy - 12, H - 5.3, 2.2, 6, 1.2)
                frame = union([frame, leg, hook])
                lid = lid.cut(box(xx - 0.3, gy - 12.3, H - 4, 2.6, 6.6, 10))
                print('TRACE lid line 421', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
            add('Gate_Frame', frame, 'bronze', explosion=(0, 0, 65))
            closed_z = axle_z - 7 * math.sin(math.pi / 3)
            panel = union([box(gx - 17, fy, closed_z - 3, 34, 2.2, 6), box(gx - 17, fy, closed_z + 23, 34, 2.2, 3)] + [box(gx + t, fy, closed_z, 2, 2.2, 26) for t in [-17, -9, -1, 7, 15]])
            panel = panel.cut(box(axle_x + 1.5, fy - 0.2, closed_z - 1.5, 8, 3, 3))
            add('Gate_Panel', panel, 'bronze', explosion=(0, 0, 80), notes='Scotch-yoke concept: 7 mm crank, +/-60 degrees, nominal lift 12.12 mm. Load and horn fit unverified.')
            hornface = capsule(axle_x, axle_z, axle_x + 3.5, closed_z, 2.2)
            hornface = union([hornface, Part.Face(Part.Wire([Part.makeCircle(4, V(axle_x, axle_z, 0))]))])
            crank = extr(hornface, 0, 2)
            crank.rotate(V(0, 0, 0), V(1, 0, 0), 90)
            crank.translate(V(0, fy - 3, 0))
            crank = crank.cut(Part.makeCylinder(1.3, 3, V(axle_x + 3.5, fy - 5.5, closed_z), V(0, 1, 0)))
            add('Original_Horn_Envelope', crank, 'white', True, notes='Nominal supplied nylon horn with a 7 mm radius hole. Verify actual hole radius and hub dimensions; do not print an assumed spline.')
            pin = union([Part.makeCylinder(1.2, 8.3, V(axle_x + 3.5, fy - 6, closed_z), V(0, 1, 0)), Part.makeCylinder(2.1, 1.2, V(axle_x + 3.5, fy + 2.2, closed_z), V(0, 1, 0))])
            pin = pin.cut(Part.makeCylinder(1.3, 1, V(axle_x + 3.5, fy - 5.9, closed_z), V(0, 1, 0)).cut(Part.makeCylinder(0.85, 1.2, V(axle_x + 3.5, fy - 6, closed_z), V(0, 1, 0))))
            add('Gate_Drive_Pin', pin, 'bronze', explosion=(0, 18, 65), notes='Nominal headed pin with rear keeper groove. Tiny FDM fit unverified; a matching nylon push-rivet is an alternative without screws.')
            pinclip = Part.makeCylinder(2.4, 0.7, V(axle_x + 3.5, fy - 5.75, closed_z), V(0, 1, 0)).cut(Part.makeCylinder(0.95, 1, V(axle_x + 3.5, fy - 5.9, closed_z), V(0, 1, 0)))
            pinclip = pinclip.cut(box(axle_x + 3.5 - 0.7, fy - 5.9, closed_z, 1.4, 1.2, 3))
            add('Gate_Pin_Keeper', pinclip, 'bronze', explosion=(0, -18, 65), notes='C-shaped keeper fits the pin groove behind the horn. Small feature requires a real fit test; not a proven production fastening.')
            shroud = extr(rr(gx - 25, sy - 5, 50, fy - sy + 13, 4).cut(rr(gx - 22.5, sy - 2.5, 45, fy - sy + 8, 0.5)), H + 6.6, 54.4)
            frontslots = [box(gx - 19 + i * 6, fy + 5, H + 26, 3, 6, 29) for i in range(7)]
            backslots = [box(gx - 19 + i * 6, sy - 6, H + 27, 3, 6, 28) for i in range(7)]
            sideslots = [box(gx + xx, sy + 3 + i * 6, H + 27, 6, 3, 28) for xx in [-26, 20] for i in range(5)]
            shroud = cut(shroud, frontslots + backslots + sideslots + [box(gx - 8, sy - 7, H + 5, 16, 7, 10)])
            shroud = union([shroud, box(gx - 23, fy - 3, H + 59, 46, 9, 2)])
            archcap = union([box(gx - 26, sy - 6, H + 6, 52, fy - sy + 15, 29), Part.makeCylinder(25, fy - sy + 15, V(gx, sy - 6, H + 35), V(0, 1, 0))])
            shroud = shroud.common(archcap)
            add('Gate_Shroud', shroud, 'bronze', explosion=(0, 0, 92), notes='Removable guard and axial keeper concept; check pinch access, slot widths and full servo sweep physically.')
    if role != 'explorer':
        px, py = (117, 145) if main else (197, 95)
        lid = lid.cut(cyl(px, py, H - 17, 8.4, 25))
        print('TRACE lid line 455', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
        guide = ring(px, py, H - 13, 11.2, 8.4, 14)
        guide = guide.cut(cyl(px, py, H - 13.1, 10.35, 10.5))
        lid = union([lid, guide]).cut(cyl(px, py, H - 13.1, 10.35, 10.5))
        print('TRACE lid line 458', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
        lid = lid.cut(extr(rr(px - 9.3, py - 9.3, 18.6, 18.6, 2), H - 13.1, 2.6))
        print('TRACE lid line 459', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
        cap = union([cyl(px, py, H - 4.3, 10, 1.5), cyl(px, py, H - 3, 7.9, 7), cyl(px, py, H - 9.3, 2.5, 5.3)])
        if main:
            cap = cap.cut(stroke([(px, py - 4), (px, py + 0.2)], 0.55, H + 3.35, 1))
        else:
            cap = cap.cut(stroke([(px - 3, py), (px - 0.5, py + 2.5), (px + 4, py - 3)], 0.65, H + 3.35, 1))
        add('Button_Cap', cap, 'bronze', explosion=(0, 0, 35), notes='Guided actuator, retaining flange and adjustable pusher. 0.3 mm radial clearance; tune switch travel.')
        cradle = extr(rr(px - 9, py - 9, 18, 18, 2).cut(rr(px - 6.35, py - 6.35, 12.7, 12.7, 1)), H - 17, 6.2)
        cradle = union([cradle, box(px - 9, py - 9, H - 17, 18, 18, 1.4)])
        cradle = cut(cradle, [box(px - 10, py - 4, H - 16, 20, 8, 2.2)])
        cradle = union([cradle, ring(px, py, H - 6, 10.1, 4, 1.25), box(px - 8.5, py - 2, H - 15, 2, 4, 10), box(px + 6.5, py - 2, H - 15, 2, 4, 10)])
        add('Switch_Cassette', cradle, 'bronze', explosion=(0, 0, -10))
        add('Tactile_Switch_Envelope', box(px - 6, py - 6, H - 15.4, 12, 12, 6), 'black', True, notes='Looks like 12 mm family in photos; body size and operating travel unmeasured.')
        for xx in [px - 13, px + 11]:
            support = box(xx, py - 9, H - 17, 2, 18, 14)
            support = support.cut(box(xx - 1, py - 3, H - 15.5, 4, 6, 2))
            hook = box(xx + (1.7 if xx < px else -3.2), py - 4, H - 18.6, 3.5, 8, 1.4)
            support = union([support, hook, box(xx, py - 4, H - 18.6, 2, 8, 2)])
            lid = union([lid, support])
            print('TRACE lid line 480', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
    if main:
        lx, ly = (76.7, 25)
        lid = lid.cut(box(lx + 4, ly + 4, H - 20, 72, 26, 25))
        print('TRACE lid line 484', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
        bezel = extr(rr(lx - 2, ly - 2, 84.6, 40, 4).cut(rr(lx + 3.5, ly + 3.5, 73, 27, 2)), H - 0.3, 2.1)
        lid = union([lid, bezel])
        print('TRACE lid line 486', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
        lcdframe = extr(rr(lx - 2, ly - 2, 84.6, 40, 3).cut(rr(lx - 0.4, ly - 0.4, 81.4, 36.8, 1)), H - 22, 17)
        lcdframe = union([lcdframe, box(lx - 2, ly - 2, H - 8, 84.6, 2, 6), box(lx - 2, ly + 34, H - 8, 84.6, 4, 4)])
        for xx in [lx - 2, lx + 80.6]:
            direction = -1 if xx < lx else 1
            ear = box(xx - 1.2 if direction < 0 else xx + 1.8, ly + 12, H - 8, 1.4, 12, 1.3)
            lcdframe = union([lcdframe, ear])
            socket = box(xx - 2, ly + 9, H - 12, 6, 18, 9)
            socket = socket.cut(box(xx - 0.3, ly + 8.7, H - 12.2, 2.6, 18.6, 9.4))
            socket = socket.cut(box(xx - 1.5 if direction < 0 else xx + 1.5, ly + 11.7, H - 8.3, 2, 12.6, 1.9))
            lid = union([lid, socket])
            print('TRACE lid line 497', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
        for xx in [lx - 2, lx + 79.6]:
            lcdframe = union([lcdframe, box(xx, ly + 5, H - 22, 3, 26, 0.8), box(xx, ly + 12, H - 19.1, 3, 5, 1.2)])
        add('LCD_Carrier', lcdframe, 'bronze', explosion=(0, 0, -25), notes='Replaceable edge carrier, parameter-adjustable to the measured PCB. Backpack clearance preserved. Hole-mounted inserts deferred until hole pattern is known.')
        add('LCD_PCB_Envelope', box(lx, ly, H - 21, 80.6, 36, 1.6), 'pcb', True)
        add('LCD_Display_Envelope', box(lx + 5, ly + 5, H - 8, 70, 25, 8), 'lcd', True)
        add('LCD_Backpack_Envelope', box(lx + 8, ly + 7, H - 30, 42, 20, 9), 'black', True)
        for yy in [103, 109, 115, 121]:
            lid = lid.cut(extr(rr(181, yy, 20, 2.5, 1.1), H - 5, 8))
            print('TRACE lid line 504', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
        buzzerseat = ring(191, 114, H - 18, 12, 10.4, 15)
        buzzerseat = buzzerseat.cut(ring(191, 114, H - 18.3, 11.6, 10.2, 1.3))
        for dx in [-12.1, 10.2]:
            buzzerseat = buzzerseat.cut(box(191 + dx, 112.8, H - 18.3, 2, 2.4, 1.6))
        lid = union([lid, buzzerseat])
        print('TRACE lid line 508', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
        buzzerkeeper = ring(191, 114, H - 18.8, 10.2, 6, 1.5)
        buzzerkeeper = union([buzzerkeeper, box(190.1, 102.7, H - 18.1, 1.8, 1.4, 1), box(190.1, 123.9, H - 18.1, 1.8, 1.4, 1)])
        add('Buzzer_Keeper', buzzerkeeper, 'bronze', explosion=(0, 0, -17), notes='Lower bayonet ring leaves room for leads. Actual buzzer and lead spacing require verification.')
        add('Buzzer_Envelope', cyl(191, 114, H - 17, 10, 11), 'black', True)
    if not main:
        for side in [0, 1]:
            grip = extr(rr(15 if side == 0 else W - 69, 136, 54, 62, 16), 0, H + 5)
            grooves = []
            for yy in range(122, 220, 10):
                for sign in [-1, 1]:
                    a = (10 if side == 0 else W - 74, yy)
                    b = (74 if side == 0 else W - 10, yy + sign * 32)
                    grooves.append(stroke([a, b], 0.48, 15, H))
            texture = union(grooves).common(grip).cut(ceiling(W, H - 0.65, False))
            lid = lid.cut(texture)
            print('TRACE lid line 524', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
    esp_x, esp_y = (137, 24) if main else (49, 86)
    add('ESP32_Optional_Envelope', box(esp_x, esp_y, 16, 60, 32, 18), 'optional', True, notes='Provisional 60 x 32 x 18 mm module reservation. Board not selected; verify breadboard header pitch and RF clearance.')
    add('ESP32_Wiring_Clearance', box(esp_x - 3, esp_y - 4, 34, 66, 40, 5), 'clearance', True, notes='Keep free for low-profile jumpers. A tall upright Dupont plug may require more height.')
    for sign in [-1, 1]:
        pts = [(ex + sign * 31, ey + 7), (ex + sign * 43, ey + 14), (ex + sign * 51, ey + 8), (ex + sign * 62, ey + 13)]
        motif = stroke(pts, 0.65, H - 0.25, 0.8)
        lid = union([lid, motif])
        print('TRACE lid line 534', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
    relief = []
    for start in range(0, 360, 45):
        if main and start in [45, 90]:
            continue
        pts = [(ex + 33 * math.cos(math.radians(t)), ey + 33 * math.sin(math.radians(t))) for t in range(start + 5, start + 40, 5)]
        relief.append(stroke(pts, 0.55, H - 0.25, 0.8))
        a = math.radians(start)
        relief.append(stroke([(ex + 29 * math.cos(a), ey + 29 * math.sin(a)), (ex + 37 * math.cos(a), ey + 37 * math.sin(a))], 0.55, H - 0.25, 0.8))
    lid = union([lid] + relief)
    print('TRACE lid line 544', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
    if main:
        hx = 102
        hz = 23
        travel = 35
        base = base.cut(box(hx, -10, hz, 30, 25, 20))
        print('TRACE base line 549', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
        base = base.cut(box(hx - 1.4, -2.55, hz - 1.1, 68, 3.0, 22.2))
        print('TRACE base line 550', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
        rails = union([box(hx - 3, -4, hz - 4, 72, 8, 2.9), box(hx - 3, -4, hz + 21.1, 72, 8, 3), box(hx + 67, -4, hz - 4, 3, 8, 28.1)])
        rails = union([rails, box(hx - 3, -4, hz - 4, 72, 1.4, 6), box(hx - 3, -4, hz + 18.1, 72, 1.4, 6)])
        rails = union([rails, box(hx - 3, 0.6, hz - 4, 72, 3.4, 6), box(hx - 3, 0.6, hz + 18.1, 72, 3.4, 6)])
        base = union([base, rails])
        print('TRACE base line 555', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
        shutter = box(hx - 1, -2.2, hz - 0.7, 32, 2.2, 21.4)
        shutter = union([shutter, box(hx + 10, -5.2, hz + 6, 10, 3.1, 8)])
        keeper = union([box(hx - 3, -3.6, hz - 0.5, 1.6, 5.4, 25), box(hx - 3, -3.6, hz + 23.5, 3.6, 11.6, 1.2)])
        base = base.cut(box(hx - 3.2, -3.8, hz - 0.7, 2, 5.8, 25.4))
        print('TRACE base line 560', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
        base = base.cut(box(hx - 3.2, -3.8, hz + 23.3, 4, 12, 1.6))
        print('TRACE base line 561', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
        add('USB_Shutter', shutter, 'bronze', explosion=(0, -24, 0), notes='Captive sliding cover: 35 mm travel. Open before inserting cable; close only when unplugged. Fit/retention prototype.')
        add('USB_Shutter_Keeper', keeper, 'bronze', explosion=(0, 0, 16), notes='Keyed end stop installed from above; its head is trapped below the closed Main lid. Remove lid for service. Coupon fit required.')
        add('USB_Plug_Clearance', box(hx + 3, 4, hz + 2, 24, 31, 16), 'clearance', True, notes='Provisional plug and bend access above breadboard. Confirm actual USB-B/C cable.')
        for yy in [103, 109, 115, 121]:
            lid = lid.cut(extr(rr(33, yy, 20, 2.5, 1.1), H - 5, 8))
            print('TRACE lid line 566', round(lid.Volume), len(lid.Solids), lid.isValid(), flush=True)
    print('Pre-seam', base.Volume, len(base.Solids), base.isValid(), lid.Volume, len(lid.Solids), lid.isValid(), flush=True)
    base.exportBrep(str(ROOT / (role + '-base-before-seam.brep')))
    lid.exportBrep(str(ROOT / (role + '-lid-before-seam.brep')))
    base = base.cut(lid)
    print('TRACE base line 572', round(base.Volume), len(base.Solids), base.isValid(), flush=True)
    add('Base', base, 'bronze', notes='Cradles, battery bay, strap anchors and cable saddles are integral. No screw bosses.')
    add('Lid', lid, 'bronze', explosion=(0, 0, 40), notes='Rear locating tabs + two press-release side latches. All fits require coupons.')
    add('Breadboard_Envelope', box(bx, by, 5, bb[0], bb[1], bb[2]), 'breadboard', True)
    add('UNO_PCB_Envelope', box(ux, uy, 7, uno[0], uno[1], 1.6), 'pcb', True)
    add('UNO_Header_Envelope', union([box(ux + 2, uy + 2, 8.6, uno[0] - 4, 5, 9), box(ux + 2, uy + uno[1] - 7, 8.6, uno[0] - 4, 5, 9)]), 'black', True)
    add('Battery_Envelope', box(batx + 1.75, baty + 11, 7, 26.5, 48.5, 17.5), 'battery', True, notes='Common PP3 maximum envelope, not brand-specific; snap/lead space at bay leading end.')
    add('Battery_Clip_Envelope', box(batx + 2, baty + 4, 7, 26, 7, 18), 'black', True)
    mx, my = (172, 72) if main else (189, 139)
    add('Power_Module_Reservation', box(mx, my, 6, 30, 22, 12), 'reservation', True, notes='REGULATOR / LOAD SWITCH: component not selected; not an installed part.')
    doc.recompute()
    doc.saveAs(str(OUT / f'{role}-revision06.FCStd'))
    printable = [o for o in shell_group.Group]
    Part.export(printable, str(OUT / f'{role}-printed-parts.step'))
    primary = {k: v for k, v in envs.items() if k in ['Breadboard_Envelope', 'UNO_PCB_Envelope', 'Battery_Envelope', 'Power_Module_Reservation', 'SG90_Body_Envelope']}
    pairs = []
    for i, (a, sa) in enumerate(primary.items()):
        for b, sb in list(primary.items())[i + 1:]:
            overlap = sa.common(sb).Volume
            pairs.append({'a': a, 'b': b, 'intersection_mm3': round(overlap, 4)})
            if overlap > 0.01:
                raise RuntimeError(f'Envelope collision {role}: {a}/{b}: {overlap}')
    fit = []
    for n, s in primary.items():
        fit.append({'component': n, 'base_intersection_mm3': round(s.common(base).Volume, 3), 'lid_intersection_mm3': round(s.common(lid).Volume, 3)})
    all_records.extend(records)
    App.closeDocument(doc.Name)
    print(role, ':', len(printable), 'printed parts;', len(envs), 'reference envelopes', flush=True)
    return {'role': role, 'nominal_size_mm': [W, D, H], 'primary_envelope_pairs': pairs, 'shell_contact_review': fit, 'physical_fit_verified': False}
if __name__ == '__main__':
    import sys
    selected = sys.argv[1:] or ['explorer', 'architect', 'main']
    if (ROOT / 'scene.json').exists():
        all_records.extend([r for r in json.loads((ROOT / 'scene.json').read_text()) if r['role'] not in selected])
    previous = json.loads((ROOT / 'CAD_VALIDATION.json').read_text()) if (ROOT / 'CAD_VALIDATION.json').exists() else {}
    checks.extend([r for r in previous.get('parts', []) if r['role'] not in selected])
    reviews = [r for r in previous.get('layout', []) if r['role'] not in selected]
    for role in selected:
        reviews.append(build(role))
        (ROOT / 'scene.json').write_text(json.dumps(all_records, indent=2))
    (ROOT / 'scene.json').write_text(json.dumps(all_records, indent=2))
    (ROOT / 'CAD_VALIDATION.json').write_text(json.dumps({'scope': 'Prototype solid validity and basic envelope checks only; not a print release.', 'parts': checks, 'layout': reviews}, indent=2))
    print('CAD, STEP and prototype STL exports complete.', flush=True)