# Measuring tendon force and travel

The first test is mechanical: leave the servo disconnected and find out how hard, and how far, each tendon has to be pulled. This measures the assembled hand, including the friction and return bands that are difficult to estimate from CAD.

## Equipment

- A force gauge or spring balance. A 0–50 N range is a useful starting point for one finger; use a larger range if the load approaches the limit.
- A ruler, a fine marker and a way to hold the palm firmly without distorting it.
- The actual tendon line, guides and return bands.
- A phone video can help match the force reading to finger position.

A luggage scale can give a rough reading, but check its minimum load and resolution. Some only lock a reading after a steady pull and will miss a short peak. A balance reading in kilograms is indicating kilogram-force here: multiply by 9.81 to obtain newtons. For example, 1.5 kg on the scale is about 14.7 N.

## One finger at a time

1. Disconnect power and unhook the tendon from the servo. Keep its route through the hand unchanged.
2. Secure the palm on the bench. Do not test with the hand strapped to a person.
3. Attach the scale to the tendon at the point where the servo would pull. Pull in the same direction as the planned drum tangent; pulling sideways changes the result.
4. Zero the scale in the test orientation. Take up loose slack without starting to close the finger, then mark the tendon against a fixed reference.
5. Pull slowly until the finger reaches its intended closed position. Stop at normal closure, not after forcing it against a hard stop.
6. Record the largest reading during the movement, not just the reading at the end. Note any sticking or sudden jumps.
7. Measure how far the tendon mark moved. This is tendon travel; it is not fingertip travel.
8. Release and check that the finger reopens. Repeat five times. Keep the highest measured pull for sizing and retain all readings.
9. Repeat at approximately the intended closing speed. The slow test alone does not capture acceleration or all dynamic effects.

If the scale itself stretches, measure the tendon mark relative to the hand, not the movement of the scale handle.

| Finger | Trial | Peak scale reading, kgf | Peak force, N | Tendon travel, mm | Return-band setup / sticking |
| --- | --- | --- | --- | --- | --- |
| | 1 | | | | |
| | 2 | | | | |
| | 3 | | | | |
| | 4 | | | | |
| | 5 | | | | |

## The two-finger test

For a first approximation, add the highest separate readings. This is conservative if their peaks occur at different points, but it cannot show how the coupling behaves.

Next, test the intended coupling or use a temporary crossbar that pulls both lines in the intended direction. If it does not reproduce the final geometry, record that difference. Watch whether one finger finishes closing first and whether the other still moves without excessive line tension.

Repeat around a chosen object and record its size and shape. Stop when contact is established; do not pull harder just to obtain a high reading. This checks closure around that object. Quantifying grip or object retention is a separate test.

## Use the measurements

Because the scale is at the servo end and the tendon passes through the actual guides, the reading already includes those routing losses. Do not add the assumed 40% friction loss a second time.

For two grooves of equal effective radius:

    torque_needed = 1.5 × (F1 + F2) × r

F is in newtons, r is in metres and torque is in N·m. The factor 1.5 is a provisional load margin.

If radii differ, use 1.5 × (F1 × r1 + F2 × r2). A lever or differential coupling needs its own force/displacement ratio.

### Worked example — invented numbers to show the method

Suppose finger A peaks at 1.2 kgf, finger B at 1.5 kgf, and the drum radius is 10 mm:

    total pull = (1.2 + 1.5) × 9.81 = 26.49 N
    torque with margin = 1.5 × 26.49 × 0.010 = 0.397 N·m

The DS3225 reference has a 5 V stall specification of 21 kgf·cm. Using the provisional 40% working allowance gives 0.824 N·m. This example is below that allowance, but actual servo temperature, current and duty still need checking.

For travel, suppose the measured requirement is 24 mm and we reserve 3 mm for slack/stretch. Over a calibrated 160° sweep:

    minimum radius = (24 + 3) / (160 × pi / 180) = 9.7 mm

A 10 mm drum would just meet that illustrative travel requirement. If the real requirement is longer, increase the radius and repeat the torque calculation. Keep line winding in one layer so the radius stays predictable.

## Send back these results

- Finger names, maximum force and travel for each.
- Paired maximum force and whether either finger stops early.
- Return-band arrangement and any sticking.
- Drum radius and available angular movement, if already built.
- Servo label or old order details if they turn up.

These readings will let us replace assumptions in [SERVO-SIZING.md](SERVO-SIZING.md) with measurements.
