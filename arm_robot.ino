#include <Servo.h>
#define BLYNK_PRINT Serial
#define BLYNK_TEMPLATE_ID "TMPL6z44tKvC6"
#define BLYNK_TEMPLATE_NAME "test"
#define BLYNK_AUTH_TOKEN "QxcnyY8PEYBdiBGtZAvbanNTcgAQMpnh"
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>

char ssid[] = "LAPTOP-3K3PRGR2 5785";
char pass[] = "09J}252c";
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
int x=0;
int minUs = 500;
int maxUs = 2500;
int servo1Pin = 2;
int servo2Pin = 0;
int servo3Pin = 4;
int servo4Pin = 5;
int a=90,b=90,c=90,d=90;;

void setup()
{
  Serial.begin(9600);
  servo1.attach(servo1Pin, minUs, maxUs);
	servo2.attach(servo2Pin, minUs, maxUs);
	servo3.attach(servo3Pin, minUs, maxUs);
	servo4.attach(servo4Pin, minUs, maxUs);
  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);
}

BLYNK_WRITE(V0)
{
  int pos1 = param.asInt(); 
  lengan1(pos1);
}

BLYNK_WRITE(V1)
{
  int pos2 = param.asInt(); 
  turn(pos2);
}

BLYNK_WRITE(V2)
{
  int pos3 = param.asInt();
  lengan2(pos3);
}

BLYNK_WRITE(V3)
{
  int pos4 = param.asInt(); 
  jepit(pos4);
}

BLYNK_WRITE(V4)
{
  if(param.asInt()==1){
  x=1;
}else{x=0;}
}

void loop()
{
  Blynk.run();
  if(x==1){
    if(digitalRead(15)==0){
    oto();}
  }}


void oto(){
  delay(100);
  turn(50);
  jepit(100);
  lengan2(105);
  lengan1(130);
  jepit(10);
  lengan2(94);
  lengan1(50);
  turn(130);
  lengan2(105);
  lengan1(130);
  jepit(100);
  lengan2(94);
  lengan1(50);
  turn(90);
  jepit(10);
}

void lengan1(int a1){
  while(a>=a1){
    if(a<=100&&a<=(170-c)){
      c++;
      servo3.write(c);
    }
    a--;
    servo1.write(a);
    delay(10);
  }
  while(a<=a1){
    a++;
    servo1.write(a);
    delay(10);
  }
  Blynk.virtualWrite(V2, c);
}

void lengan2(int c1){
  while(c>=c1){
     if(c<=160&&c<=(170-a)){
      a++;
      servo1.write(a);
    }
    c--;
    servo3.write(c);
    delay(10);
  }
  while(c<=c1){
    
    c++;
    servo3.write(c);
    delay(10);
  }Blynk.virtualWrite(V0, a);
}

void turn(int b1){
    while(b!=b1){
    if(b>=b1){b--;}
    else{b++;}
    servo2.write(b);
    delay(10);
  }
}

void jepit(int d1){
    while(d!=d1){
    if(d>=d1){d--;}
    else{d++;}
    servo4.write(d);
    delay(10);
  }
}

