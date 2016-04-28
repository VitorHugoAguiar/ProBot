#!/usr/bin/python
import sys
import zmq

# Connection to our subscriber socket
contextS = zmq.Context()
subscriber = contextS.socket(zmq.SUB)
subscriber.connect('tcp://139.162.157.96:5570')
subscriber.setsockopt(zmq.SUBSCRIBE, b"")
poller = zmq.Poller()
poller.register(subscriber, zmq.POLLIN)

# Socket to talk to clients
contextP = zmq.Context()
publisher = contextP.socket(zmq.PUB)
publisher.connect("tcp://139.162.157.96:5559")
publisher.sndhwm = 1100000

class publisher_and_subscriber():
	
    def subscriber(self):	
        socks = dict(poller.poll(0))
        if socks:
            if socks.get(subscriber) == zmq.POLLIN:
                string = subscriber.recv(zmq.NOBLOCK)
                return string
            else:
                print ("error:message timeout")
    

    def publisher(self, midi_device, ForwardReverse, LeftRight):	
        publisher.send_string('{0} {1:.3f} {2:.3f}'.format(midi_device, ForwardReverse, LeftRight),zmq.NOBLOCK)
        
	
		
