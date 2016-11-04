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
import MPU6050File
import BatteryMonitorFile

# Initialization of classes from local files
InitProgram=StartFile.StartFileClass()
RestartProgram=RestartProgramFile.RestartProgramClass()
Sabertooth = SabertoothFile.SabertoothClass()
PID = PIDControllersFile.PIDControllersClass()
Encoders = EncodersFile.EncodersClass()
Pconst = ProBotConstantsFile.Constants()
MPU6050 = MPU6050File.MPU6050(0x68)
PWM = PWMFile.PWMClass()
WebPage = WebPageFile.WebPageClass()
MotorsControlSignals=MotorsControlFile.MotorsControlClass()
Battery = BatteryMonitorFile.BatteryMonitorClass()

InitParameters=InitProgram.StartProgram()
userChoice=InitParameters[0]


class ProBot():
    def __init__(self,  LoopTimeRatioSeg=0):
	self.LoopTimeRatioSeg=LoopTimeRatioSeg


    def mainRoutine(self):
    	# Starting the main program
	MPU6050.Calibration_MPU6050()
	time.sleep(0.5)

        while True:
            try:
		LoopTime=datetime.datetime.now()
		Battery.VoltageValue('LiPo')
		# Reading the MPU6050 values and use the complementary filter to get better values
		MPU6050.Complementary_filter(self.LoopTimeRatioSeg)

		# Readings from the encoders
                EncodersReadings = Encoders.EncodersValues()
		wheelPosition1  = EncodersReadings [0]               
		wheelPosition2 = EncodersReadings [1]
		#print MPU6050.filteredX
		# Checking if the angle is out of range
		if MPU6050.filteredX<-20 or MPU6050.filteredX>20:
			RestartProgram.RestartProgramRoutine(userChoice)
		
		# Reading the values from the webpage
                WebPage_info = WebPage.WebPage_Values()
                PositionRef = WebPage_info [0]
                TurnMotorRight = WebPage_info [1]
                TurnMotorLeft = WebPage_info [2]
		
                # With the values from the WebPage, we can calculate the outputs from the controllers
                PositionController1 = PID.standardPID((PositionRef+TurnMotorRight), wheelPosition1, 'Position1', userChoice)
                PositionController2 = PID.standardPID((PositionRef+TurnMotorLeft), wheelPosition2, 'Position2', userChoice)
                
		rightMotor = PID.standardPID(PositionController1, MPU6050.filteredX, 'Angle1', userChoice)
                leftMotor = PID.standardPID(PositionController2, MPU6050.filteredX, 'Angle2', userChoice)
 		
 		# Sending the right values to the Sabertooth or the PWM controller
		MotorsControlSignals.MotorsControl(rightMotor, leftMotor, userChoice)

		LoopTime2 = datetime.datetime.now()
		LoopTimeRatio=LoopTime2-LoopTime
		self.LoopTimeRatioSeg=(LoopTimeRatio.microseconds*0.001)/1000

	    except OSError as err:
    		print("OS error: {0}".format(err))
	    except ValueError:
    		print("Could not convert data to an integer.")			
            except:
		
		InitProgram.StopProgram(1)

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
