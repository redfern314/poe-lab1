import sys
from PySide.QtCore import *
from PySide.QtGui import *
import client
import re

class Form(QDialog):
   
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        # Create widgets
        self.setWindowTitle('Pan and Tilt Scan')
        self.precision = QLineEdit("1")
        self.angle = QLineEdit("90")
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
        label2 = QLabel("Maximum scan angle:\n(0<=x<=90)")
        self.status = QLabel("Status: Waiting for connection")
        mainlayout.addLayout(layout1)
        mainlayout.addLayout(layout2)
        mainlayout.addLayout(layout3)
        layout1.addWidget(label1)
        layout1.addWidget(self.precision,alignment=Qt.AlignRight)
        layout2.addWidget(label2)
        layout2.addWidget(self.angle,alignment=Qt.AlignRight)
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

    def readData(self):
        while self.serial.inWaiting()>0:
            r=self.serial.read(1)
            if(r=='\n'):
                [[pos1,pos2,light]]=re.findall("(.*)\|(.*)\|(.*)", self.tempdata.strip())
                self.data[0].append(pos1)
                self.data[1].append(pos2)
                self.data[2].append(light)
                self.tempdata=""
            elif(r=='@'):
                self.timer.stop()
                self.status.setText("Scan successful!")
                #print self.data
            else:
                self.tempdata+=r

    def connectToArduino(self):
        s=client.connectToArduino()
        if(s!=None):
            self.status.setText("Status: Connected!")
            self.start.setEnabled(True)
            self.abort.setEnabled(True)
            self.serial=s

    def startScan(self):
        #validate fields
        precision_text=str(self.precision.text())
        angle_text=str(self.angle.text())
        if((not self.is_numeric(precision_text)) or (not self.is_numeric(angle_text))):
            msgBox=QMessageBox()
            msgBox.setText("Please enter valid numeric values.")
            msgBox.exec_()
        else:
            precision=int(precision_text)
            angle=int(angle_text)
            if(precision<1 or precision>50 or angle<0 or angle>90):
                msgBox=QMessageBox()
                msgBox.setText("Please enter valid values.")
                msgBox.exec_()
            else:
                cmd="1"+"{0:02d}".format(precision)+"{0:02d}".format(angle)+'\n'
                print cmd.strip()
                self.serial.write(cmd)
                self.tempdata = ""
                self.data = [[],[],[]]
                self.timer.start(10)
                self.status.setText("Scanning......")

    def abortScan(self):
        self.serial.write("0\n")
        self.status.setText("ABORT")

    def makePlot(self):
        self.parseAngles()
        client.showHeatMap(self.data)

    def parseAngles(self):
        self.data[0]=map(int, self.data[0])
        self.data[1]=map(int, self.data[1])
        self.data[2]=map(int, self.data[2])
        for i in range(len(self.data[0])):
            if(self.data[1][i]>90):
                self.data[1][i]=180-self.data[1][i]
                self.data[0][i]+=180

    def is_numeric(self, s):
        try:
            int(s)
            return True
        except ValueError:
            return False
 
 
if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())