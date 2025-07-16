#include <BluetoothSerial.h>
BluetoothSerial SerialBT;
#include <EEPROM.h>
#include <WiFi.h>
#include <WiFiClient.h>
#include <WiFiAP.h>
#include <ESP32MX1508.h>
#include <ESP32Servo.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <HCSR04.h>
#include <IRremoteESP8266.h>
#include <IRrecv.h>
#include <IRutils.h>
LiquidCrystal_I2C lcd(0x27,16,2);
HCSR04 hc(14, new int[3]{12,13,5}, 3);
IRrecv irrecv(18);
decode_results results;
Servo myservo;
MX1508 motorA(25,17,4,5);
MX1508 motorB(16,27,2,3);

const char *ssid = "ESPduino Robot";
const char *password = "byRidho22";
WiFiServer server(80);
char data,kode;
const int linesensorR = 2;
const int linesensorL = 4;
byte jumlah=1,jumlah2=1;    
byte pilihan=0;
byte pilihanA=0;
byte pilihanB=0;
byte pilihanC=0;
short poin=0;
int cm,lihatkanan1,lihatkiri1;
byte block[8] = {0x0,0xe,0x1b,0xf,0x7,0xf,0x1e,0xa};
byte human[8]= {0xe,0xc,0x1e,0x1e,0x1e,0xe,0xa,0x1b};
byte zonk[8] = {0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0};
short  x=17,kebenaran;
short p,d=1,e,b=0,c=0;
const byte keyboard[4][3]PROGMEM={
  {1  ,2  ,3},
  {4  ,5  ,6},
  {7  ,8  ,9},
  {10 ,0  ,11}};
float angka;
unsigned long waktusebelum=0;
unsigned long waktusekarang;
float ya1,ya2,hasil;
float buttonPushCounter = 0;   
int buttonState = 0;         
int lastButtonState = 0;  
float buttonPushCounter1 = 0;   
int buttonState1 = 0;         
int lastButtonState1 = 0;  
int v,vcal;
int va,vb;

void setup() {
  // initialize serial communication:
  EEPROM.begin(64);
  Serial.begin(115200);
  irrecv.enableIRIn(); 
  results.value=0;
  myservo.attach(26);
  lcd.init();
  lcd.backlight();
  WiFi.softAP(ssid, password);
  IPAddress myIP = WiFi.softAPIP();
  lcd.createChar(0, block);
  lcd.createChar(1, human);
  lcd.createChar(3, zonk);
  lcd.setCursor(0,0);
  lcd.print(F("Made BY Ridho"));
  delay(2000);
  awal();}

void awal(){
 lcd.clear();
 myservo.write(80);
 jumlah=1;    
 pilihan=0;
 pilihanA=0;
 pilihanB=0;
 poin=0;
 v=EEPROM.read(3);
 vcal=EEPROM.read(4);
 vb=map(v, 1, 10, 100, 255);
 va=vb-vcal;
 buttonPushCounter = 0;   
 buttonPushCounter1 = 0;   
  if(EEPROM.read(1)==1){lcd.backlight();
  }else if(EEPROM.read(1)==0){lcd.noBacklight();}
  if(EEPROM.read(2)==1){SerialBT.begin("ESPduino32 Robot");
  }else if(EEPROM.read(2)==0){SerialBT.end();}
  menu();
  if(pilihan==1){avrobot();}
  if(pilihan==2){
    lcd.setCursor(0,0);
    lcd.print(F("IR Remote Mode"));
    irrobot();}
  if(pilihan==3){
    lcd.setCursor(0,0);
    lcd.print(F("Bluetooth Mode"));
    SerialBT.begin("ESPduino32 Robot");
    lcd.setCursor(0,1);
    blrobot();}
  if(pilihan==4){
    lcd.setCursor(0,0);
    lcd.print(F("WIFI Mode"));
    server.begin();
    loop();}
  if(pilihan==5){
    lcd.setCursor(0,0);
    lcd.print(F("Line Follower"));
    lfrobot();}
  if(pilihan==6){
    lcd.setCursor(0,0);
    lcd.print(F("Object Follower"));
    ofrobot();}
  if(pilihan==7){game();}
  if(pilihan==8){penggaris();}
  if(pilihan==9){more();}
  if(pilihan==10 ){set();}
 
}

