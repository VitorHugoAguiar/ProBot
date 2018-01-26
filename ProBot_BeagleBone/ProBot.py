#!/usr/bin/python

# Python Standard Library Imports
import sys
import os
import math
import decimal
import time
import datetime
import threading
import smbus
import memcache

# Local files
import SabertoothFile
import PIDControllersFile
import EncodersFile
import ProBotConstantsFile
import PWMFile
import WebPageFile
import RestartProgramFile
import MotorsControlFile
import StartFile
import mpu6050File

shared = memcache.Client([('localhost', 15)], debug=0)
shared.set('MainRoutinePID', str(os.getpid()))

# Initialization of classes from local files
InitProgram = StartFile.StartFileClass()
RestartProgram = RestartProgramFile.RestartProgramClass()
Sabertooth = SabertoothFile.SabertoothClass()
PID = PIDControllersFile.PIDControllersClass()
Encoders = EncodersFile.EncodersClass()
Pconst = ProBotConstantsFile.Constants()
PWM = PWMFile.PWMClass()
WebPage = WebPageFile.WebPageClass()
MotorsControlSignals = MotorsControlFile.MotorsControlClass()
InitParameters = InitProgram.StartProgram()
userChoice = InitParameters[0]
mpu6050=mpu6050File.mpu6050Class()


class ProBot():

    def __init__(self,  LoopTimeResult=0, wheelVelocity1=0, wheelVelocity2=0, EncodersTimeout=0.01, clearTimer=0, bus=smbus.SMBus(2)):
	self.LoopTimeResult=LoopTimeResult
	self.wheelVelocity1=wheelVelocity1
	self.wheelVelocity2=wheelVelocity2
	self.EncodersTimeout=EncodersTimeout    
	self.clearTimer=clearTimer
	self.bus=bus

    def EncodersTimer(self):
	if Encoders!=None:
		self.wheelVelocity1, self.wheelVelocity2  = Encoders.EncodersValues()	
		EncodersThread = threading.Timer(self.EncodersTimeout, ProBot.EncodersTimer)
		EncodersThread.daemon=True
     		EncodersThread.start()
		self.clearTimer=1


    def StartAndStopMainRoutine(self):
	try:
		StartAndStop = shared.get('StartAndStop')

		if StartAndStop =="1":
			shared.set('MainRoutineStatus', "started")
			ProBot.mainRoutine()

		shared.set('MainRoutineStatus', "stopped")

		print ("\nWaiting for the admin start")
    		while shared.get('MainRoutine')!='"start"':
			shared.get('MainRoutine')
			time.sleep(1)
		print("\nReceived the start from the admin")

		shared.set('StartAndStop', "1")
		ProBot.mainRoutine()

        except KeyboardInterrupt:
		    shared.set('MainRoutineStatus', "stopped")
                    InitProgram.StopProgram()
                    print("Unexpected error:\n", sys.exc_info()[0])
                    sys.exit('\n\nPROGRAM STOPPED!!!\n')
                    raise

    def mainRoutine(self):
	try:

		# Calibration of MPU6050
		mpu6050.Calibration()
        	time.sleep(2)
		EncodersThread = threading.Timer(self.EncodersTimeout, ProBot.EncodersTimer)
		EncodersThread.daemon=True
		EncodersThread.start()

		while True:
		    try:
		    	LoopTimeStart=time.time()

                        if shared.get('MainRoutine') =='"stop"':
				shared.set('StartAndStop', "0")
				shared.set('MainRoutineStatus', "stopped")
				RestartProgram.RestartProgramRoutine()

		    	# Reading the values from the webpage
                    	VelocityRef, TurnMotorRight, TurnMotorLeft = WebPage.WebPage_Values()
						
			# Reading the MPU6050 values and use the complementary filter to get better values
		    	ComplementaryAngle=mpu6050.Complementary_filter(self.LoopTimeResult)

			# Checking if the angle is out of range
		    	if ComplementaryAngle<-20 or ComplementaryAngle>20:
				RestartProgram.RestartProgramRoutine()
				
			# With the values from the WebPage, we can calculate the outputs from the controllers
               	    	TargetAngle1 = PID.standardPID((VelocityRef+TurnMotorRight), self.wheelVelocity1, 'Velocity1', userChoice)
                    	TargetAngle2 = PID.standardPID((VelocityRef+TurnMotorLeft), self.wheelVelocity2, 'Velocity2', userChoice)
						
		    	rightMotor = PID.standardPID(TargetAngle1, ComplementaryAngle, 'Angle1', userChoice)
                    	leftMotor = PID.standardPID(TargetAngle2, ComplementaryAngle, 'Angle2', userChoice)
			
 		    	# Sending the right values to the Sabertooth or the PWM controller
	            	MotorsControlSignals.MotorsControl(rightMotor, leftMotor, userChoice)

		    	LoopTimeEnd=time.time()
	            	self.LoopTimeResult=LoopTimeEnd-LoopTimeStart
			
		    except IOError, err:
			print(IOError, err)
			self.bus.write_byte_data(0x68, 0x1A, 0x80)
			self.bus.write_byte_data(0x68, 0x6B, 0x00)
			self.bus.write_byte_data(0x68,0xA5,0x5A)
                    	continue

	except KeyboardInterrupt:
		    if self.clearTimer==1:
		    	if EncodersThread.isAlive():
				EncodersThread.cancel()
                    		EncodersThread.join(0)

		    shared.set('MainRoutineStatus', "stopped")
		    shared.set('MainRoutine', "stopped")

		    InitProgram.StopProgram()

		    print("Unexpected error:\n", sys.exc_info()[0])
		    sys.exit('\n\nPROGRAM STOPPED!!!\n')
		    raise

    def main(self):
	if userChoice=='1':
        	Sabertooth.CommunicationStart()
	if userChoice=='2':
		PWM.PWMStart()

	ProBot.StartAndStopMainRoutine()

if __name__ == '__main__':
    ProBot = ProBot()
    ProBot.main()

