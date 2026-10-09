# Firmware

**10 October 2026: servo outputs are disabled by default.** `SERVO_OUTPUTS_ENABLED = false` is a commissioning lock, not a human-use approval mechanism. Read [pre-human-test preparation](../docs/PRE-HUMAN-TEST.md) and [current wiring](../docs/WIRING.md). No person connected during initial commissioning.

Open `ProstheticHand/ProstheticHand.ino` in Arduino IDE. Select **Arduino Nano / ATmega328P** and install Arduino's **Servo** library. The OYMotion EMG filter is included beside the sketch, so there is no separate EMG library to install. Some older Nano bootloaders require the IDE's Old Bootloader option.

## The simple averaging step

Open `ProstheticHand/ProstheticHand.ino`; keep its helper files in the same folder. The sketch reads A0, filters the signal, averages its activity and moves the three groups together. The averaging helper in `HandControl.h` is:

```cpp
sum -= history[index];                 // oldest sample out
history[index] = uint32_t(value * value);
sum += history[index];                 // newest sample in
index = (index + 1) % AVERAGE_SAMPLES;
level = sum / AVERAGE_SAMPLES;          // mean of 32 consecutive activity samples
```

`value` is the filtered EMG after the arithmetic-range clamp. Squaring before averaging measures activity; averaging the raw signal alone would drift around its DC bias and can hide contraction. `AVERAGE_SAMPLES = 32` gives a 32 ms window at the 1 kHz sampling rate. Change the three `OPEN_US`/`CLOSE_US` pairs only after calibrating the real mechanisms. Calibration, arming and the hold timeout remain in the helper so the main sketch stays short.

## What it does

The sensor connects to A0. The code samples at nominally 1 kHz, uses OYMotion's 50 Hz notch/high-pass/low-pass filters, squares the filtered signal using 32-bit arithmetic, and averages 32 consecutive samples. This follows the processing direction of [DFRobot's SEN0240 example](https://wiki.dfrobot.com/sen0240/docs/20737), with averaging and servo control added.

On reset, keep the muscle relaxed for five seconds. The first second lets the filter settle; the remaining four estimate the largest resting activity. The closing threshold is three times that resting peak plus 25, with a minimum of 100. These are initial tuning choices, not universal physiological thresholds. Activity must exceed the threshold for 80 ms before closing. It must fall below half the threshold to reopen. A grip command times out after three seconds and requires relaxation before another grip.

There is one EMG channel. It commands all three groups together; it cannot independently select a finger or grip pattern.

| Pin | Connection |
| --- | --- |
| A0 | SEN0240 A; add 1 MΩ to GND |
| D2 | Normally-open momentary hold-to-enable switch to GND, internal pull-up |
| D9 | Thumb servo signal |
| D10 | Index/middle servo signal |
| D11 | Ring/little servo signal |
| 5V | Clean regulated 5 V logic supply; not servo power |
| GND | Shared signal reference, with motor returns routed separately |

## First run

1. Program with electrodes removed, servo supply off and external logic supply disconnected from the Nano. Unplug USB before body-connected battery testing.
2. On the fixture, provide a resting test input and leave the enable switch open. Wait five seconds. The LED lights when calibration completes; rapid blinking indicates a latched fault. Calibration alone does not enable outputs.
3. For the first servo check, remove horns/tendons and confirm motor model and supply. Deliberately set `SERVO_OUTPUTS_ENABLED = true` and recompile for the fixture test. Release the switch **after calibration** for at least 50 ms, then hold it to enable. A switch held across startup/reset remains inhibited. Simulate rest, activity and rest; never use a person as the initial test input. Reattaching commands `OPEN_US`; it does not know the motor's physical position.
4. `OPEN_US = 1100` and `CLOSE_US = 1300` are deliberately small test movements, not full closure. Determine unloaded endpoints one servo at a time, then attach loose tendons and increase travel gradually. Never use nominal angle alone to establish the real range. Change the arrays separately if a servo must turn in the other direction.
5. Set `PLOT = true` only for diagnostic logging using an appropriately isolated arrangement, or with electrodes disconnected. Output columns are activity, threshold and close command. Do not connect a mains-connected computer while electrodes are worn.

A signal that stays above threshold prevents a new grip after rearming or timeout. Motor noise can trigger false contractions: test with motor power off and on before loaded tendons. Wearer calibration is a separate professionally reviewed stage. A lost or noisy electrode can still look plausible.

## Limits

The software does not measure tendon tension, grip force, temperature or actual finger position. The ADC rail check can catch some broken connections but cannot reliably detect electrode loss: a disconnected/noisy electrode can still look valid. The arm switch detaches servo signals; servo gearing may remain resistant to movement. It is not an emergency mechanical release. The main power switch and accessible tendon release remain necessary for bench work.

A sampling delay of at least 2 ms latches a fault. The loop schedule has not been measured on hardware; the compiled firmware is not a real-time validation result.

## Reproduce checks

```
arduino-cli core install arduino:avr
arduino-cli lib install Servo
arduino-cli compile --fqbn arduino:avr:nano:cpu=atmega328 firmware/ProstheticHand
c++ -std=c++11 tests/control_test.cpp -o /tmp/control_test
/tmp/control_test
```

Original control code: MIT. Included `EMGFilters.cpp` and `.h`: OYMotion BSD-2-Clause, with notices retained. Source linked by DFRobot: https://github.com/YeezB/EMG_Filter at commit `867fa1d30244b22f28a68787adfd5648066c4736`. Arduino Servo is an external LGPL-2.1-or-later dependency; no firmware binary is distributed here.