void loop() { 
  buttonState = digitalRead(19);
  if (buttonState != lastButtonState) {
    if (buttonState == HIGH) {
      buttonPushCounter++;
    } else { 
    }  
  }
  lastButtonState = buttonState;
   buttonState1 = digitalRead(23);
  if (buttonState1 != lastButtonState1) {
    if (buttonState1 == HIGH) {
      buttonPushCounter1++;
    } else {
    }
    
  }
  lastButtonState1 = buttonState1;
  angka=(buttonPushCounter+buttonPushCounter1)/200;
  WiFiClient client = server.available();   // listen for incoming clients
  lcd.setCursor(0,1);
  lcd.print(angka);
  lcd.print("m");
  if (client) {                             // if you get a client,
    String currentLine = "",perintah="";                // make a String to hold incoming data from the client
    while (client.connected()) {            // loop while the client's connected
      if (client.available()) {             // if there's bytes to read from the client,
        char c = client.read();             // read a byte, then
         perintah=perintah+c;                   // print it out the serial monitor
        if (c == '\n') {                    // if the byte is a newline character

          // if the current line is blank, you got two newline characters in a row.
          // that's the end of the client HTTP request, so send a response:
          if (currentLine.length() == 0) {
            // HTTP headers always start with a response code (e.g. HTTP/1.1 200 OK)
            // and a content-type so the client knows what's coming, then a blank line:
            client.println("HTTP/1.1 200 OK");
            client.println("Content-type:text/html");
            client.println();

            // the content of the HTTP response follows the header:
            client.print("Click <a href=\"/H\">here</a> to turn ON the LED.<br>");
            client.print("Click <a href=\"/L\">here</a> to turn OFF the LED.<br>");

            // The HTTP response ends with another blank line:
            client.println();
            // break out of the while loop:
            break;
          } else {    // if you got a newline, then clear currentLine:
            currentLine = "";
          }
        } else if (c != '\r') {  // if you got anything else but a carriage return character,
          currentLine += c;      // add it to the end of the currentLine
        }
      }
    }
    // close the connection:
    client.stop();
    kode=perintah.charAt(15);
    switch (kode){
  case 'F' :
  maju();
  break;
  case 'B' :
  mundur();
  break;
  case 'R' :
  belokkanan();
  break;
  case 'L' :
  belokkiri();
  break;
  case 'S' :
  berhenti();
  break;
  case 'G' :
  motorA.motorGo(225);
  motorB.motorGo(180);
  break;
  case 'I' :
  motorA.motorGo(170);
  motorB.motorGo(225);
  break;
  case 'H' :
  motorA.motorRev(225);
  motorB.motorRev(180);
  break;
  case 'J' :
  motorA.motorRev(170);
  motorB.motorRev(225);
  break;
  case 'W' :
  berhenti();
  WiFi.mode(WIFI_OFF);
  awal();
  break;
 }
  }
}
 
void play(){
  cm=hc.dist(0);
  if(cm==0){cm=300;}
  irrecv.decode(&results);
  irrecv.resume();
  if(results.value==16738455){berhenti();
      awal();}
  avfall();
if(cm>=30){
  maju();}
  else{
    berhenti();
    delay(300);
    mundur();
    delay(800);
    berhenti();
    delay(500);
    if(pilihanA==2){
      lihatkanan();
      delay(500);
      lihatkiri();
      delay(500);
      if(lihatkanan1>=lihatkiri1){
        belokkanan();
        delay(400);
        berhenti();
        delay(300);
      }else{belokkiri();
        delay(400);
        berhenti();
        delay(300);}
    }else{
    belokkanan();
    delay(400);
    berhenti();
    delay(500);}}
    play();
    }

void play1(){
  irrecv.decode(&results);
  irrecv.resume();
  if(results.value==16738455){berhenti();
      awal();}
  avfall();
  maju();
  int d0=hc.dist(0);
  if(d0==0){d0=300;}
  delay(70);
  int d1=hc.dist(1);
  if(d1==0){d1=300;}
  delay(70);
  int d2=hc.dist(2);
  if(d2==0){d2=300;}
  delay(60);
  if(d1<=30||d2<=30){
  if(d1>=d2){
    belokkanan();
    delay(400);
    berhenti();}
    else if(d1<d2){belokkiri();
    delay(400);
    berhenti();}}
  if(d0<=20){
    belokkanan();
    delay(400);
    berhenti();
  }play1();
  }
    
