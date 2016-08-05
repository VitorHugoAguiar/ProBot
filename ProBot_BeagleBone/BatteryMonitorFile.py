#!/usr/bin/python

# Python Standart Library Imports
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import ProBotConstantsFile

# Initialization of classes from local files
Pconst = ProBotConstantsFile.Constants()

# Start the ADC
ADC.setup()

GPIO.setup(Pconst.GreenLED, GPIO.OUT)
GPIO.setup(Pconst.RedLED, GPIO.OUT)

# Battery measurement
class BatteryMonitorClass():

        def VoltageValue(self, type):
            
            # Reading the voltage from the LiPo battery
            options = {'LiPo': [Pconst.AnalogPinLiPo, Pconst.mLiPo, Pconst.MinRedLiPo, Pconst.GreenLED, Pconst.RedLED]}
            voltageVar = options[type]

            BatteryVoltageVal = ADC.read(voltageVar[0])                                         # ADC readings from the battery
            BatteryRealValue = float((voltageVar[1]*BatteryVoltageVal))          		# Real voltage from the LiPo battery
	    
            if BatteryRealValue < voltageVar[2]:					        # Definition of the Red region for the battery
                GPIO.output(voltageVar[3], GPIO.HIGH)
                GPIO.output(voltageVar[4], GPIO.HIGH)
	    else:
		GPIO.output(voltageVar[4], GPIO.LOW)

            return BatteryRealValue
