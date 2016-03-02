#!/usr/bin/python

# Python Standard Library Imports
import Adafruit_BBIO.UART as UART
import Adafruit_I2C as Adafruit_I2C
import Adafruit_BBIO.GPIO as GPIO
import sys
import math
import decimal
import time
import zmq
import mpu6050
import Kalman
import BatteryMonitor
import Controllers
import Encoders
import SocketCommunication
import ProBotConstants


print ('\nChoose the type of control of the ProBot:')
print ('\n1 - WebPage')
print ('2 - MidiDevice')
userChoice=input('\nYour choice is: ')

import Sabertooth

# Start the UART1
UART.setup("UART1")

# Initialization of classes from local files
mpu = mpu6050.MPU6050()
PC = Sabertooth.PacketizedCommunication()
KF = Kalman.KalmanFilter()
Battery = BatteryMonitor.BatteryVoltage()
PID = Controllers.PIDControllers()
Enc = Encoders.EncodersReadings()
Pub_Sub = SocketCommunication.publisher_and_subscriber()
Pconst = ProBotConstants.Constants()

UserChoice = Pub_Sub.userChoice(userChoice)

# Configuration the type of GPIO's
GPIO.setup(Pconst.RedLED, GPIO.OUT)
GPIO.setup(Pconst.GreenLED, GPIO.OUT)

class ProBot():
    def __init__(self, wheelPositionRef=0, VelocityRef=0, TurnMotorRight=0, TurnMotorLeft=0, id=0, value=0):
	self.wheelPositionRef = wheelPositionRef
        self.VelocityRef = VelocityRef
        self.TurnMotorRight = TurnMotorRight
        self.TurnMotorLeft = TurnMotorLeft
	self.id=id
	self.value=value

    def MPU6050_initialization(self):
        # MPU6050 initialization
	mpu.dmpInitialize()
	mpu.setDMPEnabled(True)
        mpu.initialize()

        # Testing connection
        if mpu.testConnection() is False:
            GPIO.output(Pconst.RedLED, GPIO.HIGH)
            GPIO.output(Pconst.GreenLED, GPIO.LOW)
        else:
            GPIO.output(Pconst.RedLED, GPIO.LOW)
            GPIO.output(Pconst.GreenLED, GPIO.HIGH)

    def SabertoothCommunication_initialization(self):
    	# Starting the communication with Sabertooth
        GPIO.output(Pconst.RedLED, GPIO.HIGH)
        PC.set_baud(PC.addr, PC.baud)
        time.sleep(3)									# Wait to stabilize the communication

        PC.stopAndReset()

        GPIO.output(Pconst.GreenLED, GPIO.HIGH)
        GPIO.output(Pconst.RedLED, GPIO.LOW)
        time.sleep(1.5)

    def Midi_device(self):
    	# Readings from the midi devices (Joystick, keyboard and UC33 )
        subscriber = Pub_Sub.subscriber()


        if subscriber is None:
            subscriber = 0
        else:
            midi_device, subscriberSplit2, subscriberSplit3  = subscriber.split()
            #print midi_device, subscriberSplit2, subscriberSplit3
            if midi_device=='UC33':
                self.id=float(decimal.Decimal(subscriberSplit2))
                self.value=float(decimal.Decimal(subscriberSplit3))
                return self.id, self.value

            if midi_device=='keyboard' or midi_device=='joystick' or midi_device=='msg':
                ForwardReverse = float(decimal.Decimal(subscriberSplit2))
                LeftRight = float(decimal.Decimal(subscriberSplit3))
                self.VelocityRef = float(ForwardReverse*1.3)
                self.TurnMotorRight = -float(LeftRight*40)
                self.TurnMotorLeft = float(LeftRight*40)
                #print ForwardReverse, LeftRight
                return  self.VelocityRef,  self.TurnMotorRight, self.TurnMotorLeft

    def mainRoutine(self):
    	# Starting the main program
        while True:
            try:
                #print userChoice
                LoopTime = time.time()

                # Verification of the voltage from the Beaglebone and motors batteries
                Battery.VoltageValue('BeagleBone')
                Battery.VoltageValue('Motors')

                # Read of the MPU6050 values
                AccAndGyr = mpu.MPU6050Values()
                AccXangle = AccAndGyr[0]
                GYRx = AccAndGyr[1]

                # Calculate the new x angle with the ofset of the calibration from the MPU6050
                ax_raw = AccXangle - Pconst.AccXangleAverage
                GYRx_raw = GYRx - Pconst.GYRxAverage
                # After the readings, we use the Kalman filter to eliminate the variations from the readings
                kalAngleX = KF.KalmanCalculate(ax_raw, GYRx_raw, LoopTime)

                #print kalAngleX
                # Readings from the encoders
                Encoders = Enc.EncodersValues()
                wheelVelocity = Encoders[0]
                wheelPosition = Encoders[1]
		wheelPosition1 = Encoders[2]
		wheelPosition2 = Encoders[3]

                Midi_device = ProBot.Midi_device()

                # With the values from the midi devices, we can calculate the outputs from the controllers
                PositionController1 = PID.standardPID(self.wheelPositionRef, wheelPosition1, self.id, self.value, 'Position1')
                PositionController2 = PID.standardPID(self.wheelPositionRef, wheelPosition2, self.id, self.value, 'Position2')
                VelocityController = PID.standardPID(self.VelocityRef, wheelVelocity, self.id, self.value, 'Velocity')
                AngleController = PID.standardPID(VelocityController, kalAngleX, self.id, self.value, 'Angle')
                rightMotor = float(AngleController+self.TurnMotorRight) #+PositionController2
                leftMotor = float(AngleController+self.TurnMotorLeft) #+PositionController1

                #publisher = Pub_Sub.publisher(wheelPosition1,wheelPosition2, wheelPosition)

                # Sending the values to the Sabertooth that is connected to the motors
                PC.drive(PC.addr, 1, int(rightMotor))
                PC.drive(PC.addr, 2, int(leftMotor))



            except:
                PC.stopAndReset()
                sys.exit('\n\nPROGRAM STOPPED!!!\n')
                raise

    def main(self):
        ProBot.MPU6050_initialization()
        ProBot.SabertoothCommunication_initialization()
        ProBot.mainRoutine()

if __name__ == '__main__':
    ProBot = ProBot()
    ProBot.main()
