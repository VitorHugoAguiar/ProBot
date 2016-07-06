#!/usr/bin/python

import time
import math
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import ProBotConstantsFile

Pconst = ProBotConstantsFile.Constants()

#PWM.start(channel, duty, freq, polarity)
PWM.start(Pconst.PWM_RF, 0, Pconst.PWM_Freq, 0)
PWM.start(Pconst.PWM_RR, 0, Pconst.PWM_Freq, 0)
PWM.start(Pconst.PWM_LF, 0, Pconst.PWM_Freq, 0)
PWM.start(Pconst.PWM_LR, 0, Pconst.PWM_Freq, 0)


class PWMClass ():
	
	def PWMStart(self):
    	    # Starting the communication with the PWM controller
            GPIO.output(Pconst.RedLED, GPIO.HIGH)

            time.sleep(3)									# Wait to stabilize the communication

	    GPIO.output(Pconst.RedLED, GPIO.LOW)
	    GPIO.output(Pconst.BlueLED, GPIO.HIGH)
	    
	def PWM_Signals(self, rightMotor, leftMotor):

	    # Sending the values to the PWM controller that is connected to the motors
	    percentageR=math.fabs(rightMotor)
	    percentageL=math.fabs(leftMotor)

    	    if rightMotor>0:
	 	PWM.set_duty_cycle(Pconst.PWM_RF, 0)
		PWM.set_duty_cycle(Pconst.PWM_RR, percentageR)
    	    elif rightMotor<0:
		PWM.set_duty_cycle(Pconst.PWM_RF, percentageR)
		PWM.set_duty_cycle(Pconst.PWM_RR, 0)
    	    elif rightMotor==0:
		PWM.set_duty_cycle(Pconst.PWM_RF, 0)
		PWM.set_duty_cycle(Pconst.PWM_RR, 0)

    	    if leftMotor>0:
		PWM.set_duty_cycle(Pconst.PWM_LF, 0)
		PWM.set_duty_cycle(Pconst.PWM_LR, percentageL)
    	    elif leftMotor<0:
		PWM.set_duty_cycle(Pconst.PWM_LF, percentageL)
		PWM.set_duty_cycle(Pconst.PWM_LR, 0)
    	    elif leftMotor==0:
		PWM.set_duty_cycle(Pconst.PWM_LF, 0)
		PWM.set_duty_cycle(Pconst.PWM_LR, 0)
			
	def PWMStop(self):
	    	PWM.stop(Pconst.PWM_RF)
		PWM.stop(Pconst.PWM_RR)
		PWM.stop(Pconst.PWM_LF)
		PWM.stop(Pconst.PWM_LR)
		PWM.cleanup()
		
		
