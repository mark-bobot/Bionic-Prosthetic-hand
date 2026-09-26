# Validation record — 26 September 2026

## Completed

- Arduino CLI build: `arduino:avr:nano:cpu=atmega328`, AVR core 1.8.8, Servo 1.2.2. Result: 7,228 bytes flash (23% of 30,720), 653 bytes global RAM (31% of 2,048).
- Host C++ control tests: calibration duration, activation debounce, relaxation, disarm/rearm, three-second timeout, rail-fault handling and arithmetic range pass.
- Host integration test using the actual included OYMotion filter: synthetic resting baseline → 80 Hz activity → resting baseline causes open → close → open. This is a synthetic software test, not a human EMG recording.
- Official Phoenix STEP downloaded from the e-NABLE catalogue link, imported successfully as 32 solids. Upstream SHA-256 recorded in `cad/README.md`.
- CadQuery 2.8.0: all four generated printable parts are valid single solids. STL exports have positive volume and are watertight. Results: `cad/cad_checks.json`.
- Reference rectangular servo bodies have zero volume intersection with the carrier. This excludes horns, ears, connectors, ties and actual manufacturing tolerances.
- Wiring diagram and CAD preview images rendered and visually inspected.

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
python docs/draw_wiring.py
python docs/make_bom.py
```

Install Arduino Servo through Library Manager. CAD generation uses CadQuery 2.8.0, trimesh and matplotlib; wiring rendering uses CairoSVG. The physical build tasks are tracked in `TODO.md`.
