#!/usr/bin/python

# Python Standard Library Imports
import Adafruit_BBIO.UART as UART
import sys
import serial
import struct
import time
import ProBotConstantsFile
import Adafruit_BBIO.GPIO as GPIO

# Initialization of classes from local files
Pconst = ProBotConstantsFile.Constants()

# Configuration the type of GPIO's
GPIO.setup(Pconst.RedLED, GPIO.OUT)
GPIO.setup(Pconst.GreenLED, GPIO.OUT)
GPIO.setup(Pconst.BlueLED, GPIO.OUT)

# Start the UART1
UART.setup("UART1")


# Packetized serial mode in the Sabertooth
class SabertoothClass():
    # Configuration of the parameters for the communication with Sabertooth 
    commands = {'motor1fwd': 0, 'motor1bwd': 1, 'vmin': 2, 'vmax': 3, 'motor2fwd': 4, 'motor2bwd': 5, 'motor1drive': 6, 'motor2drive': 7, 'timeout': 14, 'baud': 15}
    baudcodes = {2400: 1, 9600: 2, 19200: 3, 38400: 4}

    # Define serial connection
    ser = serial.Serial('/dev/ttyO1', Pconst.baud, timeout=0.5)

    # Initialization of the sabertooth connection
    ser.flush()
    ser.write(chr(0xAA))
    ser.flush()

    def set_baud(self, address, baudrate):
        self.packet = self.make_packet(address, self.commands['baud'], self.baudcodes[baudrate])		# Packet format
        self.ser.write(self.packet)										# Write packet in the serial

    def drive(self, address, motor, speed):									# Drive function for both motors with the commands defined above
        if motor == 1:
            command = 0
        elif motor == 2:
            command = 4
        else:
            return false

        if speed < 0:												# Values must be always positive and direction is given by the command +1
            command = command + 1
            speed = -speed
        if speed > 127:												# Since all values are positive we only compare with 127
            speed = 127
        self.packet = self.make_packet(address, command, speed)
        self.ser.write(self.packet)

    def make_packet(self, address, command, data):								# Packet struct
        return struct.pack('BBBB', address, command, data, (127 & (address+command + data)))

    def stopAndReset(self):											# Stop and Reset function to begin or end
        self.drive(Pconst.addr, 1, int(0))
        self.drive(Pconst.addr, 2, int(0))
        self.ser.flush()	
        
    def CommunicationStart(self):
        try:
	    import StartFile
            InitProgram=StartFile.StartFileClass()
	    
	    # Starting the communication with Sabertooth
            GPIO.output(Pconst.RedLED, GPIO.HIGH)
            self.set_baud(Pconst.addr, Pconst.baud)
            time.sleep(3)												# Wait to stabilize the communication

            self.stopAndReset()

       	except:
	    InitProgram.StopProgram()
	    print("Unexpected error:\n", sys.exc_info()[0])
	    sys.exit('\n\nPROGRAM STOPPED!!!\n')
            raise
