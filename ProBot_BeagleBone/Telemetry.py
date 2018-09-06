#!/usr/bin/python

# Python Standart Library Imports
import os
import sys
import Adafruit_BBIO.ADC as ADC
import memcache
import socket
import fcntl
import struct
import shlex
from subprocess import Popen, PIPE, STDOUT
import urllib2
import time

# Local files
import StartAndStop
import ProBotConstantsFile

# Initialization of classes from local files
Pconst = ProBotConstantsFile.Constants()
StartAndStop = StartAndStop.StartAndStopClass()

time.sleep(60)
ADC.setup()
shared = memcache.Client([('localhost', 15)], debug=0)

	
def get_interface_ipaddress(network):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,struct.pack('256s', network[:15]))[20:24])

def get_simple_cmd_output(cmd, stderr=STDOUT):
    #Execute a simple external command and get its output.

    args = shlex.split(cmd)
    return Popen(args, stdout=PIPE, stderr=stderr).communicate()[0]


def get_ping_time(host):
    host = host.split(':')[0]
    cmd = "fping {host} -C 3 -q".format(host=host)
    
    result = str(get_simple_cmd_output(cmd)).replace('\\', '').split(':')[-1].replace("n'", '').replace("-", '').replace( "b''", '').split()
    res = [float(x) for x in result]
    if len(res) > 0:
        return sum(res) / len(res)
    else:
        return 999999


def main():
	latencyList_mean = []
	latency_mean = 0

	while True:
    		try:
	
			latency = get_ping_time(Pconst.broker)
    			bat_value= (1.8 * ADC.read(Pconst.AnalogPinLiPo) * (100 + 7.620)/7.620) + 0.2
			bat_value_percentage =  (bat_value * 25)-525
    			angle_value = shared.get('ComplementaryAngle')
			
			MainRoutineStatus = shared.get('MainRoutineStatus')
    		
                        not_executing = StartAndStop.StartAndStopToWeb()
                        if not_executing==0:
                                MainRoutineStatus=0
			
			latencyList_mean.append(int(latency))
			
                        if len(latencyList_mean) == 5:
                       		latency_mean = sum(latencyList_mean)/len(latencyList_mean)
                        	latencyList_mean[:] = []	
                        

                        Topics =['telemetry']
			try:
				if urllib2.urlopen('http://216.58.192.142', timeout=300):
					if angle_value:
                        			TopicsVariables = {'telemetry': ['ProBot' + str(Pconst.probotID), int(bat_value_percentage), str(int(angle_value + 90)), MainRoutineStatus, int(latency_mean),get_interface_ipaddress('wlan0')]}
					else:
						TopicsVariables = {'telemetry': ['ProBot' + str(Pconst.probotID), int(bat_value_percentage), str('NaN'), MainRoutineStatus, int(latency_mean),get_interface_ipaddress('wlan0')]}
			
                        		for i in range(0, len(Topics)):
                                		message = ','.join(map(str, TopicsVariables[str(Topics[i])]))
						print Topics[i], message
                                		shared.set(Topics[i], message)
			except urllib2.URLError as err: 
				print "No Internet!"
				continue

    		except KeyboardInterrupt:
        		sys.exit('\n\nPROGRAM STOPPED!!!\n')
        		raise

if __name__ == '__main__':
	main()

