#Citations:
#   pyserial port scan from http://pythontestscripts.blogspot.com/2011/12/pyserial-port-scan.html

import serial #serial library
from serial.tools import list_ports
import sys

def connectToArduino():
    pass #dummy code
    #loop through avail serial ports
    connected=False

    for i in range(100):
        available=findAvailPorts()
        msg=""
        for avail in available:
            s=serial.Serial(avail, 9600, timeout=1)
            w=s.inWaiting()
            
            r=""
            while w>0 and r!='\n':
                msg+=r
                r=s.read(1)
                w=s.inWaiting()   

            print msg
            if(msg.strip()=='Arduino Ready' or msg.strip()=='Connected\n'):
                #connected=True
                print avail+': '+msg.strip()+'!!!!'
                s.write('Python Ready\n')

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