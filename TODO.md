# Remaining work

## Files completed
- [x] Select classic Nano and SEN0240; set three groups: thumb, index/middle, ring/little.
- [x] Write simple EMG control firmware and retain OYMotion notices.
- [x] Compile for Nano and test control logic on the host.
- [x] Draw proposed wiring and list power/protection components.
- [x] Import official Phoenix STEP; preserve original geometry.
- [x] Create editable carrier, spool, fairlead and equaliser CAD; export STEP/STL.
- [x] Create the reference BOM with quantities and explicit cost allowances.

- [x] Add an integrated electronics/battery enclosure, lid, switches and strap station; export checked reference geometry.

## Before connecting loaded tendons
- [ ] Select exact battery, switches, fuse holder and connector sizes; update assumed CAD envelopes.
- [ ] Check board headers, USB alignment, switch threads and wire service loops against the physical components.
- [ ] Identify actual servo voltage range, spline, body dimensions and connector pinout.
- [ ] Print a test fit; check horn bolts, cable exits, ties and clearances.
- [ ] Measure tendon force and travel using [TENDON-TEST.md](TENDON-TEST.md).
- [ ] Rerun torque sizing for the actual line radius and equaliser routing.
- [ ] Check supply voltage, polarity, fuse/wire ratings and regulator temperature.
- [ ] Calibrate pulse endpoints with horns/tendons disconnected, then loose tendons.

## Hardware validation
- [ ] Verify sampling timing, relaxed/contraction separation and motor-noise immunity.
- [ ] Test reopening, arming, timeout and faults; establish manual tendon release.
- [ ] Check paired-finger contact, equaliser travel and line wear.
- [ ] Measure current, heating and performance over repeated cycles and intended holding duration.
- [ ] Choose hand scale and design a proper cuff; validate retention and cooling in the new enclosure.
- [ ] Record cost quotations, final assembly photos, test data and demonstration video.
- [ ] Review historical project claims separately from results of this reconstruction.

## Superseded custom-hand study (revision C)
- [x] Generate new palm, two-joint fingers, opposed thumb, wrist plate and compact housing CAD.
- [x] Check printable solids, component clashes and sampled finger/thumb motion.
- [ ] Confirm left/right hand, amputation level, residual-limb dimensions and socket/interface requirements with the intended user and prosthetist.
- [ ] Complete constrained tendon routing, equaliser mounts and service access.
- [ ] Establish joint stops, return-elastic preload, friction and required tendon travel on one finger.
- [ ] Verify real servo ears, horns, battery, switches and cable bends in the compact enclosure.
- [ ] Validate wrist fasteners, housing cooling and load retention on a bench before fitting.

## Current Phoenix v3 adaptation
- [x] Add right-arm open saddle and independent EMG-band carrier using the published electrode board outline.
- [ ] Replace placeholder lumen with assessed right residual-limb/socket geometry; resolve anatomical length, suspension, liner and skin-pressure requirements.
- [ ] Measure electrode package thickness/contact protrusion and verify its independent soft retention and cable route.
- [x] Remove the unused spool groove and lower maximum enclosure height to 60 mm; calculate force/travel at the retained radius.
- [ ] Verify thinner-spool horn bolts, tendon anchors and 2.75 mm nominal roof clearance; measure force/travel through the complete routing.
- [x] Round the housing corners, lower the rear roof and recess the controls/cover screws.
- [ ] Slice the curved lid with suitable supports; test thin screw seats, actual low-profile heads and both fastener lengths.
- [x] Restore original Phoenix v3 palm, finger and pin geometry as the selected hand.
- [x] Export original source parts and add a wrist-pivot cradle study for the compact housing.
- [ ] Right side confirmed; confirm Phoenix scale and residual-limb requirements and socket/interface dimensions.
- [ ] Verify the original thumb orientation against the official assembly guide; remove the exploded-view offset only after confirming fit.
- [ ] Select and verify wrist axle/retention, and complete a neutral-position wrist lock.
- [ ] Complete servo-to-Phoenix tendon routing and restrained paired-finger equalisers.
- [ ] Verify original joints, tendon forces/travel, motor limits, enclosure fit and loaded assembly on a bench.

## Integrated bionic CAD — prototype 0.2
- [x] Read current personal-statement v4 and retain its architecture.
- [x] Add closed distal shell, removable ventral door and electrode access.
- [x] Add a palm receiver and connected thumb fork; retain source palm/finger shapes.
- [x] Add constrained equaliser cassette, thumb-line slider, real guide ports and wrist liner comb.
- [x] Add dedicated housing liner entries and reinforced cassette-bearing seats.
- [x] Expose the simple 32-sample averaging helper; compile Nano firmware and rerun host control/filter tests.
- [ ] Choose actual thumb shoulder axle, wrist axle/retainers, clamp supports, inserts and fastener lengths; physically verify joint play and retention.
- [ ] Install and measure flexible-line paths, slack, bends, equaliser differential travel and accessible manual release.
- [ ] Test original finger articulation and the new thumb mount throughout the required motion on a bench.
- [ ] Fit the socket/suspension/liner to measured right residual-limb anatomy and verify EMG contact and skin pressure.
- [ ] Measure actual closure/contact forces, noise, heating, grip and repeated-cycle behaviour.

The earlier exploded-thumb and open-saddle entries are historical design stages. The 0.2 CAD now supplies a connected mount and full shell; physical acceptance remains open.

## Small exterior refinement — 6 October 2026

- [x] Round cassette walls and thumb-support corners without changing mounting centres or overall part envelopes.
- [x] Soften the cassette cover edge and add shallow screw-head seats.
- [x] Recheck meshes, static assembly clearances, equaliser travel and sampled thumb positions.
- [ ] Measure selected cover screw heads and verify the 2 mm remaining seat and insert engagement on a printed sample.
