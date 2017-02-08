#!/usr/bin/python
import sys
import zmq

# Connection to our subscriber socket
contextS = zmq.Context()
subscriber = contextS.socket(zmq.SUB)
subscriber.setsockopt(zmq.SUBSCRIBE, "")
poller = zmq.Poller()
poller.register(subscriber, zmq.POLLIN)
subscriber.connect('tcp://localhost:5584')

# Connection to our publisher socket
contextP = zmq.Context()
publisher = contextP.socket(zmq.PUB)
publisher.connect("tcp://localhost:5583")
publisher.sndhwm = 1000000000


class SocketClass():

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








