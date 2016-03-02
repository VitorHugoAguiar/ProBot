#!/usr/bin/python
import sys
import zmq

# Connection to our subscriber socket
contextS = zmq.Context()
subscriber = contextS.socket(zmq.SUB)

subscriber.setsockopt(zmq.SUBSCRIBE, "")
poller = zmq.Poller()
poller.register(subscriber, zmq.POLLIN)

# Connection to our publisher socket
contextP = zmq.Context()
publisher = contextP.socket(zmq.PUB)
publisher.connect("tcp://192.168.1.120:5579")
publisher.sndhwm = 1100000


class publisher_and_subscriber():
    def userChoice(self, userChoice):
        if userChoice==1:
            subscriber.connect('tcp://192.168.1.120:5580')
        if userChoice==2:
            subscriber.connect('tcp://139.162.157.96:5560')

    def subscriber(self):
        socks = dict(poller.poll(0))
        if socks:
            if socks.get(subscriber) == zmq.POLLIN:
                string = subscriber.recv(zmq.NOBLOCK)
                return string

            else:
                print "error:message timeout"

    def publisher(self, var1):
		publisher.send_string('{}'.format(var1),zmq.NOBLOCK)
