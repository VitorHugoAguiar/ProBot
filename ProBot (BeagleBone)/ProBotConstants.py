#!/usr/bin/python

# Constants used in the algorithm
class Constants():
    def __init__(self):
        self.AccXangleAverage = -0.43432634994							# Calibration of the MPU6050
        self.GYRxAverage = -65
        self.RedLED = "P8_13"
        self.GreenLED = "P9_27"
        self.KpP = 0
        self.KiP = 0
        self.KdP = 0
        self.KpV = 10
        self.KiV = 0.3
        self.KdV = 1
        self.KpA = 10
        self.KiA = 0.75
        self.KdA = -0.3
        self.limitV = 1000
        self.limitP = 310
        self.limitA = 310
        self.integrated_error_P = 0
        self.integrated_error_V = 0
        self.integrated_error_A = 0
        self.integrated_error_VA = 0
        self.last_error_P = 0
        self.last_error_V = 0
        self.last_error_A = 0
        self.last_error_VA = 0
        self.mBeagle = 13.01256
        self.bBeagle = 0
        self.MinRedBeagle = 10.5
        self.GreenBatteryBeagle = "P9_15"
        self.RedBatteryBeagle = "P9_23"
        self.AnalogPinBeagle = "P9_38"
        self.mMotors = -27.036
        self.bMotors = 27.04
        self.MinRedMotors = 20
        self.GreenBatteryMotors = "P8_18"
        self.RedBatteryMotors = "P8_14"
        self.AnalogPinMotors = "P9_40"
        self.tenths = 0.1
        self.hundredths=0.01
        self.thousandths=0.001
