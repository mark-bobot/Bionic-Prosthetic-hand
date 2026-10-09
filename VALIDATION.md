# Validation record — 26 September 2026

## Resized receiver candidate — 8 October 2026

`cad/sizing/build_adapter.py` checks the 120% example against the existing fixed hardware. A new receiver preserves the two M4 forearm centres; a revised lower shell adds two local head-clearance pockets. The CAD checks include one-solid/mesh validation for both replacements, cylindrical bore positions, bearing material beneath the screw recesses, static interference, thirteen sampled hand poses against the receiver/fixed components and complete/open export matching. Results and source/output hashes: `cad/sizing/adapter_exports/adapter_checks.json`. Original hand-to-hand checks are inherited by uniform scaling rather than rerun; no loaded or fitted-use acceptance is claimed.

`tests/receiver_geometry_test.py` checks valid receiver solids and fixed bolt geometry at 90% and 140%, and rejects out-of-range or NaN scales. Those boundary tests do not validate complete assemblies at those sizes. The original 0.4.3 assembly remains separate.

## Anthropometric sizing study — 7 October 2026

`cad/sizing` exports a uniformly scaled original hand and a separate adjustable limb/liner clearance envelope. It checks STEP bounds and volume scaling for all eleven corrected hand solids, and tests the envelope/resized hand against the existing hardware geometry. The seven arithmetic tests cover missing measurements, signed anatomical registration, length/width mismatch and stroke limits. The report never labels these geometric checks as patient fit. The illustrated 120% hand needs a new receiver; the existing forearm and its motion acceptance remain at 100%. See `cad/sizing/README.md` for exact scope.

## 0.4.3 follow-up — 7 October 2026

- `closure_checks.json`: thirteen simultaneous five-digit poses clear the palm, each other, wrist support and both arm halves at the 0.001 mm³ reporting threshold. The trajectory reaches 60° MCP / 70° PIP, with thumb root −90° / tip 40°. These are samples, not continuous or loaded-motion acceptance.
- `assembly_checks.json`: matches all eleven hand solids in the complete, open and close-up STEP exports by bounds, centre and volume, with documented numerical integration tolerances. Source, STEP and preview hashes prevent stale packaging.
- `servo_reference.py`: manufacturer drawing-based case, ears and shaft; spools moved from a 10 mm to the specified 11.5 mm offset. Rebuilt static assembly and seven printable parts pass existing checks. Horns, wiring and actual bought-part fit are not validated.
- `tests/pull_sizing_test.py`: checks torque units, force/travel trade-offs, invalid inputs and missing measurements/calibration. The supplied measurement template remains unresolved; no physical readings were invented.

## Current forearm integration — 6 October 2026

The current selection is [cad/forearm](cad/forearm/README.md). Seven new parts are valid single solids with watertight, positive-volume STL exports. The complete static assembly has no reported part/envelope overlaps above 0.001 mm³. Equipment and both shell halves clear the reserved socket lumen. The lower shell includes a battery cradle and two under-floor strap passages; controls are recessed in the upper shell. Results: `cad/forearm/checks.json`.

On 7 October 2026 the original v3 right-hand placemat was retrieved and visually inspected alongside the original STEP. The short/long/long/short finger order is confirmed. The thumb now uses the native palm pin axis and the centre of its 6.5 mm inner fork gap. The displaced fork is removed; only the added support is relieved. `cad/forearm/layout_checks.json` records eight clear thumb poses between −60° and −90° root rotation, with 10°/30° tip bend. These are discrete CAD samples, not full thumb opposition, pin-fit or physical validation. Source geometry remains unchanged.

`cad/forearm/motion_checks.json` records 18 equaliser poses, three thumb-slider poses and a 45° MCP / 15° PIP four-finger pose. The discrete mechanism samples span 38 mm and include 6 × 2 mm tendon-base screw-head allowances. No continuous sweep, moving-cord clearance or installed-fastener acceptance is claimed.

**Fingertip inversion fixed in 0.4.2:** all five distal source solids were still upside down in the previous assembly. They now roll 180° longitudinally, placing their own return-band tabs dorsally. The previous reported 30–60° PIP interference came from that placement error. Forty four-finger adjacent-part checks through 60° bends now remain below 0.001 mm³ (maximum approximately 0.000895 mm³). The displayed rest PIP angle is 10° because corrected 0°/5° poses contact the original stop surfaces. `cad/forearm/exports/finger_motion_diagnostic.json` records the corrected samples. This does not validate pins, full continuous closure or loaded operation.

