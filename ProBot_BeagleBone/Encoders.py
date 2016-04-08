#!/usr/bin/python

# Python Standard Library Imports
import eqep
import math
import ProBotConstants

Pconst = ProBotConstants.Constants()

# Instantiate an instance of the driver for encoder of the motor 1
encoder1 = eqep.eQEP("/sys/devices/ocp.3/48302000.epwmss/48302180.eqep", eqep.eQEP.MODE_ABSOLUTE)
# Instantiate an instance of the driver for encoder of the motor 2
encoder2 = eqep.eQEP("/sys/devices/ocp.3/48304000.epwmss/48304180.eqep", eqep.eQEP.MODE_ABSOLUTE)


class EncodersReadings():
    def __init__(self, LastwheelPosition1=0, LastwheelPosition2=0):
        self.LastwheelPosition1 = LastwheelPosition1
	self.LastwheelPosition2 = LastwheelPosition2

    def EncodersValues(self, ResetPositionEncoders):
	if ResetPositionEncoders==1:
		encoder1.set_position(0)
		encoder2.set_position(0)

        wheelPosition1 = encoder1.get_position()					# Get position from the first encoder
        wheelPosition2 = encoder2.get_position()					# Get position from the second encoder

        wheelPosition1_m = (float(wheelPosition1)) / Pconst.ticks * math.pi * Pconst.wheelDiameter	# Calculate the travelled distance for first encoder
        wheelPosition2_m = (float(wheelPosition2)) / Pconst.ticks * math.pi * Pconst.wheelDiameter	# Calculated the travelled distance for second encoder

        wheelVelocity1 = float(wheelPosition1_m - self.LastwheelPosition1)				# Wheel velocity (we are sampling at 100ms the encoders)
	wheelVelocity2 = float(wheelPosition2_m - self.LastwheelPosition2)   		

 
	self.LastwheelPosition1 = wheelPosition1_m   
	self.LastwheelPosition2 = wheelPosition2_m

        return wheelVelocity1, wheelVelocity2
