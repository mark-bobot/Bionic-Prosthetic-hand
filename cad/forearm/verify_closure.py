"""Simultaneous five-digit closure samples. No tendons, pins or contact dynamics."""
from pathlib import Path
import json
import cadquery as cq
from hand import posed
from thumb_mount import posed_thumb
R=Path(__file__).resolve().parent;O=R/'exports'
check=json.loads((R/'checks.json').read_text())
fixed={}
for n in ['palm_receiver','forearm_lower','forearm_upper']:
 fixed[n]=cq.importers.importStep(str(O/(n+'.step'))).translate((0,0,check['parts'][n]['assembly_zmin_mm']))
records=[]
for step in range(13):
 t=step/12;mcp=60*t;pip=10+60*t;tr=-60-30*t;tp=10+30*t
 hand={**posed(mcp,pip),**posed_thumb(tr,tp)}
 items=list(hand.items());hits=[];max_volume=0
 for i,(n,p) in enumerate(items):
  for nn,q in items[i+1:]+list(fixed.items()):
   a,b=p.val().BoundingBox(),q.val().BoundingBox()
   if any(min(getattr(a,k+'max'),getattr(b,k+'max'))-max(getattr(a,k+'min'),getattr(b,k+'min'))<=1e-5 for k in 'xyz'):continue
   hit=p.intersect(q,clean=False).val()
   assert hit.isValid(),(step,n,nn,'invalid boolean')
   v=max(0,hit.Volume());max_volume=max(max_volume,v)
   if v>.001:hits.append({'parts':[n,nn],'overlap_mm3':v})
 records.append({'step':step,'fraction':t,'MCP':mcp,'PIP':pip,'thumb_root':tr,'thumb_tip':tp,'max_overlap_mm3':max_volume,'collisions':hits})
 print(records[-1],flush=True)
 # Export a useful clear flexion view only; never label an intersecting pose accepted.
 if step==9 and not hits:cq.exporters.export(cq.Compound.makeCompound([p.val() for p in hand.values()]),str(O/'simultaneous_flexion_hand.step'))
result={'scope':'13 simultaneous five-digit samples; MCP 0..60, PIP 10..70, thumb root -60..-90, tip 10..40 degrees. No continuous sweep, tendon, pin, elastic, load or recipient-fit validation.',
 'samples':records,'first_collision_step':next((r['step'] for r in records if r['collisions']),None),'all_samples_clear':all(not r['collisions'] for r in records)}
(R/'closure_checks.json').write_text(json.dumps(result,indent=2)+'\n')
