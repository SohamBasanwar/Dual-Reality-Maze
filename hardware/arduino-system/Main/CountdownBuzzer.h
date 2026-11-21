#pragma once
#include <stdint.h>

// Current chapters last ten minutes: halfway is 300 seconds remaining.
// Return at most one warning per update, even after a delayed packet.
class CountdownBuzzer {
  bool tracking=false;
  uint16_t previous=0;
public:
  uint16_t observe(uint16_t seconds, bool playing) {
    if(!playing){tracking=false;return 0;}
    if(!tracking || seconds>previous){tracking=true;previous=seconds;return 0;}
    const uint16_t marks[]={300,180,120,60,50,40,30,25,20,15,10,9,8,7,6,5,4,3,2,1};
    uint16_t warning=0;
    for(uint8_t i=0;i<sizeof(marks)/sizeof(marks[0]);i++)
      if(previous>marks[i] && seconds<=marks[i])warning=marks[i];
    previous=seconds;
    // At expiry, stop rather than replaying an already missed warning.
    return seconds?warning:0;
  }
};
