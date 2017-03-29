#!/usr/bin/python

# Python Standart Library Imports
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import ProBotConstantsFile
import time
import SocketBatteryFile
import sys

# Initialization of classes from local files
Pconst = ProBotConstantsFile.Constants()
Pub_Sub2 = SocketBatteryFile.SocketClass()

# Start the ADC
ADC.setup()

# Start the GPIO's
GPIO.setup(Pconst.GreenLED, GPIO.OUT)
GPIO.setup(Pconst.RedLED, GPIO.OUT)


class BatteryMonitorClass():

        def VoltageValue(self):
	            
            	# Reading the voltage from the LiPo battery
		while True:
            		try:	
				BatteryVoltageVal = ADC.read(Pconst.AnalogPinLiPo)                                 # ADC readings from the battery
				BatteryRealValue=(BatteryVoltageVal*1.8)*(107200/7200)
				BatteryPercentage=int((14.2857*BatteryRealValue)-265.714)
								
            			if BatteryPercentage < Pconst.MinRedLiPo:					        			# Definition of the Red region for the battery
                			GPIO.output(Pconst.GreenLED, GPIO.HIGH)
                			GPIO.output(Pconst.RedLED, GPIO.HIGH)
	    			else:

					GPIO.output(Pconst.RedLED, GPIO.LOW)
					
				print BatteryPercentage											
				publisher=Pub_Sub2.publisher(BatteryPercentage)

							
            		except:
				print("Unexpected error:\n", sys.exc_info()[0])
				sys.exit('\n\nBattery readings STOPPED!!!\n')
				raise

if __name__ == '__main__':
    BatteryMonitorClass = BatteryMonitorClass()
    BatteryMonitorClass.VoltageValue()
