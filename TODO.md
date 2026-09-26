# Remaining work

## First: establish whether the owned servo works
- [ ] Identify servo model and allowable supply voltage; verify nominal torque and 180° variant.
- [ ] Follow [the tendon test](TENDON-TEST.md): measure each finger's travel and maximum pull with return elastics installed.
- [ ] Measure the paired load through the intended routing, including intended contact load.
- [ ] Select drum radius from travel and rerun [servo sizing](SERVO-SIZING.md).
- [ ] Test both fingers for motion, current, supply sag, heating and intended hold duration.
- [ ] Resolve unequal travel/contact using appropriate coupling, compliance or limits.

## Compact packaging and parts
- [x] Match the DFRobot dry-electrode sensor to catalogue SKU SEN0240 and select the classic Arduino Nano.
- [ ] Check the physical sensor connector labels before wiring.
- [ ] Set hand scale, maximum enclosure dimensions and target mass.
- [ ] Decide actuator count and which fingers are paired; decide whether a display is needed.
- [ ] Lay out servos, spools, controller, sensor board, power and cables in CAD.
- [ ] Complete [BOM](BOM.md) quantities, supplier quotations and total cost.
- [ ] Size power regulation, battery capacity, wiring and protection from measured demand.

## Implementation
- [ ] Publish modified editable CAD and printable files with upstream attribution.
- [ ] Publish the actual wiring diagram.
- [ ] Implement calibrated EMG processing appropriate to the sensor output; distinguish raw averaging from envelope smoothing.
- [ ] Implement deliberate reopening, start-up behaviour, travel limits and loss-of-signal behaviour.
- [ ] Preserve third-party notices for any reused firmware/library.
- [ ] Identify any recreated files as new reconstructions.

## Evidence and release
- [ ] Record electrode-contact improvement with a controlled comparison.
- [ ] Record raw/processed EMG signals and control response delay.
- [ ] Publish torque calculations populated with measured forces, geometry and voltage.
- [ ] Record a demonstration of both paired fingers and the rest of the hand.
- [ ] Publish build instructions, assembly photos, limitations and test results.
- [ ] Check each project claim against the released implementation; revise unsupported wording.
