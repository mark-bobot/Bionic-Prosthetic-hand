// SPDX-License-Identifier: MIT
// Nano + DFRobot SEN0240. OYMotion filter files retain their BSD-2-Clause licence.
#include <Servo.h>
#include "EMGFilters.h"
#include "HandControl.h"

const byte EMG_PIN = A0;
const byte ARM_PIN = 2;             // Toggle switch to GND; open switch = disarmed.
const byte SERVO_PINS[] = {9, 10, 11}; // Thumb, index+middle, ring+little.
// Small initial test movement, NOT calibrated full-hand endpoints.
// First test with horns/tendons disconnected. Adjust each pair for your linkage.
const int OPEN_US[]  = {1100, 1100, 1100};
const int CLOSE_US[] = {1300, 1300, 1300};
const int STEP_US = 10;             // Every 20 ms; limits commanded closing rate.
const bool PLOT = false;            // Diagnostic serial output, 20 Hz.

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

  uint32_t ms = millis();
  if (ms - lastServo >= 20) {
    lastServo = ms;
    for (byte i = 0; i < 3; ++i) {
      bool enabled = hand.calibrated && !hand.fault && digitalRead(ARM_PIN) == LOW;
      if (!enabled) {
        servos[i].detach();         // Removes command; does NOT guarantee mechanical release.
        positionUs[i] = OPEN_US[i];
        continue;
      }
      if (!servos[i].attached()) {
        servos[i].writeMicroseconds(OPEN_US[i]);
        servos[i].attach(SERVO_PINS[i], 500, 2500); // DS3225 reference bounds; verify actual unit.
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
