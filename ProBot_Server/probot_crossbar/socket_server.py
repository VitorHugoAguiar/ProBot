###############################################################################
##
##  Copyright (C) 2014, Tavendo GmbH and/or collaborators. All rights reserved.
##
##  Redistribution and use in source and binary forms, with or without
##  modification, are permitted provided that the following conditions are met:
##
##  1. Redistributions of source code must retain the above copyright notice,
##     this list of conditions and the following disclaimer.
##
##  2. Redistributions in binary form must reproduce the above copyright notice,
##     this list of conditions and the following disclaimer in the documentation
##     and/or other materials provided with the distribution.
##
##  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
##  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
##  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
##  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
##  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
##  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
##  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
##  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
##  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
##  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
##  POSSIBILITY OF SUCH DAMAGE.
##
###############################################################################

from __future__ import print_function
from os import environ

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep

from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from twisted.logger import Logger

from threading import Timer

class AppSession(ApplicationSession):

    log = Logger()
    timeout = 5

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
        #self.lastMsg = 0
        probotid = None
        lastBat = None
        
        def receive_id(probot_id):
        
            if "B-" in probot_id:
                probotid=probot_id.split('-')[1]
                self.log.info("initializing subscribers for id {probotid}", probotid=probotid)
                topic = "probot-bat-{}".format(probotid)
                                
                def battery_timeout():
                    self.log.info("battery not received from probot {probotid}", probotid=probotid)
                    self.publish('bridge-topic', probotid, 0, "BATTERY TIMEOUT") # para publicar na bridge
                    print("BATTERY TIMEOUT")
                    self.publish(topic, "error")
                    
                self.bat_alive_timer = Timer(30, battery_timeout,())
                self.bat_alive_timer.start()
                               
                if probotid != None:                
                    def receive_bat(bat_value):
                        #global lastBat
                        #lastBat = bat_value.split('-')[1]
                        print(bat_value)
                        #print(lastBat)
                        #self.log.info("last battery from {topic}: {lastBat}", topic=topic, lastBat=lastBat)
                        #self.publish('bridge-topic', probotid, lastBat) # para publicar na bridge
                        self.log.info("last battery from {topic}: {bat_value}", topic=topic, bat_value=bat_value)
                        self.publish('bridge-topic', probotid, bat_value, "UPDATE") # para publicar na bridge
                        self.bat_alive_timer.cancel()
                        self.bat_alive_timer = Timer(30, battery_timeout,())
                        self.bat_alive_timer.start()                        
                    self.subscribe(receive_bat, topic)                                                   
                            
            else:
                #if not "B-" in probot_id:
                self.log.info("initializing subscribers for id {probotid} (controls)", probotid=probot_id)
                probotid=probot_id
                topic = "probot-topic-{}".format(probotid)
                keepalive_topic = "keepalive-{}".format(probotid)
                if probotid != None:
                    print(probotid)
                    def receive_msg(msg):
                        self.log.info("event from {topic} received: {msg}", topic=topic, msg=msg)
                self.subscribe(receive_msg, topic)    
        
                def webclient_timeout():
                    self.log.info("keepalive not received from probot {probotid}", probotid=probotid)
                    #global lastBat
                    #if lastBat != None:
                    self.publish('bridge-topic', probotid, 0, "WEB TIMEOUT") # para publicar na bridge
                    print("WEB TIMEOUT")
                    #else:
                        #self.publish('bridge-topic', probotid, "error")
        
                self.keep_alive_timer = Timer(30, webclient_timeout,())
                self.keep_alive_timer.start()
        
                def reset_timer():
                    self.keep_alive_timer.cancel()
                    self.keep_alive_timer = Timer(30, webclient_timeout,())
                    self.keep_alive_timer.start()
            
                self.subscribe(reset_timer, keepalive_topic)
            
        self.subscribe(receive_id, "general-topic")
        
        yield sleep(1)	
        #self.publish('bridge-topic', probot_id) # para publicar na bridge

		
        #self.log.info("subscribed to topic 'probot2beagle'")

       ## PUBLISH and CALL every second .. forever
        #while True:

            ## PUBLISH an event
            #self.publish('blabla', msg)
            #self.log.info("published an probot2Web from python")

            #yield sleep(1)
	    
    def onLeave(self, details):
         print("session left")

    def onDisconnect(self):
         print("transport disconnected")

if __name__ == '__main__':
        runner = ApplicationRunner(
            environ.get("AUTOBAHN_DEMO_ROUTER", u"ws://127.0.0.1:8080/ws"),
                    u"realm1",
                    extra=dict(
                               max_events=5,  # [A] pass in additional configuration
                    ),
            )
        runner.run(AppSession , auto_reconnect=True)


