# Preliminary two-finger servo sizing

Status: calculation with assumptions, not a verified capability or a recovered historical calculation. Prepared 26 September 2026.

## Known inputs and unknowns

The owner reports generic 25 kg·cm, 180-degree servos and a DFRobot EMG sensor. Servo model, actual torque-versus-voltage rating, power source, spool radius, tendon travel, finger forces and duty cycle are unconfirmed.

Treat the advertised torque as nominal stall torque for this preliminary calculation. A generic servo's actual output may differ. Do not choose a supply voltage from this number alone.

## Model

Assume two separate tendons winding in single-layer grooves at the same effective radius r. Each tendon takes up r × angle; sharing the shaft divides the available torque between the loads, not the angular travel.

- Nominal stall torque: 25 kgf·cm × 0.0980665 = 2.4517 N·m.
- Provisional working allowance: 40% of nominal stall torque = 0.9807 N·m = 10 kgf·cm.
- Tendon-routing efficiency eta: 0.60 (assume 40% loss).
- Additional load margin M: 1.5.
- F1 and F2: required finger-side tendon tensions, including return-elastic and finger-joint resistance and any intended contact load.

These percentages are explicit engineering assumptions for screening, not manufacturer continuous-duty ratings, measured friction or proof of safe operation. Heat and duty-cycle testing are still required.

Required torque including load margin:

    torque_required = M × r × (F1 + F2) / eta

For equal finger loads:

    F_each_limit = eta × torque_working / (2 × M × r)

Use metres and newtons to obtain N·m.

## Results

| Effective spool radius | Tendon travel at 180° | Travel at an illustrative 160° usable sweep | Equal finger-side tension limit under assumptions |
| --- | ---: | ---: | ---: |
| 8 mm | 25.1 mm | 22.3 mm | 24.5 N each |
| 10 mm | 31.4 mm | 27.9 mm | 19.6 N each |
| 12 mm | 37.7 mm | 33.5 mm | 16.3 N each |
| 15 mm | 47.1 mm | 41.9 mm | 13.1 N each |

180° = pi radians; travel = r × angle. The 160° sweep reserves illustrative endpoint margin; the actual usable sweep must be measured. A direct servo horn is a different geometry and must not be assigned drum travel r × angle without a winding drum.

At 10 mm radius:

| Assumed tension required per finger | Torque including friction allowance and 1.5 margin | Comparison with provisional 10 kgf·cm allowance |
| --- | ---: | --- |
| 10 N | 0.50 N·m / 5.10 kgf·cm | Below allowance |
| 15 N | 0.75 N·m / 7.65 kgf·cm | Below allowance |
| 20 N | 1.00 N·m / 10.20 kgf·cm | Slightly above allowance |
| 30 N | 1.50 N·m / 15.30 kgf·cm | Above allowance |

No row asserts the actual force required by this hand. The hand has not been measured.

## Friction and rating sensitivity

At 10 mm radius, reducing routing efficiency from 0.60 to 0.40 lowers the calculated equal-finger limit from 19.6 N to 13.1 N. If actual stall torque is only 20 kgf·cm, the same 40% working assumption, 0.60 efficiency and 1.5 margin give 15.7 N per finger.

Account for printed-channel roughness, tight tendon bends, breakaway friction, elastic return tension, joint binding and line stretch. Additional wound layers increase effective radius, increasing torque demand. Use the largest working radius for torque sizing. Poor routing can exceed the assumed losses.

Two fingers rarely have identical force and travel requirements. With a rigid two-groove drum, one finger can contact an object before the other and become overloaded. An equaliser or controlled compliance may be needed; its changed geometry must be recalculated.

Do not confuse tendon tension with fingertip force. In a simplified single-joint example, a 20 N tendon acting at a 5 mm moment arm supplies 0.10 N·m. Applied against a contact point 50 mm from that joint, this corresponds to only 2 N before return-elastic and other losses. The actual multi-joint hand requires its actual geometry and contact configuration.

## Voltage, current and packaging

A manufacturer DS3225 datasheet is a comparison only, not identification of the owned servo. It lists 21 kgf·cm stall torque at 5 V and 24.5 kgf·cm at 6.8 V; corresponding stall currents are 1.9 A and 2.3 A. Its body is 40 × 20 × 40.5 mm and mass is 60 g. The datasheet covers 180° and 270° variants.

Source: https://dsservo.com/d_file/DS3225%20datasheet.pdf

Three such bodies would weigh 180 g and occupy approximately 97 cm³ of body volume alone, before horns, mounts, spools, wires or clearance. This shows why packaging must be checked before committing to three standard-size servos.

Use a servo power branch sized from the actual servo's transient and simultaneous-load requirements; do not supply servo motor current through an Arduino pin or onboard regulator. Keep a clean sensor/logic supply and route high-current returns away from the EMG signal path. In a non-isolated control design the signal grounds need a deliberate common reference.

## Decision and next measurements

The advertised 25 kgf·cm class is a plausible candidate for a paired-finger prototype. This calculation does not yet approve the generic servo or establish useful grip strength.

A 10–12 mm radius drum is a candidate to test, not a final specification. Choose the smallest radius that provides measured travel plus allowance for slack/stretch over the calibrated safe angular sweep.

1. With the servo disconnected, pull each assembled finger's tendon through the intended routing using a force gauge or spring scale. Keep the return bands installed. Record maximum pull and required travel over the full closure, at a representative speed.
2. Measure both together and then under the intended object-contact load. Record where each finger makes contact. Do not extrapolate unloaded closure into grip capacity.
3. If pull is measured at the servo end through the full routing, it already includes those routing losses: compare M × r × (measured F1 + measured F2) with the working allowance, without dividing by eta again.
4. At 10 mm radius, the provisional 0.9807 N·m allowance and M = 1.5 correspond to a total measured servo-side tension limit of 65.4 N. This is a model-derived test target, not a certified continuous load limit.
5. Verify the actual servo label, voltage range, angular sweep and spool dimensions. Bench-test both fingers with controlled travel; record current, supply sag, motion, temperatures and holding duration under the intended duty cycle.
6. Add measured results and revise the calculation before calling the servo sufficient.

## Reference supply choice for the next build

Use DS3225 as the reference model while the owned servo remains unidentified. Its manufacturer specifies **4.8–6.8 V**. Plan around **regulated 5 V** for the first design calculations, not the top of that range. This is a reference design choice, not confirmation of the owned unit's allowable supply.

At the published 5 V rating of 21 kgf·cm, the provisional 40% working allowance is 8.4 kgf·cm = 0.824 N·m. Keeping 60% routing efficiency and the 1.5 load margin gives **16.5 N per finger at a 10 mm radius**, instead of the nominal-25-kgf·cm result of 19.6 N. If measuring at the servo end through the complete routing, the corresponding combined-force limit is **54.9 N**, with no additional routing-loss factor.

These are preliminary screening limits. No manufacturer continuous-duty rating is inferred from the 40% allowance. A different generic servo may have different torque, current or voltage limits.

The reference stall current at 5 V is 1.9 A per servo. Three reference units could therefore demand 5.7 A together at stall, before the rest of the electronics and supply margin. That is a sizing warning, not a normal running-current estimate or permission to run stalled. The final regulator, battery, wiring and connector ratings need the actual actuator count and measured demand.

Follow [the tendon test](TENDON-TEST.md) before choosing the final drum radius.
