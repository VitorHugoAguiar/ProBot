#!/usr/bin/python

# Python Standart Library Imports
import os
import sys
import Adafruit_BBIO.ADC as ADC
import memcache
import time
import pyping
import socket

# Local files
import StartAndStop
import ProBotConstantsFile

# Initialization of classes from local files
Pconst = ProBotConstantsFile.Constants()
StartAndStop = StartAndStop.StartAndStopClass()

time.sleep(60)
ADC.setup()
shared = memcache.Client([('localhost', 15)], debug=0)

        
def main():

        while True:
                    try:
                        r = pyping.ping(Pconst.broker)        
                        
                        bat_value= (1.8 * ADC.read(Pconst.AnalogPinLiPo) * (100 + 7.620)/7.620) + 0.2
                        bat_value_percentage =  (bat_value * 25)-525
                        angle_value = shared.get('ComplementaryAngle')
                                                
                        MainRoutineStatus = shared.get('MainRoutineStatus')
                        
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.connect(("8.8.8.8", 80))
                    
                        not_executing = StartAndStop.StartAndStopToWeb()
                        if not_executing==0:
                                MainRoutineStatus=0
                        
                        Topics =['telemetry']
                        try:
                                
                            if angle_value:
                                    angle_value = int(angle_value + 90)
                            else:
                                    angle_value = 'NaN'
                                
                            TopicsVariables = {'telemetry': ['ProBot' + str(Pconst.probotID), int(bat_value_percentage), str(angle_value), MainRoutineStatus, r.avg_rtt, s.getsockname()[0]]}
                                 
                        
                            for i in range(0, len(Topics)):
                                    message = ','.join(map(str, TopicsVariables[str(Topics[i])]))
                                    print Topics[i], message
                                    shared.set(Topics[i], message)
                        except:  
                            continue

                    except KeyboardInterrupt:
                        s.close()
                        sys.exit('\n\nPROGRAM STOPPED!!!\n')
                        raise

if __name__ == '__main__':
        main()

