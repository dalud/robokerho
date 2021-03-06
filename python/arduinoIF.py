import serial
from serial.tools import list_ports
from time import sleep


class Arduino:
    def __init__(self):
        self.arduino = False
        self.i = 0
    
    def connect(self):        
        while(not self.arduino):
            try:
                for port in list_ports.comports():
                    print(port)
                self.arduino = serial.Serial(str(list_ports.comports()[self.i]).split()[0], 9600, timeout=1)
                #self.arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
                print('Arduino:', arduino)
            except:
                print('Connecting Arduino via USB. i =', self.i)
                self.i += 1

    def write(self, msg):        
        self.arduino.write(msg.encode())
        self.arduino.write('\n'.encode())
        #sleep(.01)

    def read(self):
        return self.arduino.readline()
        #sleep(1)
