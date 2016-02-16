#!/usr/bin/python
import sys
import zmq

# Connection to our subscriber socket
contextS = zmq.Context()
subscriber = contextS.socket(zmq.SUB)
subscriber.connect('tcp://139.162.157.96:5560')
subscriber.setsockopt(zmq.SUBSCRIBE, "")
poller = zmq.Poller()
poller.register(subscriber, zmq.POLLIN)

# Connection to our publisher socket
contextP = zmq.Context()
publisher = contextP.socket(zmq.PUB)
publisher.connect("tcp://139.162.157.96:5569")
publisher.sndhwm = 1100000

class publisher_and_subscriber():	
    def subscriber(self):	
        socks = dict(poller.poll(0))
        if socks:
            if socks.get(subscriber) == zmq.POLLIN:
                string = subscriber.recv(zmq.NOBLOCK)							
                return string
            else:
                print "error:message timeout"
    
    def publisher(self, var1, var2, var3):	
		publisher.send_string('{0:.3f} {1:.3f} {2:.3f}'.format(var1, var2, var3),zmq.NOBLOCK)
