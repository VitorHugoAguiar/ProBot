#!/usr/bin/python

# Global Constants
class Constants:
    def __init__(self):
	self.probotID = <ProBotID>
	self.broker = <Server IPAddress>
	self.baud = 38400
	self.addr = 128
	self.PWM_Freq = 20000
	self.PWM_L_DIR = "P9_14"
	self.PWM_L_PWM = "P9_22"
	self.PWM_R_DIR = "P9_42"
	self.PWM_R_PWM = "P8_13"
        self.RedLED = "P8_7"
        self.GreenLED = "P8_9"
	self.BlueLED = "P8_11"
        self.AnalogPinLiPo = "P9_40"

