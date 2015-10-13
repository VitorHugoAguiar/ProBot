#!/usr/bin/python

# Python Standard Library Imports
import time

# Global variables
global x_angle
global x_bias
global P_00
global P_01
global P_10
global P_11
global dt
global y
global S
global K_0 
global K_1

# Variables initialization
x_angle = 0
x_bias = 0
P_00 = 0
P_01 = 0
P_10 = 0
P_11 = 0
dt=0
y=0
S=0
K_0=0 
K_1=0
Q_angle  =  0.001 
Q_gyro   =  0.003  
R_angle  =  0.03

# Kalman filter for the accelerometer and gyroscope data
class KalmanFilter():
	def KalmanCalculate (self,newAngle, newRate, looptime):				
		global x_angle
		global x_bias
		global P_00
		global P_01
		global P_10
		global P_11
		global dt
		global y
		global S
		global K_0 
		global K_1

		b= time.time()							# Time stamp of the loop
		dt=b-looptime							# Loop time of the code
	
		x_angle += dt * (newRate - x_bias)
		P_00 +=  - dt * (P_10 + P_01) + Q_angle * dt
		P_01 +=  - dt * P_11
		P_10 +=  - dt * P_11
		P_11 +=  + Q_gyro * dt

		y = newAngle - x_angle
		S = P_00 + R_angle
		K_0 = P_00 / S
		K_1 = P_10 / S
	
		x_angle +=  K_0 * y
		x_bias  +=  K_1 * y
		P_00 -= K_0 * P_00
		P_01 -= K_0 * P_01
		P_10 -= K_1 * P_00
		P_11 -= K_1 * P_01
	
		return x_angle
