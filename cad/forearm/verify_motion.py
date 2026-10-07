"""Discrete CAD checks, not a swept-motion or physical acceptance test."""
from pathlib import Path
import json
import cadquery as cq
from hand import posed

R = Path(__file__).resolve().parent
O = R / 'exports'
report = json.loads((R / 'checks.json').read_text())

def part(name):
    return cq.importers.importStep(str(O / (name + '.step'))).translate(
        (0, 0, report['parts'][name]['assembly_zmin_mm']))

fixed = {name: part(name) for name in [
    'forearm_lower', 'forearm_upper', 'internal_tendon_base',
    'internal_tendon_cover', 'palm_receiver']}
# Low-profile M3 head allowances on the cassette floor; hardware is not in the preview.
for x in [-30, 30]:
    for y in [-82, -26]:
        fixed[f'cassette_screw_head_{x}_{y}'] = (cq.Workplane('XY').circle(3)
            .extrude(2).translate((x, y, 8)))
eq = cq.importers.importStep(str(R.parent / 'exports/pair_equaliser.step'))
records = []
for x in [-16, 16]:
    for y in [-74, -55, -36]:
        for angle in [-30, 0, 30]:
            moving = eq.rotate((0, 0, 0), (0, 0, 1), angle).translate((x, y, 9))
            records.append({'part': 'equaliser', 'x_mm': x, 'y_mm': y,
                            'angle_deg': angle, 'overlap_mm3': {
                                n: moving.intersect(p).val().Volume() for n, p in fixed.items()}})
for y in [-74, -55, -36]:
    moving = part('thumb_slider').translate((0, y + 37, 0))
    records.append({'part': 'thumb_slider', 'y_mm': y, 'overlap_mm3': {
        n: moving.intersect(p).val().Volume() for n, p in fixed.items()}})

# Check both shell halves against the reserved residual-limb space.
lumen = (cq.Workplane('XY').ellipse(35, 32).workplane(offset=137)
         .ellipse(27, 25).loft(ruled=True)
         .rotate((0, 0, 0), (1, 0, 0), -90).translate((0, -297, 8)))
lumen_checks = {n: fixed[n].intersect(lumen).val().Volume()
                for n in ['forearm_lower', 'forearm_upper']}

# This modest flexion pose is the accepted illustration, not full closure.
hand = posed(45, 15)
items = list(hand.items())
partial = []
for i, (n, p) in enumerate(items):
    for nn, q in items[i + 1:] + list(fixed.items()):
        a, b = p.val().BoundingBox(), q.val().BoundingBox()
        if any(min(getattr(a,k+'max'),getattr(b,k+'max')) -
               max(getattr(a,k+'min'),getattr(b,k+'min')) <= 1e-5 for k in 'xyz'):
            continue
        v = p.intersect(q).val().Volume()
        if v > .001:
            partial.append([n, nn, v])
out = {'scope': '21 discrete mechanism poses; 38 mm end-to-end travel; not a continuous sweep',
       'mechanism_poses': records, 'shell_lumen_overlap_mm3': lumen_checks,
       'partial_finger_pose_degrees': {'MCP': 45, 'PIP': 15},
       'partial_finger_collisions': partial,
       'full_flexion_accepted': False,
       'full_flexion_note': 'Correctly rolled tips checked at discrete bends; full closure still requires tendon, pin, return-band, stop and load validation.'}
(R / 'motion_checks.json').write_text(json.dumps(out, indent=2) + '\n')
failed = [r for r in records if max(r['overlap_mm3'].values()) > .001]
print(json.dumps({'failed_mechanism_poses': failed, 'shell_lumen_overlap_mm3': lumen_checks,
                  'partial_finger_collisions': partial}, indent=2), flush=True)
assert not failed and not partial and max(lumen_checks.values()) < .001
