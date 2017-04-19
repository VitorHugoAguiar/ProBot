#!/usr/bin/python

# Python Standart Library Imports
import SocketStartAndStop
import SocketStartAndStop2
import SocketStartAndStop3
import subprocess
import sys
import os

Pub_Sub4 = SocketStartAndStop.SocketClass()
Pub_Sub5 = SocketStartAndStop2.SocketClass()
Pub_Sub6 = SocketStartAndStop3.SocketClass()

class StartAndStopClass():

    def __init__(self, StartAndStopMsg=0, OnlyOnce=0):
        self.StartAndStopMsg = StartAndStopMsg
	self.OnlyOnce=OnlyOnce
    def StartAndStop_Value(self):
	while True:
        	subscriber = Pub_Sub4.subscriber() # Readings from the WebPage
		if subscriber is None:
			self.StartAndStopMsg=0
		
        	else:
			incomingMsg1 = subscriber.replace("[", "")
	    		incomingMsg2 = incomingMsg1.replace("'", "")
	    		incomingMsg3 = incomingMsg2.replace("]", "") 
                        incomingMsg4 = incomingMsg3.replace(" ", "")
	    		self.StartAndStopMsg = incomingMsg4.replace(",", "") 		
			if self.StartAndStopMsg[0]!="s":
				self.StartAndStopMsg=0			
		print (self.StartAndStopMsg)
		
        	with open("/home/machinekit/ProBot/ProBot_BeagleBone/pidProBot.tmp","r") as f:
                	scriptA_pid = f.read()
        	chk_sA = subprocess.Popen(['kill -0 '+str(scriptA_pid)+' > /dev/null 2>&1; echo $?'],stdout=subprocess.PIPE,shell=True)
        	chk_sA.wait()
        	sA_status = chk_sA.stdout.read()

        	if int(sA_status) == 0:
                	print("Running")
                	publisher5=Pub_Sub5.publisher("start")
                	if self.StartAndStopMsg=="stop":
                        	publisher6=Pub_Sub6.publisher("stop")
				self.OnlyOnce=0
        	else:
                	print("Not running")
			publisher5=Pub_Sub5.publisher("stopped")
			if self.OnlyOnce==0:
                		if self.StartAndStopMsg=="start":
                        		subprocess.Popen(['python /home/machinekit/ProBot/ProBot_BeagleBone/ProBot.py 2'],stdout = subprocess.PIPE,stderr = subprocess.PIPE,shell=True)
					self.OnlyOnce=1



if __name__ == '__main__':
    StartAndStopClass = StartAndStopClass()
    StartAndStopClass.StartAndStop_Value()

