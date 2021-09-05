#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

#include <SPI.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

uint16_t phonemeA[] = {400, 350, 370, 420, 300, 250, 300, 400, 400}; //AEIH
uint16_t phonemeO[] = {375, 375, 550, 250, 150, 400, 300, 340, 400}; //OUW  !!!!!
uint16_t phonemeB[] = {350, 400, 300, 330, 350, 330, 350, 340, 440}; //BMP
uint16_t phonemeG[] = {360, 390, 300, 330, 350, 330, 300, 340, 400}; //GKXYJR
uint16_t phonemeS[] = {365, 385, 300, 330, 350, 330, 300, 450, 400}; //CDNSTZKQ
uint16_t phonemeTh[] = {360, 390, 350, 350, 350, 350, 350, 495, 350};//Th
uint16_t phonemeL[] = {375, 375, 370, 420, 300, 250, 300, 480, 400};//L
uint16_t phonemeF[] = {350, 400, 300, 330, 350, 330, 260, 340, 400};//FV

char chars[] = { 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z' };

char inPrimary;
char inSecondary;

int pause = 150;

int val = 375;
int width0 = 375;
int width1 = 375;

void setup() {
   pinMode(2, INPUT);
   Serial.begin(9600);       // start serial communication at 9600bps
   delay(200);
   pwm.begin();
   pwm.setPWMFreq(60);
  
   phonemePose(phonemeB);   
}
void loop() {
  if(digitalRead(2)) {
    phonemeMatch(chars[random(sizeof(chars))]);
  }
  delay(10);  
}

void phonemePose(uint16_t phoneme[]) {
  for(uint8_t i = 0; i <=8; i++){
    pwm.setPWM(i, 0, phoneme[i]);
  }
}

void phonemeMatch(char letter){
  Serial.println(letter);
  if ((letter == 'a') || (letter == 'e') || (letter == 'i') || (letter == 'h'))
    phonemePose(phonemeA);
  if ((letter == 'o') || (letter == 'u') || (letter == 'w'))
    phonemePose(phonemeO);
  if ((letter == 'b') || (letter == 'm') || (letter == 'p'))
    phonemePose(phonemeB);  
  if ((letter == 'g') || (letter == 'k') || (letter == 'x') || (letter == 'y') || (letter == 'j') || (letter == 'r'))
    phonemePose(phonemeG);    
  if ((letter == 'c') || (letter == 'd') || (letter == 'n') || (letter == 's') || (letter == 't') || (letter == 'z') || (letter == 'k') || (letter == 'q'))
    phonemePose(phonemeS);  
  if ((letter == 'l'))
    phonemePose(phonemeL);
  if ((letter == 'f') || (letter == 'v'))
    phonemePose(phonemeF);  

  delay(pause);
}
