#!/usr/bin/python

# Python Standard Library Imports
import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO

# Start the ADC
ADC.setup()

# Pin assigment
GreenBattery="P9_15"
YellowBattery="P9_12"
RedBattery="P9_23"
AnalogPin="P9_38"

# Pin setup
GPIO.setup(GreenBattery, GPIO.OUT)
GPIO.setup(YellowBattery, GPIO.OUT)
GPIO.setup(RedBattery, GPIO.OUT)

# Battery measurement
# We need to evaluate the voltage of the battery to avoid damaging it
# The battery used is a 12V nominal voltage, so the margin for voltage measurement is up to 13V
class BatteryValue():
	def BatteryVoltage(self):
		BatteryVoltageVal=ADC.read(AnalogPin)
		BatteryVoltageVolt=float (BatteryVoltageVal*1.8)		# ADC voltage measured
		BatteryRealValue=float (7.2292*BatteryVoltageVolt)		# Real Voltage

		if BatteryRealValue<10.5:											# Define Red region, under 10,5V
			GPIO.output(GreenBattery, GPIO.LOW)
			GPIO.output(YellowBattery, GPIO.LOW)
			GPIO.output(RedBattery, GPIO.HIGH)
	
		if BatteryRealValue>10.5 and BatteryRealValue<12:		# Define Yellow region, between 10,5 and 12V
			GPIO.output(GreenBattery, GPIO.LOW)
			GPIO.output(YellowBattery, GPIO.HIGH)
			GPIO.output(RedBattery, GPIO.LOW)	
	
		if BatteryRealValue>12:												# Define the green region, over 12V
			GPIO.output(GreenBattery, GPIO.HIGH)
			GPIO.output(YellowBattery, GPIO.LOW)
			GPIO.output(RedBattery, GPIO.LOW)

		return BatteryRealValue
