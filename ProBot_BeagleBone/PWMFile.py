#!/usr/bin/python

import time
import math
import sys
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import ProBotConstantsFile

Pconst = ProBotConstantsFile.Constants()

#PWM.start(channel, duty, freq, polarity)
PWM.start(Pconst.PWM_RR, 50, Pconst.PWM_Freq)
PWM.start(Pconst.PWM_RF, 100, Pconst.PWM_Freq) #pwm
PWM.start(Pconst.PWM_LR, 50, Pconst.PWM_Freq)
PWM.start(Pconst.PWM_LF, 100, Pconst.PWM_Freq) #pwm


class PWMClass ():
	
	def PWMStart(self):
    	    try:
		import StartFile
	    	InitProgram=StartFile.StartFileClass()

	    	# Starting the communication with the PWM controller
            	GPIO.output(Pconst.RedLED, GPIO.HIGH)

            	time.sleep(3)									# Wait to stabilize the communication

	    	GPIO.output(Pconst.RedLED, GPIO.LOW)
	    	GPIO.output(Pconst.BlueLED, GPIO.HIGH)
	    except:
            	InitProgram.StopProgram()
            	print("Unexpected error:\n", sys.exc_info()[0])
            	sys.exit('\n\nPROGRAM STOPPED!!!\n')
            	raise

	def PWM_Signals(self, rightMotor, leftMotor):

	    # Sending the values to the PWM controller that is connected to the motors
	    percentageR=int(math.fabs(rightMotor))
	    percentageL=int(math.fabs(leftMotor))
	    #print int(percentageR), int(percentageL)
	    #print int(rightMotor), int(leftMotor)
	    
	    if rightMotor>0:
		PWM.set_duty_cycle(Pconst.PWM_RR,  0)
		PWM.set_duty_cycle(Pconst.PWM_RF, percentageR)
	    elif rightMotor<0:
		PWM.set_duty_cycle(Pconst.PWM_RR,  100)
		PWM.set_duty_cycle(Pconst.PWM_RF,  percentageR)
	    elif rightMotor==0:
		PWM.set_duty_cycle(Pconst.PWM_RF, 0)
		
    	    if leftMotor>0:
	        PWM.set_duty_cycle(Pconst.PWM_LR, 100)
	        PWM.set_duty_cycle(Pconst.PWM_LF, percentageL)
	    elif leftMotor<0:
	    	PWM.set_duty_cycle(Pconst.PWM_LR, 0)
		PWM.set_duty_cycle(Pconst.PWM_LF, percentageL)
    	    elif leftMotor==0:
		PWM.set_duty_cycle(Pconst.PWM_LF, 0)

			
	def PWMStop(self):
	    	PWM.stop(Pconst.PWM_RF)
		PWM.stop(Pconst.PWM_RR)
		PWM.stop(Pconst.PWM_LF)
		PWM.stop(Pconst.PWM_LR)
		PWM.cleanup()
		
		
