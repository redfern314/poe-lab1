/*Setup functions for a semi-sphere room sweep which detects the ambient light of its suroundings 
using a photoresistor. This interfaces with a Python 3 GUI and code which produces a graph in Python.

Derek Redfern & Halie Murray-Davis
*/

//Define global variables, set initial positions for motors to zero:

int servo1=3;       //digital PWM pins for signal to the two servos.
int servo2=5;

double theta1 = 0;    //sets initial position so we can control servo's position range=[1,180].
double theta2 = 0;

double counter;       //MAYBE?????

double photoresistor=1; //analog in chanel for photo resistor


void setup() {
  pinmode(servo1, OUTPUT);      //sets up servos as outputs so they can be positioned.
  pinmode(servo2, OUTPUT);
  pinmode(photoresistor, INPUT);
  
  
  double counter=0;       //defining variables. *counter not necessary, yet, but I think we'll need it.
}

//calling python output stuff: Python :)

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

