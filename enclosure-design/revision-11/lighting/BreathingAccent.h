#pragma once
#include <Arduino.h>
#include <math.h>

// One PWM output controls four resistor-limited LED branches through a
// logic-level N-channel MOSFET. Pass a VERIFIED unused PWM pin from setup().
// No delay(), no I2C calls, no changes to the central RGB status light.
class BreathingAccent {
 public:
  void begin(uint8_t pwmPin, uint8_t maximum = 160, uint32_t cycleMs = 4000) {
    pin_ = pwmPin;
    maximum_ = maximum;
    cycle_ = cycleMs < 1000 ? 1000 : cycleMs;
    start_ = millis();
    last_ = start_;
    pinMode(pin_, OUTPUT);
    analogWrite(pin_, 0);
    begun_ = true;
  }
  void update(uint32_t now) {
    if (!begun_ || uint32_t(now - last_) < 20) return;
    last_ = now;
    const float phase = float(uint32_t(now - start_) % cycle_) / float(cycle_);
    const float ease = 0.5f - 0.5f * cosf(6.28318530718f * phase);
    // Gentle gamma-like shaping: soft minimum, smooth maximum and minimum.
    const uint8_t duty = uint8_t(maximum_ * ease * ease + 0.5f);
    analogWrite(pin_, duty);
  }
  void off() {
    if (begun_) analogWrite(pin_, 0);
    begun_ = false;
  }
 private:
  uint8_t pin_ = 0, maximum_ = 160;
  uint32_t cycle_ = 4000, start_ = 0, last_ = 0;
  bool begun_ = false;
};
