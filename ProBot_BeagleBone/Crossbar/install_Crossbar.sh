#!/bin/sh
set -ex
sudo apt-get install -y build-essential libssl-dev libffi-dev python-dev
sudo python get-pip.py
sudo pip install --upgrade six
sudo pip install --upgrade setuptools
git clone https://github.com/crossbario/crossbar.git
cd crossbar
sudo pip install --upgrade -e .

