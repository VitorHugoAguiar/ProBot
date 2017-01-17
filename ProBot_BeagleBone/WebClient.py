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

# Initialization of classes from local files
Pub_Sub = SocketWebPageFile.SocketClass()
Pub_Sub2 = SocketBatteryFile.SocketClass()

class AppSession(ApplicationSession):

    log = Logger()

    @inlineCallbacks
    def onJoin(self, details):

        ## SUBSCRIBE to a topic and receive events
        def probot_topic_2(msg):
                
        	msg2=[msg.encode('utf-8') for msg in msg]
            
        	publisher=Pub_Sub.publisher(msg2)
             

        sub = yield self.subscribe(probot_topic_2, 'probot-topic-2')
        self.log.info("subscribed to topic 'probot-topic-2'")

	self.publish('general-topic', "B-2")


        ## PUBLISH and CALL every second .. forever
        while True:
		
		## PUBLISH an event
       		subscriber = Pub_Sub2.subscriber()	
		if subscriber is None:
			subscriber=0
			Bat_perc=0	
       		else:
			if 'Bat-' in subscriber:
            			Bat_perc=subscriber.split('-')[1]			
		
		self.publish('probot-bat-2', Bat_perc)
		self.log.info("published on probot-bat-2: {msg}", msg=Bat_perc)
        	yield sleep(1)

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
        environ.get("AUTOBAHN_DEMO_ROUTER", u"wss://89.109.64.175:8080/ws"),
        u"realm1",
        ssl=options,  # try removing this, but still use self-signed cert
    )
    runner.run(AppSession, auto_reconnect=True)
