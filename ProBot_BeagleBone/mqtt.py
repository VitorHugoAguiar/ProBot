#!/usr/bin/python

# Python Standart Library Imports
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import socket
import random
import os
import sys
import Adafruit_BBIO.ADC as ADC

# Local files
import StartAndStop
import ProBotConstantsFile
import mpu6050File
import SocketWebPageFile
import SocketStartAndStop
import SocketStartAndStop2

# Initialization of classes from local files
Pconst = ProBotConstantsFile.Constants()
StartAndStop = StartAndStop.StartAndStopClass()
mpu6050=mpu6050File.mpu6050Class()
Pub_SubWeb = SocketWebPageFile.SocketClass()
Pub_SubStart = SocketStartAndStop.SocketClass()
Pub_SubStart2 = SocketStartAndStop2.SocketClass()

ADC.setup()

# mqtt variables
broker = '89.109.64.175'
port = 1883
telemetry = ['battery', 'angle', 'mainRoutine']
probotID = '2'
bat_value = 0
angle_value = 0
mainRoutineStatus = 'stopped'
timerS=0.2

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("\nConnected to the server!")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('keys/' + probotID, qos=0)
    client.subscribe('MainRoutine/' + probotID, qos=0)
    client.subscribe('shutdownProBot/' + probotID, qos=0)
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic + " " + str(msg.payload))
    if (msg.topic=='MainRoutine/' + probotID):
    	Pub_SubStart.publisher(str(msg.payload))	
    if (msg.topic=='keys/' + probotID):
        Pub_SubWeb.publisher(msg.payload)
    if (msg.topic=='shutdownProBot/' + probotID):
	if msg.payload=='"shutdown"':
		os.system("sudo shutdown -h now")

def on_disconnect(client, userdata, rc):
    print("Disconnected!")
    Pub_SubWeb.publisher("0 0 0 0")

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.will_set('ClientStatus', probotID + '/OFF-LINE', qos=0)
client.connect_async(broker, port, keepalive=5)

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect=on_disconnect

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_start()

while True:
    try:
    	topic = 'telemetry'

    	bat_value= int((1.8 * ADC.read(Pconst.AnalogPinLiPo) * (100 + 7.620)/7.620) + 1.9)
    	angle_value, gyro_yout_scaled = mpu6050.RollPitch()

    	MainRoutine=Pub_SubStart2.subscriber()

    	if MainRoutine!=None:
    		mainRoutineStatus=MainRoutine

    	else:
		not_executing = StartAndStop.StartAndStopToWeb()
        	if not_executing==0:
        		mainRoutineStatus=0

    	message = probotID + ',' + str(bat_value) + ',' + str(angle_value) + ',' + str(mainRoutineStatus)
    	client.publish(topic, message, qos=0)
    	time.sleep(timerS)

    except KeyboardInterrupt:
        sys.exit('\n\nPROGRAM STOPPED!!!\n')
        raise

