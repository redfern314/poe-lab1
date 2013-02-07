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

Servo servo1;      //servos are servos
Servo servo2;

double data;
double counter;       //MAYBE?????
double photoresistor=1; //analog in chanel for photo resistor
int stepSize;

void setup() {
  servo1.attach(3);       //digital PWM pins for signal to the two servos
  servo2.attach(5);
  
  pinMode(photoresistor, INPUT);
  Serial.begin(9600);
  
  counter=0;       //defining variables. *counter not necessary, yet, but I think we'll need it.
}

void loop(){
  while (Serial.available() > 0) { //we have a command waiting!
    
  }
  if(stepSize) {
    
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
