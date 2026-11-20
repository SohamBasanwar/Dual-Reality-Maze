#include <Wire.h>
#include <WiFiS3.h>
#include <hd44780.h>
#include <hd44780ioClass/hd44780_I2Cexp.h>
// Diagnostics only. RGB/buzzer run only on explicit serial T command; no servo command.
hd44780_I2Cexp lcd;
WiFiServer server(80);
WiFiClient client;
uint16_t nonce=0;
uint32_t last=0,lastStatus=0,clientStart=0;
uint32_t outputStart=0,busHz=100000;
int outputStage=-1;
bool outputTest=false;
int lcdStatus=-999,lcdReadback=-999,apStart=-999;
String scanList,requestLine,latest[2];
byte crc(byte*b,int n){byte c=0;while(n--)c^=*b++;return c;}
uint16_t word(byte*b,int i){return b[i]|uint16_t(b[i+1])<<8;}
void test(byte addr){
 byte command[4]={0xC1,byte(nonce),byte(nonce>>8),0};command[3]=crc(command,3);
 Wire.beginTransmission(addr);Wire.write(command,4);byte tx=Wire.endTransmission();
 byte b[16]={},n=0;Wire.requestFrom(addr,(byte)16);while(Wire.available()){byte c=Wire.read();if(n<16)b[n++]=c;}
 bool valid=n==16&&b[0]==0xD1&&b[1]==addr&&b[15]==crc(b,15);
 bool echo=valid&&word(b,8)==nonce;
 String s="{\"ms\":"+String(millis())+",\"addr\":"+String(addr)+",\"tx\":"+String(tx)+",\"bytes\":"+String(n);
 s+=",\"valid\":";s+=valid?"true":"false";s+=",\"echoOK\":";s+=echo?"true":"false";
 s+=",\"seq\":"+String(word(b,2))+",\"rx\":"+String(word(b,10))+",\"x\":"+String(word(b,4))+",\"y\":"+String(word(b,6));
 s+=",\"button\":"+String(b[12])+",\"presses\":"+String(addr==17?word(b,13):0)+",\"servoUs\":"+String(addr==16?word(b,13):0)+"}";
 latest[addr-16]=s;Serial.println(s);
}
String statusJSON(){
 return String("{\"type\":\"status\",\"scan\":[")+scanList+"],\"busHz\":"+String(busHz)+",\"lcdInit\":"+String(lcdStatus)+",\"lcdReadbackErrors\":"+String(lcdReadback)+",\"apStart\":"+String(apStart)+",\"wifiStatus\":"+String(WiFi.status())+",\"ip\":\""+WiFi.localIP().toString()+"\"}";
}
void setup(){
 Serial.begin(115200);Wire.begin();Wire.setClock(100000);
 for(byte a=1;a<127;a++){Wire.beginTransmission(a);if(Wire.endTransmission()==0){if(scanList.length())scanList+=",";scanList+=String(a);}}
 lcdStatus=lcd.begin(16,2);
 if(lcdStatus==0){
  lcd.backlight();lcd.clear();lcd.print("DUAL REALITY");lcd.setCursor(0,1);lcd.print("LCD TEST 1234");
  const char* lines[]={"DUAL REALITY","LCD TEST 1234"};lcdReadback=0;
  for(byte row=0;row<2;row++){lcd.setCursor(0,row);for(byte i=0;lines[row][i];i++){int r=lcd.read();if(r<0){lcdReadback=r;break;}if(r!=lines[row][i])lcdReadback++;}if(lcdReadback<0)break;}
 }
 if(WiFi.status()!=WL_NO_MODULE){apStart=WiFi.beginAP("DualRealityMaze","MazeDemo362");if(apStart==WL_AP_LISTENING)server.begin();}
 Serial.println(statusJSON());
}
void loop(){
 while(Serial.available()){
  char c=Serial.read();
  if(c=='5'||c=='1'){busHz=c=='5'?50000:100000;Wire.setClock(busHz);Serial.println(statusJSON());}
  // T requires confirmed common-cathode RGB wiring and passive piezo.
  if(c=='T'){outputStart=millis();outputStage=-1;outputTest=true;pinMode(3,OUTPUT);pinMode(5,OUTPUT);pinMode(9,OUTPUT);}
 }
 if(outputTest){
  int stage=(millis()-outputStart)/2000;
  if(stage!=outputStage){
   outputStage=stage;digitalWrite(3,stage==0);digitalWrite(5,stage==1);digitalWrite(9,stage==2);
   if(stage==3)tone(6,660,200);
   if(stage>=4){noTone(6);outputTest=false;}
   Serial.print("# OUTPUT_TEST_STAGE ");Serial.println(stage);
  }
 }
 if(millis()-last>=100){last=millis();nonce++;test(0x10);test(0x11);}
 if(millis()-lastStatus>=5000){lastStatus=millis();Serial.println(statusJSON());}
 if(!client){client=server.available();if(client){clientStart=millis();requestLine="";}}
 if(client){
  byte budget=128;bool ready=false;
  while(budget--&&client.available()){char c=client.read();if(c=='\n'){ready=true;break;}if(c!='\r'&&requestLine.length()<160)requestLine+=c;}
  if(ready){
   String body;
   if(requestLine=="GET /servo?cmd=sweep HTTP/1.1"||requestLine=="GET /servo?cmd=stop HTTP/1.1"){
    byte c[4]={0xC2,byte(requestLine.indexOf("sweep")>=0?1:2),0,0};c[3]=crc(c,3);
    Wire.beginTransmission(0x10);Wire.write(c,4);byte tx=Wire.endTransmission();
    body=String("{\"commandSent\":")+(tx==0?"true":"false")+",\"tx\":"+String(tx)+"}";
   }else body="{\"diagnostic\":true,\"status\":"+statusJSON()+",\"boards\":["+latest[0]+","+latest[1]+"]}";
   client.print("HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nCache-Control: no-store\r\nConnection: close\r\nContent-Length: ");client.print(body.length());client.print("\r\n\r\n");client.print(body);client.stop();
  }else if(millis()-clientStart>500)client.stop();
 }
}
