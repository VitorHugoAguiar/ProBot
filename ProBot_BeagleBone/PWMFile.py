#!/usr/bin/python

import time
import math
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM
import ProBotConstantsFile

Pconst = ProBotConstantsFile.Constants()

#PWM.start(channel, duty, freq, polarity)
PWM.start(Pconst.PWM_R_DIR, 50, Pconst.PWM_Freq)
PWM.start(Pconst.PWM_R_PWM, 0, Pconst.PWM_Freq) #pwm
PWM.start(Pconst.PWM_L_DIR, 50, Pconst.PWM_Freq)
PWM.start(Pconst.PWM_L_PWM, 0, Pconst.PWM_Freq) #pwm


class PWMClass ():
	
	def PWMStart(self):
    	    # Starting the communication with the PWM controller
            GPIO.output(Pconst.RedLED, GPIO.HIGH)

            time.sleep(3)									# Wait to stabilize the communication

	    GPIO.output(Pconst.RedLED, GPIO.LOW)
	    GPIO.output(Pconst.BlueLED, GPIO.HIGH)
	    
	def PWM_Signals(self, rightMotor, leftMotor):

	    # Sending the values to the PWM controller that is connected to the motors
	    percentageR=int(math.fabs(rightMotor))
	    percentageL=int(math.fabs(leftMotor))
	    #print int(percentageR), int(percentageL)
	    #print int(rightMotor), int(leftMotor)
	    
	    if rightMotor>0:
		PWM.set_duty_cycle(Pconst.PWM_R_DIR, 100)
		PWM.set_duty_cycle(Pconst.PWM_R_PWM, percentageR)
	    elif rightMotor<0:
		PWM.set_duty_cycle(Pconst.PWM_R_DIR,  0)
		PWM.set_duty_cycle(Pconst.PWM_R_PWM,  percentageR)
	    elif rightMotor==0:
		PWM.set_duty_cycle(Pconst.PWM_R_PWM, 0)
		
    	    if leftMotor>0:
	        PWM.set_duty_cycle(Pconst.PWM_L_DIR, 0)
	        PWM.set_duty_cycle(Pconst.PWM_L_PWM, percentageL)
	    elif leftMotor<0:
	    	PWM.set_duty_cycle(Pconst.PWM_L_DIR, 100)
      	    	PWM.set_duty_cycle(Pconst.PWM_L_PWM, percentageL)
    	    elif leftMotor==0:
	   	PWM.set_duty_cycle(Pconst.PWM_L_PWM, 0)

			
	def PWMStop(self):
	    	PWM.stop(Pconst.PWM_R_PWM)
		PWM.stop(Pconst.PWM_R_DIR)
		PWM.stop(Pconst.PWM_L_PWM)
		PWM.stop(Pconst.PWM_L_DIR)
		PWM.cleanup()
		
		
