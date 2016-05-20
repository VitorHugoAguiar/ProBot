import sys
import decimal
from twisted.internet import reactor
from twisted.python import log
from twisted.web.server import Site
from twisted.web.static import File

from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol, \
    listenWS

class BroadcastServerProtocol(WebSocketServerProtocol):

    directionUp=0
    directionDown=0
    ValuesFR=0
    ValuesLR=0
    maxValFR=0
    maxValLR=0

    def onOpen(self):
        self.factory.register(self)

    def onMessage(self, payload, isBinary):

	direction=float(decimal.Decimal(payload.decode('utf8')))
	if direction==0:
		BroadcastServerProtocol.ValuesFR=0
		BroadcastServerProtocol.ValuesLR=0
        if (direction>=100 and direction<=300):
		direction=(direction-200)*0.01
	  	BroadcastServerProtocol.ValuesFR=direction
	if direction>=400 and direction<=600:
           	direction=(direction-500)*0.01
	   	BroadcastServerProtocol.ValuesLR=direction

        msg = "{0} {1:.3f} {2:.3f}".format("msg", BroadcastServerProtocol.ValuesFR, BroadcastServerProtocol.ValuesLR)
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
