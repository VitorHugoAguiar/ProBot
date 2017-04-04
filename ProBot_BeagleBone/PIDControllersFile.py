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
		KpV=Pconst.SaberTooth_KpV
		KiV=Pconst.SaberTooth_KiV
		KdV=Pconst.SaberTooth_KdV
		KpA=Pconst.SaberTooth_KpA
		KiA=Pconst.SaberTooth_KiA
		KdA=Pconst.SaberTooth_KdA

	if userChoice=='2':
		KpV=Pconst.PWM_KpV
		KiV=Pconst.PWM_KiV
		KdV=Pconst.PWM_KdV
		KpA=Pconst.PWM_KpA
		KiA=Pconst.PWM_KiA
		KdA=Pconst.PWM_KdA

	# Loading the variables for the controllers
        typeController = { 
	  'Velocity1': [KpV, KiV, KdV, Pconst.limitV, Pconst.integrated_error_V1, Pconst.last_error_V1],
          'Velocity2': [KpV, KiV, KdV, Pconst.limitV, Pconst.integrated_error_V2, Pconst.last_error_V2],
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
        if(type is 'Velocity1'):
            Pconst.integrated_error_V1 = controllerVar[4]
            Pconst.last_error_V1= controllerVar[5]
	    #PID_result = max(-18, min(PID_result, 18)) 

        if(type is 'Velocity2'):
            Pconst.integrated_error_V2 = controllerVar[4]
 	    Pconst.last_error_V2= controllerVar[5]           
	    #PID_result = max(-18, min(PID_result, 18)) 
            

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
