#!/usr/bin/python
import sys
import os
import zmq
import SocketCommunication

# Initialization of classes from local files
Pub_Sub = SocketCommunication.publisher_and_subscriber()

class Restart():
    def RestartProgram (self):
	while True:
		# Checking if the program needs to restart
		restartVar = Pub_Sub.subscriber2()
		if restartVar is None:
    			restartVar = 0
			userChoice = '0'
			userChoice1 = '0'
		else:
    			userChoice, userChoice1 = restartVar.split()
    			# Sending the previous value of the user's choices to the ProBot.py file
			if userChoice=='0':
				python = sys.executable
    				os.execl(python, python, * sys.argv)
			publisher2=Pub_Sub.publisher2(userChoice, userChoice1)

if __name__ == '__main__':
	Restart=Restart()
	Restart.RestartProgram()