void lihatkanan(){
  myservo.write(10);
  delay(500);
  lihatkanan1=hc.dist(0);
  myservo.write(80);
}

void lihatkiri(){
  myservo.write(150);
  delay(500);
  lihatkiri1=hc.dist(0);
  myservo.write(80);
}

void maju(){
  motorA.motorGo(va);
  motorB.motorGo(vb);
  }

void berhenti(){
  motorA.motorStop();
  motorB.motorStop();
   }
  
void belokkanan(){
  motorA.motorRev(va);
  motorB.motorGo(vb);
   }

 void belokkiri(){
  motorA.motorGo(va);
  motorB.motorRev(vb);
  }

  void mundur(){
  motorA.motorRev(va);
  motorB.motorRev(vb);
   }

  void irrobot(){
      results.value=0;
      irrecv.decode(&results);
      irrecv.resume();
      if(results.value==16718055){maju();}
      if(results.value==16730805){mundur();}
      if(results.value==16734885){belokkanan();}
      if(results.value==16716015){belokkiri();}
      if(results.value==0){berhenti();}
      if(results.value==16738455){berhenti();
      awal();}
      delay(150);
      irrobot();
  }

void blrobot(){
  kecepatan();
  lcd.setCursor(0,1);
  lcd.print(angka);
  lcd.print("m");
  if(SerialBT.available()>0){
 data=SerialBT.read();}
 switch (data){
  case 'F' :
  maju();
  break;
  case 'B' :
  mundur();
  break;
  case 'R' :
  belokkanan();
  break;
  case 'L' :
  belokkiri();
  break;
  case 'S' :
  berhenti();
  break;
  case 'G' :
  motorA.motorGo(225);
  motorB.motorGo(180);
  break;
  case 'I' :
  motorA.motorGo(170);
  motorB.motorGo(225);
  break;
  case 'H' :
  motorA.motorRev(225);
  motorB.motorRev(180);
  break;
  case 'J' :
  motorA.motorRev(170);
  motorB.motorRev(225);
  break;
  case 'X' :
  SerialBT.end();
  cm=0;
  awal();
  break;
 }blrobot();
}

void ofrobot(){
  avfall();
  results.value=0;
  irrecv.decode(&results);
  irrecv.resume();
   if(results.value==16738455){
       berhenti();
        awal();}
    int s=hc.dist(0);
    while(s<=40){
    s=hc.dist(0);
    if(s>=20){maju();}
    if(s<=15){mundur();}
    }
    delay(60);
     while(hc.dist(1)<=20){
     motorB.motorGo(200);
      }
      delay(60);
    while(hc.dist(2)<=20){
     motorA.motorGo(190);
      }
      delay(60);
      berhenti();
  ofrobot();
  }

void lfrobot(){
  state();
  if(digitalRead(linesensorL)==0&&digitalRead(linesensorR)==1){
    belokkiri(); }
   else if(digitalRead(linesensorR)==0&&digitalRead(linesensorL)==1){
    belokkanan(); }
   else if(digitalRead(linesensorR)==1&&digitalRead(linesensorL)==1){
    motorA.motorGo(190);
    motorB.motorGo(190);
   }
   else if(digitalRead(linesensorR)==0&&digitalRead(linesensorL)==0){
    berhenti();}
  lfrobot();
}

 void menu(){
  results.value=0;
  while(results.value!=16726215)
  {
    lcd.setCursor(0,0);
    lcd.print(F("#MODE#"));
    state();
    key();
    lcd.setCursor(0,1);
    if(jumlah%10==1){lcd.print(F(">AV Robot  "));// 1=jumlah mod 10
      pilihan=1;}
    else if(jumlah%10==2){ lcd.print(F(">IR Robot  "));// 2=jumlah mod 10
      pilihan=2;}
    else if(jumlah%10==3){ lcd.print(F(">BL Robot  "));
      pilihan=3;}
    else if(jumlah%10==4){ lcd.print(F(">WIFI Robot"));
      pilihan=4;}
    else if(jumlah%10==5){ lcd.print(F(">LF Robot  "));
      pilihan=5;}
    else if(jumlah%10==6){ lcd.print(F(">OF Robot  "));
      pilihan=6;}
    else if(jumlah%10==7){ lcd.print(F(">Game      "));
      pilihan=7;}
    else if(jumlah%10==8){ lcd.print(F(">Ruler     "));
      pilihan=8;}
    else if(jumlah%10==9){ lcd.print(F(">Test      "));
      pilihan=9;}
    else if(jumlah%10==0){ lcd.print(F(">Setting   "));
      pilihan=10;}
  }
  lcd.print(F(" <OK>"));
  results.value=0;
  delay(1000);
  lcd.clear();
}

