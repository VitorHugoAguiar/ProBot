#!/usr/bin/python

# Python Standard Library Imports
import Adafruit_BBIO.UART as UART
from Adafruit_I2C import Adafruit_I2C
import Adafruit_BBIO.GPIO as GPIO
from time import sleep
from decimal import *
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
#Testing connection 
if mpu.testConnection()==False:
	GPIO.output(RedLED, GPIO.HIGH)
	GPIO.output(GreenLED, GPIO.LOW)  
else:
	GPIO.output(RedLED, GPIO.LOW)
	GPIO.output(GreenLED, GPIO.HIGH) 
 
#Initialization of classes from the others files
PC = Sabertooth.PacketizedCommunication()
KF = Kalman.KalmanFilter()
Battery = BatteryMonitor.BatteryVoltage()
PID = Controllers.PIDControllers()
Enc=Encoders.EncodersReadings()
Pub_Sub=SocketCommunication.publisher_and_subscriber()


#Starting the main program
wheelPositionRef=0
VelocityRef=0
TurnMotorRight=0
TurnMotorLeft=0


GPIO.output(RedLED, GPIO.HIGH)	
PC.set_baud(PC.addr,PC.baud)
sleep(3)									# Wait to stabilize the communication
																			
PC.stopAndReset()

GPIO.output(GreenLED, GPIO.HIGH)

AccXangleAverage=-0.43432634994							# Calibration of the MPU6050
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
		wheelPosition=Encoders[1]

		subscriber=Pub_Sub.subscriber()
		if subscriber==None:
			subscriber=0			
		else:
			forward=subscriber[0]+""+subscriber[1]+""+subscriber[2]+""+subscriber[3]+""+subscriber[4]			
			reverse=subscriber[6]+""+subscriber[7]+""+subscriber[8]+""+subscriber[9]+""+subscriber[10]
			left=subscriber[12]+""+subscriber[13]+""+subscriber[14]+""+subscriber[15]+""+subscriber[16]
			right=subscriber[18]+""+subscriber[19]+""+subscriber[20]+""+subscriber[21]+""+subscriber[22]			
			
		forwardDecimal = float(Decimal(forward))
		if forwardDecimal>0:
			VelocityRef=float(forwardDecimal*1.3)
			
		reverseDecimal = float(Decimal(reverse))
		if reverseDecimal>0:
			VelocityRef=-float(reverseDecimal*1.3)

		
		# With the values from the server, we can calculate the outputs from the controllers			
		PidVelocityRef= PID.standardPID(wheelPositionRef,wheelPosition, 0)			
		PidAngleRef= PID.standardPID(VelocityRef,wheelVelocity, 1)
		PidMotorRef = PID.standardPID(PidAngleRef,kalAngleX, 2)


		if forwardDecimal == 0 and reverseDecimal==0:
			VelocityRef=0

		
		
		rightDecimal = float(Decimal(right))
		if rightDecimal>0:
			TurnMotorRight=float(rightDecimal*40)
			TurnMotorLeft=-float(rightDecimal*40)
	
		
		leftDecimal = float(Decimal(left))
		if leftDecimal>0:
			TurnMotorRight=-float(leftDecimal*40)
			TurnMotorLeft=float(leftDecimal*40)

		if rightDecimal==0 and leftDecimal==0:
			TurnMotorRight=0
			TurnMotorLeft=0

		rightMotor=float(PidMotorRef+TurnMotorRight)
		leftMotor=float(PidMotorRef+TurnMotorLeft)


		graph_variable1=wheelPositionRef
		graph_variable2=wheelPosition	
		graph_variable3=PidVelocityRef	
		graph_variable4=wheelVelocity	
		graph_variable5=PidAngleRef	
		graph_variable6=kalAngleX
		graph_variable7=int(PidMotorRef)	
		graph_variable8=0

		# Setting the Beaglebone as publisher to send some variables to the server
		publisher=Pub_Sub.publisher(graph_variable1, graph_variable2, graph_variable3, graph_variable4, graph_variable5, graph_variable6, graph_variable7, graph_variable8)
		


		# Sending the values to the Sabertooth that is connected to the motors	
			
		PC.drive(PC.addr, 1, int(rightMotor))
															
		PC.drive(PC.addr, 2, int(leftMotor))
		
	except:
		PC.stopAndReset()
		print "\n\nPROGRAM STOPPED!!!\n"
		sys.exit(0)
		raise
		