The assembly assumes 160 mm from residual-limb end to wrist. Bought-part lead/connector geometry, high-current component selection, straps, print strength, patient-specific fit and all hardware tests remain open. Firmware is unchanged; previous compile/control-test records remain historical. Rebuild commands are in the current guide.

## Completed

- Arduino CLI build: `arduino:avr:nano:cpu=atmega328`, AVR core 1.8.8, Servo 1.2.2. Result: 7,228 bytes flash (23% of 30,720), 653 bytes global RAM (31% of 2,048).
- Host C++ control tests: calibration duration, activation debounce, relaxation, disarm/rearm, three-second timeout, rail-fault handling and arithmetic range pass.
- Host integration test using the actual included OYMotion filter: synthetic resting baseline → 80 Hz activity → resting baseline causes open → close → open. This is a synthetic software test, not a human EMG recording.
- Official Phoenix STEP downloaded from the e-NABLE catalogue link, imported successfully as 32 solids. Upstream SHA-256 recorded in `cad/README.md`.
- CadQuery 2.8.0: all four generated printable parts are valid single solids. STL exports have positive volume and are watertight. Results: `cad/cad_checks.json`.
- Reference rectangular servo bodies have zero volume intersection with the carrier. This excludes horns, ears, connectors, ties and actual manufacturing tolerances.
- Wiring diagram and CAD preview images rendered and visually inspected.

- Revision B integrated base and lid pass valid-single-solid and watertight-positive-volume mesh checks. Ten electronic/battery/switch envelopes have no detected intersection with the base, lid or each other. Base/lid fit and servo/spool-to-base clearance checks pass. See `cad/integration_checks.json` and the scope limits in `cad/INTEGRATION.md`.

- Three optional fit coupons pass single-solid and watertight-positive-volume checks; see `cad/coupon_checks.json`.

## Not performed

No board upload, on-device timing measurement, real EMG capture, servo load/temperature/current test, physical print fit, structural analysis, grip test or wearable assessment has been performed. No clinical or production acceptance is claimed. BOM prices are planning allowances, not a completed set of supplier quotes.

## Reproduce

```
arduino-cli compile --fqbn arduino:avr:nano:cpu=atmega328 firmware/ProstheticHand
c++ -std=c++11 tests/control_test.cpp -o /tmp/control_test
/tmp/control_test
c++ -std=c++11 tests/filter_test.cpp firmware/ProstheticHand/EMGFilters.cpp -o /tmp/filter_test
/tmp/filter_test
python cad/build.py
python cad/integrate.py
python cad/fit_coupons.py
python docs/draw_wiring.py
python docs/make_bom.py
```

Install Arduino Servo through Library Manager. CAD generation uses CadQuery 2.8.0, trimesh and matplotlib; wiring rendering uses CairoSVG. The physical build tasks are tracked in `TODO.md`.

## Revision C geometry study — 27 September 2026

The original minimal-hand and compact-pack scripts export 15 valid single-solid printable part variants (including both mirrored palms). STL meshes are watertight with positive volume. Reference component/fixture pairs, the static hand assembly and the hand-to-housing assembly have no detected volume clashes. Each long finger was checked against its adjacent link and palm at synchronized 0/15/30/45/60-degree joint positions; thumb-to-palm checks use the same samples. These checks pass after adding thumb relief. They do not establish independent-joint swept clearance, tendon routing, grip function, structural strength or arm fit. See `cad/compact/*checks.json` and [revision C scope](cad/compact/README.md).

## Phoenix v3 restoration — 27 September 2026

The selected hand now uses the 32 solids extracted from the hash-verified official Phoenix v3 STEP. No original palm/finger geometry is altered. The new wrist cradle passes valid-single-solid and watertight-positive-volume STL checks. The reference view uses the compact enclosure and original hand parts; the thumb is deliberately exploded because its joint orientation is unresolved. Sub-0.001 mm³ source joint contacts are reported separately from larger clashes. Some diagnostic source STL conversions fail watertightness checks, so the repository supplies source STEP parts and links to the official printable STLs rather than distributing those conversions. See `cad/phoenix_v3/checks.json`. No physical fit or articulation acceptance is claimed.

