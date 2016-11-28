#!/usr/bin/python

import smbus
import math
import sys
import ProBotConstantsFile
import Adafruit_BBIO.GPIO as GPIO
import StartFile

# Initialization of classes from local files
Pconst = ProBotConstantsFile.Constants()
InitProgram=StartFile.StartFileClass()

# Configuration the type of GPIO's
GPIO.setup(Pconst.RedLED, GPIO.OUT)
GPIO.setup(Pconst.GreenLED, GPIO.OUT)
GPIO.setup(Pconst.BlueLED, GPIO.OUT)

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

class mpu6050Class():
	
	# Now wake up the MPU6050 as it starts in sleep mode
	bus.write_byte_data(address, power_mgmt_1, 0)
	
	def __init__(self,  lastAccelerometerAngleX=0):
		self.lastAccelerometerAngleX=lastAccelerometerAngleX


	def read_byte(self, adr):
    		return bus.read_byte_data(address, adr)

	def read_word(self,adr):
    		high = bus.read_byte_data(address, adr)
    		low = bus.read_byte_data(address, adr+1)
    		val = (high << 8) + low
    		return val

	def read_word_2c(self,adr):
    		val = mpu6050.read_word(adr)
    		if (val >= 0x8000):
        		return -((65535 - val) + 1)
    		else:
        		return val

	def dist(self,a,b):
    		return math.sqrt((a*a)+(b*b))

	def get_y_rotation(self,x,y,z):
    		radians = math.atan2(x, mpu6050.dist(y,z))
    		return -math.degrees(radians)

	def get_x_rotation(self,x,y,z):
    		radians = math.atan2(y, mpu6050.dist(x,z))
    		return math.degrees(radians)
    		
    	def Calibration(self):
    		try:
	    		# Calibration of the MPU6050
	    		filteredX=mpu6050.Complementary_filter(0)
	    		while filteredX<-0.2 or filteredX>0.2:
	        		filteredX=mpu6050.Complementary_filter(0)
	
	    		GPIO.output(Pconst.BlueLED, GPIO.LOW)
	    		GPIO.output(Pconst.GreenLED, GPIO.HIGH)

        	except:
	    		InitProgram.StopProgram(0)
	    		print("Unexpected error:\n", sys.exc_info()[0])
	    		sys.exit('\n\nPROGRAM STOPPED!!!\n')
            		raise 
            
	def Complementary_filter(self, LoopTimeRatioSeg):
		
		gyro_xout = mpu6050.read_word_2c(0x43)
		gyro_yout = mpu6050.read_word_2c(0x45)
		gyro_zout = mpu6050.read_word_2c(0x47)

		accel_xout = mpu6050.read_word_2c(0x3b)
		accel_yout = mpu6050.read_word_2c(0x3d)
		accel_zout = mpu6050.read_word_2c(0x3f)

		accel_xout_scaled = accel_xout / 16384.0
		accel_yout_scaled = accel_yout / 16384.0
		accel_zout_scaled = accel_zout / 16384.0
	
		AccXangle=mpu6050.get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

		# Complementary filter
    		filteredX = float(0.98 * (self.lastAccelerometerAngleX+LoopTimeRatioSeg*gyro_xout/131.0) + (1 - 0.98) * AccXangle)
    		
    		self.lastAccelerometerAngleX=filteredX
    		
		filteredX=filteredX+Pconst.Angle_offset
		return filteredX
            

mpu6050 = mpu6050Class()


	
