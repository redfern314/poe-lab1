/*Setup functions for a semi-sphere room sweep which detects the ambient light of its suroundings 
using a photoresistor. This interfaces with a Python 3 GUI and code which produces a graph in Python.

Derek Redfern & Halie Murray-Davis
*/

//Get libraries: 
#include<Servo.h>;
#include <stream.h>;

//Define global variables, set initial positions for motors to zero:

double theta = 0;    //sets initial position so we can control servo's position range=[1,180].
double phi = 0;

Servo servo1;      //servos are servos
Servo servo2;
int pos; //positions for motors
int pos2;

int led = 13;

boolean runScan = false;

String data;
double photoresistor=A0; //analog in chanel for photo resistor
int i=0; //counter for data acquision from photo resistor.

String inputString="";
boolean stringComplete = false;

//stuff from serial port:
char start;
int precision=10;
int angle=30;


void setup() {
  Serial.begin(9600);     //start serial port so we can write data to it.
  servo1.attach(3);       //digital PWM pins for signal to the two servos
  servo2.attach(5);
  pinMode(photoresistor, INPUT);    //set photoresisstor up as an input
  pinMode(led, OUTPUT);
  
  
  while (Serial.available() <= 0) { //wait for a response
      Serial.println("Arduino Ready");   // send a starting message
      delay(300);
  }
}

void movement(){        //define a function which will move the servos in a specified pattern.
  for(pos==0; pos<=180; pos = pos + round(precision/9)) {    //Step through an arch for the bottom servo.
    servo1.write(pos);
    delay (50/precision);
    returndata();
        if ((pos==0 || pos==180)){    //move the photo resistor up a step (size of which is determined by the percision value) at ends of arc.
            delay (70);
            pos2=pos2+precision;
            servo2.write(pos2);
            delay (30);
            returndata();
        }
    }
    
  for (pos==180; pos>0; pos = pos - round(precision/9)) {     //this case accomplishes movement in the opposite direction
    servo1.write(pos);
    delay (50/precision);
    returndata();
      if (pos==0 || pos2==180)  {
        pos2=pos2+precision;
        servo2.write(pos2);
        delay (30);
        returndata();
      }
  }
  if(pos2>=180) {
    pos=0;
    pos2=0;
    servo1.write(pos);
    servo2.write(pos2);
    Serial.print("@");
    runScan=false;
  }
}

void returndata(){      //sets up a function which writes data to the serial port so we can use it in the python code to make a graph.
    int light=analogRead(photoresistor);    //reads the light from the photoresistor.
    Serial.print(pos);
    Serial.print("|");
    Serial.print(pos2);
    Serial.print("|");
    Serial.print(light);
    Serial.print("\n");
}

void loop(){
  if (stringComplete) {
    stringComplete=false;
    if(inputString[0]=='0') {
      runScan=false;
    } else if(inputString[0]=='1') {
      //TODO: extract new vars
      runScan=true;
      pos=0;
      pos2=0;
      digitalWrite(led, HIGH);
    }
    inputString="";
  }
  if (runScan) {
    movement(); //calls previously defined movement function.
  }
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    } 
  }
}
