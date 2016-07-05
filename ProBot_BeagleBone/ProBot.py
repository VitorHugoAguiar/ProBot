#!/usr/bin/python

# Python Standard Library Imports
import Adafruit_I2C as Adafruit_I2C
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import threading
import sys
import os
import math
import decimal
import time
import datetime
import zmq
import BatteryMonitor
import Controllers
import Encoders
import SocketCommunication
import ProBotConstants
import LowPassFilter
from math import atan, atan2, sqrt,pi
from MPU6050 import MPU6050
import Sabertooth

# We create a file to store the userChoice (Sabertooth or PWM)
userChoiceFile = open("userChoice.txt", "r+")
userChoice = userChoiceFile.read(1);
# Close opend file
userChoiceFile.close()

if userChoice=='0':
	print ('\nChoose the type of control of the ProBots motors:')
	print ('\n1 - Sabertooth 2x25')
	print ('2 - PWM Controller OSMC3-2')
	userChoice=input('\nYour choice is: ')
	userChoice=str(userChoice)

	userChoiceFile = open("userChoice.txt", "wb")
	userChoiceFile.write(userChoice);
	userChoiceFile.close()


# Initialization of classes from local files
PC = Sabertooth.PacketizedCommunication()
Battery = BatteryMonitor.BatteryVoltage()
PID = Controllers.PIDControllers()
Enc = Encoders.EncodersReadings()
Pconst = ProBotConstants.Constants()
LPF=LowPassFilter.LowPassFilter()
Pub_Sub = SocketCommunication.publisher_and_subscriber()


#PWM.start(channel, duty, freq, polarity)
PWM.start(Pconst.PWM_RF, 0, Pconst.PWM_Freq, 0)
PWM.start(Pconst.PWM_RR, 0, Pconst.PWM_Freq, 0)
PWM.start(Pconst.PWM_LF, 0, Pconst.PWM_Freq, 0)
PWM.start(Pconst.PWM_LR, 0, Pconst.PWM_Freq, 0)


# Configuration the type of GPIO's
GPIO.setup(Pconst.RedLED, GPIO.OUT)
GPIO.setup(Pconst.GreenLED, GPIO.OUT)
GPIO.setup(Pconst.BlueLED, GPIO.OUT)

if userChoice=='1':
	print "\nSending commands to the address", Pconst.addr, "with a baudrate of\n", Pconst.baud

if userChoice=='2':
	print "\nSending a PWM signal with a frequency of", Pconst.PWM_Freq, "Hz"

