import serial #serial library

def connectToArduino():
    pass #dummy code

ser = serial.Serial(0) #connect to first serial port
print ser.portstr #check to see which one that is

connectToArduino()