#!/usr/bin/python

# Python Standard Library Imports
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO

# Start the ADC
ADC.setup()

# Pin assigment for the Beaglebone battery
GreenBattery = "P9_15"
YellowBattery = "P9_12"
RedBattery = "P9_23"
AnalogPin = "P9_38"
# Pin assigment for the motors battery
GreenBattery2 = "P8_18"
RedBattery2= "P8_14"
AnalogPin2 = "P9_40"

# Definition of the GPIO's
GPIO.setup(GreenBattery, GPIO.OUT)
GPIO.setup(YellowBattery, GPIO.OUT)
GPIO.setup(RedBattery, GPIO.OUT)
GPIO.setup(GreenBattery2, GPIO.OUT)
GPIO.setup(RedBattery2, GPIO.OUT)

# Battery measurement
# We need to evaluate the voltage of the batteries to avoid damaging it
# We are using 12V batteries, one for the Beaglebone and two in series for the motors (for now)
class BatteryVoltage():
	def BatteryVoltageBeaglebone(self):
		BatteryVoltageVal = ADC.read(AnalogPin)
		BatteryRealValue = float(13.01256*BatteryVoltageVal)						# Real voltage from the BeagleBone battery

		if BatteryRealValue < 10.5:													# Define Red region, under 10,5V
			GPIO.output(GreenBattery, GPIO.LOW)
			GPIO.output(YellowBattery, GPIO.LOW)
			GPIO.output(RedBattery, GPIO.HIGH)
			
		if BatteryRealValue > 10.5 and BatteryRealValue < 12:						# Define Yellow region, between 10,5 and 12V
			GPIO.output(GreenBattery, GPIO.LOW)
			GPIO.output(YellowBattery, GPIO.HIGH)
			GPIO.output(RedBattery, GPIO.LOW)	
	
		if BatteryRealValue > 12:													# Define the green region, over 12V
			GPIO.output(GreenBattery, GPIO.HIGH)
			GPIO.output(YellowBattery, GPIO.LOW)
			GPIO.output(RedBattery, GPIO.LOW)

		return BatteryRealValue
		
	def BatteryVoltageMotors(self):
		BatteryVoltageVal2 = ADC.read(AnalogPin2)*1.8
		BatteryRealValue2 = float((-15.02*BatteryVoltageVal2)+27.04)				# Real voltage from the motors batteries

		if BatteryRealValue2 < 18:													# Define Red region, under 18V	
			GPIO.output(GreenBattery2, GPIO.LOW)
			GPIO.output(RedBattery2, GPIO.HIGH)
			
		else:																		# Define the green region, over 18V
			GPIO.output(GreenBattery2, GPIO.HIGH)
			GPIO.output(RedBattery2, GPIO.LOW)

		return BatteryRealValue2
