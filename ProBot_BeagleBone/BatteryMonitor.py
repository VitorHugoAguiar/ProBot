#!/usr/bin/python

# Python Standart Library Imports
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import ProBotConstants

# Initialization of classes from local files
Pconst = ProBotConstants.Constants()

# Start the ADC
ADC.setup()

# Definition of the GPIO's
GPIO.setup(Pconst.RedLED, GPIO.OUT)
GPIO.setup(Pconst.GreenLED, GPIO.OUT)

# Battery measurement
class BatteryVoltage():

        def VoltageValue(self, type):
            # Readings from the BeagleBone and Motors batteries
            options = {'LiPo': [Pconst.AnalogPinLiPo, Pconst.mLiPo, Pconst.MinRedLiPo, Pconst.GreenLED, Pconst.RedLED]}
            voltageVar = options[type]

            BatteryVoltageVal = ADC.read(voltageVar[0])                                         # Readings from the ADC battery
            BatteryRealValue = float((voltageVar[1]*BatteryVoltageVal))          		# Real voltage from the LiPo battery
	    
            if BatteryRealValue < voltageVar[2]:					        # Definition of the Red region for the battery
                GPIO.output(voltageVar[3], GPIO.HIGH)
                GPIO.output(voltageVar[4], GPIO.HIGH)
	    else:
		GPIO.output(voltageVar[4], GPIO.LOW)

            return BatteryRealValue
