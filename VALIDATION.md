# Validation record — 26 September 2026

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
