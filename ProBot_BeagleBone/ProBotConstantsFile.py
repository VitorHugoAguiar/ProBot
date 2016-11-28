#!/usr/bin/python

import eqep

# Constants used in the algorithm
class Constants():
    def __init__(self):
	self.baud=38400
	self.addr=128
	self.PWM_Freq=15000
	self.PWM_RR="P9_14"
	self.PWM_RF="P9_22"
	self.PWM_LR="P8_13"
	self.PWM_LF="P9_42"
        self.ticks = 10000
        self.wheelDiameter = 0.3
        self.RedLED = "P8_7"
        self.GreenLED = "P8_9"
	self.BlueLED = "P8_11"
	self.rad_to_deg = 57.29578
	self.Angle_offset = 2.2
        self.SaberTooth_KpP = 250
        self.SaberTooth_KiP = 1
        self.SaberTooth_KdP = 20
        self.SaberTooth_KpA = 16
        self.SaberTooth_KiA = 1.7
        self.SaberTooth_KdA = -2
        self.PWM_KpP = 220
        self.PWM_KiP = 2
        self.PWM_KdP = 8
        self.PWM_KpA = 6
        self.PWM_KiA = 1.2
        self.PWM_KdA = -0.2
        self.limitP = 310 
        self.limitA = 310 
        self.integrated_error_P1 = 0
        self.integrated_error_P2 = 0
        self.integrated_error_A1 = 0
        self.integrated_error_A2 = 0
        self.last_error_P1 = 0
        self.last_error_P2 = 0
        self.last_error_A1 = 0
        self.last_error_A2 = 0
        self.mLiPo = 25.2951
        self.MinRedLiPo = 20
        self.AnalogPinLiPo = "P9_40"
        self.ajustFR = 0.0085
        self.ajustLR = 0.003
	self.encoder1 = eqep.eQEP("/sys/devices/ocp.3/48302000.epwmss/48302180.eqep", eqep.eQEP.MODE_ABSOLUTE)
	self.encoder2 = eqep.eQEP("/sys/devices/ocp.3/48304000.epwmss/48304180.eqep", eqep.eQEP.MODE_ABSOLUTE)
