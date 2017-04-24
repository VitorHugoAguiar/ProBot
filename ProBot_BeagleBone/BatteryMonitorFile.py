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
				BatteryVoltage = (1.8 * ADC.read(Pconst.AnalogPinLiPo) * (100 + 7.620)/7.620) + 0.5       # Vout = 1.8 * Vin * (R1+R2/R2) + (adjust value because of the resistor tolerance) 
							
            			if BatteryVoltage < Pconst.MinRedLiPo:					        	  # Definition of the Red region for the battery
                			GPIO.output(Pconst.GreenLED, GPIO.HIGH)
                			GPIO.output(Pconst.RedLED, GPIO.HIGH)
	    			else:

					GPIO.output(Pconst.RedLED, GPIO.LOW)
					

				print round(BatteryVoltage, 2)											
				publisher=Pub_Sub2.publisher(int(round(BatteryVoltage, 0)))

            		except:
				print("Unexpected error:\n", sys.exc_info()[0])
				sys.exit('\n\nBattery readings STOPPED!!!\n')
				raise

if __name__ == '__main__':
    BatteryMonitorClass = BatteryMonitorClass()
    BatteryMonitorClass.VoltageValue()
