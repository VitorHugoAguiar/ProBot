#!/usr/bin/python

# Python Standard Library Imports
from eqep import eQEP

# Instantiate an instance of the driver for encoder of the motor 1
encoder1 = eQEP("/sys/devices/ocp.3/48302000.epwmss/48302180.eqep", eQEP.MODE_ABSOLUTE)
# Instantiate an instance of the driver for encoder of the motor 2
encoder2 = eQEP("/sys/devices/ocp.3/48304000.epwmss/48304180.eqep", eQEP.MODE_ABSOLUTE)

# Set the polling period of the encoder's to 0.1 seconds, or 100,000,000 nanoseconds
encoder1.set_period(100000000)
encoder2.set_period(100000000)

# PID functions
class PIDControllers():

	PI = 3.14159265
	
	# Velocity PI values
	KpVelocity = 2.000
	KiVelocity = 0.500

	# Angle PID values
	KpAngle = 7.000
	KiAngle = 5.000
	KdAngle = 9.000
		
	def __init__(self, LastwheelPosition = 0, errorVelocity = 0, integrated_errorVelocity = 0, errorAngle = 0, integrated_errorAngle = 0, last_errorAngle = 0):
		
		self.LastwheelPosition = LastwheelPosition										
		self.errorVelocity = errorVelocity
		self.integrated_errorVelocity = integrated_errorVelocity
		self.errorAngle = errorAngle
		self.integrated_errorAngle = integrated_errorAngle
		self.last_errorAngle = last_errorAngle
		
		
	def PiVelocity(self, PiVelocityRef):
			
		wheelPosition1 = -encoder1.poll_position()				# Get position from the first encoder
		wheelPosition2 = encoder2.poll_position()					# Get position from the second encoder
		wheelPosition1_m = (float (wheelPosition1))/float(980*self.PI*0.2032)	# Calculate the travelled distance for first encoder
		wheelPosition2_m = (float (wheelPosition2))/float(980*self.PI*0.2032)	# Calculated the travelled distance for second encoder	
	
		wheelPosition = float(wheelPosition1_m+wheelPosition2_m)/2		# Average travelled distance from the robot
	
		wheelVelocity = wheelPosition-self.LastwheelPosition			# Wheel velocity (we are sampling at 100ms the encoders)
	
		self.LastwheelPosition = wheelPosition					# Keep the position for next cycle
	
		self.errorVelocity = float (PiVelocityRef)-float (wheelVelocity)		# Error for requested velocity
		pTermVelocity = self.KpVelocity*float(self.errorVelocity)			# Proportional term of the error
		self.integrated_errorVelocity += float (self.errorVelocity)		# Integral error
		iTermVelocity = self.KiVelocity*float (self.integrated_errorVelocity)	# Integral term of the error
		PiAngleRef = float (pTermVelocity) + float (iTermVelocity)			# Velocity PID result
	
		return -PiAngleRef
	
	def PidAngle(self, x_angle, PiAngleRef):

		self.errorAngle = float (PiAngleRef)-float (x_angle)			# Error for requested angle
		pTermAngle = self.KpAngle*float (self.errorAngle)			# Proportional term of the error
		self.integrated_errorAngle += float (self.errorAngle)			# Integral error
		if self.integrated_errorAngle < -35:					# Integral limits
			self.integrated_errorAngle = -35
		if self.integrated_errorAngle > 35:
			self.integrated_errorAngle = 35
	
		iTermAngle = self.KiAngle*float (self.integrated_errorAngle)			# Integral term of the error
		dTermAngle = self.KdAngle*(self.errorAngle-self.last_errorAngle)		# Derivative term of the error
		self.last_errorAngle = self.errorAngle						# Keep actual value
		PidMotorRef = float (pTermAngle) + float (iTermAngle) + float (dTermAngle)	# Angle PID result
	
		if PidMotorRef < -127:								# Limits for motor reference
			PidMotorRef = -127
		
		if PidMotorRef > 127:
			PidMotorRef = 127
	
		return PidMotorRef
