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

# Initialization of classes from local files
Pub_Sub = SocketFile.SocketClass()

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
        	subscriber = Pub_Sub.subscriber()
		if subscriber is None:
			subscriber=0
			Bat_perc=0
        	else:
			if 'Bat-' in subscriber:
            			bat=subscriber.split('-')[1]			
				Bat_perc=((int(bat)*15.385)-287.673)
		
		self.publish('probot-bat-2', int(Bat_perc))
		self.log.info("published on probot-bat-2: {msg}", msg=int(Bat_perc))
                yield sleep(1)

if __name__ == '__main__':
        runner = ApplicationRunner(
            environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://89.109.64.175:8080/ws"),
                    u"realm1",       
            )
        runner.run(AppSession, auto_reconnect=True)



