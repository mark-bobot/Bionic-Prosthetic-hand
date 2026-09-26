"""Small fit prints before the full enclosure. CC BY 4.0. Run after integrate.py."""
from pathlib import Path
import json
import cadquery as cq
import trimesh
R=Path(__file__).resolve().parent; O=R/'exports'
def box(l,w,h,x=0,y=0,z=0):
 return cq.Workplane('XY').box(l,w,h,centered=(True,True,False)).translate((x,y,z))
carrier=cq.importers.importStep(str(O/'servo_carrier.step'))
pocket=carrier.intersect(box(54,38,16,0,-34)).translate((0,34,0))
# Same hole and nut trap as the lid bosses, accessible from below.
fastener=box(16,16,4).cut(cq.Workplane('XY').circle(1.7).extrude(5))
fastener=fastener.cut(cq.Workplane('XY').polygon(6,6.6).extrude(2.5))
# Same 3 mm panel thickness and reference switch cut-outs as lid.
switches=box(44,26,3)
for x,d in [(-11,12.2),(11,6.2)]:
 switches=switches.cut(cq.Workplane('XY').center(x,0).circle(d/2).extrude(4))
report={}
for n,p in [('servo_fit_coupon',pocket),('nut_fit_coupon',fastener),('switch_fit_coupon',switches)]:
 assert len(p.solids().vals())==1 and p.val().isValid()
 cq.exporters.export(p,str(O/f'{n}.step'))
 cq.exporters.export(p,str(O/f'{n}.stl'),tolerance=.08,angularTolerance=.15)
 m=trimesh.load_mesh(O/f'{n}.stl');assert m.is_watertight and m.volume>0
 report[n]={'size_mm':m.extents.tolist(),'watertight':True,'volume_mm3':float(m.volume)}
(R/'coupon_checks.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
