#!/usr/bin/python

# Python Standart Library Imports
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import os
import sys
import memcache


# Local files
import ProBotConstantsFile

# Initialization of classes from local files
Pconst = ProBotConstantsFile.Constants()

shared = memcache.Client([('localhost', 15)], debug=0)

# mqtt variables
port = 1883
        

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("\nConnected to the server!")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('keys/' + 'ProBot' + Pconst.probotID, qos=0)
    client.subscribe('MainRoutine/' + 'ProBot' + Pconst.probotID, qos=0)
    client.subscribe('shutdownProBot/' + 'ProBot' + Pconst.probotID, qos=0)
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
        
    if (msg.topic=='MainRoutine/' + 'ProBot' + Pconst.probotID):        
        shared.set('MainRoutine', msg.payload)
        
    if (msg.topic=='keys/' + 'ProBot'+ Pconst.probotID):
        #print msg.payload
        shared.set('keys', msg.payload)

    if (msg.topic=='shutdownProBot/' + 'ProBot' + Pconst.probotID):
        if msg.payload=='shutdown':
                os.system("sudo shutdown -h now")

def on_disconnect(client, userdata, rc):
    print("Disconnected!")
    shared.set('keys', '0 0 0 0')


client = mqtt.Client(protocol=mqtt.MQTTv311)
client.will_set('ClientStatus', 'ProBot' + str(Pconst.probotID) + '/Offline', qos=0)
client.connect_async(Pconst.broker, port, keepalive=5)

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect=on_disconnect

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()

def main():
        while True:
                    try:

                        processname = 'Telemetry.py'
                        tmp = os.popen("ps -Af").read()
                        proccount = tmp.count(processname)

                        topic = 'telemetry'                        
                        message = shared.get(topic)
                        
                        if message:
                                if proccount < 0 or proccount == 0:
                                        topic = 'ClientStatus'
                                        message = 'ProBot' + str(Pconst.probotID) + '/Offline'
                                        #print message
                                client.publish(topic, message , qos=0)
                        
                    except KeyboardInterrupt:
                        shared.set('keys', "0 0 0 0")
                        sys.exit('\n\nPROGRAM STOPPED!!!\n')
                        raise

if __name__ == '__main__':
        main()

