#!/usr/bin/python

import threading
import BatteryMonitorFile
import SocketFile
import time
import ctypes

Battery = BatteryMonitorFile.BatteryMonitorClass()
Pub_Sub = SocketFile.SocketClass()

class SendMsgServerClass():

    def MsgServer (self, interval, worker_func, iterations = 0):
      if iterations != 1:
        threading.Timer (interval, self.MsgServer, [interval, worker_func, 0 if iterations == 0 else iterations-1]).start ()

      worker_func ()

    def sendMsgServer (self):
     	# Verification of the voltage from the Beaglebone and motors batteries
	thread = threading.Timer(1, self.sendMsgServer)
	thread.start() 
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

        
        
        
        
        
