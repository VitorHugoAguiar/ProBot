#!/usr/bin/python

# Python Standard Library Imports
import Adafruit_BBIO.UART as UART
import Adafruit_I2C as Adafruit_I2C
import Adafruit_BBIO.GPIO as GPIO
import sys
import math
import decimal
import time
import zmq
import mpu6050
import Sabertooth
import Kalman
import BatteryMonitor
import Controllers
import Encoders
import SocketCommunication
import ProBotConstants

# Start the UART1
UART.setup("UART1")

# Configuration of the GPIO's
RedLED = "P8_13"
GreenLED = "P9_27"
# Configuration the type of GPIO's
GPIO.setup(RedLED, GPIO.OUT)
GPIO.setup(GreenLED, GPIO.OUT)
 
#Initialization of classes from local files
mpu = mpu6050.MPU6050()
PC = Sabertooth.PacketizedCommunication()
KF = Kalman.KalmanFilter()
Battery = BatteryMonitor.BatteryVoltage()
PID = Controllers.PIDControllers()
Enc=Encoders.EncodersReadings()
Pub_Sub=SocketCommunication.publisher_and_subscriber()
Pconst=ProBotConstants.Constants()

class ProBot():
	def __init__(self, wheelPositionRef=0, VelocityRef=0,TurnMotorRight=0,TurnMotorLeft=0, forward=0, reverse=0, left=0 , right=0):
		#Starting the main program
		self.wheelPositionRef=wheelPositionRef
		self.VelocityRef=VelocityRef
		self.TurnMotorRight=TurnMotorRight
		self.TurnMotorLeft=TurnMotorLeft
		self.forward=forward
		self.reverse=reverse
		self.left=left
		self.right=right

	
	def MPU6050_initialization (self):
		# MPU6050 initialization
		mpu.initialize()
		#Testing connection 
		if mpu.testConnection() is False:
			GPIO.output(RedLED, GPIO.HIGH)
			GPIO.output(GreenLED, GPIO.LOW)  
		else:
			GPIO.output(RedLED, GPIO.LOW)
			GPIO.output(GreenLED, GPIO.HIGH)
 
	def Communication_initialization(self):
		GPIO.output(RedLED, GPIO.HIGH)
		PC.set_baud(PC.addr,PC.baud)
		time.sleep(3)									# Wait to stabilize the communication
																			
		PC.stopAndReset()

		GPIO.output(GreenLED, GPIO.HIGH)
		GPIO.output(RedLED, GPIO.LOW)
		time.sleep(1.5)

	def Joystick(self):
		subscriber=Pub_Sub.subscriber()
		if subscriber is None:
			subscriber=0
			
		else:	
			self.forward, self.reverse, self.left, self.right = subscriber.split()
			
		forwardDecimal = float(decimal.Decimal(self.forward))
		reverseDecimal = float(decimal.Decimal(self.reverse))
		rightDecimal = float(decimal.Decimal(self.right))
		leftDecimal = float(decimal.Decimal(self.left))
		
		if forwardDecimal>0:
			VelocityRef=float(forwardDecimal*1.3)
		else:
			VelocityRef=-float(reverseDecimal*1.3)
				
		if forwardDecimal == 0 and reverseDecimal==0:
			VelocityRef=0
				
		
		if rightDecimal>0:
			TurnMotorRight=float(rightDecimal*40)
			TurnMotorLeft=-float(rightDecimal*40)
		else:
			TurnMotorRight=-float(leftDecimal*40)
			TurnMotorLeft=float(leftDecimal*40)

		if rightDecimal==0 and leftDecimal==0:
			TurnMotorRight=0
			TurnMotorLeft=0
			
		return VelocityRef, TurnMotorRight, TurnMotorLeft
					
	
	def mainRoutine(self):
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
				ax_raw = AccXangle - Pconst.AccXangleAverage		
				GYRx_raw = GYRx - Pconst.GYRxAverage
				# After the readings, we use the Kalman filter to eliminate the variations from the readings		
				kalAngleX = KF.KalmanCalculate(ax_raw,GYRx_raw, LoopTime)
			
				# Readings from the encoders
				Encoders=Enc.EncodersValues()
				wheelVelocity=Encoders[0]
				wheelPosition=Encoders[1]
			
				Joystick=ProBot.Joystick()
				VelocityRef=Joystick[0]
				TurnMotorRight=Joystick[1]
				TurnMotorLeft=Joystick[2]
			
				# With the values from the server, we can calculate the outputs from the controllers			
				PidVelocityRef= PID.standardPID(self.wheelPositionRef,wheelPosition, 0)			
				PidAngleRef= PID.standardPID(VelocityRef,wheelVelocity, 1)
				PidMotorRef = PID.standardPID(PidAngleRef,kalAngleX, 2)
			
				rightMotor=float(PidMotorRef+TurnMotorRight)
				leftMotor=float(PidMotorRef+TurnMotorLeft)
		
				# Sending the values to the Sabertooth that is connected to the motors	
				PC.drive(PC.addr, 1, int(rightMotor))								
				PC.drive(PC.addr, 2, int(leftMotor))
			except:
				PC.stopAndReset()
				sys.exit('\n\nPROGRAM STOPPED!!!\n')
				raise
		
	def main(self):
		ProBot.MPU6050_initialization()
		ProBot.Communication_initialization()
		ProBot.mainRoutine()

if __name__ == '__main__':
	ProBot=ProBot()
	ProBot.main()


		
