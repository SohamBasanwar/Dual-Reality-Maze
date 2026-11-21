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
 * Sketch: Explorer
 * Target board: Arduino UNO R3
 * Role: I2C peripheral at 0x10
 * Connections:
 * Joystick X=A0, Y=A1, click=D2 to GND (INPUT_PULLUP);
 * Photoresistor divider=A2; SDA=A4; SCL=A5; common GND.
 * Keep Protocol.h beside this sketch. All three boards share signal ground.
 */

#include <Wire.h>
#include "Protocol.h"

volatile uint8_t reply[PACKET_SIZE], requestedGate=0, requestedMode=0;
volatile bool commandReady=false;
uint32_t lastCommand=0, lastSample=0, changedAt=0;
uint16_t presses=0;uint8_t sequence=0;
bool lastRaw=false, stable=false;
void requested(){uint8_t b[PACKET_SIZE];for(uint8_t i=0;i<PACKET_SIZE;i++)b[i]=reply[i];Wire.write(b,PACKET_SIZE);}
void received(int count){uint8_t b[4];uint8_t n=0;while(Wire.available()){uint8_t v=Wire.read();if(n<4)b[n++]=v;}
 if(count==4&&n==4&&b[0]==0xA5&&checksum(b,3)==b[3]){requestedGate=b[1];requestedMode=b[2];commandReady=true;}}
void setup(){pinMode(2,INPUT_PULLUP);
 Wire.begin(EXPLORER);
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


 if(now-lastSample>=5){lastSample=now;uint8_t b[PACKET_SIZE]={1,sequence++};
 putWord(b,2,analogRead(A0));
 putWord(b,4,analogRead(A1));putWord(b,6,analogRead(A2));

 putWord(b,8,presses);b[10]=stable;b[11]=checksum(b,11);
 noInterrupts();for(uint8_t i=0;i<PACKET_SIZE;i++)reply[i]=b[i];interrupts();
 }
}
