"""Phoenix-derived bionic integration. CadQuery 2.8.0; mm; CC BY 4.0.
Patient fit and strength are unverified. Original source hand is retained.
"""
from pathlib import Path
import json,math,hashlib
import cadquery as cq
import trimesh
R=Path(__file__).resolve().parent;O=R/'exports';O.mkdir(exist_ok=True)
P=json.loads((R.parent/'arm_interface/parameters.json').read_text())
def box(w,l,h,x=0,y=0,z=0):return cq.Workplane('XY').box(w,l,h,centered=(True,True,False)).translate((x,y,z))
def cyl(d,h,x,y,z):return cq.Workplane('XY').circle(d/2).extrude(h).translate((x,y,z))
def slot(w,l,h,x,y,z):return cq.Workplane('XY').center(x,y).slot2D(l,w,angle=90).extrude(h).translate((0,0,z))
def bore_y(d,l,x,y,z):return cq.Workplane('XZ').circle(d/2).extrude(l,both=True).translate((x,y,z))
def envelope(extra=0):
 return (cq.Workplane('XY').ellipse(P['distal_inner_width_mm']/2+extra,P['distal_inner_depth_mm']/2+extra)
 .workplane(offset=P['length_mm']).ellipse(P['proximal_inner_width_mm']/2+extra,P['proximal_inner_depth_mm']/2+extra)
 .loft().rotate((0,0,0),(1,0,0),90).translate((0,P['distal_y_mm'],P['centre_z_mm'])))
outer=envelope(P['wall_mm']);inner=envelope()
# Reuse saddle geometry, preserving assembly coordinates (print export had zmin=-44).
saddle=cq.importers.importStep(str(R.parent/'arm_interface/exports/right_open_saddle.step')).translate((0,0,-44))
# Closed distal end: a structural interface, not a pressure prescription.
cap=(cq.Workplane('XY').ellipse(P['distal_inner_width_mm']/2+P['wall_mm'],P['distal_inner_depth_mm']/2+P['wall_mm']).extrude(3).rotate((0,0,0),(1,0,0),90).translate((0,-22,-40)))
socket_dorsal=saddle.union(cap)
# Removable lower shell, 0.6 mm seam gap. Separate straps hold upper/lower sections.
door=outer.cut(inner).intersect(box(140,200,100,0,-95,-144.6))
for y in [-60,-140]:
 for x in [-35,35]:
  door=door.union(box(24,28,4,x,y,-49).edges('|Z').fillet(3))
  door=door.cut(slot(3.5,22,8,42 if x>0 else -42,y,-51))
door=door.cut(inner)
# Electrode access through the ventral shell. Probe is held by an independent soft band.
door=door.cut(box(28,45,40,0,-105,-90).edges('|Z').fillet(3))
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
 .rotate((0,0,0),(0,0,1),50).translate(thumb_root))
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
for angle in [0,15,30,45]:
 moving=(cq.Workplane('XY').newObject([source[24]]).translate(tuple(-v for v in pr))
 .rotate((0,0,0),(1,0,0),angle))
 fork=fork.cut(moving)
fork=fork.rotate((0,0,0),(0,0,1),50).translate(thumb_root)
receiver=receiver.union(box(35,37,4,-49,22.5,-8).edges('|Z').fillet(5)).union(fork)
# Recheck fork against the source thumb at sampled hinge angles.
for angle in [0,15,30,45]:
 assert fork.intersect(thumb_pose(cq.Workplane('XY').newObject([source[24]]),angle)).val().Volume()<1e-4
# Removable equaliser cassette above the forward housing. Keep winding radius unchanged.
base=box(94,74,2,0,-52,65).edges('|Z').fillet(5)
# Continuous rounded wall follows the existing floor; 3 mm wall and ports retained.
cassette_wall=(box(94,74,7,0,-52,67).edges('|Z').fillet(5)
 .cut(box(88,68,9,0,-52,66).edges('|Z').fillet(2)))
