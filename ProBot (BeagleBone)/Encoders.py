#!/usr/bin/python

# Python Standard Library Imports
import eqep 
import math

# Instantiate an instance of the driver for encoder of the motor 1
encoder1 = eqep.eQEP("/sys/devices/ocp.3/48300000.epwmss/48300180.eqep", eqep.eQEP.MODE_ABSOLUTE)
# Instantiate an instance of the driver for encoder of the motor 2
encoder2 = eqep.eQEP("/sys/devices/ocp.3/48304000.epwmss/48304180.eqep", eqep.eQEP.MODE_ABSOLUTE)

# Set the polling period of the encoder's to 0.1 seconds, or 100,000,000 nanoseconds
encoder1.set_period(20000000) 
encoder2.set_period(20000000)


class EncodersReadings():
    def __init__(self, LastwheelPosition=0):
        self.LastwheelPosition = LastwheelPosition										

    def EncodersValues(self):

        wheelPosition1 = -encoder1.poll_position()					# Get position from the first encoder
        wheelPosition2 = encoder2.poll_position()					# Get position from the second encoder

        wheelPosition1_m = (float(wheelPosition1)) / 980 * math.pi * 0.2032		# Calculate the travelled distance for first encoder
        wheelPosition2_m = (float(wheelPosition2)) / 980 * math.pi * 0.2032		# Calculated the travelled distance for second encoder	

        wheelPosition = float(wheelPosition1_m + wheelPosition2_m)/2			# Average travelled distance from the robot

        wheelVelocity = wheelPosition - self.LastwheelPosition				# Wheel velocity (we are sampling at 100ms the encoders)

        self.LastwheelPosition = wheelPosition						# Keep the position for next cycle

        return wheelVelocity, wheelPosition
