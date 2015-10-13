#!/usr/bin/python

# Python Standard Library Imports
import serial
import struct

# Baudrate and address for sabertooth controller
baud=19200
addr=128

# Define serial connection
ser = serial.Serial('/dev/ttyO1',baud, timeout=0.5)

# Initialization of the sabertooth connection
print "\nSending commands to the address",addr, "with a baudrate of\n", baud
ser.flush()
ser.write(chr(0xAA))
ser.flush()

# Packetized serial mode in the Sabertooth
class PacketizedCommunication():
	
	# Configuration of the parameters for the communication with Sabertooth/Kangaroo 
	commands = {'motor1fwd':0,'motor1bwd':1,'vmin':2,'vmax':3,'motor2fwd':4,'motor2bwd':5,'motor1drive':6,'motor2drive':7,'timeout':14,'baud':15}
	baudcodes = {2400:1, 9600:2, 19200:3, 38400:4}

	def set_baud(self,address, baudrate):
		self.packet = self.make_packet(address, self.commands['baud'], self.baudcodes[baudrate])	# Packet format
		ser.write(self.packet)										# Write packet in the serial

	def drive(self,address, motor, speed):									# Drive function for both motors with the commands defined above
		if motor==1:
			command = 0
		elif motor==2:
			command = 4
		else:
			return false
		if speed<0:											 # Values must be always positive and direction is given by the command +1
			command = command + 1
			speed = -speed
		if speed >127:											 # Since all values are positive we only compare with 127
			speed = 127
		self.packet = self.make_packet(address, command, speed)
		ser.write(self.packet)
		
	def make_packet(self,address,command,data):								 # Packet struct
		return struct.pack('BBBB', address, command, data, (127&(address+command+data)))

	def stopAndReset(self):											 # Stop and Reset function to begin or end
		self.drive(addr, 1, int(0))
		self.drive(addr, 2, int(0))
		
		
