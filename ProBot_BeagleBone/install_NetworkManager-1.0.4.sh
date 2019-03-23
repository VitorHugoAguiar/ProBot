#!/bin/sh
set -ex
sudo apt-get -y install intltool libdbus-glib-1-dev libgudev-1.0-dev libnl-3-dev libnl-route-3-dev libnl-genl-3-dev uuid-dev libreadline-dev libnss3-dev ppp-dev libndp-dev python-gi python-dbus libnewt-dev python-zmq python-smbus

tar xf NetworkManager-1.0.4.tar.xz
cd NetworkManager-1.0.4

sudo ./configure --prefix=/usr\
    --sysconfdir=/etc    \
    --localstatedir=/var \
    --with-nmtui         \
    --disable-ppp        \
    --with-systemdsystemunitdir=no \
    --docdir=/usr/share/doc/network-manager-1.0.4

sudo make && sudo make install

sudo cp network-manager /etc/init.d && sudo cp NetworkManager.conf /etc/NetworkManager && sudo update-rc.d network-manager defaults
