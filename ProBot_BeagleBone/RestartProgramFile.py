#!/usr/bin/python

# Python Standart Library Imports
import Adafruit_BBIO.GPIO as GPIO
import sys
import os

# Local files
import ProBotConstantsFile
import SabertoothFile
import PWMFile

# Initialization of classes from local files
PWM = PWMFile.PWMClass()
Pconst = ProBotConstantsFile.Constants()
Sabertooth = SabertoothFile.SabertoothClass()

# Configuration the type of GPIO's
GPIO.setup(Pconst.RedLED, GPIO.OUT)

class RestartProgramClass():

    def RestartProgramRoutine(self):
	# Routine called when the angle is out of range or the admin stopped the mainRoutine and we need to restart the program
	Sabertooth.stopAndReset()
	PWM.PWMStop()
	
	GPIO.output(Pconst.GreenLED, GPIO.LOW)

	print "\nProBot angle's out of range or the admin stopped the mainRoutine!!!"
	print "\nRestarting the Program..."

   	python = sys.executable
    	os.execl(python, python, * sys.argv)
 
