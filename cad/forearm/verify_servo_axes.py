"""Compare shaft and drum axes recovered from exported STEP cylindrical faces."""
from pathlib import Path
import json,math,hashlib
import cadquery as cq
R=Path(__file__).resolve().parent;O=R/'exports'
report=json.loads((R/'checks.json').read_text())
solids=cq.importers.importStep(str(O/'complete_forearm.step')).solids().vals()
def bounds(s):
 b=s.BoundingBox();return [b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax]
def component(name):
 target=report['components'][name]['bounds_mm']
 found=[s for s in solids if max(abs(a-b) for a,b in zip(bounds(s),target))<1e-4]
 assert len(found)==1,(name,len(found));return found[0]
def axis_xy(s,radius):
 axes=[]
 for f in s.Faces():
  if f.geomType()!='CYLINDER':continue
  c=f._geomAdaptor().Cylinder();a=c.Axis()
  if abs(c.Radius()-radius)<1e-4 and abs(a.Direction().Z())>.999999:
   q=a.Location();axes.append((q.X(),q.Y()))
 assert axes
 assert all(math.dist(axes[0],q)<1e-4 for q in axes)
 return axes[0]
rows=[]
for i in range(3):
 servo=component('servo_'+str(i));spool=component('spool_'+str(i))
 shaft_axis=axis_xy(servo,2.95);drum_axis=axis_xy(spool,12)
 error=math.dist(shaft_axis,drum_axis)
 assert error<1e-4,(i,error)
 gap=spool.BoundingBox().zmin-servo.BoundingBox().zmax
 rows.append({'servo':i,'shaft_axis_xy_mm':shaft_axis,'spool_axis_xy_mm':drum_axis,'axis_error_mm':error,'shaft_top_to_spool_base_mm':gap})
(R/'servo_axis_checks.json').write_text(json.dumps({'assembly_sha256':hashlib.sha256((O/'complete_forearm.step').read_bytes()).hexdigest(),'scope':'Exported axes only; the metal horn, fixing hardware, cable bends and actual servo fit remain unvalidated.','rows':rows},indent=2)+'\n')
print(json.dumps(rows,indent=2),flush=True)
