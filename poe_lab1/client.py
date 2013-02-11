#Citations:
#   pyserial port scan from http://pythontestscripts.blogspot.com/2011/12/pyserial-port-scan.html

import serial #serial library
from serial.tools import list_ports
import sys
from pylab import *
import numpy as np
import matplotlib.pyplot as plt

def connectToArduino():         #code to connect to the arduino through the serial port: 
    #loop through avail serial ports
    connected=False     #doesn't do anything until it finds an open serial port.        

    
    available=findAvailPorts()      #works with function defined below to find the available serial ports
    for avail in available:         #Takes the available ports found and processes them so they can be used to communicate with the Arduino
        s=serial.Serial(avail, 9600, timeout=1)
        msg=""
        r=""
        for i in range(100000):
            w=s.inWaiting()

            while w>0 and r!='\n':
                r=s.read(1)
                msg+=r
                w=s.inWaiting() 

            if(msg.strip()=='Arduino Ready'):       #when it has a port ready, it displays message that the arduino and python are ready.
                s.write('Python Ready\n')
                return s

            if r=='\n':         #if it doesn't have a port readyt , it doesn't display any message.
                msg=""  

    return None

def findAvailPorts():
    available=[]        #sets the available ports as an empty array. 
    ports = list_ports.comports()       #function from a library which finds available ports.

    for i in range(len(ports)):         #tries all the serial ports and returns the ones which are open.
        try:
            s = serial.Serial(ports[i][0], 9600, timeout=1)
            available.append(ports[i][0])       #Adds open ports to the array
            s.close()
        except serial.SerialException:
            pass

    return available        #Function returns the available ports so it can be used by the above function: connecttoArduino.

def showHeatMap(data):      #code to produce a graph of the intensity of light around the room.
    r=np.array(data[1])     #radius from polar coordinate position sent from Arduino.
    theta=np.array(data[0]) #angle position, sent from arduino.
    x=r*np.cos(theta)       #converting to rectangular:
    y=r*np.sin(theta)
    xmin = x.min()      #setting axies bounds:
    xmax = x.max()
    ymin = y.min()
    ymax = y.max()
    plt.subplots_adjust(hspace=0.5)     #setting the third dimension of the plot, intensity:
    plt.subplot(111)
    plt.hexbin(x,y,C=data[2], cmap=plt.cm.hot)
    plt.axis([xmin, xmax, ymin, ymax])
    plt.title("Light Source Heat Map")
    cb = plt.colorbar()
    cb.set_label('counts')

    plt.show()