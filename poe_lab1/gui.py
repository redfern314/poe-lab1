import sys
from PySide.QtCore import *
from PySide.QtGui import *
import client

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
        label2 = QLabel("Maximum scan angle:\n(0<x<=90)")
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
       
    # Greets the user
    def greetings(self):
        print ("Hello %s" % self.edit.text())    

    def connectToArduino(self):
        s=client.connectToArduino()
        if(s!=None):
            self.status.setText("Status: Connected!")
            self.start.setEnabled(True)
            self.abort.setEnabled(True)
            self.serial=s

    def startScan(self):
        #
        pass

    def abortScan(self):
        self.serial.write("0\n")
        pass

    def makePlot(self):
        pass
 
 
if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    # Create and show the form
    form = Form()
    form.show()
    # Run the main Qt loop
    sys.exit(app.exec_())