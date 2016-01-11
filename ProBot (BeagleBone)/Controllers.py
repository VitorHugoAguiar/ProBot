#!/usr/bin/python

# Python Standard Library Imports
import math
import ProBotConstants 
import decimal
Pconst = ProBotConstants.Constants()


# PID functions
class PIDControllers():
    # Build a constructor	
    def __init__(self, error=0, Matrix=0, KpP_UC33=0, KiP_UC33=0, KdP_UC33=0, KpV_UC33=0, KiV_UC33=0, KdV_UC33=0, KpA_UC33=0, KiA_UC33=0, KdA_UC33=0):						
        self.error = error
	self.Matrix = [0 for x in range(34)]
	self.KpP_UC33=KpP_UC33
	self.KiP_UC33=KiP_UC33
	self.KdP_UC33=KdP_UC33
	self.KpV_UC33=KpV_UC33
	self.KiV_UC33=KiV_UC33
	self.KdV_UC33=KdV_UC33
	self.KpA_UC33=KpA_UC33
	self.KiA_UC33=KiA_UC33
	self.KdA_UC33=KdA_UC33
	
    def standardPID(self, reference, measured, id, value, type):
        self.error = float(reference - measured)
	# Updating the local variables with the values from th UC33 
	idInt=int(id)	
	self.Matrix[idInt]=value	
	self.KpP_UC33=(0.1*self.Matrix[25]+0.01*self.Matrix[17]+0.001*self.Matrix[9]-0.1*self.Matrix[1])
	self.KiP_UC33=(0.1*self.Matrix[26]+0.01*self.Matrix[18]+0.001*self.Matrix[10]-0.1*self.Matrix[2])
	self.KdP_UC33=(0.1*self.Matrix[27]+0.01*self.Matrix[19]+0.001*self.Matrix[11]-0.1*self.Matrix[3])
	self.KpV_UC33=(0.1*self.Matrix[28]+0.01*self.Matrix[20]+0.001*self.Matrix[12]-0.1*self.Matrix[4])
	self.KiV_UC33=(0.1*self.Matrix[29]+0.01*self.Matrix[21]+0.001*self.Matrix[13]-0.1*self.Matrix[5])
	self.KdV_UC33=(0.1*self.Matrix[30]+0.01*self.Matrix[22]+0.001*self.Matrix[14]-0.1*self.Matrix[6])
	self.KpA_UC33=(0.1*self.Matrix[31]+0.01*self.Matrix[23]+0.001*self.Matrix[15]-0.1*self.Matrix[7])
	self.KiA_UC33=(0.1*self.Matrix[32]+0.01*self.Matrix[24]+0.001*self.Matrix[16]-0.1*self.Matrix[8])
	self.KdA_UC33=(0.1*self.Matrix[33])
	
	# Loading the variables for the controllers
        typeController = {'Position': [Pconst.KpP+self.KpP_UC33, Pconst.KiP+self.KiP_UC33, Pconst.KdP+self.KdP_UC33, Pconst.limitP, Pconst.integrated_error_P, Pconst.last_error_P], 'Velocity': [Pconst.KpV+self.KpV_UC33, Pconst.KiV+self.KiV_UC33, Pconst.KdV+self.KdV_UC33, Pconst.limitV, Pconst.integrated_error_VA, Pconst.last_error_VA], 'Angle': [Pconst.KpA+self.KpA_UC33, Pconst.KiA+self.KiA_UC33, Pconst.KdA+self.KdA_UC33, Pconst.limitA, Pconst.integrated_error_VA, Pconst.last_error_VA]}
        controllerVar=typeController[type]
	
	# Code for the controllers PID
        pTerm = float(controllerVar[0] * self.error)
        controllerVar[4] += float(self.error)
	
	# Limiting the integrated error, avoiding windup
        controllerVar[4] = max(-controllerVar[3], min(controllerVar[4], controllerVar[3]))

        iTerm = float(controllerVar[1] * controllerVar[4])
        dTerm = float(controllerVar[2] * (self.error - controllerVar[5]))
        controllerVar[5] = self.error
	
        PID_result = float(pTerm + iTerm + dTerm)
	
	# Updating the integrated error	and the last error for the next loop
        if(type is 'Position'):
            Pconst.integrated_error_P = controllerVar[4]
            Pconst.last_error_P= controllerVar[5]

        if(type is 'Velocity'):
            Pconst.integrated_error_VA = controllerVar[4]
            Pconst.last_error_VA= controllerVar[5]	
		
        if(type is 'Angle'):
            Pconst.integrated_error_VA = controllerVar[4]
            Pconst.last_error_VA= controllerVar[5]	
            PID_result = max(-127, min(PID_result, 127))					# Limiting the output for the motors (-127, 127)
		
        return PID_result
