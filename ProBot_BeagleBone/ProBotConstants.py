#!/usr/bin/python

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
        self.SaberTooth_KpV = 280
        self.SaberTooth_KiV = 0.6
        self.SaberTooth_KdV = 12
        self.SaberTooth_KpA = 18
        self.SaberTooth_KiA = 2.2
        self.SaberTooth_KdA = -2
        self.PWM_KpV = 0
        self.PWM_KiV = 0
        self.PWM_KdV = 0
        self.PWM_KpA = 0
        self.PWM_KiA = 0
        self.PWM_KdA = 0
        self.limitV = 310 
        self.limitA = 310 
        self.integrated_error_V1 = 0
        self.integrated_error_V2 = 0
        self.integrated_error_A1 = 0
        self.integrated_error_A2 = 0
        self.last_error_V1 = 0
        self.last_error_V2 = 0
        self.last_error_A1 = 0
        self.last_error_A2 = 0
        self.mLiPo = 25.2951
        self.MinRedLiPo = 20
        self.AnalogPinLiPo = "P9_40"
        self.ajustFR = 0.0085
        self.ajustLR = 0.005



