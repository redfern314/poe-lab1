#Citations:
#   pyserial port scan from http://pythontestscripts.blogspot.com/2011/12/pyserial-port-scan.html

import serial #serial library
from serial.tools import list_ports
import sys

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