## Rounded enclosure — 5 October 2026

The compact base, tray and curved lid pass valid-single-solid and positive-volume watertight STL checks. All modelled component/fixture pairs have zero reported volume clashes. The rebuilt Phoenix reference assembly reports no larger static collisions; inherited source contacts and source mesh limitations remain recorded separately. Both assembly and internal-layout previews were visually inspected. Original Phoenix source geometry remains unchanged.

The housing has 12 mm outer corner radii, a 65 mm motor-end roof falling to 59 mm at the rear, a 5 mm recessed switch panel and 2 mm screw-head recesses. These are CAD dimensions, not measured print results. Thin screw seats, actual switch/head fit, curved-cover support removal, cable clearance and cooling require physical checks. Servo and battery envelopes remain assumptions. No firmware changes or new hardware tests were performed in this revision.

## Lower single-groove revision — 5 October 2026

Supersedes the preceding rounded housing dimensions. Current front/rear roof heights are 60/57 mm. The base, tray, lid and new 6.75 mm single-groove spool are valid single solids with positive-volume watertight STL meshes. Modelled component/fixture pairs have no volume collisions. The new spool retains a 12 mm groove-floor radius; measured hardware and line-layer build-up are not represented.

`python3 calculations/tendon_forces.py` regenerates the force/travel report and JSON using the DS3225 5 V reference, explicit working/margin assumptions and 40/60/80% routing-efficiency scenarios. The 60% case gives 13.39 N per paired finger and 34.35 mm take-up at an illustrative 160 degrees. Actual closure tension, fingertip force, structural strength and thermal duty remain unmeasured. Firmware is unchanged.

The rebuilt Phoenix reference assembly reports no larger static collisions. The current exterior preview and force/travel plot were visually inspected. Inherited source mesh limitations and the deliberately exploded thumb remain unchanged.

## Right-arm interface concept — 5 October 2026

The open saddle and EMG-band carrier pass valid-single-solid and positive-volume watertight STL checks. The new parts have no modelled volume collisions with one another, the probe envelope, or the complete current Phoenix/housing assembly. The front housing bridge includes relief around the existing cradle plate. The saddle does not intrude into its placeholder lumen. These are geometric checks, not tissue-pressure, suspension or strength tests.

Personal-statement v4 was read locally from current IWA text and its embedded preview. DFRobot confirms a 22 × 35 mm dry-electrode board and placement along muscle direction on exposed skin. Electrode thickness, contact protrusion, residual-limb dimensions, straps, liner and anatomical alignment remain unverified. No patient-specific socket or wrist lock has been completed. Firmware and earlier force calculations remain unchanged.

## Prototype 0.1 package finalisation — 5 October 2026

Selected parts and firmware sources are listed with SHA-256 hashes in `release/manifest.json`. `release/package.py` verifies required files and existing collision reports and checks ZIP integrity. This is packaging validation, not a new CAD solve or physical acceptance. No geometry or firmware changed in this finalisation.

Host control tests passed again: calibration, debounce, release, arming, timeout, fault handling and arithmetic. The real included OYMotion filter/controller integration test passed with synthetic rest/contraction/rest input. The earlier Arduino compile result remains historical; no fresh board compile or upload was performed. Current hand-scale, thumb, wrist lock, tendon/equaliser retention, real component fit and individual socket fitting gates remain open in `BUILD.md`.

## Integrated right bionic revision 0.2 — 5 October 2026

The source STEP SHA-256 remains verified and all original palm/finger shapes are retained. The new connected thumb fork translates the thumb root 18 mm outward and 6 mm upward; root relief is made in the added fork only. The eight new printable variants pass valid-single-solid and positive-volume watertight mesh checks. The complete static assembly has no reported volume clashes above the script's threshold. Equalisers pass 18 sampled combinations (three travel positions, ±30/0° tilt); thumb MCP samples 0/15/30/45° pass against the fork, fixed assembly, receiver and guide comb. A separate final STEP intersection check finds 0 mm³ overlap between the independent EMG carrier and each of the dorsal shell and ventral door. These are sampled geometric checks, not continuous full-joint articulation, structural testing or grip acceptance.

