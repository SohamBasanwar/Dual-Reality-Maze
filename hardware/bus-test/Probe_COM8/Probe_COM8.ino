#include <Wire.h>
const byte ADDRESS=17;
volatile byte sample[16]={}; volatile uint16_t nonce=0,receives=0;
uint16_t seq=0,presses=0;unsigned long last=0,changed=0;
bool raw=false,stable=false;
byte crc(byte*b,int n){byte c=0;while(n--)c^=*b++;return c;}
void word(byte*b,int i,uint16_t n){b[i]=n;b[i+1]=n>>8;}
void request(){byte b[16];for(byte i=0;i<16;i++)b[i]=sample[i];word(b,8,nonce);word(b,10,receives);b[15]=crc(b,15);Wire.write(b,16);}
void receive(int n){byte b[4];int k=0;while(Wire.available()){byte c=Wire.read();if(k<4)b[k++]=c;}
 if(n==4&&k==4&&b[0]==0xC1&&crc(b,3)==b[3]){nonce=b[1]|uint16_t(b[2])<<8;receives++;}}
void setup(){Serial.begin(115200);pinMode(2,INPUT_PULLUP);Wire.begin(ADDRESS);Wire.onReceive(receive);Wire.onRequest(request);}
void loop(){
 bool current=digitalRead(2)==LOW;
 if(current!=raw){raw=current;changed=millis();}
 if(raw!=stable&&millis()-changed>=30){stable=raw;if(stable)presses++;}
 if(millis()-last>=10){last=millis();byte b[16]={0xD1,ADDRESS};word(b,2,seq++);word(b,4,analogRead(A0));word(b,6,analogRead(A1));b[12]=stable;word(b,13,presses);noInterrupts();for(byte i=0;i<16;i++)sample[i]=b[i];interrupts();}}
