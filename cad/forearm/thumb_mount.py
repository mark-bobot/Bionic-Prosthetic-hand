"""Retained wrist support; thumb assembles on the original Phoenix palm hinge."""
from pathlib import Path
import hashlib
import cadquery as cq
R=Path(__file__).resolve().parent
def box(w,l,h,x=0,y=0,z=0):return cq.Workplane('XY').box(w,l,h,centered=(True,True,False)).translate((x,y,z))
def cyl(d,h,x,y,z):return cq.Workplane('XY').circle(d/2).extrude(h).translate((x,y,z))
def slot(w,l,h,x,y,z):return cq.Workplane('XY').center(x,y).slot2D(l,w,angle=90).extrude(h).translate((0,0,z))
# Fixed palm support: retain original 6 mm wrist-bore attachment and add a lower stop.
cradle=cq.importers.importStep(str(R.parent/'phoenix_v3/exports/phoenix_wrist_cradle.step'))
receiver=cradle.union(box(70,15,8,0,-6,-4)).union(box(70,52,4,0,17,-8).edges('|Z').fillet(4))
# 20 mm retention strap around the rear of the printed palm and support.
for x in [-24,31]:receiver=receiver.cut(slot(3,22,7,x,16,-10))
# Two M4 support screws/pads at fore end. Actual heights are set on the bench.
for x in [-18,18]:
 receiver=receiver.union(cyl(10,4,x,32,-4)).cut(cyl(4.4,15,x,32,-10))
# Match only the underside of the retained palm; leave 0.3 mm vertical assembly clearance.
reference=cq.importers.importStep(str(R.parent/'phoenix_v3/exports/phoenix_motorised_reference.step'))
palm_source=max((q for q in reference.solids().vals() if q.BoundingBox().ymax>0),key=lambda q:q.Volume())
receiver=receiver.cut(cq.Workplane('XY').newObject([palm_source]).translate((0,0,-.3))).cut(cq.Workplane('XY').newObject([palm_source]))
# Plate mounts to component housing using existing two M4 positions.
# Local scallop clears the original thumb sweep; left strap slot moves inboard.
receiver=receiver.cut(box(20,32,12,-39,38,-10).edges('|Z').fillet(2))
# Native thumb placement is defined with the same source and datum as the fingers.
# No outboard fork, relocated joint, or cuts to the Phoenix source surfaces.
from hand import S as source, joint, X, Y, ZMIN
import math
axis=cq.Vector(-math.cos(math.radians(50)), math.sin(math.radians(50)), 0)
faces=[]
for f in source[2].Faces():
 if f.geomType()!='CYLINDER':continue
 c=f._geomAdaptor().Cylinder();d=c.Axis().Direction()
 if abs(abs(cq.Vector(*d.Coord()).dot(axis))-1)<1e-6 and any(abs(c.Radius()-r)<1e-4 for r in [2.5,2.7]):
  ends=[v.Center().dot(axis) for v in f.Vertices()]
  faces.append((min(ends),max(ends),c))
# Three bore intervals: first ear, its narrower inner shoulder, opposite ear.
intervals=sorted(set((round(a,6),round(b,6)) for a,b,c in faces))
assert len(intervals)==3,intervals
inner_faces=(intervals[1][1],intervals[2][0])
assert abs(inner_faces[1]-inner_faces[0]-6.5)<1e-4
c=faces[0][2];origin=cq.Vector(*c.Axis().Location().Coord())
centre=origin+axis*(sum(inner_faces)/2-origin.dot(axis))
thumb_root=(centre-cq.Vector(X,Y,ZMIN)).toTuple()
pr=joint(24,2.3);pt=joint(24,2.375)
entries=[]
for f in source[27].Faces():
 if f.geomType()=='CYLINDER' and abs(f._geomAdaptor().Cylinder().Radius()-2.25)<1e-4:
  b=f.BoundingBox();q=f._geomAdaptor().Cylinder().Axis().Location()
  entries.append(((b.xmin+b.xmax)/2,q.Y(),q.Z()))
dr=((min(v[0] for v in entries)+max(v[0] for v in entries))/2,entries[0][1],entries[0][2])
# -60 degrees is the checked display pose, not an inferred anatomical angle or stop.
# A coplanar thumb at zero degrees collides with the original palm shoulders.
def thumb_pose(shape,tilt=-60):
 return (shape.translate(tuple(-v for v in pr)).rotate((0,0,0),(1,0,0),tilt)
 .rotate((0,0,0),(0,0,1),130).translate(thumb_root))
def posed_thumb(root_angle=-60,tip_angle=10):
 p=cq.Workplane('XY').newObject([source[24]])
 d=(cq.Workplane('XY').newObject([source[27]])
 .rotate(dr,(dr[0],dr[1]+1,dr[2]),180)
 .translate(tuple(pt[i]-dr[i] for i in range(3))))
 d=d.rotate(pt,(pt[0]+1,pt[1],pt[2]),-tip_angle)
 return {'thumb_proximal':thumb_pose(p,root_angle),'thumb_distal':thumb_pose(d,root_angle)}
thumb_proximal,thumb_distal=posed_thumb().values()
