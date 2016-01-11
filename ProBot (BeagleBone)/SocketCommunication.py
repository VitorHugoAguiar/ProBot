#!/usr/bin/python
import sys
import zmq

# Connection to  our subscriber socket
context = zmq.Context()
subscriber = context.socket(zmq.SUB)
subscriber.connect('tcp://176.58.125.166:5560')
subscriber.setsockopt(zmq.SUBSCRIBE, "")
poller = zmq.Poller()
poller.register(subscriber, zmq.POLLIN)


class publisher_and_subscriber():	
    def subscriber(self):	
        socks = dict(poller.poll(0))
        if socks:
            if socks.get(subscriber) == zmq.POLLIN:
                string = subscriber.recv(zmq.NOBLOCK)							
                return string
            else:
                print "error:message timeout"