void avrobot(){
  results.value=0;
  while(results.value!=16726215)
  {
    lcd.setCursor(0,0);
    lcd.print(F("<Avoiding>"));
    state();
    lcd.setCursor(0,1);
    if(jumlah%3==1){ 
      lcd.print(F("V 0.1"));
      pilihanA=1;}
    else if(jumlah%3==2){  
      lcd.print(F("V 0.2"));
      pilihanA=2;}
     else if(jumlah%3==0){ 
      lcd.print(F("V 0.3"));
      pilihanA=3;}
  }
  lcd.print(F("  <OK>"));
  delay(1000);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(F("Avoiding Robot"));
  results.value=0;
  if(pilihanA==3){play1();}
  play();

}

void game()
{ results.value=0;
  d=1;
  while(results.value!=16726215)
  { state();
    if(jumlah2==1||jumlah2==2){
    lcd.setCursor(0,0);
    if(jumlah2==1){lcd.print(F("<Math Game 1>"));}else{lcd.print(F("<Math Game 2>"));}
    lcd.setCursor(0,1);
    if(jumlah%4==1){ 
      lcd.print(F("Add       "));
      pilihanB=1;}
    else if(jumlah%4==2){  
      lcd.print(F("Sub       "));
      pilihanB=2;}
    else if(jumlah%4==3){ 
      lcd.print(F("Multp     "));
      pilihanB=3;}
    else if(jumlah%4==0){  
      lcd.print(F("Div       "));
      pilihanB=4;}
  }else if (jumlah2==3){
    lcd.setCursor(0,0);
    lcd.print(F("<RUN Game>   "));
    lcd.setCursor(0,1);
    lcd.print("     ");}
    if(jumlah2>3){jumlah2=1;}
    if(jumlah2<1){jumlah2=3;}
  }
  lcd.print(F(" <OK>"));
  delay(1000);
  poin=0;
  lcd.clear();
  if(jumlah2==3){rungame();}
  p=jumlah;
  e=jumlah2;
  paket();
}

void paket(){
  angka=0;
  lcd.setCursor(0,0);
  lcd.print(F("Pack Number:"));
  results.value=0;
  while(results.value!=16726215){
  if(irrecv.decode(&results)){
    irrecv.resume();
    if(results.value==16738455){
       berhenti();
       awal();}
    if(results.value==16726215){lanjut();}
    key();
    if(angka<1000){if(results.value!=4294967295){angka=(10*angka)+jumlah;}}}
    lcd.setCursor(0,1);
    lcd.print(angka,0);
  }}

  void lanjut(){
  if(angka>250||angka<1){lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(F("ERROR"));
  delay(2000);
  paket();}
  if(e==1){angka=angka+1000;}
  lcd.print(F("  <OK>"));
  if(p==1){randomSeed(angka);}
  else if(p==2){randomSeed(angka+250);}
  else if(p==3){randomSeed(angka+500);}
  else if(p==4){randomSeed(angka+750);}
  delay(2000);
  lcd.clear();
  soal();
}

