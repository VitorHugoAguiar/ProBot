#!/usr/bin/python

# Python Standard Library Imports
import math
import ProBotConstantsFile
import decimal
import time

# Initialization of classes from local files
Pconst = ProBotConstantsFile.Constants()

# PID functions
class PIDControllersClass():
    # Build a constructor
    def __init__(self, error=0):
        self.error = error
	
    def standardPID(self, reference, measured, type, userChoice):
        self.error = float(reference - measured)
	
	# Load the right values for the controllers,  depending on if we are using Sabertooth of PWM controller
	if userChoice=='1':	
		KpP=Pconst.SaberTooth_KpP
		KiP=Pconst.SaberTooth_KiP
		KdP=Pconst.SaberTooth_KdP
		KpA=Pconst.SaberTooth_KpA
		KiA=Pconst.SaberTooth_KiA
		KdA=Pconst.SaberTooth_KdA

	if userChoice=='2':
		KpP=Pconst.PWM_KpP
		KiP=Pconst.PWM_KiP
		KdP=Pconst.PWM_KdP
		KpA=Pconst.PWM_KpA
		KiA=Pconst.PWM_KiA
		KdA=Pconst.PWM_KdA

	# Loading the variables for the controllers
        typeController = { 
	  'Position1': [KpP, KiP, KdP, Pconst.limitP, Pconst.integrated_error_P1, Pconst.last_error_P1],
          'Position2': [KpP, KiP, KdP, Pconst.limitP, Pconst.integrated_error_P2, Pconst.last_error_P2],
          'Angle1': [KpA, KiA, KdA, Pconst.limitA, Pconst.integrated_error_A1, Pconst.last_error_A1],
          'Angle2': [KpA, KiA, KdA, Pconst.limitA, Pconst.integrated_error_A2, Pconst.last_error_A2]}

        controllerVar=typeController[type]

	# Code for the PID controllers
        pTerm = float(controllerVar[0] * self.error)
        controllerVar[4] += float(self.error)

	# Limiting the integrated error, avoiding windup
        controllerVar[4] = max(-controllerVar[3], min(controllerVar[4], controllerVar[3]))

        iTerm = float(controllerVar[1] * controllerVar[4])
        dTerm = float(controllerVar[2] * (self.error - controllerVar[5]))
        controllerVar[5] = self.error

        PID_result = float(pTerm + iTerm + dTerm)

	# Updating the integrated error	and the last error for the next loop
        if(type is 'Position1'):
            Pconst.integrated_error_P1 = controllerVar[4]
            Pconst.last_error_P1= controllerVar[5]

        if(type is 'Position2'):
            Pconst.integrated_error_P2 = controllerVar[4]
            Pconst.last_error_P2= controllerVar[5]

	if(type is 'Angle1'):
            Pconst.integrated_error_A1 = controllerVar[4]
            Pconst.last_error_A1= controllerVar[5]
            if userChoice=='1':
            	PID_result = max(-127, min(PID_result, 127)) 			#Limiting the PID values because of the Sabertooth range (-127, 127)
            if userChoice=='2':
		PID_result = max(-100, min(PID_result, 100))			#Limiting the percentage of the PWM
		
	if(type is 'Angle2'):
            Pconst.integrated_error_A2 = controllerVar[4]			
            Pconst.last_error_A2= controllerVar[5]
            if userChoice=='1':							#Limiting the PID values because of the Sabertooth range (-127, 127)	
            	PID_result = max(-127, min(PID_result, 127))			
            if userChoice=='2':
		PID_result = max(-100, min(PID_result, 100))			#Limiting the percentage of the PWM					


        return -PID_result
