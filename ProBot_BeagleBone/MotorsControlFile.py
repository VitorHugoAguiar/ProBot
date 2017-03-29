#!/usr/bin/python
 
# Python Standart Library Imports
import SabertoothFile
import PWMFile
import ProBotConstantsFile

# Initialization of classes from local files
Sabertooth = SabertoothFile.SabertoothClass()
PWM = PWMFile.PWMClass()
Pconst = ProBotConstantsFile.Constants()


class MotorsControlClass():
    
    def MotorsControl(self,rightMotor, leftMotor, userChoice):
	if userChoice=='1':
		# Sending the values to the Sabertooth that is connected to the motors
		Sabertooth.drive(Pconst.addr, 1, int(rightMotor))
	        Sabertooth.drive(Pconst.addr, 2, int(leftMotor))

	if userChoice=='2':
		# Sending the values to the pwm controller that is connected to the motors
		PWM.PWM_Signals(round(rightMotor, 2), round(leftMotor, 2))
