
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
        probotid = None
        lastBat = None
        
        def receive_id(probot_id):
        
            if "B-" in probot_id:
                probotid=probot_id.split('-')[1]
                self.log.info("initializing subscribers for id {probotid}", probotid=probotid)
                topic = "probot-bat-{}".format(probotid)
                                
                def battery_timeout():
                    self.log.info("battery not received from probot {probotid}", probotid=probotid)
                    self.publish('bridge-topic', probotid, 0, "BATTERY TIMEOUT") # to publish on the bridge
                    print("BATTERY TIMEOUT")
                    self.publish(topic, "error")
                    
                self.bat_alive_timer = Timer(30, battery_timeout,())
                self.bat_alive_timer.start()
                               
                if probotid != None:                
                    def receive_bat(bat_value):
                        print(bat_value)
                        self.log.info("last battery from {topic}: {bat_value}", topic=topic, bat_value=bat_value)
                        self.publish('bridge-topic', probotid, bat_value, "UPDATE") # to publish on the bridge
                        self.bat_alive_timer.cancel()
                        self.bat_alive_timer = Timer(30, battery_timeout,())
                        self.bat_alive_timer.start()                        
                    self.subscribe(receive_bat, topic)                                                   
                            
            else:
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
                    self.publish('bridge-topic', probotid, 0, "WEB TIMEOUT") # to publish on the bridge
                    print("WEB TIMEOUT")
        
                self.keep_alive_timer = Timer(30, webclient_timeout,())
                self.keep_alive_timer.start()
        
                def reset_timer():
                    self.keep_alive_timer.cancel()
                    self.keep_alive_timer = Timer(30, webclient_timeout,())
                    self.keep_alive_timer.start()
            
                self.subscribe(reset_timer, keepalive_topic)
            
        self.subscribe(receive_id, "general-topic")
        
        yield sleep(1)	
	    
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


