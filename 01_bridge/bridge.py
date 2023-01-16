import serial
import serial.tools.list_ports as sp
import numpy as np
import requests
import time

IO_USERNAME = "PLACEHOLDER"
IO_KEY = "PLACEHOLDER"

class AFBridge():
    
    def serialSetup(self):
        # Setting up the serial comunication
        self.serial = None
        print("List of Available ports: ")

        # Retrieving the available port list
        ports = sp.comports()
        for p in ports:
            print(p.device, p.description)
            # Checking for Arduino connection
            if 'arduino' in p.description.lower():
                self.port = p.device
        
        # Connecting to the Arduino port
        try:
            if self.port is not None:
                self.serial = serial.Serial(self.port, 9600, timeout=0)
        except:
            self.serial = None

        # Opening the port
        self.serial.open()

        # Internal buffer
        self.buffer = []
        

    def setup(self):
        # General setup
        self.serialSetup()

    def loop(self):
        # Loop for serial handling
        last_time = time.time()
        while(True):
            # Fisrt I check for a byte on the serial port
            if not self.serial is None:
                if self.serial.in_waiting > 0:
                    # There are data available
                    last_char = self.serial.read(1)

                    # Checking for EOL
                    if last_char == b'\xfe':
                        pass

    def useData(self):
        pass

if __name__ == "__main__":
    bridge = AFBridge()
    bridge.setup()
    bridge.loop()