#!/usr/bin/python

# Python Standard Library Imports
import math

# PID functions
class PIDControllers():

	# Build a constructor	
	def __init__(self, error = 0, integrated_error = 0, integrated_error_f = [0, 0], last_error_f=[0, 0], last_error = 0):
									
		self.error = error
		self.integrated_error = integrated_error
		self.last_error = last_error
		self.integrated_error_f = integrated_error_f
		self.last_error_f = last_error_f
   	 
	
	def standardPID(self, reference, measured, type):
		self.error = float(reference - measured)

		# Here we choose the controller
		if (type == 0):                                                          # Type 0 - Position 
						
			Kp = 0	
			Ki = 0
			Kd = 0
			limit = 1000										
			self.integrated_error = self.integrated_error_f[0]
			self.last_error = self.last_error_f[0]


		elif (type == 1):
											# Type 1 - Velocity
			Kp = 10
			Ki = 0.3
			Kd = 1
			limit =310
			self.integrated_error = self.integrated_error_f[1]
			self.last_error = self.last_error_f[1]
			
		 	
		elif (type == 2):
											 # Type 2 - Angle
			Kp = 10
			Ki = 0.75
			Kd = -0.3
			limit = 310
			self.integrated_error = self.integrated_error_f[1]
			self.last_error = self.last_error_f[1]


		else:
			pass

		
		pTerm = float(Kp * self.error)
		self.integrated_error += float(self.error)

		if (self.integrated_error < -limit):					# Integral limits
			self.integrated_error = -limit
		elif (self.integrated_error > limit):
			self.integrated_error = limit
		else:
			pass 
		
		iTerm = float(Ki * self.integrated_error)
		dTerm = float(Kd * (self.error - self.last_error))
		self.last_error = self.error
		PID_result = float(pTerm + iTerm + dTerm)
		
		if (type == 0):
			self.integrated_error_f[0] = self.integrated_error
			self.last_error_f[0] = self.last_error
			return PID_result
			
		elif (type == 1):
			self.integrated_error_f[1] = self.integrated_error
			self.last_error_f[1] = self.last_error
			return PID_result
		
		elif(type == 2):
			
			self.integrated_error_f[1] = self.integrated_error
			self.last_error_f[1] = self.last_error
			
			if (PID_result < -127):						# Limits for motor reference
				PID_result = -127
			if (PID_result > 127):
				PID_result = 127
			
			return PID_result
		
		else:
			pass

			
