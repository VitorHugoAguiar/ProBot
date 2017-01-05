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

from threading import Timer

class AppSession(ApplicationSession):

    log = Logger()

    @inlineCallbacks
    def onJoin(self, details):
        probotid = None
        lastBat = None
        ProBotTimerBat={}
        ProBotTimerWeb={}

        def receive_id(probot_id):

            if "B-" in probot_id:
                probotid=probot_id.split('-')[1]
		if int(probotid)>=len(ProBotTimerBat):
			ProBotTimerBat[int(probotid)]=0

		self.log.info("initializing subscribers for id {probotid}", probotid=probotid)
                topic = "probot-bat-{}".format(probotid)

                def battery_timeout():
                    self.log.info("battery not received from probot {probotid}", probotid=probotid)
                    self.publish('bridge-topic', probotid, 0, "BATTERY TIMEOUT") # to publish on the bridge
                    print("BATTERY TIMEOUT")
                    self.publish(topic, "error")

		ProBotTimerBat[int(probotid)]=Timer(60, battery_timeout,())
                ProBotTimerBat[int(probotid)].start()

                if (probotid != None):
                    def receive_bat(bat_value):
                        self.log.info("last battery from {topic}: {bat_value}", topic=topic, bat_value=bat_value)
                        self.publish('bridge-topic', probotid, bat_value, "UPDATE") # to publish on the bridge
			ProBotTimerBat[int(probotid)].cancel()
			ProBotTimerBat[int(probotid)]=Timer(60, battery_timeout,())
	                ProBotTimerBat[int(probotid)].start()
                    self.subscribe(receive_bat, topic)

            else:
                probotid=probot_id
                if int(probotid)>=len(ProBotTimerWeb):
                	ProBotTimerWeb[int(probotid)]=0

		self.log.info("initializing subscribers for id {probotid} (controls)", probotid=probot_id)
		topic = "probot-topic-{}".format(probotid)
                keepalive_topic = "keepalive-{}".format(probotid)
		print("KEEPALIVE")

                def webclient_timeout():
                    self.log.info("keepalive not received from probot {probotid}", probotid=probotid)
                    self.publish('bridge-topic', probotid, 0, "WEB TIMEOUT") # to publish on the bridge
                    print("WEB TIMEOUT")

                ProBotTimerWeb[int(probotid)]=Timer(10, webclient_timeout,())
                ProBotTimerWeb[int(probotid)].start()
		ProBotTimerWeb[int(probotid)].cancel()

                def reset_timer():
                        ProBotTimerWeb[int(probotid)].cancel()
                        ProBotTimerWeb[int(probotid)]=Timer(10, webclient_timeout,())
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




