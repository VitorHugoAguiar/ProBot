#!/usr/bin/python

import eqep

# Constants used in the algorithm
class Constants:
    def __init__(self):
	self.baud=38400
	self.addr=128
	self.PWM_Freq=10000
	self.PWM_L_DIR="P9_14"
	self.PWM_L_PWM="P9_22"
	self.PWM_R_DIR="P9_42"
	self.PWM_R_PWM="P8_13"
        self.ticks = 10000
        self.wheelDiameter = 0.25
        self.RedLED = "P8_7"
        self.GreenLED = "P8_9"
	self.BlueLED = "P8_11"
	self.rad_to_deg = 57.29578
	self.Angle_offset = 0
	self.GYR_offset=2.7
        self.SaberTooth_KpP = 280
        self.SaberTooth_KiP = 0.6
        self.SaberTooth_KdP = 12
        self.SaberTooth_KpA = 18
        self.SaberTooth_KiA = 2.2
        self.SaberTooth_KdA = -2
        self.PWM_KpP = 390
        self.PWM_KiP = 1
        self.PWM_KdP = 100
        self.PWM_KpA = 5
        self.PWM_KiA = 1.7
        self.PWM_KdA = -0.05
	self.limitP = 200
        self.limitA = 200 
        self.integrated_error_P1 = 0
        self.integrated_error_P2 = 0
        self.integrated_error_A1 = 0
        self.integrated_error_A2 = 0
        self.last_error_P1 = 0
        self.last_error_P2 = 0
        self.last_error_A1 = 0
        self.last_error_A2 = 0
        self.MinRedLiPo = 20
        self.AnalogPinLiPo = "P9_40"
        self.ajustFR = 0.0045
        self.ajustLR = 0.0025
	self.encoder1 = eqep.eQEP("/sys/devices/ocp.3/48302000.epwmss/48302180.eqep", eqep.eQEP.MODE_ABSOLUTE)
	self.encoder2 = eqep.eQEP("/sys/devices/ocp.3/48304000.epwmss/48304180.eqep", eqep.eQEP.MODE_ABSOLUTE)
