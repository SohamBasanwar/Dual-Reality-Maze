"""Generate firmware; then run prepare-submission.py to restore submission headers."""
from pathlib import Path
R=Path(__file__).parent/'arduino-system'
def put(p,s):
 p=R/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8')
common=r'''#pragma once
#include <Arduino.h>
const uint8_t EXPLORER=0x10, ARCHITECT=0x11, PACKET_SIZE=12;
inline uint8_t checksum(const uint8_t* b,uint8_t n){uint8_t c=0;while(n--)c^=*b++;return c;}
inline uint16_t wordAt(const uint8_t* b,uint8_t i){return uint16_t(b[i])|(uint16_t(b[i+1])<<8);}
inline void putWord(uint8_t* b,uint8_t i,uint16_t v){b[i]=v;b[i+1]=v>>8;}
// Common-cathode RGB: each colour MUST have its own 330 ohm resistor.
const bool RGB_COMMON_ANODE=false;
inline void rgb(bool r,bool g,bool b){digitalWrite(3,r^RGB_COMMON_ANODE);digitalWrite(5,g^RGB_COMMON_ANODE);digitalWrite(6,b^RGB_COMMON_ANODE);}
inline void initRGB(){pinMode(3,OUTPUT);pinMode(5,OUTPUT);pinMode(6,OUTPUT);rgb(1,0,0);}
'''
for name,architect in [('Explorer',False),('Architect',True)]:
 put(f'{name}/{name}.ino',r'''#include <Wire.h>
#include "Protocol.h"
'''+('#include <Servo.h>\nServo gate;\nconst uint16_t CLOSED_US=1200, OPEN_US=1800; // Validated unloaded horn range.\nbool lastOpen=false;\nuint32_t gateMovedAt=0;\n' if architect else '')+r'''
volatile uint8_t reply[PACKET_SIZE], requestedGate=0, requestedMode=0;
volatile bool commandReady=false;
uint32_t lastCommand=0, lastSample=0, changedAt=0;
uint16_t presses=0;uint8_t sequence=0;
bool lastRaw=false, stable=false;
void requested(){uint8_t b[PACKET_SIZE];for(uint8_t i=0;i<PACKET_SIZE;i++)b[i]=reply[i];Wire.write(b,PACKET_SIZE);}
void received(int count){uint8_t b[4];uint8_t n=0;while(Wire.available()){uint8_t v=Wire.read();if(n<4)b[n++]=v;}
 if(count==4&&n==4&&b[0]==0xA5&&checksum(b,3)==b[3]){requestedGate=b[1];requestedMode=b[2];commandReady=true;}}
void setup(){pinMode(2,INPUT_PULLUP);
'''+(' // Pulse the servo only when the requested gate position changes.\n' if architect else '')+f' Wire.begin({"ARCHITECT" if architect else "EXPLORER"});'+r'''
 Wire.onRequest(requested);Wire.onReceive(received);
 #if defined(WIRE_HAS_TIMEOUT)
 Wire.setWireTimeout(25000,true);
 #endif
}
void loop(){uint32_t now=millis();
 bool raw=digitalRead(2)==LOW;if(raw!=lastRaw){lastRaw=raw;changedAt=now;}
 if(now-changedAt>=30&&raw!=stable){stable=raw;if(stable)presses++;}
 noInterrupts();bool fresh=commandReady;uint8_t g=requestedGate,m=requestedMode;commandReady=false;interrupts();
 if(fresh){lastCommand=now;}
 bool connected=lastCommand&&now-lastCommand<1500;
 bool healthy=connected && (m & 4);

'''+(' bool open=healthy && (m&3)==1 && g;\n if(open!=lastOpen){lastOpen=open;gate.writeMicroseconds(open?OPEN_US:CLOSED_US);if(!gate.attached())gate.attach(9);gateMovedAt=now;}\n if(gate.attached() && now-gateMovedAt>=700)gate.detach();\n' if architect else '')+r'''
 if(now-lastSample>=5){lastSample=now;uint8_t b[PACKET_SIZE]={1,sequence++};
 putWord(b,2,analogRead(A0));
'''+(' putWord(b,4,0);putWord(b,6,0);\n' if architect else ' putWord(b,4,analogRead(A1));putWord(b,6,analogRead(A2));\n')+r'''
 putWord(b,8,presses);b[10]=stable;b[11]=checksum(b,11);
 noInterrupts();for(uint8_t i=0;i<PACKET_SIZE;i++)reply[i]=b[i];interrupts();
 }
}
''');put(f'{name}/Protocol.h',common)
put('Main/Protocol.h',common)
put('Main/Main.ino',r'''#include <Wire.h>
#include <hd44780.h>
#include <hd44780ioClass/hd44780_I2Cexp.h>
#include "Protocol.h"
#if defined(ARDUINO_UNOR4_WIFI)
#include <WiFiS3.h>
#define HUB_WIFI 1
const char AP_NAME[]="DualRealityMaze";
const char AP_PASSWORD[]="MazeDemo362"; // Change locally if desired (8+ characters).
WiFiServer server(80);WiFiClient client;String requestLine;uint32_t requestStart;
#else
#define HUB_WIFI 0
#endif
hd44780_I2Cexp lcd;
bool lcdOK=false;uint8_t e[PACKET_SIZE]={},a[PACKET_SIZE]={};
uint32_t eSeen=0,aSeen=0,lastPoll=0,lastSend=0,lastLCD=0,lastCommand=0;
uint8_t mode=0,gateOpen=0;unsigned secondsLeft=0;
String serialLine;
bool apOK=true;
bool wifiGameSeen=false;
uint32_t lastWifiGame=0;
enum LinkStatus { START_OR_FAULT, CONTROLLERS_CONNECTED, WIFI_GAME_READY };
LinkStatus linkStatus=START_OR_FAULT;
void updateStatus(){
 bool freshGame=wifiGameSeen && millis()-lastWifiGame<2000;
 if(!online(eSeen)||!online(aSeen)||!lcdOK||!apOK||(wifiGameSeen&&!freshGame))linkStatus=START_OR_FAULT;
 else linkStatus=freshGame?WIFI_GAME_READY:CONTROLLERS_CONNECTED;
 digitalWrite(3,(linkStatus==START_OR_FAULT)^RGB_COMMON_ANODE);
 digitalWrite(5,(linkStatus==CONTROLLERS_CONNECTED)^RGB_COMMON_ANODE);
 digitalWrite(9,(linkStatus==WIFI_GAME_READY)^RGB_COMMON_ANODE);
}
bool online(uint32_t t){return t&&millis()-t<500;}
void pollBoard(uint8_t addr,uint8_t* out,uint32_t &seen){uint8_t b[PACKET_SIZE],n=0;
 Wire.requestFrom(addr,PACKET_SIZE);while(Wire.available()){uint8_t v=Wire.read();if(n<PACKET_SIZE)b[n++]=v;}
 if(n==PACKET_SIZE&&b[0]==1&&checksum(b,11)==b[11]){if(!seen||b[1]!=out[1])seen=millis();memcpy(out,b,PACKET_SIZE);}
}
void commandBoard(uint8_t addr){uint8_t b[4]={0xA5,gateOpen,uint8_t(mode | (linkStatus!=START_OR_FAULT?4:0) | (linkStatus==WIFI_GAME_READY?8:0)),0};b[3]=checksum(b,3);Wire.beginTransmission(addr);Wire.write(b,4);Wire.endTransmission();}
void inputJSON(Print &p){p.print("{\"v\":1,\"ms\":");p.print(millis());
 p.print(",\"eOK\":");p.print(online(eSeen)?"true":"false");p.print(",\"aOK\":");p.print(online(aSeen)?"true":"false");
 p.print(",\"x\":");p.print(wordAt(e,2));p.print(",\"y\":");p.print(wordAt(e,4));p.print(",\"light\":");p.print(wordAt(e,6));
 p.print(",\"ep\":");p.print(wordAt(e,8));p.print(",\"pot\":");p.print(wordAt(a,2));p.print(",\"ap\":");p.print(wordAt(a,8));p.print(",\"led\":\"");p.print(linkStatus==WIFI_GAME_READY?"blue":linkStatus==CONTROLLERS_CONNECTED?"green":"red");p.println("\"}");}
bool feedback(const String &s){unsigned g,m,t;char extra;
 if(sscanf(s.c_str(),"S,%u,%u,%u%c",&g,&m,&t,&extra)!=3||g>1||m>2||t>36000)return false;
 gateOpen=g;mode=m;secondsLeft=t;lastCommand=millis();return true;}
void setup(){Serial.begin(115200);Wire.begin();Wire.setClock(100000);
 #if defined(WIRE_HAS_TIMEOUT)
 Wire.setWireTimeout(25000,true);
 #endif
 // Main RGB differs from the R3 mapping: blue is D9, buzzer is D6.
 pinMode(3,OUTPUT);pinMode(5,OUTPUT);pinMode(9,OUTPUT);pinMode(10,OUTPUT);pinMode(2,INPUT_PULLUP);
 digitalWrite(3,!RGB_COMMON_ANODE);digitalWrite(5,RGB_COMMON_ANODE);digitalWrite(9,RGB_COMMON_ANODE);
 lcdOK=lcd.begin(16,2)==0;if(lcdOK){lcd.backlight();lcd.print("Dual Reality");}
 tone(6,440,100);
 #if HUB_WIFI
 apOK=WiFi.status()!=WL_NO_MODULE && WiFi.beginAP(AP_NAME,AP_PASSWORD)==WL_AP_LISTENING;
 if(apOK){server.begin();Serial.print("# AP IP: ");Serial.println(WiFi.localIP());}
 #endif
}
void loop(){uint32_t now=millis();
 while(Serial.available()){char c=Serial.read();if(c=='\n'){feedback(serialLine);serialLine="";}else if(c!='\r'){if(serialLine.length()<80)serialLine+=c;else serialLine="";}}
 if(!lastCommand||now-lastCommand>1500){mode=0;gateOpen=0;}
 if(now-lastPoll>=25){lastPoll=now;pollBoard(EXPLORER,e,eSeen);pollBoard(ARCHITECT,a,aSeen);updateStatus();commandBoard(EXPLORER);commandBoard(ARCHITECT);}
 if(now-lastSend>=50){lastSend=now;inputJSON(Serial);}

 unsigned phase=now%2400;analogWrite(10,(phase<1200?phase:2400-phase)*180UL/1200);
 if(lcdOK&&now-lastLCD>=500){lastLCD=now;char line[17];snprintf(line,sizeof(line),"E:%s A:%s        ",online(eSeen)?"OK":"--",online(aSeen)?"OK":"--");lcd.setCursor(0,0);lcd.print(line);snprintf(line,sizeof(line),"%s %02u:%02u   ",mode==1?"PLAY":mode==2?"PAUSE":"READY",secondsLeft/60,secondsLeft%60);lcd.setCursor(0,1);lcd.print("                ");lcd.setCursor(0,1);lcd.print(line);}
 #if HUB_WIFI
 if(!client){client=server.available();if(client){requestStart=now;requestLine="";}}
 if(client){bool ready=false;while(client.available()){char c=client.read();if(c=='\n'){ready=true;break;}if(c!='\r'&&requestLine.length()<160)requestLine+=c;}
  if(ready){bool input=requestLine.startsWith("GET /input ");bool ok=false;
   if(requestLine.startsWith("GET /state?cmd=")){int end=requestLine.indexOf(' ',15);if(end>0)ok=feedback(requestLine.substring(15,end));if(ok){wifiGameSeen=true;lastWifiGame=millis();}}
   client.println(input||ok?"HTTP/1.1 200 OK":"HTTP/1.1 400 Bad Request");client.println("Content-Type: application/json");client.println("Cache-Control: no-store");client.println("Connection: close");client.println();if(input)inputJSON(client);else client.println(ok?"{\"ok\":true}":"{\"ok\":false}");client.stop();
  }else if(now-requestStart>300){client.stop();}
 }
 #endif
}
''')
print(R)
