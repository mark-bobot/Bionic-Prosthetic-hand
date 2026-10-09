// SPDX-License-Identifier: MIT
#pragma once
#include <stdint.h>

// One EMG channel commands all three servo groups together.
class HandControl {
 public:
  uint32_t level = 0, threshold = 100;
  bool calibrated = false, closed = false, fault = false, enabled = false;

  void sample(int filtered, int raw, bool armed) {
    // Filter first, then average signal power so positive/negative EMG does not cancel.
    level = averageActivity(filtered);

    // SEN0240 output is 0–3 V on the classic Nano's default 5 V ADC range.
    // A 1 Mohm A0-to-GND resistor makes an unplugged signal tend towards zero.
    if (raw < 2 || raw > 650) {
      if (bad < 50) ++bad;
    } else bad = 0;
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
    // Observe a released switch AFTER calibration. A switch held at startup
    // must never enable outputs, even when the signal looks relaxed.
    if (!armed) {
      if (releaseCount < 50) ++releaseCount;
      armReleased = releaseCount >= 50; // 50 ms release qualification at 1 kHz.
    } else releaseCount = 0;
    enabled = armed && armReleased && !fault;
    if (!enabled) {
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
  static const uint8_t AVERAGE_SAMPLES = 32; // 32 ms at 1 kHz sampling.

  uint32_t averageActivity(int filtered) {
    int32_t value = filtered;
    if (value > 2047) value = 2047;
    if (value < -2047) value = -2047;
    sum -= history[index];              // Remove the oldest sample.
    history[index] = uint32_t(value * value);
    sum += history[index];              // Add the newest sample.
    index = (index + 1) % AVERAGE_SAMPLES;
    return sum / AVERAGE_SAMPLES;
  }

  uint32_t history[AVERAGE_SAMPLES] = {}, sum = 0, restPeak = 0;
  uint16_t samples = 0, bad = 0, activeCount = 0, holdCount = 0;
  uint8_t index = 0, releaseCount = 0;
  bool waitingForRest = true, armReleased = false;
};
