# Draft bill of materials

Status: preliminary; quantities, prices and fit are not final. Updated 26 September 2026.

[Servo sizing](SERVO-SIZING.md) · [Tendon measurement guide](TENDON-TEST.md) · [Remaining work](TODO.md)

## Parts

| Item | Preliminary quantity per hand | Selection/status |
| --- | --- | --- |
| Modified Phoenix Hand v3 printed parts | 1 set | Hand size, CAD modifications and print material to confirm |
| Generic 25 kgf·cm, 180° servo | 1 for paired-finger test; potentially 3 for a five-digit layout | Owner reports possession; exact models, quantity owned and rated voltage unknown. Three actuators for 2+2+1 is a proposal, not the documented original mapping |
| Servo horn, screw and grooved tendon drum | 1 per actuator | Confirm spline; candidate 10–12 mm effective radius subject to measured travel and torque |
| Paired-finger coupling/equaliser | As required | Determine from unequal finger travel and object contact |
| DFRobot EMG sensor kit | 1 | SEN0240 Gravity Analog EMG Sensor by DFRobot/OYMotion: catalogue match to the owner's DFRobot dry-electrode description |
| Compact Arduino controller | 1 | Classic Arduino Nano selected for this build; original board model unspecified |
| Servo power regulator/BEC | 1 appropriately rated branch | Plan around a regulated 5 V servo branch using DS3225 as the reference; actual servo compatibility and measured peak current still need checking |
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

## Selected electronics

The classic Arduino Nano is 45 × 18 mm. The classic Nano is selected for this build. Allow extra room for connectors, wires and mounting.

Source: https://docs.arduino.cc/hardware/nano

DFRobot lists its Gravity Analog EMG Sensor by OYMotion, with metal dry electrodes, as SKU SEN0240. This matches the owner's description and is the BOM selection; the physical unit has not been inspected. Its signal conditioner and electrode board are each 22 × 35 mm. Supply is 3.3–5.5 V; analog output is 0–3 V around a 1.5 V reference.

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

## First wiring layout to develop

For the classic 5 V Nano, plan sensor A to A0, sensor + to a clean regulated 5 V logic/sensor rail, and sensor - to signal ground. The 0–3 V output fits the classic Nano's default 5 V ADC range. Do not assume that every Nano-family board uses 5 V logic.

One servo signal can use D9, with further signal pins assigned after the actuator count is settled. Power servos from their own adequately rated branch, not through the Nano. Join signal grounds deliberately and keep motor-return currents out of the sensor wiring. Put local decoupling near the electronics; choose values after the supply and wiring layout are fixed.

The DS3225 is a reference part for sizing, not an identification of the generic servo. Its specified supply range is 4.8–6.8 V. A regulated 5 V design point has published torque/current data and also suits the sensor, but the servo branch and clean sensor/logic branch must handle noise separately. The reference upper limit does not authorise applying 6.8 V to an unidentified servo. A two-cell lithium pack must not feed this reference servo directly: its fully charged voltage exceeds that range.

Source: https://dsservo.com/d_file/DS3225%20datasheet.pdf
