#!/usr/bin/python

# Python Standard Library Imports
import Adafruit_BBIO.UART as UART
from Adafruit_I2C import Adafruit_I2C
import Adafruit_BBIO.GPIO as GPIO
from time import sleep
import time
import math
import sys
import csv
import zmq
import mpu6050
import Sabertooth
import Kalman
import BatteryMonitor
import Controllers
import Encoders
import SocketCommunication
import DataFile

RAD_TO_DEG = 57.29578							

# Start the UART1
UART.setup("UART1")

# Configuration of the GPIO's
RedLED = "P8_13"
GreenLED = "P9_27"
ResetButton = "P8_15"

GPIO.setup(ResetButton, GPIO.IN)
GPIO.setup(RedLED, GPIO.OUT)
GPIO.setup(GreenLED, GPIO.OUT)

# MPU6050 initialization
mpu = mpu6050.MPU6050()
mpu.initialize()
#Test connection 
if mpu.getDeviceID() != 52:
	GPIO.output(RedLED, GPIO.HIGH)

#Initialization of classes from the others files
PC = Sabertooth.PacketizedCommunication()
KF = Kalman.KalmanFilter()
Battery = BatteryMonitor.BatteryVoltage()
PID = Controllers.PIDControllers()
Enc=Encoders.EncodersReadings()
Data=DataFile.DataClass()
Pub_Sub=SocketCommunication.publisher_and_subscriber()


#Starting the main program
wheelPositionRef=0

GPIO.output(RedLED, GPIO.HIGH)	
PC.set_baud(PC.addr,PC.baud)
sleep(3)									# Wait to stabilize the communication
																			
PC.stopAndReset()

GPIO.output(GreenLED, GPIO.HIGH)

AccXangleAverage=0.43432634994							# Calibration of the MPU6050
GYRxAverage=-65

GPIO.output(RedLED, GPIO.LOW)
sleep(1.5)	

	
while True:
	try:
		LoopTime=time.time()
		
		# Verification of the voltage from the Beaglebone and motors batteries
		Battery.BatteryVoltageBeaglebone()	
		Battery.BatteryVoltageMotors()
	
		#Read of the MPU6050 values
		AccAndGyr = mpu.MPU6050Values()	
		AccXangle = AccAndGyr[0]
		GYRx = AccAndGyr[1]
		
		#Calculate the new x angle with the ofset of the calibration from the MPU6050 
		ax_raw = AccXangle - AccXangleAverage		
		GYRx_raw = GYRx - GYRxAverage
		# After the readings, we use the Kalman filter to eliminate the variations from the readings		
		kalAngleX = KF.KalmanCalculate(ax_raw,GYRx_raw, LoopTime)
		
		# Readings from the encoders
		Encoders=Enc.EncodersValues()
		wheelVelocity=Encoders[0]
		wheelPositionPosition=Encoders[1]

		# We use zmq to publisher and subscribe some values to/from a server (PC)
		# Initialition of the subscriber on the BeagleBone. With that, we can receive the values for the compensators from the midi controler on the server (PC)
		subscriber=Pub_Sub.subscriber()
		# Just some code to decode the message from the server
		if subscriber==None:
			pass
		
		else:
			for x in range(0, len(subscriber)):
				
				if(subscriber[x]==" "):	
					if x==1:					
						id= subscriber[x-1]
						if len(subscriber)==5:
							value=subscriber[len(subscriber)-3]+ "" +subscriber[len(subscriber)-2]+ "" +subscriber[len(subscriber)-1]
						if len(subscriber)==4:
							value=subscriber[len(subscriber)-2]+ "" +subscriber[len(subscriber)-1]
						if len(subscriber)==3:
							value=subscriber[len(subscriber)-1]	
										
					else:	
						id=subscriber[x-2]+""+subscriber[x-1]
						if len(subscriber)==6:
							value=subscriber[len(subscriber)-3]+ "" +subscriber[len(subscriber)-2]+ "" +subscriber[len(subscriber)-1]
						if len(subscriber)==5:
							value=subscriber[len(subscriber)-2]+ "" +subscriber[len(subscriber)-1]
						if len(subscriber)==4:
							value=subscriber[len(subscriber)-1] 
				
		# With the values from the server, we can calculate the outputs from the controllers			
		PidVelocityRef= PID.standardPID(wheelPositionRef,wheelPositionPosition, 0 , int(id), int(value))			
		#PidAngleRef= PID.standardPID(PidVelocityRef,wheelVelocity, 1, int(id), int(value))
		PidMotorRef = PID.standardPID(PidVelocityRef,kalAngleX, 2, int(id), int(value))
												
		# Setting the Beaglebone as publisher to send some variables to the server
		publisher=Pub_Sub.publisher(PidMotorRef, kalAngleX)
			
		# Sending the values to the Sabertooth that is connected to the motors	
		PC.drive(PC.addr, 1, int(PidMotorRef))
															
		PC.drive(PC.addr, 2, int(PidMotorRef))
		
	except:
		PC.stopAndReset()
		print "\n\nPROGRAM STOPPED!!!\n"
		sys.exit(0)
		raise
		
