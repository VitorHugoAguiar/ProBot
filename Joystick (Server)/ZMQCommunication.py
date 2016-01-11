#!/usr/bin/python
import sys
import zmq

# Socket to talk to clients
context = zmq.Context()
publisher = context.socket(zmq.PUB)
publisher.connect("tcp://176.58.125.166:5559")
publisher.sndhwm = 1100000


class Publisher():
	def publisher(self, midi_device, ForwardReverse, LeftRight):	
		publisher.send_string('{0} {1:.3f} {2:.3f}'.format(midi_device, ForwardReverse, LeftRight),zmq.NOBLOCK)
	
		
