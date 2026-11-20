import FreeCAD as A
import Part
V=A.Vector
def contact_shoe(px,py,z,delta,box,cyl,union):
    q=union([cyl(px,py,z-delta,2.5,4+delta),box(px-1.2,py-1.2,z+3.9,2.4,2.4,3.2)])
    for sign in [-1,1]:
        pts=[V(px+sign*u,py-.8,z+v) for u,v in [(1.15,6.35),(1.5,6.35),(1.5,6.6),(1.15,7.1)]]
        tab=Part.Face(Part.makePolygon(pts+[pts[0]])).extrude(V(0,1.6,0));q=q.fuse(tab)
    return q.cut(box(px-.25,py-1.3,z+4.5,.5,2.6,2.8)).removeSplitter()
def release_cuts(px,py,z,box):
    return [box(px-1.65,py-1.4,z+6.2,3.3,2.8,.8),
            box(px-2.7,py-.9,z+6.3,1.35,1.8,.65),box(px+1.35,py-.9,z+6.3,1.35,1.8,.65)]
