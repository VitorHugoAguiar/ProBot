#!/usr/bin/python

# Python Standart Library Imports
import smbus
import math
import sys
import time
import os
import memcache

# Local files
import ProBotConstantsFile

# Initialization of classes from local files
Pconst = ProBotConstantsFile.Constants()

shared = memcache.Client([('localhost', 15)], debug=0)

class mpu6050Class():
        
        def __init__(self):
                self.Angle_offset = 1.3 #-0.7
                self.GYR_offset = 0.1 #0.67

                # Power management registers
                self.power_mgmt_1 = 0x6b
                self.bus = smbus.SMBus(2) # or bus = smbus.SMBus(1) for Revision 2 boards        
                self.accel_scale_modifier = 16384.0 
                self.gyro_scale_modifier = 131.0 

                self.lastAccelerometerAngle = 0
                self.address = 0x68

                self.bus.write_byte_data(self.address, 0x1A, 0x80)

                # Now wake up the MPU6050 as it starts in sleep mode
                self.bus.write_byte_data(self.address, self.power_mgmt_1, 0x00)
                self.bus.write_byte_data(self.address, 0xA5, 0x5A)
                time.sleep(1)
                                
            
        def read_byte(self, adr):
                return self.bus.read_byte_data(self.address, adr)
                

        def read_word(self,adr):
                    high = self.bus.read_byte_data(self.address, adr)
                    low = self.bus.read_byte_data(self.address, adr+1)
                    val = (high << 8) + low
                    return val

        def read_word_2c(self,adr):
                    val = self.read_word(adr)
                    if (val >= 0x8000):
                        return -((65535 - val) + 1)
                    else:
                        return val

        def dist(self,a,b):
                    return math.sqrt((a*a)+(b*b))

        def get_y_rotation(self,x,y,z):
                    radians = math.atan2(x, self.dist(y,z))
                    return -math.degrees(radians)

        def get_x_rotation(self,x,y,z):
                    radians = math.atan2(y, self.dist(x,z))
                    return math.degrees(radians)


        def Calibration(self):
                import RestartProgramFile
                RestartProgram = RestartProgramFile.RestartProgramClass()

                print "\nProBot must be at 90 degrees!!!"
                                
                while True:
       
                        if shared.get('MainRoutine')=='"stop"':
                                shared.set('StartAndStop', "0")
                                shared.set('MainRoutineStatus', "stopped")
                                RestartProgram.RestartProgramRoutine()
                                
                        Pitch, gyro_xout_scaled=self.RollPitch()
                                                
                        if Pitch>-0.5 and Pitch<0.5:
                                break

                print ("\nBe carefull! The mainRoutine is going to START!")                                                
                
                shared.set('MainRoutineStatus', "started")
                return Pitch

        def RollPitch(self):        
                gyro_xout = self.read_word_2c(0x43)
                gyro_yout = self.read_word_2c(0x45)
                gyro_zout = self.read_word_2c(0x47)

                gyro_xout_scaled = gyro_xout/self.gyro_scale_modifier
                gyro_yout_scaled = gyro_yout/self.gyro_scale_modifier
                gyro_zout_scaled = gyro_zout/self.gyro_scale_modifier

                accel_xout = self.read_word_2c(0x3b)
                accel_yout = self.read_word_2c(0x3d)
                accel_zout = self.read_word_2c(0x3f)

                accel_xout_scaled = accel_xout /self.accel_scale_modifier
                accel_yout_scaled = accel_yout /self.accel_scale_modifier 
                accel_zout_scaled = accel_zout /self.accel_scale_modifier
                
                Pitch = self.get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)        
                
                Pitch += self.Angle_offset
                gyro_yout_scaled += self.GYR_offset
                                                
                return [Pitch, gyro_yout_scaled]
        
        
        def Complementary_filter(self, LoopTimeRatioSeg):
                Pitch, gyro_yout_scaled=self.RollPitch()

                # Complementary filter
                ComplementaryAngle = float (0.98 * (self.lastAccelerometerAngle + LoopTimeRatioSeg*gyro_yout_scaled) + (1 - 0.98) * Pitch)
                self.lastAccelerometerAngle = ComplementaryAngle
                                                
                return ComplementaryAngle
