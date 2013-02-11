#Citations:
#   pyserial port scan from http://pythontestscripts.blogspot.com/2011/12/pyserial-port-scan.html

import serial #serial library
from serial.tools import list_ports
import sys
from pylab import *
import numpy as np
import matplotlib.pyplot as plt

def connectToArduino():
    pass #dummy code
    #loop through avail serial ports
    connected=False

    
    available=findAvailPorts()
    for avail in available:
        s=serial.Serial(avail, 9600, timeout=1)
        msg=""
        r=""
        for i in range(100000):
            w=s.inWaiting()

            while w>0 and r!='\n':
                r=s.read(1)
                msg+=r
                w=s.inWaiting() 

            if(msg.strip()=='Arduino Ready'):
                s.write('Python Ready\n')
                return s

            if r=='\n':
                msg=""  

    return None

def findAvailPorts():
    available=[]
    ports = list_ports.comports()

    for i in range(len(ports)):
        try:
            s = serial.Serial(ports[i][0], 9600, timeout=1)
            available.append(ports[i][0])
            s.close()
        except serial.SerialException:
            pass

    return available

def showHeatMap(data):
    r=np.array(data[1])
    theta=np.array(data[0])
    x=r*np.cos(theta)
    y=r*np.sin(theta)
    xmin = x.min()
    xmax = x.max()
    ymin = y.min()
    ymax = y.max()
    plt.subplots_adjust(hspace=0.5)
    plt.subplot(111)
    plt.hexbin(x,y,C=data[2], cmap=plt.cm.hot)
    plt.axis([xmin, xmax, ymin, ymax])
    plt.title("Light Source Heat Map")
    cb = plt.colorbar()
    cb.set_label('counts')

    plt.show()

if __name__ == '__main__':
    a=[]
    b=[]
    c=[]
    for i in range(360):
        for j in range(30):
            a.append(i)
            b.append(j*3)
            c.append(5*rand(1))

    a=[a,b,c]
    showHeatMap(a)