#!/bin/sh
set -ex
(sudo crontab -l ; echo "@reboot sleep 20 && /home/machinekit/ProBot/ProBot_BeagleBone/WebClient.py ws://139.162.157.96:9000") |sudo crontab -
(sudo crontab -l ; echo "@reboot sh /home/machinekit/ProBot/ProBot_BeagleBone/EnableEncoders.sh") |sudo crontab -
(sudo crontab -l ; echo "@reboot python /home/machinekit/ProBot/ProBot_BeagleBone/forward_ZMQ_Client.py") |sudo crontab -
(sudo crontab -l ; echo "@reboot python /home/machinekit/ProBot/ProBot_BeagleBone/RestartProgram_ZMQ.py") |sudo crontab -
(sudo crontab -l ; echo "@reboot python /home/machinekit/ProBot/ProBot_BeagleBone/RestartProgram.py") |sudo crontab -
