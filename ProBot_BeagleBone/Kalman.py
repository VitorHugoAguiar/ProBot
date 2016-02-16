#!/usr/bin/python

# Python Standard Library Imports
import time


# Kalman filter for the accelerometer and gyroscope data
class KalmanFilter():
    def __init__(self, angle=0, bias=0, P_00=0, P_01=0, P_10=0, P_11=0, y=0, S=0, K_0=0, K_1=0, Q_angle=0.001, Q_gyro=0.003, R_angle=0.03):	
        self.angle = angle		
        self.bias = bias
        self.P_00 = P_00
        self.P_01 = P_01
        self.P_10 = P_10
        self.P_11 = P_11
        self.y = y
        self.S = S
        self.K_0 = K_0
        self.K_1 = K_1
        self.Q_angle = Q_angle
        self.Q_gyro = Q_gyro
        self.R_angle = R_angle

    def KalmanCalculate(self, newAngle, newRate, LoopTime):
        currtm = time.time()
        dt = float(currtm-LoopTime)

        self.angle += dt * (newRate - self.bias)
        self.P_00 += - dt * (self.P_10 + self.P_01) + self.Q_angle * dt
        self.P_01 += - dt * self.P_11
        self.P_10 += - dt * self.P_11
        self.P_11 += + self.Q_gyro * dt

        self.y = newAngle - self.angle
        self.S = self.P_00 + self.R_angle
        self.K_0 = self.P_00 / self.S
        self.K_1 = self.P_10 / self.S

        self.angle += self.K_0 * self.y
        self.bias += self.K_1 * self.y
        self.P_00 -= self.K_0 * self.P_00
        self.P_01 -= self.K_0 * self.P_01
        self.P_10 -= self.K_1 * self.P_00
        self.P_11 -= self.K_1 * self.P_01

        return self.angle
