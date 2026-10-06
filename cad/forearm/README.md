# Forearm-integrated Phoenix — 0.4.0 design candidate

This replaces the separate box mounted above the arm. Three servos, battery, Nano, EMG conditioner and tendon mechanism sit inside a split forearm shell. The original Phoenix v3 palm and finger shapes are retained. This is an unfitted bench-development design, not a working or wearable prosthesis.

![Exterior](exports/complete_preview.png)

## Hand correction

The earlier placement assigned a long distal part to the index finger and a short one to the ring finger. The corrected order is **short index, long middle, long ring, short little**. The dorsal return-band features face upward; positive flexion in the new placement script curls the fingers toward the palm. The added thumb fork spreads the thumb outward/backward in the open pose instead of pointing it along the fingers. Its local yaw changes from 50° to 130°; that number is a CAD placement angle, not an anatomical prescription.

These choices were checked against John Diamond's [Phoenix v2 assembly guide, especially pages 8, 18 and 19](https://e-nable.fr/files/Phoenix_v2_assembly_guide.pdf). [e-NABLE's v3 catalogue](https://hub.e-nable.org/s/e-nable-devices/wiki/208/e-nable-phoenix-hand-v3) identifies the v2 lineage. The v3 placemat itself was not accessible. The guide is linked, not redistributed; its licence is separate from the CAD licence.

`hand.py` recovers joint centres from source cylindrical faces and preserves all original source surfaces. The upstream STEP is hash-checked. **Full finger closure is not accepted:** the placement diagnostic detects small proximal/distal surface overlaps at PIP bends of 30° and above (up to about 4.82 mm³ at the sampled 60° pose). The 45° MCP / 15° PIP illustration clears the other modelled fingers, palm and fixed arm parts. Verify original pins, stops, assembly orientation and joint clearances before commanding deeper closure. Source shapes have not been silently cut to remove this result.

## Inside the arm

![Upper shell and tendon cover removed](exports/open_preview.png)

| Location | Parts and provision |
| --- | --- |
| Distal forearm, dorsal level | Three low-profile FT5425BL reference servos on an integral shelf, with low retaining walls and tie slots |
| Below motors | 70 × 32 × 22 mm battery allowance in a cradle; two 10 mm strap tunnels |
| Forward, below tendon mechanism | Removable Nano/EMG tray, separate 5 V regulator, fuse and distribution allowances |
| Forward, upper level | Two covered equaliser lanes and a separate lower thumb slider lane; five tendon exits |
| Upper shell | Recessed main disconnect and arm-switch positions |
| Socket underside | Window for an independently strapped SEN0240 electrode carrier, aligned with the placeholder socket taper |
| Socket side seam | Cable passage from the electrode area toward the equipment bay |

![Electronics from underneath; both shells and tray removed](exports/electronics_preview.png)

Green blocks are the Nano and EMG conditioner; gold is the battery; dark blocks are motors and electrical allowances. These envelopes do not include complete wiring, plugs, straps or every fastener. The electrode has an assumed 6 mm thickness; contact protrusion, liner clearance and muscle location still need measurement.

The shell is approximately **102 mm wide × 102 mm deep at its largest section**, including seam bosses. Its curved body is 279 mm long; the proximal opening to the hand's wrist datum is 295 mm. These dimensions describe the forearm, not the total spread hand. The three motors occupy different longitudinal positions so their spools do not overlap. The shell wraps this equipment instead of carrying a separate roof box.

Compared in the same CAD axes, maximum assembly depth falls from **145 to 102 mm**, about **30% less**. This uses more length: the full assembly's longitudinal bounds increase from about 317 to 434 mm because the equipment is beyond the limb end rather than stacked above it. It is a packaging trade-off, not a 30% volume reduction or proof of anatomical fit. `envelope_comparison.json` records both exported assemblies; regenerate with `python cad/forearm/compare.py`.

## The space requirement that must be checked

The model reserves an empty socket from Y = −295 to −160 mm: **135 mm of socket length**, with nominal inner elliptical diameters of about 70 × 64 mm proximally and 54 × 50 mm distally. These are geometric placeholders, not measured anatomy or a liner specification.

It then assumes **160 mm from the residual-limb end to the wrist datum**. The equipment bay begins beyond the limb end, separated by a 3 mm bulkhead. No modelled equipment occupies the reserved limb volume. If the recipient has less distal space, this arrangement would make the arm too long: it must be repackaged around measured anatomy or use substantially different actuators. Do not shorten the socket or put components into occupied limb space to force a fit. Suspension, pressure distribution and alignment require individual fitting.

## Selected parts and hardware

Print-coordinate STEP/STL pairs are in `exports/`. Their minimum Z is zero; assembly positions are recorded in `checks.json`. `complete_forearm.step` is the assembly reference, not a print-in-place object.

| Added print | Quantity |
| --- | ---: |
| `forearm_lower`, with servo shelf and battery cradle | 1 |
| `forearm_upper`, with recessed controls | 1 |
| `electronics_tray` | 1 |
| `internal_tendon_base`, `internal_tendon_cover` | 1 each |
| `thumb_slider` | 1 |
| `palm_receiver`, with revised thumb fork | 1 |
| `../compact/exports/single_groove_spool.stl` | 3 |
| `../exports/pair_equaliser.stl` | 2 |
| `../arm_interface/exports/emg_band_carrier.stl` | 1 |

Use the original right Phoenix hand/pins at the selected scale from the [official release](https://www.thingiverse.com/thing:4056253). Some source STEP-to-STL conversions failed earlier mesh checks, so the source hand's diagnostic meshes are not offered as accepted printable files. The source hand is included in the assembly STEP. Do not scale the whole motorised assembly: hardware dimensions would change.

Additional hardware allowance: ten M3 through-fastener sets for the shell seam; four for the electronics tray; four for the tendon base; two for its cover; two M4 sets at the forearm/receiver interface; and two M4 palm-support positions. Access and engagement lengths need to be selected against a print. The tendon cover captures two top-loaded M3 nuts in 6.6 mm corner-to-corner hex pockets, 2.4 mm deep. M3 × 6 mm cover screws are the starting allowance: check nut fit and engagement, and keep their tips above Z = 11 mm so they do not obstruct the lower thumb lane. These pockets provide metal threads; the printed clearance bores are not threads. The tendon-base motion check includes 6 mm diameter × 2 mm high screw-head allowances at X = ±30 mm, in 6.4 mm access pockets. Shell seam bosses have only about 1.3 mm radial wall around the bore and require a strength/print check.

Retain the original wrist axle/retainers, a fitted thumb axle, three matching metal servo horns and their retaining screws, six M2 horn/spool fasteners, servo ties, two socket straps, a separate electrode band, palm-retention strap, battery straps, insulating board pads, tendon, return bands and liner stock. Battery straps must fit the nominal 1 mm gap below the servo shelf (maximum 0.8 mm strap allowance). These counts specify CAD provisions; they do not establish load-rated attachment or a complete priced shopping kit.

## Electronics, pull and travel

The replacement-parts [electrical BOM and force model](../slim/README.md#replacement-bom-and-power-changes) apply: three FT5425BL candidates, classic 5 V Nano with low soldered connections, SEN0240 and separate 5 V logic regulator. A protected 2S rail feeds these particular servos directly. The owned generic servos are unidentified and are not approved for that rail.

At the retained 12.3 mm effective spool radius, the screening model gives about **10.8 / 13.2 / 15.1 N per paired tendon at 6.0 / 7.4 / 8.4 V**, using the lower of manufacturer rated torque and 40% stall torque, 60% assumed routing efficiency and a separate 1.5 margin. This is tendon pull, not fingertip force or continuous-duty approval. [Manufacturer data](https://www.feetechrc.com/Data/feetechrc/upload/file/20210810/6376418710101296552903409.pdf); generated values: `../slim/forces.json`.

The new routing has not been measured. Longer bends and liners can reduce efficiency; repeat the [full-path tendon test](../../TENDON-TEST.md) before accepting these figures. Ideal take-up at 160° is 34.35 mm, within the 38 mm sampled slider range, but required hand closure travel remains unmeasured. The potential combined stall demand reaches 15 A at 8.4 V. Select the actual protected pack, disconnect, fuse, wire and connectors together; the earlier 10 A parts and 7.5 A fuse are not an accepted substitute. The CAD still contains reference volumes for those unselected components.

The existing [Nano firmware](../../firmware/README.md) is unchanged: smoothing, one EMG input and three linked servo commands. Calibrate each new servo with tendons disconnected. There is no active force/current feedback. The old generic-servo 5 V power diagram is historical; use the candidate topology in the linked electrical guide.

## Checks and rebuild

`checks.json`: seven valid single-solid added parts; watertight positive-volume STLs; no modelled static component/part overlaps above 0.001 mm³; no equipment intrusion into the reserved socket. `motion_checks.json`: both shell halves also clear that socket; 18 equaliser poses (three positions × three angles × two bars) and three thumb-slider positions clear the fixed geometry and sampled fastener heads. This is a set of discrete tests, not a continuous sweep. Fork relief is checked at four thumb-root angles; full thumb opposition and tendon paths remain unaccepted.

With CadQuery 2.8.0, trimesh, numpy, matplotlib and Pillow:

```sh
python cad/forearm/hand.py --check-motion
python cad/forearm/build.py
python cad/forearm/verify_motion.py
python cad/forearm/previews.py
python cad/forearm/package.py
```

The hand diagnostic intentionally records deeper PIP interference. It must not be interpreted as a passing full-motion test. Mechanical fit, cable bends, manual release, palm restraint, structural strength, EMG/motor-noise performance, battery protection and heat under load remain bench acceptance work. No hardware was assembled, powered or fitted for this revision.
