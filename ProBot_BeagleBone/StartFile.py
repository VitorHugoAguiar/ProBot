#!/usr/bin/python

import sys
import ProBotConstantsFile
import PWMFile
import SabertoothFile
import Adafruit_BBIO.GPIO as GPIO

Sabertooth = SabertoothFile.SabertoothClass()
PWM = PWMFile.PWMClass()
Pconst = ProBotConstantsFile.Constants()

# Configuration the type of GPIO's
GPIO.setup(Pconst.RedLED, GPIO.OUT)
GPIO.setup(Pconst.GreenLED, GPIO.OUT)
GPIO.setup(Pconst.BlueLED, GPIO.OUT)


class StartFileClass():

    def StartProgram(self):
      try:
        if len(sys.argv) >= 2:
          userChoice=sys.argv[1]
	  if  ((userChoice!="1") and (userChoice!="2")):
		print ("\nOption not available. Try again with 'python ProBot.py 1 (or 2)' or 'python ProBot.py 1 (or 2) manual'\n")
		sys.exit(1)
                raise
		
		
	  userChoiceFile = open("userChoice.txt", "wb")
	  userChoiceFile.write(userChoice);
	  userChoiceFile.close()
	  if len(sys.argv) == 3:
          	if  sys.argv[2]!="manual":
                	print ("\nOption not available. Try again with 'python ProBot.py 1 (or 2)' or 'python ProBot.py 1 (or 2) manual'\n")
			sys.exit(1)
	               	raise
			
	  	else:
			StartAndStop="1"

	  	StartAndStopFile = open("StartAndStop.txt", "wb")
          	StartAndStopFile.write(StartAndStop);
          	StartAndStopFile.close()
	
	  
        # We create a file to store the userChoice (Sabertooth or PWM)
        userChoiceFile = open("userChoice.txt", "r+")
        userChoice = userChoiceFile.read(1);
        # Close opend file
        userChoiceFile.close()

        if userChoice=='0':
	  print ('\nChoose the type of control of the ProBots motors:')
	  print ('\n1 - Sabertooth 2x25A')
	  print ('2 - Cytron 5-25V')
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
		
    def StopProgram(self):
      PWM.PWMStop()
      Sabertooth.stopAndReset()
      GPIO.output(Pconst.GreenLED, GPIO.LOW)
      GPIO.output(Pconst.RedLED, GPIO.LOW)
      GPIO.output(Pconst.BlueLED, GPIO.LOW)
      userChoiceFile = open("userChoice.txt", "wb")
      userChoiceFile.write("0")
      userChoiceFile.close()

      StartAndStopFile = open("StartAndStop.txt", "wb")
      StartAndStopFile.write("0");
      StartAndStopFile.close()

