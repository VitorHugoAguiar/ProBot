#!/usr/bin/python
import sys
import zmq
import ZMQCommunication

from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientFactory, \
    WebSocketClientProtocol, \
    connectWS

Pub_Sub = ZMQCommunication.publisher_and_subscriber()

class BroadcastClientProtocol(WebSocketClientProtocol):

    def onMessage(self, payload, isBinary):
        direction=payload.decode('utf8')
        print direction
        publisher = Pub_Sub.publisher(direction)

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Need the WebSocket server address, i.e. ws://139.162.157.96:9000")
        sys.exit(1)

    factory = WebSocketClientFactory(sys.argv[1])
    factory.protocol = BroadcastClientProtocol
    connectWS(factory)

    reactor.run()