void soal()
{ if(poin==10)
  { lcd.setCursor(0,0);
    lcd.print(F("You Win!"));
    delay(5000);
    lcd.clear();
    awal();
  }else if(poin==-5){
    lcd.setCursor(0,0);
    lcd.print(F("You Lose!"));
    delay(5000);
    lcd.clear();
    awal();
  }
  lcd.setCursor(0,0);
  lcd.print(F("READY..."));
  delay(1000);
  state();
  ya1=random(-10,50);//pemilihan x1
  ya2=random(-10,50);//pemilihan  x2
  if(jumlah2==1){
  kebenaran=random(0,2);//pemilihan hasil(benar/salah)
  if(kebenaran==0)//jika hasil=salah maka program berikut dijalankan
  { if(pilihanB==1)//untuk penjumlahan
    { hasil=ya1+ya2+10;}
    else if(pilihanB==2)//untuk pengurangan
    { hasil=ya1-ya2+10;}
    else if(pilihanB==3)//untuk perkalian
    { hasil=ya1*ya2+10;}
    else if(pilihanB==4)//untuk pembagian
    { hasil=ya1/ya2+0.1;}
  }
  else// jika hasil=benar maka program ini dijalankan
  { if(pilihanB==1)
    { hasil=ya1+ya2;}
    else if(pilihanB==2)
    { hasil=ya1-ya2;}
    else if(pilihanB==3)
    { hasil=ya1*ya2;}
    else if(pilihanB==4)
    { hasil=ya1/ya2;}
  }}else{if(pilihanB==1)
    { hasil=ya1+ya2;}
    else if(pilihanB==2)
    { hasil=ya1-ya2;}
    else if(pilihanB==3)
    { hasil=ya1*ya2;}
    else if(pilihanB==4)
    { hasil=ya1/ya2;}}
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(ya1,0);
  if(pilihanB==1)
  { lcd.print("+");}
  else if(pilihanB==2)
  { lcd.print("-");}
  else if(pilihanB==3)
  { lcd.print("x");}
  else if(pilihanB==4)
  { lcd.print("/");}
  lcd.print(ya2,0);
  lcd.print("=");
  results.value=0;
  if(jumlah2==1){
  if(pilihanB==4){//khusus untuk pembagian akan ditampilkan bilangan desimal
    lcd.print(hasil,2);}
  else{ lcd.print(hasil,0);}}else{lcd.print(" ?");}
  int s=5;
  if(jumlah2==1){
    waktusebelum=0;
  while(s!=-1)
  {  waktusekarang=millis();
    if(waktusekarang-waktusebelum>1500){
      lcd.setCursor(12,1);
      lcd.print(s);
      s--;
      waktusebelum=millis();
      if(s==-1){kosong();}}
    irrecv.decode(&results);
    irrecv.resume();
    if(results.value==16738455){
       berhenti();
        awal();}
    if(results.value==16734885)
    { if(kebenaran==1)
      { jwbbenar();}
      else
      { jwbsalah();}
      delay(2000);
      lcd.clear();
      soal();
    }
    else if(results.value==16716015)
    { if(kebenaran==1)
      { jwbsalah();}
      else
      { jwbbenar();}
      delay(2000);
      lcd.clear();
      soal();
    }
    }}
    
  if (jumlah2==2){
    jumlah=0;
    angka=0;
    p=5;
    while(results.value!=16726215){
    results.value=0;
    waktusekarang=millis();
    if(waktusekarang-waktusebelum>1500){
      lcd.setCursor(12,1);
      lcd.print(p);
      p--;
      waktusebelum=millis();
      if(p==-1){kosong();}
    }
    if(irrecv.decode(&results)){
    irrecv.resume();
    if(results.value==16738455){
       berhenti();
        awal();}
    key();
    if(results.value==16756815){jumlah=0;}
    if(results.value==16726215){
      if(hasil==angka){jwbbenar();}else{jwbsalah();}
      delay(2000);
      lcd.clear();
      soal();}
    if(results.value!=4294967295){angka=(10*angka)+jumlah;}}
    lcd.setCursor(0,1);
    lcd.print(angka,0);}
  }}
  /*jika pemain tidak memasukkan jawaban (kosong)*/
  void kosong(){
    lcd.setCursor(0,1);
    lcd.print(F("Answer: "));
    if(jumlah2==1){
    if(kebenaran==1)
    { lcd.print(F("True "));}
    else
    { lcd.print(F("False"));}}
    else{lcd.print(hasil,0);}
    delay(2000);
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print(F("Your Answer: - "));
    lcd.setCursor(0,1);
    lcd.print(F("+0   point: "));
    lcd.print(poin);
    delay(2000);
    lcd.clear();
    soal();
}

void jwbbenar()//jika jawaban yang dimasukkan benar
{ lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(F("You're Right"));
  lcd.setCursor(0,1);
  lcd.print(F("+1   point: "));
  poin++;
  lcd.print(poin);
  
} 

void jwbsalah()//jika jawaban yang dimasukkan salah
{ lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(F("You're Wrong"));
  lcd.setCursor(0,1);
  lcd.print(F("-1   point: "));
  poin--;
  lcd.print(poin);  
} 

