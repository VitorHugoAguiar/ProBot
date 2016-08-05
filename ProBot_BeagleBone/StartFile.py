#!/usr/bin/python
import Adafruit_BBIO.GPIO as GPIO
import sys
import threading
import ctypes
import ProBotConstantsFile
import SocketFile
import PWMFile
import SabertoothFile
import BatteryMonitorFile

Sabertooth = SabertoothFile.SabertoothClass()
PWM = PWMFile.PWMClass()
Pconst = ProBotConstantsFile.Constants()
Pub_Sub = SocketFile.SocketClass()
Battery = BatteryMonitorFile.BatteryMonitorClass()


class StartFileClass():

    def StartProgram(self):
      try:
        if len(sys.argv) >= 2:
          userChoice=sys.argv[1]
	  userChoiceFile = open("userChoice.txt", "wb")
	  userChoiceFile.write(userChoice);
	  userChoiceFile.close()
	
  
        # We create a file to store the userChoice (Sabertooth or PWM)
        userChoiceFile = open("userChoice.txt", "r+")
        userChoice = userChoiceFile.read(1);
        # Close opend file
        userChoiceFile.close()

        if userChoice=='0':
	  print ('\nChoose the type of control of the ProBots motors:')
	  print ('\n1 - Sabertooth 2x25A')
	  print ('2 - PWM Controller OSMC3-2')
	  userChoice=input('\nYour choice is: ')
	  userChoice=str(userChoice)

	  userChoiceFile = open("userChoice.txt", "wb")
	  userChoiceFile.write(userChoice);
	  userChoiceFile.close()
		
        if userChoice=='1':
	  print "\nSending commands to the address", Pconst.addr, "with a baudrate of\n", Pconst.baud

        if userChoice=='2':
	  print "\nSending a PWM signal with a frequency of", Pconst.PWM_Freq, "Hz"
		
        return userChoice
      except:
        print("Unexpected error:\n", sys.exc_info()[0])
        sys.exit('\n\nPROGRAM STOPPED!!!\n')
        raise
		
    def StopProgram(self, final):
      #GPIO.output(Pconst.GreenLED, GPIO.HIGH)
      #GPIO.output(Pconst.RedLED, GPIO.HIGH)
      PWM.PWMStop()
      Sabertooth.stopAndReset()
      userChoiceFile = open("userChoice.txt", "wb")
      userChoiceFile.write("0")
      userChoiceFile.close()

