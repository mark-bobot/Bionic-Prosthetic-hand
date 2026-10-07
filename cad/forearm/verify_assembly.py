"""Reject a complete/open assembly containing stale hand placement."""
from pathlib import Path
import hashlib,json
import cadquery as cq
import numpy as np
from hand import models
from thumb_mount import posed_thumb
R=Path(__file__).resolve().parent
O=R/'exports'

def signature(shape):
 b=shape.BoundingBox();c=shape.Center()
 return np.array([b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax,c.x,c.y,c.z,shape.Volume()])

def verify():
 expected={**models,**posed_thumb()}
 result={'scope':'11 original hand solids matched by bounds, centre of mass and volume to current source placements; detects stale/inverted digit exports','tolerances':{'bounds_mm':.0001,'centre_mm':.005,'volume_relative':.0005,'reason':'STEP reimport changes numerical mass integration slightly; bounding placements must still agree tightly.'},'assemblies':{}}
 for name in ['complete_forearm','open_forearm','hand_layout']:
  path=O/(name+'.step');solids=cq.importers.importStep(str(path)).solids().vals()
  actual=[signature(s) for s in solids]
  matched={}
  for part,shape in expected.items():
   wanted=signature(shape.val());found=[i for i,v in enumerate(actual)
    if np.allclose(wanted[:6],v[:6],rtol=0,atol=1e-4)
    and np.allclose(wanted[6:9],v[6:9],rtol=0,atol=.005)
    and np.isclose(wanted[9],v[9],rtol=.0005,atol=.001)]
   assert len(found)==1,(name,part,found)
   matched[part]=found[0]
  assert len(set(matched.values()))==len(expected)
  result['assemblies'][name]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'matched_solids':matched}
 result['source_sha256']={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in ['hand.py','thumb_mount.py','servo_reference.py','build.py','previews.py','verify_assembly.py']}
 result['preview_sha256']={n:hashlib.sha256((O/n).read_bytes()).hexdigest() for n in ['complete_preview.png','open_preview.png','electronics_preview.png','hand_layout_preview.png','flexion_preview.png']}
 (R/'assembly_checks.json').write_text(json.dumps(result,indent=2)+'\n')
 print('Verified all 11 hand solids in complete, open and hand-detail exports.',flush=True)
 return result
if __name__=='__main__':verify()