base=base.union(cassette_wall)
for x in [-32,0,32]:base=base.union(box(2,68,7,x,-52,67))
# Integral feet over the existing front housing fastener stations (global y=-82).
for x in [-41,41]:base=base.union(cyl(12,1,x,-82,64)).cut(cyl(3.4,10,x,-82,63))
# Lid bosses clear the full equaliser and thumb-slider travel.
lid_bosses=[(x,y) for x in [-43,43] for y in [-70,-27]]
for x,y in lid_bosses:base=base.union(cyl(6,7,x,y,67)).cut(cyl(3.4,14,x,y,64)).cut(cyl(4.2,4,x,y,67))
# Two input lines; four finger output lines. Thumb uses a separate narrow lane.
for x in [-16,16,-37]:base=base.cut(bore_y(2.2,6,x,-87.5,70))
for x in [-26,-6,6,26,-37]:base=base.cut(bore_y(2.2,6,x,-16.5,70))
# Cover: screw seats and inspection windows keep knots/return motion accessible.
cover=box(94,74,3,0,-52,74).edges('|Z').fillet(5).edges('>Z').chamfer(.8)
# Shallow head seats keep 2 mm of cover under heads; actual screw heads must be measured.
for x,y in lid_bosses:
 cover=cover.cut(cyl(3.4,5,x,y,73)).cut(cyl(6.2,1.2,x,y,76))
for x in [-16,16]:cover=cover.cut(slot(4,34,5,x,-50,73))
cover=cover.cut(slot(3,30,5,-37,-50,73))
# Existing equaliser: equal arms, 20 mm output pitch. Constrained under removable cover.
eq=cq.importers.importStep(str(R.parent/'exports/pair_equaliser.step'))
left=eq.translate((-16,-36,68));right=eq.translate((16,-36,68))
thumb_slider=box(6,12,4,-37,-36,68).edges('|Z').fillet(1.5)
for y in [-40,-32]:thumb_slider=thumb_slider.cut(cyl(2.4,6,-37,y,67))
# Sample full slider travel and equaliser tilt; 38 mm stroke with +/-30 degree in-plane tilt.
travel_checks=[]
for x in [-16,16]:
 for y in [-74,-55,-36]:
  for a in [-30,0,30]:
   bar=eq.rotate((0,0,0),(0,0,1),a).translate((x,y,68))
   v=bar.intersect(base).val().Volume()+bar.intersect(cover).val().Volume()
   assert v<1e-4,('equaliser pose',x,y,a,v)
   travel_checks.append([x,y,a])
for y in [-74,-55,-36]:
 slider=thumb_slider.translate((0,y+36,0));assert slider.intersect(base).val().Volume()<1e-4
# Wrist exit comb, with five PTFE liner seats, mounted to the receiver plate.
comb=box(82,8,10,0,-14,15).edges('|Z').fillet(2)
for x in [-31,31]:comb=comb.union(box(8,8,11,x,-14,4))
for x in [-26,-6,6,26,-37]:comb=comb.cut(bore_y(2.2,8,x,-14,20))
# Two M3 fasteners down through receiver plate; long stock cut to measured fit.
for x in [-31,31]:comb=comb.cut(cyl(3.4,24,x,-14,2));receiver=receiver.cut(cyl(3.4,10,x,-14,-5))
# Dedicated input feed-throughs in a copy of the current lid (extra geometry only).
local_lid=cq.importers.importStep(str(R.parent/'compact/exports/compact_lid.step')).translate((0,0,52))
housing_lid=local_lid.rotate((0,0,0),(0,0,1),180).translate((0,-30,4))
for x in [-40,0,40]:housing_lid=housing_lid.cut(cyl(2.4,12,x,-130,56))
# Restore full cover thickness at the two cassette-bearing seats.
for x in [-41,41]:housing_lid=housing_lid.union(cyl(6.4,2,x,-82,62)).cut(cyl(3.4,8,x,-82,60))
# Print exports; assembly coordinates tracked so sources can be reproduced.
parts={'socket_dorsal':socket_dorsal,'socket_ventral_door':door,'fixed_palm_receiver':receiver,
       'tendon_cassette_base':base,'tendon_cassette_cover':cover,'thumb_line_slider':thumb_slider,'wrist_guide_comb':comb,'housing_lid_with_feedthroughs':housing_lid}
report={'status':'Right transradial bionic CAD prototype; placeholder socket, no clinical fit or strength acceptance',
 'source_sha256':source_hash,'thumb_root_sampled_angles_deg':[0,15,30,45], 'thumb_fork_bore_mm':4.6, 'parts':{},'equaliser_sampled_poses':travel_checks,'slider_stroke_mm':38,
 'socket_placeholder_parameters':P,'collisions':[],
 'finish':{'cassette_outer_corner_radius_mm':5,'cassette_wall_mm':3,'cover_edge_chamfer_mm':.8,'cover_head_recess_diameter_mm':6.2,'cover_head_recess_depth_mm':1,'thumb_support_corner_radius_mm':5},'notes':[
 'Original palm/finger geometry retained; connected thumb fork offsets the source thumb by 18 mm outward and 6 mm upward.',
 'Receiver lower support and retention strap restrain the original pivot; clamp load and hardware fit unverified.',
 'Cassette adds height: installed maximum Z=77 mm; housing alone remains 60 mm high.',
 'Cassette uses actual existing two equaliser solids; PTFE loops/cords and strap closures require physical installation.']}
