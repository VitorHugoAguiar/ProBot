#!/usr/bin/python

# Python Standart Library Imports
import Adafruit_BBIO.GPIO as GPIO
import sys
import os
import ProBotConstantsFile
import SabertoothFile
import PWMFile
import math
#from MPU6050 import MPU6050
import mpu6050File

#sensor=MPU6050(0x68)
PWM = PWMFile.PWMClass()
Pconst = ProBotConstantsFile.Constants()
Sabertooth = SabertoothFile.SabertoothClass()
mpu6050=mpu6050File.mpu6050Class()

class RestartProgramClass():

    def RestartProgramRoutine(self, userChoice):
    	try:
		import StartFile
		# Routine called when the angle is out of range and we need to restart the program
		Sabertooth.stopAndReset()
		PWM.PWMStop()
	
		GPIO.output(Pconst.GreenLED, GPIO.LOW)
		GPIO.output(Pconst.RedLED, GPIO.LOW)
		GPIO.output(Pconst.BlueLED, GPIO.HIGH)

		print "\nProBot angle's out of range!!!"
		print "\nPut ProBot at 90 degrees!!!"
        	
		#while (True):
		mpu6050.Calibration()		
			#Acc_Data = sensor.set_accel_range(0x18)
               		#sensor.set_gyro_range(0x18)
		        #if Acc_Data>-0.5 or Acc_Data<0.5:
			#	break
		       	
			# Calibration of mpu6050
               		#sensor.Calibration()
                	#break


		
		GPIO.output(Pconst.BlueLED, GPIO.LOW)	
		print "\nRestarting the Program..."
      	
		userChoiceFile = open("userChoice.txt", "wb")
		userChoiceFile.write( userChoice);
		userChoiceFile.close()

   		python = sys.executable
    		os.execl(python, python, * sys.argv)
    	
	except:
		InitProgram.StopProgram()
                print("Unexpected error:\n", sys.exc_info()[0])
                sys.exit('\n\nPROGRAM STOPPED!!!\n')
                raise

