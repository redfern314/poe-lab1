/*Setup functions for a semi-sphere room sweep which detects the ambient light of its suroundings 
using a photoresistor. This interfaces with a Python 3 GUI and code which produces a graph in Python.

Derek Redfern & Halie Murray-Davis

coments are cool!!!!
*/

//Get libraries: 
#include<Servo.h>

//Define global variables, set initial positions for motors to zero:

double theta = 0;    //sets initial position so we can control servo's position range=[1,180].
double phi = 0;

int led = 13;

Servo servo1;      //servos are servos
Servo servo2;

double data;
double counter;       //MAYBE?????
double photoresistor=1; //analog in chanel for photo resistor
int stepSize;

void setup() {
  servo1.attach(3);       //digital PWM pins for signal to the two servos
  servo2.attach(5);
  pinMode(led, OUTPUT);
  
  pinMode(photoresistor, INPUT);
  Serial.begin(9600);
  
  counter=0;       //defining variables. *counter not necessary, yet, but I think we'll need it.

  while (Serial.available() <= 0) {
      Serial.println("Arduino Ready");   // send a starting message
      delay(300);
  }
}



String inputString="";
boolean stringComplete = false;

void loop(){
  if (stringComplete) {
    Serial.println("Received!");
    stringComplete=false;
    digitalWrite(led, HIGH);
    //handle command here
  }
  delay(30);
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



int readSerial() {
  
}

void writeSerial() {
  
}

//calling python output stuff: Python :)

/*
void move1(PYTHON1) {
    if (PYTHON1==0) {
        end    
    }

    else {
      for (theta1<=180) {
          theta1++
      }
    }
}

*/
