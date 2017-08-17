#!/usr/bin/python

# Python Standart Library Imports
import subprocess
import os

# Local files
import SocketStartAndStop

# Initialization of classes from local files
Pub_Sub = SocketStartAndStop.SocketClass()

class StartAndStopClass():
			
    def StartAndStopToWeb(self):			
	with open(os.getcwd()+"/pidProBot.tmp","r") as f: 
               scriptA_pid = f.read()
        chk_sA = subprocess.Popen(['kill -0 '+str(scriptA_pid)+' > /dev/null 2>&1; echo $?'],stdout=subprocess.PIPE,shell=True)
        chk_sA.wait()
        sA_status = chk_sA.stdout.read()
			
       	if int(sA_status) != 0:	
		return 0
			
	
