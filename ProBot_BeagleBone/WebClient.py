#!/usr/bin/python
import sys
import zmq
import SocketCommunication

from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory
from twisted.python import log

from autobahn.twisted.websocket import WebSocketClientFactory, \
    WebSocketClientProtocol, \
    connectWS

# Initialization of classes from local files
Pub_Sub = SocketCommunication.publisher_and_subscriber()

class EchoClientProtocol(WebSocketClientProtocol):

    def onMessage(self, payload, isBinary):
        if not isBinary:
            publisher=Pub_Sub.publisher(payload.decode('utf8'))
	    print payload.decode('utf8')
	

class EchoClientFactory(ReconnectingClientFactory, WebSocketClientFactory):

    protocol = EchoClientProtocol

    maxDelay = 10


    def startedConnecting(self, connector):
        print('Started to connect.')


    def clientConnectionLost(self, connector, reason):
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)


    def clientConnectionFailed(self, connector, reason):
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print("Need the WebSocket server address, i.e. ws://139.162.157.96:9000")
        sys.exit(1)

    log.startLogging(sys.stdout)

    factory = EchoClientFactory(sys.argv[1])
    connectWS(factory)

    reactor.run()
