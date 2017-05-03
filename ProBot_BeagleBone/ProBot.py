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
import SocketStartAndStop
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
Pub_SubStart=SocketStartAndStop.SocketClass()
Pub_SubStart2=SocketStartAndStop2.SocketClass()


class ProBot():
   
    def __init__(self,  LoopTimeResult=0, wheelVelocity1=0, wheelVelocity2=0, EncodersTimeout=0.01, clearTimer=0):
	self.LoopTimeResult=LoopTimeResult
	self.wheelVelocity1=wheelVelocity1
	self.wheelVelocity2=wheelVelocity2
	self.EncodersTimeout=EncodersTimeout    
	self.clearTimer=clearTimer

    def EncodersTimer(self):
	if Encoders!=None:
		self.wheelVelocity1, self.wheelVelocity2  = Encoders.EncodersValues()	
		EncodersThread = threading.Timer(self.EncodersTimeout, ProBot.EncodersTimer)
		EncodersThread.daemon=True
     		EncodersThread.start()
		self.clearTimer=1
	
    def StartAndStopMainRoutine(self):
	try:
        	# We create a file to store the userChoice (Sabertooth or PWM)
        	StartAndStopFile = open("/home/machinekit/ProBot/ProBot_BeagleBone/StartAndStop.txt", "r+")
        	StartAndStop = StartAndStopFile.read(1);
        	# Close opend file
        	StartAndStopFile.close()

		if StartAndStop !="0":
			Pub_SubStart2.publisher("start")
                	StartAndStopFile = open("StartAndStop.txt", "wb")
                	StartAndStopFile.write("1");
                	StartAndStopFile.close()
			ProBot.mainRoutine()

       		Pub_SubStart2.publisher("stopped")

		print ("\nWaiting for the admin start")
    		while Pub_SubStart.subscriber()!="start":
			Pub_SubStart.subscriber()    	
			time.sleep(1)
		print("\nReceiced the start from the admin")

		Pub_SubStart2.publisher("start")
		StartAndStopFile = open("StartAndStop.txt", "wb")
        	StartAndStopFile.write("1");
       		StartAndStopFile.close()
	
		ProBot.mainRoutine()
		
        except KeyboardInterrupt:
		    Pub_SubStart2.publisher("stopped")
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
			#msg = Pub_SubStart.subscriber()

                        if Pub_SubStart.subscriber() == "stop":
				StartAndStopFile = open("StartAndStop.txt", "wb")
        			StartAndStopFile.write("0");
        			StartAndStopFile.close()
				RestartProgram.RestartProgramRoutine()
                        

		    	# Reading the values from the webpage
                    	VelocityRef, TurnMotorRight, TurnMotorLeft = WebPage.WebPage_Values()
				   		
			# Reading the MPU6050 values and use the complementary filter to get better values 
		    	ComplementaryAngle=mpu6050.Complementary_filter(self.LoopTimeResult)
   
		    	# Checking if the angle is out of range
		    	if ComplementaryAngle<-20 or ComplementaryAngle>20:
				RestartProgram.RestartProgramRoutine()
						     		  	    
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
		    if self.clearTimer==1:
		    	if EncodersThread.isAlive():
				EncodersThread.cancel()
                    		EncodersThread.join(0)
			
		    Pub_SubStart2.publisher("stopped")
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