for n,p in parts.items():
 assert len(p.solids().vals())==1 and p.val().isValid(),(n,len(p.solids().vals()))
 b=p.val().BoundingBox();q=p.translate((0,0,-b.zmin))
 cq.exporters.export(q,str(O/f'{n}.step'));cq.exporters.export(q,str(O/f'{n}.stl'),tolerance=.07,angularTolerance=.15)
 m=trimesh.load_mesh(O/f'{n}.stl');assert m.is_watertight and m.volume>0,n
 report['parts'][n]={'watertight':True,'size_mm':m.extents.tolist(),'assembly_zmin_mm':b.zmin,'volume_mm3':float(m.volume)}
# Existing assembly includes its old cradle; replace only that part with the receiver.
old=cq.importers.importStep(str(R.parent/'phoenix_v3/exports/phoenix_motorised_reference.step'))
old_solids=old.solids().vals();cradle_shape=cradle.val()
# Find old cradle by its bounding box and volume rather than a brittle import index.
remaining=[]
for s in old_solids:
 b=s.BoundingBox();c=cradle_shape.BoundingBox()
 is_cradle=(abs(s.Volume()-cradle_shape.Volume())<.01 and abs(b.ymin-c.ymin)<.01 and abs(b.ymax-c.ymax)<.01)
 old_lid_shape=local_lid.rotate((0,0,0),(0,0,1),180).translate((0,-30,4)).val()
 is_old_lid=(abs(s.Volume()-old_lid_shape.Volume())<.01 and abs(b.zmax-old_lid_shape.BoundingBox().zmax)<.01)
 is_old_thumb=(b.xmin<-55 and b.ymax>0 and b.zmin>8)
 if not is_cradle and not is_old_thumb and not is_old_lid:remaining.append(s)
assert len(remaining)==len(old_solids)-4
existing=cq.Workplane('XY').newObject([cq.Compound.makeCompound(remaining)])
carrier=cq.importers.importStep(str(R.parent/'arm_interface/exports/emg_band_carrier.step')).translate((0,-105,-78))
models={'independent_emg_carrier':carrier,'existing_hand_and_housing':existing,'thumb_proximal':thumb_proximal,'thumb_distal':thumb_distal,**parts,'equaliser_index_middle':left,'equaliser_ring_little':right}
# Sample thumb MCP positions against the fixed hand and receiver as well as its fork.
for angle in [0,15,30,45]:
 for moving in [thumb_pose(cq.Workplane('XY').newObject([source[24]]),angle),
                thumb_pose(cq.Workplane('XY').newObject([source[27]]).translate(tuple(pt[i]-dr[i] for i in range(3))),angle)]:
  for fixture in [existing,receiver,comb]:
   v=moving.intersect(fixture).val().Volume()
   assert v<.001,('thumb sampled assembly',angle,v)
# Pair intersections, with contact tolerances kept separate from volume collisions.
items=list(models.items())
for i,(n,p) in enumerate(items):
 for nn,q in items[i+1:]:
  a,b=p.val().BoundingBox(),q.val().BoundingBox()
  if any(min(getattr(a,k+'max'),getattr(b,k+'max'))-max(getattr(a,k+'min'),getattr(b,k+'min'))<=1e-5 for k in 'xyz'):continue
  v=p.intersect(q).val().Volume()
  if v>1e-4:report['collisions'].append([n,nn,v])
(R/'checks.json').write_text(json.dumps(report,indent=2)+'\n')
assert not report['collisions'],report['collisions']
assembly=cq.Assembly(name='right_bionic_prototype')
for n,p in models.items():assembly.add(p,name=n)
cq.exporters.export(assembly.toCompound(),str(O/'complete_right_bionic.step'))
# Preview uses depth testing so hidden mesh triangles do not show through covers.
from render import render as render_preview
render_preview(O/'complete_right_bionic.step',O/'complete_preview.png')
print(json.dumps({'parts':report['parts'],'collisions':report['collisions'],'equaliser_poses':len(travel_checks)},indent=2))
