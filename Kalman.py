#!/usr/bin/python

# Python Standard Library Imports
import time

# Kalman filter for the accelerometer and gyroscope data
class KalmanFilter():
	
	Q_angle = 0.001
	Q_gyro = 0.003
	R_angle = 0.03
	
	def __init__(self,x_angle = 0, x_bias = 0, P_00 = 0, P_01 = 0, P_10 = 0,P_11 = 0, dt = 0, y = 0, S = 0, K_0 = 0, K_1 = 0):
		self.x_angle = x_angle		
		self.x_bias = x_bias
		self.P_00 = P_00
		self.P_01 = P_01
		self.P_10 = P_10
		self.P_11 = P_11
		self.dt = dt
		self.y = y
		self.S = S
		self.K_0 = K_0
		self.K_1 = K_1		
	
	def KalmanCalculate (self, newAngle, newRate, looptime):

		b = time.time()									# Time stamp
		self.dt = b - looptime								# Loop time for Kalman prediction
	
		self.x_angle += self.dt * (newRate - self.x_bias)
		self.P_00 +=  - self.dt * (self.P_10 + self.P_01) + self.Q_angle * self.dt
		self.P_01 +=  - self.dt * self.P_11
		self.P_10 +=  - self.dt * self.P_11
		self.P_11 +=  + self.Q_gyro * self.dt

		self.y = newAngle - self.x_angle
		self.S = self.P_00 + self.R_angle
		self.K_0 = self.P_00 / self.S
		self.K_1 = self.P_10 / self.S
	
		self.x_angle +=  self.K_0 * self.y
		self.x_bias  +=  self.K_1 * self.y
		self.P_00 -= self.K_0 * self.P_00
		self.P_01 -= self.K_0 * self.P_01
		self.P_10 -= self.K_1 * self.P_00
		self.P_11 -= self.K_1 * self.P_01
	
		return self.x_angle
