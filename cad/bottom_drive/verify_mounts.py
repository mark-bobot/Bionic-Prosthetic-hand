"""Check nominal fastener allowances against the exported print solids."""
from pathlib import Path
import json,hashlib
import cadquery as cq
import numpy as np
R=Path(__file__).resolve().parent;O=R/'exports'
j=json.loads((O/'checks.json').read_text());deck=j['box_deck_global_z_mm']
parts={}
for n,q in j['parts'].items():
 if n in ['two_groove_drum','thumb_drum']:continue
 s=cq.importers.importStep(str(O/f'{n}.step')).val()
 z=q.get('assembly_global_zmin_mm',q.get('assembly_local_zmin_mm',0)+deck)
 parts[n]=s.translate((0,0,z))
def cyl(r,h,x,y,z):return cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z))
fasteners={}
for x in [-34,34]:
 for y in [-86,-30]:
  body=cyl(2,deck+1.8-13,x,y,13)
  head=cq.Solid.makeCone(2,4.2,2.2,cq.Vector(x,y,deck+1.8))
  fasteners[f'box_M4_{x}_{y}']=body.fuse(head)
for x in [-18,18]:
 fasteners[f'receiver_M4_{x}']=cyl(2,9.5,x,-24,-6.5).fuse(cyl(4,2.5,x,-24,3))
ear_top=j['motor_ear_top_local_z_mm']+deck
height=j['box_body_size_mm'][2]+deck
for i,(x,y) in enumerate(j['motor_mount_holes_local_xy_mm']):
 fasteners[f'motor_M3_shank_{i}']=cyl(1.5,height-(ear_top-2.5),x,y,ear_top-2.5)
 fasteners[f'motor_M3_nut_{i}']=cq.Workplane('XY').center(x,y).polygon(6,6.2).circle(1.5).extrude(2.4).translate((0,0,height-2.5)).val()
def bounds(s):
 b=s.BoundingBox();return [b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax]
solids=cq.importers.importStep(str(O/'complete.step')).solids().vals()
for n,b in j['components'].items():
 if not n.endswith('_servo_reference'):continue
 target=list(b);target[4]+=deck;target[5]+=deck
 match=[s for s in solids if np.allclose(bounds(s),target,atol=.0001,rtol=0)]
 assert len(match)==1,n
 parts[n]=match[0]
hits=[]
for n,s in fasteners.items():
 for nn,p in parts.items():
  a=s.BoundingBox();b=p.BoundingBox()
  if any(min(getattr(a,k+'max'),getattr(b,k+'max'))-max(getattr(a,k+'min'),getattr(b,k+'min'))<=1e-6 for k in 'xyz'):continue
  v=s.intersect(p).Volume()
  if v>.001:hits.append([n,nn,v])
result={'scope':'Nominal box/receiver screws and twelve M3 motor shanks/nuts against printed parts and exported servo references. Motor head allowances are checked in checks.json. Not purchased-fastener fit, tool access or structural acceptance.','collisions_mm3':hits}
result['source_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),O/'checks.json',O/'complete.step',*[O/f'{n}.step' for n in parts if not n.endswith('_servo_reference')]]}
(O/'mount_checks.json').write_text(json.dumps(result,indent=2)+'\n')
assert not hits,hits
print('Box/receiver fasteners and twelve motor shank/nut sets clear printed parts and servo references.')
