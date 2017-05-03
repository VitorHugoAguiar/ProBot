#!/usr/bin/python

# Python Standard Library Imports
import math
import ProBotConstantsFile

# Initialization of classes from local files
Pconst = ProBotConstantsFile.Constants()


class EncodersClass():
    def __init__(self, LastwheelPosition1=0, LastwheelPosition2=0):
        self.LastwheelPosition1 = LastwheelPosition1
	self.LastwheelPosition2 = LastwheelPosition2

    def EncodersValues(self):

        wheelTicks1 = -Pconst.encoder1.get_position()		# Get position from the first encoder
        wheelTicks2 = -Pconst.encoder2.get_position()		# Get position from the second encoder
				
        wheelPosition1_m = (float(wheelTicks1)) / Pconst.ticks * math.pi * Pconst.wheelDiameter	# First wheel distance travelled 
        wheelPosition2_m = (float(wheelTicks2)) / Pconst.ticks * math.pi * Pconst.wheelDiameter	# Second wheel distance travelled

        wheelVelocity1 = float(wheelPosition1_m - self.LastwheelPosition1)			# Wheel velocity
	wheelVelocity2 = float(wheelPosition2_m - self.LastwheelPosition2)   		

	self.LastwheelPosition1 = wheelPosition1_m   
	self.LastwheelPosition2 = wheelPosition2_m

        return [wheelVelocity1, wheelVelocity2]
