#!/usr/bin/python

# Python Standard Library Imports
import sys
import os
import math
import time
import datetime
import threading
import smbus
import memcache
import Adafruit_BBIO.GPIO as GPIO

# Local files
import SabertoothFile
import PIDControllersFile
import EncodersFile
import ProBotConstantsFile
import PWMFile
import WebPageFile
import RestartProgramFile
import MotorsControlFile
import StartFile
import MPU6050File

# Initialization of classes from local files
InitProgram = StartFile.StartFileClass()
RestartProgram = RestartProgramFile.RestartProgramClass()
Sabertooth = SabertoothFile.SabertoothClass()
PID = PIDControllersFile.PIDControllersClass()
Encoders = EncodersFile.EncodersClass()
Pconst = ProBotConstantsFile.Constants()
PWM = PWMFile.PWMClass()
WebPage = WebPageFile.WebPageClass()
MotorsControlSignals = MotorsControlFile.MotorsControlClass()
InitParameters = InitProgram.StartProgram()
userChoice = InitParameters[0]
MPU6050 = MPU6050File.mpu6050Class()

shared = memcache.Client([('localhost', 15)], debug=0)
shared.set('MainRoutinePID', str(os.getpid()))

# Configuration the type of GPIO's
GPIO.setup(Pconst.RedLED, GPIO.OUT)
GPIO.setup(Pconst.GreenLED, GPIO.OUT)
GPIO.setup(Pconst.BlueLED, GPIO.OUT)

class ProBot():

    def __init__(self):
        self.LoopTimeResult = 0
        self.wheelVelocity1 = 0
        self.wheelVelocity2 = 0
        self.EncodersTimeout = 0.025    
        self.clearTimer = 0
        self.clearTimerMPU = 0
        self.MPUTimeout = 0.3 
        self.ComplementaryAngle = 0
        self.EncodersThread = 0
        self.MPUThread = 0

    def EncodersTimer(self):
        if Encoders:
                self.wheelVelocity1, self.wheelVelocity2  = Encoders.EncodersValues()        
                self.EncodersThread = threading.Timer(self.EncodersTimeout, ProBot.EncodersTimer)
                self.EncodersThread.daemon=True
                self.EncodersThread.start()
                self.clearTimer=1

    def MPUTimer(self):
        if MPU6050:
                shared.set('ComplementaryAngle', self.ComplementaryAngle)
                self.MPUThread = threading.Timer(self.MPUTimeout, ProBot.MPUTimer)
                self.MPUThread.daemon=True
                self.MPUThread.start()
                self.clearTimerMPU=1

    def StartAndStopMainRoutine(self):
        try:
                StartAndStop = shared.get('StartAndStop')

                if StartAndStop =="1":
                        shared.set('MainRoutineStatus', "started")
                        ProBot.mainRoutine()

                shared.set('MainRoutineStatus', "stopped")

                print ("\nWaiting for the admin start")
                while shared.get('MainRoutine')!='"start"':
                        shared.get('MainRoutine')
                        time.sleep(1)
                print("\nReceived the start from the admin")

                shared.set('StartAndStop', "1")
                ProBot.mainRoutine()

        except KeyboardInterrupt:
                    shared.set('MainRoutineStatus', "stopped")
                    InitProgram.StopProgram()
                    print("Unexpected error:\n", sys.exc_info()[0])
                    sys.exit('\n\nPROGRAM STOPPED!!!\n')
                    raise

    def mainRoutine(self):
        try:

                # Calibration of MPU6050
                GPIO.output(Pconst.RedLED, GPIO.LOW)
                GPIO.output(Pconst.BlueLED, GPIO.HIGH)
          
                MPU6050.Calibration()
                
                GPIO.output(Pconst.BlueLED, GPIO.LOW)
                GPIO.output(Pconst.GreenLED, GPIO.HIGH)

                time.sleep(2)
                
                ProBot.EncodersTimer()
                ProBot.MPUTimer()
                
                while True:
                    try:
                            LoopTimeStart=time.time()

                            if shared.get('MainRoutine') =='"stop"':
                                shared.set('StartAndStop', "0")
                                shared.set('MainRoutineStatus', "stopped")
                                RestartProgram.RestartProgramRoutine()

                            # Reading the values from the webpage
                            VelocityRef, TurnMotorRight, TurnMotorLeft = WebPage.WebPage_Values()
                                                                                                
                            # Reading the MPU6050 values and use the complementary filter to get better values
                            self.ComplementaryAngle = MPU6050.Complementary_filter(self.LoopTimeResult)
                        
                            # Checking if the angle is out of range
                            if self.ComplementaryAngle<-20 or self.ComplementaryAngle>20:
                                RestartProgram.RestartProgramRoutine()
                                
                            # With the values from the WebPage, we can calculate the outputs from the controllers
                            TargetAngle1 = PID.standardPID((VelocityRef+TurnMotorRight), self.wheelVelocity1, 'Velocity1', userChoice)
                            TargetAngle2 = PID.standardPID((VelocityRef+TurnMotorLeft), self.wheelVelocity2, 'Velocity2', userChoice)
                        
                            rightMotor = PID.standardPID(TargetAngle1, self.ComplementaryAngle, 'Angle1', userChoice)
                            leftMotor = PID.standardPID(TargetAngle2, self.ComplementaryAngle, 'Angle2', userChoice)
                        
                             # Sending the right values to the Sabertooth or the PWM controller
                            MotorsControlSignals.MotorsControl(rightMotor, leftMotor, userChoice)

                            LoopTimeEnd=time.time()
                            self.LoopTimeResult=LoopTimeEnd-LoopTimeStart
                        
                    except IOError, err:
                        print(IOError, err)
                        continue

        except KeyboardInterrupt:
                    InitProgram.StopProgram()

                    shared.set('MainRoutineStatus', "stopped")
                    shared.set('MainRoutine', "stopped")                    

                    if self.clearTimer==1:
                        if self.EncodersThread.isAlive():
                                self.EncodersThread.join(1)
                                self.EncodersThread.cancel()

                    if self.clearTimerMPU==1:  
                        if self.MPUThread.isAlive():
                                self.MPUThread.join(1)
                                self.MPUThread.cancel()

                    print("Unexpected error:\n", sys.exc_info()[0])
                    sys.exit('\n\nPROGRAM STOPPED!!!\n')
                    raise

    def main(self):
        if userChoice=='1':
                Sabertooth.CommunicationStart()
        if userChoice=='2':
                PWM.PWMStart()

        ProBot.StartAndStopMainRoutine()

if __name__ == '__main__':
    ProBot = ProBot()
    ProBot.main()

