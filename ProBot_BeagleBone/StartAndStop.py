#!/usr/bin/python

# Python Standart Library Imports
import SocketStartAndStop
import SocketStartAndStop2
import subprocess
import sys
import os
import signal
import threading
import multiprocessing

Pub_Sub = SocketStartAndStop.SocketClass()
Pub_Sub2 = SocketStartAndStop2.SocketClass()

class StartAndStopClass():

    def __init__(self, StartAndStopMsg=0, OnlyOnce=0):
        self.StartAndStopMsg = StartAndStopMsg
	self.OnlyOnce=OnlyOnce

    def startThread(self):
	subprocess.Popen(['python /home/machinekit/ProBot/ProBot_BeagleBone/ProBot.py 2'], stdout = subprocess.PIPE, stderr = subprocess.PIPE, shell=True, preexec_fn=os.setpgrp, close_fds=True)
	return

    def StartAndStop_Value(self):
		
        	subscriber = Pub_Sub.subscriber() # Readings from the WebPage
		if subscriber is None:
			self.StartAndStopMsg=0
		
        	else:
			incomingMsg1 = subscriber.replace("[", "")
	    		incomingMsg2 = incomingMsg1.replace("'", "")
	    		incomingMsg3 = incomingMsg2.replace("]", "") 
                        incomingMsg4 = incomingMsg3.replace(" ", "")
	    		self.StartAndStopMsg = incomingMsg4.replace(",", "") 		
			
		
        	with open("/home/machinekit/ProBot/ProBot_BeagleBone/pidProBot.tmp","r") as f:
                	scriptA_pid = f.read()
        	chk_sA = subprocess.Popen(['kill -0 '+str(scriptA_pid)+' > /dev/null 2>&1; echo $?'],stdout=subprocess.PIPE,shell=True) 
		chk_sA.wait()
        	sA_status = chk_sA.stdout.read()

        	if int(sA_status) == 0:
                	#Running
                	if self.StartAndStopMsg=="stop":
                        	publisher2=Pub_Sub2.publisher("stop")
				self.OnlyOnce=0
			return "start"
        	else:
                	#Not running
			if self.OnlyOnce==0:
                		if self.StartAndStopMsg=="start":
					multiprocessing.Process(target=self.startThread).start()   			
					self.OnlyOnce=1
			return "stopped"
			
