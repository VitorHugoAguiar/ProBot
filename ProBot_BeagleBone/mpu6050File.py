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

class mpu6050Class():
	# Power management registers
	power_mgmt_1 = 0x6b
	power_mgmt_2 = 0x6c
	bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
		
	# Scale Modifiers
    	ACCEL_SCALE_MODIFIER_2G = 16384.0
    	ACCEL_SCALE_MODIFIER_4G = 8192.0
    	ACCEL_SCALE_MODIFIER_8G = 4096.0
    	ACCEL_SCALE_MODIFIER_16G = 2048.0

    	GYRO_SCALE_MODIFIER_250DEG = 131.0
    	GYRO_SCALE_MODIFIER_500DEG = 65.5
    	GYRO_SCALE_MODIFIER_1000DEG = 32.8
    	GYRO_SCALE_MODIFIER_2000DEG = 16.4
	
	accel_scale_modifier=ACCEL_SCALE_MODIFIER_2G
	gyro_scale_modifier=GYRO_SCALE_MODIFIER_250DEG

    	def __init__(self, address=0x68, lastAccelerometerAngleX=0):
		self.lastAccelerometerAngleX=lastAccelerometerAngleX	
		self.address = address
		# Now wake up the MPU6050 as it starts in sleep mode
		self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)
		
	def read_byte(self, adr):
    		return self.bus.read_byte_data(self.address, adr)

	def read_word(self,adr):
    		high = self.bus.read_byte_data(self.address, adr)
    		low = self.bus.read_byte_data(self.address, adr+1)
    		val = (high << 8) + low
    		return val

	def read_word_2c(self,adr):
    		val = self.read_word(adr)
    		if (val >= 0x8000):
        		return -((65535 - val) + 1)
    		else:
        		return val

	def dist(self,a,b):
    		return math.sqrt((a*a)+(b*b))

	def get_y_rotation(self,x,y,z):
    		radians = math.atan2(x, self.dist(y,z))
    		return -math.degrees(radians)

	def get_x_rotation(self,x,y,z):
    		radians = math.atan2(y, self.dist(x,z))
    		return math.degrees(radians)


	def Calibration(self):
		AccAndGyr=self.Accx_Gyro()
		AccXangle=AccAndGyr[0]
		gyro_xout_scaled=AccAndGyr[1]
    		filteredX=self.Complementary_filter(AccXangle,gyro_xout_scaled,0)
		
		while (filteredX<-0.5 or filteredX>0.5):
                	AccAndGyr=self.Accx_Gyro()
                	AccXangle=AccAndGyr[0]
                	gyro_xout_scaled=AccAndGyr[1]
			filteredX=self.Complementary_filter(AccXangle,gyro_xout_scaled,0)
			
		GPIO.output(Pconst.BlueLED, GPIO.LOW)
	    	GPIO.output(Pconst.GreenLED, GPIO.HIGH)
		return filteredX



	def Accx_Gyro(self):
		
                gyro_xout = self.read_word_2c(0x43)
		gyro_yout = self.read_word_2c(0x45)
                gyro_zout = self.read_word_2c(0x47)

                gyro_xout_scaled = gyro_xout/self.gyro_scale_modifier
                gyro_yout_scaled = gyro_yout/self.gyro_scale_modifier
                gyro_zout_scaled = gyro_zout/self.gyro_scale_modifier

                accel_xout = self.read_word_2c(0x3b)
                accel_yout = self.read_word_2c(0x3d)
                accel_zout = self.read_word_2c(0x3f)

                accel_xout_scaled = accel_xout /self.accel_scale_modifier
                accel_yout_scaled = accel_yout /self.accel_scale_modifier 
                accel_zout_scaled = accel_zout /self.accel_scale_modifier

                AccXangle=self.get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
		
		return AccXangle, gyro_xout_scaled
	
	
	def Complementary_filter(self, AccX, GYRx, LoopTimeRatioSeg):

		# Complementary filter
    		filteredX = float(0.98 * (self.lastAccelerometerAngleX+LoopTimeRatioSeg*GYRx) + (1 - 0.98) * AccX)
    		self.lastAccelerometerAngleX=filteredX
		filteredX=filteredX+Pconst.Angle_offset

		return filteredX
