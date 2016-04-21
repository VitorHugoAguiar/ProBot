#!/bin/sh
set -ex
sudo apt-get update

sudo sh -c \
"echo 'Package: *
Pin: release a=stable
Pin-Priority: 900

Package: *
Pin: release o=Debian
Pin-Priority: -10' > \
/etc/apt/preferences.d/sid;"

(sudo crontab -l ; echo "@reboot sleep 20 && python $(pwd -P)/WebClient.py $input_variable:$input_variable2") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(sudo crontab -l ; echo "@reboot sh $(pwd -P)/EnableEncoders.sh") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(sudo crontab -l ; echo "@reboot python $(pwd -P)/forward_ZMQ_Client.py") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(sudo crontab -l ; echo "@reboot python $(pwd -P)/RestartProgram_ZMQ.py") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -
(sudo crontab -l ; echo "@reboot python $(pwd -P)/RestartProgram.py") 2>&1 | grep -v "no crontab" | sort | uniq | crontab -

sudo rm -rf /etc/apt/apt.conf.d/02compress-indexes 

sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 43DDF224
sudo sh -c \
  "echo 'deb http://deb.machinekit.io/debian jessie main' > \
  /etc/apt/sources.list.d/machinekit.list"

sudo apt-get update
sudo apt-get install -y -t sid libczmq-dev
sudo apt-get install -y apt-show-versions
sudo apt-get install -y linux-image-3.8.13-xenomai-r78 
sudo apt-get install -y machinekit-xenomai machinekit-dev