void rungame(){
  p=random(2,5);
  if(p==2){
    for(x=17;x>=-2;x--){
      lcd.setCursor(x,1);
      lcd.write(byte(0));
      lcd.setCursor(x+1,1);
      lcd.write(byte(0));
      lcd.setCursor(x+2,1);
      lcd.write(byte(3));
      manusia();
      delay(150-(0.05*poin));
    }
  }else if(p==3){
    for(x=17;x>=-3;x--){
      lcd.setCursor(x,1);
      lcd.write(byte(0));
      lcd.setCursor(x+1,1);
      lcd.write(byte(0));
      lcd.setCursor(x+2,1);
      lcd.write(byte(0));
      lcd.setCursor(x+3,1);
      lcd.write(byte(3));
      manusia();
      delay(150-(0.05*poin));
     
    }
  }else if(p==4){
    for(x=17;x>=-4;x--){
      lcd.setCursor(x,1);
      lcd.write(byte(0));  
      lcd.setCursor(x+1,1);
      lcd.write(byte(0));
      lcd.setCursor(x+2,1);
      lcd.write(byte(0));
      lcd.setCursor(x+3,1);
      lcd.write(byte(0));
      lcd.setCursor(x+4,1);
      lcd.write(byte(3));
      manusia();
      if(poin<2000){
      delay(150-(0.05*poin));}
      else{delay(50);}
    }}rungame();
  }

void manusia(){
  poin++;
  lcd.setCursor(12,0);
  lcd.print(poin);
  state();
  if(results.value==16718055){
  if(x==4||x==3||x==2||x==1){
   lcd.setCursor(3,1);
   lcd.write(byte(0));}else{
   lcd.setCursor(3,1);
   lcd.write(byte(3));}
   lcd.setCursor(3,0);
   lcd.write(byte(1));
   if(d!=0){e=x-4;}
   if(e<-4){e=16;}
   d=0;
  }
  if(e==x){ 
    d=1;
    lcd.setCursor(3,0);
    lcd.write(byte(3));}
  lcd.setCursor(3,d);
  lcd.write(byte(1));
  if(d==1&&x==3){lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(F("GAME OVER  "));
  lcd.setCursor(0,1);
  lcd.print(F("Score :"));
  lcd.print(poin);
  delay(5000);
    awal();
 }}

void set(){
  results.value=0;
  lcd.setCursor(0,0);
  lcd.print(F("<Setting>"));
  while(results.value!=16726215)
  { state();
    lcd.setCursor(0,1);
    if(jumlah%3==1){
    lcd.print(F("Backlight"));
    lcd.setCursor(11,1);
    if(jumlah2 %2==1){ 
      lcd.print(F("-ON "));
      pilihanC=11;}
    else if(jumlah2 %2==0){ 
      lcd.print(F("-OFF"));
      pilihanC=12;
  }}else if(jumlah%3==2){
     lcd.print(F("Bluetooth"));
    lcd.setCursor(11,1);
    if(jumlah2 %2==1){ 
      lcd.print(F("-ON "));
      pilihanC=21;}
    else if(jumlah2 %2==0){ 
      lcd.print(F("-OFF"));
      pilihanC=22;
  }}else if(jumlah%3==0){
     lcd.print(F("Speed          "));
     pilihanC=3;
  }}
  lcd.print("*");
  if(pilihanC==11){
    EEPROM.write(1,1);
  }else if(pilihanC==12){EEPROM.write(1,0);}
  if(pilihanC==21){
    EEPROM.write(2,1);
  }else if(pilihanC==22){EEPROM.write(2,0);}
  EEPROM.commit();
  if(pilihanC==3){speedset();}
  delay(2000);
  results.value=0;
  awal();  
}

void speedset(){
  results.value=0;
  jumlah=1;
  jumlah2=EEPROM.read(3);
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(">SPEED SET");
  while(results.value!=16726215)
  { state();
    if(jumlah2<=1){jumlah2=1;}
    if(jumlah2>=10){jumlah2=10;}
    if(jumlah%2==1){
      lcd.setCursor(0,1);
      lcd.print("Speed:");
      lcd.print(v);
       v=jumlah2;}
     if(jumlah%2==0){
      lcd.setCursor(0,1);
      lcd.print("R-L:  ");
      lcd.print(vcal);
      vcal=jumlah2;
    }lcd.print("  ");
  }EEPROM.write(3,v);
   EEPROM.write(4,vcal);
   EEPROM.commit();
   delay(1000);
   awal();
}

