# Forearm-integrated Phoenix design candidate

The separate box above the arm has been replaced by split curved forearm shells. Motors, battery, Nano, EMG conditioner and the three tendon lanes are inside. The lower shell includes a servo shelf and battery cradle; controls sit in a top recess. The original Phoenix palm and finger surfaces are retained, with corrected index/ring distal-part assignment and revised open thumb spread.

Start with `cad/forearm/README.md` in the ZIP. It selects seven new print parts, the reused spools/equalisers/electrode carrier and the original Phoenix hand. Use `cad/forearm/exports/complete_forearm.step` for assembly placement. Old top-box layouts are retained as history, not as the current print list.

Validation: valid single-solid new parts and watertight positive-volume STL meshes; clear modelled static assembly and reserved limb volume; 21 sampled tendon-mechanism positions plus a modest finger-flexion pose. No physical build or load test was performed.

Two important limits remain: the design assumes 160 mm from residual-limb end to wrist, and deeper PIP flexion produces small overlaps between original source parts in the placement diagnostic. Full closure and recipient fit are not accepted. Actual replacement servos, high-current 2S power parts, wiring, tendons, fasteners and thermal duty still need bench verification. The old generic-servo 5 V wiring is not the selected candidate's power topology.

Mechanical CAD/documentation retain CC BY 4.0 with original Phoenix attribution; firmware licensing is unchanged. This is a prerelease design package, not a validated prosthesis.
