#!/bin/sh
set -ex
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
