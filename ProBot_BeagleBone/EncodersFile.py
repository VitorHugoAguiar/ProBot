#!/usr/bin/python


# Python Standard Library Imports
import math

# Local files
import ProBotConstantsFile

# Initialization of classes from local files
Pconst = ProBotConstantsFile.Constants()


class EncodersClass():
    def __init__(self, LastwheelPosition1=0, LastwheelPosition2=0, old_wheelTicks1=0, old_wheelTicks2=0):
        self.LastwheelPosition1 = LastwheelPosition1
	self.LastwheelPosition2 = LastwheelPosition2
        self.old_wheelTicks1 = old_wheelTicks1
        self.old_wheelTicks2 = old_wheelTicks2


    def EncodersValues(self):

        wheelTicks1 = -Pconst.encoder1.get_position()		# Get position from the first encoder
        wheelTicks2 = -Pconst.encoder2.get_position()		# Get position from the second encoder
					
        wheelPosition1_m = (float(wheelTicks1)) / Pconst.ticks * math.pi * Pconst.wheelDiameter	# First wheel distance travelled 
        wheelPosition2_m = (float(wheelTicks2)) / Pconst.ticks * math.pi * Pconst.wheelDiameter	# Second wheel distance travelled

        wheelVelocity1 = float(wheelPosition1_m - self.LastwheelPosition1)			# Wheel velocity
	wheelVelocity2 = float(wheelPosition2_m - self.LastwheelPosition2)   		

	self.LastwheelPosition1 = wheelPosition1_m   
	self.LastwheelPosition2 = wheelPosition2_m

 
        factor = ((60/0.01)/10000)  # 1min /delay between encoders update/counts_per_rev
        rpm1 = (wheelTicks1 - self.old_wheelTicks1)*factor
        rpm2 = (wheelTicks2 - self.old_wheelTicks2)*factor
	
        self.old_wheelTicks1 = wheelTicks1
        self.old_wheelTicks2 = wheelTicks2

	acel1=wheelVelocity1/0.01
	acel2=wheelVelocity2/0.01

	#publisher=Pub_Sub.publisher(acel1, acel2)


	return [wheelVelocity1, wheelVelocity2]
