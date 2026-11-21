#pragma once
#include <stdint.h>

// Original 12 x 8 pixel maze: explorer, opening gate, pulsing portal.
inline void mazeMatrixFrame(uint8_t (&pixels)[8][12],uint32_t tick,bool gateOpen,bool fault){
 const char* walls[]={"111111111111","100000000001","101010111101","101010100001","100000000001","101110111101","100000000001","111111111111"};
 const uint8_t path[][2]={{1,6},{1,5},{1,4},{2,4},{3,4},{3,3},{3,2},{4,2},{5,2},{5,3},{5,4},{6,4},{7,4},{8,4},{9,4},{10,4},{10,3},{10,2}};
 for(uint8_t y=0;y<8;y++)for(uint8_t x=0;x<12;x++)pixels[y][x]=fault?0:walls[y][x]=='1';
 if(fault){
  for(uint8_t y=1;y<5;y++)pixels[y][5]=1;
  pixels[6][5]=1;
  if((tick/3)%2){pixels[3][1]=pixels[3][2]=pixels[3][9]=pixels[3][10]=1;}
  return;
 }
 for(uint8_t i=0;i<sizeof(path)/sizeof(path[0]);i++)pixels[path[i][1]][path[i][0]]=0;
 pixels[3][7]=pixels[4][7]=pixels[5][7]=gateOpen?0:1;
 pixels[1][10]=pixels[2][9]=pixels[2][11]=pixels[3][10]=1;
 pixels[2][10]=(tick/2)%2;
 uint8_t step=tick%(gateOpen?18:12);
 pixels[path[step][1]][path[step][0]]=1;
}
