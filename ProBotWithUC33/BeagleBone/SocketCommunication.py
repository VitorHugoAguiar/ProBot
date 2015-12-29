#!/usr/bin/python
import sys
import zmq
import time

#Initalization of the publisher
context1 = zmq.Context()
publisher = context1.socket(zmq.PUB)
publisher.bind("tcp://*:%s" % 5555)

context = zmq.Context()

# First, connect our subscriber socket
subscriber = context.socket(zmq.SUB)
subscriber.connect('tcp://192.168.11.2:5561')
subscriber.setsockopt(zmq.SUBSCRIBE, b'')

time.sleep(1)

# Second, synchronize with publisher
syncclient = context.socket(zmq.REQ)
syncclient.connect('tcp://192.168.11.2:5562')

# send a synchronization request
syncclient.send(b'')

# wait for synchronization reply
syncclient.recv()

poller=zmq.Poller()
poller.register(subscriber,zmq.POLLIN)

class publisher_and_subscriber():
		
	def publisher(self, graph_variable, graph_variable2):
		publisher.send("%f %f" % (graph_variable, graph_variable2))
	
	def subscriber(self):	
		socks=dict(poller.poll(0))
		if socks:
			if socks.get(subscriber)==zmq.POLLIN:
				string = subscriber.recv(zmq.NOBLOCK)								
				return string		
								
			else:
				print "error:message timeout"				
		



