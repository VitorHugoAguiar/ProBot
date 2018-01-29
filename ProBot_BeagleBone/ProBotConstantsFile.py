#!/usr/bin/python
import eqep

# Constants
class Constants:
    def __init__(self):
	self.probotID = '1'
	self.broker = '89.109.64.175'
	self.baud = 38400
	self.addr = 128
	self.PWM_Freq = 20000
	self.PWM_L_DIR = "P9_14"
	self.PWM_L_PWM = "P9_22"
	self.PWM_R_DIR = "P9_42"
	self.PWM_R_PWM = "P8_13"
        self.ticks = 10000
        self.wheelDiameter = 0.25
        self.RedLED = "P8_7"
        self.GreenLED = "P8_9"
	self.BlueLED = "P8_11"
	self.rad_to_deg = 57.29578
	self.Angle_offset = 2
	self.GYR_offset = 4.5
        self.SaberTooth_KpV = 280
        self.SaberTooth_KiV = 0.6
        self.SaberTooth_KdV = 12
        self.SaberTooth_KpA = 18
        self.SaberTooth_KiA = 2.2
        self.SaberTooth_KdA = -2
        self.PWM_KpV = 75 
        self.PWM_KiV = 0.6 
        self.PWM_KdV = 200 
        self.PWM_KpA = 6 
        self.PWM_KiA = 1.7 
        self.PWM_KdA = -0.001
	self.limitV = 800
        self.limitA = 1000 
        self.integrated_error_V1 = 0
        self.integrated_error_V2 = 0
        self.integrated_error_A1 = 0
        self.integrated_error_A2 = 0
        self.last_error_V1 = 0
        self.last_error_V2 = 0
        self.last_error_A1 = 0
        self.last_error_A2 = 0
        self.MinRedLiPo = 20
        self.AnalogPinLiPo = "P9_40"
        self.ajustFR = 0.018 #0.02 #0.015
        self.ajustLR = 0.007
	self.encoder1 = eqep.eQEP("/sys/devices/platform/ocp/48302000.epwmss/48302180.eqep", eqep.eQEP.MODE_ABSOLUTE)
	self.encoder2 = eqep.eQEP("/sys/devices/platform/ocp/48304000.epwmss/48304180.eqep", eqep.eQEP.MODE_ABSOLUTE)
