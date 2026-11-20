#include <cassert>
#include <cstdint>
#include <cstdio>
#include "../BreathingAccent.h"
uint32_t clockMs=0;
int duty=-1,writeCount=0,configuredPin=-1;
int main(){
 BreathingAccent a;
 a.update(100);assert(writeCount==0);
 a.begin(5);assert(duty==0 && configuredPin==5);
 int previous=0;
 for(uint32_t t=20;t<=2000;t+=20){a.update(t);assert(duty>=previous && duty<=160);previous=duty;}
 assert(duty==160);
 for(uint32_t t=2020;t<=4000;t+=20){a.update(t);assert(duty<=previous && duty>=0);previous=duty;}
 assert(duty==0);
 int writes=writeCount;a.update(4001);assert(writeCount==writes);
 a.off();assert(duty==0);writes=writeCount;a.update(6000);assert(writeCount==writes);
 clockMs=0xfffffff0u;a.begin(6,255,4000);a.update(0x000007c0u);assert(duty==255); // 2000 ms across rollover
 clockMs=100;a.begin(9,100,1);a.update(600);assert(duty==100); // clamped minimum 1000 ms period
 puts("PASS: real helper compiles; monotonic fade halves, cycle bounds, rate limit, off, reset and millis rollover.");
}
