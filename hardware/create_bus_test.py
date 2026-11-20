from pathlib import Path
R=Path(__file__).parent/'bus-test'
for port,address in [('COM6',16),('COM8',17)]:
 name='Probe_'+port;d=R/name;d.mkdir(parents=True,exist_ok=True)
 code=r'''#include <Wire.h>
const byte ADDRESS=ADDR;
volatile byte sample[16]={}; volatile uint16_t nonce=0,receives=0;
uint16_t seq=0;unsigned long last=0;
byte crc(byte*b,int n){byte c=0;while(n--)c^=*b++;return c;}
void word(byte*b,int i,uint16_t n){b[i]=n;b[i+1]=n>>8;}
void request(){byte b[16];for(byte i=0;i<16;i++)b[i]=sample[i];word(b,8,nonce);word(b,10,receives);b[15]=crc(b,15);Wire.write(b,16);}
void receive(int n){byte b[4];int k=0;while(Wire.available()){byte c=Wire.read();if(k<4)b[k++]=c;}
 if(n==4&&k==4&&b[0]==0xC1&&crc(b,3)==b[3]){nonce=b[1]|uint16_t(b[2])<<8;receives++;}}
void setup(){Serial.begin(115200);pinMode(2,INPUT_PULLUP);Wire.begin(ADDRESS);Wire.onReceive(receive);Wire.onRequest(request);}
void loop(){if(millis()-last>=10){last=millis();byte b[16]={0xD1,ADDRESS};word(b,2,seq++);word(b,4,analogRead(A0));word(b,6,analogRead(A1));b[12]=digitalRead(2)==LOW;noInterrupts();for(byte i=0;i<16;i++)sample[i]=b[i];interrupts();}}
'''.replace('ADDR;',str(address)+';')
 (d/(name+'.ino')).write_text(code)
d=R/'MainProbe';d.mkdir(parents=True,exist_ok=True)
(d/'MainProbe.ino').write_text(r'''#include <Wire.h>
uint16_t nonce=0;uint32_t last=0;
byte crc(byte*b,int n){byte c=0;while(n--)c^=*b++;return c;}
uint16_t word(byte*b,int i){return b[i]|uint16_t(b[i+1])<<8;}
void test(byte addr){byte command[4]={0xC1,byte(nonce),byte(nonce>>8),0};command[3]=crc(command,3);
 Wire.beginTransmission(addr);Wire.write(command,4);byte tx=Wire.endTransmission();
 byte b[16]={},n=0;Wire.requestFrom(addr,(byte)16);while(Wire.available()){byte c=Wire.read();if(n<16)b[n++]=c;}
 bool valid=n==16&&b[0]==0xD1&&b[1]==addr&&b[15]==crc(b,15);
 Serial.print("{\"ms\":");Serial.print(millis());Serial.print(",\"addr\":");Serial.print(addr);Serial.print(",\"tx\":");Serial.print(tx);Serial.print(",\"bytes\":");Serial.print(n);Serial.print(",\"valid\":");Serial.print(valid?"true":"false");Serial.print(",\"echoOK\":");Serial.print(valid&&word(b,8)==nonce?"true":"false");Serial.print(",\"seq\":");Serial.print(word(b,2));Serial.print(",\"rx\":");Serial.print(word(b,10));Serial.print(",\"x\":");Serial.print(word(b,4));Serial.print(",\"y\":");Serial.print(word(b,6));Serial.print(",\"button\":");Serial.print(b[12]);Serial.println("}");}
void setup(){Serial.begin(115200);Wire.begin();Wire.setClock(100000);}
void loop(){if(millis()-last>=100){last=millis();nonce++;test(0x10);test(0x11);}}
''')
print(R)
