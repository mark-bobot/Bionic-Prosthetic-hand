# Separate-box force and mounting scenarios

These are calculated requirements for assumed tendon loads, not proof that the unidentified servos can provide them continuously. Tendon force is not fingertip force. No supply voltage is inferred from a generic motor label.

At effective drum radius `r = 0.0123 m`, hand tendon force `F` and assumed routing efficiency `eta`: `T_box = F/eta`, `torque_pair = 2*r*F/eta`, and `torque_thumb = r*F/eta`. Efficiency scenarios cover transmission losses; they are not measured coefficients. Measure each finger through its complete bend and reopening cycle.

| Hand tendon load, each | Efficiency | Pair torque | Thumb torque | Total exit pull, five cords |
| ---: | ---: | ---: | ---: | ---: |
| 5 N | 40% | 0.307 Nm | 0.154 Nm | 62.5 N |
| 5 N | 60% | 0.205 Nm | 0.103 Nm | 41.7 N |
| 5 N | 80% | 0.154 Nm | 0.077 Nm | 31.2 N |
| 10 N | 40% | 0.615 Nm | 0.307 Nm | 125.0 N |
| 10 N | 60% | 0.410 Nm | 0.205 Nm | 83.3 N |
| 10 N | 80% | 0.307 Nm | 0.154 Nm | 62.5 N |
| 15 N | 40% | 0.922 Nm | 0.461 Nm | 187.5 N |
| 15 N | 60% | 0.615 Nm | 0.307 Nm | 125.0 N |
| 15 N | 80% | 0.461 Nm | 0.231 Nm | 93.8 N |

## Why the attachment matters

For the 10 N / 60% example, simultaneous pulling creates 83.3 N at the five enclosure exits. With the cords hypothetically parallel to the forearm, the current exit heights give about **5.59 Nm** around the nominal cuff crown. Reacting that only as a couple across the two strap stations (33 mm apart) corresponds to **169 N**. This is an illustrative load path, not a prediction of strap tension, skin pressure or actual use.

The example is enough to rule out assuming that two straps make a secure wearable attachment. First support the box and palm on a rigid bench fixture, identify the actual cord directions and measure loads. A fitted socket, neutral wrist restraint and load-spreading attachment need separate design and verification before worn powered use. Making the straps tighter is not a substitute for that work.

A claimed 25 kg·cm stall label converts to 2.45 Nm, but it is unverified and is not a continuous rating. No working-torque fraction is asserted here. Check the identified motor specifications, then measure current, temperature, release behaviour and travel under the actual loads. The ideal 160° travel is 34.35 mm; it does not establish full hand closure.

## Minimum measurement procedure

1. Hold the palm and cuff at a fixed wrist angle in a rigid bench fixture, with power disconnected.
2. Pull one original cord using a force gauge or a spring scale with a suitable range. Record force and displacement from fully open to the intended closed position, including the peak. Keep fingers clear of pinch points.
3. Repeat with the final guides and liners. Test paired cords together; check both free motion and one finger contacting an object first. Fixed coupled drums do not adapt independently.
4. Measure the actual motor case, ears, shaft, horn, lead exit and rated supply. Compare measured requirements with verified motor data before selecting the power supply.
5. Start powered bench trials at limited travel with a reachable disconnect and a way to slacken the tendons manually. Loss of power alone may not release the geared servos.

Reproduce with `python cad/cuff_box/force_check.py`. Geometry comes from the current CAD check report; the 33 mm strap spacing follows this design revision. JSON results are in `exports/force_scenarios.json`.
