#!/usr/bin/python

# Python Standard Library Imports
import math

# PID functions
class PIDControllers():

	# Build a constructor	
	def __init__(self, error = 0, integrated_error = 0, integrated_error_f = [0, 0, 0], last_error_f=[0, 0, 0], last_error = 0, KpP_tenths=0, KpP1_tenths=0, KpP_hundredths=0,KpP_thousandths=0, KiP_tenths=0, KiP1_tenths=0, KiP_hundredths=0, KiP_thousandths=0, KdP_tenths=0, KdP1_tenths=0, KdP_hundredths=0, KdP_thousandths=0, KpA_tenths=0, KpA1_tenths=0,KpA_hundredths=0, KpA_thousandths=0, KiA_tenths=0, KiA1_tenths=0,KiA_hundredths=0, KiA_thousandths=0, KdA_tenths=0, KdA1_tenths=0,KdA_hundredths=0, KdA_thousandths=0,     KpV_tenths=0, KpV_hundredths=0, KpV_thousandths=0, KiV_tenths=0, KiV_hundredths=0, KiV_thousandths=0, KdV_tenths=0, KdV_hundredths=0, KdV_thousandths=0):
									
		self.error = error
		self.integrated_error = integrated_error
		self.last_error = last_error
		self.integrated_error_f = integrated_error_f
		self.last_error_f = last_error_f
		
		# We are using a midi controller (Evolution UC33) to tune the controllers
		# So, we can ajust tenths, hundredths, thousandths for each parameter of the Position, Velocity and Angle controller
		
		# Position controller
		self.KpP_tenths=KpP_tenths
		self.KpP1_tenths=KpP1_tenths
		self.KpP_hundredths=KpP_hundredths
		self.KpP_thousandths=KpP_thousandths

		self.KiP_tenths=KiP_tenths
		self.KiP1_tenths=KiP_tenths
		self.KiP_hundredths=KiP_hundredths
		self.KiP_thousandths=KiP_thousandths

		self.KdP_tenths=KdP_tenths
		self.KdP1_tenths=KdP_tenths
		self.KdP_hundredths=KdP_hundredths
		self.KdP_thousandths=KdP_thousandths

		# Velocity controller
		self.KpA_tenths=KpA_tenths
		self.KpA1_tenths=KpA_tenths
		self.KpA_hundredths=KpA_hundredths
		self.KpA_thousandths=KpA_thousandths

		self.KiA_tenths=KiA_tenths
		self.KiA1_tenths=KiA_tenths
		self.KiA_hundredths=KiA_hundredths
		self.KiA_thousandths=KiA_thousandths

		self.KdA_tenths=KdA_tenths
		self.KdA1_tenths=KdA_tenths
		self.KdA_hundredths=KdA_hundredths
		self.KdA_thousandths=KdA_thousandths

		# Angle controller
		self.KpV_tenths=KpV_tenths
		self.KpV_hundredths=KpV_hundredths
		self.KpV_thousandths=KpV_thousandths

		self.KiV_tenths=KiV_tenths
		self.KiV_hundredths=KiV_hundredths
		self.KiV_thousandths=KiV_thousandths

		self.KdV_tenths=KdV_tenths
		self.KdV_hundredths=KdV_hundredths
		self.KdV_thousandths=KdV_thousandths
	
	def standardPID(self, reference, measured, type, id, value):
		self.error = float(reference - measured)
		
		# For each id (pontenciometer), we atribute a diferent parameter
		
		# Position controller
		# Kp from Position controller
 		if (id == 25 or id==1):
			if id==25:			
				self.KpP_tenths=float(value*0.1)
			if id==1:			
				self.KpP1_tenths=float(value*0.1)
		if (id == 17):
			self.KpP_hundredths=float(value*0.01)
		if (id == 9):
			self.KpP_thousandths=float(value*0.001)

		# Ki from Position controller
		if (id == 26 or id==2):
			if id==26:			
				self.KiP_tenths=float(value*0.1)
			if id==2:			
				self.KiP1_tenths=float(value*0.1)
		if (id == 18):
			self.KiP_hundredths=float(value*0.01)
		if (id == 10):
			self.KiP_thousandths=float(value*0.001)

		# Kd from Position controller
		if (id == 27 or id==3):
			if id==27:
				self.KdP_tenths=float(value*0.1)
			if id==3:
				self.KdP1_tenths=float(value*0.1)
		if (id == 19):
			self.KdP_hundredths=float(value*0.01)
		if (id == 11):
			self.KdP_thousandths=float(value*0.001)


		# Velocity controller
		# Kp from Velocity controller
		if (id == 28 or id==4):
			if id==28:
				self.KpA_tenths=float(value*0.1)
			if id==4:
				self.KpA1_tenths=float(value*0.1)
		if (id == 20):
			self.KpA_hundredths=float(value*0.01)
		if (id == 12):
			self.KpA_thousandths=float(value*0.001)

		# Ki from Velocity controller
		if (id == 29 or id==5):
			if id==29:
				self.KiA_tenths=float(value*0.1)
			if id==5:
				self.KiA1_tenths=float(value*0.1)
		if (id == 21):
			self.KiA_hundredths=float(value*0.01)
		if (id == 13):
			self.KiA_thousandths=float(value*0.001)

		# Kd from Velocity controller
		if (id == 30 or id==6):
			if id==30:
				self.KdA_tenths=float(value*0.1)
			if id==6:
				self.KdA1_tenths=float(value*0.1)
		if (id == 22):
			self.KdA_hundredths=float(value*0.01)
		if (id == 14):
			self.KdA_thousandths=float(value*0.001)

		

		# Angle controller
		# Kp from Angle controller
		if (id == 31):				
			self.KpV_tenths=float(value*0.1)
		if (id == 23):
			self.KpV_hundredths=float(value*0.01)
		if (id == 15):
			self.KpV_thousandths=float(value*0.001)

		# Ki from Angle controller
		if (id == 32):
			self.KiV_tenths=float(value*0.1)
		if (id == 24):
			self.KiV_hundredths=float(value*0.01)
		if (id == 16):
			self.KiV_thousandths=float(value*0.001)

		# Kd from Angle controller
		if (id == 7 ):
			self.KdV_tenths=float(value*0.1)
		if (id == 8):
			self.KdV_hundredths=float(value*0.01)
		if (id == 33):
			self.KdV_thousandths=float(value*0.001)		
		
		# Here we choose the controller
		if (type == 0):																			# Type 0 - Position 			
			Kp = float(self.KpP_tenths-self.KpP1_tenths+self.KpP_hundredths+self.KpP_thousandths)		
			Ki = float(self.KiP_tenths-self.KiP1_tenths+self.KiP_hundredths+self.KiP_thousandths)
			Kd = float(self.KdP_tenths-self.KdP1_tenths+self.KdP_hundredths+self.KdP_thousandths)
			limit = 200000										
			#self.integrated_error = self.integrated_error_f[0]
			#self.last_error = self.last_error_f[0]
			
			
		elif (type == 1):																		# Type 1 - Velocity
			Kp = float(self.KpV_tenths+self.KpV_hundredths+self.KpV_thousandths)		
			Ki = float(self.KiV_tenths+self.KiV_hundredths+self.KiV_thousandths)
			Kd = float(self.KdV_tenths+self.KdV_hundredths+self.KdV_thousandths)
			limit = 200000
			self.integrated_error = self.integrated_error_f[1]
			self.last_error = self.last_error_f[1]
			
		 	
		elif (type == 2):																		# Type 2 - Angle
			Kp = float(self.KpA_tenths-self.KpA1_tenths+self.KpA_hundredths+self.KpA_thousandths)
			Ki = float(self.KiA_tenths-self.KiA1_tenths+self.KiA_hundredths+self.KiA_thousandths)
			Kd = float(self.KdA_tenths-self.KdA1_tenths+self.KdA_hundredths+self.KdA_thousandths)
			limit = 35
			self.integrated_error = self.integrated_error_f[2]
			self.last_error = self.last_error_f[2]
			
		else:
			pass
		
		pTerm = float(Kp * self.error)
		self.integrated_error += float(self.error) 
		
		if (self.integrated_error < -limit):													# Integral limits
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
			return -PID_result
		
		elif(type == 2):
			
			self.integrated_error_f[2] = self.integrated_error
			self.last_error_f[2] = self.last_error
			
			if (PID_result < -127):																# Limits for motor reference
				PID_result = -127
			if (PID_result > 127):
				PID_result = 127
			return PID_result
		
		else:
			pass

			
