// SPDX-License-Identifier: MIT
#pragma once
#include <stdint.h>

// One EMG channel commands all three servo groups together.
class HandControl {
 public:
  uint32_t level = 0, threshold = 100;
  bool calibrated = false, closed = false, fault = false;

  void sample(int filtered, int raw, bool armed) {
    // 32-sample mean of squared, filtered EMG. Use 32-bit multiplication on AVR.
    int32_t v = filtered;
    if (v > 2047) v = 2047;
    if (v < -2047) v = -2047;
    sum -= history[index];
    history[index] = uint32_t(v * v);
    sum += history[index];
    index = (index + 1) % 32;
    level = sum / 32;

    // SEN0240 output is 0–3 V on the classic Nano's default 5 V ADC range.
    // A 1 Mohm A0-to-GND resistor makes an unplugged signal tend towards zero.
    bad = (raw < 2 || raw > 650) ? bad + 1 : 0;
    if (bad >= 50) fault = true;  // Reset is required after a fault.

    if (!calibrated) {
      ++samples;
      if (samples > 1000 && level > restPeak) restPeak = level;
      if (samples >= 5000) {
        threshold = restPeak * 3 + 25;
        if (threshold < 100) threshold = 100;
        calibrated = true;
      }
      closed = false;
      return;
    }
    if (!armed || fault) {
      closed = false; activeCount = 0; holdCount = 0; waitingForRest = true;
      return;
    }
    if (level < threshold / 2) {
      closed = false; activeCount = 0; holdCount = 0; waitingForRest = false;
    } else if (!closed && !waitingForRest) {
      activeCount = level > threshold ? activeCount + 1 : 0;
      if (activeCount >= 80) closed = true;
    }
    if (closed && ++holdCount >= 3000) {
      closed = false; waitingForRest = true; activeCount = 0; holdCount = 0;
    }
  }

 private:
  uint32_t history[32] = {}, sum = 0, restPeak = 0;
  uint16_t samples = 0, bad = 0, activeCount = 0, holdCount = 0;
  uint8_t index = 0;
  bool waitingForRest = true;
};
