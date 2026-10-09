// SPDX-License-Identifier: MIT
// Nano + DFRobot SEN0240. OYMotion filter files retain their BSD-2-Clause licence.
#include <Servo.h>
#include "EMGFilters.h"
#include "HandControl.h"

const byte EMG_PIN = A0;
const byte ARM_PIN = 2;             // Normally-open hold-to-enable switch to GND.
const byte SERVO_PINS[] = {9, 10, 11}; // Thumb, index+middle, ring+little.
// Small initial test movement, NOT calibrated full-hand endpoints.
// First test with horns/tendons disconnected. Adjust each pair for your linkage.
const int OPEN_US[]  = {1100, 1100, 1100};
const int CLOSE_US[] = {1300, 1300, 1300};
const int STEP_US = 10;             // Every 20 ms; limits commanded closing rate.
const bool PLOT = false;            // Diagnostic serial output, 20 Hz.
// Shipping configuration: signal processing only, NO servo pulses.
// Set true only for supervised fixture commissioning with horns/tendons removed.
// This setting is not permission for human use. See docs/PRE-HUMAN-TEST.md.
const bool SERVO_OUTPUTS_ENABLED = false;

Servo servos[3];
EMGFilters filter;
HandControl hand;
int positionUs[3];
uint32_t nextSample, lastServo = 0, lastPlot = 0;

void setup() {
  pinMode(ARM_PIN, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(115200);
  filter.init(SAMPLE_FREQ_1000HZ, NOTCH_FREQ_50HZ, true, true, true);
  // Match DFRobot's 1 kHz filtering and squared activity, then average it.
  nextSample = micros();
  for (byte i = 0; i < 3; ++i) positionUs[i] = OPEN_US[i];
  // Servos remain detached during the five-second relaxed calibration.
}

void loop() {
  uint32_t now = micros();
  if ((int32_t)(now - nextSample) < 0) return;
  if (now - nextSample >= 2000) {
    hand.fault = true;              // Timing was lost: reset and recalibrate.
    nextSample = now;
  }
  nextSample += 1000;
  int raw = analogRead(EMG_PIN);
  hand.sample(filter.update(raw), raw, digitalRead(ARM_PIN) == LOW);

  bool enabled = SERVO_OUTPUTS_ENABLED && hand.enabled;
  // Detach on the next sample, rather than waiting for a 20 ms servo update.
  // Firmware can hang; this is NOT a hardwired disconnect or a grip release.
  if (!enabled) {
    for (byte i = 0; i < 3; ++i) {
      servos[i].detach();
      positionUs[i] = OPEN_US[i];
    }
  }

  uint32_t ms = millis();
  if (ms - lastServo >= 20) {
    lastServo = ms;
    for (byte i = 0; i < 3; ++i) {
      if (!enabled) {
        continue;
      }
      if (!servos[i].attached()) {
        servos[i].writeMicroseconds(OPEN_US[i]);
        servos[i].attach(SERVO_PINS[i], 500, 2500); // FT5425BL reference only; verify actual unit.
      }
      int target = hand.closed ? CLOSE_US[i] : OPEN_US[i];
      if (positionUs[i] < target) positionUs[i] = min(positionUs[i] + STEP_US, target);
      if (positionUs[i] > target) positionUs[i] = max(positionUs[i] - STEP_US, target);
      servos[i].writeMicroseconds(positionUs[i]);
    }
    digitalWrite(LED_BUILTIN, hand.fault ? (ms / 150) % 2 : hand.calibrated);
  }
  if (PLOT && ms - lastPlot >= 50 && Serial.availableForWrite() >= 40) {
    lastPlot = ms;
    Serial.print(hand.level); Serial.print(' ');
    Serial.print(hand.threshold); Serial.print(' ');
    Serial.println(hand.closed ? hand.threshold : 0);
  }
}
