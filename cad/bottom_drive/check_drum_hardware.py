"""Swept clearance for explicitly constrained M2 drum-head projections."""
from pathlib import Path
import json,hashlib
import cadquery as cq
R=Path(__file__).resolve().parent;O=R/'exports'
j=json.loads((O/'checks.json').read_text())
base=cq.importers.importStep(str(O/'box_base.step')).val()
rows=[]
for name,b in j['components'].items():
 if not name.endswith('_spool'):continue
 x=(b[0]+b[1])/2;y=(b[2]+b[3])/2;z=b[4]
 # Two holes at 8 mm radius, 4.5 mm diameter heads, <=1.2 mm projection.
 sweep=cq.Workplane('XY').center(x,y).circle(10.25).circle(5.75).extrude(1.2).translate((0,0,z-1.2)).val()
 v=sweep.intersect(base).Volume()
 rows.append({'drum':name,'swept_head_base_intersection_mm3':v,'nominal_lowest_head_z_mm':z-1.2,'nominal_floor_clearance_mm':z-1.2-4})
 assert v<.001,(name,v)
result={'scope':'Geometric sweep against case base only, using assumed 4.5 mm diameter heads at 8 mm radius and maximum 1.2 mm projection. Not identification of actual screws or horn fit. Tolerance/deflection not included.',
 'required_maximum_head_projection_mm':1.2,'rows':rows,
 'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),O/'checks.json',O/'box_base.step']}}
(O/'drum_hardware_checks.json').write_text(json.dumps(result,indent=2)+'\n')
print('Projected drum-head sweeps clear base; minimum nominal clearance:',min(r['nominal_floor_clearance_mm'] for r in rows),'mm')
