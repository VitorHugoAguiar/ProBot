#!/usr/bin/python
import sys
import LowPassFilter
from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol, \
    listenWS

LPF=LowPassFilter.LowPassFilter()

class BroadcastServerProtocol(WebSocketServerProtocol):

    directionUp=0
    directionDown=0
    FilteredValuesFR=0
    FilteredValuesLR=0
    maxValFR=0
    maxValLR=0

    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):
        if payload.decode('utf8')=="0":
            BroadcastServerProtocol.FilteredValuesFR=LPF.lowPassFilterFR(0)
            BroadcastServerProtocol.FilteredValuesLR=LPF.lowPassFilterLR(0)

        if payload.decode('utf8')=="up":
            BroadcastServerProtocol.maxValFR=0.7
            BroadcastServerProtocol.FilteredValuesFR=LPF.lowPassFilterFR(BroadcastServerProtocol.maxValFR)

        if payload.decode('utf8')=="down":
            BroadcastServerProtocol.maxValFR=-0.7
            BroadcastServerProtocol.FilteredValuesFR=LPF.lowPassFilterFR(BroadcastServerProtocol.maxValFR)

        if payload.decode('utf8')=="left":
            BroadcastServerProtocol.maxValLR=0.8
            BroadcastServerProtocol.FilteredValuesLR=LPF.lowPassFilterLR(BroadcastServerProtocol.maxValLR)

        if payload.decode('utf8')=="right":
            BroadcastServerProtocol.maxValLR=-0.8
            BroadcastServerProtocol.FilteredValuesLR=LPF.lowPassFilterLR(BroadcastServerProtocol.maxValLR)


        msg = "{0} {1:.3f} {2:.3f}".format("msg", BroadcastServerProtocol.FilteredValuesFR, BroadcastServerProtocol.FilteredValuesLR)
        factory.broadcast(msg)


    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.factory.unregister(self)


class BroadcastServerFactory(WebSocketServerFactory):

    """
    Simple broadcast server broadcasting any message it receives to all
    currently connected clients.
    """

    def __init__(self, url, debug=False, debugCodePaths=False):
        WebSocketServerFactory.__init__(self, url, debug=debug, debugCodePaths=debugCodePaths)
        self.clients = []

    def register(self, client):
        if client not in self.clients:
            print("registered client {}".format(client.peer))
            self.clients.append(client)

    def unregister(self, client):
        if client in self.clients:
            print("unregistered client {}".format(client.peer))
            self.clients.remove(client)

    def broadcast(self, msg):
        print(msg)
        for c in self.clients:
            c.sendMessage(msg.encode('utf8'))


if __name__ == '__main__':

    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        log.startLogging(sys.stdout)
        debug = True
    else:
        debug = False

    ServerFactory = BroadcastServerFactory
    factory = ServerFactory(u"ws://139.162.157.96:9000",
                            debug=debug,
                            debugCodePaths=debug)

    factory.protocol = BroadcastServerProtocol
    listenWS(factory)

    webdir = File(".")
    web = Site(webdir)
    reactor.listenTCP(8080, web)
    reactor.run()
