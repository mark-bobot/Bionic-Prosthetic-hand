"""Attach the smaller-part pack to retained Phoenix and socket geometry; mm."""
from pathlib import Path
import json,sys
import cadquery as cq
import trimesh
R=Path(__file__).resolve().parent;O=R/'exports'
def box(w,l,h,x=0,y=0,z=0):return cq.Workplane('XY').box(w,l,h,centered=(True,True,False)).translate((x,y,z))
def cyl(d,h,x,y,z):return cq.Workplane('XY').circle(d/2).extrude(h).translate((x,y,z))
def load(p):return cq.importers.importStep(str(p))
def world(s):return s.rotate((0,0,0),(0,0,1),180).translate((0,-30,4))
def signature(s):
 b=s.BoundingBox();return [s.Volume(),b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax]
def matches(a,b):return all(abs(x-y)<.002 for x,y in zip(signature(a),signature(b)))
old_pack=world(load(R.parent/'compact/exports/compact_assembly.step')).solids().vals()
old=load(R.parent/'bionic/exports/complete_right_bionic.step').solids().vals()
report=json.loads((R.parent/'bionic/checks.json').read_text())
moving=['tendon_cassette_base','tendon_cassette_cover','thumb_line_slider']
replace={}
for name in moving+['housing_lid_with_feedthroughs']:
 replace[name]=load(R.parent/f'bionic/exports/{name}.step').translate((0,0,report['parts'][name]['assembly_zmin_mm']))
eq=load(R.parent/'exports/pair_equaliser.step')
replace['equaliser_left']=eq.translate((-16,-36,68));replace['equaliser_right']=eq.translate((16,-36,68))
keep=[];removed=0
for s in old:
 if any(matches(s,q) for q in old_pack) or any(matches(s,q.val()) for q in replace.values()):removed+=1
 else:keep.append(s)
# Old compact lid is absent in the bionic assembly; the feedthrough lid replaces it.
assert removed==len(old_pack)-1+len(replace),(removed,len(old_pack),len(replace))
new_pack=world(load(O/'compact_assembly.step'))
plain_lid=world(load(O/'compact_lid.step').translate((0,0,47)))
new_pack_solids=[s for s in new_pack.solids().vals() if not matches(s,plain_lid.val())]
assert len(new_pack_solids)==len(new_pack.solids().vals())-1
lid=plain_lid
for x in [-40,0,40]:lid=lid.cut(cyl(2.4,10,x,-130,48))
# Cassette bearings remain at the same XY fastener stations, 10 mm lower.
for x in [-41,41]:lid=lid.union(cyl(6.4,2,x,-82,52)).cut(cyl(3.4,8,x,-82,50))
models={f'retained_{i}':cq.Workplane('XY').newObject([s]) for i,s in enumerate(keep)}
models.update({f'pack_{i}':cq.Workplane('XY').newObject([s]) for i,s in enumerate(new_pack_solids)})
models['feedthrough_lid']=lid
for name,p in replace.items():
 if name!='housing_lid_with_feedthroughs':models[name]=p.translate((0,0,-10))
collisions=[]
items=list(models.items())
for i,(n,p) in enumerate(items):
 for nn,q in items[i+1:]:
  a,b=p.val().BoundingBox(),q.val().BoundingBox()
  if any(min(getattr(a,k+'max'),getattr(b,k+'max'))-max(getattr(a,k+'min'),getattr(b,k+'min'))<=1e-5 for k in 'xyz'):continue
  v=p.intersect(q).val().Volume()
  if v>.001:collisions.append([n,nn,v])
assert not collisions,collisions
# The whole cassette and its moving bars translate together; inherited internal travel remains unchanged.
# Source source-joint contacts below 0.001 mm3 are tolerated as in the parent assembly.
assert lid.val().isValid() and len(lid.solids().vals())==1
b=lid.val().BoundingBox();print_lid=lid.translate((0,0,-b.zmin))
for ext in ['step','stl']:cq.exporters.export(print_lid,str(O/f'feedthrough_lid.{ext}'))
m=trimesh.load_mesh(O/'feedthrough_lid.stl');assert m.is_watertight and m.volume>0
assembly=cq.Compound.makeCompound([p.val() for p in models.values()])
cq.exporters.export(assembly,str(O/'complete_slim_candidate.step'))
checks={'status':'Replacement-parts layout candidate; power system and hardware fit unverified','collisions':collisions,
 'housing_mm':[94,160,50],'previous_housing_mm':[94,160,60],
 'housing_plus_cassette_height_mm':63,'previous_housing_plus_cassette_height_mm':73,
 'cassette_translation_mm':[0,0,-10],'source_hand_sha256':report['source_sha256'],
 'retained_solids':len(keep),'feedthrough_lid_watertight':True,'feedthrough_lid_assembly_zmin_mm':b.zmin,
 'open_checks':['Actual servo ear/shaft/horn geometry and connector clearance','Protected 2S pack and high-current path selection','Full swept articulation and flexible tendon routing','Enclosure thermal test and fitted socket']}
(R/'integration_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
sys.path.insert(0,str(R.parent/'bionic'))
from render import render
render(O/'complete_slim_candidate.step',O/'complete_preview.png',title='Smaller-part bionic Phoenix — layout candidate')
print(json.dumps(checks,indent=2))
