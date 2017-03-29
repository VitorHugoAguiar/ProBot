#!/usr/bin/python

# Python Standard Library Imports
import sys
import os
import math
import decimal
import time
import datetime

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

# Initialization of classes from local files
Sabertooth = SabertoothFile.SabertoothClass()
PID = PIDControllersFile.PIDControllersClass()
Encoders = EncodersFile.EncodersClass()
Pconst = ProBotConstantsFile.Constants()
PWM = PWMFile.PWMClass()
WebPage = WebPageFile.WebPageClass()
RestartProgram = RestartProgramFile.RestartProgramClass()
MotorsControlSignals = MotorsControlFile.MotorsControlClass()
InitProgram = StartFile.StartFileClass()
mpu6050=mpu6050File.mpu6050Class()

InitParameters = InitProgram.StartProgram()
userChoice = InitParameters[0]


class ProBot():
   
    def __init__(self,  LoopTimeResult=0):
	self.LoopTimeResult=LoopTimeResult
	

    def mainRoutine(self):
	try:
		# Calibration of MPU6050
		mpu6050.Calibration()
        	time.sleep(1)
		while True:
		    try:
		    	LoopTimeStart=time.time()
		
		    	# Readings from the encoders
		    	wheelPosition1, wheelPosition2  = Encoders.EncodersValues()               
		    		
		    	# Reading the values from the webpage
                    	PositionRef, TurnMotorRight, TurnMotorLeft = WebPage.WebPage_Values()
		
		   	# Reading the MPU6050 values and use the complementary filter to get better values 
		    	ComplementaryAngle=mpu6050.Complementary_filter(self.LoopTimeResult)
   
		    	# Checking if the angle is out of range
		    	if ComplementaryAngle<-20 or ComplementaryAngle>20:
				RestartProgram.RestartProgramRoutine(userChoice)
						     		  	    
		    	# With the values from the WebPage, we can calculate the outputs from the controllers
               	    	PositionController1 = PID.standardPID((PositionRef+TurnMotorRight), wheelPosition1, 'Position1', userChoice)
                    	PositionController2 = PID.standardPID((PositionRef+TurnMotorLeft), wheelPosition2, 'Position2', userChoice)
					                    
		    	rightMotor = PID.standardPID(round (PositionController1, 2), ComplementaryAngle, 'Angle1', userChoice)
                    	leftMotor = PID.standardPID(round (PositionController2, 2), ComplementaryAngle, 'Angle2', userChoice)

 		    	# Sending the right values to the Sabertooth or the PWM controller
	            	MotorsControlSignals.MotorsControl(rightMotor, leftMotor, userChoice)

		    	LoopTimeEnd=time.time()
	            	self.LoopTimeResult=LoopTimeEnd-LoopTimeStart
		
		
		    except IOError, err:
			print(IOError, err)
                    	continue

	except KeyboardInterrupt:
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

