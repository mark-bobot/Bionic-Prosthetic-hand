# Before any human testing

**Status on 10 October 2026: HOLD.** The user reports an original Phoenix v3 hand print only. The bionic extension is not printed and the system is not wired. No physical test result, motor identification or wearer-specific fit has been supplied.

This is the working sequence for one intended wearer with a right missing hand. It separates work you can do now from decisions requiring an assembled fixture and a qualified prosthetic-fitting professional. The current arm adapter is a geometric candidate, not a prescribed socket.

## 1. What you can do now — no electronics needed

1. Inspect the original right-hand print against its source instructions. Record scale, material, print orientation, joint pins and any cracks or rough bearing surfaces.
2. Assemble the native hand joints, return bands and five tendon paths if not already assembled. Secure the palm on a rigid fixture. Check opening and closing manually without binding.
3. Measure each finger's force and travel using [the bottom-drive worksheet](../calculations/BOTTOM-DRIVE-PULL.md). Save repeated raw readings and photos. Label these hand-only results; they omit the extension's friction.
4. Identify the three servos using their case label and original order details. Measure body, mounting ears, shaft, horn and fastener stack. A “25 kg·cm” label does not establish voltage, dimensions or operating torque.
5. Compare those measurements with the selected FT5425BL candidate. The bottom-drive housing is not a verified fit for the owned generic servos. If they differ, revise the housing before printing.

Do not print the full extension merely to meet the current CAD dimensions. Start with measured motor/horn fit and representative mounting coupons. Hand-only force results can reject an unsuitable candidate early, but cannot establish the final motor margin.

## 2. Freeze the assembly and test criteria

The responsible engineer and fitting professional must agree intended tasks and limits before qualification: permitted loads/travel, speed, grip-release force/time, skin-contact temperature, power behaviour, duty cycle, structural proof/fatigue loads, cycle count and wear limits. Leave unknowns blank in the [test record](../release/production/bench_record_template.json); blank does not mean passed.

Complete the BOM with exact purchased parts and revisions: motors, metal horns, screws/retainers, tendon/liners/returns, regulator, power protection, disconnect, connectors, wire sizes, battery/BMS, band/backing and insulation. Record drawings, ratings, source evidence and measured sizes. Do not select a larger fuse to work around an unexplained trip.

Plan the complete load path through drum, motor ears, structural cover, case mounts, receiver, palm axle, stops, straps and socket. Specify print process and representative test articles. The original Phoenix wrist-powered gauntlet is not automatically suitable for a missing-hand conversion.

## 3. Mechanical fixture qualification

With the extension fitted to a rigid arm-shaped fixture and all power disconnected:

- Verify actual horn/fastener fit, engagement and retention. The paired drum's M2 hardware has only 0.6 mm nominal floor clearance under the stated head allowance. Measure it through full travel and under the agreed load; nominal CAD clearance is not acceptance.
- Check five complete tendon routes, terminations, one-layer winding, continuous motion, pinch points and reopening. Run the paired-travel screen on full-route readings.
- Restrain palm rotation with the actual stops and retention strap; the axle alone is a hinge.
- Verify the structural cover, printed motor posts, arm mounts and receiver with agreed load tests. Inspect deformation, cracks and fastener movement; retain measurements.
- Test simultaneous and asymmetric contact on objects/fixtures. Fixed two-groove pairs are not adaptive differentials.
- Resolve cable access and strain relief using [EMG mounting](EMG-MOUNTING.md). No body is needed to test plug fit, cover removal or snag clearance.

### Mechanical release is an unresolved design blocker

No validated release mechanism is currently included. Software disarm, signal detach and main power-off are insufficient because geared motors can resist opening. Before powered fitting, provide an externally accessible means to unload the five tendon paths without opening the motor cover, touching pinch points, requiring a motor to turn, or asking the wearer to pull against the grip.

A competent mechanical designer must choose and detail the release based on measured tendon loads and achievable access. Test it with power removed, a mechanically immobilised motor shaft and a downstream tendon jam on fixtures. Demonstrate actual finger opening and object release, not just movement of a lever. If a jam prevents opening, the mechanism fails that case. Verify retention during normal use and access in the prescribed fitted position. No release-time or load rating is claimed here.

Do not improvise a live jam with hands in the mechanism, or cut a loaded tendon near a person as the planned emergency procedure.

## 4. Electrical commissioning — all electrodes off people

Use the updated [wiring specification](WIRING.md), labelled harness and recorded component ratings. Keep motor plugs disconnected initially.

1. Inspect continuity, polarity, insulation and absence of shorts. Verify regulated outputs on dummy loads before connecting boards.
2. Check the output-disabled firmware and sensor signal path using an appropriate test source. Measure the regulator under its real load.
3. Only on the fixture, set SERVO_OUTPUTS_ENABLED true for unloaded motor commissioning. Start with horns/tendons removed. Confirm each motor direction and safe endpoints; inversion changes the required winding direction.
4. Confirm startup/restart with S2 held cannot enable pulses. Release S2 for at least 50 ms after calibration, then hold it and allow a relaxed input before commanding closure. Check disarm, timing fault, ADC fault and timeout.
5. Attach loose tendons and increase the agreed command range gradually. Measure voltage/current at the actual motor and logic connectors, including simultaneous motion. Check overshoot, sag, return-current interference, inrush, connector and enclosure temperatures.
6. Exercise input disconnects, frozen input, plausible noise, brownout, restart and control loss under a defined fixture fault plan. Record actual behaviour. The ADC check does not reliably identify lost skin contact; the software has no force, current or temperature feedback.
7. Demonstrate both electrical disconnect and independent mechanical release. Retest affected cases after any revision.

The software's nominal 1 kHz sample rate must be measured on the board. Do not infer timing, servo response or force from a successful compile. Routine host tests model logic only.

## 5. Repeatability and durability

Run the pre-agreed load and duty sequence with representative objects and all five routes installed. Record cycle count, currents, temperatures, force/travel changes, failures, screw movement and wear. Include release tests before and after the run. Replace worn components and document any design change; rerun affected checks on the final configuration.

An arbitrary “100 cycles passed” is not a life or clinical claim. Acceptance criteria and intended service interval must be justified before the test.

## 6. Professional review before connecting or fitting a person

Provide the actual build/BOM, code revision, fixture evidence, hazards and unresolved issues to the fitting professional and responsible manufacturer/engineer. They must establish the wearer's residual-limb interface, suspension, alignment, available muscle site, skin-contact materials, cable routing and trial protocol. Confirm applicable obligations and consent/process for the intended trial.

A record that is complete on paper is not authorisation. A sensor-only session is still human testing. If approved, the first signal assessment should have all servo connectors physically removed and output-disabled firmware. Unpowered fitting and later powered functional trials are separate decisions with agreed supervision, stop conditions and follow-up.

Powered trials must not proceed while mechanical release, power protection, structural evidence, signal-control limitations or fitting remain unresolved. This repository cannot substitute for those reviews.

## Results and handoff

Use bench_record_template.json as a blank record; attach actual raw measurements, photos, hardware lots, code/build hashes, instruments and reviewer identity. Keep failures and revisions. All entries initially read NOT_RUN. The existing readiness.json gates remain OPEN until supported evidence is reviewed; do not mark them complete because instructions exist.

The immediate next action is the unpowered five-finger force/travel measurement in section 1, followed by motor identification. That determines whether the proposed extension should be printed at all.