class ProBot():
    def __init__(self, wheelPositionRef=0, PositionRef=0, TurnMotorRight=0, TurnMotorLeft=0, lastAccelerometerAngleX=0, LoopTimeRatioSeg=0, sensor=0, filteredX=0, down=0, up=0, left=0, right=0):
	self.wheelPositionRef = wheelPositionRef
        self.PositionRef = PositionRef
        self.TurnMotorRight = TurnMotorRight
        self.TurnMotorLeft = TurnMotorLeft
	self.lastAccelerometerAngleX=lastAccelerometerAngleX
	self.LoopTimeRatioSeg=LoopTimeRatioSeg
	self.sensor=MPU6050(0x68)
	self.filteredX=filteredX
	self.up=up
	self.down=down
	self.left=left
	self.right=right

    def Calibration_MPU6050(self):
    	# Calibration of the MPU6050, on the begginer of the program
	ProBot.MPU6050Readings()
	while self.filteredX<-0.2 or self.filteredX>0.2:
		ProBot.MPU6050Readings()

    def MPU6050Readings(self):
    	# Readings from the MPU6050
        accel_data = self.sensor.get_accel_data()
    	gyro_data = self.sensor.get_gyro_data()
  
 	AccXangle = ((atan2(accel_data['y'],accel_data['z'])+pi)*Pconst.rad_to_deg)-180
	
	# Complementary filter
    	self.filteredX = float(0.98 * (self.lastAccelerometerAngleX+self.LoopTimeRatioSeg*gyro_data['x']) + (1 - 0.98) * AccXangle)
    	self.lastAccelerometerAngleX=self.filteredX
	self.filteredX=self.filteredX+Pconst.Angle_offset				# Angle offset
	return self.filteredX

    def SabertoothCommunication_initialization(self):
    	# Starting the communication with Sabertooth
        GPIO.output(Pconst.RedLED, GPIO.HIGH)
        PC.set_baud(Pconst.addr, Pconst.baud)
        time.sleep(3)									# Wait to stabilize the communication

        PC.stopAndReset()

	GPIO.output(Pconst.RedLED, GPIO.LOW)
	GPIO.output(Pconst.BlueLED, GPIO.HIGH)


    def PWM_initialization(self):
    	# Starting the communication with the PWM controller
        GPIO.output(Pconst.RedLED, GPIO.HIGH)

        time.sleep(3)									# Wait to stabilize the communication

	GPIO.output(Pconst.RedLED, GPIO.LOW)
	GPIO.output(Pconst.BlueLED, GPIO.HIGH)

    def WebPage(self):
    	# Readings from the WebPage
        subscriber = Pub_Sub.subscriber()

        if subscriber is None:
            subscriber = 0

        else:
	    incomingMsg = subscriber.split(" ")

	    if incomingMsg[0]=="web":
		self.up = incomingMsg[1]
		self.down = incomingMsg[2]
		self.left = incomingMsg[3]
		self.right = incomingMsg[4]
		# print incomingMsg[0], self.up, self.down, self.left, self.right

	    Forward = float(decimal.Decimal(self.up))
	    Reverse = -float(decimal.Decimal(self.down))
	    Left = float(decimal.Decimal(self.left))
	    Right = -float(decimal.Decimal(self.right))

	    ForwardReverse=Forward+Reverse
	    LeftRight=Left+Right

	    ForwardReverse=LPF.lowPassFilterFR(ForwardReverse)
	    LeftRight=LPF.lowPassFilterLR(LeftRight)
	    self.PositionRef = -float(ForwardReverse*Pconst.ajustFR)
	    self.TurnMotorRight = float(LeftRight*Pconst.ajustLR)
	    self.TurnMotorLeft = -float(LeftRight*Pconst.ajustLR)
	    #print self.PositionRef, self.TurnMotorRight, selfTurnMotorLeft
	    return  self.PositionRef,  self.TurnMotorRight, self.TurnMotorLeft

    def MsgServer (self, interval, worker_func, iterations = 0):
      if iterations != 1:
        threading.Timer (interval, ProBot.MsgServer, [interval, worker_func, 0 if iterations == 0 else iterations-1]).start ()

      worker_func ()

    def sendMsgServer (self):
     	# Verification of the voltage from the Beaglebone and motors batteries
	t = threading.Timer(1, ProBot.sendMsgServer)
	t.start() 
	batteryValue=str('{0:.2f}'.format(Battery.VoltageValue('LiPo')))
	info="ProBot2_info" + " " + batteryValue
        publisher=Pub_Sub.publisher(info)
	#print info


    def RestartProgram(self):
    	# Routine called when the angle is out of range and we need to restart the program
	PC.stopAndReset()
	
	GPIO.output(Pconst.GreenLED, GPIO.LOW)
	GPIO.output(Pconst.RedLED, GPIO.LOW)
	GPIO.output(Pconst.BlueLED, GPIO.HIGH)

	print "\nProBot angle's out of range!!!"
	print "\nPut ProBot at 90 degrees!!!"
	
	while self.filteredX<-0.2 or self.filteredX>0.2:
		ProBot.MPU6050Readings()

	GPIO.output(Pconst.BlueLED, GPIO.LOW)	
	print "\nRestarting the Program..."
      	
	userChoiceFile = open("userChoice.txt", "wb")
	userChoiceFile.write( userChoice);
	userChoiceFile.close()

   	python = sys.executable
    	os.execl(python, python, * sys.argv)

    def motorsControl(self, rightMotor, leftMotor):
	if userChoice=='1':
		# Sending the values to the Sabertooth that is connected to the motors
		PC.drive(Pconst.addr, 1, int(rightMotor))
	        PC.drive(Pconst.addr, 2, int(leftMotor))

	if userChoice=='2':
		# Sending the values to the PWM controller that is connected to the motors
		percentageR=math.fabs(rightMotor)
		percentageL=math.fabs(leftMotor)

		if rightMotor>0:
			PWM.set_duty_cycle(Pconst.PWM_RF, 0)
			PWM.set_duty_cycle(Pconst.PWM_RR, percentageR)
		elif rightMotor<0:
			PWM.set_duty_cycle(Pconst.PWM_RF, percentageR)
			PWM.set_duty_cycle(Pconst.PWM_RR, 0)
		elif rightMotor==0:
			PWM.set_duty_cycle(Pconst.PWM_RF, 0)
			PWM.set_duty_cycle(Pconst.PWM_RR, 0)

		if leftMotor>0:
			PWM.set_duty_cycle(Pconst.PWM_LF, 0)
			PWM.set_duty_cycle(Pconst.PWM_LR, percentageL)
		elif leftMotor<0:
			PWM.set_duty_cycle(Pconst.PWM_LF, percentageL)
			PWM.set_duty_cycle(Pconst.PWM_LR, 0)
		elif leftMotor==0:
			PWM.set_duty_cycle(Pconst.PWM_LF, 0)
			PWM.set_duty_cycle(Pconst.PWM_LR, 0)

    def mainRoutine(self):

    	# Starting the main program
	ProBot.Calibration_MPU6050()
	GPIO.output(Pconst.BlueLED, GPIO.LOW)
	GPIO.output(Pconst.GreenLED, GPIO.HIGH)
	ProBot.sendMsgServer()
	#ProBot.MsgServer (0.1, ProBot.sendMsgServer)
	

	time.sleep(0.5)


        while True:
            try:
		LoopTime=datetime.datetime.now()

		# Reading the MPU6050 values
		ProBot.MPU6050Readings()

		# Readings from the encoders
                Encoders = Enc.EncodersValues()
		wheelPosition1  = Encoders [0]               
		wheelPosition2 = Encoders[1]
		
		# Checking if the angle is out of range
		if self.filteredX<-20 or self.filteredX>20:
			ProBot.RestartProgram()
		
		# Reading the values from the midi device and the webpage
                WebPage = ProBot.WebPage()

                # With the values from the midi devices or WebPage, we can calculate the outputs from the controllers
                PositionController1 = PID.standardPID((self.PositionRef+self.TurnMotorRight), wheelPosition1, 'Position1', userChoice)
                PositionController2 = PID.standardPID((self.PositionRef+self.TurnMotorLeft), wheelPosition2, 'Position2', userChoice)
                
		rightMotor = PID.standardPID(PositionController1, self.filteredX, 'Angle1', userChoice)
                leftMotor = PID.standardPID(PositionController2, self.filteredX, 'Angle2', userChoice)
 
		ProBot.motorsControl(rightMotor, leftMotor)

		LoopTime2 = datetime.datetime.now()
		LoopTimeRatio=LoopTime2-LoopTime
		self.LoopTimeRatioSeg=(LoopTimeRatio.microseconds*0.001)/1000

	    except OSError as err:
    		print("OS error: {0}".format(err))
	    except ValueError:
    		print("Could not convert data to an integer.")			
            except:

		info="ProBot2_info" + " " + "off"
        	publisher=Pub_Sub.publisher(info)

		if 'threading' in sys.modules:
    		    del sys.modules['threading']

                PC.stopAndReset()
		PWM.stop(Pconst.PWM_RF)
		PWM.stop(Pconst.PWM_RR)
		PWM.stop(Pconst.PWM_LF)
		PWM.stop(Pconst.PWM_LR)
		PWM.cleanup()

		userChoiceFile = open("userChoice.txt", "wb")
		userChoiceFile.write("0");
		userChoiceFile.close()

 		print("Unexpected error:\n", sys.exc_info()[0])
		sys.exit('\n\nPROGRAM STOPPED!!!\n')
                raise



    def main(self):
	if userChoice=='1':
        	ProBot.SabertoothCommunication_initialization()
	if userChoice=='2':
		ProBot.PWM_initialization()
        ProBot.mainRoutine()

if __name__ == '__main__':
    ProBot = ProBot()
    ProBot.main()
