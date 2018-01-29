#!/usr/bin/python

# Python Standard Library Imports
import time
import math
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

# Local files
import ProBotConstantsFile
#import LowPassFilter2

# Initialization of classes from local files
Pconst = ProBotConstantsFile.Constants()
#LPF = LowPassFilter2.LowPassFilter()

# Start the GPIO's
GPIO.setup(Pconst.RedLED, GPIO.OUT)
GPIO.setup(Pconst.BlueLED, GPIO.OUT)

#PWM.start(channel, duty, freq, polarity)
PWM.start(Pconst.PWM_R_DIR, 50, Pconst.PWM_Freq)
PWM.start(Pconst.PWM_R_PWM, 0, Pconst.PWM_Freq) #pwm
PWM.start(Pconst.PWM_L_DIR, 50, Pconst.PWM_Freq)
PWM.start(Pconst.PWM_L_PWM, 0, Pconst.PWM_Freq) #pwm

class PWMClass ():
	
	def PWMStart(self):
    	    # Starting the communication with the PWM controller
            GPIO.output(Pconst.RedLED, GPIO.HIGH)
            time.sleep(3)						# Wait to stabilize the communication
	    
	def PWM_Signals(self, rightMotor, leftMotor):
	    # Sending the values to the PWM controller that is connected to the motors
	    percentageR=abs(rightMotor)
	    percentageL=abs(leftMotor)
	    	    
	    if rightMotor>0:
		PWM.set_duty_cycle(Pconst.PWM_R_DIR, 100)
		PWM.set_duty_cycle(Pconst.PWM_R_PWM, percentageR)

    	    elif rightMotor<0:
                PWM.set_duty_cycle(Pconst.PWM_R_DIR, 0)
		PWM.set_duty_cycle(Pconst.PWM_R_PWM, percentageR)

	    elif rightMotor==0:
                PWM.set_duty_cycle(Pconst.PWM_R_PWM, 0)

    	    if leftMotor>0:
                PWM.set_duty_cycle(Pconst.PWM_L_DIR, 0)
	       	PWM.set_duty_cycle(Pconst.PWM_L_PWM, percentageL)
		#time.sleep(timeSleep)
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
		
		
