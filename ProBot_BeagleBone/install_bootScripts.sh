#!/bin/sh
set -ex
(sudo crontab -l ; echo "@reboot sh /home/machinekit/ProBot/ProBot_BeagleBone/EnableEncoders.sh") |sudo crontab -
(sudo crontab -l ; echo "@reboot sh /home/machinekit/ProBot/ProBot_BeagleBone/forward_ZMQ_Client") |sudo crontab -
(sudo crontab -l ; echo "@reboot sh /home/machinekit/ProBot/ProBot_BeagleBone/WebClient.py ws://139.162.157.96:9000") |sudo crontab -
