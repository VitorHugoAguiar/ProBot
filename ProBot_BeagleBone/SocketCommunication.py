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
publisher.connect("tcp://localhost:5579")
publisher.sndhwm = 1100000

# Connection to our subscriber socket
contextS2 = zmq.Context()
subscriber2 = contextS2.socket(zmq.SUB)
subscriber2.setsockopt(zmq.SUBSCRIBE, "")
poller2 = zmq.Poller()
poller2.register(subscriber2, zmq.POLLIN)
subscriber2.connect('tcp://localhost:5701')

# Connection to our publisher socket
contextP2 = zmq.Context()
publisher2 = contextP2.socket(zmq.PUB)
publisher2.connect("tcp://localhost:5700")
publisher2.sndhwm = 1100000


class publisher_and_subscriber():
    def userChoice(self, userChoice):
        if userChoice=='1':
            subscriber.connect('tcp://localhost:5580')
        if userChoice=='2':
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


    def subscriber2(self):
        socks = dict(poller2.poll(0))
        if socks:
            if socks.get(subscriber2) == zmq.POLLIN:
                string = subscriber2.recv(zmq.NOBLOCK)
                return string

            else:
                print "error:message timeout"

    def publisher2(self, var1, var2):
	publisher2.send_string('{} {}'.format(var1, var2),zmq.NOBLOCK)





