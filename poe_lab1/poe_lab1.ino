/*Setup functions for a semi-sphere room sweep which detects the ambient light of its suroundings 
using a photoresistor. This interfaces with a Python 3 GUI and code which produces a graph in Python.

Derek Redfern & Halie Murray-Davis

coments are cool!!!!
*/

//Get libraries: 
#include<Servo.h>
#include <SoftwareSerial.h>;
#include <stream.h>;

//Define global variables, set initial positions for motors to zero:

double theta = 0;    //sets initial position so we can control servo's position range=[1,180].
double phi = 0;

Servo servo1;      //servos are servos
Servo servo2;
int pos;

//double data;
double counter;       //MAYBE?????
double photoresistor=1; //analog in chanel for photo resistor
int stepSize;
SoftwareSerial portOne (0,1);

//stuff from serial port:
//char start;
int precision;
int angle;


void setup() {
  Serial.begin(9600);
  servo1.attach(3);       //digital PWM pins for signal to the two servos
  servo2.attach(5);
  portOne.begin(9600); //could need a while statement but ex says needed only for Leonardo...
  pinMode(photoresistor, INPUT);
  
  
  counter=0;       //defining variables. *counter not necessary, yet, but I think we'll need it.
}

void loop(){
  portOne.listen();
  Serial.println("Data from port one:");
  while (portOne.available()>0) {
    
    if (Serial.read()>=0) {
      
      char c=Serial.read();
      char d=Serial.read();
      int C=(int) (c);
      int D=(int) (d);
      precision= 'C' + 'D';
      
      char a=Serial.read();
      char b=Serial.read();
      int A= (int) (a); 
      int B = (int) (b);
      angle='A' + 'B';
      Serial.print(angle);
      
      for(pos=0; pos<180; pos = pos + precision) {
        servo1.write(pos);
        delay (50*precision^-1);
      }
      
      
          
    }
    else {}
    
    //Serial.print(data);
    /*if portOne(1)==1{
    
    }
    else {
      end
    }
    */
  }

}


/*
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
