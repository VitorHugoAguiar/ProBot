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

        def VoltageValue(self, type):
	            
            	# Reading the voltage from the LiPo battery
		options = {'LiPo': [Pconst.AnalogPinLiPo, Pconst.mLiPo, Pconst.MinRedLiPo, Pconst.GreenLED, Pconst.RedLED]}
            	voltageVar = options[type]
		while True:
            		try:	
				BatteryVoltageVal = ADC.read(voltageVar[0])                                 # ADC readings from the battery
				
				BatteryRealValue=BatteryVoltageVal*1.8
				BatteryRealValue=BatteryRealValue*(107200/7200)
				BatteryPercentage=int((14.2857*BatteryRealValue)-265.714)
								
            			if BatteryPercentage < voltageVar[2]:					        			# Definition of the Red region for the battery
                			GPIO.output(voltageVar[3], GPIO.HIGH)
                			GPIO.output(voltageVar[4], GPIO.HIGH)
	    			else:

					GPIO.output(voltageVar[4], GPIO.LOW)
											
				publisher=Pub_Sub2.publisher(BatteryPercentage)
				print BatteryPercentage
				
            			
               		except OSError as err:
    				print("OS error: {0}".format(err))
	    		except ValueError:
    				print("Could not convert data to an integer.")			
            		except:
				print("Unexpected error:\n", sys.exc_info()[0])
				sys.exit('\n\nBattery readings stopped!!!\n')
				raise
    	def main(self):
		BatteryMonitorClass.VoltageValue('LiPo')
            
if __name__ == '__main__':
    BatteryMonitorClass = BatteryMonitorClass()
    BatteryMonitorClass.main()
