#!/usr/bin/python

# Python Standart Library Imports
import subprocess
import os
import memcache

shared = memcache.Client([('localhost', 15)], debug=0)

class StartAndStopClass():

    def StartAndStopToWeb(self):
	if shared.get('MainRoutinePID')==None:
		return 0
	chk_sA = subprocess.Popen(['kill -0 '+shared.get('MainRoutinePID')+' > /dev/null 2>&1; echo $?'],stdout=subprocess.PIPE,shell=True)
        chk_sA.wait()
        sA_status = chk_sA.stdout.read()

       	if int(sA_status) != 0:
		return 0

