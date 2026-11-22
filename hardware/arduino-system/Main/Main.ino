/*
 * CS 362 - Project Submission Header
 * Team Number:
 * Project Name: Dual-Reality Maze
 * Team Members (Name - NetID):
 *   Soham Basanwar - sbasan3
 *   Ronit Mishra - rmish
 *   Prince Patel - ppate515
 *
 * Abstract (100 words):
 * Dual-Reality Maze is a cooperative fantasy game controlled by three Arduino
 * boards. The Explorer uses a joystick to navigate and a photoresistor to
 * reveal hidden paths. The Architect uses a potentiometer and pushbutton to
 * select and operate maze mechanisms, while a servo represents gate movement. A
 * Main Arduino coordinates both controllers through wired I2C and communicates
 * with the laptop game over Wi-Fi. An LCD displays status and time, an RGB LED
 * indicates connection readiness, and a buzzer provides feedback. Original work
 * combines the story, puzzles, game software, communication protocol, and
 * physical controller interactions into one shared experience requiring
 * coordinated teamwork.
 *
 * Sketch: Main
 * Target board: Arduino UNO R4 WiFi
 * Role: I2C controller; Wi-Fi access point and laptop bridge
 * Connections:
 * LCD=5V/GND/SDA/SCL; controller bus=A4/A5; RGB R=D9, G=D5, B=D3,
 * one resistor per color; buzzer=D6; optional LED driver=D10.
 * A4=SDA and A5=SCL on the same 5V bus; not the 3.3V Qwiic connector.
 * Keep Protocol.h beside this sketch. All three boards share signal ground.
 */

