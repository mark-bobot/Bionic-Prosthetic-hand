"""Analytical scenarios for the separate box; no measured motor or wearer claims."""
from pathlib import Path
import json
import math

HERE = Path(__file__).resolve().parent
report = json.loads((HERE / 'exports/checks.json').read_text())
radius_m = report['transmission']['effective_radius_mm'] / 1000
profile = report['profile']
crown = profile['cuff_axis_z_mm'] + profile['formed_cuff_outer_radius_mm']
port_heights_m = [(report['box_deck_global_z_mm'] + p['z_mm'] - crown) / 1000
                  for p in report['ports_local_mm']]
rows = []
for force in [5, 10, 15]:
    for efficiency in [0.4, 0.6, 0.8]:
        line_force = force / efficiency
        moment = sum(port_heights_m) * line_force
        rows.append(dict(hand_tendon_force_each_N=force, routing_efficiency=efficiency,
                         paired_motor_torque_Nm=2 * radius_m * line_force,
                         thumb_motor_torque_Nm=radius_m * line_force,
                         total_box_exit_pull_N=5 * line_force,
                         idealised_pitch_moment_Nm=moment,
                         equivalent_33mm_support_couple_N=moment / 0.033))
result = dict(scope='Assumed equal tensions on five hand tendons; not fingertip forces or measured capability.',
              model='Quasistatic, one cord layer, constant routing efficiency, simultaneous pull. Pitch example: all cords parallel to forearm at exit; reference is nominal cuff crown.',
              limitations='Excludes acceleration, return-band variation, tissue compliance, local pressure, friction changing with angle, servo heating, knots and actual attachment geometry. The 33 mm couple is not strap tension or a rating.',
              effective_radius_mm=radius_m * 1000,
              assumed_stall_label_kgcm=25,
              assumed_stall_label_Nm=25 * 0.0980665,
              stall_label_verified=False,
              operating_voltage_V=None,
              rows=rows)
(HERE / 'exports/force_scenarios.json').write_text(json.dumps(result, indent=2) + '\n')
lines = ['# Separate-box force and mounting scenarios', '',
         'These are calculated requirements for assumed tendon loads, not proof that the unidentified servos can provide them continuously. Tendon force is not fingertip force. No supply voltage is inferred from a generic motor label.', '',
         'At effective drum radius `r = 0.0123 m`, hand tendon force `F` and assumed routing efficiency `eta`: `T_box = F/eta`, `torque_pair = 2*r*F/eta`, and `torque_thumb = r*F/eta`. Efficiency scenarios cover transmission losses; they are not measured coefficients. Measure each finger through its complete bend and reopening cycle.', '',
         '| Hand tendon load, each | Efficiency | Pair torque | Thumb torque | Total exit pull, five cords |',
         '| ---: | ---: | ---: | ---: | ---: |']
for row in rows:
    lines.append(f"| {row['hand_tendon_force_each_N']} N | {row['routing_efficiency']:.0%} | {row['paired_motor_torque_Nm']:.3f} Nm | {row['thumb_motor_torque_Nm']:.3f} Nm | {row['total_box_exit_pull_N']:.1f} N |")
example = next(row for row in rows if row['hand_tendon_force_each_N']==10 and row['routing_efficiency']==0.6)
lines += ['', '## Why the attachment matters', '',
          f"For the 10 N / 60% example, simultaneous pulling creates {example['total_box_exit_pull_N']:.1f} N at the five enclosure exits. With the cords hypothetically parallel to the forearm, the current exit heights give about **{example['idealised_pitch_moment_Nm']:.2f} Nm** around the nominal cuff crown. Reacting that only as a couple across the two strap stations (33 mm apart) corresponds to **{example['equivalent_33mm_support_couple_N']:.0f} N**. This is an illustrative load path, not a prediction of strap tension, skin pressure or actual use.", '',
          'The example is enough to rule out assuming that two straps make a secure wearable attachment. First support the box and palm on a rigid bench fixture, identify the actual cord directions and measure loads. A fitted socket, neutral wrist restraint and load-spreading attachment need separate design and verification before worn powered use. Making the straps tighter is not a substitute for that work.', '',
          'A claimed 25 kg·cm stall label converts to 2.45 Nm, but it is unverified and is not a continuous rating. No working-torque fraction is asserted here. Check the identified motor specifications, then measure current, temperature, release behaviour and travel under the actual loads. The ideal 160° travel is 34.35 mm; it does not establish full hand closure.', '',
          '## Minimum measurement procedure', '',
          '1. Hold the palm and cuff at a fixed wrist angle in a rigid bench fixture, with power disconnected.',
          '2. Pull one original cord using a force gauge or a spring scale with a suitable range. Record force and displacement from fully open to the intended closed position, including the peak. Keep fingers clear of pinch points.',
          '3. Repeat with the final guides and liners. Test paired cords together; check both free motion and one finger contacting an object first. Fixed coupled drums do not adapt independently.',
          '4. Measure the actual motor case, ears, shaft, horn, lead exit and rated supply. Compare measured requirements with verified motor data before selecting the power supply.',
          '5. Start powered bench trials at limited travel with a reachable disconnect and a way to slacken the tendons manually. Loss of power alone may not release the geared servos.', '',
          'Reproduce with `python cad/cuff_box/force_check.py`. Geometry comes from the current CAD check report; the 33 mm strap spacing follows this design revision. JSON results are in `exports/force_scenarios.json`.', '']
(HERE / 'FORCES.md').write_text('\n'.join(lines))
