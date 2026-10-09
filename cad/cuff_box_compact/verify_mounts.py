"""Check nominal fastener allowances against the exported print solids."""
from pathlib import Path
import json,hashlib
import cadquery as cq
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
hits=[]
for n,s in fasteners.items():
 for nn,p in parts.items():
  v=s.intersect(p).Volume()
  if v>.001:hits.append([n,nn,v])
result={'scope':'Nominal screw shanks and heads against exported printed parts only; not identified purchased screws, nuts, access sweeps or structural acceptance. Box screws are countersunk; receiver screws have cylindrical heads.','collisions_mm3':hits}
result['source_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),O/'checks.json',*[O/f'{n}.step' for n in parts]]}
(O/'mount_checks.json').write_text(json.dumps(result,indent=2)+'\n')
assert not hits,hits
print('Six nominal mounting screw allowances clear exported printed parts.')
