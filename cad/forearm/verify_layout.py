"""Source-derived hinge alignment and discrete original-thumb assembly checks."""
from pathlib import Path
import hashlib,json,math
import cadquery as cq
import hand
from thumb_mount import posed_thumb,thumb_root,axis,inner_faces,receiver
R=Path(__file__).resolve().parent

def overlap(a,b):
 aa,bb=a.val().BoundingBox(),b.val().BoundingBox()
 if any(min(getattr(aa,k+'max'),getattr(bb,k+'max'))<=max(getattr(aa,k+'min'),getattr(bb,k+'min')) for k in 'xyz'):return 0.
 hit=a.intersect(b,clean=False).val()
 assert hit.isValid(),'Invalid intersection result'
 return max(0.,hit.Volume())

# The thumb's original pin line and the transformed proximal pin line coincide.
root=cq.Vector(*thumb_root)+cq.Vector(hand.X,hand.Y,hand.ZMIN)
assert inner_faces[0]<root.dot(axis)<inner_faces[1]
records=[]
for angle in [-60,-70,-80,-90]:
 for tip in [0,15]:
  moving=posed_thumb(angle,tip);p,d=moving.values()
  checks={'proximal_to_palm':overlap(p,hand.palm),'distal_to_palm':overlap(d,hand.palm),
          'proximal_to_distal':overlap(p,d),'proximal_to_support':overlap(p,receiver),
          'distal_to_support':overlap(d,receiver)}
  records.append({'root_degrees':angle,'tip_degrees':tip,'overlap_mm3':checks})
  print(records[-1],flush=True)
report={'source_step_sha256':hashlib.sha256(hand.source.read_bytes()).hexdigest(),
 'thumb_root_mm':thumb_root,'thumb_axis':axis.toTuple(),'thumb_fork_clear_gap_mm':inner_faces[1]-inner_faces[0],
 'thumb_display_pose_degrees':{'root':-60,'tip':0,'yaw':130},
 'finger_order':['short index','long middle','long ring','short little'],
 'original_palm_and_digit_shapes_modified':False,'additional_thumb_fork_removed':True,
 'sampled_thumb_poses':records,'scope':'Discrete samples only; no pins, tendons, return bands, loads, or fitted anatomy; not full opposition acceptance'}
(R/'layout_checks.json').write_text(json.dumps(report,indent=2)+'\n')
assert all(max(r['overlap_mm3'].values())<.001 for r in records),'Sampled thumb pose fails'
