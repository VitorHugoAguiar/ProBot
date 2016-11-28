#!/usr/bin/python

# Python Standart Library Imports
import Adafruit_BBIO.GPIO as GPIO
import sys
import os
import ProBotConstantsFile
import SabertoothFile
import mpu6050File
import PWMFile

PWM = PWMFile.PWMClass()
mpu6050 = mpu6050File.mpu6050Class()
Pconst = ProBotConstantsFile.Constants()
Sabertooth = SabertoothFile.SabertoothClass()

class RestartProgramClass():

    def RestartProgramRoutine(self, userChoice):
    	# Routine called when the angle is out of range and we need to restart the program
	Sabertooth.stopAndReset()
	PWM.PWMStop()
	
	GPIO.output(Pconst.GreenLED, GPIO.LOW)
	GPIO.output(Pconst.RedLED, GPIO.LOW)
	GPIO.output(Pconst.BlueLED, GPIO.HIGH)

	print "\nProBot angle's out of range!!!"
	print "\nPut ProBot at 90 degrees!!!"
	
	filteredX=mpu6050.Complementary_filter(0)
	
	while filteredX<-0.2 or filteredX>0.2:
		filteredX=mpu6050.Complementary_filter(0)

	GPIO.output(Pconst.BlueLED, GPIO.LOW)	
	print "\nRestarting the Program..."
      	
	userChoiceFile = open("userChoice.txt", "wb")
	userChoiceFile.write( userChoice);
	userChoiceFile.close()

   	python = sys.executable
    	os.execl(python, python, * sys.argv)
    	


