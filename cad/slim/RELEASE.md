# Smaller-part layout candidate 0.3.0

Start with `cad/slim/README.md`, which selects the appropriate parts and explains the power changes. The generic-servo baseline remains documented separately in `BUILD.md`.

This candidate replaces the tall reference servos with low-profile FT5425BL bodies and lowers the Nano connection allowance. The housing changes from 94 × 160 × 60 mm to 94 × 160 × 50 mm; housing plus cassette height changes from 73 to 63 mm. Phoenix hand geometry, socket, thumb placement and spool radius are retained. Editable sources, STEP/STL files, component layout, voltage-dependent force calculations and a replacement BOM are included.

Servo ears, shafts, horns, plug access and the Nano installed height remain assumed envelopes. The direct protected-2S servo supply is a change from the earlier regulated-5V system. Actual battery/protection/disconnect/fuse/wire/connector selection is still required; the old electrical parts are not approved substitutes. No actual grip, runtime, temperature or patient-fit performance is claimed. Firmware is retained with its small setup sweep; it has no new current/force feedback.

Pack solids and the modified lid pass mesh/solid checks; modelled component/fixture pairs and the complete static assembly pass intersection checks. This is geometric evidence only, subject to the explicitly assumed bought-part envelopes.
