#include <cassert>
#include "arduino-system/Main/MazeMatrix.h"
int main(){
 uint8_t pixels[8][12];
 for(int fault=0;fault<2;fault++)for(int open=0;open<2;open++)for(unsigned tick=0;tick<80;tick++){
  mazeMatrixFrame(pixels,tick,open,fault);
  for(auto &row:pixels)for(auto pixel:row)assert(pixel==0 || pixel==1);
  if(fault)assert(pixels[6][5]==1);
  else if(!open)assert(pixels[4][7]==1);
 }
 mazeMatrixFrame(pixels,0,false,false);assert(pixels[6][1]==1);
 mazeMatrixFrame(pixels,1,false,false);assert(pixels[6][1]==0 && pixels[5][1]==1);
 mazeMatrixFrame(pixels,0,true,false);assert(pixels[4][7]==0);
}
