#code to create a GUI for a room light sensing device which allows 
# the user to control the precision of the scan and abort it. 
# It also gives them a button to connect to the arduino.

import sys      #inport libraries:
from PySide.QtCore import *
from PySide.QtGui import *
import client
import re

class Form(QDialog):        #GUI class
   
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.setWindowTitle('Pan and Tilt Scan')
        self.precision = QLineEdit("10")
        self.start = QPushButton("Start Scan")
        self.abort = QPushButton("Abort Scan")   
        self.start.setEnabled(False)
        self.abort.setEnabled(False)
        self.plot = QPushButton("Generate Plot")    
        self.arduinoConnect = QPushButton("Connect to Arduino") 
        # Create layout and add widgets
        mainlayout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QHBoxLayout()
        layout4 = QHBoxLayout()
        label1 = QLabel("Scan step size:\n(1<=x<=50)")
        self.status = QLabel("Status: Waiting for connection")
        mainlayout.addLayout(layout1)
        mainlayout.addLayout(layout2)
        mainlayout.addLayout(layout3)
        layout1.addWidget(label1)
        layout1.addWidget(self.precision,alignment=Qt.AlignRight)
        layout3.addWidget(self.start)
        layout3.addWidget(self.abort)
        layout4.addWidget(self.arduinoConnect)
        layout4.addWidget(self.plot)
        mainlayout.addSpacing(25)
        mainlayout.addWidget(self.status,alignment=Qt.AlignCenter)
        mainlayout.addLayout(layout4)
        # Set dialog layout
        self.setLayout(mainlayout)
        # Add button signal to greetings slot
        self.start.clicked.connect(self.startScan)
        self.abort.clicked.connect(self.abortScan)
        self.plot.clicked.connect(self.makePlot)
        self.arduinoConnect.clicked.connect(self.connectToArduino)
        self.serial=None

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.readData)

        self.tempdata = ""
        self.data = [[],[],[]]

    def readData(self): #reads data from the serial port
        while self.serial.inWaiting()>0:
            r=self.serial.read(1)
            if(r=='\n'):
                [[pos1,pos2,light]]=re.findall("(.*)\|(.*)\|(.*)", self.tempdata.strip())
                if(self.is_numeric(pos1) and self.is_numeric(pos2) and self.is_numeric(light)):
                    self.data[0].append(pos1)
                    self.data[1].append(pos2)
                    self.data[2].append(light)
                print self.tempdata
                self.tempdata=""
            elif(r=='@'):
                self.timer.stop()
                self.status.setText("Scan successful!")     #displays message when scann is successful
            else:
                self.tempdata+=r        #does nothing if scan wasn't successful.

    def connectToArduino(self):
        s=client.connectToArduino() #code to connect to arduino when the connect button is pushed. Also aborts when the abort button is pushed:
        if(s!=None):
            self.status.setText("Status: Connected!")
            self.start.setEnabled(True)
            self.abort.setEnabled(True)
            self.serial=s

    def startScan(self):        #starts the scan when the start scan button is pushed:
        #validate fields
        precision_text=str(self.precision.text())
        if(not self.is_numeric(precision_text)):         #checks entries into GUI fields for compatibility:
            msgBox=QMessageBox()
            msgBox.setText("Please enter valid numeric values.")
            msgBox.exec_()
        else:
            precision=int(precision_text)
            if(precision<1 or precision>50):
                msgBox=QMessageBox()
                msgBox.setText("Please enter valid values.")
                msgBox.exec_()
            else:
                cmd="1"+"{0:02d}".format(precision)+'\n'        #If entries are corrects, begins scan and displays message telling user it's scanning:
                print cmd.strip()
                self.serial.write(cmd)
                self.tempdata = ""
                self.data = [[],[],[]]
                self.timer.start(10)
                self.status.setText("Scanning......")

    # aborts scan if abort button is pushed
    def abortScan(self):        
        self.serial.write("0\n")
        self.status.setText("ABORT")

    def makePlot(self):         #Makes plot when called
        self.parseAngles()
        client.showHeatMap(self.data)

    #parses the angle data recieved from the servo
    def parseAngles(self):      
        self.data[0]=map(int, self.data[0])
        self.data[1]=map(int, self.data[1])
        self.data[2]=map(int, self.data[2])
        for i in range(len(self.data[0])):
            if(self.data[1][i]>90):
                self.data[1][i]-=90
                self.data[0][i]+=180
            else:
                self.data[1][i]=90-self.data[1][i]
            if(self.data[2][i]<0):
                self.data[2][i]=0
            elif(self.data[2][i]>100):
                self.data[2][i]=100
            self.data[2][i]=100-self.data[2][i]

    #checks to make sure s is numeric
    def is_numeric(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False
 
 
if __name__ == '__main__':  #Runs when you run the file. The main function:
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())