# Bill of materials — three-servo prototype

One thumb servo, one index/middle servo and one ring/little servo. The current hand is the [original Phoenix v3 adaptation](cad/phoenix_v3/README.md); the costs below remain the revision B baseline. Compact-housing/cradle hardware and any fitted socket are not yet fully costed. This is the complete **reference build list**, including power and mounting consumables. Physical servo fit, hand sizing and load validation remain open; do not treat it as a purchase-ready matched kit.

**Current rounded-cover hardware:** four M3 through-fastener sets, with heads at most 6 mm diameter × 2 mm high to fit the recesses. Front/rear overall housing heights are 65/59 mm; measure from the recessed screw seat to the nut before selecting or trimming lengths. The older M3 × 45 revision B row below does not fit this housing. Inspect the 1 mm screw-seat thickness in a print sample. Switches need measured bushings and nuts for the 3 mm recessed panel. See [current housing notes](cad/compact/README.md).

[Wiring](docs/WIRING.md) · [CAD](cad/README.md) · [Firmware](firmware/README.md)

All monetary values below are **GBP planning allowances**, except the explicitly historical mechanical subtotal. They are not claimed as current quotes. They exclude shipping, taxes not included in a seller price, tools and labour. Owned items are included to show replacement cost.

| Item | Qty | Allowance each (£) | Line (£) | Selection / notes |
| --- | ---: | ---: | ---: | --- |
| Phoenix mechanical supplies | 1 | 21.52 | 21.52 | Screws, return bands, hand tendons, padding, fingertip grips and hand straps; existing five-hand purchase average |
| Phoenix printed parts | 1 | 8.00 | 8.00 | One hand set; filament allowance, scale dependent |
| Printed actuator add-ons | 1 | 9.00 | 9.00 | Integrated base ×1, lid ×1, spools ×3, equalisers ×2, fairleads ×3 |
| 25 kg·cm positional servo, 180° | 3 | 12.00 | 36.00 | Owned generic units; DS3225 only a reference; verify before purchasing |
| Classic Arduino Nano | 1 | 25.00 | 25.00 | A000005 / ATmega328P, 5 V; selected controller |
| DFRobot SEN0240 EMG kit | 1 | 45.00 | 45.00 | Owned; kit includes dry electrode, signal board, belt and leads |
| Pololu D24V90F5 servo regulator | 1 | 32.00 | 32.00 | Fixed 5 V; verify thermal/current headroom in enclosure |
| Pololu D24V5F5 logic regulator | 1 | 10.00 | 10.00 | Fixed 5 V / 500 mA class |
| Protected 2S battery pack | 1 | 18.00 | 18.00 | 7.4 V nominal, 1,000 mAh; ≥10 A discharge, balancing/undervoltage protection; reference CAD pocket assumes a 70 × 32 × 22 mm pack |
| Matching 2S charger | 1 | 20.00 | 20.00 | Match chemistry and pack connector; off-device charging |
| Metal servo horn | 3 | 3.00 | 9.00 | Spline must match actual servo; two holes must match spool slots |
| M2 bolts, nuts and washers | 1 | 2.00 | 2.00 | Six bolts plus six nuts/washers for three horns; length selected after horn fit |
| 4.8 mm cable ties | 6 | 0.10 | 0.60 | Three servo restraints plus three fairlead restraints; retain spares |
| 25 mm carrier straps | 2 | 2.00 | 4.00 | Separate from original hand straps; length to suit fixture/cuff |
| Carrier foam pad | 1 | 2.00 | 2.00 | 196 × 110 mm starting footprint; supplementary to hand padding |
| M3 lid hardware | 1 | 2.00 | 2.00 | Four M3 × 45 screws, nuts and washers; shorten and deburr screws to fit 41 mm stack |
| Insulating mounting pads and battery strap | 1 | 3.00 | 3.00 | Nominal 1 mm board mounting layer; 10 mm soft battery strap |
| PTFE liner | 1 | 2.00 | 2.00 | 2 mm OD / 1 mm ID, 0.5 m stock; cut guide inserts as needed |
| Additional braided tendon | 1 | 2.00 | 2.00 | 2 m allowance for actuator routing, nominal 0.5–0.8 mm; check knots and creep |
| Main switch | 1 | 3.00 | 3.00 | ≥10 A DC at battery voltage; CAD assumes 12 mm bushing and 16 × 20 × 20 mm body |
| 7.5 A fuse and holder | 1 | 3.00 | 3.00 | Fuse at battery; verify inrush and wire protection in testing |
| Arm toggle switch | 1 | 1.00 | 1.00 | Low-current SPST, D2 to GND; CAD assumes 6 mm bushing, 10 × 10 × 12 mm body |
| Power wiring and connectors | 1 | 6.00 | 6.00 | 18 AWG main leads, keyed ≥10 A connectors, distribution and insulation |
| Signal wiring / small perfboard | 1 | 3.00 | 3.00 | Short connections, strain relief, no breadboard motor-power path |
| Capacitors | 1 | 1.00 | 1.00 | 1,000 µF 10 V; 10 µF 10 V; 100 nF ceramic |
| Resistors | 1 | 0.20 | 0.20 | 220 Ω ×3, 1 MΩ ×1 |

**Planning total: £268.32, including £20 for the charger.** If all three servos and the complete EMG kit are already owned, subtract £81: remaining allowance £187.32. This is not a verified shopping total.

## Sources and quantities

- SEN0240 identity and kit contents: [DFRobot](https://www.dfrobot.com/product-1661.html). Manufacturer listing checked 26 September 2026: US$49.50; the £45 above is an allowance, not a currency conversion or UK quote.
- Nano dimensions and board identity: [Arduino](https://docs.arduino.cc/hardware/nano). Use the classic 5 V board, not a differently powered Nano variant.
- Servo reference dimensions/electrical data: [DS3225 datasheet](https://dsservo.com/d_file/DS3225%20datasheet.pdf). The owned model remains unknown.
- Servo regulator: [Pololu #2866](https://www.pololu.com/product/2866), manufacturer listing US$36.82 on the check date. Available continuous current depends on cooling/input voltage; "9 A" is not a guaranteed enclosure rating.
- Logic regulator: [Pololu #2843](https://www.pololu.com/product/2843), manufacturer listing US$8.95 on the check date.
- The original mechanical list records £107.59 for five hands, or £21.52 each rounded. This is the first row only; those hand supplies are not separately charged again. The carrier straps, padding and extended tendons are additional.
- Exact Phoenix pin/screw/band counts depend on the selected hand scale and official assembly instructions. The original-hand row is a supplies set, not a claim that these individual quantities have been verified. [Phoenix v3 source and instructions](https://hub.e-nable.org/p/devices?p=e-NABLE+Phoenix+Hand+v3).

No display is included in this simple version. The Nano LED indicates calibration/fault status; a screen would add code, wiring and space without helping the first mechanical test. A soldering iron, multimeter, force gauge, ruler/calipers, printer and suitable battery charger are needed; the charger is costed above, other tools are excluded.

Revision B includes an electronics enclosure and assumed battery pocket; see [integration details](cad/INTEGRATION.md). There is no completed wearable cuff. Regulator mounting must provide insulation and ventilation. Final part orders still require checking the owned servo spline, voltage and dimensions, plus battery/charger compatibility.
