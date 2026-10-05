# Prototype 0.1 — definitive build entry point

**Design package for bench development. Not a completed functional hand or a fitted prosthesis.**

Use this document to select parts. Revision B and the custom-hand revision C remain historical references. Do not combine their housings, spools or hand parts with this selection.

## Selected design

Right e-NABLE Phoenix v3 hand; three servos (thumb, index/middle, ring/little); classic 5 V Nano; SEN0240 dry electrode; 94 × 160 × 60 mm compact housing; single-groove spools; right-arm open support and separately strapped electrode carrier. The rear housing height is 57 mm. Servo identification, limb dimensions and several bought-part envelopes remain unconfirmed.

## Print and CAD selection

| Part | Qty | Selected file |
| --- | ---: | --- |
| Housing base | 1 | `cad/compact/exports/compact_base.stl` |
| Electronics tray | 1 | `cad/compact/exports/compact_tray.stl` |
| Curved lid | 1 | `cad/compact/exports/compact_lid.stl` |
| Single-groove spool | 3 | `cad/compact/exports/single_groove_spool.stl` |
| Floating equaliser | 2 | `cad/exports/pair_equaliser.stl` |
| Fairlead, candidate only | Up to 3 | `cad/exports/tendon_fairlead.stl`; mounting/path unfinished |
| Wrist cradle study | 1 | `cad/phoenix_v3/exports/phoenix_wrist_cradle.stl` |
| Right open forearm saddle | 1 | `cad/arm_interface/exports/right_open_saddle.stl`; dummy-fixture use |
| Electrode carrier | 1 | `cad/arm_interface/exports/emg_band_carrier.stl`; measure probe first |
| Phoenix hand and original hardware | One selected right-hand set | [Official release](https://www.thingiverse.com/thing:4056253); select scale before printing |

STEP counterparts are editable. `cad/arm_interface/exports/right_arm_reference.step` contains the latest complete reference placement. It includes component envelopes and an exploded thumb; it is not a print-in-place file. Do not print envelope boxes as parts. No rescaling of the entire assembly: it would alter screw, servo and electrode dimensions.

## Hardware and wiring

Use the [electronic BOM](BOM.md), [wiring](docs/WIRING.md), [current cover/horn hardware notes](cad/compact/README.md#current-lower-housing--5-october-2026), and [arm-interface additions](cad/arm_interface/README.md#added-reference-bom). The older £268.32 total is a revision B allowance, not a fully priced current kit. Exact switch, battery, horn and servo models must be confirmed before purchasing or drilling. Cover screws have different front/rear lengths and thin recessed seats; inspect a sample first.

Firmware: `firmware/ProstheticHand/ProstheticHand.ino`, with the adjacent included filter and control files. Follow [setup and initial limits](firmware/README.md). D9 thumb, D10 index/middle, D11 ring/little; SEN0240 output A0. The firmware has one EMG channel and commands the three groups together. No force feedback is implemented.

## Assembly sequence and acceptance gates

1. **Identify parts.** Measure servo case/ears/spline, horn and bolt heights, battery, switch bodies, board headers and electrode package/contact protrusion. Update the CAD envelopes if necessary. Confirm the actual servo voltage before powering it.
2. **Bench fit only.** Check a spool/horn, cover screw-seat sample and electrode-holder sample. Slice the curved lid with appropriate supports. Inspect bores, strap slots and line passages. Mount the forearm support to a dummy fixture; its ellipse dimensions are placeholders.
3. **Dry assembly.** Fit motors and electronics without loaded tendons. Check actual plugs, cable bends, battery restraint, service access and clearance above the spools. Follow the wiring guide and firmware first-run procedure.
4. **Complete unresolved mechanisms before loaded motion.** Verify original thumb orientation and joint assembly; design/verify the wrist lock and retained axle; mount and restrain the two equalisers and route five finger tendons; provide accessible manual tendon release. These items are not supplied as finished designs in 0.1.
5. **Measure and calibrate.** Use [the tendon test](TENDON-TEST.md), return bands installed. Record peak force and travel, including breakaway friction. Calibrate each servo with disconnected tendons first. The initial firmware command is a small test movement, not full closure.
6. **Validate on a bench.** Record current, heating, opening after relaxation, false activation, timeout, jam behaviour and repeated cycles. Geometric checks do not replace these tests.
7. **Individual fitting is a separate stage.** Supply residual-limb measurements and get socket/liner, suspension, pressure and EMG-site assessment. Do not treat the open saddle or unspecified straps as a proven wearable attachment.

## Force calculation retained

At 5 V the DS3225 reference is rated 21 kgf·cm at stall. With an assumed 40% working fraction, 1.5 load margin, 60% routing efficiency and 12.3 mm effective radius, the model gives 13.4 N per paired-finger tendon and 34.3 mm ideal take-up at 160°. These are not measured values for the owned servo or hand and are not fingertip grip force. [Full assumptions and reproducible calculations](calculations/README.md).

## Package verification

`python release/package.py` verifies the selected files, required geometry check records and firmware sources; emits `release/manifest.json` with SHA-256 hashes; and creates a ZIP under `/tmp`. This verifies packaging consistency, not physical operation. The release contains all tracked project files for provenance, including clearly labelled historical designs. This guide controls the selected build.

New work is AI-assisted reconstruction. It does not establish historical tests claimed in a personal statement. Licence boundaries and original Phoenix attribution are retained in [LICENSE.md](LICENSE.md).
