#!/bin/sh

sudo grep -q -F 'deb http://httpredir.debian.org/debian jessie-backports main' /etc/apt/sources.list || echo 'deb http://httpredir.debian.org/debian jessie-backports main' >> /etc/apt/sources.list
sudo grep -q -F 'deb http://httpredir.debian.org/debian stretch main'  /etc/apt/sources.list || echo 'deb http://httpredir.debian.org/debian stretch main' >> /etc/apt/sources.list

sudo grep -q -F 'APT::Default-Release "jessie";' /etc/apt/apt.conf.d/10apt || echo 'APT::Default-Release "jessie";' >> /etc/apt/apt.conf.d/10apt

sudo apt-get update
sudo apt-get install -y python-zmq python-tornado/jessie-backports salt-common/stretch

sudo apt-get install -y salt-minion/stretch