Nano firmware compiles freshly with `arduino:avr:nano:cpu=atmega328`, AVR core 1.8.8, Servo 1.3.0: 7,228 bytes flash, 653 bytes global RAM. Host control and actual OYMotion filter/controller integration tests pass. The averaging helper was extracted for clarity; its 32-sample mean and control behaviour are retained. No board upload or real EMG capture was performed.

The current statement v4 text was reread locally and its design requirements are traced in `cad/bionic/README.md`. Hardware clearances remain nominal, socket dimensions remain placeholder values, flexible lines/straps and fastener insertion are not fully modelled, and actual release, fit, load, noise and thermal tests remain required. Package integrity checks and selected-file SHA-256 hashes are recorded by `release/package.py`.

## Small exterior refinement 0.2.1 — 6 October 2026

The cassette now has continuous rounded 3 mm walls with 5/2 mm outer/inner corner radii, a 0.8 mm top-edge chamfer and 6.2 mm diameter × 1 mm-deep screw-head recesses. The added thumb-support plate has 5 mm corner radii. All eight printable parts remain valid single solids with watertight, positive-volume meshes. All eight exported bounding dimensions and assembly Z positions agree with 0.2 within 0.001 mm. Source hand hash, socket parameters, thumb bore, 38 mm slider travel and sampled angles are unchanged.

The rebuilt assembly has no detected static volume collisions; the independent EMG carrier is now included in the routine pair checks. All 18 equaliser poses and four sampled thumb-root angles pass. Firmware, servo/spool geometry, component placement and force calculations are unchanged; no repeat firmware build or hardware test was needed for this geometry-only refinement. Recessed screw seating, joint motion under load, print strength and patient fit remain unverified.

## Smaller-part layout candidate — 6 October 2026

`cad/slim/build_pack.py` passes valid-single-solid and positive-volume watertight checks for its four exports, including the retained spool geometry. Component-envelope/fixture pair checks pass after adding local relief for the conservative servo-ear envelopes at the front inner corners. The added feed-through lid also passes solid and watertight checks.

`cad/slim/integrate.py` retains 16 hand/interface solids, replaces the old component pack and lowers the complete cassette by 10 mm. No static pair intersections above 0.001 mm³ are reported. Source hand identity remains recorded; cassette internal sampled clearance is inherited through rigid translation, not rerun as a new articulation study. The final CAD and internal layout previews were visually inspected.

Housing height is 50 mm, compared with 60 mm previously; housing-plus-cassette height is 63 mm versus 73 mm. Width/length remain 94/160 mm. Force/current calculations use FEETECH manufacturer data and explicit margins, with source links in the candidate guide. Firmware is unchanged and was not recompiled for this packaging study. Actual servo mounting, headerless Nano clearance, high-current protected battery circuit, flexible routing, thermal/load testing and individual socket fit remain unverified.

## Separate strap-on cuff box — 8 October 2026

This is a separate layout, not a revision to the integrated forearm. The original Phoenix hand and flat source gauntlet are unchanged. Five new print types (six pieces) pass valid-single-solid and positive-volume watertight STL checks. Static component/cord checks, expanded servo-ear keep-outs and the nominal cuff-volume clearance report no intersections above 0.001 mm³. Three sampled finger/thumb poses clear the new enclosure. Recovered shaft/drum axes agree, and exported STEP component bounds match after reimport. Exterior and open previews were visually inspected. Results and source/output hashes are in `cad/cuff_box/exports/checks.json`.

The case body is 94 × 96 × 71.5 mm; strap ears increase width to 110 mm. Servos remain unidentified, with editable assumed body/ear/shaft envelopes. The cuff is a cylindrical reference rather than a reconstructed thermoformed gauntlet or a fitted socket; the original wrist connection is not assembled in this reference view. No continuous tendon-motion, strap retention, fitted use, print strength, motor duty or electrical acceptance is claimed. Firmware is unchanged.

