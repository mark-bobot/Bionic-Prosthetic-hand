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
           title=f'Forearm-integrated Phoenix — {label} CAD', solid_colors=palette)

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
