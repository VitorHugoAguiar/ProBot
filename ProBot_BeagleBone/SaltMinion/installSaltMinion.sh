#!/bin/sh

sudo echo 'deb http://httpredir.debian.org/debian jessie-backports main' >> /etc/apt/sources.list
sudo echo 'deb http://httpredir.debian.org/debian stretch main' >> /etc/apt/sources.list

sudo echo 'APT::Default-Release "jessie";' > /etc/apt/apt.conf.d/10apt

sudo apt-get update
sudo apt-get install python-zmq python-tornado/jessie-backports salt-common/stretch

sudo apt-get install salt-minion/stretch
