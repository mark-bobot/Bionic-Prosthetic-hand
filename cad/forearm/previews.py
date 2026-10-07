"""Render exported geometry, including a lower service view of the electronics."""
from pathlib import Path
import json, sys
import cadquery as cq
import numpy as np
R = Path(__file__).resolve().parent
O = R / 'exports'
sys.path.insert(0, str(R.parent / 'bionic'))
from render import render
report = json.loads((R / 'checks.json').read_text())

def bounds(s):
    b = s.BoundingBox()
    return [b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax]

palette = []
for name, info in report['components'].items():
    color = [65,77,88]
    if name.startswith('spool'): color = [202,167,95]
    if name in ['Nano', 'EMG_conditioner']: color = [72,155,119]
    if name == 'battery': color = [220,167,73]
    if name == 'logic_regulator': color = [146,118,169]
    palette.append({'bounds': info['bounds_mm'], 'color': color})
for label in ['complete', 'open']:
    render(O / f'{label}_forearm.step', O / f'{label}_preview.png',
           title=f'Phoenix v3 · 0.4.3 — {label} · corrected fingertips', solid_colors=palette, view=(-145,28))

omit = []
for name in ['forearm_lower', 'forearm_upper', 'electronics_tray']:
    p = cq.importers.importStep(str(O / f'{name}.step')).translate(
        (0, 0, report['parts'][name]['assembly_zmin_mm']))
    omit.append(bounds(p.val()))
assembly = cq.importers.importStep(str(O / 'complete_forearm.step'))
keep = [s for s in assembly.solids().vals()
        if not any(np.allclose(bounds(s), b, atol=.001, rtol=0) for b in omit)]
cq.exporters.export(cq.Compound.makeCompound(keep), str(O / 'lower_service_view.step'))
render(O / 'lower_service_view.step', O / 'electronics_preview.png',
       title='Lower service view — shells and electronics tray removed',
       solid_colors=palette, view=(-35,-28))

# Close-up keeps the native thumb attachment visible from the thumb side.
from hand import models
from thumb_mount import posed_thumb
hand_parts={**models,**posed_thumb()}
cq.exporters.export(cq.Compound.makeCompound([p.val() for p in hand_parts.values()]),str(O/'hand_layout.step'))
render(O/'hand_layout.step', O/'hand_layout_preview.png',
       title='Phoenix v3 — corrected fingertip orientation', view=(-145,28))

# This pose passed the simultaneous closure check; it is not a loaded grip.
closure=json.loads((R/'closure_checks.json').read_text())
assert not closure['samples'][9]['collisions']
render(O/'simultaneous_flexion_hand.step', O/'flexion_preview.png',
       title='Phoenix v3 · 0.4.3 — sampled five-digit flexion', view=(-145,28))

# Check the complete assembly against the same hand used in the close-up.
from verify_assembly import verify
verify()
