# Draft bill of materials

Status: preliminary; quantities, prices and fit are not final. Updated 26 September 2026.

[Servo sizing and assumptions](SERVO-SIZING.md) · [Remaining work](TODO.md)

## Parts

| Item | Preliminary quantity per hand | Selection/status |
| --- | --- | --- |
| Modified Phoenix Hand v3 printed parts | 1 set | Hand size, CAD modifications and print material to confirm |
| Generic 25 kgf·cm, 180° servo | 1 for paired-finger test; potentially 3 for a five-digit layout | Owner reports possession; exact models, quantity owned and rated voltage unknown. Three actuators for 2+2+1 is a proposal, not the documented original mapping |
| Servo horn, screw and grooved tendon drum | 1 per actuator | Confirm spline; candidate 10–12 mm effective radius subject to measured travel and torque |
| Paired-finger coupling/equaliser | As required | Determine from unequal finger travel and object contact |
| DFRobot EMG sensor kit | 1 | Owner-confirmed brand; likely SEN0240 Gravity/OYMotion dry-electrode kit, SKU still to confirm |
| Compact Arduino controller | 1 | Classic Nano proposed; original board model unspecified |
| Servo power regulator/BEC | 1 appropriately rated branch | Voltage/current cannot be finalised until actual servo and load are identified |
| Clean sensor/logic regulator | 1 branch, implementation TBD | Sensor/board-compatible voltage; decoupling and return routing required |
| Battery, protection, switch, fuse and compatible charging arrangement | 1 system | Chemistry, capacity and protection to size after load/runtime measurements |
| Tendon line | 1 set | Existing notes reference 80 lb braided fishing line; final diameter/length/knots and abrasion behaviour to verify |
| Elastic return elements | 1 set | Existing notes reference non-latex dental bands; number and force to measure |
| Palm/tensioner screws and servo mounts | 1 set | Sizes and quantities from final CAD |
| Firm foam padding | 1 set | Listed in original mechanical BOM |
| Fingertip grips | 1 set | Listed in original mechanical BOM |
| Hook-and-loop straps | As required | Existing note specifies 300 × 25 mm straps |
| Wires, locking connectors, strain relief and decoupling capacitors | 1 set | Size for current and layout; values/quantities TBD |
| Small status display | Optional, 1 | Only if required; select module dimensions/interface after controller and power budget. Not part of the existing project description |

## Compact electronics candidates

The classic Arduino Nano is 45 × 18 mm. It is a proposed compact controller, not evidence of which board was originally used.

Source: https://docs.arduino.cc/hardware/nano

If the DFRobot sensor is SEN0240, its signal conditioner and dry-electrode board are each 22 × 35 mm. The sensor supply range is 3.3–5.5 V, and its analog output spans 0–3 V around a 1.5 V reference. Confirm the SKU before final wiring.

Source: https://wiki.dfrobot.com/sen0240/

Reserve space for connectors and cable bends, not just PCB outlines. The electrode belongs at the forearm sensing site. Forearm-mounted actuators/power are an option to evaluate if the palm cannot accommodate them; this would require revising tendon routing and friction assumptions.

## Signal-processing implication

SEN0240 provides a fluctuating EMG signal; simply averaging the raw waveform can cancel activity around its baseline. For a new implementation, estimate/remove the baseline, filter as appropriate, then compute a rectified or RMS activity measure and smooth it before applying calibrated thresholds. Verify the actual former code before describing its processing historically.

DFRobot's example uses filtering and squared filtered samples. Preserve its OYMotion copyright/licence notice if reusing that code or its library.

Source: https://wiki.dfrobot.com/sen0240/docs/20737

## Cost status

The existing mechanical BOM records £107.59 for five hands, or £21.52 per hand rounded. Its listed items are screws, tendon/cord, elastic bands, padding, fingertip grips and straps.

This is a historical mechanical-parts subtotal, not a current supplier quotation or complete bionic-hand cost. It does not establish costs for printing, servos, EMG sensing, controller, battery, regulators, wiring or tools. Do not add the individual listed components again on top of this subtotal.

A complete total remains TBD. Record quantity, unit price, source, quote date, shipping/tax and owned-versus-to-buy status when the component choices are fixed.
