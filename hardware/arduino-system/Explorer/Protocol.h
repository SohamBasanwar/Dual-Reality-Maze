#pragma once
#include <Arduino.h>
const uint8_t EXPLORER=0x10, ARCHITECT=0x11, PACKET_SIZE=12;
inline uint8_t checksum(const uint8_t* b,uint8_t n){uint8_t c=0;while(n--)c^=*b++;return c;}
inline uint16_t wordAt(const uint8_t* b,uint8_t i){return uint16_t(b[i])|(uint16_t(b[i+1])<<8);}
inline void putWord(uint8_t* b,uint8_t i,uint16_t v){b[i]=v;b[i+1]=v>>8;}
// Common-cathode RGB: each colour MUST have its own 330 ohm resistor.
const bool RGB_COMMON_ANODE=false;
inline void rgb(bool r,bool g,bool b){digitalWrite(3,r^RGB_COMMON_ANODE);digitalWrite(5,g^RGB_COMMON_ANODE);digitalWrite(6,b^RGB_COMMON_ANODE);}
inline void initRGB(){pinMode(3,OUTPUT);pinMode(5,OUTPUT);pinMode(6,OUTPUT);rgb(1,0,0);}
