#!/usr/bin/python

# Python Standard Library Imports
import time

# Local files
import ProBotConstantsFile

# Initialization of classes from local files
Pconst = ProBotConstantsFile.Constants()

# PID functions
class PIDControllersClass():
    # Build a constructor
    def __init__(self):
        self.error = 0
        self.SaberTooth_KpV = 280
        self.SaberTooth_KiV = 0.6
        self.SaberTooth_KdV = 12
        self.SaberTooth_KpA = 18
        self.SaberTooth_KiA = 2.2
        self.SaberTooth_KdA = -2
        self.PWM_KpV = 75
        self.PWM_KiV = 0.6
        self.PWM_KdV = 0.2
        self.PWM_KpA = 9
        self.PWM_KiA = 3
        self.PWM_KdA = -0.001
        self.limitV = 800
        self.limitA = 1000
        self.integrated_error_V1 = 0
        self.integrated_error_V2 = 0
        self.integrated_error_A1 = 0
        self.integrated_error_A2 = 0
        self.last_error_V1 = 0
        self.last_error_V2 = 0
        self.last_error_A1 = 0
        self.last_error_A2 = 0
        
    def standardPID(self, reference, measured, type, userChoice):
        self.error = float(reference - measured)
        
        # Load the right values for the controllers,  depending on if we are using Sabertooth of PWM controller
        if userChoice=='1':        
                KpV = self.SaberTooth_KpV
                KiV = self.SaberTooth_KiV
                KdV = self.SaberTooth_KdV
                KpA = self.SaberTooth_KpA
                KiA = self.SaberTooth_KiA
                KdA = self.SaberTooth_KdA

        if userChoice=='2':
                KpV = self.PWM_KpV
                KiV = self.PWM_KiV
                KdV = self.PWM_KdV
                KpA = self.PWM_KpA
                KiA = self.PWM_KiA
                KdA = self.PWM_KdA
        
        # Loading the variables for the controllers
        typeController = { 
          'Velocity1': [KpV, KiV, KdV, self.limitV, self.integrated_error_V1, self.last_error_V1],
          'Velocity2': [KpV, KiV, KdV, self.limitV, self.integrated_error_V2, self.last_error_V2],
          'Angle1': [KpA, KiA, KdA, self.limitA, self.integrated_error_A1, self.last_error_A1],
          'Angle2': [KpA, KiA, KdA, self.limitA, self.integrated_error_A2, self.last_error_A2]}

        controllerVar = typeController[type]

        # Code for the PID controllers
        pTerm = float(controllerVar[0] * self.error)
        controllerVar[4] += float(self.error)

        # Limiting the integrated error, avoiding windup
        controllerVar[4] = max(-controllerVar[3], min(controllerVar[4], controllerVar[3]))

        iTerm = float(controllerVar[1] * controllerVar[4])
        dTerm = float(controllerVar[2] * (self.error - controllerVar[5]))
        controllerVar[5] = self.error

        PID_result = float(pTerm + iTerm + dTerm)

        # Updating the integrated error        and the last error for the next loop
        if(type is 'Velocity1'):
            self.integrated_error_V1 = controllerVar[4]
            self.last_error_V1 = controllerVar[5] 

        if(type is 'Velocity2'):
            self.integrated_error_V2 = controllerVar[4]
            self.last_error_V2 = controllerVar[5]
             
        if(type is 'Angle1'):
            self.integrated_error_A1 = controllerVar[4]
            self.last_error_A1 = controllerVar[5]
            if userChoice == '1':
                PID_result = max(-127, min(PID_result, 127))                         #Limiting the PID values because of the Sabertooth range (-127, 127)
            if userChoice == '2':
                PID_result = max(-100, min(PID_result, 100))                        #Limiting the percentage of the PWM
                
        if(type is 'Angle2'):
            self.integrated_error_A2 = controllerVar[4]                        
            self.last_error_A2 = controllerVar[5]
            if userChoice=='1':                                                        #Limiting the PID values because of the Sabertooth range (-127, 127)        
                PID_result = max(-127, min(PID_result, 127))                        
            if userChoice=='2':
                PID_result = max(-100, min(PID_result, 100))                        #Limiting the percentage of the PWM                                        

        return -PID_result
