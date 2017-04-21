#!/usr/bin/python

# Python Standard Library Imports
import sys
import os
import math
import decimal
import time
import datetime
import threading

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
import SocketStartAndStop2

pidf = open("/home/machinekit/ProBot/ProBot_BeagleBone/pidProBot.tmp","w")
pidf.write(str(os.getpid()))
pidf.close()

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
Pub_Sub2 = SocketStartAndStop2.SocketClass()

class ProBot():
   
    def __init__(self,  LoopTimeResult=0, wheelVelocity1=0, wheelVelocity2=0, EncodersTimeout=0.01):
	self.LoopTimeResult=LoopTimeResult
	self.wheelVelocity1=wheelVelocity1
	self.wheelVelocity2=wheelVelocity2
	self.EncodersTimeout=EncodersTimeout    
	
    def EncodersTimer(self):
	if Encoders==None:
		pass
	else:
		self.wheelVelocity1, self.wheelVelocity2  = Encoders.EncodersValues()	
		EncodersThread = threading.Timer(self.EncodersTimeout, ProBot.EncodersTimer)
		EncodersThread.daemon=True
     		EncodersThread.start()
	
    def mainRoutine(self):
	try:

		# Calibration of MPU6050
		mpu6050.Calibration()
        	time.sleep(1)

		EncodersThread = threading.Timer(self.EncodersTimeout, ProBot.EncodersTimer)
		EncodersThread.daemon=True
		EncodersThread.start()
		
		while True:
		    try:
		    	LoopTimeStart=time.time()             
                        subscriber2 = Pub_Sub2.subscriber() # Readings from the WebPage
                        if subscriber2=="stop":
                                raise KeyboardInterrupt()

		    	# Reading the values from the webpage
                    	VelocityRef, TurnMotorRight, TurnMotorLeft = WebPage.WebPage_Values()
				   		
			# Reading the MPU6050 values and use the complementary filter to get better values 
		    	ComplementaryAngle=mpu6050.Complementary_filter(self.LoopTimeResult)
   
		    	# Checking if the angle is out of range
		    	if ComplementaryAngle<-20 or ComplementaryAngle>20:
				RestartProgram.RestartProgramRoutine(userChoice)
						     		  	    
		    	# With the values from the WebPage, we can calculate the outputs from the controllers
               	    	VelocityController1 = PID.standardPID((VelocityRef+TurnMotorRight), self.wheelVelocity1, 'Velocity1', userChoice)
                    	VelocityController2 = PID.standardPID((VelocityRef+TurnMotorLeft), self.wheelVelocity2, 'Velocity2', userChoice)
					                    
		    	rightMotor = PID.standardPID(round (VelocityController1, 2), ComplementaryAngle, 'Angle1', userChoice)
                    	leftMotor = PID.standardPID(round (VelocityController2, 2), ComplementaryAngle, 'Angle2', userChoice)

 		    	# Sending the right values to the Sabertooth or the PWM controller
	            	MotorsControlSignals.MotorsControl(rightMotor, leftMotor, userChoice)

		    	LoopTimeEnd=time.time()
	            	self.LoopTimeResult=LoopTimeEnd-LoopTimeStart				

		    except IOError, err:
			print(IOError, err)
                    	continue

	except KeyboardInterrupt:
		    if not EncodersThread.isAlive():
			EncodersThread.cancel()
                    	EncodersThread.join(0)
		    
		    InitProgram.StopProgram()
		    print("Unexpected error:\n", sys.exc_info()[0])
		    sys.exit('\n\nPROGRAM STOPPED!!!\n')
		    raise


    def main(self):
	if userChoice=='1':
        	Sabertooth.CommunicationStart()
	if userChoice=='2':
		PWM.PWMStart()
        ProBot.mainRoutine()

if __name__ == '__main__':
    ProBot = ProBot()
    ProBot.main()

