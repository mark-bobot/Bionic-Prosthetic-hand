# Current build entry point

**Selected engineering candidate: bottom tendon drive. Intended future use: a fitted device for one wearer. Status: NOT READY FOR FITTED USE OR PRODUCTION.**

Start with [one-wearer build preparation](release/production/README.md), then the [matched mechanical guide](cad/bottom_drive/README.md). Use the [current package verifier](release/production/package.py). Older integrated-forearm, upright-box and historical 0.2.1 kits are separate designs; do not combine their shells, receivers, covers or power specifications.

The current assembly retains the original Phoenix hand and uses three inverted FT5425BL replacement-servo references: thumb, index/middle, ring/little. The Nano and SEN0240 remain; battery/power supply is external. This does not identify the generic motors already owned.

Seven new print types make eight pieces. The complete STEP is an assembly reference, not a print-in-place file. The arm carrier remains a placeholder until wearer-specific socket, suspension and alignment are established by an appropriate fitting professional.

The most immediate mechanical gate is the horn/drum fastener stack: head projection ≤1.2 mm leaves only 0.6 mm nominal floor clearance. Verify real tolerances, fasteners and deflection before selecting the print. Full external tendon routing, wrist restraint, manual release, strength, electrical/thermal behaviour and durability remain unaccepted.

[Arduino setup and limits](firmware/README.md) · [Tendon measurements](TENDON-TEST.md) · [Open production/fitting gates](release/production/readiness.json) · [Validation evidence](VALIDATION.md)

The firmware is development code. Inversion requires unloaded winding-direction and endpoint calibration. No physical force feedback, validated electrode-loss detection or mechanical release is supplied by the control code.
