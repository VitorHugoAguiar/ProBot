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
    thread=0
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
      GPIO.output(Pconst.GreenLED, GPIO.LOW)
      GPIO.output(Pconst.RedLED, GPIO.LOW)
      PWM.PWMStop()
      Sabertooth.stopAndReset()
      info="ProBot2_info" + " " + "off"
      publisher=Pub_Sub.publisher(info)
      userChoiceFile = open("userChoice.txt", "wb")
      userChoiceFile.write("0")
      userChoiceFile.close()
      if final==1:
          self.terminate_thread(self.thread)

		
    def MsgServer (self, interval, worker_func, iterations = 0):
      if iterations != 1:
        threading.Timer (interval, self.MsgServer, [interval, worker_func, 0 if iterations == 0 else iterations-1]).start ()

      worker_func ()

    def sendMsgServer (self):
     	# Verification of the voltage from the Beaglebone and motors batteries
	self.thread = threading.Timer(1, self.sendMsgServer)
	self.thread.start() 
	#t.join(1)
	batteryValue=str('{0:.2f}'.format(Battery.VoltageValue('LiPo')))
	info="ProBot2_info" + " " + batteryValue
        publisher=Pub_Sub.publisher(info)
        #self.terminate_thread(thread)

    def terminate_thread(self, thread):
    	"""Terminates a python thread from another thread.

    	:param thread: a threading.Thread instance
    	"""
    	
    	if not thread.isAlive():
    	    return

    	exc = ctypes.py_object(SystemExit)
    	res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
    	    ctypes.c_long(thread.ident), exc)
    	if res == 0:
    	    raise ValueError("nonexistent thread id")
    	elif res > 1:
    	    # """if it returns a number greater than one, you're in trouble,
      	  # and you should call it again with exc=NULL to revert the effect"""
        	ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        	raise SystemError("PyThreadState_SetAsyncExc failed")
