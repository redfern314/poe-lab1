#Citations:
#   pyserial port scan from http://pythontestscripts.blogspot.com/2011/12/pyserial-port-scan.html

import serial #serial library
from serial.tools import list_ports

def connectToArduino(available):
    pass #dummy code
    #loop through avail serial ports
    flag=True

    while flag:
        for avail in available:
            s=serial.Serial(avail, 9600, timeout=1)
            w=s.inWaiting()
            #print w
            r=s.read(10)
            print r
            if(r==5):
                print avail+': '+r

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

connectToArduino(findAvailPorts())