void state(){
      results.value=0;
      if(irrecv.decode(&results)){
      irrecv.resume(); // Receive the next value
      if(results.value==16718055){
        jumlah--;}
      else if(results.value==16730805){
        jumlah++;}
      else if(results.value==16734885){
        jumlah2++;}
      else if(results.value==16716015){
        jumlah2--;}
      else if(results.value==16738455){
       berhenti();
        awal();}}
  }

void avfall(){
  while(digitalRead(linesensorL)==0&&digitalRead(linesensorR)==0){
    berhenti();
    state();
  }
  if(digitalRead(linesensorR)==0){
    mundur();
    delay(800);
    berhenti();
    belokkiri();
    delay(500);
    berhenti();
    }
  if(digitalRead(linesensorL)==0){
    mundur();
    delay(800);
    berhenti();
    belokkanan();
    delay(500);
    berhenti();
    }
}

void penggaris(){
  results.value=0;
  state();
  if(results.value==4294967295){
       berhenti();
        awal();}
  cm=hc.dist(0)*1.05;
  if(cm==0){cm=300;}
  lcd.setCursor(0,0);
  lcd.print(F("Distance:"));
  lcd.setCursor(0,1);
  lcd.print(cm);
  lcd.print(F("cm   "));
  penggaris();}

void key(){
   switch (results.value){
    case 16753245 :
    jumlah=keyboard[0][0];
    break;
    case 16736925 :
    jumlah=keyboard[0][1];
    break;
    case 16769565 :
    jumlah=keyboard[0][2];
    break;
    case 16720605 :
    jumlah=keyboard[1][0];
    break;
    case 16712445 :
    jumlah=keyboard[1][1];
    break;
    case 16761405 :
    jumlah=keyboard[1][2];
    break;
    case 16769055 :
    jumlah=keyboard[2][0];
    break;
    case 16754775 :
    jumlah=keyboard[2][1];
    break;
    case 16748655 :
    jumlah=keyboard[2][2];
    break;
    case 16750695 :
    jumlah=keyboard[3][1];
    break;
    case 16756815 :
    angka=angka/-10;
    break;
   }
}

void more(){
   lcd.clear();
   lcd.setCursor(0,0);
   lcd.print(F("<Testing>  "));
   delay(1000);
  for (d = 0;d<= 160; d += 1) { 
    myservo.write(d);              
    delay(15);                       
  }
  for (d = 160; d >= 0; d -= 1) { 
    myservo.write(d);              
    delay(15);                       
  }myservo.write(80);
   delay(1000);
    maju();
   delay(1000);
    mundur();
   delay(1000);
   berhenti();
   delay(500);
   belokkanan();
   delay(800);
   berhenti();
   delay(500);
   belokkiri();
   delay(800);
   berhenti();
   d=random(1,7);
   while(jumlah!=d){
    lcd.setCursor(0,1);
    lcd.print(F("press "));
    lcd.print(d);
    state();
    key();
   }lcd.print(F(" <OK>"));
   delay(1000);
   while(digitalRead(0)==1&&digitalRead(4)==1){
   lcd.setCursor(0,1);
   lcd.print(F("Lift The Robot"));
   } 
   delay(1000);
   lcd.clear();
   d=random(5,30);
   while(cm!=d){
    cm=hc.dist(0)*1.05;
  if(cm==0){cm=300;}
  lcd.setCursor(0,0);
  lcd.print(F("Set to "));
  lcd.print(d);
  lcd.print("cm  ");
  lcd.setCursor(0,1);
  lcd.print(cm);
  lcd.print("cm   ");
  }lcd.clear();
  lcd.setCursor(3,0);
  lcd.print(F("Testing"));
  lcd.setCursor(2,1);
  lcd.print(F("Successful"));
  delay(2000);
  d=1;
   awal();  
}

void kecepatan(){
 buttonState = digitalRead(19);
  if (buttonState != lastButtonState) {
    if (buttonState == HIGH) {
      buttonPushCounter++;
    } else { 
    }  
  }
  lastButtonState = buttonState;
   buttonState1 = digitalRead(23);
  if (buttonState1 != lastButtonState1) {
    if (buttonState1 == HIGH) {
      buttonPushCounter1++;
    } else {
  }}
  lastButtonState1 = buttonState1;
  cm=(buttonPushCounter+buttonPushCounter1)/2;
  }
