"""Added thumb support in the open/spread orientation shown by the Phoenix guide."""
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
for x in [-31,31]:receiver=receiver.cut(slot(3,22,7,x,16,-10))
# Two M4 support screws/pads at fore end. Actual heights are set on the bench.
for x in [-18,18]:
 receiver=receiver.union(cyl(10,4,x,32,-4)).cut(cyl(4.4,15,x,32,-10))
# Match only the underside of the retained palm; leave 0.3 mm vertical assembly clearance.
reference=cq.importers.importStep(str(R.parent/'phoenix_v3/exports/phoenix_motorised_reference.step'))
palm_source=max((q for q in reference.solids().vals() if q.BoundingBox().ymax>0),key=lambda q:q.Volume())
receiver=receiver.cut(cq.Workplane('XY').newObject([palm_source]).translate((0,0,-.3))).cut(cq.Workplane('XY').newObject([palm_source]))
# Plate mounts to component housing using existing two M4 positions.
# Connected thumb fork: source thumb geometry moves 18 mm outward and 6 mm upward.
# This creates room for a mount while leaving the palm and both source thumb parts intact.
source_path=R.parent/'upstream/phoenix_v3.step'
source_hash=hashlib.sha256(source_path.read_bytes()).hexdigest()
assert source_hash=='3d7086af7fd8a3b8f33ca87d8af6b10bdc7fc9038eb923bf920633acd7227620'
source=cq.importers.importStep(str(source_path)).solids().vals()
def axis_joint(shape,r):
 faces=[f for f in shape.Faces() if f.geomType()=='CYLINDER' and abs(f._geomAdaptor().Cylinder().Radius()-r)<1e-4]
 assert faces
 f=faces[0];b=f.BoundingBox();q=f._geomAdaptor().Cylinder().Axis().Location()
 return ((b.xmin+b.xmax)/2,q.Y(),q.Z())
pr=axis_joint(source[24],2.3);pt=axis_joint(source[24],2.375)
thumb_root=(-56.9714,31.4971,11.8007)
def thumb_pose(shape,tilt=0):
 return (shape.translate(tuple(-v for v in pr)).rotate((0,0,0),(1,0,0),tilt)
 .rotate((0,0,0),(0,0,1),130).translate(thumb_root))
thumb_proximal=thumb_pose(cq.Workplane('XY').newObject([source[24]]))
# Distal bore centre from source coaxial faces, preserving its original hinge geometry.
entries=[]
for f in source[27].Faces():
 if f.geomType()=='CYLINDER' and abs(f._geomAdaptor().Cylinder().Radius()-2.25)<1e-4:
  b=f.BoundingBox();q=f._geomAdaptor().Cylinder().Axis().Location();entries.append(((b.xmin+b.xmax)/2,q.Y(),q.Z()))
dr=((min(v[0] for v in entries)+max(v[0] for v in entries))/2,entries[0][1],entries[0][2])
thumb_distal=thumb_pose(cq.Workplane('XY').newObject([source[27]]).translate(tuple(pt[i]-dr[i] for i in range(3))))
# Fork in its local joint coordinates; two bearing cheeks, 7.6 mm clear spacing.
fork=box(14,12,3,0,-4,-18)
for x in [-4.8,4.8]:
 ear=cq.Workplane('YZ').circle(6).extrude(2).translate((x-1,0,0))
 stem=box(2,8,17,x,-4,-17)
 ear=ear.union(stem).cut(cq.Workplane('YZ').circle(2.3).extrude(4).translate((x-2,0,0)))
 fork=fork.union(ear)
# Root-body relief in new fork only; preserve the source thumb itself.
for angle in [0,-15,-30,-45]:
 moving=(cq.Workplane('XY').newObject([source[24]]).translate(tuple(-v for v in pr))
 .rotate((0,0,0),(1,0,0),angle))
 fork=fork.cut(moving)
fork=fork.rotate((0,0,0),(0,0,1),130).translate(thumb_root)
receiver=receiver.union(box(35,37,4,-49,22.5,-8).edges('|Z').fillet(5)).union(fork)
# Recheck fork against the source thumb at sampled hinge angles.
for angle in [0,-15,-30,-45]:
 assert fork.intersect(thumb_pose(cq.Workplane('XY').newObject([source[24]]),angle)).val().Volume()<1e-4
