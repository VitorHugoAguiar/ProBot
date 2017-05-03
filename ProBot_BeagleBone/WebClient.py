#!/usr/bin/python

from __future__ import print_function
import sys
import os
import time

from os import environ
import six
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.logger import Logger
from twisted.internet._sslverify import OpenSSLCertificateAuthorities
from twisted.internet.ssl import CertificateOptions
from OpenSSL import crypto
#from threading import Timer,Thread,Event
#import multiprocessing

import StartAndStop
import mpu6050File 
import ProBotConstantsFile
import Adafruit_BBIO.ADC as ADC
import SocketWebPageFile
import SocketStartAndStop
import SocketStartAndStop2


# Initialization of classes from local files
StartAndStop = StartAndStop.StartAndStopClass()
mpu6050=mpu6050File.mpu6050Class()
Pub_SubWeb = SocketWebPageFile.SocketClass()
Pub_SubStart = SocketStartAndStop.SocketClass()
Pub_SubStart2 = SocketStartAndStop2.SocketClass()

Pconst = ProBotConstantsFile.Constants()
ADC.setup()

class AppSession(ApplicationSession):
    
    log = Logger()

    @inlineCallbacks
    def onJoin(self, details):
	self.MainRoutine="stopped"  	
	## subscribe to the web topic (interface controls)
        def probot_topic(msg):
		Pub_SubWeb.publisher([msg.encode('utf-8') for msg in msg])
		                        	    
       	sub = yield self.subscribe(probot_topic, 'probot-topic-1')
        self.log.info("subscribed to topic 'probot-topic-1'")

        ## subscribe to the StartAndStop topic
        def probot_topic_StartAndStop(msg):
		Pub_SubStart.publisher(str([msg.encode('utf-8') for msg in msg]).replace("[", "").replace("'", "").replace("]", "").replace(" ", "").replace(",", ""))
		
        sub = yield self.subscribe(probot_topic_StartAndStop, 'probot-StartAndStop-1')
        self.log.info("subscribed to topic 'probot-StartAndStop-1'")

	self.publish('general-topic', "probot-1")
	       	
	while True:
		MainRoutine=Pub_SubStart2.subscriber()		

		if MainRoutine!=None:
			self.MainRoutine=MainRoutine
		else:
			not_executing = StartAndStop.StartAndStopToWeb()
			if not_executing==0:
				self.MainRoutine=0

           	AngleValue, gyro_yout_scaled = mpu6050.RollPitch()
		Battery = (1.8 * ADC.read(Pconst.AnalogPinLiPo) * (100 + 7.620)/7.620) + 0.5

		self.publish('probot-bat-1', int(Battery))
		self.publish('probot-angle-1', AngleValue)
                self.publish('probot-mainRoutine-1', self.MainRoutine)		
		self.log.info("published on probot-bat-1: {msg}", msg=int(Battery))
		self.log.info("published on probot-angle-1: {msg}", msg=AngleValue)
                self.log.info("published on probot-mainRoutine-1: {msg}", msg=self.MainRoutine)
        	yield sleep(0.1)

    def onDisconnect(self):
        print("disconnected")
	Pub_SubWeb.publisher("['0.000', '0.000', '0.000', '0.000']")  
	

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