#include <Wire.h>
#include <hd44780.h>
#include <hd44780ioClass/hd44780_I2Cexp.h>
#include "Protocol.h"
#include "CountdownBuzzer.h"
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
uint8_t lcdAddress=0,faults=0;
uint32_t lastLCDProbe=0;
char oldTop[17]={},oldBottom[17]={};
uint32_t eSeen=0,aSeen=0,lastPoll=0,lastSend=0,lastLCD=0,lastCommand=0;
uint8_t mode=0,gateOpen=0;unsigned secondsLeft=0;
String serialLine;
bool apOK=true;
uint8_t gameTransport=0; // 0 waiting, 1 USB, 2 Wi-Fi
CountdownBuzzer countdown;
uint32_t buzzerWarnings=0;
uint16_t lastBuzzerSecond=0;
const uint8_t BUZZER_PIN=6;
const uint16_t WARNING_HZ=660, WARNING_MS=85;
enum LinkStatus { START_OR_FAULT, CONTROLLERS_CONNECTED, WIFI_GAME_READY };
LinkStatus linkStatus=START_OR_FAULT;
const uint8_t RGB_RED_PIN=9, RGB_GREEN_PIN=5, RGB_BLUE_PIN=3;
void updateStatus(){
 bool freshGame=lastCommand && millis()-lastCommand<1500;
 faults=(!online(eSeen)?1:0)|(!online(aSeen)?2:0)|(!lcdOK?4:0)|(!apOK && !(freshGame&&gameTransport==1)?16:0);
 if(faults)linkStatus=START_OR_FAULT;
 else linkStatus=freshGame?WIFI_GAME_READY:CONTROLLERS_CONNECTED;
 digitalWrite(RGB_RED_PIN,(linkStatus==START_OR_FAULT)^RGB_COMMON_ANODE);
 digitalWrite(RGB_GREEN_PIN,(linkStatus==CONTROLLERS_CONNECTED)^RGB_COMMON_ANODE);
 digitalWrite(RGB_BLUE_PIN,(linkStatus==WIFI_GAME_READY)^RGB_COMMON_ANODE);
}
bool online(uint32_t t){return t&&millis()-t<500;}
void pollBoard(uint8_t addr,uint8_t* out,uint32_t &seen){uint8_t b[PACKET_SIZE],n=0;
 Wire.requestFrom(addr,PACKET_SIZE);while(Wire.available()){uint8_t v=Wire.read();if(n<PACKET_SIZE)b[n++]=v;}
 if(n==PACKET_SIZE&&b[0]==1&&checksum(b,11)==b[11]){if(!seen||b[1]!=out[1])seen=millis();memcpy(out,b,PACKET_SIZE);}
}
void commandBoard(uint8_t addr){uint8_t b[4]={0xA5,gateOpen,uint8_t(mode | (linkStatus!=START_OR_FAULT?4:0) | (linkStatus==WIFI_GAME_READY?8:0)),0};b[3]=checksum(b,3);Wire.beginTransmission(addr);Wire.write(b,4);Wire.endTransmission();}
size_t inputJSON(char* buffer,size_t capacity){
 int n=snprintf(buffer,capacity,
  "{\"v\":1,\"ms\":%lu,\"fw\":\"2026-11-21-countdown-r2\",\"exchange\":true,\"faults\":%u,\"lcdOK\":%s,\"apOK\":%s,\"gateRequested\":%u,\"mode\":%u,\"eOK\":%s,\"aOK\":%s,\"x\":%u,\"y\":%u,\"light\":%u,\"ep\":%u,\"pot\":%u,\"ap\":%u,\"beeps\":%lu,\"beepSecond\":%u,\"led\":\"%s\"}\n",
  (unsigned long)millis(),faults,lcdOK?"true":"false",apOK?"true":"false",gateOpen,mode,
  online(eSeen)?"true":"false",online(aSeen)?"true":"false",
  wordAt(e,2),wordAt(e,4),wordAt(e,6),wordAt(e,8),wordAt(a,2),wordAt(a,8),
  (unsigned long)buzzerWarnings,lastBuzzerSecond,
  linkStatus==WIFI_GAME_READY?"blue":linkStatus==CONTROLLERS_CONNECTED?"green":"red");
 return n>0 && (size_t)n<capacity?(size_t)n:0;
}
bool feedback(const String &s,uint8_t transport){unsigned g,m,t;char extra;
 if(sscanf(s.c_str(),"S,%u,%u,%u%c",&g,&m,&t,&extra)!=3||g>1||m>2||t>36000)return false;
 gateOpen=g;mode=m;secondsLeft=t;lastCommand=millis();gameTransport=transport;
 const uint16_t warning=countdown.observe(t,m==1 && online(eSeen) && online(aSeen) && lcdOK);
 if(warning){tone(BUZZER_PIN,WARNING_HZ,WARNING_MS);buzzerWarnings++;lastBuzzerSecond=warning;}
 if(m!=1 || t==0)noTone(BUZZER_PIN);
 return true;
}
void setup(){Serial.begin(115200);Wire.begin();Wire.setClock(100000);
 #if defined(WIRE_HAS_TIMEOUT)
 Wire.setWireTimeout(25000,true);
 #endif
 // Main is the only board with an RGB LED: red D9, green D5, blue D3.
 pinMode(RGB_RED_PIN,OUTPUT);pinMode(RGB_GREEN_PIN,OUTPUT);pinMode(RGB_BLUE_PIN,OUTPUT);pinMode(10,OUTPUT);pinMode(2,INPUT_PULLUP);
 digitalWrite(RGB_RED_PIN,!RGB_COMMON_ANODE);digitalWrite(RGB_GREEN_PIN,RGB_COMMON_ANODE);digitalWrite(RGB_BLUE_PIN,RGB_COMMON_ANODE);
 lcdOK=lcd.begin(16,2)==0;if(lcdOK){lcd.backlight();lcd.print("Dual Reality");}
 if(lcdOK)lcdAddress=lcd.getProp(hd44780_I2Cexp::Prop_addr);
 tone(BUZZER_PIN,440,80);
 #if HUB_WIFI
 apOK=WiFi.status()!=WL_NO_MODULE && WiFi.beginAP(AP_NAME,AP_PASSWORD)==WL_AP_LISTENING;
 if(apOK){server.begin();Serial.print("# AP IP: ");Serial.println(WiFi.localIP());}
 #endif
}
void loop(){uint32_t now=millis();
 while(Serial.available()){char c=Serial.read();if(c=='\n'){feedback(serialLine,1);serialLine="";}else if(c!='\r'){if(serialLine.length()<80)serialLine+=c;else serialLine="";}}
 // Serial feedback may have advanced lastCommand beyond the loop's old timestamp.
 now=millis();
 if(lastCommand && now-lastCommand>=1500){lastCommand=0;mode=0;gateOpen=0;gameTransport=0;countdown.observe(secondsLeft,false);noTone(BUZZER_PIN);}
 if(now-lastPoll>=25){lastPoll=now;pollBoard(EXPLORER,e,eSeen);pollBoard(ARCHITECT,a,aSeen);updateStatus();commandBoard(EXPLORER);commandBoard(ARCHITECT);}
 if(now-lastSend>=50){lastSend=now;if(Serial){char body[512];size_t size=inputJSON(body,sizeof(body));if(size)Serial.write((const uint8_t*)body,size);}}

 unsigned phase=now%2400;analogWrite(10,(phase<1200?phase:2400-phase)*180UL/1200);
 if(lcdAddress && now-lastLCDProbe>=500){
  lastLCDProbe=now;Wire.beginTransmission(lcdAddress);bool present=Wire.endTransmission()==0;
  if(present&&!lcdOK){lcdOK=lcd.begin(16,2)==0;if(lcdOK){lcd.backlight();oldTop[0]=oldBottom[0]=0;}}
  else lcdOK=present;
 }
 if(lcdOK&&now-lastLCD>=250){
  lastLCD=now;char top[17],bottom[17];
  snprintf(top,sizeof(top),"E:%s A:%s        ",online(eSeen)?"OK":"--",online(aSeen)?"OK":"--");
  snprintf(bottom,sizeof(bottom),"%-5s %02u:%02u     ",mode==1?"PLAY":mode==2?"PAUSE":"READY",secondsLeft/60,secondsLeft%60);
  if(strcmp(top,oldTop)){lcd.setCursor(0,0);lcd.print(top);strcpy(oldTop,top);}
  if(strcmp(bottom,oldBottom)){lcd.setCursor(0,1);lcd.print(bottom);strcpy(oldBottom,bottom);}
 }
 #if HUB_WIFI
 if(!client){client=server.available();if(client){requestStart=now;requestLine="";}}
 if(client){bool ready=false;while(client.available()){char c=client.read();if(c=='\n'){ready=true;break;}if(c!='\r'&&requestLine.length()<160)requestLine+=c;}
  if(ready){
   bool input=requestLine.startsWith("GET /input "),ok=false;
   bool exchange=requestLine.startsWith("GET /exchange?cmd=");
   int prefix=exchange?18:15;
   if(exchange || requestLine.startsWith("GET /state?cmd=")){
    int end=requestLine.indexOf(' ',prefix);
    if(end>0)ok=feedback(requestLine.substring(prefix,end),2);
   }
   updateStatus();
   char body[512];
   if(input || (exchange&&ok))inputJSON(body,sizeof(body));
   else strcpy(body,ok?"{\"ok\":true}":"{\"ok\":false}");
   char response[768];
   int length=snprintf(response,sizeof(response),
    "HTTP/1.1 %s\r\nContent-Type: application/json\r\nCache-Control: no-store\r\nConnection: close\r\nContent-Length: %u\r\n\r\n%s",
    input||ok?"200 OK":"400 Bad Request",(unsigned)strlen(body),body);
   if(length>0 && (size_t)length<sizeof(response))client.write((const uint8_t*)response,length);
   client.stop();
  }else if(now-requestStart>300){client.stop();}
 }
 #endif
}
