"""Compare exported CAD bounds; this is not a volume or patient-fit comparison."""
from pathlib import Path
import json
import cadquery as cq
R = Path(__file__).resolve().parents[2]
out = {}
for name, path in [('previous', 'cad/slim/exports/complete_slim_candidate.step'),
                   ('current', 'cad/forearm/exports/complete_forearm.step')]:
    shape = cq.importers.importStep(str(R / path))
    b = cq.Compound.makeCompound(shape.solids().vals()).BoundingBox()
    out[name] = {'file': path, 'whole_assembly_bounds_mm':
                 [b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax], 'maximum_depth_mm': b.zlen}
out['depth_reduction_percent'] = 100 * (1 - out['current']['maximum_depth_mm'] /
                                      out['previous']['maximum_depth_mm'])
out['scope'] = 'CAD bounding depth in common assembly axes; different assumed socket length; not a volume or patient-fit comparison.'
(R / 'cad/forearm/envelope_comparison.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