`cad/cuff_box/force_check.py` calculates required paired/thumb torque over explicit 5/10/15 N hand-tendon loads and 40/60/80% routing-efficiency scenarios. It also exposes a potentially large tipping load: the 10 N/60% simultaneous-pull example gives about 5.59 Nm around the nominal cuff crown when the exit cords run parallel to the forearm. That simplified load path is not a prediction of actual strap tension. Wrist stabilisation and a load-spreading attachment must be resolved on a bench before treating the module as wearable. The generic 25 kg·cm stall label and operating voltage remain unverified.

## Lower box and rigid arm adapter — finalised 9 October 2026

Seven print types (eight pieces) pass valid-single-solid and positive-volume watertight STL checks. The enclosure body is 94 × 96 × 54.9 mm, 23.2% lower than the preceding cuff box; removing strap ears reduces box width from 110 to 94 mm. This requires the shorter FT5425BL replacement-servo reference, not the unidentified owned motors.

The new open arm carrier connects to the box through four M4 positions and to the unchanged Phoenix hand through the palm receiver. Static component/cord, ear-envelope, adapter/receiver and reserved limb-volume checks pass. Thirteen sampled finger/thumb poses clear the new assembly. Six nominal mounting-screw shank/head allowances clear the exported print geometry. Source/output hashes and reimported assembly placements were checked; complete and open previews were inspected. See cad/cuff_box_compact/exports/checks.json and mount_checks.json.

A reproducible 10 N per hand-tendon, 60% efficiency scenario gives 0.410 Nm required paired-motor torque and a 3.74 Nm internal box pitch reaction around its seating plane. This is not net wearer torque: tendon reactions also enter the palm. No structural, suspension, pressure, actual motor/horn fit, complete cord routing or continuous-motion acceptance is claimed. Wrist axle retention, the palm restraint/stop pads and individual residual-limb fitting require physical work. Firmware is unchanged.

## Bottom-drive cartridge — 9 October 2026

The three replacement-servo references are inverted inside the existing-size 94 × 96 × 54.9 mm housing. The arm adapter, palm receiver and original hand geometry are retained. Cord exits move down by 29.9–42.1 mm. A 4 mm structural cover, twelve motor-ear pillars/bolts and captive-nut pockets replace reliance on hanging retaining ties.

Static part/component/internal-cord checks, drawing-positioned ear checks, adapter/receiver and reserved limb-space checks pass. Thirteen sampled hand poses clear the revised assembly. Seven print types remain eight pieces. Nominal box/receiver fasteners and twelve M3 motor-shank/nut sets clear exported printed parts and servo references.

A separate swept-head check reserves a maximum 1.2 mm projection below the drums for 4.5 mm diameter heads at 8 mm radius. Its minimum nominal floor clearance is only 0.6 mm; actual horn/fastener dimensions, tolerances and deflection remain acceptance gates. This is not compatibility with arbitrary M2 cap heads or nuts.

The unchanged 12.3 mm effective radius retains ideal pulling force and 34.35 mm take-up at an assumed 160°. The five parallel-cord, 10 N-per-hand-tendon, 60%-efficiency example reduces internal box pitch from 3.74 to 0.84 Nm. It is not net wearer torque or a measured friction reduction. No full external tendon routing, continuous cord motion, hanging-motor strength, service slack, thermal or fitted-use validation is claimed. Firmware remains unchanged; inverted winding direction and endpoints require unloaded calibration.

Final bottom-drive STEP reimports and source/output hashes passed. Complete and underside-mechanism previews were visually inspected. The illustrated lower drums remain enclosed in the complete model.

## One-wearer preparation audit — 9 October 2026

The build entry point now selects the bottom-drive candidate consistently. The historical 0.2.1 packager is explicitly labelled; a new selected-kit packager verifies geometry source/output hashes, hardware reports, quantities, file presence, ZIP integrity and packaged-file hashes. Its production-required mode returns exit code 2 while fitted-use evidence is incomplete. A negative check confirmed stale CAD hashes block packaging.

The unchanged firmware passed fresh controller and actual OYMotion-filter integration tests. A fresh Nano compile passed after supplying the existing Servo-library path: 7,228 bytes flash and 653 bytes RAM. The initial default-path compile failure and successful retry are recorded in release/production/software_checks.txt. No upload or physical verification occurred.

Eleven physical, fitting, manufacturing and regulatory evidence gates remain open. The generated kit is bench engineering material, not production approval or an accepted fitted device.
