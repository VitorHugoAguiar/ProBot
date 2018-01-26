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
import memcache

# Local files
import StartAndStop
import ProBotConstantsFile
import mpu6050File

ADC.setup()
shared = memcache.Client([('localhost', 15)], debug=0)

# Initialization of classes from local files
Pconst = ProBotConstantsFile.Constants()
StartAndStop = StartAndStop.StartAndStopClass()
mpu6050=mpu6050File.mpu6050Class()

# mqtt variables
port = 1883
telemetry = ['battery', 'angle', 'mainRoutine']
bat_value = 0
angle_value = 0
mainRoutineStatus = 'stopped'
timerS=0.2

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("\nConnected to the server!")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe('keys/' + Pconst.probotID, qos=0)
    client.subscribe('MainRoutine/' + Pconst.probotID, qos=0)
    client.subscribe('shutdownProBot/' + Pconst.probotID, qos=0)
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    if (msg.topic=='MainRoutine/' + Pconst.probotID):	
	shared.set('MainRoutine', msg.payload)
	
    if (msg.topic=='keys/' + Pconst.probotID):
	shared.set('keys', msg.payload)

    if (msg.topic=='shutdownProBot/' + Pconst.probotID):
	if msg.payload=='"shutdown"':
		os.system("sudo shutdown -h now")

def on_disconnect(client, userdata, rc):
    print("Disconnected!")
    shared.set('keysValues', "0 0 0 0")

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.will_set('ClientStatus', Pconst.probotID + '/OFF-LINE', qos=0)
client.connect_async(Pconst.broker, port, keepalive=5)

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

    	bat_value= round((1.8 * ADC.read(Pconst.AnalogPinLiPo) * (100 + 7.620)/7.620) + 0.2, 2)
    	angle_value, gyro_yout_scaled = mpu6050.RollPitch()
	#if shared.get('ComplementaryAngle')==None:
	#	angle_value=0
	#else:
	#	angle_value = shared.get('ComplementaryAngle')
	
	MainRoutineStatus = shared.get('MainRoutineStatus')
    	mainRoutineStatus=MainRoutineStatus

	not_executing = StartAndStop.StartAndStopToWeb()
        if not_executing==0:
        	mainRoutineStatus=0

    	message = Pconst.probotID + ',' + str(bat_value) + ',' + str(angle_value) + ',' + str(mainRoutineStatus)
    	client.publish(topic, message, qos=0)
    	time.sleep(timerS)
	

    except KeyboardInterrupt:
        sys.exit('\n\nPROGRAM STOPPED!!!\n')
        raise

