#! /bin/sh
# first program to run to enable the readings from the encoders
sudo echo bone_eqep0 > /sys/devices/bone_capemgr.9/slots
sudo echo bone_eqep2b > /sys/devices/bone_capemgr.9/slots
