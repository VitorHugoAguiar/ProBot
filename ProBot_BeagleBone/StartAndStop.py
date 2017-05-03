#!/usr/bin/python

# Python Standart Library Imports
#import SocketStartAndStop2
import subprocess
import SocketStartAndStop

Pub_Sub = SocketStartAndStop.SocketClass()

class StartAndStopClass():
			
    def StartAndStopToWeb(self):			
	with open("/home/machinekit/ProBot/ProBot_BeagleBone/pidProBot.tmp","r") as f:
               scriptA_pid = f.read()
        chk_sA = subprocess.Popen(['kill -0 '+str(scriptA_pid)+' > /dev/null 2>&1; echo $?'],stdout=subprocess.PIPE,shell=True)
        chk_sA.wait()
        sA_status = chk_sA.stdout.read()
			
       	if int(sA_status) != 0:	
		return 0
			
	
