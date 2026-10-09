"""Rigid, ventrally open arm carrier; dimensions are an unfitted design study."""
import cadquery as cq

def box(w,l,h,x,y,z):
    return cq.Workplane('XY').box(w,l,h,centered=(True,True,False)).translate((x,y,z))

def make_arm_adapter(p,deck):
    ri=p['adapter_inner_radius_mm'];ro=ri+p['adapter_wall_mm'];cz=p['cuff_axis_z_mm']
    start=-24-p['adapter_length_mm']
    outer=cq.Solid.makeCylinder(ro,-38-start,cq.Vector(0,start,cz),cq.Vector(0,1,0))
    inner=cq.Solid.makeCylinder(ri,200,cq.Vector(0,-200,cz),cq.Vector(0,1,0))
    shell=cq.Workplane('XY').newObject([outer.cut(inner)]).intersect(box(120,200,100,0,-100,-10))
    for y in [-142,-57]:
        for side in [-1,1]:
            lug=box(12,27,5,side*35,y,-10).edges('|Z').fillet(2)
            shell=shell.union(lug).cut(box(3,21,9,side*38,y,-12))
    for x in [-34,34]:
        for y in [-86,-30]:
            post=box(12,12,deck-14,x,y,14).edges('|Z').fillet(2)
            if y==-30:
                shell=shell.union(box(10,24,23,x,-36,-6))
            shell=shell.union(post)
            bore=cq.Workplane('XY').center(x,y).circle(2.2).extrude(deck+4).translate((0,0,12))
            nut=cq.Workplane('XY').center(x,y).polygon(6,8).extrude(3.5).translate((0,0,14))
            shell=shell.cut(bore).cut(nut)
            shell=shell.cut(box(8,8,3.5,x+(4 if x>0 else -4),y,14))
    shell=shell.union(box(74,22,6,0,-24,-6))
    for side in [-1,1]:shell=shell.union(box(10,24,12,side*32,-38,-6))
    for x in [-18,18]:
        shell=shell.cut(cq.Workplane('XY').center(x,-24).circle(2.2).extrude(10).translate((0,0,-8)))
        shell=shell.cut(cq.Workplane('XY').center(x,-24).polygon(6,8).extrude(3.5).translate((0,0,-6)))
    reserved=cq.Solid.makeCylinder(ri,-44-start,cq.Vector(0,start,cz),cq.Vector(0,1,0))
    shell=shell.cut(cq.Workplane('XY').newObject([reserved]))
    return shell.val()
