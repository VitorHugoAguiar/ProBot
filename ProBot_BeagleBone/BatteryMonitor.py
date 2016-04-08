#!/usr/bin/python

# Python Standart Library Imports
import Adafruit_BBIO.ADC as ADC
import ProBotConstants

# Initialization of classes from local files
Pconst = ProBotConstants.Constants()

# Start the ADC
ADC.setup()

# Battery measurement
class BatteryVoltage():

        def VoltageValue(self, type):
            # Reading from the LiPo battery
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
