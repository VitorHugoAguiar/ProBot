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

# Global variables
global PI
global wheelPositionError
global integrated_wheelPositionError
global errorVelocity
global integrated_errorVelocity
global errorAngle
global last_errorAngle
global integrated_errorAngle
global wheelPosition
global LastwheelPosition


PI = 3.14159265358979323846							# PI value
wheelPositionError=0								# Initialization of all variables
integrated_wheelPositionError=0
errorVelocity=0
integrated_errorVelocity=0
errorAngle=0
last_errorAngle=0
integrated_errorAngle=0
wheelPosition=0
LastwheelPosition=0

# PID values (some are still not in use)

wheelPositionRef=0.000

# Position PID values
KpPosition=0.000
KiPosition=0.000

# Velocity PID values
KpVelocity=2.000
KiVelocity=0.500

# Angle PID values
KpAngle=7.000 
KiAngle=5.000
KdAngle=9.000

# PID functions
class PIDControllers():

	def PiPosition(self):
		
		global wheelPositionError
		global integrated_wheelPositionError
		global wheelPosition

		wheelPositionError=float (wheelPositionRef)-float (wheelPosition)	 # Error of the requested position
		pTermPosition=KpPosition*float(wheelPositionError)			 # Proportional term of the error
		integrated_wheelPositionError +=float (wheelPositionError)		 # Integral error
		iTermPosition=KiPosition*float (integrated_wheelPositionError)		 # Integral term of the error
		PiVelocityRef=float (pTermPosition)+float (iTermPosition)		 # PID result
	
		return PiVelocityRef
	
	def PiVelocity(self,PiVelocityRef):
	
		global LastwheelPosition
		global errorVelocity
		global integrated_errorVelocity
		global wheelPosition
	
		wheelPosition1=-encoder1.poll_position()				# Get position from the first encoder
		wheelPosition2=encoder2.poll_position()					# Get position from the second encoder
		wheelPosition1_m=(float (wheelPosition1))/(980*PI*0.2032)		# Calculate the travelled distance for first encoder
		wheelPosition2_m=(float (wheelPosition2))/(980*PI*0.2032)		# Calculated the travelled distance for second encoder	
	
	
		wheelPosition=float(wheelPosition1_m+wheelPosition2_m)/2		# Average travelled distance from the robot
	
		wheelVelocity=wheelPosition-LastwheelPosition				# Wheel velocity (we are sampling at 100ms the encoders)
	
		LastwheelPosition=wheelPosition						# Keep the position for next cycle
	
		errorVelocity=float (PiVelocityRef)-float (wheelVelocity)		# Error for requested velocity
		pTermVelocity=KpVelocity*float(errorVelocity)				# Proportional term of the error
		integrated_errorVelocity +=errorVelocity				# Integral error
		iTermVelocity=KiVelocity*float (integrated_errorVelocity)		# Integral term of the error
		PiAngleRef=pTermVelocity+iTermVelocity					# Velocity PID result
	
		return -PiAngleRef
	
	def PidAngle(self,x_angle,PiAngleRef):
		
		global errorAngle
		global last_errorAngle
		global integrated_errorAngle

		errorAngle=float (PiAngleRef)-float (x_angle)				# Error for requested angle
		pTermAngle=KpAngle*errorAngle						# Proportional term of the error
		integrated_errorAngle +=errorAngle					# Integral error
		if integrated_errorAngle<-35:						# Integral limits
			integrated_errorAngle=-35
		if integrated_errorAngle>35:
			integrated_errorAngle=35
	
		iTermAngle=KiAngle*integrated_errorAngle				# Integral term of the error
		dTermAngle=KdAngle*(errorAngle-last_errorAngle)				# Derivative term of the error
		last_errorAngle=errorAngle						# Keep actual value
		PidMotorRef=pTermAngle+iTermAngle+dTermAngle				# Angle PID result
	
		if PidMotorRef<-127:							# Limits for motor reference
			PidMotorRef=-127
		
		if PidMotorRef>127:
			PidMotorRef=127
	
		return PidMotorRef
