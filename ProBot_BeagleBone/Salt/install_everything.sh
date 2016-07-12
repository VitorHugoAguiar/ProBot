#!/bin/sh

export LANGUAGE=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_TYPE=en_US.UTF-8

(sudo crontab -l ; echo "@reboot sleep 20 && python $(pwd -P)/WebClient.py ws://192.168.10.236:9000") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(sudo crontab -l ; echo "@reboot sh $(pwd -P)/EnableEncoders.sh") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(sudo crontab -l ; echo "@reboot python $(pwd -P)/forward_ZMQ_Client.py") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -

cd ..
cd Machinekit
sudo sh install_Machinekit.sh


cd ..
cd Encoders
sudo sh install_Encoders.sh

cd ..
cd Crossbar
sudo sh install_Crossbar.sh

echo "BeagleBone is gonna shutdown.."

sudo shutdown -h now
