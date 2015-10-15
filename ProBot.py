#!/usr/bin/python

# Python Standard Library Imports
import Adafruit_BBIO.UART as UART
from Adafruit_I2C import Adafruit_I2C
import Adafruit_BBIO.GPIO as GPIO
import serial
import struct
import time
import math
from time import sleep
import datetime
import mpu6050
import Sabertooth
import Kalman
import BatteryMonitor
import Controllers

# Start the UART1
UART.setup("UART1")

# Configuration of the GPIO's
RedLED="P8_13"
GreenLED="P9_27"
ResetButton="P8_15"

GPIO.setup(ResetButton, GPIO.IN)
GPIO.setup(RedLED, GPIO.OUT)
GPIO.setup(GreenLED, GPIO.OUT)

# MPU6050 initialization
mpu = mpu6050.MPU6050()
mpu.initialize()
#Test connection 
if mpu.getDeviceID()!=52:
	GPIO.output(RedLED, GPIO.HIGH)

#Initialization of classes from the others files
PC=Sabertooth.PacketizedCommunication()
KF=Kalman.KalmanFilter()
Battery=BatteryMonitor.BatteryValue()
PID=Controllers.PIDControllers()

# Calibration of the values from the sensor MPU6050 (vertical position)
def MPU6050_Calibration():
	
	numReadings=100													# Number of readings for calibration
	ax_total=0
	GYRx_total=0

	while (AccXangle<-1 or AccXangle>1):									# Keep angle between these values
		MPU6050_Values()												# Call function to get the values
	
	for i in range(0,numReadings):
		ax_total=AccXangle+ax_total
		GYRx_total=GYRx+GYRx_total
	
	ax_average=float (ax_total)/numReadings								# Average accelerometer value
	GYRx_average=float (GYRx_total)/numReadings							# Average gyroscope value
	
	return ax_average, GYRx_average										# Returns the offset
	
	
def MPU6050_Values():
	
	global AccXangle
	global GYRx
	PI = 3.14159265358979323846
	RAD_TO_DEG = 57.29578												# Convertion rate, Rad to Deg
 
	GYRx=mpu.readGYRx()												# Reading of variables of interest
	accZ=mpu.readACCz()
	accY=mpu.readACCy()
	
	AccXangle = (math.atan2(accY,accZ)+PI)*RAD_TO_DEG						# Calculation of the angle in X axis
	AccXangle-=180													# Correction of angle (depends on the position of the sensor)
	
	return AccXangle,GYRx


PC.set_baud(Sabertooth.addr,Sabertooth.baud)
sleep(3)																# Wait to stabilize the communication

PC.stopAndReset()

AccAndGyr=MPU6050_Values()											# Make a reading from the MPU6050 to get in the while () condition from the calibration
AccXangle=AccAndGyr[0]
GYRx=AccAndGyr[1]				

AccAndGyrAverage=MPU6050_Calibration()									# Calibration routine												
ax_average=AccAndGyrAverage[0]
GYRx_average=AccAndGyrAverage[1]

GPIO.output(GreenLED, GPIO.HIGH)											# Led state to green
sleep(1.5)

PiVelocityRef=0.000	

while True:
	LoopTime = time.time()																	# Start the time stamp for the loop
	
	if Battery.BatteryVoltage()<10.5:															# Case low battery, stop robot
		PC.stopAndReset()
	else:
		#Read of the MPU6050 values
		AccAndGyr=MPU6050_Values()											# Make a reading from the MPU6050 to get in the while () condition from the calibration
		AccXangle=AccAndGyr[0]
		GYRx=AccAndGyr[1]	
	
		#Calculate the new x angle with the ofset of the Calibration 
		ax_raw=AccXangle-ax_average														# Calculate the values from MPU6050 to send to the Kalman filter
		GYRx_raw=GYRx-GYRx_average
		
		x_angle=KF.KalmanCalculate(ax_raw,GYRx_raw,LoopTime)									# Get filtered value in function of acceleration, angle and looptime
	
													# Calculate VelocityRef based on position
		PiAngleRef=PID.PiVelocity(PiVelocityRef)													# Calculate AngleRef based on velocity
		PidMotorRef=PID.PidAngle(x_angle,PiAngleRef)											# Calculate MotorRef based on the angle	
	
		PC.drive(Sabertooth.addr, 1, int(PidMotorRef))											# Value sent to motors
		PC.drive(Sabertooth.addr, 2, int(PidMotorRef))
		
		