#!/bin/sh
set -ex
sudo apt-get install -y build-essential libssl-dev libffi-dev python-dev
sudo python get-pip.py
sudo pip install --upgrade setuptools
sudo pip install crossbar
