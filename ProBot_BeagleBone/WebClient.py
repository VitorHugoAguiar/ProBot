#!/usr/bin/python


from __future__ import print_function
from os import environ

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.logger import Logger

import sys
import os

import SocketFile
import BatteryMonitorFile

# Initialization of classes from local files
Pub_Sub = SocketFile.SocketClass()
Battery = BatteryMonitorFile.BatteryMonitorClass()


class AppSession(ApplicationSession):

    log = Logger()
    
    def __init__(self, config = None):
        ApplicationSession.__init__(self, config)
        print("component created")

    def onConnect(self):
         print("transport connected")
         self.join(self.config.realm)

    def onChallenge(self, challenge):
         print("authentication challenge received")

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
            try:
                   ## PUBLISH an event
		   Bat_perc= int(((Battery.VoltageValue('LiPo'))*15.385)-287.673)
                   self.publish('probot-bat-2', Bat_perc)
                   self.log.info("published on probot-bat-2: {msg}", msg=Bat_perc)
                   yield sleep(1)
		   
            except:	
                   python = sys.executable
                   os.execl(python, python, * sys.argv)

    def onLeave(self, details):
         print("session left")

    def onDisconnect(self):
         print("transport disconnected")

if __name__ == '__main__':
        runner = ApplicationRunner(
            environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://89.109.64.175:8080/ws"),
                    u"realm1",
                    extra=dict(
				max_events=5, # [A] pass in additional configuration
                    ),
            )
        runner.run(AppSession, auto_reconnect=True)



