#!/usr/bin/python
import Adafruit_BBIO.GPIO as GPIO
import sys
import PWMFile
import SabertoothFile
import SocketFile
import ProBotConstantsFile

Sabertooth = SabertoothFile.SabertoothClass()
PWM = PWMFile.PWMClass()
Pconst = ProBotConstantsFile.Constants()
Pub_Sub = SocketFile.SocketClass()

GPIO.output(Pconst.GreenLED, GPIO.LOW)
GPIO.output(Pconst.RedLED, GPIO.LOW)
GPIO.output(Pconst.BlueLED, GPIO.LOW)
PWM.PWMStop()
Sabertooth.stopAndReset()
userChoiceFile = open("userChoice.txt", "wb")
userChoiceFile.write("0")
userChoiceFile.close()
