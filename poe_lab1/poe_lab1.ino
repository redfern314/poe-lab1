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
int pos; //posions for motors
int pos2;

String data;
double photoresistor=1; //analog in chanel for photo resistor
int i=0; //counter for data acquision from photo resistor.

//stuff from serial port:
char start;
int precision;
int angle;


void setup() {
  Serial.begin(9600);     //start serial port so we can write data to it.
  servo1.attach(3);       //digital PWM pins for signal to the two servos
  servo2.attach(5);
  pinMode(photoresistor, INPUT);    //set photoresisstor up as an input
}

void movement(){        //define a function which will move the servos in a specified pattern.
  for(pos==0; pos<180; pos = pos + round(precision/9)) {    //Step through an arch for the bottom servo.
    servo1.write(pos);
    delay (50/precision);
        if ((pos==0 || pos==180)){    //move the photo resistor up a step (size of which is determined by the percision value) at ends of arc.
            delay (70);
            pos2=pos2+precision;
            servo2.write(pos2);
            delay (30);
        }
    }
    
  for (pos==180; pos>0; pos = pos - round(precision/9)) {     //this case accomplishes movement in the opposite direction
    servo1.write(pos);
    delay (50/precision);
      if (pos2==(180-(angle/2)) || pos2==(90-(angle/2)))  {
      pos2=pos2+precision;
      servo2.write(pos2);
      delay (30);
      }
  }
}

void returndata(){      //sets up a function which writes data to the serial port so we can use it in the python code to make a graph.
    int light=analogRead(photoresistor);    //reads the light from the photoresistor.
    String e = String (pos);      //change the position integers into strings:
    String f = String (pos2); 
    String g = String (light);
    String data = e+f+g;      //combines the strings into a single sting
    Serial.println(data);     //prints data to the serial port
}

void loop(){
  Serial.println("Data from port one:");    
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
    }    
     movement();  //calls previously defined movement function.
     returndata();
    }