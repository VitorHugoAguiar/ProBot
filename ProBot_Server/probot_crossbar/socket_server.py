from __future__ import print_function
from os import environ
import six


from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet._sslverify import OpenSSLCertificateAuthorities
from twisted.internet.ssl import CertificateOptions
from OpenSSL import crypto
from autobahn.twisted.util import sleep

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.logger import Logger
from twisted.web import client
from threading import Timer,Thread,Event
import threading
from time import sleep

class AppSession(ApplicationSession):
    client._HTTP11ClientFactory.noisy = False
    log = Logger()
    
    @inlineCallbacks
    def onJoin(self, details):
        probotid = None
        lastBat = None
	ProBotTimerBat={}
        ProBotTimerWeb={}
	timerBatInterval=5
	timerWebInterval=3
        def receive_id(probot_id):
            if "probot-" in probot_id:
                probotid=probot_id.split('-')[1]
		if int(probotid)>=len(ProBotTimerBat):
		    ProBotTimerBat[int(probotid)]=0
		
		self.log.info("initializing subscribers for id {probotid}", probotid=probotid)
                topic = "probot-bat-{}".format(probotid)

		def start_timer():
		    ProBotTimerBat[int(probotid)]=Timer(timerBatInterval, battery_timeout)
                    ProBotTimerBat[int(probotid)].start()

		def cancel_timer():
		    ProBotTimerBat[int(probotid)].cancel()
                    ProBotTimerBat[int(probotid)].join()

		def battery_timeout():
		    while (True):
		    	self.log.info("battery not received from probot {probotid}", probotid=probotid)
                    	self.publish('bridge-topic', probotid, 0, "BATTERY TIMEOUT") # to publish on the bridge
                    	print("BATTERY TIMEOUT")
                    	self.publish(topic, "error")
			break

		start_timer()

                if (probotid != None):
                    def receive_bat(bat_value):
			cancel_timer()
			start_timer()
			self.log.info("last battery from {topic}: {bat_value}", topic=topic, bat_value=bat_value)
			self.publish('bridge-topic', probotid, bat_value, "UPDATE") # to publish on the bridge
		    
		    self.subscribe(receive_bat, topic)
		   
            else:
                probotid=probot_id
		self.log.info("initializing subscribers for id {probotid} (controls)", probotid=probot_id)
		topic = "probot-topic-{}".format(probotid)
		keepalive_topic = "keepalive-{}".format(probotid)
		print("KEEPALIVE")
			
                def webclient_timeout():
                	self.log.info("keepalive not received from probot {probotid}", probotid=probotid)
                    	self.publish('bridge-topic', probotid, 0, "WEB TIMEOUT") # to publish on the bridge
                    	print("WEB TIMEOUT")

                ProBotTimerWeb[int(probotid)]=Timer(timerWebInterval, webclient_timeout,())
                ProBotTimerWeb[int(probotid)].start()
		ProBotTimerWeb[int(probotid)].cancel()

                def reset_timer():
                       	ProBotTimerWeb[int(probotid)].cancel()
                       	ProBotTimerWeb[int(probotid)]=Timer(timerWebInterval, webclient_timeout,())
                       	ProBotTimerWeb[int(probotid)].start()

               	self.subscribe(reset_timer, keepalive_topic)

		def receive_msg(msg):
                       	self.log.info("event from {topic} received: {msg}", topic=topic, msg=msg)
		self.subscribe(receive_msg, topic)


        self.subscribe(receive_id, "general-topic")
        yield sleep(1)

    def onLeave(self, details):
         print("session left")

    def onDisconnect(self):
	print("transport disconnected")
	if reactor.running:
		reactor.stop()




