#include <cassert>
#include <vector>
#include "arduino-system/Main/CountdownBuzzer.h"
int main(){
 CountdownBuzzer timer;std::vector<int> actual;
 for(int second=600;second>=0;--second){
  auto beep=timer.observe(second,true);if(beep)actual.push_back(beep);
  for(int duplicate=0;duplicate<20;duplicate++)assert(timer.observe(second,true)==0);
 }
 assert((actual==std::vector<int>{300,180,120,60,50,40,30,25,20,15,10,9,8,7,6,5,4,3,2,1}));
 assert(timer.observe(600,true)==0);assert(timer.observe(301,true)==0);
 assert(timer.observe(299,true)==300); // A skipped threshold still warns once.
 assert(timer.observe(299,false)==0);assert(timer.observe(299,true)==0);
 assert(timer.observe(298,true)==0); // Resume does not replay halfway.
 assert(timer.observe(21,true)==25); // Coalesce missed warnings, never a burst.
 assert(timer.observe(20,true)==20);
 assert(timer.observe(19,false)==0);assert(timer.observe(18,true)==0);
 assert(timer.observe(0,true)==0);
}
