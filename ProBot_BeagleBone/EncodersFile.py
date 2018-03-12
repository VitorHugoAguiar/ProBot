#!/usr/bin/python

# Python Standard Library Imports
import math
import eqep

# Local files
import LowPassFilter

# Initialization of classes from local files
LPF = LowPassFilter.LowPassFilter()

class EncodersClass():

    def __init__(self):
        self.LastwheelPosition1 = 0
	self.LastwheelPosition2 = 0
	self.ticks = 10000
        self.wheelDiameter = 0.25
	self.encoder1 = eqep.eQEP("/sys/devices/platform/ocp/48302000.epwmss/48302180.eqep", eqep.eQEP.MODE_ABSOLUTE)
	self.encoder2 = eqep.eQEP("/sys/devices/platform/ocp/48304000.epwmss/48304180.eqep", eqep.eQEP.MODE_ABSOLUTE)

    def EncodersValues(self):
        wheelTicks1 = -self.encoder1.get_position()		# Get position from the first encoder (left wheel)
        wheelTicks2 = -self.encoder2.get_position()		# Get position from the second encoder (right wheel)
	wheelTicks1 = LPF.lowPassFilter(wheelTicks1, 'EncoderL')
	wheelTicks2 = LPF.lowPassFilter(wheelTicks2, 'EncoderR')
	wheelPosition1_m = (float(wheelTicks1)) / self.ticks * math.pi * self.wheelDiameter	# Left wheel distance travelled
        wheelPosition2_m = (float(wheelTicks2)) / self.ticks * math.pi * self.wheelDiameter	# Right wheel distance travelled

        wheelVelocity1 = float(wheelPosition1_m - self.LastwheelPosition1)	# Left wheel velocity
	wheelVelocity2 = float(wheelPosition2_m - self.LastwheelPosition2)	# Right wheel velocity

	self.LastwheelPosition1 = wheelPosition1_m
	self.LastwheelPosition2 = wheelPosition2_m

	return wheelVelocity1, wheelVelocity2
	

