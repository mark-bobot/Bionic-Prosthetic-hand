# Measure the printed Phoenix hand first

The current design winds two separate grooves on one shaft. It has **no equaliser**. Use this sheet and check_bottom_drive_pull.py for bottom-drive; the older MEASURED-PULL.md describes the earlier differential mechanism.

You have the original Phoenix v3 print, but no extension or wiring. Begin unpowered on a rigid fixture. If pins, tendons or return bands are not installed, complete the original hand assembly first. Confirm correct right-hand orientation, smooth joints and passive reopening. Do not use a person as the fixture.

## Record five individual paths

Use a calibrated force gauge and displacement scale. Pull at the intended drum tangent through the installed route, using actual tendons and return bands. Mark each line at the same repeatable slack-free starting position without pretensioning a finger closed. Record peak force versus displacement, closure travel, and the maximum tested travel that remains within the agreed mechanical load/position limit. Do not find that limit by forcing a hard stop.

Repeat each path at least three times for an initial reproducibility check and retain every trace; this is not durability qualification. Record sticking, routing and return-band configuration. A scale that only latches a steady load may miss breakaway peaks.

With only the printed hand, these are **hand-only measurements**: keep full_route_measured false. Repeat with the complete extension, liners and terminations before accepting the motor calculation. Select the peak over the full proposed common stroke, not merely each finger's first closure point.

Copy bottom_drive_pull_template.json and enter measured values. Missing measurements are null, not zero. For each motor enter its measured effective winding radius, calibrated usable sweep and justified operating torque at the lowest measured loaded rail voltage. The generic owned servos remain unidentified; no torque or voltage has been assigned to them.

Run from the repository root:

    python calculations/check_bottom_drive_pull.py my_measurements.json --output my_result.json

Missing data, unconfirmed setup or failed arithmetic returns exit code 2. SCREEN_PASS returns 0 but never approves hardware or human use.

## What the calculation checks

For a paired drum of effective radius r, the conservative required torque is margin × r × (peak force 1 + peak force 2), using N and metres. The thumb has one term. No extra routing-efficiency factor is applied to full-route gauge readings.

Both grooves take up the same distance. Required common take-up is the larger closure travel; maximum permitted by the supplied measurements is the smaller maximum-tested travel. Those must overlap and fit within r × usable angle (radians). Set each line length at the same open pose; arbitrary slack is not a substitute for travel compatibility.

For example only, closure travels 22 and 30 mm with tested maxima 25 and 32 mm have no common interval: the first finger would exceed its tested travel before the second closes. A torque calculation alone must not pass this pair.

Even an interval that passes during free closure cannot accommodate every object contact. Test asymmetric contact on a rigid object fixture. If one finger blocks and the other remains open or force rises excessively, reduce the accepted task/command range or redesign the transmission; do not raise torque until it moves.

Keep one-layer winding and measure radius at maximum take-up. Any changed line diameter, knot, return band, route, groove, horn or mechanical limit requires an updated screen and affected bench tests.
