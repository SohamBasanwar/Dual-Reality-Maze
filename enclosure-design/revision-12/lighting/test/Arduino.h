#pragma once
#include <cstdint>
constexpr int OUTPUT=1;
extern uint32_t clockMs;
extern int duty,writeCount,configuredPin;
inline uint32_t millis(){return clockMs;}
inline void pinMode(uint8_t pin,int){configuredPin=pin;}
inline void analogWrite(uint8_t pin,int value){configuredPin=pin;duty=value;++writeCount;}
