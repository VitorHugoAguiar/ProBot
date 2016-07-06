#! /bin/sh
sudo echo bone_eqep1 > /sys/devices/bone_capemgr.9/slots
sudo echo bone_eqep2 > /sys/devices/bone_capemgr.9/slots
sleep 10
sudo /sbin/iwconfig wlan2 power off

