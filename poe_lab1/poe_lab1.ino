/*Setup functions for a semi-sphere room sweep which detects the ambient light of its suroundings 
using a photoresistor. This interfaces with a Python 3 GUI and code which produces a graph in Python.

Derek Redfern & Halie Murray-Davis
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
int pos; //posions for motors
int pos2;

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

void movement(){
  for(pos=0; pos<180; pos = pos + precision) {
    servo1.write(pos);
    delay (50*precision^-1);
        if ((pos==0 || pos==180) && (pos2==(180-(angle/2)) || pos2==(90-(angle/2)))) {
          pos2=pos2+precision;
          servo2.write(pos2);
          delay (15);
        }
    }
    
  for (pos=180; pos>0; pos=pos - precision) {
    servo1.write(pos);
    delay (50*precision^-1);
        if ( (pos==0 || pos==180) && (pos2==(180-(angle/2)) || pos2==(90-(angle/2))) ) {
          pos2=pos2+precision;
          servo2.write(pos2);
          delay (15);
        }
  }
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
       
      movement();  //calls previously defined movement function.
    }
    else {}}}
