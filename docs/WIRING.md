# Wiring

**Current 0.4.2 forearm candidate:** use the [replacement-servo power topology](../cad/slim/README.md#replacement-bom-and-power-changes). FT5425BL candidates take the protected 2S servo rail directly, with a separate 5 V logic supply. Their high-current protection and actual components remain unselected. Signal pins below are retained. The diagram and power-component values below are the historical generic-servo 5 V baseline; do not apply them unchanged to the replacement-servo candidate.

![Wiring diagram](wiring.svg)

The drawing gives the electrical nets; it is not a PCB layout. Follow connector labels rather than relying on cable colours.

| From | To |
| --- | --- |
| Protected 2S battery + | 7.5 A fuse near battery, then ≥10 A DC main switch |
| Switched battery + | VIN on both regulator boards |
| Battery − | Star ground / both regulator GNDs |
| D24V90F5 VOUT | Servo 5 V distribution, then all three servo + pins |
| Servo returns | Distribution ground, then a dedicated heavy return to star |
| D24V5F5 VOUT | Nano 5V and SEN0240 + |
| Nano GND / sensor − | Logic ground return to star |
| SEN0240 A | Nano A0; 1 MΩ from A0 to GND |
| Nano D2 | Arm switch to GND |
| Nano D9 / D10 / D11 | 220 Ω series resistor to thumb / index-middle / ring-little signal |
| 1,000 µF 10 V capacitor | Servo distribution + to GND; check polarity |
| 100 nF and 10 µF capacitors | Sensor + to sensor −, close to board |

Use short 18 AWG input/distribution leads and suitably rated connectors for the main power path; the servo leads retain their supplied connectors. Keep EMG cable and sensor ground away from switching and motor-current wiring. The two regulators share ground; this is not galvanic isolation or medical isolation. Separate rails reduce shared supply impedance but do not guarantee noise-free measurements.

The 5 V servo regulator is a reference selection with thermal/current limits depending on input voltage and cooling. Verify voltage under simultaneous movement. Three DS3225 references have 5.7 A total stall current at 5 V; this does not describe the unknown generic servos. Do not intentionally run them stalled. Confirm actual supply requirements before connecting.

For development, an external current-limited supply may replace the battery only with electrodes disconnected. For electrodes on skin, use battery operation with USB and charger disconnected. Program the Nano with external logic power removed to avoid backfeeding. A battery must include appropriate cell protection and use its matching charger; the fuse alone provides neither cell balancing nor low-voltage protection.

The main switch removes power, but a geared servo can still resist reopening when unpowered. Keep the test fixture's tendons accessible for manual release. This is a bench prototype, not a device for unsupervised wear.
