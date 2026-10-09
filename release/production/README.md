# One-wearer build preparation

**Status: NOT READY FOR FITTED USE OR PRODUCTION.**

**10 October update:** the user has the original Phoenix v3 print only; no extension or wiring. Start with [pre-human-test preparation](../../docs/PRE-HUMAN-TEST.md). The kit now includes current wiring, EMG mounting notes, a fixed-groove measurement checker, blank bench record and output-disabled firmware. These changes do not close any physical acceptance gate.

Target: one wearer with a right missing hand; retain original Phoenix hand geometry, three-motor paired-finger drive, Nano and SEN0240. Selected mechanical candidate: cad/bottom_drive. No commercial distribution or clinical approval is asserted.

The candidate is a starting point for engineering and prosthetic fitting, not a prescribed socket. No wearer measurements, clinical fitting record, physical assembly, measured tendon load, validated manual release or durability evidence has been supplied.

## Selected build

Use only the seven print types listed by [the bottom-drive guide](../../cad/bottom_drive/README.md): base, structural motor cover, rear board carrier, two paired drums, one thumb drum, arm adapter and palm receiver. Eight pieces total. The original right Phoenix hand must be obtained at the selected scale from the credited official source; the repository's source STEP conversion is not a newly validated printable hand kit.

The generated manifest freezes the exact selected STL, STEP, firmware and report hashes. The package script rejects stale source/output hashes, failed CAD checks, inconsistent quantities and missing files. It does not manufacture evidence or approve fitted use.

    python release/production/package.py
    python release/production/package.py --require-production

The second command deliberately exits nonzero while the physical/fitting gates remain open. Do not use the historical release/package.py kit for this candidate.

## Purchased-part completion

| Item | Quantity | Current state / required closure |
| --- | ---: | --- |
| FT5425BL candidate servo | 3 | Verify exact revision, ear/shaft/horn dimensions and delivered samples |
| Metal horns and shaft screws | 3 sets | Exact horn SKU, hole pattern and engagement unselected |
| M2 drum fasteners | 6 | Measured projection must be ≤1.2 mm; nominal remaining floor gap only 0.6 mm |
| M3 motor ear bolts and nuts | 12 sets | Select actual length and retainers against printed carrier |
| M3 cover / board-carrier sets | 4 / 2 | Specify lengths, head style, torque and retention after sample fit |
| M4 box / palm-receiver sets | 4 / 2 | Verify stack, engagement, tool access and no exposed limb-side tips |
| Wrist axle, retainers, stops and palm strap | 1 set | Sizes and reliable anti-rotation restraint not physically accepted |
| Arm straps, liner, socket interface | Wearer-specific | Prosthetist selection; do not order by placeholder cylinder dimensions |
| Classic 5 V Nano | 1 | Verify board revision and installed connector envelope |
| SEN0240 kit | 1 | Measure supplied conditioner, electrode and connector/contact geometry |
| Separate 5 V logic regulator | 1 | Verify noise, current and dropout across selected supply range |
| Motor supply, fuse, disconnect, wiring, connectors | 1 system | Exact rated parts unselected; do not inherit older generic-servo power kit |
| Tendons, liners and return bands | 5 paths / hand set | Specify material, diameter, terminations, friction, wear and release method |

Prices and a final procurement total are intentionally unresolved. A partially specified BOM is not a purchase-ready production BOM.

## Fitting and verification sequence

1. A prosthetist establishes residual-limb condition, socket/liner geometry, suspension, usable muscle sites, functional goals and fitting limits. Record the prescribed hand scale, limb clearance and alignment. Do not derive acceptance from the existing 32 mm radius.
2. Identify and inspect the purchased components. Record serial/lot, dimensions, datasheet revision and photos. Fit a horn/drum and a mounting coupon before a complete print.
3. Establish the print process: material/batch, machine, orientation, layer/perimeter settings, supports and post-processing. Qualify that process with representative loaded parts; generic infill settings are not a strength certificate.
4. Assemble on a rigid fixture. Inspect every force-transmitting joint, fastener and tendon termination. Verify actual moving clearance throughout travel, including the tight underside drum heads, and both directions of cover removal.
5. Define required hand tasks and measure each full-route tendon force/displacement, breakaway force, paired-finger behaviour and return-band reopening. Set load and travel limits from the measured system; stall torque is not the allowable operating torque.
6. Complete and test an accessible mechanical release. Disabling servo signals or cutting power is not assumed to release a geared grip. Check loss of power, seized motor and jammed tendon on the fixture.
7. Validate the electrical system: motor/logic rails, wiring and protection coordination, peak current, sag, interference, temperature and disconnect operation. Use an appropriate isolated arrangement for body-connected measurements; do not connect a worn electrode to a mains-linked bench setup.
8. Calibrate inverted winding direction and endpoints unloaded. Test EMG rest/contraction, motion artefacts, electrode loss, false activation, disarm, timeout, timing and restart with motors operating. The existing single channel cannot independently command finger groups or guarantee electrode-loss detection.
9. Agree and document load, cycle-life, temperature, release-time and wear acceptance criteria before qualification. Run repeated cycles and representative faults on the bench; record failures and rerun affected tests after fixes. No arbitrary cycle count is presented as clinical acceptance.
10. Only after engineering and fitting review, proceed through supervised unpowered fitting and any professionally approved functional trials. Record comfort, pressure, skin response, suspension, electrode stability and follow-up/maintenance needs.

## Evidence record

For each gate in readiness.json, retain: exact source revision/profile, hardware lots, test method and equipment/calibration, pre-agreed acceptance criterion, observations/raw data, result, date and responsible reviewer. CAD reports and firmware tests alone cannot close physical or fitting gates. The manifest remains marked blocked regardless of package integrity.

## Regulatory scope

For a one-wearer device supplied in Great Britain, establish the applicable pathway with the responsible manufacturer and qualified professional. A customised CAD file alone does not establish custom-made status or compliance. MHRA describes specific requirements for custom-made devices, including the prescription basis and manufacturer obligations. This package makes no classification or conformity determination.

Sources checked 9 October 2026: [MHRA custom-made devices](https://www.gov.uk/government/publications/custom-made-medical-devices/custom-made-devices-in-great-britain), [prosthetic/orthotic device guidance](https://www.gov.uk/government/publications/medical-devices-legal-requirements-for-specific-medical-devices/medical-devices-legal-requirements-for-specific-medical-devices).

Original geometry, software and licence notices are retained. This preparation does not substantiate past physical tests or personal-statement claims.
