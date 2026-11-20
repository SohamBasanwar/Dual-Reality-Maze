#include <Wire.h>
#include <Servo.h>
Servo testServo;
bool servoTest=false;
uint32_t servoStart=0;
volatile byte servoCommand=0;
bool wideTest=false;
uint16_t commandedUs=0;
const byte ADDRESS=16;
volatile byte sample[16]={}; volatile uint16_t nonce=0,receives=0;
uint16_t seq=0;unsigned long last=0;
byte crc(byte*b,int n){byte c=0;while(n--)c^=*b++;return c;}
void word(byte*b,int i,uint16_t n){b[i]=n;b[i+1]=n>>8;}
void request(){byte b[16];for(byte i=0;i<16;i++)b[i]=sample[i];word(b,8,nonce);word(b,10,receives);b[15]=crc(b,15);Wire.write(b,16);}
void receive(int n){byte b[4];int k=0;while(Wire.available()){byte c=Wire.read();if(k<4)b[k++]=c;}
 if(n==4&&k==4&&crc(b,3)==b[3]){
  if(b[0]==0xC1){nonce=b[1]|uint16_t(b[2])<<8;receives++;}
  if(b[0]==0xC2&&b[2]==0&&(b[1]==1||b[1]==2))servoCommand=b[1];
 }}
void setup(){Serial.begin(115200);pinMode(2,INPUT_PULLUP);Wire.begin(ADDRESS);Wire.onReceive(receive);Wire.onRequest(request);}
void loop(){
 byte action;noInterrupts();action=servoCommand;servoCommand=0;interrupts();
 if(action==2){testServo.detach();servoTest=false;commandedUs=0;Serial.println("# SERVO_STOP");}
 if(action==1&&!servoTest){
  testServo.writeMicroseconds(1500);testServo.attach(9);servoStart=millis();servoTest=true;wideTest=true;
  Serial.println("# WIFI_I2C_SWEEP_BEGIN 1200..1800us");
 }
 while(Serial.available())if(Serial.read()=='V'){
  testServo.writeMicroseconds(1500);testServo.attach(9);servoStart=millis();servoTest=true;wideTest=false;
  Serial.println("# SERVO_TEST_BEGIN D9 center +/-100us");
 }
 if(servoTest){
  uint32_t elapsed=millis()-servoStart;
  if(wideTest){
   const int points[]={1500,1200,1800,1200,1800,1500};
   if(elapsed<10000){byte segment=elapsed/2000;commandedUs=points[segment]+(long(points[segment+1])-points[segment])*long(elapsed%2000)/2000;}
   else if(elapsed<11000)commandedUs=1500;
   else {testServo.detach();servoTest=false;commandedUs=0;Serial.println("# WIFI_I2C_SWEEP_END detached");}
  }else{
   if(elapsed<2000)commandedUs=1500;
   else if(elapsed<4000)commandedUs=1400;
   else if(elapsed<6000)commandedUs=1600;
   else if(elapsed<8000)commandedUs=1500;
   else {testServo.detach();servoTest=false;commandedUs=0;Serial.println("# SERVO_TEST_END detached");}
  }
  if(servoTest)testServo.writeMicroseconds(commandedUs);
 }
 if(millis()-last>=10){last=millis();byte b[16]={0xD1,ADDRESS};word(b,2,seq++);word(b,4,analogRead(A0));word(b,6,analogRead(A1));b[12]=digitalRead(2)==LOW;word(b,13,commandedUs);noInterrupts();for(byte i=0;i<16;i++)sample[i]=b[i];interrupts();}}
