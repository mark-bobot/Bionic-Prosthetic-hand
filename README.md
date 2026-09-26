# Bionic Prosthetic Hand

A three-servo adaptation of the e-NABLE Phoenix Hand v3, using a DFRobot SEN0240 dry-electrode EMG sensor and an Arduino Nano.

One servo drives the thumb, one drives the index and middle fingers, and one drives the ring and little fingers. A muscle contraction closes the groups together; relaxing opens them. The design uses a separate forearm carrier so the original palm and fingers can stay unchanged.

## Build files

- [Arduino code and setup](firmware/README.md)
- [Wiring diagram](docs/WIRING.md)
- [Editable CAD, STEP and printable STL files](cad/README.md)
- [Bill of materials and cost allowances](BOM.md)
- [Torque and tendon-travel calculations](SERVO-SIZING.md)
- [Measuring tendon force](TENDON-TEST.md)
- [Checks performed](VALIDATION.md)
- [What remains](TODO.md)

![Three-servo carrier](cad/exports/carrier_preview.png)

## Status

This is a newly reconstructed bench-prototype design. The Nano sketch compiles and the software control tests pass. The generated CAD passes solid/mesh checks. The hardware has not been assembled or tested: motor fit, tendon load, grip performance, electrical noise and thermal performance remain unverified.

The servos owned for this project are generic units advertised as 25 kg·cm with 180° travel. DS3225 dimensions and 5 V electrical specifications are used as a reference, not as identification of those units. The initial code uses a small test movement; calibrate endpoints before expecting full finger closure.

The source project description mentions improved electrode contact, averaging sensor readings, tendon actuation and sharing a servo between two fingers. The files here implement a new version of that idea; they are not recovered original firmware or CAD, and do not establish earlier test results.

## Original design

Phoenix Hand v3 is credited by [e-NABLE](https://hub.e-nable.org/p/devices?p=e-NABLE+Phoenix+Hand+v3) to Jason Bryant, John Diamond, Scott Darrow, Andreas Bastian, Team Unlimbited, e-NABLE France and Jeremy Simon. It derives from Phoenix Hand v2 and Unlimbited Phoenix Hand, with labelled pins among the v3 changes.

The [original Thingiverse design](https://www.thingiverse.com/thing:4056253) is CC BY 4.0. The official STEP file is included unchanged; new carrier, spool, guide and equaliser parts are separate. The mechanical change is rerouting wrist-driven tendons to external servo actuation. No endorsement by the original designers is implied.

## Licences

Documentation and mechanical CAD: **CC BY 4.0**. Original firmware: **MIT**. Included OYMotion filter files: **BSD-2-Clause**, with their notices retained. Arduino's Servo library is an external **LGPL-2.1-or-later** dependency. See [LICENSE.md](LICENSE.md).

This is an educational bench prototype, not a validated fitted prosthesis.
