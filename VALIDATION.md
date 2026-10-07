# Validation record — 26 September 2026

## Current forearm integration — 6 October 2026

The current selection is [cad/forearm](cad/forearm/README.md). Seven new parts are valid single solids with watertight, positive-volume STL exports. The complete static assembly has no reported part/envelope overlaps above 0.001 mm³. Equipment and both shell halves clear the reserved socket lumen. The lower shell includes a battery cradle and two under-floor strap passages; controls are recessed in the upper shell. Results: `cad/forearm/checks.json`.

On 7 October 2026 the original v3 right-hand placemat was retrieved and visually inspected alongside the original STEP. The short/long/long/short finger order is confirmed. The thumb now uses the native palm pin axis and the centre of its 6.5 mm inner fork gap. The displaced fork is removed; only the added support is relieved. `cad/forearm/layout_checks.json` records eight clear thumb poses between −60° and −90° root rotation, with 0°/15° tip bend. These are discrete CAD samples, not full thumb opposition, pin-fit or physical validation. Source geometry remains unchanged.

`cad/forearm/motion_checks.json` records 18 equaliser poses, three thumb-slider poses and a 45° MCP / 15° PIP four-finger pose. The discrete mechanism samples span 38 mm and include 6 × 2 mm tendon-base screw-head allowances. No continuous sweep, moving-cord clearance or installed-fastener acceptance is claimed.

**Known failure retained:** the source-joint diagnostic reports PIP overlaps beginning at the sampled 30° bend, reaching approximately 4.82 mm³ at a sampled 60° pose. `cad/forearm/exports/finger_motion_diagnostic.json` preserves these results. Full finger closure is not accepted; the successful modest pose must not be read as a full-motion pass.

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
