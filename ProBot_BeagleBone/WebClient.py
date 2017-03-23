#!/usr/bin/python

from __future__ import print_function
from os import environ
import six

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner

from twisted.logger import Logger
from twisted.internet._sslverify import OpenSSLCertificateAuthorities
from twisted.internet.ssl import CertificateOptions
from OpenSSL import crypto

import sys
import os
import time
import SocketWebPageFile
import SocketBatteryFile
import SocketAngleFile

# Initialization of classes from local files
Pub_Sub = SocketWebPageFile.SocketClass()
Pub_Sub2 = SocketBatteryFile.SocketClass()
Pub_Sub3=SocketAngleFile.SocketClass()

class AppSession(ApplicationSession):

    log = Logger()

    @inlineCallbacks
    def onJoin(self, details):

        ## SUBSCRIBE to a topic and receive events
        def probot_topic(msg):
                
        	msg2=[msg.encode('utf-8') for msg in msg]
            
        	publisher=Pub_Sub.publisher(msg2)
         	    

        sub = yield self.subscribe(probot_topic, 'probot-topic_probot_id')
        self.log.info("subscribed to topic 'probot-topic-probot_id'")
	self.publish('general-topic', "probot-probot_id")

        ## PUBLISH and CALL every second .. forever
       	while True:

		#self.publish('general-topic', "probot-1")	
		
		## PUBLISH an event
       		Bat = Pub_Sub2.subscriber()
		Angle= Pub_Sub3.subscriber()
		if Bat==None:
			Bat=0	
		if Angle==None:
			Angle=90
		
		self.publish('probot-bat-probot_id', Bat)
		self.publish('probot-angle-probot_id', Angle)
		self.log.info("published on probot-bat-probot_id: {msg}", msg=Bat)
		self.log.info("published on probot-angle-probot_id: {msg}", msg=Angle)
        	yield sleep(1)

    def onDisconnect(self):
        print("disconnected")
	publisher=Pub_Sub.publisher("['0.000', '0.000', '0.000', '0.000']")        


if __name__ == '__main__':
    # load the self-signed cert the server is using
    cert = crypto.load_certificate(
        crypto.FILETYPE_PEM,
        six.u(open('/home/machinekit/ProBot/ProBot_BeagleBone/server.crt', 'r').read())
    )
    # tell Twisted to use just the one certificate we loaded to verify connections
    options = CertificateOptions(
        trustRoot=OpenSSLCertificateAuthorities([cert]),
    )
    # ...which we pass as "ssl=" to ApplicationRunner (passed to SSL4ClientEndpoint)
    runner = ApplicationRunner(
        environ.get("AUTOBAHN_DEMO_ROUTER", u"wss://server_ip:8080/ws"),
        u"realm1",
        ssl=options,  # try removing this, but still use self-signed cert
    )
    runner.run(AppSession, auto_reconnect=True)
