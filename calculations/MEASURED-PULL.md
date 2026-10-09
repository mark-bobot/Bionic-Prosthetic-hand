# Check the actual tendon pull

**Historical equaliser layout.** For the current bottom-drive fixed paired grooves, use [BOTTOM-DRIVE-PULL.md](BOTTOM-DRIVE-PULL.md) and its measurement template/checker. Do not transfer the equaliser travel assumptions to the current kit.

Use this after assembling the hand on a bench fixture. Leave the servo disconnected. Measure at the point where its spool pulls the tendon, through the complete installed route and with the actual return bands. For the paired channels, retain the equaliser and both fingers during the measurement. Record peak pull and input travel, including the worst point in the movement.

Make a copy of `measured_pull_template.json`, enter readings for the thumb, index/middle pair and ring/little pair, and run:

```sh
python calculations/check_measured_pull.py my_measurements.json --output my_result.json
```

The supplied template contains **no measured forces or travels**. Its initial result is `MEASUREMENTS_REQUIRED`. Its radius, sweep, slack and torque are reference settings; replace them with justified values for the actual setup. `servo_and_sweep_confirmed` must remain false until the servo is identified, its torque allowance is justified at the lowest loaded supply voltage, and its usable endpoints are measured. The checker then reports `CALIBRATION_REQUIRED` if the arithmetic passes but this confirmation is missing. A `SCREEN_PASS` is only a torque/travel calculation, not hardware acceptance.

## Equations

With measured actuator-end force F in N, effective winding radius r in m, and separate load margin M:

- Required torque = M × F × r.
- Available travel = r × usable angle in radians.
- Minimum radius = (measured travel + slack allowance) / usable angle.
- Maximum radius = allowed torque / (M × measured force).

Use consistent units; the script accepts millimetres and converts internally. A feasible radius interval exists only when the minimum is no greater than the maximum. A small spool may have enough force but insufficient stroke; a large spool may provide the stroke but exceed the torque allowance.

**Do not apply a routing-efficiency factor again.** Measuring at the actuator end already includes losses along the route. The older finger-side estimates use an assumed efficiency because they do not have these measurements. Keep winding in one layer and account for the largest effective radius when checking torque.

The template's 0.6668522 N·m is the current candidate's 6 V rated-torque cap, converted from 6.8 kgf·cm. It comes from the [FT5425BL A/0 manufacturer specification, page 3](https://www.feetechrc.com/Data/feetechrc/upload/file/20210810/6376418710101296552903409.pdf). This does not identify the user's generic servos or establish continuous operation inside an enclosure. The 160° sweep and 3 mm slack reserve are starting assumptions.

The current equaliser has output holes 20 mm apart. At an assumed ±30° tilt, its ideal maximum output-travel difference is 20 sin(30°) = **10 mm**. This excludes line-angle effects and compliance. A pair requiring a greater difference can reach a bar stop even when mean travel is adequate. Measure the assembled pair and watch for this; a stopped bar does not continue equalising as assumed.

Record here before entering results:

| Channel | Peak actuator-end force (N) | Input travel (mm) | Sticking / early contact / bar stop |
| --- | --- | --- | --- |
| Thumb | not measured | not measured | |
| Index + middle | not measured | not measured | |
| Ring + little | not measured | not measured | |

Use a bench contact fixture to assess loaded closure. These calculations do not set safe tissue pressure or validate a fitted socket. Current, temperature, reopening, tendon wear, manual release and repeated operation remain separate checks.
